"""End-to-end defocus deblur + aberration correction with depth-conditioned simulation.

Trains an image restoration network on RGBD inputs: depth is estimated on-the-fly
from each RGB batch with Depth Anything V2 and used to drive depth-varying PSF
simulation (`render_mode="psf_patch_depth_interp"`). The normalized depth is also
fed as an extra input channel to the network so it can learn depth-aware deblurring.

Usage:
    python 8_defocus_deblur.py [--config configs/8_defocus_deblur.yml]

Reference:
    [1] Xinge Yang, Chuong Nguyen, Wenbin Wang, Kaizhang Kang, Wolfgang Heidrich, Xiaoxing Li. "Efficient Depth- and Spatially-Varying Image Simulation for Defocus Deblur." ICCV Workshop 2025.
    [2] Lihe Yang et al. "Depth Anything V2." NeurIPS 2024.
"""

import argparse
import logging
import os

import lpips
import torch
import torch.nn as nn
import torch.optim as optim
import yaml
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from tqdm import tqdm

from end2end_imaging import Camera
from end2end_imaging.network import (
    DepthAnythingV2Estimator,
    NAFNet,
    PerceptualLoss,
    PhotographicDataset,
)
from end2end_imaging.utils import batch_psnr, batch_ssim, setup_experiment

# Defaults preserve the historical behavior if a config omits the `loss:` block.
DEFAULT_LOSS_WEIGHTS = {"rgb_l1": 1.0, "rgb_perceptual": 0.5, "raw_l1": 1.0}

logger = logging.getLogger(__name__)


def config(config_path):
    """Load YAML config and bootstrap the experiment directory."""
    with open(config_path) as f:
        args = yaml.load(f, Loader=yaml.FullLoader)
    setup_experiment(args, script_path=__file__)
    return args


class Trainer:
    """Single-GPU trainer for depth-aware defocus deblur."""

    def __init__(self, args):
        self.args = args
        self.device = args["device"]

        self._init_camera(args["camera"])
        self._init_data(args["train_set"], args["eval_set"])
        self._init_depth_estimator(args["depth_estimator"])
        self._init_model(args["network"], args["train"])
        self._init_loss(args.get("loss", DEFAULT_LOSS_WEIGHTS))

    def _init_camera(self, camera_args):
        """Initialize the camera (lens + sensor)."""
        self.camera = Camera(
            lens_file=camera_args["lens_file"],
            sensor_file=camera_args["sensor_file"],
            device=self.device,
        )

    def _init_depth_estimator(self, depth_args):
        """Initialize the off-the-shelf depth estimator (frozen)."""
        self.depth_estimator = DepthAnythingV2Estimator(
            model_name=depth_args["model_name"],
            depth_min_mm=depth_args["depth_min_mm"],
            depth_max_mm=depth_args["depth_max_mm"],
            infer_size=depth_args.get("infer_size", 518),
            device=self.device,
        )

    def _init_model(self, net_args, train_args):
        """Initialize the image restoration model and optimizer."""
        expected_in, expected_out = Camera.output_channels(train_args["output_type"])
        if net_args["in_chan"] != expected_in or net_args["out_chan"] != expected_out:
            raise ValueError(
                f"network channel mismatch for output_type='{train_args['output_type']}': "
                f"expected in_chan={expected_in}, out_chan={expected_out}; "
                f"got in_chan={net_args['in_chan']}, out_chan={net_args['out_chan']}"
            )

        self.model = NAFNet(
            in_chan=net_args["in_chan"],
            out_chan=net_args["out_chan"],
            width=net_args["width"],
            middle_blk_num=net_args["middle_blk_num"],
            enc_blk_nums=net_args["enc_blk_nums"],
            dec_blk_nums=net_args["dec_blk_nums"],
        ).to(self.device)

        if net_args.get("ckpt_path"):
            state_dict = torch.load(net_args["ckpt_path"], map_location=self.device)
            self.model.load_state_dict(state_dict.get("model", state_dict))

        self.optimizer = optim.AdamW(self.model.parameters(), lr=float(train_args["lr"]))
        total_steps = train_args["epochs"] * len(self.train_loader)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=total_steps, eta_min=1e-7
        )

        self.render_mode = train_args["render_mode"]
        self.output_type = train_args["output_type"]

        self.l1_loss = nn.L1Loss()
        self.lpips_metric = lpips.LPIPS(net="alex").to(self.device)

    def _init_loss(self, loss_cfg):
        """Build the loss term registry from a ``{name: weight}`` config dict.

        Recognized keys:
            - ``rgb_l1``       : L1 in sRGB after ISP
            - ``rgb_perceptual``: VGG16-feature MSE in sRGB
            - ``raw_l1``       : L1 in the 4-channel RGGB output space

        Any key absent from ``loss_cfg`` (or set to 0) is skipped — no
        backbone is allocated for it. Add new term branches in
        :meth:`compute_loss` and register them by name here.
        """
        unknown = set(loss_cfg) - {"rgb_l1", "rgb_perceptual", "raw_l1"}
        if unknown:
            raise ValueError(f"Unknown loss term(s): {sorted(unknown)}")
        self.loss_weights = {k: float(v) for k, v in loss_cfg.items() if float(v) != 0.0}
        # Only build the VGG backbone if the perceptual term is actually used.
        if self.loss_weights.get("rgb_perceptual", 0.0) != 0.0:
            self.lpips_loss = PerceptualLoss(device=self.device)
        else:
            self.lpips_loss = None
        logger.info(f"Active loss terms: {self.loss_weights}")

    def _init_data(self, train_set_config, eval_set_config):
        """Initialize data loaders."""
        if train_set_config["dataset"] == "./datasets/DIV2K_train_HR" and not os.path.exists(
            "./datasets/DIV2K_train_HR"
        ):
            logger.info("Downloading DIV2K dataset...")
            from end2end_imaging.network.dataset import download_div2k
            download_div2k("./datasets")
        elif train_set_config["dataset"] == "./datasets/BSDS300/images/train" and not os.path.exists(
            "./datasets/BSDS300/images/train"
        ):
            logger.info("Downloading BSDS300 dataset...")
            from end2end_imaging.network.dataset import download_bsd300
            download_bsd300("./datasets")

        train_dataset = PhotographicDataset(
            train_set_config["dataset"], img_res=train_set_config["res"], is_train=True
        )
        val_dataset = PhotographicDataset(
            eval_set_config["dataset"], img_res=eval_set_config["res"], is_train=False
        )

        self.train_loader = DataLoader(
            train_dataset,
            batch_size=train_set_config["batch_size"],
            shuffle=True,
            num_workers=train_set_config["num_workers"],
            pin_memory=True,
        )
        self.val_loader = DataLoader(
            val_dataset,
            batch_size=eval_set_config["batch_size"],
            shuffle=False,
            num_workers=eval_set_config["num_workers"],
            pin_memory=True,
        )

    def add_depth(self, data_dict):
        """Estimate depth from the batch's RGB and attach it as ``data_dict["depth"]``."""
        img = data_dict["img"].to(self.device, non_blocking=True)
        data_dict["img"] = img
        # Depth estimator outputs positive mm (shape (B, 1, H, W)); detached graph (frozen).
        data_dict["depth"] = self.depth_estimator.estimate(img)
        return data_dict

    def forward(self, inputs):
        """Run the model forward pass. Outputs are unclamped to preserve gradients."""
        return self.model(inputs)

    def compute_loss(self, outputs, targets):
        """Compute the weighted sum of loss terms enabled in ``self.loss_weights``."""
        sensor = self.camera.sensor
        # Intentional ISP-domain augmentation: random gamma/CCM/AWB shared by outputs and targets per step.
        sensor.sample_augmentation()
        # Lazy: only compute the sRGB pair if any RGB-domain term is active.
        rgb_needed = any(k.startswith("rgb_") for k in self.loss_weights)
        if rgb_needed:
            # Clamp only for the gamma-bounded RGB path; raw_l1 keeps gradients on saturating pixels.
            outputs_rgb = sensor.process2rgb(outputs.clamp(0, 1), in_type="rggb")
            targets_rgb = sensor.process2rgb(targets, in_type="rggb")

        terms = {}
        if "rgb_l1" in self.loss_weights:
            terms["rgb_l1"] = self.loss_weights["rgb_l1"] * self.l1_loss(outputs_rgb, targets_rgb)
        if "rgb_perceptual" in self.loss_weights:
            terms["rgb_perceptual"] = self.loss_weights["rgb_perceptual"] * self.lpips_loss(outputs_rgb, targets_rgb)
        if "raw_l1" in self.loss_weights:
            terms["raw_l1"] = self.loss_weights["raw_l1"] * self.l1_loss(outputs, targets)

        loss = sum(terms.values())
        loss_dict = {k: v.item() for k, v in terms.items()}
        loss_dict["total_loss"] = loss.item()
        return loss, loss_dict

    def compute_metrics(self, outputs, targets):
        """Compute scalar PSNR / SSIM / LPIPS in sRGB space."""
        sensor = self.camera.sensor
        sensor.reset_augmentation()
        outputs_rgb = sensor.process2rgb(outputs, in_type="rggb")
        targets_rgb = sensor.process2rgb(targets, in_type="rggb")
        return {
            "psnr": batch_psnr(outputs_rgb, targets_rgb).mean().item(),
            "ssim": batch_ssim(outputs_rgb, targets_rgb),
            "lpips": self.lpips_metric(outputs_rgb * 2 - 1, targets_rgb * 2 - 1).mean().item(),
        }

    def _save_triplet(self, inputs, outputs, targets, path):
        """Save vertically stacked [input | output | target] in sRGB for visual inspection."""
        sensor = self.camera.sensor
        sensor.reset_augmentation()
        inputs_rgb = sensor.process2rgb(inputs[:, :4, :, :], in_type="rggb")
        outputs_rgb = sensor.process2rgb(outputs[:, :4, :, :], in_type="rggb")
        targets_rgb = sensor.process2rgb(targets[:, :4, :, :], in_type="rggb")
        save_image(torch.cat([inputs_rgb, outputs_rgb, targets_rgb], dim=2), path)

    def train_epoch(self, epoch):
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        log_every = self.args["train"]["log_every_n_steps"]
        epochs = self.args["train"]["epochs"]

        for i, data_dict in enumerate(tqdm(self.train_loader)):
            data_dict = self.add_depth(data_dict)
            inputs, targets = self.camera.render(
                data_dict, render_mode=self.render_mode, output_type=self.output_type
            )

            outputs = self.forward(inputs)
            loss, loss_dict = self.compute_loss(outputs, targets)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()

            total_loss += loss_dict["total_loss"]

            if (i + 1) % log_every == 0:
                logger.info(
                    f"Epoch: {epoch + 1}/{epochs}, "
                    f"Batch: {i + 1}/{len(self.train_loader)}, "
                    f"Loss: {loss_dict['total_loss']:.4f}"
                )
                self._save_triplet(
                    inputs,
                    outputs.detach().clamp(0, 1),
                    targets,
                    f"{self.args['result_dir']}/train_epoch{epoch}_batch{i}.png",
                )

        return total_loss / len(self.train_loader)

    @torch.no_grad()
    def validate(self, epoch):
        """Run validation."""
        self.model.eval()
        val_psnr, val_ssim, val_lpips, val_samples = 0.0, 0.0, 0.0, 0

        for i, data_dict in enumerate(tqdm(self.val_loader, desc="Validating")):
            data_dict = self.add_depth(data_dict)
            inputs, targets = self.camera.render(
                data_dict, render_mode=self.render_mode, output_type=self.output_type
            )

            outputs = self.forward(inputs).clamp(0, 1)
            metrics = self.compute_metrics(outputs, targets)

            bs = inputs.size(0)
            val_psnr += metrics["psnr"] * bs
            val_ssim += metrics["ssim"] * bs
            val_lpips += metrics["lpips"] * bs
            val_samples += bs

            if i == 0:
                self._save_triplet(
                    inputs, outputs, targets,
                    f"{self.args['result_dir']}/val_epoch{epoch}.png",
                )

        return {
            "val_psnr": val_psnr / val_samples,
            "val_ssim": val_ssim / val_samples,
            "val_lpips": val_lpips / val_samples,
        }

    def save_checkpoint(self, epoch):
        """Save full training state so a run can be resumed."""
        torch.save(
            {
                "model": self.model.state_dict(),
                "optimizer": self.optimizer.state_dict(),
                "scheduler": self.scheduler.state_dict(),
                "epoch": epoch,
            },
            f"{self.args['result_dir']}/network_epoch{epoch}.pth",
        )

    def train(self):
        """Run the full training process."""
        epochs = self.args["train"]["epochs"]
        for epoch in range(epochs):
            train_loss = self.train_epoch(epoch)
            logger.info(f"Epoch {epoch + 1}/{epochs} - Loss: {train_loss:.4f}")

            if (epoch + 1) % self.args["train"]["eval_every_n_epochs"] == 0:
                self.save_checkpoint(epoch + 1)
                val_metrics = self.validate(epoch + 1)
                logger.info(
                    f"  Val PSNR: {val_metrics['val_psnr']:.2f} dB, "
                    f"SSIM: {val_metrics['val_ssim']:.4f}, "
                    f"LPIPS: {val_metrics['val_lpips']:.4f}"
                )
                logger.info("-" * 50)

        self.save_checkpoint(epochs)
        logger.info("Training completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--config",
        default="configs/8_defocus_deblur.yml",
        help="Path to YAML config file.",
    )
    cli_args = parser.parse_args()

    args = config(cli_args.config)
    trainer = Trainer(args)
    trainer.train()

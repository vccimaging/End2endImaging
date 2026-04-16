"""End-to-end computational photography: train an image restoration network with physically accurate image simulation.

Usage:
    python 7_comp_photography.py

Reference:
    [1] Xinge Yang, Chuong Nguyen, Wenbin Wang, Kaizhang Kang, Wolfgang Heidrich, Xiaoxing Li. "Efficient Depth- and Spatially-Varying Image Simulation for Defocus Deblur." ICCV Workshop 2025.
"""

import logging
import os
import random
import shutil
import string
from datetime import datetime

import lpips
import torch
import torch.nn as nn
import torch.optim as optim
import yaml
from torch.utils.data import DataLoader
from torchvision.utils import save_image
from tqdm import tqdm

from end2end_imaging import Camera
from end2end_imaging.network import NAFNet, PerceptualLoss, PhotographicDataset
from end2end_imaging.utils import batch_psnr, batch_ssim, set_logger, set_seed


def config():
    """Load and prepare configuration."""
    with open("configs/7_comp_photography.yml") as f:
        args = yaml.load(f, Loader=yaml.FullLoader)

    # Set up result directory
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(4))
    current_time = datetime.now().strftime("%m%d-%H%M%S")
    exp_name = f"{current_time}-Comp-Photography-{random_string}"

    result_dir = f"./results/{exp_name}"
    os.makedirs(result_dir, exist_ok=True)
    args["result_dir"] = result_dir

    # Set random seed
    if args["seed"] is None:
        args["seed"] = random.randint(0, 1000)
    set_seed(args["seed"])

    # Configure logging
    set_logger(result_dir)
    logging.info(f"Experiment: {args['exp_name']}")

    # Configure device
    if torch.cuda.is_available():
        args["device"] = torch.device("cuda")
        logging.info(f"Using {torch.cuda.get_device_name(0)}")
    else:
        args["device"] = torch.device("cpu")
        logging.info("Using CPU")

    # Save config and code
    with open(f"{result_dir}/config.yml", "w") as f:
        yaml.dump(args, f)
    shutil.copy("7_comp_photography.py", f"{result_dir}/7_comp_photography.py")

    return args


class Trainer:
    """Single-GPU trainer for end-to-end computational photography."""

    def __init__(self, args):
        self.args = args
        self.device = args["device"]

        # Initialize camera, dataset, model
        self._init_camera(args["camera"])
        self._init_data(args["train_set"], args["eval_set"])
        self._init_model(args["network"], args["train"])

    def _init_camera(self, camera_args):
        """Initialize the camera (lens + sensor)."""
        self.camera = Camera(
            lens_file=camera_args["lens_file"],
            sensor_file=camera_args["sensor_file"],
            device=self.device,
        )

    def _init_model(self, net_args, train_args):
        """Initialize the image restoration model and optimizer."""
        self.model = NAFNet(
            in_chan=net_args["in_chan"],
            out_chan=net_args["out_chan"],
            width=net_args["width"],
            middle_blk_num=net_args["middle_blk_num"],
            enc_blk_nums=net_args["enc_blk_nums"],
            dec_blk_nums=net_args["dec_blk_nums"],
        ).to(self.device)

        # Load checkpoint if provided
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

        # Loss functions
        self.l1_loss = nn.L1Loss()
        self.lpips_loss = PerceptualLoss(device=self.device)

        # Evaluation metric
        self.lpips_metric = lpips.LPIPS(net="alex").to(self.device)

    def _init_data(self, train_set_config, eval_set_config):
        """Initialize data loaders."""
        # Download dataset if not exists
        if train_set_config["dataset"] == "./datasets/DIV2K_train_HR" and not os.path.exists(
            "./datasets/DIV2K_train_HR"
        ):
            print("Downloading DIV2K dataset...")
            from end2end_imaging.network.dataset import download_div2k
            download_div2k("./datasets")
        elif train_set_config["dataset"] == "./datasets/BSDS300/images/train" and not os.path.exists(
            "./datasets/BSDS300/images/train"
        ):
            print("Downloading BSDS300 dataset...")
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

    def compute_loss(self, inputs, targets):
        """Compute loss between model outputs and targets."""
        outputs = self.model(inputs).clamp(0, 1)

        # Convert to RGB (with random ISP augmentation) for loss computation
        sensor = self.camera.sensor
        sensor.sample_augmentation()
        outputs_rgb = sensor.process2rgb(outputs, in_type="rggb")
        targets_rgb = sensor.process2rgb(targets, in_type="rggb")

        # Loss in RGB space (pixel + perceptual)
        l1_loss = self.l1_loss(outputs_rgb, targets_rgb)
        perceptual_loss = self.lpips_loss(outputs_rgb, targets_rgb)
        rgb_loss = l1_loss + 0.5 * perceptual_loss

        # Loss in RAW space
        raw_loss = self.l1_loss(outputs, targets)

        loss = rgb_loss + raw_loss
        loss_dict = {
            "rgb_loss": rgb_loss.item(),
            "raw_loss": raw_loss.item(),
            "total_loss": loss.item(),
        }
        return loss, loss_dict

    def compute_metrics(self, outputs, targets):
        """Compute evaluation metrics (PSNR, SSIM, LPIPS)."""
        sensor = self.camera.sensor
        sensor.reset_augmentation()
        outputs_rgb = sensor.process2rgb(outputs, in_type="rggb")
        targets_rgb = sensor.process2rgb(targets, in_type="rggb")

        return {
            "psnr": batch_psnr(outputs_rgb, targets_rgb),
            "ssim": batch_ssim(outputs_rgb, targets_rgb),
            "lpips": self.lpips_metric(outputs_rgb * 2 - 1, targets_rgb * 2 - 1),
        }

    def train_epoch(self, epoch):
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0

        for i, data_dict in enumerate(tqdm(self.train_loader)):
            # Simulate camera capture (lens aberration + sensor noise)
            inputs, targets = self.camera.render(
                data_dict, render_mode=self.render_mode, output_type=self.output_type
            )

            # Forward pass and compute loss
            loss, loss_dict = self.compute_loss(inputs, targets)

            # Backward and optimize
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()

            total_loss += loss_dict["total_loss"]

            # Log progress
            if (i + 1) % self.args["train"]["log_every_n_steps"] == 0:
                print(
                    f"Epoch: {epoch + 1}/{self.args['train']['epochs']}, "
                    f"Batch: {i + 1}/{len(self.train_loader)}, "
                    f"Loss: {loss_dict['total_loss']:.4f}"
                )

                # Save sample images
                with torch.no_grad():
                    outputs = self.model(inputs)
                    sensor = self.camera.sensor
                    sensor.reset_augmentation()
                    inputs_rgb = sensor.process2rgb(inputs[:, :4, :, :], in_type="rggb")
                    outputs_rgb = sensor.process2rgb(outputs.detach()[:, :4, :, :], in_type="rggb")
                    targets_rgb = sensor.process2rgb(targets[:, :4, :, :], in_type="rggb")
                    save_image(
                        torch.cat([inputs_rgb, outputs_rgb, targets_rgb], dim=2),
                        f"{self.args['result_dir']}/train_epoch{epoch}_batch{i}.png",
                    )

        return total_loss / len(self.train_loader)

    @torch.no_grad()
    def validate(self, epoch):
        """Run validation."""
        self.model.eval()
        val_psnr, val_ssim, val_lpips, val_samples = 0.0, 0.0, 0.0, 0

        for i, data_dict in enumerate(tqdm(self.val_loader, desc="Validating")):
            inputs, targets = self.camera.render(
                data_dict, render_mode=self.render_mode, output_type=self.output_type
            )

            outputs = self.model(inputs).clamp(0, 1)
            metrics = self.compute_metrics(outputs, targets)

            bs = inputs.size(0)
            val_psnr += metrics["psnr"] * bs
            val_ssim += metrics["ssim"] * bs
            val_lpips += metrics["lpips"] * bs
            val_samples += bs

            # Save sample validation images
            if i == 0:
                sensor = self.camera.sensor
                sensor.reset_augmentation()
                inputs_rgb = sensor.process2rgb(inputs[:, :4, :, :], in_type="rggb")
                outputs_rgb = sensor.process2rgb(outputs[:, :4, :, :], in_type="rggb")
                targets_rgb = sensor.process2rgb(targets[:, :4, :, :], in_type="rggb")
                save_image(
                    torch.cat([inputs_rgb, outputs_rgb, targets_rgb], dim=2),
                    f"{self.args['result_dir']}/val_epoch{epoch}.png",
                )

        return {
            "val_psnr": val_psnr / val_samples,
            "val_ssim": val_ssim / val_samples,
            "val_lpips": val_lpips / val_samples,
        }

    def save_checkpoint(self, epoch):
        """Save model checkpoint."""
        torch.save(self.model.state_dict(), f"{self.args['result_dir']}/network_epoch{epoch}.pth")

    def train(self):
        """Run the full training process."""
        for epoch in range(self.args["train"]["epochs"]):
            train_loss = self.train_epoch(epoch)
            print(f"Epoch {epoch + 1}/{self.args['train']['epochs']} — Loss: {train_loss:.4f}")

            # Validate and save checkpoint
            if (epoch + 1) % self.args["train"]["eval_every_n_epochs"] == 0:
                self.save_checkpoint(epoch + 1)
                val_metrics = self.validate(epoch + 1)
                print(
                    f"  Val PSNR: {val_metrics['val_psnr']:.2f} dB, "
                    f"SSIM: {val_metrics['val_ssim']:.4f}, "
                    f"LPIPS: {val_metrics['val_lpips']:.4f}"
                )
                print("-" * 50)

        self.save_checkpoint(self.args["train"]["epochs"])
        print("Training completed!")


if __name__ == "__main__":
    args = config()
    trainer = Trainer(args)
    trainer.train()

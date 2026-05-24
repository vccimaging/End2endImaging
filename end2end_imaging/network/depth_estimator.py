"""Depth estimation wrapper for end-to-end training.

Uses Depth Anything V2 (from Hugging Face Transformers) to estimate per-pixel
depth from sRGB inputs, then maps the model's relative inverse-depth output to
positive metric depth (mm) in a configured scene range. The metric depth is the
contract expected by :meth:`Camera.render` with ``render_mode="psf_patch_depth_interp"``.
"""

import logging

import torch
import torch.nn.functional as F


logger = logging.getLogger(__name__)


_IMAGENET_MEAN = (0.485, 0.456, 0.406)
_IMAGENET_STD = (0.229, 0.224, 0.225)
_DA_V2_PATCH = 14


class DepthAnythingV2Estimator:
    """Estimate metric depth (mm) from sRGB batches using Depth Anything V2.

    The HF model returns relative inverse depth (disparity-like, higher = closer).
    We normalize per-image to ``[0, 1]`` and map linearly **in disparity space**
    into the physical range ``[depth_min_mm, depth_max_mm]``. Because depth is
    the reciprocal of disparity, equal steps in normalized disparity correspond
    to much smaller depth steps near the camera than far from it — so near-field
    depths are densely sampled and far-field depths are coarsely sampled, which
    matches how defocus PSF spreads change with depth.

    Args:
        model_name: HuggingFace model id, e.g. ``"depth-anything/Depth-Anything-V2-Small-hf"``.
        depth_min_mm: Near-plane distance (closest sampled depth).
        depth_max_mm: Far-plane distance (farthest sampled depth).
        infer_size: Side length (must be a multiple of 14) used for the DA-V2 forward pass.
        device: Compute device. Defaults to CUDA if available.
    """

    def __init__(
        self,
        model_name="depth-anything/Depth-Anything-V2-Small-hf",
        depth_min_mm=300.0,
        depth_max_mm=5000.0,
        infer_size=518,
        device=None,
    ):
        from transformers import AutoModelForDepthEstimation

        if infer_size % _DA_V2_PATCH != 0:
            raise ValueError(
                f"infer_size must be a multiple of {_DA_V2_PATCH}; got {infer_size}"
            )

        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.depth_min_mm = float(depth_min_mm)
        self.depth_max_mm = float(depth_max_mm)
        self.infer_size = int(infer_size)

        logger.info(f"Loading depth estimator: {model_name}")
        self.model = AutoModelForDepthEstimation.from_pretrained(model_name).to(self.device).eval()
        for p in self.model.parameters():
            p.requires_grad = False

        mean = torch.tensor(_IMAGENET_MEAN, device=self.device).view(1, 3, 1, 1)
        std = torch.tensor(_IMAGENET_STD, device=self.device).view(1, 3, 1, 1)
        self._mean = mean
        self._std = std

    @torch.no_grad()
    def estimate(self, rgb):
        """Estimate per-pixel metric depth (mm) for a batch.

        Args:
            rgb: sRGB tensor of shape ``(B, 3, H, W)`` with values in ``[0, 1]``.

        Returns:
            depth_mm: tensor of shape ``(B, 1, H, W)``, positive mm in
                ``[depth_min_mm, depth_max_mm]``.
        """
        if rgb.dim() != 4 or rgb.shape[1] != 3:
            raise ValueError(f"Expected (B, 3, H, W) sRGB tensor; got {tuple(rgb.shape)}")

        B, _, H, W = rgb.shape
        rgb = rgb.to(self.device)
        rgb_norm = (rgb - self._mean) / self._std
        rgb_resized = F.interpolate(
            rgb_norm, size=(self.infer_size, self.infer_size), mode="bilinear", align_corners=False
        )

        outputs = self.model(pixel_values=rgb_resized)
        # predicted_depth is (B, h, w) inverse-depth at the model's grid.
        disp = outputs.predicted_depth.unsqueeze(1)
        disp = F.interpolate(disp, size=(H, W), mode="bilinear", align_corners=False)

        # Per-image min-max normalization → [0, 1] disparity. Higher = closer.
        disp_min = disp.amin(dim=(2, 3), keepdim=True)
        disp_max = disp.amax(dim=(2, 3), keepdim=True)
        disp_norm = (disp - disp_min) / (disp_max - disp_min + 1e-8)

        # Linear interpolation in disparity (1/depth) space, then invert to get depth.
        # disp_norm=1 (closest) → 1/depth_min ; disp_norm=0 (farthest) → 1/depth_max.
        disp_near = 1.0 / self.depth_min_mm
        disp_far = 1.0 / self.depth_max_mm
        disp_phys = disp_far + disp_norm * (disp_near - disp_far)
        depth_mm = 1.0 / disp_phys
        return depth_mm

"""Demosaic, or Color Filter Array (CFA)."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Demosaic(nn.Module):
    """Demosaic, or Color Filter Array (CFA).

    Converts a Bayer pattern image to a full RGB image by interpolating
    missing color values at each pixel location.

    Supported Bayer patterns (the four common 2x2 layouts):
        - "rggb", "bggr", "grbg", "gbrg"

    Supported methods:
        - "bilinear": Simple bilinear interpolation (fast, lower quality)
        - "malvar": Malvar-He-Cutler high-quality gradient-corrected interpolation

    The interpolation kernels are pattern-independent; only the per-pixel color
    sampling masks (built from ``self.bayer_pattern``) differ between patterns.

    Reference:
        [1] Malvar, He, Cutler. "High-Quality Linear Interpolation for Demosaicing
            of Bayer-Patterned Color Images", ICASSP 2004.
    """

    # 2x2 Bayer tile offsets (row, col) for each color-filter position.
    # ``gr`` is the green pixel that shares a row with red; ``gb`` is the green
    # pixel that shares a row with blue. Red and blue always sit on opposite
    # corners of the 2x2 tile, with the two greens on the other diagonal.
    _BAYER_OFFSETS = {
        "rggb": {"r": (0, 0), "gr": (0, 1), "gb": (1, 0), "b": (1, 1)},
        "bggr": {"r": (1, 1), "gr": (1, 0), "gb": (0, 1), "b": (0, 0)},
        "grbg": {"r": (0, 1), "gr": (0, 0), "gb": (1, 1), "b": (1, 0)},
        "gbrg": {"r": (1, 0), "gr": (1, 1), "gb": (0, 0), "b": (0, 1)},
    }

    def __init__(self, bayer_pattern="rggb", method="malvar"):
        """Initialize demosaic.

        Args:
            bayer_pattern: Bayer pattern, one of "rggb", "bggr", "grbg", "gbrg".
            method: Demosaic method, "bilinear" or "malvar".

        Raises:
            ValueError: If ``bayer_pattern`` is not one of the supported patterns.
        """
        super().__init__()

        bayer_pattern = bayer_pattern.lower()
        if bayer_pattern not in self._BAYER_OFFSETS:
            raise ValueError(
                f"Unsupported bayer_pattern: {bayer_pattern!r}. "
                f"Supported patterns: {sorted(self._BAYER_OFFSETS)}."
            )

        self.bayer_pattern = bayer_pattern
        self.method = method

        # Pre-compute Malvar kernels if using that method
        if method == "malvar":
            self._init_malvar_kernels()

    def _init_malvar_kernels(self):
        """Initialize Malvar-He-Cutler demosaic kernels.

        These 5x5 kernels perform gradient-corrected bilinear interpolation
        to reduce color artifacts at edges.

        Reference:
            Malvar, He, Cutler. "High-Quality Linear Interpolation for Demosaicing
            of Bayer-Patterned Color Images", ICASSP 2004.
            https://www.ipol.im/pub/art/2011/g_mhcd/
        """
        # Kernel for G at R locations and G at B locations (same kernel)
        # This interpolates Green at Red or Blue pixel positions
        kernel_g_at_rb = torch.tensor([
            [ 0,  0, -1,  0,  0],
            [ 0,  0,  2,  0,  0],
            [-1,  2,  4,  2, -1],
            [ 0,  0,  2,  0,  0],
            [ 0,  0, -1,  0,  0],
        ], dtype=torch.float32) / 8.0

        # Kernel for R at G in R row, B column (Gr positions)
        # and B at G in B row, R column (Gb positions)
        kernel_rb_at_g_rbcol = torch.tensor([
            [ 0,  0,  0.5,  0,  0],
            [ 0, -1,  0,   -1,  0],
            [-1,  4,  5,    4, -1],
            [ 0, -1,  0,   -1,  0],
            [ 0,  0,  0.5,  0,  0],
        ], dtype=torch.float32) / 8.0

        # Kernel for R at G in B row, R column (Gb positions)
        # and B at G in R row, B column (Gr positions)
        kernel_rb_at_g_rbrow = torch.tensor([
            [ 0,  0, -1,  0,  0],
            [ 0, -1,  4, -1,  0],
            [0.5, 0,  5,  0, 0.5],
            [ 0, -1,  4, -1,  0],
            [ 0,  0, -1,  0,  0],
        ], dtype=torch.float32) / 8.0

        # Kernel for R at B locations and B at R locations
        kernel_rb_at_br = torch.tensor([
            [ 0,  0, -1.5,  0,   0],
            [ 0,  2,  0,    2,   0],
            [-1.5, 0, 6,    0, -1.5],
            [ 0,  2,  0,    2,   0],
            [ 0,  0, -1.5,  0,   0],
        ], dtype=torch.float32) / 8.0

        # Register as buffers (moved to device with model)
        self.register_buffer("malvar_g_at_rb", kernel_g_at_rb.view(1, 1, 5, 5))
        self.register_buffer("malvar_rb_at_g_rbcol", kernel_rb_at_g_rbcol.view(1, 1, 5, 5))
        self.register_buffer("malvar_rb_at_g_rbrow", kernel_rb_at_g_rbrow.view(1, 1, 5, 5))
        self.register_buffer("malvar_rb_at_br", kernel_rb_at_br.view(1, 1, 5, 5))

    def _bayer_masks(self, H, W, device, dtype):
        """Build per-color sampling masks for the configured Bayer pattern.

        Args:
            H (int): Image height.
            W (int): Image width.
            device: Target device for the masks.
            dtype: Target dtype for the masks.

        Returns:
            tuple: ``(r_mask, gr_mask, gb_mask, b_mask)``, each of shape
            ``[1, 1, H, W]`` with ones at the positions sampled by that color
            (``gr``: green in the red row, ``gb``: green in the blue row).
        """
        offsets = self._BAYER_OFFSETS[self.bayer_pattern]
        masks = {}
        for name, (r0, c0) in offsets.items():
            mask = torch.zeros((1, 1, H, W), device=device, dtype=dtype)
            mask[:, :, r0::2, c0::2] = 1
            masks[name] = mask
        return masks["r"], masks["gr"], masks["gb"], masks["b"]

    def _malvar_demosaic(self, bayer):
        """Malvar-He-Cutler high-quality demosaic method (differentiable).

        Uses gradient-corrected 5x5 kernels to interpolate missing colors
        while preserving edges better than simple bilinear interpolation. The
        kernels are fixed; the configured ``self.bayer_pattern`` only selects
        which pixels are treated as R / Gr / Gb / B via the sampling masks.

        Args:
            bayer (torch.Tensor): Input tensor of shape [B, 1, H, W], data range [0, 1].

        Returns:
            raw_rgb (torch.Tensor): Output tensor of shape [B, 3, H, W], data range [0, 1].
        """
        B, C, H, W = bayer.shape

        # Pad the bayer image for 5x5 kernel (2 pixels on each side)
        bayer_pad = F.pad(bayer, (2, 2, 2, 2), mode="reflect")

        # Per-color sampling masks for the configured Bayer pattern
        r_mask, gr_mask, gb_mask, b_mask = self._bayer_masks(
            H, W, bayer.device, bayer.dtype
        )
        g_mask = gr_mask + gb_mask  # All green positions

        # Apply Malvar kernels via convolution (kernels follow the input device/dtype).
        # G at R and B locations
        g_at_rb = F.conv2d(bayer_pad, self.malvar_g_at_rb.to(bayer), padding=0)

        # R at Gr locations (R row, B col) - use horizontal kernel
        r_at_gr = F.conv2d(bayer_pad, self.malvar_rb_at_g_rbcol.to(bayer), padding=0)

        # R at Gb locations (B row, R col) - use vertical kernel
        r_at_gb = F.conv2d(bayer_pad, self.malvar_rb_at_g_rbrow.to(bayer), padding=0)

        # R at B locations
        r_at_b = F.conv2d(bayer_pad, self.malvar_rb_at_br.to(bayer), padding=0)

        # B at Gr locations (R row, B col) - use vertical kernel
        b_at_gr = F.conv2d(bayer_pad, self.malvar_rb_at_g_rbrow.to(bayer), padding=0)

        # B at Gb locations (B row, R col) - use horizontal kernel
        b_at_gb = F.conv2d(bayer_pad, self.malvar_rb_at_g_rbcol.to(bayer), padding=0)

        # B at R locations
        b_at_r = F.conv2d(bayer_pad, self.malvar_rb_at_br.to(bayer), padding=0)

        # Assemble the RGB channels
        # Red channel: R at R (original) + R at Gr + R at Gb + R at B
        red = (bayer * r_mask +
               r_at_gr * gr_mask +
               r_at_gb * gb_mask +
               r_at_b * b_mask)

        # Green channel: G at Gr + G at Gb (original) + G at R + G at B
        green = (bayer * g_mask +
                 g_at_rb * r_mask +
                 g_at_rb * b_mask)

        # Blue channel: B at B (original) + B at Gr + B at Gb + B at R
        blue = (bayer * b_mask +
                b_at_gr * gr_mask +
                b_at_gb * gb_mask +
                b_at_r * r_mask)

        # Stack channels
        raw_rgb = torch.cat([red, green, blue], dim=1)

        # Clamp to valid range (kernel interpolation can exceed [0, 1])
        raw_rgb = torch.clamp(raw_rgb, 0.0, 1.0)

        return raw_rgb

    def _bilinear_demosaic(self, bayer):
        """Bilinear interpolation demosaic method.

        Builds sparse single-color planes (using the pattern-aware sampling
        masks) and convolves each with a bilinear interpolation kernel. Applied
        to a sparse Bayer plane, these kernels reproduce the standard 2-neighbor
        and 4-neighbor averages while passing through the originally sampled
        pixels unchanged. The kernels are pattern-independent.

        Args:
            bayer (torch.Tensor): Input tensor of shape [B, 1, H, W], data range [0, 1].

        Returns:
            raw_rgb (torch.Tensor): Output tensor of shape [B, 3, H, W], data range [0, 1].
        """
        B, C, H, W = bayer.shape

        # Per-color sampling masks for the configured Bayer pattern
        r_mask, gr_mask, gb_mask, b_mask = self._bayer_masks(
            H, W, bayer.device, bayer.dtype
        )
        g_mask = gr_mask + gb_mask

        # Sparse single-color planes (zero where the color is not sampled)
        r_plane = bayer * r_mask
        g_plane = bayer * g_mask
        b_plane = bayer * b_mask

        # Bilinear interpolation kernels for sparse Bayer planes.
        # R/B sit on a regular grid, so a full 3x3 bilinear kernel reproduces the
        # 2-neighbor (edge) and 4-neighbor (diagonal) averages. Green sits on a
        # quincunx, so it only needs the 4 orthogonal neighbors.
        kernel_rb = torch.tensor(
            [
                [0.25, 0.5, 0.25],
                [0.5, 1.0, 0.5],
                [0.25, 0.5, 0.25],
            ],
            device=bayer.device,
            dtype=bayer.dtype,
        ).view(1, 1, 3, 3)
        kernel_g = torch.tensor(
            [
                [0.0, 0.25, 0.0],
                [0.25, 1.0, 0.25],
                [0.0, 0.25, 0.0],
            ],
            device=bayer.device,
            dtype=bayer.dtype,
        ).view(1, 1, 3, 3)

        red = F.conv2d(F.pad(r_plane, (1, 1, 1, 1), mode="reflect"), kernel_rb)
        green = F.conv2d(F.pad(g_plane, (1, 1, 1, 1), mode="reflect"), kernel_g)
        blue = F.conv2d(F.pad(b_plane, (1, 1, 1, 1), mode="reflect"), kernel_rb)

        raw_rgb = torch.cat([red, green, blue], dim=1)
        return raw_rgb

    def forward(self, bayer):
        """Demosaic a Bayer pattern image to RGB.

        Args:
            bayer: Input tensor of shape [1, H, W] or [B, 1, H, W].

        Returns:
            raw_rgb: Output tensor of shape [3, H, W] or [B, 3, H, W],
                matching the dimensionality of the input.

        Raises:
            ValueError: If ``self.method`` is not "bilinear" or "malvar".
        """
        if bayer.dim() == 3:
            bayer = bayer.unsqueeze(0)
            batch_dim = False
        else:
            batch_dim = True

        if self.method == "bilinear":
            raw_rgb = self._bilinear_demosaic(bayer)
        elif self.method == "malvar":
            raw_rgb = self._malvar_demosaic(bayer)
        else:
            raise ValueError(f"Invalid demosaic method: {self.method}. Use 'bilinear' or 'malvar'.")

        if not batch_dim:
            raw_rgb = raw_rgb.squeeze(0)

        return raw_rgb

    def reverse(self, img):
        """Inverse demosaic from RAW RGB to RAW Bayer.

        Samples one channel per pixel according to ``self.bayer_pattern``, the
        exact inverse of the mosaicing implied by :meth:`forward` (each color is
        re-read from the channel it was originally sampled into).

        Args:
            img (torch.Tensor): RAW RGB image, shape [3, H, W] or [B, 3, H, W], data range [0, 1].

        Returns:
            torch.Tensor: Bayer image, shape [1, H, W] or [B, 1, H, W], data range [0, 1].

        Raises:
            ValueError: If the input does not have 3 or 4 dimensions, or if the
                channel dimension is not 3.
        """
        if img.ndim == 3:
            # Input shape: [3, H, W]
            batch_dim = False
            C, H, W = img.shape
        elif img.ndim == 4:
            # Input shape: [B, 3, H, W]
            batch_dim = True
            B, C, H, W = img.shape
        else:
            raise ValueError(
                "Input image must have 3 or 4 dimensions corresponding to [3, H, W] or [B, 3, H, W]."
            )

        if C != 3:
            raise ValueError("Input image must have 3 channels corresponding to RGB.")

        offsets = self._BAYER_OFFSETS[self.bayer_pattern]
        # (channel index, (row offset, col offset)) for each sampled position.
        # R from the red channel, both greens from the green channel, B from blue.
        samples = [
            (0, offsets["r"]),
            (1, offsets["gr"]),
            (1, offsets["gb"]),
            (2, offsets["b"]),
        ]

        if batch_dim:
            bayer = torch.zeros((B, 1, H, W), dtype=img.dtype, device=img.device)
            for ch, (r0, c0) in samples:
                bayer[:, 0, r0::2, c0::2] = img[:, ch, r0::2, c0::2]
        else:
            bayer = torch.zeros((1, H, W), dtype=img.dtype, device=img.device)
            for ch, (r0, c0) in samples:
                bayer[0, r0::2, c0::2] = img[ch, r0::2, c0::2]

        return bayer

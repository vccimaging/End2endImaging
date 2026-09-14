"""DWDN: Deep Wiener Deconvolution Network for MetaSpectra+ reconstruction.

Non-blind: uses the known (fixed) per-sub-image PSF kernels. Each RGB sub-image
is lifted to a feature map, Wiener-deconvolved in the feature/frequency domain
with its channel's kernel, then all deconvolved features are concatenated and
refined by a multi-scale network (NAFNet). Follows Dong et al. (2021) adapted to
the multi-aperture setting (MetaH2 / 2-in-1).
"""

import torch
import torch.nn as nn

from .nafnet import NAFNet


class FeatureWienerDeconv(nn.Module):
    """Feature-domain Wiener deconvolution with a learnable per-channel SNR."""

    def __init__(self, n_feat):
        super().__init__()
        self.log_snr = nn.Parameter(torch.zeros(n_feat))

    def forward(self, feat, kernel_full):
        """feat: [B, Cf, H, W]; kernel_full: [1, 1, H, W] (origin-centered, sums to 1)."""
        K = torch.fft.rfft2(kernel_full)                 # [1, 1, H, W//2+1]
        Ff = torch.fft.rfft2(feat)                        # [B, Cf, H, W//2+1]
        snr = torch.exp(self.log_snr).view(1, -1, 1, 1)
        deconv = (torch.conj(K) / (K.abs() ** 2 + 1.0 / snr)) * Ff
        return torch.fft.irfft2(deconv, s=feat.shape[-2:])


class DWDN(nn.Module):
    def __init__(
        self,
        kernels,
        in_chan=12,
        out_chan=26,
        n_sub=4,
        feat=32,
        width=32,
        middle_blk_num=1,
        enc_blk_nums=(1, 1, 1, 18),
        dec_blk_nums=(1, 1, 1, 1),
    ):
        super().__init__()
        self.register_buffer("kernels", kernels)  # [n_sub, ks, ks], fixed (non-blind)
        self.n_sub = n_sub
        self.chan_per_sub = in_chan // n_sub
        self.pre = nn.Sequential(
            nn.Conv2d(self.chan_per_sub, feat, 3, padding=1),
            nn.GELU(),
            nn.Conv2d(feat, feat, 3, padding=1),
        )
        self.wiener = FeatureWienerDeconv(feat)
        self.refine = NAFNet(
            in_chan=feat * n_sub,
            out_chan=out_chan,
            width=width,
            middle_blk_num=middle_blk_num,
            enc_blk_nums=list(enc_blk_nums),
            dec_blk_nums=list(dec_blk_nums),
        )

    def _padded_kernel(self, ker, H, W):
        """Place a [ks, ks] kernel into an origin-centered [1, 1, H, W] map."""
        ks = ker.shape[-1]
        full = torch.zeros(1, 1, H, W, device=ker.device, dtype=ker.dtype)
        full[0, 0, :ks, :ks] = ker
        return torch.roll(full, shifts=(-(ks // 2), -(ks // 2)), dims=(-2, -1))

    def forward(self, x):
        B, _, H, W = x.shape
        ks = self.kernels.shape[-1]
        if ks > H or ks > W:
            raise ValueError(
                f"DWDN requires input H,W >= kernel size ks={ks}, got H={H}, W={W}. "
                f"Increase crop_size to >= optics.ks, or reduce optics.ks."
            )
        feats = []
        for s in range(self.n_sub):
            sub = x[:, s * self.chan_per_sub : (s + 1) * self.chan_per_sub]
            f = self.pre(sub)
            k = self._padded_kernel(self.kernels[s], H, W)
            feats.append(self.wiener(f, k))
        return self.refine(torch.cat(feats, dim=1))

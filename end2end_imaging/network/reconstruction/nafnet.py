"""
NAFNet: Nonlinear Activation Free Network for Image Restoration
Paper: Simple Baselines for Image Restoration (ECCV2022)
Liangyu Chen*, Xiaojie Chu*, Xiangyu Zhang, Jian Sun
https://github.com/megvii-research/NAFNet/blob/main/basicsr/models/archs/NAFNet_arch.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class NAFNet(nn.Module):
    """Nonlinear Activation Free Network for image restoration.

    A U-Net-style encoder-decoder with NAFBlocks that replace nonlinear activations
    with SimpleGate (element-wise multiplication of channel-split halves). Includes
    a global residual connection from input to output.

    Reference: "Simple Baselines for Image Restoration" (ECCV 2022).

    Args:
        in_chan: Number of input channels. Defaults to 3.
        out_chan: Number of output channels. Defaults to 3.
        width: Base channel width. Defaults to 32.
        middle_blk_num: Number of NAFBlocks in the bottleneck. Defaults to 1.
        enc_blk_nums: Number of NAFBlocks per encoder stage. Defaults to ``[1, 1, 1, 28]``.
        dec_blk_nums: Number of NAFBlocks per decoder stage. Defaults to ``[1, 1, 1, 1]``.
    """

    def __init__(
        self,
        in_chan=3,
        out_chan=3,
        width=32,  # 64
        middle_blk_num=1,
        enc_blk_nums=[1, 1, 1, 28],
        dec_blk_nums=[1, 1, 1, 1],
    ):
        super().__init__()

        self.intro = nn.Conv2d(
            in_channels=in_chan,
            out_channels=width,
            kernel_size=3,
            padding=1,
            stride=1,
            groups=1,
            bias=True,
        )
        self.ending = nn.Conv2d(
            in_channels=width,
            out_channels=out_chan,
            kernel_size=3,
            padding=1,
            stride=1,
            groups=1,
            bias=True,
        )

        self.encoders = nn.ModuleList()
        self.decoders = nn.ModuleList()
        self.middle_blks = nn.ModuleList()
        self.ups = nn.ModuleList()
        self.downs = nn.ModuleList()

        chan = width
        for num in enc_blk_nums:
            self.encoders.append(nn.Sequential(*[NAFBlock(chan) for _ in range(num)]))
            self.downs.append(nn.Conv2d(chan, 2 * chan, 2, 2))
            chan = chan * 2

        self.middle_blks = nn.Sequential(
            *[NAFBlock(chan) for _ in range(middle_blk_num)]
        )

        for num in dec_blk_nums:
            self.ups.append(
                nn.Sequential(
                    nn.Conv2d(chan, chan * 2, 1, bias=False), nn.PixelShuffle(2)
                )
            )
            chan = chan // 2
            self.decoders.append(nn.Sequential(*[NAFBlock(chan) for _ in range(num)]))

        self.padder_size = 2 ** len(self.encoders)

        # Initialize weights  
        self.initialize_weights()  

    def initialize_weights(self):
        """Initialize all module weights.

        Uses truncated-normal initialization (std 0.02) for conv and linear
        layers per the NAFNet paper, sets BatchNorm to identity scale, and
        zeros the final conv so the global residual yields an exact identity
        on the first ``out_chan`` input channels at the start of training.
        """
        # NAFNet has no ReLU (uses SimpleGate); kaiming-relu inflates activations by sqrt(2)
        # at every layer. Use trunc_normal(std=0.02) per the NAFNet paper.
        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.Linear)):
                nn.init.trunc_normal_(m.weight, std=0.02)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
        # Zero the final conv so the global residual makes the network an exact identity
        # on the first `out_chan` input channels at step 0. Training then learns the correction.
        nn.init.zeros_(self.ending.weight)
        if self.ending.bias is not None:
            nn.init.zeros_(self.ending.bias)

    def forward(self, inp):
        """Forward pass with global residual connection.

        Args:
            inp: Input image tensor of shape ``(B, in_chan, H, W)``.

        Returns:
            Restored image tensor of shape ``(B, out_chan, H, W)``.
        """
        B, C, H, W = inp.shape
        inp = self.check_image_size(inp)

        x = self.intro(inp)

        encs = []

        for encoder, down in zip(self.encoders, self.downs):
            x = encoder(x)
            encs.append(x)
            x = down(x)

        x = self.middle_blks(x)

        for decoder, up, enc_skip in zip(self.decoders, self.ups, encs[::-1]):
            x = up(x)
            x = x + enc_skip
            x = decoder(x)

        x = self.ending(x)
        x = x + inp[:, :x.shape[1], :, :]

        return x[:, :, :H, :W]

    def check_image_size(self, x):
        """Pad the input so its spatial dims are divisible by ``padder_size``.

        Args:
            x: Input tensor of shape ``(B, C, H, W)``.

        Returns:
            Zero-padded tensor whose height and width are multiples of
            ``self.padder_size``.
        """
        _, _, h, w = x.size()
        mod_pad_h = (self.padder_size - h % self.padder_size) % self.padder_size
        mod_pad_w = (self.padder_size - w % self.padder_size) % self.padder_size
        x = F.pad(x, (0, mod_pad_w, 0, mod_pad_h))
        return x


class LayerNormFunction(torch.autograd.Function):
    """Autograd function implementing channel-wise LayerNorm for NCHW tensors."""

    @staticmethod
    def forward(ctx, x, weight, bias, eps):
        ctx.eps = eps
        N, C, H, W = x.size()
        mu = x.mean(1, keepdim=True)
        var = (x - mu).pow(2).mean(1, keepdim=True)
        y = (x - mu) / (var + eps).sqrt()
        ctx.save_for_backward(y, var, weight)
        y = weight.view(1, C, 1, 1) * y + bias.view(1, C, 1, 1)
        return y

    @staticmethod
    def backward(ctx, grad_output):
        eps = ctx.eps

        N, C, H, W = grad_output.size()
        y, var, weight = ctx.saved_variables
        g = grad_output * weight.view(1, C, 1, 1)
        mean_g = g.mean(dim=1, keepdim=True)

        mean_gy = (g * y).mean(dim=1, keepdim=True)
        gx = 1.0 / torch.sqrt(var + eps) * (g - y * mean_gy - mean_g)
        return (
            gx,
            (grad_output * y).sum(dim=3).sum(dim=2).sum(dim=0),
            grad_output.sum(dim=3).sum(dim=2).sum(dim=0),
            None,
        )


class LayerNorm2d(nn.Module):
    """Channel-wise LayerNorm module for 4D ``(B, C, H, W)`` tensors."""

    def __init__(self, channels, eps=1e-6):
        super(LayerNorm2d, self).__init__()
        self.register_parameter("weight", nn.Parameter(torch.ones(channels)))
        self.register_parameter("bias", nn.Parameter(torch.zeros(channels)))
        self.eps = eps

    def forward(self, x):
        """Apply channel-wise LayerNorm to a ``(B, C, H, W)`` tensor."""
        return LayerNormFunction.apply(x, self.weight, self.bias, self.eps)


class AvgPool2d(nn.Module):
    """Adaptive average pooling with test-time local-window support.

    Drop-in replacement for ``nn.AdaptiveAvgPool2d(1)`` that, at inference,
    derives a pooling window from ``base_size``/``train_size`` to keep the
    receptive field consistent with training (TLC, "Test-time Local
    Converter"). An optional ``fast_imp`` path trades exactness for speed.

    Args:
        kernel_size: Explicit pooling window; inferred from ``base_size`` when None.
        base_size: Reference window size used to derive ``kernel_size`` at test time.
        auto_pad: Whether to replicate-pad the output back to the input size.
        fast_imp: Use the faster, non-equivalent strided implementation.
        train_size: Training input size used to scale the window at test time.
    """

    def __init__(
        self,
        kernel_size=None,
        base_size=None,
        auto_pad=True,
        fast_imp=False,
        train_size=None,
    ):
        super().__init__()
        self.kernel_size = kernel_size
        self.base_size = base_size
        self.auto_pad = auto_pad

        # only used for fast implementation
        self.fast_imp = fast_imp
        self.rs = [5, 4, 3, 2, 1]
        self.max_r1 = self.rs[0]
        self.max_r2 = self.rs[0]
        self.train_size = train_size

    def extra_repr(self) -> str:
        return "kernel_size={}, base_size={}, stride={}, fast_imp={}".format(
            self.kernel_size, self.base_size, self.kernel_size, self.fast_imp
        )

    def forward(self, x):
        """Average-pool ``x`` over a (possibly test-time inferred) local window.

        Args:
            x: Input tensor of shape ``(B, C, H, W)``.

        Returns:
            Pooled tensor, replicate-padded back to the input size when
            ``auto_pad`` is set.
        """
        if self.kernel_size is None and self.base_size:
            train_size = self.train_size
            if isinstance(self.base_size, int):
                self.base_size = (self.base_size, self.base_size)
            self.kernel_size = list(self.base_size)
            self.kernel_size[0] = x.shape[2] * self.base_size[0] // train_size[-2]
            self.kernel_size[1] = x.shape[3] * self.base_size[1] // train_size[-1]

            # only used for fast implementation
            self.max_r1 = max(1, self.rs[0] * x.shape[2] // train_size[-2])
            self.max_r2 = max(1, self.rs[0] * x.shape[3] // train_size[-1])

        if self.kernel_size[0] >= x.size(-2) and self.kernel_size[1] >= x.size(-1):
            return F.adaptive_avg_pool2d(x, 1)

        if self.fast_imp:  # Non-equivalent implementation but faster
            h, w = x.shape[2:]
            if self.kernel_size[0] >= h and self.kernel_size[1] >= w:
                out = F.adaptive_avg_pool2d(x, 1)
            else:
                r1 = [r for r in self.rs if h % r == 0][0]
                r2 = [r for r in self.rs if w % r == 0][0]
                # reduction_constraint
                r1 = min(self.max_r1, r1)
                r2 = min(self.max_r2, r2)
                s = x[:, :, ::r1, ::r2].cumsum(dim=-1).cumsum(dim=-2)
                n, c, h, w = s.shape
                k1, k2 = (
                    min(h - 1, self.kernel_size[0] // r1),
                    min(w - 1, self.kernel_size[1] // r2),
                )
                out = (
                    s[:, :, :-k1, :-k2]
                    - s[:, :, :-k1, k2:]
                    - s[:, :, k1:, :-k2]
                    + s[:, :, k1:, k2:]
                ) / (k1 * k2)
                out = torch.nn.functional.interpolate(out, scale_factor=(r1, r2))
        else:
            n, c, h, w = x.shape
            s = x.cumsum(dim=-1).cumsum_(dim=-2)
            s = torch.nn.functional.pad(s, (1, 0, 1, 0))  # pad 0 for convenience
            k1, k2 = min(h, self.kernel_size[0]), min(w, self.kernel_size[1])
            s1, s2, s3, s4 = (
                s[:, :, :-k1, :-k2],
                s[:, :, :-k1, k2:],
                s[:, :, k1:, :-k2],
                s[:, :, k1:, k2:],
            )
            out = s4 + s1 - s2 - s3
            out = out / (k1 * k2)

        if self.auto_pad:
            n, c, h, w = x.shape
            _h, _w = out.shape[2:]
            # print(x.shape, self.kernel_size)
            pad2d = ((w - _w) // 2, (w - _w + 1) // 2, (h - _h) // 2, (h - _h + 1) // 2)
            out = torch.nn.functional.pad(out, pad2d, mode="replicate")

        return out


def replace_layers(model, base_size, train_size, fast_imp, **kwargs):
    """Recursively replace ``nn.AdaptiveAvgPool2d`` modules with ``AvgPool2d``.

    Args:
        model: Module whose children are scanned in place.
        base_size: Reference window size passed to the new ``AvgPool2d``.
        train_size: Training input size passed to the new ``AvgPool2d``.
        fast_imp: Whether the replacement uses the fast pooling path.
        **kwargs: Additional keyword arguments forwarded during recursion.
    """
    for n, m in model.named_children():
        if len(list(m.children())) > 0:
            ## compound module, go inside it
            replace_layers(m, base_size, train_size, fast_imp, **kwargs)

        if isinstance(m, nn.AdaptiveAvgPool2d):
            pool = AvgPool2d(
                base_size=base_size, fast_imp=fast_imp, train_size=train_size
            )
            assert m.output_size == 1
            setattr(model, n, pool)


class Local_Base:
    """Mixin that swaps global pooling for local pooling via [`replace_layers`][end2end_imaging.network.reconstruction.nafnet.replace_layers]."""

    def convert(self, *args, train_size, **kwargs):
        """Replace global pooling layers and run a dummy forward to set windows.

        Args:
            *args: Positional arguments forwarded to
                [`replace_layers`][end2end_imaging.network.reconstruction.nafnet.replace_layers]
                (e.g. ``base_size``, ``fast_imp``).
            train_size: Training input size used to build the dummy tensor and
                configure the local pooling windows.
            **kwargs: Additional keyword arguments forwarded to
                [`replace_layers`][end2end_imaging.network.reconstruction.nafnet.replace_layers].
        """
        replace_layers(self, *args, train_size=train_size, **kwargs)
        imgs = torch.rand(train_size)
        with torch.no_grad():
            self.forward(imgs)


class SimpleGate(nn.Module):
    """Gating layer that splits channels in half and multiplies the two halves."""

    def forward(self, x):
        """Split the channel dimension in two and return their element-wise product.

        Args:
            x: Input tensor of shape ``(B, C, H, W)`` with even ``C``.

        Returns:
            Tensor of shape ``(B, C // 2, H, W)``.
        """
        x1, x2 = x.chunk(2, dim=1)
        return x1 * x2


class NAFBlock(nn.Module):
    """Nonlinear Activation Free block.

    Combines a depthwise-conv branch with Simplified Channel Attention and a
    feed-forward branch, both using SimpleGate instead of nonlinear
    activations, with learnable residual scales ``beta`` and ``gamma``.

    Args:
        c: Number of input/output channels.
        DW_Expand: Channel expansion factor for the depthwise branch. Defaults to 2.
        FFN_Expand: Channel expansion factor for the feed-forward branch. Defaults to 2.
        drop_out_rate: Dropout probability; 0 disables dropout. Defaults to 0.0.
    """

    def __init__(self, c, DW_Expand=2, FFN_Expand=2, drop_out_rate=0.0):
        super().__init__()
        dw_channel = c * DW_Expand
        self.conv1 = nn.Conv2d(
            in_channels=c,
            out_channels=dw_channel,
            kernel_size=1,
            padding=0,
            stride=1,
            groups=1,
            bias=True,
        )
        self.conv2 = nn.Conv2d(
            in_channels=dw_channel,
            out_channels=dw_channel,
            kernel_size=3,
            padding=1,
            stride=1,
            groups=dw_channel,
            bias=True,
        )
        self.conv3 = nn.Conv2d(
            in_channels=dw_channel // 2,
            out_channels=c,
            kernel_size=1,
            padding=0,
            stride=1,
            groups=1,
            bias=True,
        )

        # Simplified Channel Attention
        self.sca = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(
                in_channels=dw_channel // 2,
                out_channels=dw_channel // 2,
                kernel_size=1,
                padding=0,
                stride=1,
                groups=1,
                bias=True,
            ),
        )

        # SimpleGate
        self.sg = SimpleGate()

        ffn_channel = FFN_Expand * c
        self.conv4 = nn.Conv2d(
            in_channels=c,
            out_channels=ffn_channel,
            kernel_size=1,
            padding=0,
            stride=1,
            groups=1,
            bias=True,
        )
        self.conv5 = nn.Conv2d(
            in_channels=ffn_channel // 2,
            out_channels=c,
            kernel_size=1,
            padding=0,
            stride=1,
            groups=1,
            bias=True,
        )

        self.norm1 = LayerNorm2d(c)
        self.norm2 = LayerNorm2d(c)

        self.dropout1 = (
            nn.Dropout(drop_out_rate) if drop_out_rate > 0.0 else nn.Identity()
        )
        self.dropout2 = (
            nn.Dropout(drop_out_rate) if drop_out_rate > 0.0 else nn.Identity()
        )

        self.beta = nn.Parameter(torch.zeros((1, c, 1, 1)), requires_grad=True)
        self.gamma = nn.Parameter(torch.zeros((1, c, 1, 1)), requires_grad=True)

    def forward(self, inp):
        """Apply the attention and feed-forward branches with residual scaling.

        Args:
            inp: Input tensor of shape ``(B, c, H, W)``.

        Returns:
            Output tensor of shape ``(B, c, H, W)``.
        """
        x = inp

        x = self.norm1(x)

        x = self.conv1(x)
        x = self.conv2(x)
        x = self.sg(x)
        x = x * self.sca(x)
        x = self.conv3(x)

        x = self.dropout1(x)

        y = inp + x * self.beta

        x = self.conv4(self.norm2(y))
        x = self.sg(x)
        x = self.conv5(x)

        x = self.dropout2(x)

        return y + x * self.gamma


if __name__ == "__main__":
    model = NAFNet(in_chan=3, out_chan=3)
    input = torch.rand(size=(16, 3, 384, 512))
    output = model(input)
    print(output.shape)

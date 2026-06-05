"""Tests for the Demosaic module across Bayer patterns.

Covers the bug where ``Demosaic`` accepted a ``bayer_pattern`` argument and
advertised "bggr" support, but every demosaicing implementation
(``_malvar_demosaic``, ``_bilinear_demosaic``, ``reverse``) was hardcoded to
the RGGB layout. These tests pin the absolute per-pattern semantics so a
pattern-agnostic implementation cannot silently produce wrong colours.

Test strategy:
- ``reverse`` must sample the channel that the pattern dictates at each
  physical 2x2-tile position (absolute oracle).
- ``forward`` must reconstruct a uniform colour from its ideal mosaic
  (known-colour sanity, built from an independent oracle).
- ``reverse(forward(bayer)) == bayer`` for every pattern (round-trip
  consistency: forward keeps the sampled value, reverse re-reads it).
- Unsupported patterns must raise ``ValueError`` instead of silently
  producing wrong output.
"""

import pytest
import torch

from end2end_imaging.sensor.isp_modules.demosaic import Demosaic

# Standard Bayer patterns supported by the module.
PATTERNS = ["rggb", "bggr", "grbg", "gbrg"]
METHODS = ["bilinear", "malvar"]

# Independent oracle: map each (row % 2, col % 2) tile position to its RGB
# channel index (R=0, G=1, B=2). Read straight off the pattern letters,
# e.g. "rggb" -> R G / G B.
_PATTERN_CHANNEL_MAP = {
    "rggb": [[0, 1], [1, 2]],
    "bggr": [[2, 1], [1, 0]],
    "grbg": [[1, 0], [2, 1]],
    "gbrg": [[1, 2], [0, 1]],
}


def _ideal_mosaic(pattern, r, g, b, H, W, device):
    """Build the ideal 1-channel Bayer for a uniform colour ``(r, g, b)``."""
    vals = [r, g, b]
    cmap = _PATTERN_CHANNEL_MAP[pattern]
    bayer = torch.zeros((1, 1, H, W), device=device)
    for rr in range(2):
        for cc in range(2):
            bayer[:, 0, rr::2, cc::2] = vals[cmap[rr][cc]]
    return bayer


class TestReverseChannelPlacement:
    """``reverse`` must sample channels per the configured Bayer pattern."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_reverse_samples_correct_channel(self, pattern, device_auto):
        """Each tile position pulls from the channel the pattern specifies."""
        H = W = 8
        img = torch.zeros(1, 3, H, W, device=device_auto)
        img[:, 0] = 0.1  # R
        img[:, 1] = 0.5  # G
        img[:, 2] = 0.9  # B

        bayer = Demosaic(bayer_pattern=pattern).reverse(img)
        assert bayer.shape == (1, 1, H, W)

        vals = [0.1, 0.5, 0.9]
        cmap = _PATTERN_CHANNEL_MAP[pattern]
        for rr in range(2):
            for cc in range(2):
                expected = vals[cmap[rr][cc]]
                block = bayer[:, 0, rr::2, cc::2]
                assert torch.allclose(
                    block, torch.full_like(block, expected)
                ), f"pattern={pattern} pos=({rr},{cc}) expected {expected}"


class TestForwardKnownColor:
    """``forward`` must reconstruct a uniform colour from its ideal mosaic."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    @pytest.mark.parametrize("method", METHODS)
    def test_uniform_color_reconstructed(self, pattern, method, device_auto):
        """A flat (r, g, b) scene demosaics back to (r, g, b) everywhere."""
        H = W = 8
        r, g, b = 0.2, 0.5, 0.9
        bayer = _ideal_mosaic(pattern, r, g, b, H, W, device_auto)

        demosaic = Demosaic(bayer_pattern=pattern, method=method)
        rgb = demosaic(bayer)

        assert rgb.shape == (1, 3, H, W)
        target = torch.tensor([r, g, b], device=device_auto).view(1, 3, 1, 1)
        assert torch.allclose(rgb, target.expand_as(rgb), atol=1e-5)


class TestReverseForwardRoundTrip:
    """``reverse(forward(bayer))`` recovers the original sampled values."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    @pytest.mark.parametrize("method", METHODS)
    def test_roundtrip_identity(self, pattern, method, device_auto):
        """Forward keeps the sampled value; reverse reads it back exactly."""
        torch.manual_seed(0)
        bayer = torch.rand(1, 1, 8, 8, device=device_auto)

        demosaic = Demosaic(bayer_pattern=pattern, method=method)
        rgb = demosaic(bayer)
        bayer_rec = demosaic.reverse(rgb)

        assert torch.allclose(bayer, bayer_rec, atol=1e-6)

    @pytest.mark.parametrize("pattern", PATTERNS)
    @pytest.mark.parametrize("method", METHODS)
    def test_roundtrip_identity_no_batch_dim(self, pattern, method, device_auto):
        """Round-trip also holds for unbatched [1, H, W] / [3, H, W] tensors."""
        torch.manual_seed(0)
        bayer = torch.rand(1, 8, 8, device=device_auto)

        demosaic = Demosaic(bayer_pattern=pattern, method=method)
        rgb = demosaic(bayer)
        assert rgb.shape == (3, 8, 8)
        bayer_rec = demosaic.reverse(rgb)
        assert bayer_rec.shape == (1, 8, 8)
        assert torch.allclose(bayer, bayer_rec, atol=1e-6)


class TestPatternValidation:
    """Unsupported patterns must fail loudly, not silently mis-demosaic."""

    def test_invalid_pattern_raises(self):
        """An unknown pattern raises ValueError at construction."""
        with pytest.raises(ValueError):
            Demosaic(bayer_pattern="xyz")

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_supported_patterns_construct(self, pattern):
        """All four standard patterns construct and store the pattern."""
        demosaic = Demosaic(bayer_pattern=pattern)
        assert demosaic.bayer_pattern == pattern

    def test_invalid_method_raises_on_forward(self, device_auto):
        """An unknown method still raises ValueError on forward (regression)."""
        demosaic = Demosaic(bayer_pattern="rggb", method="nope")
        bayer = torch.rand(1, 1, 8, 8, device=device_auto)
        with pytest.raises(ValueError):
            demosaic(bayer)


class TestRGBSensorPatternPropagation:
    """The configurable RGBSensor must honour its bayer_pattern end-to-end."""

    @pytest.mark.parametrize("pattern", PATTERNS)
    def test_sensor_demosaic_uses_pattern(self, pattern, device_auto):
        """RGBSensor wires bayer_pattern into its embedded Demosaic."""
        from end2end_imaging.sensor.rgb_sensor import RGBSensor

        sensor = RGBSensor(bayer_pattern=pattern)
        sensor.to(device_auto)
        assert sensor.isp.demosaic.bayer_pattern == pattern

        torch.manual_seed(0)
        bayer = torch.rand(1, 1, 8, 8, device=device_auto)
        rec = sensor.isp.demosaic.reverse(sensor.isp.demosaic(bayer))
        assert torch.allclose(bayer, rec, atol=1e-6)

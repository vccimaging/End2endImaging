"""Backward-compatible imports for differentiable tensor operations.

DeepLens moved these helpers into :mod:`deeplens.utils`.  End2endImaging
historically exposed them from ``end2end_imaging.deeplens.ops``, so retain
that import path while using the synced upstream implementations.
"""

from .utils import diff_float, diff_quantize, grid_sample_xy, interp1d

__all__ = ["diff_float", "diff_quantize", "grid_sample_xy", "interp1d"]

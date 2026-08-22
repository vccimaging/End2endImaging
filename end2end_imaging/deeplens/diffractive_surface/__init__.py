"""Diffractive surface module."""

from .diffractive import DiffractiveSurface
from .binary2 import Binary2
from .diffracted_rotation import DiffractedRotation
from .fresnel import Fresnel
from .grating import Grating
from .pixel2d import Pixel2D
from .rank1 import Rank1
from .rotational_symmetric import RotationallySymmetric
from .thinlens import ThinLens
from .zernike import Zernike
from .._compat import accept_legacy_surface_distance

for _surface_cls in (
    DiffractiveSurface,
    Binary2,
    DiffractedRotation,
    Fresnel,
    Grating,
    Pixel2D,
    Rank1,
    RotationallySymmetric,
    ThinLens,
    Zernike,
):
    accept_legacy_surface_distance(_surface_cls)

del _surface_cls

__all__ = ["DiffractiveSurface", "DiffractedRotation", "Fresnel", "Grating", "Pixel2D", "Rank1", "RotationallySymmetric", "ThinLens", "Zernike", "Binary2"]

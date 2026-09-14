"""Phase surface implementations for diffractive optics."""

from .base_phase import Phase
from .binary2 import Binary2Phase
from .cubic import CubicPhase
from .fresnel import FresnelPhase
from .grating import GratingPhase
from .nurbs import NURBSPhase
from .poly import PolyPhase
from .vortex import VortexPhase
from .zernike import ZernikePhase

from .._compat import accept_legacy_surface_distance

for _surface_cls in (
    Phase,
    FresnelPhase,
    Binary2Phase,
    PolyPhase,
    GratingPhase,
    ZernikePhase,
    CubicPhase,
    NURBSPhase,
    VortexPhase,
):
    accept_legacy_surface_distance(_surface_cls)

del _surface_cls

__all__ = [
    "Phase",
    "FresnelPhase",
    "Binary2Phase",
    "PolyPhase",
    "GratingPhase",
    "ZernikePhase",
    "CubicPhase",
    "NURBSPhase",
    "VortexPhase",
]

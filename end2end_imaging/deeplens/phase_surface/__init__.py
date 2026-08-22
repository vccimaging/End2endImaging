"""Phase surface implementations for diffractive optics."""

from .phase import Phase
from .fresnel import FresnelPhase
from .binary2 import Binary2Phase
from .poly import PolyPhase
from .grating import GratingPhase
from .zernike import ZernikePhase
from .cubic import CubicPhase
from .nurbs import NURBSPhase
from .vortex import VortexPhase
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

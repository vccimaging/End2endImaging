from .base import Surface

from .aperture import Aperture
from .aspheric import Aspheric
from .cubic import Cubic
from .mirror import Mirror
from .plane import Plane
from .prism import Prism
from .qtype import QTypeFreeform
from .spheric import Spheric
from .spiral import Spiral
from .thinlens import ThinLens
from .._compat import accept_legacy_surface_distance

for _surface_cls in (
    Surface,
    Aperture,
    Aspheric,
    Cubic,
    Mirror,
    Plane,
    Prism,
    QTypeFreeform,
    Spheric,
    Spiral,
    ThinLens,
):
    accept_legacy_surface_distance(_surface_cls)

del _surface_cls

__all__ = [
    "Surface",
    "Aperture",
    "Aspheric",
    "Cubic",
    "Mirror",
    "Plane",
    "Prism",
    "QTypeFreeform",
    "Spheric",
    "Spiral",
    "ThinLens",
]

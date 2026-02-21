# GeoLens API Reference

`GeoLens` is the primary differentiable lens model. It uses vectorised
PyTorch ray tracing through multi-element refractive surfaces and is the
recommended choice for automated optical design and image simulation.

The class uses a **mixin architecture**:

| Mixin | Responsibility |
|-------|---------------|
| `GeoLensEval` | Spot diagrams, MTF, vignetting, distortion |
| `GeoLensOptim` | Loss functions, constraints, optimizer helpers |
| `GeoLensVis` | 2-D layout and ray visualisation |
| `GeoLensIO` | Read/write JSON, Zemax `.zmx` |
| `GeoLensTolerance` | Monte-Carlo and sensitivity tolerance analysis |
| `GeoLensVis3D` | 3-D mesh visualisation via PyVista |

## Main Class

::: deeplens.optics.geolens.GeoLens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Mixin Classes

::: deeplens.optics.geolens_pkg.eval.GeoLensEval
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geolens_pkg.optim.GeoLensOptim
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geolens_pkg.io.GeoLensIO
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geolens_pkg.tolerance.GeoLensTolerance
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geolens_pkg.vis.GeoLensVis
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geolens_pkg.view_3d.GeoLensVis3D
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## References

1. Xinge Yang, Qiang Fu, and Wolfgang Heidrich, "Curriculum learning for
   ab initio deep learned refractive optics," *Nature Communications* 2024.
2. Jun Dai et al., "Tolerance-Aware Deep Optics," *arXiv:2502.04719*, 2025.

## See Also

- [Lens](lens.md) — Base `Lens` class
- [HybridLens](hybridlens.md) — Hybrid / diffractive lens types
- [Optics](optics.md) — Surfaces, rays, and PSF utilities

# Lens API Reference

Base class for all lens systems. Every lens type (`GeoLens`,
`HybridLens`, `DiffractiveLens`, `ParaxialLens`, `PSFNetLens`)
inherits from `Lens`, which defines the public PSF/rendering API and
the sensor configuration helpers.

::: deeplens.optics.lens.Lens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## See Also

- [GeoLens](geolens.md) — Differentiable refractive ray-tracing lens
- [HybridLens](hybridlens.md) — Hybrid refractive-diffractive lens, and other lens types
- [Optics](optics.md) — Surfaces, rays, and PSF utilities

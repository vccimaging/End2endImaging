# Optics API Reference

This page documents optical primitives: surfaces, rays, complex wave
fields, and PSF utilities.

## Base Classes

### DeepObj

::: deeplens.optics.base.DeepObj
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### Surface (base)

::: deeplens.optics.geometric_surface.base.Surface
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Geometric Surfaces

::: deeplens.optics.geometric_surface.Spheric
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geometric_surface.Aspheric
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.geometric_surface.Plane
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

::: deeplens.optics.geometric_surface.Aperture
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

::: deeplens.optics.geometric_surface.Cubic
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

::: deeplens.optics.geometric_surface.Mirror
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

## Diffractive Surfaces

::: deeplens.optics.diffractive_surface.Fresnel
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.diffractive_surface.Binary2
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.diffractive_surface.Pixel2D
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.diffractive_surface.Zernike
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.optics.diffractive_surface.Grating
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

## Phase Surfaces

::: deeplens.optics.phase_surface.Phase
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Material

::: deeplens.optics.material.Material
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Ray and Wave Fields

### Ray

::: deeplens.optics.light.Ray
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### ComplexWave

::: deeplens.optics.light.ComplexWave
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### AngularSpectrumMethod

::: deeplens.optics.light.AngularSpectrumMethod

## PSF Utilities

### Monte-Carlo Integral

::: deeplens.optics.imgsim.forward_integral

### PSF Convolution

::: deeplens.optics.imgsim.conv_psf

::: deeplens.optics.imgsim.conv_psf_map

::: deeplens.optics.imgsim.conv_psf_depth_interp

::: deeplens.optics.imgsim.conv_psf_map_depth_interp

::: deeplens.optics.imgsim.conv_psf_pixel

## See Also

- [Lens](lens.md) — Base `Lens` class
- [GeoLens](geolens.md) — `GeoLens` with full ray-tracing API
- [HybridLens](hybridlens.md) — Diffractive and hybrid lens types

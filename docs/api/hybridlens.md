# Alternative Lens Models

This page documents four additional lens types that complement the main
`GeoLens` model.

## HybridLens

A hybrid refractive-diffractive lens that couples a `GeoLens` with a
diffractive optical element (DOE). Uses a differentiable ray–wave pipeline:
coherent ray tracing to the DOE plane, phase modulation by the DOE, and
Angular Spectrum Method propagation to the sensor.

!!! note
    `HybridLens` operates in `torch.float64` by default for numerical
    stability of the wave-propagation step.

::: deeplens.optics.hybridlens.HybridLens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### References

Xinge Yang et al., "End-to-End Hybrid Refractive-Diffractive Lens Design
with Differentiable Ray-Wave Model," *SIGGRAPH Asia* 2024.

## DiffractiveLens

A pure wave-optics lens in which every optical element is modelled as a
phase surface. Propagation between surfaces uses scalar diffraction theory
(Angular Spectrum Method, Fresnel, or Fraunhofer).

::: deeplens.optics.diffraclens.DiffractiveLens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### References

1. Vincent Sitzmann et al., "End-to-end optimization of optics and image
   processing for achromatic extended depth of field," *SIGGRAPH* 2018.
2. Qilin Sun et al., "Learning Rank-1 Diffractive Optics for Single-shot
   High Dynamic Range Imaging," *CVPR* 2020.

## ParaxialLens

A thin-lens / ABCD-matrix model that simulates defocus (circle of
confusion) but not higher-order aberrations. Useful as a fast baseline
for bokeh rendering.

::: deeplens.optics.paraxiallens.ParaxialLens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## PSFNetLens

A neural surrogate that wraps a `GeoLens` with an MLP network that
predicts PSFs directly from `(fov, depth, focus_distance)` without
running ray tracing. Provides ~100× speedup over full ray tracing after
a one-time training phase.

::: deeplens.optics.psfnetlens.PSFNetLens
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### References

Xinge Yang et al., "Aberration-Aware Depth-from-Focus," *IEEE TPAMI* 2023.

## See Also

- [Lens](lens.md) — Base `Lens` class
- [GeoLens](geolens.md) — Primary differentiable refractive lens
- [Optics](optics.md) — Diffractive surfaces and wave propagation

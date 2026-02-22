# Optics API Reference

The `deeplens.optics` module contains the differentiable lens models, optical surfaces, light representations, and image simulation utilities.

---

## Base Classes

### DeepObj

Base class for all optical objects. Provides device transfer, dtype conversion, and cloning by introspecting instance tensors.

::: deeplens.optics.DeepObj
    options:
      members: ["to", "astype", "clone"]

### Lens

Abstract base class for all lens types. Defines the shared interface: `psf()`, `psf_rgb()`, `render()`, etc.

::: deeplens.optics.Lens
    options:
      members: ["psf", "psf_rgb", "psf_map", "render"]

---

## Lens Models

### GeoLens

Differentiable multi-element refractive lens via geometric ray tracing. This is the primary lens model in DeepLens.

`GeoLens` uses a mixin architecture — functionality is split across `GeoLensEval`, `GeoLensOptim`, `GeoLensVis`, `GeoLensIO`, `GeoLensTolerance`, and `GeoLensVis3D`.

::: deeplens.optics.GeoLens
    options:
      members: false

#### Evaluation (GeoLensEval)

::: deeplens.optics.geolens_pkg.eval.GeoLensEval
    options:
      members: false

#### Optimization (GeoLensOptim)

::: deeplens.optics.geolens_pkg.optim.GeoLensOptim
    options:
      members: false

#### I/O (GeoLensIO)

::: deeplens.optics.geolens_pkg.io.GeoLensIO
    options:
      members: false

#### Visualization (GeoLensVis)

::: deeplens.optics.geolens_pkg.vis.GeoLensVis
    options:
      members: false

#### Tolerancing (GeoLensTolerance)

::: deeplens.optics.geolens_pkg.tolerance.GeoLensTolerance
    options:
      members: false

#### 3D Visualization (GeoLensVis3D)

::: deeplens.optics.geolens_pkg.view_3d.GeoLensVis3D
    options:
      members: false

### HybridLens

Combines a `GeoLens` with a diffractive optical element (DOE). Performs coherent ray tracing to the DOE plane, then Angular Spectrum Method (ASM) propagation to the sensor.

::: deeplens.optics.HybridLens
    options:
      members: false

### DiffractiveLens

Pure wave-optics lens using diffractive surfaces and scalar diffraction propagation.

::: deeplens.optics.DiffractiveLens
    options:
      members: false

### ParaxialLens

Thin-lens / circle-of-confusion model for simple depth-of-field and bokeh simulation.

::: deeplens.optics.ParaxialLens
    options:
      members: false

### PSFNetLens

Neural surrogate that wraps a `GeoLens` with an MLP to predict PSFs. Useful for fast, differentiable PSF evaluation during end-to-end training.

::: deeplens.optics.PSFNetLens
    options:
      members: false

---

## Surfaces

### Surface

Base class for all geometric optical surfaces. Implements surface intersection (Newton's method with one differentiable step) and differentiable vector Snell's law refraction.

::: deeplens.optics.geometric_surface.Surface
    options:
      members: ["__init__", "ray_reaction"]

### Spheric

Spherical surface defined by curvature $c = 1/R$.

::: deeplens.optics.geometric_surface.Spheric
    options:
      members: ["__init__"]

### Aspheric

Even-asphere surface: spherical base with polynomial corrections.

::: deeplens.optics.geometric_surface.Aspheric
    options:
      members: ["__init__"]

### Aperture

::: deeplens.optics.geometric_surface.Aperture
    options:
      members: ["__init__"]

---

## Light Representations

### Ray

Geometric ray representation carrying origin, direction, wavelength, validity mask, energy, and optical path length (OPL).

::: deeplens.optics.Ray
    options:
      members: false

### ComplexWave

Complex electromagnetic field with Angular Spectrum Method (ASM), Fresnel, and Fraunhofer propagation via `torch.fft`.

::: deeplens.optics.ComplexWave
    options:
      members: ["__init__"]

---

## PSF Utilities

Functions for convolving images with point spread functions.

::: deeplens.optics.imgsim.psf.conv_psf

::: deeplens.optics.imgsim.psf.conv_psf_map

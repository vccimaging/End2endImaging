# DeepLens API Reference

The `end2end_imaging.deeplens` module contains the differentiable lens models, optical surfaces, light representations, and image simulation utilities.

---

## Base Classes

Base class for all optical objects. Provides device transfer, dtype conversion, and cloning by introspecting instance tensors.

::: end2end_imaging.deeplens.DeepObj

Abstract base class for all lens types. Defines the shared interface: `psf()`, `psf_rgb()`, `render()`, etc.

::: end2end_imaging.deeplens.Lens

---

## Lens Models

Differentiable multi-element refractive lens via geometric ray tracing. This is the primary lens model.

`GeoLens` uses a mixin architecture — functionality is split across `GeoLensPSF`, `GeoLensEval`, `GeoLensSeidel`, `GeoLensOptim`, `GeoLensSurfOps`, `GeoLensVis`, `GeoLensIO`, and `GeoLensVis3D`.

::: end2end_imaging.deeplens.GeoLens

::: end2end_imaging.deeplens.geolens_pkg.psf_compute.GeoLensPSF

::: end2end_imaging.deeplens.geolens_pkg.eval.GeoLensEval

::: end2end_imaging.deeplens.geolens_pkg.eval_seidel.GeoLensSeidel

::: end2end_imaging.deeplens.geolens_pkg.optim.GeoLensOptim

::: end2end_imaging.deeplens.geolens_pkg.optim_ops.GeoLensSurfOps

::: end2end_imaging.deeplens.geolens_pkg.io.GeoLensIO

::: end2end_imaging.deeplens.geolens_pkg.vis.GeoLensVis

::: end2end_imaging.deeplens.geolens_pkg.vis3d.GeoLensVis3D

Combines a `GeoLens` with a diffractive optical element (DOE). Performs coherent ray tracing to the DOE plane, then Angular Spectrum Method (ASM) propagation to the sensor.

::: end2end_imaging.deeplens.HybridLens

Pure wave-optics lens using diffractive surfaces and scalar diffraction propagation.

::: end2end_imaging.deeplens.DiffractiveLens

Thin-lens / circle-of-confusion model for simple depth-of-field and bokeh simulation.

::: end2end_imaging.deeplens.DefocusLens

Neural surrogate that wraps a `GeoLens` with an MLP to predict PSFs. Useful for fast, differentiable PSF evaluation during end-to-end training.

::: end2end_imaging.deeplens.PSFNetLens

---

## Surfaces

Base class for all geometric optical surfaces. Implements surface intersection (Newton's method with one differentiable step) and differentiable vector Snell's law refraction.

::: end2end_imaging.deeplens.geometric_surface.Surface

Spherical surface defined by curvature $c = 1/R$.

::: end2end_imaging.deeplens.geometric_surface.Spheric

Even-asphere surface: spherical base with polynomial corrections.

::: end2end_imaging.deeplens.geometric_surface.Aspheric

::: end2end_imaging.deeplens.geometric_surface.Aperture

---

## Light Representations

Geometric ray representation carrying origin, direction, wavelength, validity mask, energy, and optical path length (OPL).

::: end2end_imaging.deeplens.Ray

Complex electromagnetic field with Angular Spectrum Method (ASM), Fresnel, and Fraunhofer propagation via `torch.fft`.

::: end2end_imaging.deeplens.ComplexWave

---

## PSF Utilities

Functions for convolving images with point spread functions.

::: end2end_imaging.deeplens.imgsim.psf.conv_psf

::: end2end_imaging.deeplens.imgsim.psf.conv_psf_map

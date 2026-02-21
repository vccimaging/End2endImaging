Optics API Reference
====================

This page documents optical primitives: surfaces, rays, complex wave
fields, and PSF utilities.

Base Classes
------------

DeepObj
^^^^^^^

.. autoclass:: deeplens.optics.base.DeepObj
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Surface (base)
^^^^^^^^^^^^^^

.. autoclass:: deeplens.optics.geometric_surface.base.Surface
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Geometric Surfaces
------------------

.. autoclass:: deeplens.optics.geometric_surface.Spheric
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geometric_surface.Aspheric
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geometric_surface.Plane
   :members:
   :show-inheritance:

.. autoclass:: deeplens.optics.geometric_surface.Aperture
   :members:
   :show-inheritance:

.. autoclass:: deeplens.optics.geometric_surface.Cubic
   :members:
   :show-inheritance:

.. autoclass:: deeplens.optics.geometric_surface.Mirror
   :members:
   :show-inheritance:

Diffractive Surfaces
--------------------

.. autoclass:: deeplens.optics.diffractive_surface.Fresnel
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.diffractive_surface.Binary2
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.diffractive_surface.Pixel2D
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.diffractive_surface.Zernike
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.diffractive_surface.Grating
   :members:
   :show-inheritance:

Phase Surfaces
--------------

.. autoclass:: deeplens.optics.phase_surface.Phase
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Material
--------

.. autoclass:: deeplens.optics.material.Material
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Ray and Wave Fields
-------------------

Ray
^^^

.. autoclass:: deeplens.optics.light.Ray
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

ComplexWave
^^^^^^^^^^^

.. autoclass:: deeplens.optics.light.ComplexWave
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

AngularSpectrumMethod
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: deeplens.optics.light.AngularSpectrumMethod

PSF Utilities
-------------

Monte-Carlo Integral
^^^^^^^^^^^^^^^^^^^^

.. autofunction:: deeplens.optics.imgsim.forward_integral

PSF Convolution
^^^^^^^^^^^^^^^

.. autofunction:: deeplens.optics.imgsim.conv_psf

.. autofunction:: deeplens.optics.imgsim.conv_psf_map

.. autofunction:: deeplens.optics.imgsim.conv_psf_depth_interp

.. autofunction:: deeplens.optics.imgsim.conv_psf_map_depth_interp

.. autofunction:: deeplens.optics.imgsim.conv_psf_pixel

See Also
--------

* :doc:`lens` – Base ``Lens`` class
* :doc:`geolens` – ``GeoLens`` with full ray-tracing API
* :doc:`hybridlens` – Diffractive and hybrid lens types

Lens API Reference
==================

Base class for all lens systems.  Every lens type (``GeoLens``,
``HybridLens``, ``DiffractiveLens``, ``ParaxialLens``, ``PSFNetLens``)
inherits from ``Lens``, which defines the public PSF/rendering API and
the sensor configuration helpers.

.. autoclass:: deeplens.optics.lens.Lens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

See Also
--------

* :doc:`geolens` – Differentiable refractive ray-tracing lens
* :doc:`hybridlens` – Hybrid refractive-diffractive lens, and other lens types
* :doc:`optics` – Surfaces, rays, and PSF utilities

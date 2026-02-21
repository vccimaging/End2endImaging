GeoLens API Reference
======================

``GeoLens`` is the primary differentiable lens model.  It uses vectorised
PyTorch ray tracing through multi-element refractive surfaces and is the
recommended choice for automated optical design and image simulation.

The class uses a **mixin architecture**:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Mixin
     - Responsibility
   * - ``GeoLensEval``
     - Spot diagrams, MTF, vignetting, distortion
   * - ``GeoLensOptim``
     - Loss functions, constraints, optimizer helpers
   * - ``GeoLensVis``
     - 2-D layout and ray visualisation
   * - ``GeoLensIO``
     - Read/write JSON, Zemax ``.zmx``
   * - ``GeoLensTolerance``
     - Monte-Carlo and sensitivity tolerance analysis
   * - ``GeoLensVis3D``
     - 3-D mesh visualisation via PyVista

Main Class
----------

.. autoclass:: deeplens.optics.geolens.GeoLens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Mixin Classes
-------------

.. autoclass:: deeplens.optics.geolens_pkg.eval.GeoLensEval
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geolens_pkg.optim.GeoLensOptim
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geolens_pkg.io.GeoLensIO
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geolens_pkg.tolerance.GeoLensTolerance
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geolens_pkg.vis.GeoLensVis
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.optics.geolens_pkg.view_3d.GeoLensVis3D
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

References
----------

1. Xinge Yang, Qiang Fu, and Wolfgang Heidrich, "Curriculum learning for
   ab initio deep learned refractive optics," *Nature Communications* 2024.
2. Jun Dai et al., "Tolerance-Aware Deep Optics," *arXiv:2502.04719*, 2025.

See Also
--------

* :doc:`lens` – Base ``Lens`` class
* :doc:`hybridlens` – Hybrid / diffractive lens types
* :doc:`optics` – Surfaces, rays, and PSF utilities

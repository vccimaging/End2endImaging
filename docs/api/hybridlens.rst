Alternative Lens Models
========================

This page documents four additional lens types that complement the main
:class:`~deeplens.optics.geolens.GeoLens` model.

HybridLens
----------

A hybrid refractive-diffractive lens that couples a ``GeoLens`` with a
diffractive optical element (DOE).  Uses a differentiable ray–wave pipeline:
coherent ray tracing to the DOE plane, phase modulation by the DOE, and
Angular Spectrum Method propagation to the sensor.

.. note::
   ``HybridLens`` operates in ``torch.float64`` by default for numerical
   stability of the wave-propagation step.

.. autoclass:: deeplens.optics.hybridlens.HybridLens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

References
^^^^^^^^^^

Xinge Yang et al., "End-to-End Hybrid Refractive-Diffractive Lens Design
with Differentiable Ray-Wave Model," *SIGGRAPH Asia* 2024.

DiffractiveLens
---------------

A pure wave-optics lens in which every optical element is modelled as a
phase surface.  Propagation between surfaces uses scalar diffraction theory
(Angular Spectrum Method, Fresnel, or Fraunhofer).

.. autoclass:: deeplens.optics.diffraclens.DiffractiveLens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

References
^^^^^^^^^^

1. Vincent Sitzmann et al., "End-to-end optimization of optics and image
   processing for achromatic extended depth of field," *SIGGRAPH* 2018.
2. Qilin Sun et al., "Learning Rank-1 Diffractive Optics for Single-shot
   High Dynamic Range Imaging," *CVPR* 2020.

ParaxialLens
------------

A thin-lens / ABCD-matrix model that simulates defocus (circle of
confusion) but not higher-order aberrations.  Useful as a fast baseline
for bokeh rendering.

.. autoclass:: deeplens.optics.paraxiallens.ParaxialLens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

PSFNetLens
----------

A neural surrogate that wraps a ``GeoLens`` with an MLP network that
predicts PSFs directly from ``(fov, depth, focus_distance)`` without
running ray tracing.  Provides ~100× speedup over full ray tracing after
a one-time training phase.

.. autoclass:: deeplens.optics.psfnetlens.PSFNetLens
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

References
^^^^^^^^^^

Xinge Yang et al., "Aberration-Aware Depth-from-Focus," *IEEE TPAMI* 2023.

See Also
--------

* :doc:`lens` – Base ``Lens`` class
* :doc:`geolens` – Primary differentiable refractive lens
* :doc:`optics` – Diffractive surfaces and wave propagation

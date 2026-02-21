Network API Reference
=====================

DeepLens provides neural network modules for two purposes:

1. **Surrogate modelling** – fast MLP/SIREN networks that predict PSFs from
   ``(fov, depth, focus_distance)`` inputs without running ray tracing.
2. **Image reconstruction** – standard restoration networks (NAFNet, UNet,
   Restormer) used in end-to-end computational imaging pipelines.

Surrogate Networks
------------------

MLP
^^^

.. autoclass:: deeplens.network.MLP
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

MLPConv
^^^^^^^

.. autoclass:: deeplens.network.MLPConv
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Siren
^^^^^

.. autoclass:: deeplens.network.Siren
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

ModulateSiren
^^^^^^^^^^^^^

.. autoclass:: deeplens.network.ModulateSiren
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Reconstruction Networks
-----------------------

NAFNet
^^^^^^

.. autoclass:: deeplens.network.NAFNet
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

UNet
^^^^

.. autoclass:: deeplens.network.UNet
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Restormer
^^^^^^^^^

.. autoclass:: deeplens.network.Restormer
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Loss Functions
--------------

.. autoclass:: deeplens.network.PerceptualLoss
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.network.PSNRLoss
   :members:
   :show-inheritance:

.. autoclass:: deeplens.network.SSIMLoss
   :members:
   :show-inheritance:

Datasets
--------

.. autoclass:: deeplens.network.ImageDataset
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: deeplens.network.PhotographicDataset
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

See Also
--------

* :doc:`../user_guide/neural_networks` – Neural network user guide
* :doc:`hybridlens` – ``PSFNetLens`` (surrogate lens model)

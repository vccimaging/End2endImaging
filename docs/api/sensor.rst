Sensor API Reference
====================

DeepLens provides four sensor models, from a minimal gamma-only pipeline to a
full physics-based noise model with Bayer demosaicing.

Sensor (minimal)
----------------

.. autoclass:: deeplens.sensor.Sensor
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

RGBSensor
---------

Full RGB sensor with Bayer CFA, shot/read noise, white balance, colour
correction matrix, and a fully invertible ISP.

.. autoclass:: deeplens.sensor.RGBSensor
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

MonoSensor
----------

.. autoclass:: deeplens.sensor.MonoSensor
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

EventSensor
-----------

.. autoclass:: deeplens.sensor.EventSensor
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

ISP Modules
-----------

InvertibleISP
^^^^^^^^^^^^^

.. autoclass:: deeplens.sensor.isp_modules.isp.InvertibleISP
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

See Also
--------

* :doc:`lens` – Lens API (optical front-end)
* :doc:`../user_guide/sensors` – Sensor user guide

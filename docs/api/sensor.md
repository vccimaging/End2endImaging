# Sensor API Reference

DeepLens provides four sensor models, from a minimal gamma-only pipeline to a
full physics-based noise model with Bayer demosaicing.

## Sensor (minimal)

::: deeplens.sensor.Sensor
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## RGBSensor

Full RGB sensor with Bayer CFA, shot/read noise, white balance, colour
correction matrix, and a fully invertible ISP.

::: deeplens.sensor.RGBSensor
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## MonoSensor

::: deeplens.sensor.MonoSensor
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## EventSensor

::: deeplens.sensor.EventSensor
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## ISP Modules

### InvertibleISP

::: deeplens.sensor.isp_modules.isp.InvertibleISP
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## See Also

- [Lens](lens.md) — Lens API (optical front-end)
- [Sensors User Guide](../user_guide/sensors.md) — Sensor user guide

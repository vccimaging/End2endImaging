# Sensor API Reference

The `deeplens.sensor` module provides differentiable sensor models with noise simulation and a full image signal processing (ISP) pipeline.

---

## Sensor Models

### Sensor

Base sensor class.

::: deeplens.sensor.Sensor
    options:
      members: ["__init__"]

### RGBSensor

Full RGB sensor with Bayer pattern, noise model (read noise + shot noise), and ISP pipeline (black level compensation, white balance, demosaicing, color correction, gamma).

::: deeplens.sensor.RGBSensor
    options:
      members: false

### MonoSensor

Monochrome sensor without color filter array.

::: deeplens.sensor.MonoSensor
    options:
      members: false

### EventSensor

Event camera sensor that outputs asynchronous brightness-change events.

::: deeplens.sensor.EventSensor
    options:
      members: false

---

## ISP Modules

Individual image signal processing stages used inside `RGBSensor`. Each module is a `torch.nn.Module`.

::: deeplens.sensor.isp_modules.BlackLevelCompensation
    options:
      members: false

::: deeplens.sensor.isp_modules.AutoWhiteBalance
    options:
      members: false

::: deeplens.sensor.isp_modules.Demosaic
    options:
      members: false

::: deeplens.sensor.isp_modules.ColorCorrectionMatrix
    options:
      members: false

::: deeplens.sensor.isp_modules.GammaCorrection
    options:
      members: false

::: deeplens.sensor.isp_modules.ToneMapping
    options:
      members: false

::: deeplens.sensor.isp_modules.DeadPixelCorrection
    options:
      members: false

::: deeplens.sensor.isp_modules.Denoise
    options:
      members: false

::: deeplens.sensor.isp_modules.LensShadingCorrection
    options:
      members: false

::: deeplens.sensor.isp_modules.AntiAliasingFilter
    options:
      members: false

::: deeplens.sensor.isp_modules.ColorSpaceConversion
    options:
      members: false

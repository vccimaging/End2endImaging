# Sensor API Reference

The `end2end_imaging.sensor` module provides differentiable sensor models with noise simulation and a full image signal processing (ISP) pipeline.

---

## Sensor Models

Base sensor class.

::: end2end_imaging.sensor.Sensor

Full RGB sensor with Bayer pattern, noise model (read noise + shot noise), and ISP pipeline (black level compensation, white balance, demosaicing, color correction, gamma).

::: end2end_imaging.sensor.RGBSensor

Monochrome sensor without color filter array.

::: end2end_imaging.sensor.MonoSensor

---

## ISP Modules

Individual image signal processing stages used inside `RGBSensor`. Each module is a `torch.nn.Module`.

::: end2end_imaging.sensor.isp_modules.BlackLevelCompensation

::: end2end_imaging.sensor.isp_modules.AutoWhiteBalance

::: end2end_imaging.sensor.isp_modules.Demosaic

::: end2end_imaging.sensor.isp_modules.ColorCorrectionMatrix

::: end2end_imaging.sensor.isp_modules.GammaCorrection

::: end2end_imaging.sensor.isp_modules.ToneMapping

::: end2end_imaging.sensor.isp_modules.DeadPixelCorrection

::: end2end_imaging.sensor.isp_modules.Denoise

::: end2end_imaging.sensor.isp_modules.LensShadingCorrection

::: end2end_imaging.sensor.isp_modules.AntiAliasingFilter

::: end2end_imaging.sensor.isp_modules.ColorSpaceConversion

# Network API Reference

The `end2end_imaging.network` module provides neural networks for PSF prediction (surrogates) and image reconstruction, plus loss functions for training.

---

## Surrogate Networks

Neural networks that learn to predict PSFs from lens parameters, replacing expensive ray tracing during training.

::: end2end_imaging.network.MLP

::: end2end_imaging.network.MLPConv

::: end2end_imaging.network.surrogate.siren.Siren

::: end2end_imaging.network.ModulateSiren

---

## Reconstruction Networks

Image restoration networks that recover a clean image from a degraded (aberrated) sensor capture.

::: end2end_imaging.network.NAFNet

::: end2end_imaging.network.UNet

::: end2end_imaging.network.Restormer

---

## Loss Functions

::: end2end_imaging.network.PerceptualLoss

::: end2end_imaging.network.PSNRLoss

::: end2end_imaging.network.SSIMLoss

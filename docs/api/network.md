# Network API Reference

The `deeplens.network` module provides neural networks for PSF prediction (surrogates) and image reconstruction, plus loss functions for training.

---

## Surrogate Networks

Neural networks that learn to predict PSFs from lens parameters, replacing expensive ray tracing during training.

### MLP

::: deeplens.network.MLP
    options:
      members: ["__init__", "forward"]

### MLPConv

::: deeplens.network.MLPConv
    options:
      members: ["__init__", "forward"]

### Siren

::: deeplens.network.surrogate.siren.Siren
    options:
      members: ["__init__", "forward"]

### ModulateSiren

::: deeplens.network.ModulateSiren
    options:
      members: ["__init__", "forward"]

---

## Reconstruction Networks

Image restoration networks that recover a clean image from a degraded (aberrated) sensor capture.

### NAFNet

::: deeplens.network.NAFNet
    options:
      members: ["__init__", "forward"]

### UNet

::: deeplens.network.UNet
    options:
      members: ["__init__", "forward"]

### Restormer

::: deeplens.network.Restormer
    options:
      members: ["__init__", "forward"]

---

## Loss Functions

::: deeplens.network.PerceptualLoss
    options:
      members: false

::: deeplens.network.PSNRLoss
    options:
      members: false

::: deeplens.network.SSIMLoss
    options:
      members: false

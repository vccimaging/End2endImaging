# Network API Reference

DeepLens provides neural network modules for two purposes:

1. **Surrogate modelling** — fast MLP/SIREN networks that predict PSFs from
   `(fov, depth, focus_distance)` inputs without running ray tracing.
2. **Image reconstruction** — standard restoration networks (NAFNet, UNet,
   Restormer) used in end-to-end computational imaging pipelines.

## Surrogate Networks

### MLP

::: deeplens.network.MLP
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### MLPConv

::: deeplens.network.MLPConv
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### Siren

::: deeplens.network.Siren
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### ModulateSiren

::: deeplens.network.ModulateSiren
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Reconstruction Networks

### NAFNet

::: deeplens.network.NAFNet
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### UNet

::: deeplens.network.UNet
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

### Restormer

::: deeplens.network.Restormer
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## Loss Functions

::: deeplens.network.PerceptualLoss
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.network.PSNRLoss
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

::: deeplens.network.SSIMLoss
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true

## Datasets

::: deeplens.network.ImageDataset
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

::: deeplens.network.PhotographicDataset
    options:
      members: true
      show_source: false
      docstring_style: google
      show_root_heading: true
      members_order: source

## See Also

- [Neural Networks User Guide](../user_guide/neural_networks.md) — Neural network user guide
- [HybridLens](hybridlens.md) — `PSFNetLens` (surrogate lens model)

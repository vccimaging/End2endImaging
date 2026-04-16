# Quickstart

This guide walks through the core workflow: loading a lens, computing PSFs, and rendering images.

## Load a Lens

`GeoLens` is the primary lens model — a differentiable multi-element refractive lens loaded from a JSON, Zemax `.zmx`, or Code V `.seq` file.

```python
from end2end_imaging import GeoLens

lens = GeoLens(filename="datasets/lenses/cellphone/cellphone80deg.json")
lens.analysis()
```

## Compute a PSF

The point spread function (PSF) describes how the lens images a point source at a given field position and wavelength.

```python
# Single on-axis PSF (monochromatic)
psf = lens.psf(points=[0.0, 0.0, -10000.0], ks=128, wvln=0.589)

# RGB PSF (weighted sum over visible wavelengths)
psf_rgb = lens.psf_rgb(points=[0.0, 0.0, -10000.0], ks=128)
```

## Render an Image

Use the `Camera` class to simulate a physically accurate image capture — including lens aberrations, sensor noise, and ISP processing:

```python
from end2end_imaging import Camera

camera = Camera(
    lens_file="datasets/lenses/cellphone/cellphone80deg.json",
    sensor_file="datasets/sensors/imx586.json",
)

# Prepare input data
data_dict = {
    "img": img_srgb,             # sRGB image, shape (B, 3, H, W), range [0, 1]
    "iso": iso,                  # ISO value, shape (B,)
    "field_center": field_center, # field position, shape (B, 2), range [-1, 1]
}

# Simulate camera capture (lens aberration + sensor noise)
data_lq, data_gt = camera.render(data_dict, render_mode="psf_map")
```

## End-to-End Camera Design

Jointly optimize a lens and a neural image processing network. The `Camera` generates training data by simulating realistic image degradation, and the network learns to restore the image:

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import NAFNet

# Initialize camera and restoration network
camera = Camera(
    lens_file="datasets/lenses/cellphone/cellphone80deg.json",
    sensor_file="datasets/sensors/imx586.json",
)
network = NAFNet(in_chan=3, out_chan=3)
optimizer = torch.optim.Adam(network.parameters(), lr=1e-4)

for step in range(num_steps):
    optimizer.zero_grad()

    # Simulate camera capture
    data_lq, data_gt = camera.render(data_dict, render_mode="psf_map")

    # Restore the degraded image
    restored = network(data_lq)
    loss = torch.nn.functional.l1_loss(restored, data_gt)

    loss.backward()
    optimizer.step()
```

See `7_comp_photography.py` for a full training example with distributed data parallel (DDP) support.

## Lens Types

Several lens models are available for different use cases:

| Lens Type | Description | Use Case |
|-----------|-------------|----------|
| `GeoLens` | Multi-element refractive ray tracing | Automated lens design, image simulation |
| `HybridLens` | Refractive lens + diffractive optical element | Hybrid optics co-design |
| `DiffractiveLens` | Pure wave-optics diffractive surfaces | Flat optics, DOE design |
| `PSFNetLens` | Neural network PSF surrogate | Fast PSF approximation |
| `ParaxialLens` | Thin-lens / circle-of-confusion model | Simple bokeh simulation |

## Next Steps

- [API Reference](api/optics.md) — full documentation for all classes
- [Examples](examples.md) — lens design, end-to-end optimization, and more

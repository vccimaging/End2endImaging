# End2endImaging

**End-to-end differentiable simulation framework for computational imaging.**

End2endImaging models the full imaging pipeline — optics, sensor, and image processing — as a differentiable computation graph built on PyTorch. This enables gradient-based optimization of camera systems from lens surfaces all the way through neural image reconstruction.

```
Scene → [ DeepLens ] → [ Sensor ] → [ Network ] → Output Image
              │              │             │
           GeoLens       RGBSensor       UNet
         HybridLens      MonoSensor     Restormer
        DiffractiveLens                 NAFNet
         ParaxialLens
         PSFNetLens
```

---

## Installation

**Prerequisites:** Python >= 3.12, CUDA-capable GPU (recommended)

```bash
git clone https://github.com/vccimaging/End2endImaging.git
cd End2endImaging
pip install -r requirements.txt
```

**Conda environment (recommended):**

```bash
conda create -n end2end_env python=3.12
conda activate end2end_env

# Linux and Mac
pip install torch torchvision
# Windows
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

pip install -r requirements.txt
```

Or use the provided environment file:

```bash
conda env create -f environment.yml -n end2end_env
```

---

## Quickstart

### Load a Lens

`GeoLens` is the primary lens model — a differentiable multi-element refractive lens loaded from a JSON, Zemax `.zmx`, or Code V `.seq` file.

```python
from end2end_imaging import GeoLens

lens = GeoLens(filename="datasets/lenses/cellphone/cellphone80deg.json")
lens.analysis()
```

### Compute a PSF

The point spread function (PSF) describes how the lens images a point source at a given field position and wavelength.

```python
# Single on-axis PSF (monochromatic)
psf = lens.psf(points=[0.0, 0.0, -10000.0], ks=128, wvln=0.589)

# RGB PSF (weighted sum over visible wavelengths)
psf_rgb = lens.psf_rgb(points=[0.0, 0.0, -10000.0], ks=128)
```

### Render an Image

Use the `Camera` class to simulate a physically accurate image capture — including lens aberrations, sensor noise, and ISP processing:

```python
from end2end_imaging import Camera

camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)

# Prepare input data
data_dict = {
    "img": img_srgb,             # sRGB image, shape (B, 3, H, W), range [0, 1]
    "iso": iso,                  # ISO value, shape (B,)
    "field_center": field_center, # field position, shape (B, 2), range [-1, 1]
}

# Simulate camera capture (lens aberration + sensor noise)
data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")
```

### End-to-End Camera Design

Jointly optimize a lens and a neural image processing network. The `Camera` generates training data by simulating realistic image degradation, and the network learns to restore the image:

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import NAFNet

# Initialize camera and restoration network
camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)
network = NAFNet(in_chan=3, out_chan=3)
optimizer = torch.optim.Adam(network.parameters(), lr=1e-4)

for step in range(num_steps):
    optimizer.zero_grad()

    # Simulate camera capture
    data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")

    # Restore the degraded image
    restored = network(data_lq)
    loss = torch.nn.functional.l1_loss(restored, data_gt)

    loss.backward()
    optimizer.step()
```

See `7_comp_photography.py` for a full training example.

---

## Architecture

### Lens Types

| Lens Type | Description | Use Case |
|-----------|-------------|----------|
| `GeoLens` | Multi-element refractive ray tracing | Automated lens design, image simulation |
| `HybridLens` | Refractive lens + diffractive optical element | Hybrid optics co-design |
| `DiffractiveLens` | Pure wave-optics diffractive surfaces | Flat optics, DOE design |
| `PSFNetLens` | Neural network PSF surrogate | Fast PSF approximation |
| `ParaxialLens` | Thin-lens / circle-of-confusion model | Simple bokeh simulation |

### Code Structure

```
end2end_imaging/
├── camera.py                    # Camera = Lens + Sensor pipeline
├── utils.py                     # Image I/O, metrics, logging
│
├── deeplens/                    # Differentiable optics
│   ├── geolens.py               #   GeoLens — refractive ray tracing
│   ├── hybridlens.py            #   HybridLens — refractive + DOE
│   ├── diffraclens.py           #   DiffractiveLens — wave optics
│   ├── paraxiallens.py          #   ParaxialLens — thin lens model
│   ├── psfnetlens.py            #   PSFNetLens — neural PSF surrogate
│   ├── geolens_pkg/             #   GeoLens evaluation, optimization, I/O, visualization
│   ├── geometric_surface/       #   Refractive surfaces (spheric, aspheric, ...)
│   ├── diffractive_surface/     #   Diffractive elements (wave optics simulation)
│   ├── phase_surface/           #   Phase surfaces (ray optics simulation)
│   ├── light/                   #   Ray and ComplexWave representations
│   ├── material/                #   Glass & plastic catalogs (Sellmeier, AGF)
│   └── imgsim/                  #   PSF convolution & Monte Carlo rendering
│
├── sensor/                      # Sensor simulation
│   ├── rgb_sensor.py            #   RGBSensor (Bayer + noise + ISP)
│   ├── mono_sensor.py           #   MonoSensor
│   └── isp_modules/             #   ISP pipeline (demosaic, white balance, gamma, ...)
│
└── network/                     # Neural networks
    ├── surrogate/               #   PSF surrogate networks (MLP, SIREN, ...)
    ├── reconstruction/          #   Image reconstruction (UNet, Restormer, ...)
    └── loss/                    #   Training losses (perceptual, PSNR, SSIM)
```

---

## Next Steps

- [API Reference](api/deeplens.md) — full class and function documentation
- [Examples](examples/index.md) — lens design, end-to-end optimization, and more
- [Contributing](contributing.md) — development setup and guidelines

# Architecture

End2endImaging models the full imaging pipeline as three differentiable modules connected by a `Camera` class.

```
Scene → [ DeepLens ] → [ Sensor ] → [ Network ] → Output Image
              │              │             │
           GeoLens       RGBSensor       UNet
         HybridLens      MonoSensor     Restormer
        DiffractiveLens                 Diffusion
         ParaxialLens
         PSFNetLens
```

## Code Structure

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

## Camera

The `Camera` class (`end2end_imaging/camera.py`) connects a `Lens` and a `Sensor` into an end-to-end differentiable pipeline:

```python
from end2end_imaging import GeoLens, Camera
from end2end_imaging.sensor import RGBSensor

lens = GeoLens(filename="datasets/lenses/cellphone/cellphone80deg.json")
sensor = RGBSensor(res=(1920, 1080))
camera = Camera(lens=lens, sensor=sensor)
```

Gradients flow through the entire pipeline — from the reconstruction loss back through the network, sensor, and into the lens surface parameters — enabling joint optimization of optics and algorithms.

## DeepLens 
The `end2end_imaging.deeplens` module contains differentiable lens models that simulate how light passes through an optical system. Two image simulation methods are supported: (1) **PSF-based simulation**, where the lens computes a point spread function and renders images via PSF convolution (all lens types), and (2) **ray tracing-based rendering**, where rays are traced from the scene through the lens to the sensor to produce images directly (currently supported in `GeoLens` only).

- **`GeoLens`** — Multi-element refractive lens via differentiable ray tracing. The primary lens model, supporting Zemax/Code V/JSON file I/O. Uses a mixin architecture for PSF computation, evaluation, Seidel aberration analysis, optimization, surface operations, visualization, and tolerancing.
- **`HybridLens`** — Refractive lens (`GeoLens`) with a diffractive optical element (DOE) placed behind it. Coherent ray tracing through the refractive elements to the DOE plane, then Angular Spectrum Method (ASM) propagation to the sensor.
- **`DiffractiveLens`** — Pure wave-optics lens using diffractive surfaces and scalar diffraction.
- **`PSFNetLens`** — Neural surrogate wrapping a `GeoLens` with an MLP for fast PSF prediction.
- **`ParaxialLens`** — Thin-lens model for simple depth-of-field and bokeh simulation.

All lens types inherit from `Lens`, which defines the shared interface (`psf()`, `render()`, etc.). All optical objects inherit from `DeepObj`, which provides `to(device)`, `clone()`, and dtype conversion.

## Sensor

The `end2end_imaging.sensor` module simulates the image sensor and its signal processing pipeline.

- **`RGBSensor`** — Full RGB sensor with Bayer color filter array, read/shot noise model, and an ISP pipeline (black level compensation, white balance, demosaicing, color correction, gamma correction).
- **`MonoSensor`** — Monochrome sensor without a color filter array.
The ISP pipeline is built from composable `torch.nn.Module` stages in `sensor/isp_modules/`.

## Network

The `end2end_imaging.network` module provides neural networks for two purposes:

- **PSF surrogates** — Networks that learn to predict PSFs from lens parameters, replacing ray tracing during training: `MLP`, `MLPConv`, `Siren`, `ModulateSiren`.
- **Image reconstruction** — Networks that restore a clean image from a degraded sensor capture: `NAFNet`, `UNet`, `Restormer`.

Loss functions (`PerceptualLoss`, `PSNRLoss`, `SSIMLoss`) are also provided for training.

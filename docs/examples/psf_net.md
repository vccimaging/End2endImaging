# PSF Surrogate Network

Train a neural network to predict the spatially-varying PSF of a lens, replacing expensive ray tracing with a fast forward pass during training.

**Script:** `3_psf_net.py`

**Reference:** Xinge Yang, Qiang Fu, Mohammed Elhoseiny and Wolfgang Heidrich, "Aberration-Aware Depth-from-Focus," *IEEE TPAMI* 2023.

## Overview

`PSFNetLens` wraps a `GeoLens` with an MLP that learns to map (field of view, depth, focus distance) to an RGB PSF. Once trained, PSF prediction is orders of magnitude faster than ray tracing.

```python
from end2end_imaging.deeplens import PSFNetLens

# Input (B, 3): (fov, depth, foc_dist)
# Output (B, 3, ks, ks): RGB PSF at the given configuration
psfnet = PSFNetLens(
    filename="datasets/lenses/cellphone/cellphone80deg.json",
    ks=64,
)

# Train the surrogate on ray-traced PSF data
psfnet.fit(epochs=100, lr=1e-3)

# Fast inference
psf = psfnet.psf(fov=0.5, depth=5000, foc_dist=10000)
```

## Usage

```bash
python 3_psf_net.py
```

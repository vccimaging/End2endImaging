# Hybrid Refractive-Diffractive Lens Design

Jointly optimize a refractive lens with a diffractive optical element (DOE) using a differentiable ray-wave model that combines geometric ray tracing with wave optics propagation.

**Script:** `6_hybridlens_design.py`

**Reference:** Xinge Yang, Matheus Souza, Kunyi Wang, Praneeth Chakravarthula, Qiang Fu and Wolfgang Heidrich, "End-to-End Hybrid Refractive-Diffractive Lens Design with Differentiable Ray-Wave Model," *SIGGRAPH Asia* 2024.

## Overview

`HybridLens` combines a `GeoLens` (refractive elements) with a diffractive surface. Light is traced through the refractive elements via ray tracing, then propagated through the DOE using the Angular Spectrum Method (ASM).

```python
from end2end_imaging.deeplens import HybridLens

# Create hybrid lens from a refractive starting point
lens = HybridLens(
    filename="datasets/lenses/cellphone/cellphone80deg.json",
    doe_res=1024,
)

# Compute PSF (coherent ray tracing + ASM propagation)
psf = lens.psf(point=[0.0, 0.0, -10000.0], ks=128, wvln=0.589)

# Optimize both refractive surfaces and DOE phase profile
optimizer = torch.optim.Adam(lens.parameters(), lr=1e-3)

for step in range(num_steps):
    optimizer.zero_grad()
    loss = lens.loss_psf()
    loss.backward()
    optimizer.step()
```

## Usage

```bash
python 6_hybridlens_design.py
```

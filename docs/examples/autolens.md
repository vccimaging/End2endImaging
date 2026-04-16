# Automated Lens Design

Design a multi-element lens from scratch using RMS spot size as the optimization objective. This is much faster than image-based lens design and demonstrates the core differentiable optics capability.

**Script:** `2_autolens_rms.py`

**Reference:** Xinge Yang, Qiang Fu and Wolfgang Heidrich, "Curriculum learning for ab initio deep learned refractive optics," *Nature Communications* 2024.

## Overview

Load a starting lens (or create one from scratch), set target specs (field of view, f-number), and optimize surface parameters with gradient descent to minimize RMS spot size across field angles.

```python
import torch
from end2end_imaging import GeoLens

# Load a starting lens design
lens = GeoLens(filename="datasets/lenses/cellphone/cellphone80deg.json")

# Set target specs and build optimizer
lens.set_target_fov_fnum(rfov=40, fnum=2.4)  # 40 deg half-diagonal FoV, F/2.4
optimizer = lens.get_optimizer(lrs=[1e-4, 1e-4, 1e-1, 1e-4])

for step in range(200):
    optimizer.zero_grad()

    # Compute RMS spot size across field angles
    loss = lens.loss_rms()

    loss.backward()
    optimizer.step()

    if step % 50 == 0:
        print(f"Step {step}: RMS spot loss = {loss.item():.4f}")

# Visualize the optimized lens
lens.draw2d()
```

## Usage

```bash
python 2_autolens_rms.py
```

Also see [AutoLens](https://github.com/vccimaging/AutoLens) for a more complete automated lens design pipeline.

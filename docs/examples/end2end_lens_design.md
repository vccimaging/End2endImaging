# End-to-End Lens Design

Jointly optimize lens optics and a neural reconstruction network, using final image quality as the training objective. This is the core end-to-end co-design workflow.

**Script:** `1_end2end_lens_design.py`

**Reference:** Xinge Yang, Qiang Fu and Wolfgang Heidrich, "Curriculum learning for ab initio deep learned refractive optics," *Nature Communications* 2024.

## Overview

The pipeline builds a differentiable `Camera` (lens + sensor), renders degraded images through it, and trains a reconstruction network to restore them. Gradients flow end-to-end from the reconstruction loss back into the lens surface parameters.

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import NAFNet

# Build camera pipeline
camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)
network = NAFNet(in_chan=3, out_chan=3)

# Optimizers for optics and network
opt_lens = torch.optim.Adam(camera.lens.parameters(), lr=1e-4)
opt_net = torch.optim.Adam(network.parameters(), lr=1e-4)

for step in range(num_steps):
    opt_lens.zero_grad()
    opt_net.zero_grad()

    # Simulate camera capture
    data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")

    # Restore and compute loss
    restored = network(data_lq)
    loss = torch.nn.functional.l1_loss(restored, data_gt)

    loss.backward()
    opt_lens.step()
    opt_net.step()
```

## Usage

```bash
python 1_end2end_lens_design.py
```

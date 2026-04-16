# Computational Photography

Train an image restoration network using physically accurate camera simulation. The `Camera` class generates realistic training data with lens aberrations and sensor noise, and the network learns to restore clean images.

**Script:** `7_comp_photography.py`

**Reference:** Xinge Yang, Chuong Nguyen, Wenbin Wang, Kaizhang Kang, Wolfgang Heidrich, Xiaoxing Li, "Efficient Depth- and Spatially-Varying Image Simulation for Defocus Deblur," *ICCV Workshop* 2025.

## Overview

This is the full training pipeline for computational photography: load a camera model, generate degraded/clean image pairs by simulating the imaging process, and train a restoration network (NAFNet) to recover the clean image.

```python
import torch
from end2end_imaging import Camera
from end2end_imaging.network import NAFNet

# Build camera pipeline
camera = Camera(
    lens_file="datasets/lenses/camera/rf50mm_f1.8.json",
    sensor_file="datasets/sensors/canon_r6.json",
)

# Restoration network
network = NAFNet(in_chan=3, out_chan=3)
optimizer = torch.optim.Adam(network.parameters(), lr=1e-4)

for step in range(num_steps):
    optimizer.zero_grad()

    # Simulate camera capture (lens aberration + sensor noise)
    data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch")

    # Restore the degraded image
    restored = network(data_lq)
    loss = torch.nn.functional.l1_loss(restored, data_gt)

    loss.backward()
    optimizer.step()
```

## Usage

```bash
python 7_comp_photography.py
```

# Task-Driven Lens Design

Design a lens from scratch using only a downstream task loss (image classification), with no classical optical design objectives (spot size, PSF, MTF). This explores unconventional lens designs optimized purely for task performance.

**Script:** `4_tasklens_img_classi.py`

**Reference:** Xinge Yang, Yunfeng Nie, Qiang Fu and Wolfgang Heidrich, "Image Quality Is Not All You Want: Task-Driven Lens Design for Image Classification," *arXiv* 2023.

## Overview

A `GeoLens` renders images through the differentiable camera pipeline, and a pretrained classifier (e.g. ResNet via `timm`) provides the training signal. The lens parameters are optimized to maximize classification accuracy rather than traditional image quality metrics.

```python
import timm
import torch
from end2end_imaging import GeoLens

# Load lens and classifier
lens = GeoLens(filename="datasets/lenses/cellphone/cellphone80deg.json")
classifier = timm.create_model("resnet50", pretrained=True)

# Optimize lens for classification accuracy
opt_lens = torch.optim.Adam(lens.parameters(), lr=1e-4)

for step in range(num_steps):
    opt_lens.zero_grad()

    # Render through lens and classify
    img_degraded = lens.render(img_batch, method="psf_patch")
    logits = classifier(img_degraded)
    loss = torch.nn.functional.cross_entropy(logits, labels)

    loss.backward()
    opt_lens.step()
```

## Usage

```bash
python 4_tasklens_img_classi.py
```

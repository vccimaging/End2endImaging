# Installation

## Prerequisites

- Python >= 3.12
- CUDA-capable GPU (recommended for performance)

## Install from GitHub

```bash
git clone https://github.com/vccimaging/End2endImaging.git
cd End2endImaging
pip install -r requirements.txt
```

## Conda Environment (Recommended)

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

## Verify GPU Support

```python
import torch
print(torch.cuda.is_available())  # Should print True
```

## Troubleshooting

**`torch.cuda.is_available()` returns `False`:**
Install PyTorch with CUDA support following [pytorch.org](https://pytorch.org/get-started/locally/).

**Import errors after install:**
Make sure you're using Python >= 3.12:

```bash
python --version
```

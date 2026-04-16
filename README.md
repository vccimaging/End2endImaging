# End2endImaging

<p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.0+-ee4c2c?logo=pytorch&logoColor=white" alt="PyTorch"></a>
    <a href="https://www.nature.com/articles/s41467-024-50835-7"><img src="https://img.shields.io/badge/NatComm-2024-orange" alt="Nature Communications 2024"></a>
    <a href="https://github.com/vccimaging/End2endImaging/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-green" alt="License"></a>
</p>

**End2endImaging** is an open-source framework for **end-to-end differentiable computational imaging**. It models the full camera pipeline — differentiable optics, sensor simulation, and neural image processing — as a single computation graph in PyTorch, enabling **optics-algorithm co-design** through gradient-based optimization.

<div align="center">
    <img src="assets/pipeline.jpg" alt="End2endImaging pipeline: differentiable optics, sensor simulation, and neural network for end-to-end computational imaging" width="80%"/>
</div>

<p align="center">
    <a href="https://vccimaging.github.io/End2endImaging/">Docs</a> •
    <a href="#community">Community</a> •
    <a href="#citation">Citation</a>
</p>

## End-to-End Differentiable Pipeline

The core of End2endImaging is the `Camera` class, which composes a lens model and a sensor into a fully differentiable imaging pipeline. Gradients flow from downstream task losses (reconstruction, detection, classification) back through the neural network, sensor noise model, ISP, and into the optical design parameters — enabling hardware-software co-optimization.

#### Differentiable Optics ([DeepLens](https://github.com/vccimaging/DeepLens))

The [`deeplens/`](end2end_imaging/deeplens/) module provides differentiable lens models for optical simulation and design:

- **GeoLens** — Multi-element refractive lens via differentiable ray tracing. Supports Zemax/Code V/JSON I/O, automated lens design, Seidel aberration analysis, and tolerancing.
- **HybridLens** — Refractive lens + diffractive optical element (DOE). Coherent ray tracing + Angular Spectrum Method propagation.
- **DiffractiveLens** — Pure wave-optics lens using diffractive surfaces and scalar diffraction.
- **PSFNetLens** — Neural surrogate wrapping a GeoLens with an MLP for fast PSF prediction.
- **ParaxialLens** — Thin-lens model for depth-of-field and bokeh simulation.

#### Sensor & ISP Simulation
Physically accurate sensor simulation with Bayer CFA, read/shot noise model, and a composable ISP pipeline (black level, white balance, demosaicing, color correction, gamma, tone mapping). Each stage is a differentiable `torch.nn.Module`.

#### Neural Networks
Built-in reconstruction networks (NAFNet, UNet, Restormer) for restoring clean images from degraded sensor captures, plus PSF surrogate networks (MLP, SIREN) for fast PSF prediction during training.

#### Additional features (available upon inquiry):

- **Kernel Acceleration.** >10x speedup and >90% GPU memory reduction with custom GPU kernels (NVIDIA & AMD).
- **Distributed Optimization.** Distributed simulation for billions of rays and high-resolution (>100k) diffractive computations.

## Applications

#### 1. End-to-End Optics-Algorithm Co-Design

Jointly optimize lens optics and neural reconstruction networks using final image quality (or classification/detection/segmentation) as the training objective. Gradients flow end-to-end from task loss into optical design parameters.

[![paper](https://img.shields.io/badge/NatComm-2024-orange)](https://www.nature.com/articles/s41467-024-50835-7)

<div align="center">
    <img src="assets/end2end.png" alt="End-to-end optics-algorithm co-design: jointly optimizing lens and neural network" height="150px"/>
</div>

#### 2. Automated Lens Design

Fully automated lens design from scratch using curriculum learning and differentiable optimization. Design camera lenses, cellphone lenses, and AR/VR optics with gradient descent. Try it with [AutoLens](https://github.com/vccimaging/AutoLens)!

[![paper](https://img.shields.io/badge/NatComm-2024-orange)](https://www.nature.com/articles/s41467-024-50835-7) [![quickstart](https://img.shields.io/badge/Project-green)](https://github.com/vccimaging/AutoLens)

<div align="center">
    <img src="assets/autolens1.gif" alt="Automated lens design optimization with differentiable ray tracing" height="270px"/>
    <img src="assets/autolens2.gif" alt="Curriculum learning for ab initio lens design" height="270px"/>
</div>

#### 3. Hybrid Refractive-Diffractive Lens Design

Design hybrid refractive-diffractive lenses (DOEs, metalenses) with a differentiable ray-wave model combining geometric ray tracing and wave optics propagation.

[![report](https://img.shields.io/badge/SiggraphAsia-2024-orange)](https://arxiv.org/abs/2406.00834)

<div align="center">
    <img src="assets/hybridlens.png" alt="Hybrid refractive-diffractive lens design with differentiable ray-wave simulation" height="200px"/>
</div>

#### 4. Implicit Lens Representation

Neural surrogate network for fast aberration-aware image simulation, enabling real-time PSF prediction for computational photography applications.

[![paper](https://img.shields.io/badge/TPAMI-2023-orange)](https://ieeexplore.ieee.org/document/10209238) [![link](https://img.shields.io/badge/Project-green)](https://github.com/vccimaging/Aberration-Aware-Depth-from-Focus)

<div align="center">
    <img src="assets/implicit_net.png" alt="Neural implicit lens representation for fast PSF prediction" height="150px"/>
</div>

## Installation

Clone this repo:

```
git clone https://github.com/vccimaging/End2endImaging
cd End2endImaging
```

Create a conda environment:
```
conda create -n end2end_env python=3.12
conda activate end2end_env

# Linux and Mac
pip install torch torchvision
# Windows
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128

pip install -r requirements.txt
```
or
```
conda env create -f environment.yml -n end2end_env
```

Run the demo code:
```
python 0_hello_deeplens.py
```

## Project Structure

```
End2endImaging/
│
├── end2end_imaging/
│   ├── camera.py          # Camera: composes lens + sensor into a differentiable pipeline
│   ├── deeplens/          # Differentiable optics (lens models, surfaces, ray tracing)
│   ├── sensor/            # Sensor simulation (Bayer CFA, noise, ISP pipeline)
│   └── network/           # Neural networks (reconstruction, PSF surrogates, losses)
│
├── 0_hello_deeplens.py    # Code tutorials
├── ...
└── write_your_own_code.py
```

## Community

Join our [Slack](https://join.slack.com/t/deeplens/shared_invite/zt-2wz3x2n3b-plRqN26eDhO2IY4r_gmjOw) workspace and WeChat Group (singeryang1999) to connect with our core contributors, receive the latest industry updates, and be part of our community. For any inquiries, contact Xinge Yang (xinge.yang@kaust.edu.sa).

## Contribution

We welcome all contributions. To get started, please read our [Contributing Guide](./CONTRIBUTING.md) or check out [open questions](https://github.com/users/singer-yang/projects/2). All project participants are expected to adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md). A list of contributors can be viewed in [Contributors](./CONTRIBUTORS.md) and below:

<a href="https://github.com/singer-yang/DeepLens/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=singer-yang/DeepLens" />
</a>

## Citation

If you use this project in your research, please cite the paper. See more in [History of DeepLens](./CITATION.md).

```bibtex
@article{yang2024curriculum,
  title={Curriculum learning for ab initio deep learned refractive optics},
  author={Yang, Xinge and Fu, Qiang and Heidrich, Wolfgang},
  journal={Nature communications},
  volume={15},
  number={1},
  pages={6572},
  year={2024},
  publisher={Nature Publishing Group UK London}
}
```

<!-- Keywords: end-to-end optics design, computational imaging, differentiable optics, differentiable ray tracing, optics-algorithm co-design, computational photography, automated lens design, optical simulation, PSF simulation, image signal processing, diffractive optics, wave optics, PyTorch optics, camera simulation, inverse optical design -->

# End2endImaging

**End-to-end differentiable simulation framework for computational imaging.**

End2endImaging models the full imaging pipeline — optics, sensor, and image processing — as a differentiable computation graph built on PyTorch. This enables gradient-based optimization of camera systems from lens surfaces all the way through neural image reconstruction.

## Key Features

- **Differentiable optical simulation** for various and complex lens systems
- **End-to-end optimization** of optics, sensor, and image processing network jointly
- **Physically accurate image simulation** that bridges the sim-to-real gap

## Quick Install

```bash
git clone https://github.com/vccimaging/End2endImaging
cd End2endImaging
pip install -r requirements.txt
```

## Getting Started

- [Installation](installation.md) — detailed setup instructions
- [Quickstart](quickstart.md) — load a lens, compute a PSF, render an image
- [API Reference](api/optics.md) — full class and function documentation
- [Examples](examples.md) — lens design, end-to-end optimization, image simulation

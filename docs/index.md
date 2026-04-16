<section class="e2e-hero" markdown>

<span class="e2e-badge">Open-Source PyTorch Framework</span>

# End2endImaging

**Differentiable simulation for computational imaging** — model the full camera pipeline as one optimizable computation graph, from lens surfaces to neural reconstruction.

[Get Started](quickstart.md){ .md-button .md-button--primary }
[API Reference](api/optics.md){ .md-button }

</section>

<div class="e2e-pipeline">
  <div class="e2e-pipeline__node">Scene</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">DeepLens</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">Sensor</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">Network</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node">Output</div>
</div>

---

<div class="feature-grid" markdown>
<div class="feature-card" markdown>
### Differentiable Optics
Ray tracing through multi-element lens systems with full gradient support — optimize surfaces, curvatures, and materials with PyTorch.
</div>
<div class="feature-card" markdown>
### End-to-End Optimization
Jointly optimize optics, sensor parameters, and neural reconstruction networks in a single differentiable pipeline.
</div>
<div class="feature-card" markdown>
### Physical Accuracy
Bridge the sim-to-real gap with faithful image formation — wave optics, sensor noise models, and full ISP simulation.
</div>
</div>

---

## Quick Install

```bash
git clone https://github.com/vccimaging/End2endImaging
cd End2endImaging
pip install -r requirements.txt
```

## Get Started

<div class="feature-grid" markdown>
<div class="feature-card" markdown>
### [Installation](installation.md)
Set up your environment with conda and CUDA support
</div>
<div class="feature-card" markdown>
### [Quickstart](quickstart.md)
Load a lens, compute a PSF, render an image
</div>
<div class="feature-card" markdown>
### [API Reference](api/optics.md)
Complete class and function documentation
</div>
<div class="feature-card" markdown>
### [Examples](examples.md)
Lens design, end-to-end optimization, and simulation
</div>
</div>

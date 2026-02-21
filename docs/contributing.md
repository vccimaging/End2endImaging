# Contributing to DeepLens

We welcome contributions to DeepLens! This guide will help you get started.

## Ways to Contribute

There are many ways to contribute to DeepLens:

* **Bug Reports**: Report bugs and issues
* **Feature Requests**: Suggest new features and enhancements
* **Code Contributions**: Submit pull requests with bug fixes or new features
* **Documentation**: Improve documentation and examples
* **Testing**: Test the software and report issues
* **Community**: Help others on Slack and GitHub Discussions

## Getting Started

1. **Fork the Repository**

   Fork the DeepLens repository on GitHub:

   https://github.com/singer-yang/DeepLens

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/DeepLens.git
   cd DeepLens
   ```

3. **Set Up Development Environment**

   ```bash
   conda create -n deeplens_dev python=3.12
   conda activate deeplens_dev
   pip install -e .

   # Install development dependencies
   pip install pytest ruff
   ```

4. **Create a Branch**

   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/bug-description
   ```

## Development Guidelines

### Code Style

DeepLens follows PEP 8 style guidelines with some modifications:

* **Line Length**: Maximum 100 characters
* **Indentation**: 4 spaces (no tabs)
* **Quotes**: Use single quotes for strings
* **Imports**: Organized in groups (standard library, third-party, local)

Format code with ruff:

```bash
ruff format .
```

Lint with ruff:

```bash
ruff check .
```

### Code Structure

Follow these conventions:

**File Organization:**

```python
# Copyright and license header
# Docstring explaining the module

# Imports (grouped)
import os
import sys

import torch
import numpy as np

from deeplens.optics import Ray

# Constants
DEFAULT_WAVELENGTH = 0.550

# Classes and functions
class MyClass:
    """Class docstring."""

    def __init__(self, param):
        """Initialize with param."""
        self.param = param
```

**Docstrings:**

Use Google-style docstrings:

```python
def calculate_psf(depth, spp=2048, wavelength=0.550):
    """Calculate Point Spread Function.

    Args:
        depth (float): Object distance in mm.
        spp (int): Samples per pixel. Default: 2048.
        wavelength (float): Wavelength in micrometers. Default: 0.550.

    Returns:
        torch.Tensor: PSF tensor with shape [C, H, W].

    Raises:
        ValueError: If depth is negative.

    Example:
        >>> psf = calculate_psf(depth=1000, spp=4096)
        >>> print(psf.shape)
        torch.Size([1, 64, 64])
    """
    if depth < 0:
        raise ValueError("Depth must be positive")

    # Implementation
    return psf
```

### Testing

Write tests for new features:

```python
# tests/test_lens.py
import pytest
import torch
from deeplens import GeoLens

def test_lens_initialization():
    """Test GeoLens initialization."""
    lens = GeoLens(
        filename='./datasets/lenses/camera/ef50mm_f1.8.json',
        device='cpu'
    )
    assert lens.foclen > 0
    assert len(lens.surfaces) > 0

def test_psf_calculation():
    """Test PSF calculation."""
    lens = GeoLens(filename='./datasets/lenses/camera/ef50mm_f1.8.json')
    psf = lens.psf(points=[0.0, 0.0, -1000.0], spp=256)

    assert psf.shape[0] == 1  # Single channel
    assert psf.sum() > 0  # Non-zero PSF
    assert torch.isfinite(psf).all()  # No NaN or Inf
```

Run tests:

```bash
pytest tests/ -v
```

## Contribution Workflow

1. **Make Changes**

   Implement your feature or bug fix following the guidelines above.

2. **Test Your Changes**

   ```bash
   # Run tests
   pytest tests/

   # Check code style
   ruff format --check .
   ruff check .
   ```

3. **Commit Your Changes**

   Write clear, descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add feature: brief description

   Detailed explanation of what changed and why.
   Closes #123"
   ```

   Commit message format:

   * First line: Brief summary (50 chars or less)
   * Blank line
   * Detailed description
   * Reference issues: `Closes #123` or `Fixes #456`

4. **Push to Your Fork**

   ```bash
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**

   * Go to the DeepLens repository on GitHub
   * Click "New Pull Request"
   * Select your fork and branch
   * Fill in the PR template:

     * Description of changes
     * Related issues
     * Testing done
     * Screenshots (if applicable)

6. **Code Review**

   * Respond to reviewer comments
   * Make requested changes
   * Push updates to your branch

7. **Merge**

   Once approved, your PR will be merged by a maintainer.

## Types of Contributions

### Bug Fixes

When fixing a bug:

1. Create an issue describing the bug (if it doesn't exist)
2. Write a test that reproduces the bug
3. Fix the bug
4. Verify the test now passes
5. Submit PR referencing the issue

### New Features

For new features:

1. Discuss in an issue or Slack first
2. Design API and implementation
3. Write comprehensive tests
4. Add documentation and examples
5. Submit PR with:

   * Implementation
   * Tests
   * Documentation
   * Example usage

### Documentation

Documentation improvements are always welcome:

* Fix typos and clarify text
* Add examples
* Improve API documentation
* Write tutorials

Documentation is in `docs/` using Markdown. To build and preview locally:

```bash
pip install mkdocs-material "mkdocstrings[python]"
mkdocs serve
```

### Examples

Add examples to demonstrate features:

* Create standalone script in root directory
* Add thorough comments
* Include sample data or instructions
* Add to documentation examples section

## Code Review Guidelines

When reviewing code:

**What to Look For:**

* **Correctness**: Does the code work as intended?
* **Tests**: Are there adequate tests?
* **Documentation**: Is it well-documented?
* **Style**: Does it follow guidelines?
* **Performance**: Are there obvious inefficiencies?
* **Compatibility**: Does it break existing code?

**How to Review:**

* Be constructive and friendly
* Explain reasoning for suggestions
* Approve when ready or request changes
* Test the code if possible

## Community Guidelines

### Be Respectful

* Be welcoming to newcomers
* Be patient with questions
* Give constructive feedback
* Respect different viewpoints

### Communication

* **GitHub Issues**: Bug reports, feature requests
* **Pull Requests**: Code contributions
* **Slack**: Quick questions, discussions
* **Email**: Private matters

### Report Issues

If you encounter:

* Bugs or errors
* Security vulnerabilities
* Code of conduct violations

Report them through appropriate channels.

## Development Setup

### Advanced Setup

For development with GPU profiling and debugging:

```bash
# Install development dependencies
pip install pytest pytest-cov ruff ipdb

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_lens.py

# Run with coverage
pytest tests/ --cov=deeplens --cov-report=html

# Run only fast tests (skip slow integration tests)
pytest tests/ -m "not slow"
```

### Building Documentation

```bash
pip install mkdocs-material "mkdocstrings[python]"
mkdocs serve

# Or build static site
mkdocs build
```

## Release Process

For maintainers releasing new versions:

1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v1.2.0`
4. Push tag: `git push origin v1.2.0`
5. Create GitHub release
6. Update documentation

## License

By contributing to DeepLens, you agree that your contributions will be licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.

## Questions?

If you have questions about contributing:

* Check existing documentation
* Search GitHub issues
* Ask on Slack
* Email: xinge.yang@kaust.edu.sa

## Thank You!

Thank you for contributing to DeepLens! Your efforts help make optical simulation and design accessible to everyone.

## See Also

* [Code of Conduct](code_of_conduct.md) - Community guidelines
* [GitHub Repository](https://github.com/singer-yang/DeepLens)
* [Join Slack](https://join.slack.com/t/deeplens/shared_invite/zt-2wz3x2n3b-plRqN26eDhO2IY4r_gmjOw)

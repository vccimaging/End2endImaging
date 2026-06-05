"""Regression tests for ISP module fixes.

Covers:
- OpenISP must construct as a proper ``nn.Module`` (regression: a missing
  ``super().__init__()`` call made construction raise ``AttributeError``).
- GammaCorrection.reset_augmentation() must be safe to call before any
  augmentation has been sampled (regression: it raised ``AttributeError``
  because ``gamma_param_org`` was created lazily in sample_augmentation()).
"""

import torch
import torch.nn as nn

from end2end_imaging.sensor.isp_modules.gamma_correction import GammaCorrection
from end2end_imaging.sensor.isp_modules.isp import OpenISP


class TestOpenISPInit:
    """OpenISP must initialize the nn.Module machinery."""

    def test_openisp_constructs(self):
        """OpenISP() builds without raising (needs super().__init__())."""
        isp = OpenISP()
        assert isinstance(isp, nn.Module)

    def test_openisp_registers_pipeline_submodule(self):
        """The internal pipeline is registered as a child module."""
        isp = OpenISP()
        child_names = [name for name, _ in isp.named_children()]
        assert "isp_pipeline" in child_names


class TestGammaCorrectionAugmentationReset:
    """reset_augmentation() must not depend on sample_augmentation() running first."""

    def test_reset_before_sample_is_safe(self):
        """reset_augmentation() before any sampling must not raise."""
        gamma = GammaCorrection(gamma_param=2.2)
        gamma.reset_augmentation()
        assert torch.allclose(gamma.gamma_param, torch.tensor(2.2))

    def test_sample_then_reset_restores_original(self):
        """After sampling, reset_augmentation() restores the original gamma."""
        gamma = GammaCorrection(gamma_param=2.2)
        original = gamma.gamma_param.clone()
        gamma.sample_augmentation()
        gamma.reset_augmentation()
        assert torch.allclose(gamma.gamma_param, original)

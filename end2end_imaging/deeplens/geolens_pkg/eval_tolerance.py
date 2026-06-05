# Copyright 2026 KAUST Computational Imaging Group, Xinge Yang and DeepLens contributors.
# This file is part of DeepLens (https://github.com/singer-yang/DeepLens).
#
# Licensed under the Apache License, Version 2.0.
# See LICENSE file in the project root for full license information.

"""Tolerance analysis compatibility helpers for ``GeoLens``."""

import numpy as np
import torch

from ..config import SPP_CALC


class GeoLensTolerance:
    """Mixin providing manufacturing tolerance APIs for ``GeoLens``."""

    def init_tolerance(self, tolerance_params=None):
        """Initialize tolerance parameters for all surfaces."""
        if tolerance_params is None:
            tolerance_params = {}

        for surface in self.surfaces:
            surface.init_tolerance(tolerance_params=tolerance_params)

    @torch.no_grad()
    def sample_tolerance(self):
        """Apply random manufacturing errors to all surfaces and refocus."""
        for surface in self.surfaces:
            surface.sample_tolerance()
        self.refocus()

    @torch.no_grad()
    def zero_tolerance(self):
        """Clear manufacturing errors from all surfaces and refocus."""
        for surface in self.surfaces:
            surface.zero_tolerance()
        self.refocus()

    def tolerancing_sensitivity(self, tolerance_params=None):
        """Estimate first-order tolerance sensitivity using surface gradients."""
        self.init_tolerance(tolerance_params=tolerance_params)

        self.get_optimizer_params()
        loss = self.loss_rms()
        loss.backward()

        sensitivity_results = {}
        for surface in self.surfaces:
            sensitivity_results.update(surface.sensitivity_score())

        tolerancing_score = sum(
            value for key, value in sensitivity_results.items() if key.endswith("_score")
        )
        loss_rss = torch.sqrt(loss.detach() ** 2 + torch.as_tensor(tolerancing_score)).item()
        sensitivity_results["loss_nominal"] = round(loss.item(), 6)
        sensitivity_results["loss_rss"] = round(loss_rss, 6)
        return sensitivity_results

    @torch.no_grad()
    def tolerancing_monte_carlo(self, trials=200, spp=SPP_CALC, tolerance_params=None):
        """Run a lightweight Monte Carlo tolerance estimate."""
        self.init_tolerance(tolerance_params=tolerance_params)

        def merit_func():
            try:
                psf = self.psf(points=[0, 0, self.obj_depth], spp=spp, recenter=True)
                return float(psf.max().detach().cpu())
            except RuntimeError:
                return 0.0

        baseline_merit = merit_func()
        merit_values = []
        for _ in range(trials):
            for surface in self.surfaces:
                surface.sample_tolerance()
            self.d_sensor = self.calc_sensor_plane()
            merit_values.append(merit_func())
            for surface in self.surfaces:
                surface.zero_tolerance()

        self.refocus()
        merit_values = np.array(merit_values, dtype=float)
        return {
            "method": "monte_carlo",
            "trials": trials,
            "baseline_merit": round(baseline_merit, 6),
            "merit_std": round(float(np.std(merit_values)), 6),
            "merit_mean": round(float(np.mean(merit_values)), 6),
        }

    def tolerancing_wavefront(self, tolerance_params=None):
        """Placeholder for wavefront-differential tolerancing."""
        return None

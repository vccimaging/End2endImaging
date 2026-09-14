"""Compatibility helpers for the embedded DeepLens package."""

from functools import wraps

import torch


def accept_legacy_surface_distance(cls):
    """Accept the pre-``d_next`` constructor keyword and attribute name."""
    original_init = cls.__init__

    @wraps(original_init)
    def init_with_legacy_distance(self, *args, **kwargs):
        legacy_position = None
        if "d" in kwargs:
            if "d_next" in kwargs:
                raise TypeError("Specify only one of 'd' and 'd_next'.")
            legacy_position = kwargs.pop("d")
            kwargs["d_next"] = legacy_position
        original_init(self, *args, **kwargs)
        if legacy_position is not None:
            self._legacy_d = torch.as_tensor(
                legacy_position,
                dtype=self.d_next.dtype,
                device=self.d_next.device,
            )

    cls.__init__ = init_with_legacy_distance

    if not hasattr(cls, "d"):
        cls.d = property(
            lambda self: getattr(self, "_legacy_d", self.d_next),
            lambda self, value: setattr(
                self,
                "_legacy_d" if hasattr(self, "_legacy_d") else "d_next",
                value,
            ),
            doc="Backward-compatible absolute position or d_next alias.",
        )

    return cls

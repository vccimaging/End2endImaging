"""DWDN integration: centered PSFs, CUDA gradients, and optimizer updates."""

import pytest
import torch

from end2end_imaging.network import DWDN


def test_dwdn_wiener_and_training_step(device):
    torch.manual_seed(42)
    kernels = torch.zeros(4, 5, 5, device=device)
    kernels[:, 2, 2] = 1
    model = DWDN(
        kernels, feat=8, width=8, enc_blk_nums=(1,), dec_blk_nums=(1,)
    ).to(device)
    image = torch.rand(2, 12, 31, 35, device=device, requires_grad=True)
    features = torch.rand(2, 8, 31, 35, device=device)
    padded = model._padded_kernel(kernels[0], 31, 35)
    # A delta PSF with the initial SNR of one has exactly one-half gain.
    torch.testing.assert_close(model.wiener(features, padded), features / 2)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    before = model.wiener.log_snr.detach().clone()
    output = model(image)
    assert output.shape == (2, 26, 31, 35)
    assert torch.isfinite(output).all()
    output.square().mean().backward()
    assert image.grad is not None and torch.isfinite(image.grad).all()
    gradients = [p.grad for p in model.parameters() if p.grad is not None]
    assert gradients and all(torch.isfinite(g).all() for g in gradients)
    assert model.wiener.log_snr.grad.abs().sum() > 0
    optimizer.step()
    assert not torch.equal(before, model.wiener.log_snr)
    torch.testing.assert_close(model.kernels, kernels)

    with pytest.raises(ValueError, match="requires input H,W"):
        model(torch.rand(1, 12, 4, 8, device=device))

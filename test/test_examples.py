"""Regression coverage for the task-driven lens-design example."""

from pathlib import Path
import runpy

from PIL import Image
import torch
import yaml


def test_tasklens_training_and_validation(tmp_path, sample_singlet_lens):
    root = Path(__file__).resolve().parents[1]
    example = runpy.run_path(str(root / "4_tasklens_img_classi.py"))
    args = yaml.load((root / "configs/4_tasklens.yml").read_text(), Loader=yaml.FullLoader)
    images = tmp_path / "images" / "class0"
    images.mkdir(parents=True)
    for index in range(3):
        Image.new("RGB", (32, 32), (80 + index * 20, 110, 140)).save(images / f"{index}.png")

    lens = sample_singlet_lens
    args.update(device=lens.device, result_dir=str(tmp_path))
    args["imagenet_train_dir"] = args["imagenet_val_dir"] = str(images.parent)
    args["train"].update(epochs=1, bs=2, img_res=(32, 32), psf_grid=2, psf_ks=15, spp=64)
    net = torch.nn.Sequential(
        torch.nn.BatchNorm2d(3),
        torch.nn.AdaptiveAvgPool2d(1),
        torch.nn.Flatten(),
        torch.nn.Linear(3, 2),
    ).to(lens.device)
    with torch.no_grad():
        net[-1].weight[0].fill_(0.05)
        net[-1].weight[1].fill_(-0.05)
        net[-1].bias.copy_(torch.tensor([1.0, 0.0], device=lens.device))
    net.requires_grad_(False)
    batch_sizes = []
    hook = net.register_forward_hook(lambda module, inputs, output: batch_sizes.append(output.shape[0]))
    try:
        example["train"](args, lens, net)
    finally:
        hook.remove()

    # One training field, four validation fields, including the final short batch.
    assert batch_sizes == [2, 1, 8, 4]
    assert args["val_acc"] == 1.0
    assert torch.equal(net[0].running_mean, torch.zeros_like(net[0].running_mean))
    assert (tmp_path / "epoch1.json").is_file()
    assert not (tmp_path / "epoch2.json").exists()

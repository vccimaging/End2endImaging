"""Hello End2endImaging — Image simulation with Camera.

Simulates a photograph through the full differentiable camera pipeline:
lens aberration (PSF convolution) + sensor noise + ISP.

Usage:
    python 0_hello_deeplens.py

References:
    [1] Xinge Yang, Qiang Fu, Wolfgang Heidrich, "Curriculum learning for ab initio
        deep learned refractive optics," Nature Communications 2024.
"""

import torch
import torchvision
import os

from end2end_imaging import GeoLens, Camera


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # -----------------------------------------------
    # 1. Build the camera pipeline (lens + sensor)
    # -----------------------------------------------
    camera = Camera(
        lens_file="./datasets/lenses/cellphone/cellphone80deg.json",
        sensor_file="./datasets/sensors/canon_r6.json",
        lens_type="geolens",
        sensor_type="rgb",
        device=device,
    )

    # -----------------------------------------------
    # 2. Load a test image (or generate a synthetic one)
    # -----------------------------------------------
    img_path = "./datasets/images/example.png"
    if os.path.exists(img_path):
        img = torchvision.io.read_image(img_path).float() / 255.0  # (3, H, W)
        img = img.unsqueeze(0)  # (1, 3, H, W)
    else:
        print(f"No image found at {img_path}, using synthetic test pattern.")
        img = torch.rand(1, 3, 512, 512)

    # -----------------------------------------------
    # 3. Prepare input data
    # -----------------------------------------------
    data_dict = {
        "img": img,                                          # sRGB image, (B, 3, H, W), [0, 1]
        "iso": torch.tensor([200.0]),                        # ISO value
        "field_center": torch.tensor([[0.0, 0.0]]),          # On-axis (center of field)
    }

    # -----------------------------------------------
    # 4. Render through the camera pipeline
    #    sRGB -> linear RGB -> PSF convolution -> Bayer -> noise -> ISP -> RGB
    # -----------------------------------------------
    with torch.no_grad():
        data_lq, data_gt = camera.render(data_dict, render_mode="psf_patch", output_type="rgb")

    print(f"Input image shape:  {img.shape}")
    print(f"Degraded output:    {data_lq.shape}  (RGB with lens aberrations + sensor noise)")
    print(f"Ground truth:       {data_gt.shape}  (clean RGB)")

    # -----------------------------------------------
    # 5. Visualize the lens and PSF
    # -----------------------------------------------
    lens = camera.lens
    lens.analysis(full_eval=False, render=False)

    # Compute on-axis RGB PSF
    psf = lens.psf_rgb(points=[0.0, 0.0, -10000.0], ks=128)
    print(f"PSF shape:          {psf.shape}")

    print("\nDone! The camera pipeline simulated lens aberrations and sensor noise.")


if __name__ == "__main__":
    main()

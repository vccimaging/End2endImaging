# Utilities API Reference

Utility functions and helper tools.

## Image Processing Utilities

### batch_psnr

```python
deeplens.utils.batch_psnr(pred, target, max_val=1.0, eps=1e-8)
```

Calculate PSNR between image batches.

**Parameters:**

- `pred` — Predicted image batch [B, C, H, W]
- `target` — Target image batch [B, C, H, W]
- `max_val` — Maximum pixel value
- `eps` — Small constant for numerical stability

**Returns:** PSNR value in dB

### batch_ssim

```python
deeplens.utils.batch_ssim(img, img_clean)
```

Calculate SSIM between image batches.

**Parameters:**

- `img` — Input image batch [B, C, H, W]
- `img_clean` — Reference image batch [B, C, H, W]

**Returns:** SSIM value [0, 1]

### batch_LPIPS

```python
deeplens.utils.batch_LPIPS(img, img_clean)
```

Compute LPIPS loss for image batch.

**Parameters:**

- `img` — Input image batch
- `img_clean` — Reference image batch

**Returns:** LPIPS distance

### img2batch

```python
deeplens.utils.img2batch(img)
```

Convert image to batch format.

**Parameters:**

- `img` — Image tensor (H, W, C) or (C, H, W), or numpy array

**Returns:** Batched image [1, C, H, W]

### Image Normalization

```python
deeplens.utils.normalize_ImageNet(batch)
```

Normalize dataset by ImageNet statistics.

**Parameters:**

- `batch` — Input image batch

**Returns:** Normalized batch

```python
deeplens.utils.denormalize_ImageNet(batch)
```

Convert normalized images back to original range.

**Parameters:**

- `batch` — Normalized batch

**Returns:** Denormalized batch

## Interpolation (deeplens.optics.utils)

### interp1d

```python
deeplens.optics.utils.interp1d(query, key, value, mode="linear")
```

Interpolate 1D query points to the key points.

**Parameters:**

- `query` — Query points [N, 1]
- `key` — Key points [M, 1]
- `value` — Value at key points [M, ...]
- `mode` — Interpolation mode

**Returns:** Interpolated value [N, ...]

### grid_sample_xy

```python
deeplens.optics.utils.grid_sample_xy(input, grid_xy, mode="bilinear", padding_mode="zeros", align_corners=False)
```

Grid sample using xy-coordinate grid [-1, 1].

**Parameters:**

- `input` — Input tensor [B, C, H, W]
- `grid_xy` — Grid xy coordinates [B, H, W, 2]

**Returns:** Sampled tensor [B, C, H, W]

## Video Utilities

### create_video_from_images

```python
deeplens.utils.create_video_from_images(image_folder, output_video_path, fps=30)
```

Create a video from a folder of images.

**Parameters:**

- `image_folder` — Path to folder containing images
- `output_video_path` — Output video path
- `fps` — Frames per second

## Logging and Setup

### set_logger

```python
deeplens.utils.set_logger(dir="./")
```

Setup logger.

**Parameters:**

- `dir` — Log directory

### gpu_init

```python
deeplens.utils.gpu_init(gpu=0)
```

Initialize device and data type.

**Parameters:**

- `gpu` — GPU index

**Returns:** `torch.device`

### set_seed

```python
deeplens.utils.set_seed(seed=0)
```

Set random seed for reproducibility.

**Parameters:**

- `seed` — Random seed

## Constants

`DEFAULT_WAVE`
:   Default wavelength (0.58756180 um)

`WAVE_RGB`
:   RGB wavelengths [0.65627250, 0.58756180, 0.48613270] um

`SPP_PSF`
:   Default samples per pixel for PSF (16384)

`SPP_COHERENT`
:   Samples per pixel for coherent calculation (~16.7M = 2^24)

`SPP_CALC`
:   Samples for computation (1024)

`SPP_RENDER`
:   Samples per pixel for rendering (32)

`DEPTH`
:   Default object depth (-20000.0 mm)

`PSF_KS`
:   Default kernel size for PSF calculation (64)

`EPSILON`
:   Small constant to avoid division by zero (1e-9)

# DeepLens Project Notes

## Architecture

- **Core optics**: `deeplens/optics/` — GeoLens, surfaces, optimization
- **Surface types**: `geometric_surface/` — `Aspheric`, `Spheric`, `Aperture`, etc.
- **Optimization**: `geolens_pkg/optim.py` (losses, optimizer), `optim_ops.py` (correct_shape, prune_surf)

## Known Issues & Fixes

### Aspheric Gradient Explosion (2026-02-28)

**Problem**: Optimization of camera lenses with `Aspheric` surfaces crashes with NaN after ~40 iterations.

**Root cause**: `Aspheric._sag()` computes `ai4 * r^4 + ai6 * r^6 + ...` with raw coordinates. The gradient `∂L/∂ai_{2n} ∝ r^{2n}`. For camera lenses with semi-diameter r=20-25mm, this produces gradients of O(10^4-10^5), compared to O(1) for curvature gradients.

Additionally, `prune_surf` (called inside `correct_shape`) oscillates surface semi-diameters between evaluation steps (e.g. 5.3mm → 24.9mm), causing ~500x gradient magnitude swings. Adam's second moment estimator (β₂=0.999, ~1000 step memory) cannot adapt fast enough, leading to 30x oversized steps that cause surface self-intersection and NaN.

**Fix** (`aspheric.py:get_optimizer_params`): Scale each aspheric coefficient's learning rate by `1 / max(r, 1)^{2n}`, so the lr-weighted gradient product is constant (`lr_base`) regardless of surface size. This decouples Adam's moment estimates from geometry changes during `prune_surf`. The r-scaling already normalizes across orders, so every order contributes equally to sag evolution (~lr_base mm/step). The former `decay` parameter was removed from the API since it would double-suppress higher orders, freezing ai6/ai8/ai10.

**Key files**:
- `deeplens/optics/geometric_surface/aspheric.py` — lr scaling fix
- `deeplens/optics/geolens_pkg/optim.py` — main optimization loop
- `deeplens/optics/geolens_pkg/optim_ops.py` — `correct_shape`, `prune_surf`

## Optimization Tips

- For camera lenses (r > 10mm), aspheric gradient magnitudes scale as r^{2n}. Always use lr normalization.
- `prune_surf` changes surface radii at each eval step — optimizer state (Adam moments) may become stale after radius changes.
- The `loss_intersec` in `loss_reg` penalizes surface self-intersection but with default weight 0.05, it may not prevent fast-growing geometry errors.

## API Notes

### `create_lens` (`geolens_pkg/utils.py`)
- Accepts `foclen` or `imgh` (mutually exclusive); the other is derived via `imgh = 2 * foclen * tan(fov/2)`.
- `flange` was renamed to `bfl` (back focal length) to match standard optics terminology.
- `enpd` parameter was removed — it is derived from `foclen / fnum / 2`.

### `optimize` / `get_optimizer` / `get_optimizer_params`
- `lrs` format: `[d, c, k, ai]` — four learning rates for distance, curvature, conic, and aspheric coefficients.
- The `decay` parameter was removed. The `1/r^{2n}` lr normalization in `Aspheric.get_optimizer_params` handles all order balancing.
- `set_target_fov_fnum()` now also updates `eqfl` (equivalent focal length) for consistency.

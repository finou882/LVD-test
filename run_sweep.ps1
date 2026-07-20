$env:PYTHONIOENCODING="utf-8"
$strengths = @(100.0, 50.0, 10.0, 1.0)
$seed = 42

# Ensure phase2 base model exists (assuming models/phase2_seed42.npz is present)
Write-Host "=== Parameter Sweep on Seed $seed ==="

foreach ($s in $strengths) {
    Write-Host "=== Running Phase 3 WITH Wine-Tower (strength=$s, homeo_gain=5.0) ==="
    uv run python -u main.py --seed $seed --start-phase 3 --wine-strength $s --homeo-gain 5.0 --save-history results/wt_s${s}_seed42.npz
}

Write-Host "=== Running Phase 3 NO Wine-Tower ==="
uv run python -u main.py --seed $seed --start-phase 3 --no-wine-tower --save-history results/no_wt_seed42.npz

Write-Host "=== All sweeps done! ==="
uv run python -u compare_sweep.py --seed $seed

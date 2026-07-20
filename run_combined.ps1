$env:PYTHONIOENCODING="utf-8"
$seed = 42

Write-Host "=== Running Phase 3 WITH Combined Features (strength=10, homeo_gain=5.0) ==="
uv run python -u main.py --seed $seed --start-phase 3 --wine-strength 10.0 --homeo-gain 5.0 --save-history results/wt_combined_seed42.npz

Write-Host "=== All done! ==="

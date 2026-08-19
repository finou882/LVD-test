$env:PYTHONIOENCODING="utf-8"
$seed = 42

Write-Host "=== Running Phase 3 WITH Combined Features (alpha=10, gamma=5.0) ==="
uv run python -u main.py --seed $seed --start-phase 3 --alpha 10.0 --gamma 5.0 --save-history results/lvd_combined_seed42.npz

Write-Host "=== All done! ==="

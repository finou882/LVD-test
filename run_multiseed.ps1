$env:PYTHONIOENCODING="utf-8"
$seeds = @(42, 123, 456, 789, 999)

Write-Host "=== Starting Multi-Seed Verification ==="
foreach ($s in $seeds) {
    Write-Host "--- Running Seed $s ---"
    
    Write-Host "1. Old Wine-Tower (alpha=50, no-homeo, no-neg-diff)"
    uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --wine-strength 50.0 --homeo-gain 1.0 --no-neg-diff --save-history results/ms_old_s${s}.npz
    
    Write-Host "2. New Combined Wine-Tower (alpha=10, homeo=5, neg-diff)"
    uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --wine-strength 10.0 --homeo-gain 5.0 --save-history results/ms_new_s${s}.npz
}

Write-Host "=== All multi-seed runs finished! ==="
uv run python -u plot_multiseed.py

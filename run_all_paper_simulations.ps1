$env:PYTHONIOENCODING="utf-8"
$seeds = @(42, 123, 456, 789, 999)

Write-Host "=========================================================="
Write-Host "  Hexable-Maze Paper Simulations Master Script (10 hours) "
Write-Host "=========================================================="

# 1. Create Monoculture Model for Fig 1 (Phase 1/2)
Write-Host "`n[1/4] Generating Phase 1/2 Monoculture Model (for Fig 1)..."
uv run python -u main.py --seed 42 --episodes 1500 --max-phase 2 --save-model models/phase2_fig1.npz
Write-Host "      -> Plotting Fig 1..."
uv run python generate_attractor_heatmap.py --model models/phase2_fig1.npz --episodes 50 --out articles/images/fig1.png

# 2. Run Phase 3 Multi-Seed Sweeps
Write-Host "`n[2/4] Running Multi-Seed Sweeps for Phase 3 (No-LVD, Old-LVD, New-LVD)..."
foreach ($s in $seeds) {
    Write-Host "----------------------------------------------------------"
    Write-Host "  >>> Seed $s <<< "
    Write-Host "----------------------------------------------------------"
    
    # 2.1 Baseline (No TRR)
    # Save the final model for the raster plot ONLY on seed 42
    if ($s -eq 42) {
        uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --no-lvd --save-history results/ms_no_lvd_s${s}.npz --save-model models/no_lvd_deep3_model.npz
    } else {
        uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --no-lvd --save-history results/ms_no_lvd_s${s}.npz
    }
    
    # 2.2 Old LVD (No neg-diff)
    uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --wine-strength 50.0 --homeo-gain 1.0 --no-neg-diff --save-history results/ms_old_s${s}.npz
    
    # 2.3 New LVD (With neg-diff)
    # Save the final model for the raster plot ONLY on seed 42
    if ($s -eq 42) {
        uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --wine-strength 10.0 --homeo-gain 5.0 --save-history results/ms_new_s${s}.npz --save-model models/wt_deep3_model.npz
    } else {
        uv run python -u main.py --seed $s --episodes 1200 --start-phase 3 --wine-strength 10.0 --homeo-gain 5.0 --save-history results/ms_new_s${s}.npz
    }
}

# 3. Generate Raster Plot (Fig Raster)
Write-Host "`n[3/4] Generating Raster Plot Comparison (Fig Raster)..."
uv run python generate_raster_comparison.py

# 4. Generate Final Paper Plots (Fig 2, Fig 6)
Write-Host "`n[4/4] Generating Multi-Seed Paper Plots (Fig 2, Fig 6)..."
uv run python plot_paper_multiseed.py

Write-Host "=========================================================="
Write-Host "  All simulations and plotting completed successfully!    "
Write-Host "  Check the articles/images/ directory for the output.    "
Write-Host "=========================================================="

# run_boost_ablation.ps1
#
# Ablation: 4 conditions, all forking from the same Phase-1/2 checkpoint per seed.
#
#   ctrl       : no-LVD, no-boost  (pure baseline)
#   boost_only : no-LVD, boost ON
#   wt_only    : LVD ON,  no-boost
#   wt         : LVD ON,  boost ON  (full method)
#
# Outputs (under results/boost_ablation/):
#   hist_p12_s{SEED}.npz           Phase1/2 history (shared)
#   hist_ctrl_s{SEED}.npz          Phase3 history (no-LVD, no-boost)
#   hist_boost_only_s{SEED}.npz    Phase3 history (no-LVD, boost ON)
#   hist_lvd_only_s{SEED}.npz       Phase3 history (LVD ON, no-boost)
#   hist_lvd_s{SEED}.npz            Phase3 history (LVD ON, boost ON)
#   model_p12_s{SEED}.npz          Phase1/2 checkpoint (reused for all forks)
#
# Usage:
#   .\run_boost_ablation.ps1
#   .\run_boost_ablation.ps1 -Seeds 42,123,456 -Phase12Ep 1500 -Phase3Ep 900
#
# Note: uv is required. Run from the workspace root.

param(
    [int[]]$Seeds      = @(42, 123, 456),
    [int]  $Phase12Ep  = 1500,
    [int]  $Phase3Ep   = 900,
    [int]  $Hidden     = 64,
    [int]  $WtaK       = 4,
    [float]$Lr         = 0.005
)

$env:PYTHONIOENCODING = "utf-8"
$outDir = "results/boost_ablation"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function Run-Phase {
    param(
        [string]$Label,
        [string]$PythonArgs
    )
    Write-Host ""
    Write-Host "  >>> $Label" -ForegroundColor Yellow
    $cmd = "uv run python main.py $PythonArgs"
    Write-Host "      $cmd" -ForegroundColor DarkGray
    Invoke-Expression $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Error "FAILED: $Label (exit $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

foreach ($seed in $Seeds) {
    $p12Model       = "$outDir/model_p12_s${seed}.npz"
    $ctrlModel      = "$outDir/model_ctrl_s${seed}.npz"
    $wtModel        = "$outDir/model_lvd_s${seed}.npz"
    $boostOnlyModel = "$outDir/model_boost_only_s${seed}.npz"
    $wtOnlyModel    = "$outDir/model_wt_only_s${seed}.npz"
    $p12Hist        = "$outDir/hist_p12_s${seed}.npz"
    $ctrlHist       = "$outDir/hist_ctrl_s${seed}.npz"
    $wtHist         = "$outDir/hist_lvd_s${seed}.npz"
    $boostOnlyHist  = "$outDir/hist_boost_only_s${seed}.npz"
    $wtOnlyHist     = "$outDir/hist_lvd_only_s${seed}.npz"

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Seed = $seed" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    # ── Phase 1/2 (shared checkpoint) ──────────────────────────────
    if (Test-Path $p12Model) {
        Write-Host "  [Phase1/2] Checkpoint already exists, skipping: $p12Model" -ForegroundColor Green
    } else {
        Run-Phase "Phase1/2  seed=$seed" (
            "--episodes $Phase12Ep " +
            "--hidden $Hidden --wta-k $WtaK --lr $Lr --seed $seed " +
            "--max-phase 2 " +
            "--save-model `"$p12Model`" " +
            "--save-history `"$p12Hist`""
        )
    }

    # ── Phase 3 fork A: control (no-LVD, no-boost) ──────────────────
    if (Test-Path $ctrlHist) {
        Write-Host "  [Phase3 CTRL] Already done, skipping: $ctrlHist" -ForegroundColor Green
    } else {
        Run-Phase "Phase3 CTRL (no-LVD, no-boost)  seed=$seed" (
            "--episodes $Phase3Ep " +
            "--hidden $Hidden --wta-k $WtaK --lr $Lr --seed $seed " +
            "--load-model `"$p12Model`" --start-phase 3 " +
            "--no-lvd --no-boost " +
            "--save-model `"$ctrlModel`" " +
            "--save-history `"$ctrlHist`""
        )
    }

    # ── Phase 3 fork B: boost only (no-LVD, boost ON) ───────────────
    if (Test-Path $boostOnlyHist) {
        Write-Host "  [Phase3 BOOST-ONLY] Already done, skipping: $boostOnlyHist" -ForegroundColor Green
    } else {
        Run-Phase "Phase3 BOOST-ONLY (no-LVD, boost ON)  seed=$seed" (
            "--episodes $Phase3Ep " +
            "--hidden $Hidden --wta-k $WtaK --lr $Lr --seed $seed " +
            "--load-model `"$p12Model`" --start-phase 3 " +
            "--no-lvd " +
            "--save-model `"$boostOnlyModel`" " +
            "--save-history `"$boostOnlyHist`""
        )
    }

    # ── Phase 3 fork C: LVD only (LVD ON, no-boost) ──────────────────
    if (Test-Path $wtOnlyHist) {
        Write-Host "  [Phase3 LVD-ONLY]   Already done, skipping: $wtOnlyHist" -ForegroundColor Green
    } else {
        Run-Phase "Phase3 LVD-ONLY (LVD ON, no-boost)  seed=$seed" (
            "--episodes $Phase3Ep " +
            "--hidden $Hidden --wta-k $WtaK --lr $Lr --seed $seed " +
            "--load-model `"$p12Model`" --start-phase 3 " +
            "--no-boost " +
            "--save-model `"$wtOnlyModel`" " +
            "--save-history `"$wtOnlyHist`""
        )
    }

    # ── Phase 3 fork D: full method (LVD ON, boost ON) ──────────────
    if (Test-Path $wtHist) {
        Write-Host "  [Phase3 LVD]   Already done, skipping: $wtHist" -ForegroundColor Green
    } else {
        Run-Phase "Phase3 LVD+boost  seed=$seed" (
            "--episodes $Phase3Ep " +
            "--hidden $Hidden --wta-k $WtaK --lr $Lr --seed $seed " +
            "--load-model `"$p12Model`" --start-phase 3 " +
            "--save-model `"$wtModel`" " +
            "--save-history `"$wtHist`""
        )
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All done!  Results in: $outDir" -ForegroundColor Cyan
Write-Host "  Next: uv run python compare_boost_ablation.py" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

"""
compare_boost_ablation.py
--------------------------
Two outputs from the ablation experiment:

  (1) fig_ablation.png  -- 4 conditions x 3 seeds = 12 lines
                           success rate in Phase 3
      Saved to: articles/images/fig_ablation.png

  (2) fig6_new.png      -- improved fig6: dead neurons (top) + success rate
                           (bottom) as mean±std bands (3 seeds each, 4 conditions)
      Saved to: articles/images/fig6.png  (overwrites)

Data source: results/boost_ablation/
  hist_ctrl_s{42,123,456}.npz          -- control (no-LVD, no-boost)
  hist_boost_only_s{42,123,456}.npz    -- R-STDP boost only (no-LVD, boost ON)
  hist_lvd_only_s{42,123,456}.npz       -- Leaky Volume Diffusion only  (LVD ON,  no-boost)
  hist_lvd_s{42,123,456}.npz            -- full method (LVD ON, boost ON)

Usage:
  uv run python compare_boost_ablation.py
  uv run python compare_boost_ablation.py --window 30 --no-overwrite
"""

import argparse
import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEEDS = [42, 123]
DATA_DIR = pathlib.Path("results/boost_ablation")
OUT_ABLATION = pathlib.Path("articles/images/fig_ablation.png")
OUT_FIG6     = pathlib.Path("articles/images/fig6.png")

COLOR_LVD_SEEDS         = ["#1976D2", "#42A5F5", "#90CAF9"]   # blue family
COLOR_CTRL_SEEDS       = ["#D32F2F", "#EF5350", "#FFCDD2"]   # red family
COLOR_BOOST_ONLY_SEEDS = ["#F57C00", "#FFA726", "#FFCC80"]   # orange family
COLOR_LVD_ONLY_SEEDS    = ["#388E3C", "#66BB6A", "#A5D6A7"]   # green family
COLOR_LVD_MEAN         = "#1565C0"
COLOR_CTRL_MEAN       = "#B71C1C"
COLOR_BOOST_ONLY_MEAN = "#E65100"
COLOR_LVD_ONLY_MEAN    = "#1B5E20"


def load(path: str) -> dict:
    d = np.load(path)
    return {k: d[k] for k in d.files}


def rolling(arr, window):
    return np.convolve(arr.astype(float), np.ones(window) / window, mode="valid")


def total_dead(d):
    return (d["n_dead_hidden1"] + d["n_dead_hidden2"] + d["n_dead_hidden3"]).astype(float)


def load_seeds(prefix, seeds):
    """Return list of dicts, one per seed."""
    results = []
    for s in seeds:
        path = DATA_DIR / f"hist_{prefix}_s{s}.npz"
        if not path.exists():
            raise FileNotFoundError(
                f"Missing: {path}\n"
                f"Run '.\\run_boost_ablation.ps1' first to generate training data."
            )
        results.append(load(str(path)))
    return results


# ─────────────────────────────────────────────────────────────────────────────
def plot_ablation(wt_list, ctrl_list, boost_only_list, wt_only_list, window, out_path):
    """
    Figure: 12 individual success-rate curves (Phase-3 only).
    3 blue   = LVD+boost (full), 3 red  = control,
    3 orange = boost-only,      3 green = wt-only
    """
    fig, ax = plt.subplots(figsize=(12, 5))

    groups = [
        (ctrl_list,       COLOR_CTRL_SEEDS,       COLOR_CTRL_MEAN,       "Control (no-LVD, no-boost)",  "--"),
        (boost_only_list, COLOR_BOOST_ONLY_SEEDS,  COLOR_BOOST_ONLY_MEAN, "Boost-Only (no-LVD)",         "-."),
        (wt_only_list,    COLOR_LVD_ONLY_SEEDS,     COLOR_LVD_ONLY_MEAN,    "LVD-Only (no-boost)",          ":"),
        (wt_list,         COLOR_LVD_SEEDS,          COLOR_LVD_MEAN,         "Leaky Volume Diffusion + STDP Boost",    "-"),
    ]
    from matplotlib.lines import Line2D
    legend_custom = []
    for data_list, seed_colors, mean_color, label, ls in groups:
        for i, (d, color) in enumerate(zip(data_list, seed_colors)):
            roll = rolling(d["success"], window) * 100
            x = np.arange(window - 1, window - 1 + len(roll))
            ax.plot(x, roll, color=color, linewidth=1.2, linestyle=ls, alpha=0.8)
        legend_custom.append(
            Line2D([0], [0], color=mean_color, linewidth=2, linestyle=ls, label=label)
        )

    ax.legend(handles=legend_custom, fontsize=9, ncol=2)
    ax.set_xlabel("Episode (Phase 3)", fontsize=11)
    ax.set_ylabel(f"Rolling success rate ({window}-ep window, %)", fontsize=11)
    ax.set_ylim(0, 55)
    ax.set_title(
        "Ablation: 4 conditions × 3 seeds  [ctrl / boost-only / wt-only / full]",
        fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
def plot_fig6(wt_list, ctrl_list, boost_only_list, wt_only_list, window, out_path):
    """
    Improved fig6: two-panel figure with mean±std bands, 4 conditions.
    Top  : dead hidden neurons (H1+H2+H3) over Phase-3 episodes
    Bottom: rolling success rate over Phase-3 episodes
    """
    def align(arrays):
        min_len = min(len(a) for a in arrays)
        return np.stack([a[:min_len] for a in arrays])

    dead_lvd         = align([total_dead(d) for d in wt_list])
    dead_ctrl       = align([total_dead(d) for d in ctrl_list])
    dead_boost_only = align([total_dead(d) for d in boost_only_list])
    dead_lvd_only    = align([total_dead(d) for d in wt_only_list])

    succ_lvd         = align([d["success"].astype(float) for d in wt_list])
    succ_ctrl       = align([d["success"].astype(float) for d in ctrl_list])
    succ_boost_only = align([d["success"].astype(float) for d in boost_only_list])
    succ_lvd_only    = align([d["success"].astype(float) for d in wt_only_list])

    T = dead_lvd.shape[1]
    episodes = np.arange(T)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True,
                                   gridspec_kw={"hspace": 0.35})

    # ── Top panel: dead neurons ───────────────────────────────────
    dead_groups = [
        (dead_ctrl,       COLOR_CTRL_MEAN,       "Control (no-LVD, no-boost)",  "--"),
        (dead_boost_only, COLOR_BOOST_ONLY_MEAN, "Boost-Only (no-LVD)",         "-."),
        (dead_lvd_only,    COLOR_LVD_ONLY_MEAN,    "LVD-Only (no-boost)",          ":"),
        (dead_lvd,         COLOR_LVD_MEAN,         "Leaky Volume Diffusion + STDP Boost",    "-"),
    ]
    for arr, color, label, ls in dead_groups:
        mean = arr.mean(axis=0)
        std  = arr.std(axis=0)
        ax1.plot(episodes, mean, color=color, linewidth=2, linestyle=ls, label=label)
        ax1.fill_between(episodes, mean - std, mean + std, color=color, alpha=0.15)

    ax1.set_ylabel("Total dead hidden neurons (H1+H2+H3)", fontsize=11)
    ax1.set_title(
        f"Dead Neuron Count: mean ± std  (seeds {SEEDS})", fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Annotate final means
    for arr, color, _, ls in dead_groups:
        final = arr.mean(axis=0)[-1]
        ax1.annotate(f"end={final:.1f}",
                     xy=(episodes[-1], final),
                     xytext=(-65, 8), textcoords="offset points",
                     color=color, fontsize=9,
                     arrowprops=dict(arrowstyle="->", color=color))

    # ── Bottom panel: success rate ────────────────────────────────
    succ_groups = [
        (succ_ctrl,       COLOR_CTRL_MEAN,       "Control (no-LVD, no-boost)",  "--"),
        (succ_boost_only, COLOR_BOOST_ONLY_MEAN, "Boost-Only (no-LVD)",         "-."),
        (succ_lvd_only,    COLOR_LVD_ONLY_MEAN,    "LVD-Only (no-boost)",          ":"),
        (succ_lvd,         COLOR_LVD_MEAN,         "Leaky Volume Diffusion + STDP Boost",    "-"),
    ]
    for arr, color, label, ls in succ_groups:
        rolls = np.stack([rolling(arr[i], window) * 100 for i in range(len(SEEDS))])
        mean  = rolls.mean(axis=0)
        std   = rolls.std(axis=0)
        x     = np.arange(window - 1, window - 1 + len(mean))
        ax2.plot(x, mean, color=color, linewidth=2, linestyle=ls, label=label)
        ax2.fill_between(x, mean - std, mean + std, color=color, alpha=0.15)

    ax2.set_xlabel("Episode (Phase 3)", fontsize=11)
    ax2.set_ylabel(f"Rolling success rate ({window}-ep window, %)", fontsize=11)
    ax2.set_title("Success Rate: mean ± std", fontsize=11)
    ax2.set_ylim(0, 55)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.suptitle(
        "Ablation: 4 conditions  \u00b7  Phase 3 (all-10-goals recall)\n"
        f"n = {len(SEEDS)} seeds each  |  ctrl / boost-only / wt-only / full",
        fontsize=12)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", type=int, default=50,
                        help="Rolling window size for success rate")
    parser.add_argument("--no-overwrite", action="store_true",
                        help="Skip saving fig6.png if it already exists")
    args = parser.parse_args()

    wt_list         = load_seeds("wt",         SEEDS)
    ctrl_list       = load_seeds("ctrl",       SEEDS)
    boost_only_list = load_seeds("boost_only", SEEDS)
    wt_only_list    = load_seeds("wt_only",    SEEDS)

    plot_ablation(wt_list, ctrl_list, boost_only_list, wt_only_list, args.window, OUT_ABLATION)

    if args.no_overwrite and OUT_FIG6.exists():
        print(f"Skipped (--no-overwrite): {OUT_FIG6}")
    else:
        plot_fig6(wt_list, ctrl_list, boost_only_list, wt_only_list, args.window, OUT_FIG6)


if __name__ == "__main__":
    main()

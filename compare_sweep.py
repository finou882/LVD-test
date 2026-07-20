import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="sweep_comparison.png")
    args = parser.parse_args()

    strengths = [100.0, 50.0, 10.0, 1.0]
    
    # Setup plot (we will plot Dead H1 and Dead Out)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Homeostatic Scaling Sweep (Seed {args.seed})", fontsize=16)

    # 1. Plot Phase 1/2 Base (if exists, though we just want Phase 3 comparison)
    # Actually, we can just load the Phase 3 files and plot them.
    # Phase 3 files start from episode 0 of Phase 3, which we can offset by 2100.
    offset = 2100

    def plot_data(file_path, label, color, ls):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        data = np.load(file_path)
        episodes = data["episode"] + offset
        dead_h1 = data["n_dead_hidden1"]
        dead_out = data["n_dead_output"]

        axes[0].plot(episodes, dead_h1, label=label, color=color, linestyle=ls, linewidth=2)
        axes[1].plot(episodes, dead_out, label=label, color=color, linestyle=ls, linewidth=2)

    colors = ['blue', 'green', 'orange', 'purple']
    
    # WT No
    plot_data(f"results/no_wt_seed{args.seed}.npz", "NO WT", "black", "--")
    
    # WT with different strengths
    for i, s in enumerate(strengths):
        plot_data(f"results/wt_s{int(s) if s.is_integer() else s}_seed{args.seed}.npz", f"WT (alpha={s})", colors[i], "-")
        
    # Plot combined
    plot_data(f"results/wt_combined_seed{args.seed}.npz", "WT Combined (alpha=10)", "red", "-.")

    axes[0].set_title("Dead Neurons in Hidden 1")
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Count (max 128)")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].set_title("Dead Neurons in Output")
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Count (max 6)")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig(args.out)
    print(f"Sweep comparison saved to: {args.out}")

if __name__ == "__main__":
    main()

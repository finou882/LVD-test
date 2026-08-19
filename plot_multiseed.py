import numpy as np
import matplotlib.pyplot as plt
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="multiseed_comparison.png")
    args = parser.parse_args()

    seeds = [42, 123, 456, 789, 999]
    window = 50

    def load_data(prefix):
        all_acc = []
        all_dead1 = []
        episodes = None
        
        for s in seeds:
            path = f"results/{prefix}_s{s}.npz"
            data = np.load(path)
            if episodes is None:
                episodes = data["episode"]
            
            # Rolling accuracy
            successes = data["success"]
            roll_acc = np.convolve(successes, np.ones(window)/window, mode="valid") * 100
            
            all_acc.append(roll_acc)
            # Match length of dead1 to roll_acc by slicing
            all_dead1.append(data["n_dead_hidden1"][window-1:])
            
        return episodes[window-1:], np.array(all_acc), np.array(all_dead1)

    # Load data
    ep_old, acc_old, dead_old = load_data("ms_old")
    ep_new, acc_new, dead_new = load_data("ms_new")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Multi-Seed Verification (5 Seeds)", fontsize=16)

    def plot_mean_std(ax, x, data, color, label):
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)
        ax.plot(x, mean, color=color, label=label, linewidth=2)
        ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2)

    # Plot Accuracy
    plot_mean_std(axes[0], ep_old, acc_old, "blue", "Old LVD (Struct Recovery)")
    plot_mean_std(axes[0], ep_new, acc_new, "red", "New LVD (Sparse/Neg-Diff)")
    axes[0].set_title("Rolling Success Rate (%)")
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(True)

    # Plot Dead Neurons (H1)
    plot_mean_std(axes[1], ep_old, dead_old, "blue", "Old LVD")
    plot_mean_std(axes[1], ep_new, dead_new, "red", "New LVD")
    axes[1].set_title("Dead Neurons in Hidden 1")
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Count (max 64)")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig(args.out)
    print(f"Plot saved to: {args.out}")

if __name__ == "__main__":
    main()

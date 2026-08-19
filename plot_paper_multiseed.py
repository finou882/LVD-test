import numpy as np
import matplotlib.pyplot as plt
import os

seeds = [42, 123, 456, 789, 999]
window = 50

def load_data(prefix):
    all_acc = []
    all_dead1 = []
    episodes = None
    
    for s in seeds:
        path = f"results/{prefix}_s{s}.npz"
        if not os.path.exists(path):
            print(f"Warning: {path} not found.")
            continue
            
        data = np.load(path)
        if episodes is None:
            episodes = data["episode"]
        
        # Rolling accuracy
        successes = data["success"]
        roll_acc = np.convolve(successes, np.ones(window)/window, mode="valid") * 100
        
        all_acc.append(roll_acc)
        # Match length of dead1 to roll_acc by slicing
        all_dead1.append(data["n_dead_hidden1"][window-1:])
        
    if len(all_acc) == 0:
        return None, None, None
        
    return episodes[window-1:], np.array(all_acc), np.array(all_dead1)

def plot_mean_std(ax, x, data, color, label, ls="-"):
    if data is None or len(data) == 0:
        return
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    ax.plot(x, mean, color=color, label=label, linewidth=2, linestyle=ls)
    ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.1)

def main():
    os.makedirs("articles/images", exist_ok=True)
    
    # Load all conditions
    ep_base, acc_base, dead_base = load_data("ms_no_wt")
    ep_homeo, acc_homeo, dead_homeo = load_data("homeo_base")
    ep_v1, acc_v1, dead_v1 = load_data("ms_old")
    ep_v2, acc_v2, dead_v2 = load_data("ms_new")
    
    ep_no_neg, acc_no_neg, dead_no_neg = load_data("wt_v2_no_negdiff")
    ep_no_hom, acc_no_hom, dead_no_hom = load_data("wt_v2_no_homeo")
    ep_a50, acc_a50, dead_a50 = load_data("wt_v2_alpha50")

    # --- FIG 2: Baseline vs Old LVD (Structural Recovery) ---
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))
    fig2.suptitle("(a) Structural Recovery in Leaky Volume Diffusion", fontsize=16)
    
    plot_mean_std(axes2[0], ep_base, dead_base, "black", "Baseline (No LVD)", "--")
    plot_mean_std(axes2[1], ep_base, acc_base, "black", "Baseline (No LVD)", "--")
    
    plot_mean_std(axes2[0], ep_v1, dead_v1, "blue", "LVD v1 (alpha=50, no-neg, no-homeo)")
    plot_mean_std(axes2[1], ep_v1, acc_v1, "blue", "LVD v1 (alpha=50, no-neg, no-homeo)")
        
    axes2[0].set_ylim(bottom=0); axes2[1].set_ylim(bottom=0)
    axes2[0].set_title("Dead Neurons (H1)")
    axes2[0].set_xlabel("Episode"); axes2[0].set_ylabel("Count")
    axes2[0].legend(); axes2[0].grid(True)
    
    axes2[1].set_title("Rolling Success Rate (%)")
    axes2[1].set_xlabel("Episode"); axes2[1].set_ylabel("Accuracy")
    axes2[1].legend(); axes2[1].grid(True)
    
    fig2.tight_layout()
    fig2.savefig("articles/images/fig2.png", dpi=300)
    print("Saved articles/images/fig2.png")

    # --- FIG 6: Old LVD vs New LVD (Sparse Maintenance & Negative Diffusion) ---
    fig6, axes6 = plt.subplots(1, 2, figsize=(14, 6))
    fig6.suptitle("(b) Maintenance of Sparsity via Negative Diffusion", fontsize=16)
    
    plot_mean_std(axes6[0], ep_v1, dead_v1, "blue", "LVD v1 (alpha=50, no-neg, no-homeo)")
    plot_mean_std(axes6[1], ep_v1, acc_v1, "blue", "LVD v1 (alpha=50, no-neg, no-homeo)")
        
    plot_mean_std(axes6[0], ep_v2, dead_v2, "red", "LVD v2 (alpha=10, neg, homeo)")
    plot_mean_std(axes6[1], ep_v2, acc_v2, "red", "LVD v2 (alpha=10, neg, homeo)")
        
    axes6[0].set_ylim(bottom=0); axes6[1].set_ylim(bottom=0)
    axes6[0].set_title("Dead Neurons (H1) - Sparsity")
    axes6[0].set_xlabel("Episode"); axes6[0].set_ylabel("Count")
    axes6[0].legend(); axes6[0].grid(True)
    
    axes6[1].set_title("Rolling Success Rate (%)")
    axes6[1].set_xlabel("Episode"); axes6[1].set_ylabel("Accuracy")
    axes6[1].legend(); axes6[1].grid(True)
    
    fig6.tight_layout()
    fig6.savefig("articles/images/fig6.png", dpi=300)
    print("Saved articles/images/fig6.png")

    # --- FIG ABLATION: Ablation Study ---
    fig_ab, axes_ab = plt.subplots(1, 2, figsize=(14, 6))
    fig_ab.suptitle("Ablation Study of LVD v2 Components", fontsize=16)
    
    # Plot conditions
    plot_mean_std(axes_ab[0], ep_v2, dead_v2, "red", "LVD v2 (Full)")
    plot_mean_std(axes_ab[1], ep_v2, acc_v2, "red", "LVD v2 (Full)")
    
    plot_mean_std(axes_ab[0], ep_homeo, dead_homeo, "black", "Homeostatic Only (No LVD)", "--")
    plot_mean_std(axes_ab[1], ep_homeo, acc_homeo, "black", "Homeostatic Only (No LVD)", "--")

    plot_mean_std(axes_ab[0], ep_no_neg, dead_no_neg, "orange", "LVD v2 (w/o NegDiff)")
    plot_mean_std(axes_ab[1], ep_no_neg, acc_no_neg, "orange", "LVD v2 (w/o NegDiff)")
    
    plot_mean_std(axes_ab[0], ep_no_hom, dead_no_hom, "purple", "LVD v2 (w/o Homeo)")
    plot_mean_std(axes_ab[1], ep_no_hom, acc_no_hom, "purple", "LVD v2 (w/o Homeo)")
    
    plot_mean_std(axes_ab[0], ep_a50, dead_a50, "green", "LVD v2 (alpha=50)")
    plot_mean_std(axes_ab[1], ep_a50, acc_a50, "green", "LVD v2 (alpha=50)")

    axes_ab[0].set_ylim(bottom=0); axes_ab[1].set_ylim(bottom=0)
    axes_ab[0].set_title("Dead Neurons (H1)")
    axes_ab[0].set_xlabel("Episode"); axes_ab[0].set_ylabel("Count")
    axes_ab[0].legend(fontsize=9); axes_ab[0].grid(True)
    
    axes_ab[1].set_title("Rolling Success Rate (%)")
    axes_ab[1].set_xlabel("Episode"); axes_ab[1].set_ylabel("Accuracy")
    axes_ab[1].legend(fontsize=9); axes_ab[1].grid(True)
    
    fig_ab.tight_layout()
    fig_ab.savefig("articles/images/fig_ablation.png", dpi=300)
    print("Saved articles/images/fig_ablation.png")

if __name__ == "__main__":
    main()

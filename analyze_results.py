import numpy as np
import sys

def print_summary(name, path):
    try:
        data = np.load(path)
        success = data["success"]
        dead1 = data["n_dead_hidden1"]
        dead2 = data["n_dead_hidden2"]
        dead3 = data["n_dead_hidden3"]
        dead_out = data["n_dead_output"]
        
        recent_acc = np.mean(success[-100:]) * 100
        print(f"--- {name} ---")
        print(f"Final Accuracy (last 100 ep): {recent_acc:.1f}%")
        print(f"Final Dead Neurons (H1,H2,H3): {dead1[-1]}, {dead2[-1]}, {dead3[-1]}")
        print(f"Final Dead Output Neurons: {dead_out[-1]}")
        print()
    except Exception as e:
        print(f"Failed to load {path}: {e}")

if __name__ == "__main__":
    print_summary("1. No Wine-Tower", "results/exp1_no_wt.npz")
    print_summary("2. Old Wine-Tower (no neg-diff, no homeo)", "results/exp2_wt_old.npz")
    print_summary("3. New Combined Wine-Tower (neg-diff + homeo)", "results/exp3_wt_new.npz")

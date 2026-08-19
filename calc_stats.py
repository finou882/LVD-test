import numpy as np
from scipy import stats
import os

seeds = [42, 123, 456, 789, 999]

def load_success_data(prefix):
    success_lists = []
    for s in seeds:
        path = f"results/{prefix}_s{s}.npz"
        if os.path.exists(path):
            data = np.load(path)
            success_lists.append(data["success"])
    return np.array(success_lists)

def main():
    old_data = load_success_data("ms_old")
    new_data = load_success_data("ms_new")

    if len(old_data) == 0 or len(new_data) == 0:
        print("Data missing.")
        return

    # 1. Overall Mean Success Rate
    old_mean_overall = np.mean(old_data, axis=1) * 100
    new_mean_overall = np.mean(new_data, axis=1) * 100
    print(f"--- Overall Mean Success Rate ---")
    print(f"LVD v1 (Old): {np.mean(old_mean_overall):.2f}% ± {np.std(old_mean_overall):.2f}%")
    print(f"LVD v2 (New): {np.mean(new_mean_overall):.2f}% ± {np.std(new_mean_overall):.2f}%")
    t, p = stats.ttest_ind(old_mean_overall, new_mean_overall)
    print(f"T-test p-value: {p:.4f}\n")

    # 2. Late Episodes (last 500 episodes) Mean Success Rate
    old_late = old_data[:, -500:]
    new_late = new_data[:, -500:]
    old_mean_late = np.mean(old_late, axis=1) * 100
    new_mean_late = np.mean(new_late, axis=1) * 100
    print(f"--- Late Episodes (Last 500) Mean Success Rate ---")
    print(f"LVD v1 (Old): {np.mean(old_mean_late):.2f}% ± {np.std(old_mean_late):.2f}%")
    print(f"LVD v2 (New): {np.mean(new_mean_late):.2f}% ± {np.std(new_mean_late):.2f}%")
    t_late, p_late = stats.ttest_ind(old_mean_late, new_mean_late)
    print(f"T-test p-value: {p_late:.4f}\n")

    # 3. Peak Rolling Accuracy
    window = 50
    old_peak = []
    new_peak = []
    for i in range(len(seeds)):
        old_roll = np.convolve(old_data[i], np.ones(window)/window, mode="valid") * 100
        new_roll = np.convolve(new_data[i], np.ones(window)/window, mode="valid") * 100
        old_peak.append(np.max(old_roll))
        new_peak.append(np.max(new_roll))
        
    print(f"--- Peak Rolling Success Rate (window={window}) ---")
    print(f"LVD v1 (Old): {np.mean(old_peak):.2f}% ± {np.std(old_peak):.2f}%")
    print(f"LVD v2 (New): {np.mean(new_peak):.2f}% ± {np.std(new_peak):.2f}%")
    t_peak, p_peak = stats.ttest_ind(old_peak, new_peak)
    print(f"T-test p-value: {p_peak:.4f}\n")

if __name__ == "__main__":
    main()

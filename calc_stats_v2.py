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
    return np.array(success_lists) if success_lists else None

def print_stats(name, data):
    if data is None or len(data) == 0:
        print(f"{name}: NO DATA")
        return None
    mean_overall = np.mean(data, axis=1) * 100
    late_data = data[:, -100:]
    mean_late = np.mean(late_data, axis=1) * 100
    print(f"{name:<25} | Overall: {np.mean(mean_overall):>5.2f}% ± {np.std(mean_overall):>5.2f}% | Late 100: {np.mean(mean_late):>5.2f}% ± {np.std(mean_late):>5.2f}%")
    return mean_overall, mean_late

def main():
    conditions = {
        "Baseline": "ms_no_wt",
        "Homeostatic Base": "homeo_base",
        "LVD v1": "ms_old",
        "LVD v2 (Full)": "ms_new",
        "LVD v2 w/o NegDiff": "wt_v2_no_negdiff",
        "LVD v2 w/o Homeo": "wt_v2_no_homeo",
        "LVD v2 alpha=50": "wt_v2_alpha50",
    }
    
    results = {}
    
    print("="*80)
    print("PERFORMANCE METRICS (Mean ± SD across N=5 seeds)")
    print("="*80)
    
    for name, prefix in conditions.items():
        data = load_success_data(prefix)
        res = print_stats(name, data)
        if res:
            results[name] = res
            
    print("\n" + "="*80)
    print("STATISTICAL TESTS (p-values vs LVD v2 Full)")
    print("="*80)
    
    if "LVD v2 (Full)" in results:
        v2_overall, v2_late = results["LVD v2 (Full)"]
        for name, res in results.items():
            if name == "LVD v2 (Full)":
                continue
            overall, late = res
            _, p_over = stats.ttest_ind(overall, v2_overall)
            _, p_late = stats.ttest_ind(late, v2_late)
            print(f"{name:<25} | Overall p={p_over:.2e} | Late 100 p={p_late:.2e}")

if __name__ == "__main__":
    main()

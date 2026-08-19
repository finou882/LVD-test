import numpy as np
seeds = [42, 123, 456, 789, 999]
conds = {
    'Baseline': 'ms_no_wt', 
    'Homeostatic Base': 'homeo_base', 
    'LVD v1': 'ms_old', 
    'LVD v2 (Full)': 'ms_new', 
    'LVD v2 w/o NegDiff': 'wt_v2_no_negdiff', 
    'LVD v2 w/o Homeo': 'wt_v2_no_homeo', 
    'LVD v2 alpha=50': 'wt_v2_alpha50'
}
for name, prefix in conds.items():
    data = []
    for s in seeds:
        data.append(np.load(f'results/{prefix}_s{s}.npz')['n_dead_hidden1'][-100:])
    print(f"{name:20} | Dead H1 (Late 100): {np.mean(data):.1f} +/- {np.std(data):.1f}")

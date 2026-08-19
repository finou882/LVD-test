import subprocess
import os
import sys
import time

if __name__ == "__main__":
    # ONLY RUN NEW CONDITIONS!
    # Original data already exists: 
    # ms_no_wt (Baseline)
    # ms_old (LVD v1)
    # ms_new (LVD v2)
    
    conditions = {
        "homeo_base": ["--episodes", "1200", "--start-phase", "3", "--no-lvd", "--homeo-gain", "5.0", "--save-history", "results/homeo_base_s{seed}.npz"],
        "wt_v2_no_negdiff": ["--episodes", "1200", "--start-phase", "3", "--wine-strength", "10.0", "--homeo-gain", "5.0", "--no-neg-diff", "--save-history", "results/wt_v2_no_negdiff_s{seed}.npz"],
        "wt_v2_no_homeo": ["--episodes", "1200", "--start-phase", "3", "--wine-strength", "10.0", "--homeo-gain", "1.0", "--save-history", "results/wt_v2_no_homeo_s{seed}.npz"],
        "wt_v2_alpha50": ["--episodes", "1200", "--start-phase", "3", "--wine-strength", "50.0", "--homeo-gain", "5.0", "--save-history", "results/wt_v2_alpha50_s{seed}.npz"],
    }
    
    seeds = [42, 123, 456, 789, 999]
    os.makedirs("results", exist_ok=True)
    
    # We will run them in batches of 4 (one seed at a time) to avoid memory overload
    print("Starting experiments...")
    start_total = time.time()
    
    for seed in seeds:
        print(f"--- Starting batch for seed {seed} ---")
        procs = []
        for cond_name, cmd_template in conditions.items():
            cmd = [c.replace("{seed}", str(seed)) for c in cmd_template]
            full_cmd = ["uv", "run", "python", "-u", "main.py"] + cmd + ["--seed", str(seed)]
            
            # Spawn the process
            log_file = open(f"results/log_{cond_name}_{seed}.txt", "w")
            p = subprocess.Popen(full_cmd, stdout=log_file, stderr=subprocess.STDOUT)
            procs.append((cond_name, p, log_file))
            print(f"Launched {cond_name} (pid={p.pid})")
            
        # Wait for this batch to finish
        for cond_name, p, log_file in procs:
            p.wait()
            log_file.close()
            if p.returncode == 0:
                print(f"Finished {cond_name} for seed {seed} successfully.")
            else:
                print(f"FAILED {cond_name} for seed {seed} (code {p.returncode}). Check logs.")
                
    print(f"All experiments finished in {time.time()-start_total:.1f}s")

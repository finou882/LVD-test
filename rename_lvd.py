import os
import re

replacements = [
    # LaTeX and Text replacements (Case Sensitive)
    (r"Wine-Tower \(WT\)", r"Leaky Volume Diffusion (LVD)"),
    (r"Wine-Tower", r"Leaky Volume Diffusion"),
    (r"Wine Tower", r"Leaky Volume Diffusion"),
    (r"WT v1", r"LVD v1"),
    (r"WT v2", r"LVD v2"),
    (r"WT機構", r"LVD制御メカニズム"), # Ensure no left-overs
    (r"WT制御メカニズム", r"LVD制御メカニズム"),
    # Code replacements
    (r"wine_tower", r"lvd"),
    (r"no_wine_tower", r"no_lvd"),
    (r"no-wine-tower", r"no-lvd"),
    (r"compare_winetower", r"compare_lvd"),
    (r"wt_s", r"lvd_s"),
    (r"wt_combined", r"lvd_combined"),
    (r"no_wt_", r"no_lvd_"),
    (r"exp1_no_wt", r"exp1_no_lvd"),
    (r"exp2_wt_old", r"exp2_lvd_old"),
    (r"exp3_wt_new", r"exp3_lvd_new"),
    (r"hist_wt_", r"hist_lvd_"),
    (r"succ_wt", r"succ_lvd"),
    (r"dead_wt", r"dead_lvd"),
    (r"COLOR_WT", r"COLOR_LVD"),
    (r"COLOR_NOWT", r"COLOR_NOLVD"),
]

directories = ['.', 'src/snn_agent', 'articles']
files_to_process = []

for d in directories:
    for f in os.listdir(d):
        if f.endswith('.py') or f.endswith('.ps1') or f.endswith('.md') or f.endswith('.tex') or f.endswith('.cff'):
            # Skip the script itself
            if f in ['rename_lvd.py', 'rename.py']: continue
            files_to_process.append(os.path.join(d, f))

for filepath in files_to_process:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements:
        new_content = re.sub(old, new, new_content)
        
    # Extra check for stray "WT" in Japanese contexts:
    # "WTが" -> "LVDが", "WTの" -> "LVDの", "WTは" -> "LVDは", "WTを" -> "LVDを"
    new_content = re.sub(r"\bWT([がのはを])", r"LVD\1", new_content)
    # "WT" -> "LVD" for standalone WT where it's safe (e.g. Figure titles like WT vs)
    new_content = re.sub(r"\bWT\b", r"LVD", new_content)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')

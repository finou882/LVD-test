import os
import re

replacements = {
    'alpha': 'alpha',
    'gamma': 'gamma',
    'i_assist': 'i_assist',
    'v_rest': 'v_rest',
    'v_thresh': 'v_thresh',
    'a_plus': 'a_plus',
    'a_minus': 'a_minus',
    'w_eff': 'w_eff',
}

directories = ['.', 'src/snn_agent']
files_to_process = []

for d in directories:
    for f in os.listdir(d):
        if f.endswith('.py') or f.endswith('.ps1'):
            files_to_process.append(os.path.join(d, f))

for filepath in files_to_process:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        new_content = re.sub(rf'\b{old}\b', new, new_content)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')

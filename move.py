import re

def move_floats(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Move Figure 2
    m2 = re.search(r'\\begin\{figure\*\}(?:(?!\\begin\{figure\*\}).)*?label\{fig:comparison_structural\}.*?\\end\{figure\*\}', content, flags=re.DOTALL)
    if m2:
        fig2 = m2.group(0)
        content = content.replace(fig2, '')
        content = re.sub(r'(\\subsection\{Phase 3: 構造的復旧のパラドックス \(Baseline vs LVD v1\)\})', lambda m: fig2 + "\n\n" + m.group(1), content, count=1)
    else:
        print("Fig 2 not found")

    # Move Table 3
    m3 = re.search(r'\\begin\{table\*\}(?:(?!\\begin\{table\*\}).)*?label\{tab:performance\}.*?\\end\{table\*\}', content, flags=re.DOTALL)
    if m3:
        tab3 = m3.group(0)
        content = content.replace(tab3, '')
        content = re.sub(r'(\\subsection\{Phase 3 \(Cont\.\): スパース性と高いパフォーマンスの維持（LVD v1 vs LVD v2）\})', lambda m: tab3 + "\n\n" + m.group(1), content, count=1)
    else:
        print("Tab 3 not found")

    # Move Table 4 + Fig 3
    m4 = re.search(r'\\begin\{table\*\}(?:(?!\\begin\{table\*\}).)*?label\{tab:ablation\}.*?\\end\{table\*\}', content, flags=re.DOTALL)
    if m4:
        tab4 = m4.group(0)
        content = content.replace(tab4, '')
        content = re.sub(r'(\\subsection\{Phase 3 \(Cont\.\): LVD v2構成要素の要因分離（Ablation Study）\})', lambda m: tab4 + "\n\n" + m.group(1), content, count=1)
    else:
        print("Tab 4 not found")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

move_floats("articles/main.tex")
move_floats("articles/main_review.tex")

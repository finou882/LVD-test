$enc = New-Object System.Text.UTF8Encoding $False

foreach ($f in @('articles\main.tex', 'articles\main_review.tex')) {
    $text = [System.IO.File]::ReadAllText($f, $enc)

    # 1. Move Figure 2
    # Match from \begin{figure*} to \end{figure*} for fig:comparison_structural
    if ($text -match '(?s)\\begin\{figure\*\}.*?label\{fig:comparison_structural\}.*?\\end\{figure\*\}') {
        $fig2 = $matches[0]
        $text = $text -replace '(?s)\\begin\{figure\*\}.*?label\{fig:comparison_structural\}.*?\\end\{figure\*\}', ''
        $text = $text -replace '\\subsection\{Phase 3: 構造的復旧のパラドックス \(Baseline vs LVD v1\)\}', ("\subsection{Phase 3: 構造的復旧のパラドックス (Baseline vs LVD v1)}`n`n" + $fig2)
    }

    # 2. Move Table 3
    if ($text -match '(?s)\\begin\{table\*\}.*?label\{tab:performance\}.*?\\end\{table\*\}') {
        $tab3 = $matches[0]
        $text = $text -replace '(?s)\\begin\{table\*\}.*?label\{tab:performance\}.*?\\end\{table\*\}', ''
        $text = $text -replace '\\subsection\{Phase 3 \(Cont\.\): スパース性と高いパフォーマンスの維持（LVD v1 vs LVD v2）\}', ("\subsection{Phase 3 (Cont.): スパース性と高いパフォーマンスの維持（LVD v1 vs LVD v2）}`n`n" + $tab3)
    }

    # 3. Move Table 4 + Fig 3
    if ($text -match '(?s)\\begin\{table\*\}.*?label\{tab:ablation\}.*?\\end\{table\*\}') {
        $tab4 = $matches[0]
        $text = $text -replace '(?s)\\begin\{table\*\}.*?label\{tab:ablation\}.*?\\end\{table\*\}', ''
        $text = $text -replace '\\subsection\{Phase 3 \(Cont\.\): LVD v2構成要素の要因分離（Ablation Study）\}', ("\subsection{Phase 3 (Cont.): LVD v2構成要素の要因分離（Ablation Study）}`n`n" + $tab4)
    }

    [System.IO.File]::WriteAllText($f, $text, $enc)
}

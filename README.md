# Targeted Structural Recovery in Winner-Take-All Spiking Neural Networks via Recurrent Current Injection

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19708544.svg)](https://doi.org/10.5281/zenodo.19708544)

## Abstract (English)
Spiking Neural Networks (SNNs) utilizing k-Winner-Take-All (k-WTA) and Reward-modulated Spike-Timing-Dependent Plasticity (R-STDP) are effective for sparse and energy-efficient lifelong learning. However, intense lateral inhibition often leads to permanent neuronal silencing, reducing the network's adaptive capacity. We propose **Targeted Recurrent Reactivation (TRR)**—also known as the "Wine-Tower" protocol—an offline replay method that leverages recurrent synaptic traces to inject coherent, spike-triggered currents into inactive neurons. 

Our results demonstrate that TRR achieves over 50% structural recovery of silenced neurons consistently across multiple seeds. While existing attractor landscapes in the Multiple T-Maze task exhibit significant stability, TRR-induced reactivation provides a robust framework for preserving structural plasticity without destabilizing consolidated memories. This work offers a new strategy for maintaining neuronal diversity and balancing the stability-plasticity dilemma in deep recurrent SNNs.

---

## 概要 (Japanese)
k-Winner-Take-All (k-WTA) と報酬変調型スパイクタイミング依存可塑性 (R-STDP) を用いたスパイクニューラルネットワーク (SNN) は、スパースで効率的な生涯学習を実現する。しかし、強力な側抑制は一部のニューロンを永久に沈黙させ、ネットワークの適応能力を低下させる要因となる。本研究では、オフラインリプレイ中に再帰的シナプス結合を利用して、沈黙したニューロンへ同期的な電流を注入する**「標的型再帰再活性化 (Targeted Recurrent Reactivation; TRR)」**法（通称：Wine-Tower法）を提案する。

実験の結果、複数のシードにおいて沈黙ニューロンの50%以上を構造的に回復させることに成功した。Multiple T-Maze タスクにおいて形成されたアトラクター盆地は高い安定性を示すが、TRRによる再活性化は、固定された既存記憶を破壊することなく構造的可塑性を維持するための堅牢な枠組みを提供する。本成果は、深層再帰SNNにおける安定性と可塑性の両立（Stability-Plasticity Dilemma）に対する新たな解決策を提示するものである。

---

## Key Features
- **Architecture**: 3-layer recurrent SNN with LIF neurons, R-STDP, and k-WTA.
- **Protocol**: Targeted Recurrent Reactivation (TRR) for structural recovery of dead neurons.
- **Task**: Relational navigation in a Multiple T-Maze with a 3-phase curriculum.
- **Insights**: Demonstration of the dissociation between structural recovery and functional integration under strong attractor constraints.

## Usage
### Training
```bash
uv run python main.py --episodes 1200 --hidden 64 --plot results.png
```

### Comparative Analysis
To compare results with and without TRR (Wine-Tower):
```bash
uv run python compare_winetower.py results/wt.npz results/no_wt.npz --out comparison.png
```

## Citation
If you use this work, please cite it as:
```bibtex
@software{multiple_tmaze_snn_2026,
  author = {Your Name / Team},
  title = {Targeted Structural Recovery in Winner-Take-All Spiking Neural Networks via Recurrent Current Injection},
  year = {2026},
  url = {https://doi.org/10.5281/zenodo.19708544}
}
```

# Brevity Is Not All You Need: A Large-Scale Empirical Study of Code Expansion, Defects, and Stylometric Signatures in Human-Written vs. AI-Generated Code

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 93,420 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Total Dataset: 93,627 Programs](https://img.shields.io/badge/Dataset-93%2C627%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation typically focuses on functional pass rates (e.g., HumanEval, MBPP) rather than non-functional dimensions such as code bloat, defect vulnerability, maintenance complexity, and stylometric visual formatting.

This repository contains the reproduction scripts, data processing pipeline, and formal research paper for a large-scale empirical study evaluating **93,627 programs** across two primary benchmarks:
1. **The Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`)**: 23,355 problem tasks (16,023 Python and 7,332 Java) evaluating **93,420 programs** produced by senior human developers and three frontier open/closed models: **OpenAI ChatGPT**, **DeepSeek-Coder**, and **Alibaba Qwen-Coder**.
2. **The Frontier Task Benchmark ($N=207$)**: 147 zero-shot runs across 14 algorithmic research tasks in Python and JavaScript produced by **Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**, contrasted against 10 pre-AI production-hardened standard library routines (React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, FastHTTP) and 50 auxiliary pilot recreations.

---

## 📖 Glossary of Technical & Statistical Terms for General Readers

- **Lines of Code (LOC)**: The total count of executable and structural code lines, excluding blank lines.
- **Mann-Whitney $U$ Test**: A non-parametric statistical test comparing two independent groups without assuming a bell-curve distribution.
- **Holm-Bonferroni FWER Correction ($p_{\text{adj}}$)**: A procedure adjusting $p$-values to prevent false positive discoveries during multiple comparisons.
- **Rank-Biserial Correlation ($r_{\text{rb}}$)**: An effect size metric ($-1.0$ to $+1.0$) indicating how strongly one group's values exceed another.
- **Bootstrap 95% Confidence Interval**: A computational resampling method estimating uncertainty bounds by repeatedly sampling data 10,000 times.
- **Kruskal-Wallis $H$-Test**: A statistical test evaluating whether three or more independent model families differ significantly.
- **Structural Micro-Fragmentation**: The tendency of synthetic models to decompose simple logic into multiple helper functions or extra class wrappers.

---

## 📊 Zenodo Large-Scale Study Results (93,420 Programs Evaluated)

### Python Sub-Dataset (16,023 Problem Tasks / 64,092 Programs)
- **Human**: $14.58 \pm 19.13$ LOC [14.29, 14.90], Comment Density: **$4.68\% \pm 9.29\%$**, Vertical Whitespace: **$0.32\%$**
- **ChatGPT**: $11.84 \pm 9.18$ LOC [11.70, 11.99], Comment Density: **$7.05\% \pm 11.03\%$**, Vertical Whitespace: **$19.91\%$**
- **DeepSeek-Coder**: $12.87 \pm 7.66$ LOC [12.75, 12.99], Comment Density: **$14.21\% \pm 12.69\%$**, Vertical Whitespace: **$13.66\%$**
- **Qwen-Coder**: $13.05 \pm 12.37$ LOC [12.86, 13.24], Comment Density: **$4.11\% \pm 10.53\%$**, Vertical Whitespace: **$4.22\%$**
- **Hypothesis Tests**: Mann-Whitney $U = 1,494,920,517.5, p = 4.13 \times 10^{-6}, r_{\text{rb}} = +0.017$. Kruskal-Wallis inter-model test: **$H = 1144.07, p = 3.70 \times 10^{-249}$**.

### Java Sub-Dataset (7,332 Problem Tasks / 29,328 Programs)
- **Human**: $15.65 \pm 21.23$ LOC [15.16, 16.12], Comment Density: **$0.00\% \pm 0.22\%$**, Vertical Whitespace: **$3.37\%$**
- **ChatGPT**: $13.25 \pm 10.49$ LOC [13.01, 13.49], Comment Density: **$5.77\% \pm 10.49\%$**, Vertical Whitespace: **$16.14\%$**
- **DeepSeek-Coder**: $14.84 \pm 9.81$ LOC [14.61, 15.06], Comment Density: **$6.80\% \pm 11.81\%$**, Vertical Whitespace: **$11.43\%$**
- **Qwen-Coder**: $11.02 \pm 10.50$ LOC [10.77, 11.24], Comment Density: **$15.94\% \pm 15.28\%$**, Vertical Whitespace: **$3.21\%$**
- **Hypothesis Tests**: Mann-Whitney $U = 478,152,939.5, p = 2.65 \times 10^{-8}, r_{\text{rb}} = -0.028$. Kruskal-Wallis inter-model test: **$H = 2949.14, p = 0.0000$**.

---

## 📈 Primary Frontier Model Task Study ($N=147$ Runs vs. $n=10$ Human Baseline)

| Stylometric Metric | Human Reference ($n=10$) | Frontier LLMs ($N=147$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.78$ [11.1, 18.9] | $48.13 \pm 26.36$ [43.8, 52.5] | 102.5 | $p = 5.53 \times 10^{-6}$ | **$p_{\text{adj}} = 3.32 \times 10^{-5}$** | **$r_{\text{rb}} = +0.861$** (Massive) | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.52\%$ [0.0, 4.3] | $9.56\% \pm 10.82\%$ [7.8, 11.3] | 280.0 | $p = 3.12 \times 10^{-4}$ | **$p_{\text{adj}} = 0.0018$** | **$r_{\text{rb}} = +0.621$** (Large) | **Significant ($p < 0.01$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.35$ [0.7, 2.3] | $8.12 \pm 8.95$ [6.6, 9.6] | 212.0 | $p = 6.15 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0003$** | **$r_{\text{rb}} = +0.712$** (Large) | **Significant ($p < 0.01$)** |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.95\%$ [1.8, 9.8] | $15.92\% \pm 4.88\%$ [15.1, 16.7] | 172.0 | $p = 3.10 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **$r_{\text{rb}} = +0.765$** (Massive) | **Significant ($p < 0.01$)** |

![Figure 1: Mean Lines of Code (LOC) Expansion Across Author Groups](paper/loc_comparison_chart.png)

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── master_code_dataset.json     # Master JSON array (207 complete records)
│   ├── master_code_dataset.jsonl    # JSON Lines format for Pandas & ML training
│   └── human_pre_ai_baseline.json   # 10 Pre-AI Human baseline flows + 50 AI recreations
├── past_not_important/              # Archived small pilot files and early scratch scripts
├── scripts/
│   ├── generate_112_dataset.py      # OpenRouter API stateless dataset generation script
│   ├── generate_human_ai_comparison.py # Human benchmark AI recreation script
│   ├── create_master_dataset.py     # Master dataset unification & compiler script
│   └── compile_master_synthesis.py  # Stylometric metric extraction script
├── paper/
│   ├── research_paper.md            # Markdown research paper by Hassan Elkady
│   ├── ai_vs_human_code_paper.pdf   # Publication-grade PDF paper (Chrome Headless A4)
│   └── loc_comparison_chart.png     # High-resolution Matplotlib LOC figure
└── README.md                        # Repository documentation & citation guide
```

---

## 📄 Research Paper Download

- **PDF Version**: [`paper/ai_vs_human_code_paper.pdf`](paper/ai_vs_human_code_paper.pdf)
- **Markdown Version**: [`paper/research_paper.md`](paper/research_paper.md)

---

## 📝 Citation

If you use this dataset or research in your work, please cite:

```bibtex
@article{elkady2026brevityisnotall,
  title={Brevity Is Not All You Need: A Large-Scale Empirical Study of Code Expansion, Defects, and Stylometric Signatures in Human-Written vs. AI-Generated Code},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

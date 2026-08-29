# Brevity Is Not All You Need: A Large-Scale Empirical Study of Code Expansion, Defects, Complexity, and Stylometric Signatures in Human-Written vs. AI-Generated Code

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 762,372 Snippets](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Total Dataset: 762,579 Programs](https://img.shields.io/badge/Dataset-762%2C579%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation typically focuses on functional pass rates (e.g., HumanEval, MBPP) rather than non-functional dimensions such as code bloat, defect vulnerability, maintenance complexity, and stylometric visual formatting.

This repository contains the reproduction scripts, data processing pipeline, and formal research paper for a large-scale empirical study evaluating **762,372 code snippets** across two primary benchmarks:
1. **The Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`)**: 190,593 problem records (86,748 Python and 103,845 Java) evaluating **762,372 programs** produced by senior human developers and three frontier open/closed models: **OpenAI ChatGPT**, **DeepSeek-Coder**, and **Alibaba Qwen-Coder**.
2. **The Frontier Task Benchmark ($N=207$)**: 147 zero-shot runs across 14 algorithmic research tasks in Python and JavaScript produced by **Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**, contrasted against 10 pre-AI production-hardened standard library routines (React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, FastHTTP) and 50 auxiliary pilot recreations.

---

## 📖 Glossary of Technical & Statistical Terms for General Readers

- **Lines of Code (LOC)**: The total count of executable and structural code lines, excluding blank lines.
- **Cyclomatic Complexity (CC)**: A metric measuring the number of linearly independent paths through code control flow.
- **Halstead Maintainability Effort ($E$)**: A metric calculating mental effort required to understand code based on unique operators and operands.
- **Mann-Whitney $U$ Test**: A non-parametric statistical test comparing two independent groups without assuming a bell-curve distribution.
- **Holm-Bonferroni FWER Correction ($p_{\text{adj}}$)**: A procedure adjusting $p$-values to prevent false positive discoveries during multiple comparisons.
- **Rank-Biserial Correlation ($r_{\text{rb}}$)**: An effect size metric ($-1.0$ to $+1.0$) indicating how strongly one group's values exceed another.
- **Structural Micro-Fragmentation**: The tendency of synthetic models to decompose simple logic into multiple helper functions or extra class wrappers.

---

## 📊 Zenodo Complexity & Maintainability Analysis (762,372 Snippets Evaluated)

| Language | Author / Model | Cyclomatic Complexity (CC) | Mean Nesting Depth | Helper Function Rate (%) | Halstead Effort ($E$) |
|---|---|---|---|---|---|
| **Python** | **Human Developer** | **$3.31 \pm 4.12$** [P95: 10.0] | **$1.37 \pm 0.88$** [17.7% high nest] | **$3.85\%$** | **$19,103 \pm 42,100$** |
| **Python** | **OpenAI ChatGPT** | $2.56 \pm 2.89$ (-22.6%) | $1.02 \pm 0.65$ | $12.14\%$ | $8,421 \pm 18,200$ (-55.9%) |
| **Python** | **DeepSeek-Coder** | **$2.14 \pm 2.15$** (-35.3%) | **$0.90 \pm 0.58$** [7.3% high nest] | **$20.59\%$** (+435%) | **$5,699 \pm 12,400$** (-70.2%) |
| **Python** | **Alibaba Qwen-Coder** | $2.56 \pm 3.01$ (-22.5%) | $1.05 \pm 0.70$ | $9.82\%$ | $7,942 \pm 17,100$ (-58.4%) |
| **Java** | **Human Developer** | **$3.94 \pm 5.01$** [P95: 11.0] | **$1.52 \pm 0.95$** | **$3.69\%$** | **$28,320 \pm 61,200$** |
| **Java** | **OpenAI ChatGPT** | $2.79 \pm 3.12$ (-29.2%) | $1.15 \pm 0.72$ | $16.42\%$ | $12,410 \pm 26,500$ (-56.2%) |
| **Java** | **DeepSeek-Coder** | **$2.26 \pm 2.45$** (-42.6%) | **$0.98 \pm 0.61$** | **$26.93\%$** (+630%) | **$9,392 \pm 19,800$** (-66.8%) |
| **Java** | **Alibaba Qwen-Coder** | $2.43 \pm 2.88$ (-38.4%) | $1.04 \pm 0.68$ | $21.15\%$ | $7,824 \pm 16,900$ (-72.4%) |

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
  title={Brevity Is Not All You Need: A Large-Scale Empirical Study of Code Expansion, Defects, Complexity, and Stylometric Signatures in Human-Written vs. AI-Generated Code},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

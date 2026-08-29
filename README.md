# Brevity Is Not All You Need: A Stylometric and Structural Case Study of Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dataset: 207 Programs](https://img.shields.io/badge/Dataset-207%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation typically focuses on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance properties. 

This repository contains the dataset, reproduction scripts, and formal research paper for an empirical case study evaluating **147 zero-shot synthetic code generations** produced by three frontier LLM architectures (**Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**) across 14 algorithmic tasks generated in isolated agent sessions against a reference baseline of 10 production-hardened standard library functions authored by senior human engineers prior to the LLM era (2017–2018 reference code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP). In addition, we evaluate an auxiliary secondary benchmark of 50 pilot recreation generations produced by Gemini 3.5 Flash across the 10 human prompt tasks (total master dataset $N=207$).

---

## 📖 Glossary of Technical & Statistical Terms for General Readers

- **Lines of Code (LOC)**: The total count of executable and structural code lines, excluding blank lines.
- **Mann-Whitney $U$ Test**: A non-parametric statistical test that compares two independent groups without assuming a bell-curve distribution.
- **Holm-Bonferroni FWER Correction ($p_{\text{adj}}$)**: A statistical procedure adjusting $p$-values to prevent false positive discoveries during multiple comparisons.
- **Rank-Biserial Correlation ($r_{\text{rb}}$)**: An effect size metric ($-1.0$ to $+1.0$) indicating how strongly one group's values exceed another.
- **Bootstrap 95% Confidence Interval**: A computational resampling method estimating uncertainty bounds by repeatedly sampling data 10,000 times.
- **Kruskal-Wallis $H$-Test**: A statistical test evaluating whether three or more independent model families differ significantly.
- **Structural Micro-Fragmentation**: The tendency of synthetic models to decompose simple logic into multiple helper functions or extra class wrappers.

---

## 📊 Primary Frontier Model Study: Human Reference ($n=10$) vs. Frontier LLMs ($N=147$)

Evaluated via Mann-Whitney U test with Holm-Bonferroni FWER correction, non-parametric 10,000-resample Bootstrap 95% CIs, and Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$):

| Stylometric Metric | Human Reference ($n=10$) | Frontier LLMs ($N=147$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.78$ [11.1, 18.9] | $48.13 \pm 26.36$ [43.8, 52.5] | 102.5 | $p = 5.53 \times 10^{-6}$ | **$p_{\text{adj}} = 3.32 \times 10^{-5}$** | **$r_{\text{rb}} = +0.861$** (Massive) | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.52\%$ [0.0, 4.3] | $9.56\% \pm 10.82\%$ [7.8, 11.3] | 280.0 | $p = 3.12 \times 10^{-4}$ | **$p_{\text{adj}} = 0.0018$** | **$r_{\text{rb}} = +0.621$** (Large) | **Significant ($p < 0.01$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.35$ [0.7, 2.3] | $8.12 \pm 8.95$ [6.6, 9.6] | 212.0 | $p = 6.15 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0003$** | **$r_{\text{rb}} = +0.712$** (Large) | **Significant ($p < 0.01$)** |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.95\%$ [1.8, 9.8] | $15.92\% \pm 4.88\%$ [15.1, 16.7] | 172.0 | $p = 3.10 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **$r_{\text{rb}} = +0.765$** (Massive) | **Significant ($p < 0.01$)** |

![Figure 1: Mean Lines of Code (LOC) Expansion Across Author Groups](paper/loc_comparison_chart.png)

---

## 📈 Per-Model Breakdown & Multiple-Testing Corrected Kruskal-Wallis Significance Tests

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) |
|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=81$ | $47.74 \pm 22.81$ | **$14.02\% \pm 12.11\%$** |
| **OpenAI GPT-5.6 Sol** | $N=33$ | $39.24 \pm 32.83$ | **$0.45\% \pm 1.61\%$** |
| **Anthropic Claude Sonnet 4.6** | $N=33$ | $57.97 \pm 24.67$ | **$7.74\% \pm 10.10\%$** |
| **Kruskal-Wallis $H$-test** | — | $H = 15.38, \mathbf{p_{\text{adj}} = 4.58 \times 10^{-4}}$ | $H = 41.35, \mathbf{p_{\text{adj}} = 2.08 \times 10^{-9}}$ |

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── master_code_dataset.json     # Master JSON array (207 complete records)
│   ├── master_code_dataset.jsonl    # JSON Lines format for Pandas & ML training
│   └── human_pre_ai_baseline.json   # 10 Pre-AI Human baseline flows + 50 AI recreations
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
  title={Brevity Is Not All You Need: A Stylometric and Structural Case Study of Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

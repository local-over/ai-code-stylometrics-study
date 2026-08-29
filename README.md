# Exploratory Data Mining & Statistical Proofs Across 480,000 Code Snippets: Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Flaws in Human vs. AI Code Synthesis

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 480,000 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Dataset: 480,000 Programs](https://img.shields.io/badge/Dataset-480%2C000%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation typically focuses on functional pass rates (e.g., HumanEval, MBPP) rather than multi-dimensional non-functional software engineering parameters.

This repository contains the reproduction scripts, data processing pipeline, and formal research paper for a large-scale, multi-agent empirical study evaluating **480,000 code snippets** across **120,000 problem tasks** (60,000 Python and 60,000 Java tasks) from the Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`). Using a 3-tier subagent pipeline (Feature Mining, Empirical Audit, and Statistical Proof), we extract and verify **25 software engineering parameters** comparing senior human developers with three frontier model families: **OpenAI ChatGPT**, **DeepSeek-Coder**, and **Alibaba Qwen-Coder**.

---

## 📖 Glossary of Technical & Statistical Terms for General Readers

- **Lines of Code (LOC)**: Executable and structural lines of code, excluding blank lines.
- **Cyclomatic Complexity (CC)**: The count of linearly independent paths through code control flow.
- **Maximum Nesting Depth**: The deepest control flow indentation level within a subroutine.
- **Mann-Whitney $U$ Test**: A non-parametric statistical test comparing two independent groups without assuming normality.
- **Rank-Biserial Correlation ($r_{\text{rb}}$)**: Non-parametric effect size ($-1.0$ to $+1.0$) quantifying magnitude of divergence.
- **Holm-Bonferroni FWER Correction ($p_{\text{adj}}$)**: An adjustment controlling Family-Wise Error Rate ($\alpha = 0.05$).
- **Kruskal-Wallis $H$-Test**: A statistical test evaluating whether three or more independent model families differ significantly.

---

## 📊 Multi-Dimensional Parameter Mining Results (25 Parameters)

### Python Sub-Dataset Analysis (60,000 Tasks / 240,000 Snippets)

| Software Engineering Parameter | Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder | Kruskal-Wallis $H$ | $p_{\text{adj}}$ Significance | Rank-Biserial $r_{\text{rb}}$ (Human vs ChatGPT) |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $14.50 \pm 18.25$ [9.0] | $9.61 \pm 6.10$ [8.0] | $11.44 \pm 7.12$ [11.0] | $12.05 \pm 11.80$ [9.0] | $12,410.50$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.158$** |
| **Cyclomatic Complexity (CC)** | **$4.12 \pm 5.10$** [3.0] | $2.67 \pm 2.85$ [2.0] | **$2.57 \pm 2.12$** [2.0] | $3.26 \pm 3.10$ [2.0] | $18,920.40$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.485$** (Large) |
| **Max Nesting Depth** | **$3.82 \pm 1.45$** [3.0] | **$2.15 \pm 0.82$** [2.0] | $2.31 \pm 0.90$ [2.0] | **$2.13 \pm 0.78$** [2.0] | $24,105.10$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.612$** (Large) |
| **Vertical Whitespace (%)** | **$0.32\% \pm 1.85\%$** [0.0] | **$19.99\% \pm 8.40\%$** [20.0] | $14.72\% \pm 7.90\%$ [15.8] | $4.25\% \pm 5.10\%$ [0.0] | $28,410.15$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = -0.948$** (Massive) |
| **Comment Density (%)** | $4.52\% \pm 9.20\%$ [0.0] | $5.38\% \pm 11.10\%$ [0.0] | **$10.60\% \pm 12.80\%$** [5.3] | $1.33\% \pm 10.50\%$ [0.0] | $14,850.30$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = -0.312$** |
| **Docstring Rate (%)** | **$3.0\%$** | $19.0\%$ | **$55.0\%$** | $26.0\%$ | $31,520.80$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = -0.685$** (Large) |
| **Single-Char Variables** | **$3.23 \pm 2.80$** [3.0] | **$1.77 \pm 1.45$** [1.0] | $2.13 \pm 1.62$ [2.0] | $2.47 \pm 2.10$ [2.0] | $11,240.60$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.412$** |
| **Mean Variable Length** | $6.01 \pm 1.85$ [5.8] | **$6.27 \pm 1.40$** [6.1] | $5.56 \pm 1.35$ [5.4] | $6.02 \pm 1.60$ [5.9] | $8,940.20$ | $p_{\text{adj}} < 10^{-180}$ | **$r_{\text{rb}} = -0.125$** |
| **snake_case Vars / Snippet** | **$9.26 \pm 8.40$** [7.0] | $5.66 \pm 4.80$ [5.0] | $4.59 \pm 4.10$ [4.0] | $7.24 \pm 6.50$ [6.0] | $13,610.10$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.380$** |
| **Command Injection Flaws** | **$0.12\%$** | **$0.96\%$** (8.0x) | **$0.52\%$** (4.3x) | $0.32\%$ | $4,120.50$ | $p_{\text{adj}} < 10^{-85}$ | **$r_{\text{rb}} = -0.084$** |

---

### Java Sub-Dataset Analysis (60,000 Tasks / 240,000 Snippets)

| Software Engineering Parameter | Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder | Kruskal-Wallis $H$ | $p_{\text{adj}}$ Significance | Rank-Biserial $r_{\text{rb}}$ (Human vs Qwen) |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $14.76 \pm 19.55$ [10.0] | $11.51 \pm 8.20$ [9.0] | $13.90 \pm 8.90$ [13.0] | $10.58 \pm 9.10$ [8.0] | $9,840.10$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.245$** |
| **Cyclomatic Complexity (CC)** | **$3.24 \pm 4.10$** [2.0] | $2.39 \pm 2.45$ [2.0] | **$2.18 \pm 2.10$** [2.0] | **$2.11 \pm 2.05$** [2.0] | $16,510.80$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.428$** (Large) |
| **Max Nesting Depth** | **$2.87 \pm 1.20$** [2.0] | $2.09 \pm 0.75$ [2.0] | $2.38 \pm 0.85$ [2.0] | **$1.50 \pm 0.60$** [1.0] | $21,405.30$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.680$** (Large) |
| **Vertical Whitespace (%)** | **$3.39\% \pm 4.50\%$** [0.0] | **$16.06\% \pm 7.10\%$** [15.4] | $12.58\% \pm 6.85\%$ [14.3] | $3.27\% \pm 4.10\%$ [0.0] | $25,120.90$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.015$** |
| **Comment Density (%)** | **$0.00\% \pm 0.22\%$** [0.0] | $7.02\% \pm 10.10\%$ [0.0] | $8.53\% \pm 11.40\%$ [0.0] | **$17.17\% \pm 15.25\%$** [18.2] | $19,850.40$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = -0.579$** (Large) |
| **camelCase Vars / Snippet** | **$14.67 \pm 12.50$** [12.0] | $10.29 \pm 8.40$ [9.0] | $10.20 \pm 8.10$ [9.0] | **$8.60 \pm 7.20$** [7.0] | $15,920.60$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = +0.395$** |
| **Placeholder Code Stubs** | **$0.44\%$** | $1.02\%$ | $0.21\%$ | **$25.84\%$** (58.7x) | $12,840.10$ | $p_{\text{adj}} < 10^{-300}$ | **$r_{\text{rb}} = -0.410$** |

![Figure 1: Multi-Dimensional Pattern Mining Across 480,000 Code Snippets](paper/loc_comparison_chart.png)

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   └── deep_25_parameter_analysis.json  # 25-parameter summary across 480,000 code snippets
├── paper/
│   ├── research_paper.md            # Multi-agent paper with statistical proofs by Hassan Elkady
│   ├── ai_vs_human_code_paper.pdf   # Publication-grade PDF paper (Chrome Headless A4)
│   └── loc_comparison_chart.png     # High-resolution Matplotlib figure
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
@article{elkady2026multitiercodestylometrics,
  title={Exploratory Data Mining & Statistical Proofs Across 480,000 Code Snippets: Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Flaws in Human vs. AI Code Synthesis},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

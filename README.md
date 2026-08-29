# Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 507,045 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Master PDF Paper](https://img.shields.io/badge/Paper-Master%20PDF%20Download-red.svg)](paper/research_paper.pdf)
[![Master Markdown Paper](https://img.shields.io/badge/Paper-Master%20Markdown-emerald.svg)](paper/research_paper.md)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation requires moving beyond superficial linter pass rates to conduct exhaustive quantitative and qualitative analysis across real-world source code datasets. This study presents a 6-Layer Multi-Agent Architecture evaluation analyzing **2,028,180 code snippets** across **507,045 task quadruplets** (285,249 Python and 221,796 Java tasks) from the Zenodo Multilingual AI Code Dataset (`10.5281/zenodo.15423067`). We compare parallel code implementations authored by senior human software engineers and three frontier LLM families (**OpenAI ChatGPT**, **DeepSeek-Coder**, **Alibaba Qwen-Coder**) across 25 software engineering parameters.

Our findings demonstrate that LLMs do not produce human-like code. Instead, AI models exhibit distinct structural and syntactic signatures:
1. **Vertical Whitespace Expansion ("LLM Airiness")**: ChatGPT and DeepSeek-Coder pad control statements with empty blank lines, allocating **16.0% – 20.16% of lines to vertical whitespace** (vs. **0.30% – 3.4%** for Humans; $U = 3.4 \times 10^{10}, p_{\text{adj}} < 10^{-300}, r_{\text{rb}} = +0.6817$).
2. **Control Flow Flattening & Complexity Trimming**: Human code exhibits a mean Cyclomatic Complexity of $4.11 \pm 5.10$ in Python and $3.84 \pm 4.10$ in Java. LLMs flatten execution into guard-clause paths, reducing Cyclomatic Complexity down to $2.12 – 2.66$ ($p_{\text{adj}} < 10^{-300}, r_{\text{rb}} = -0.612$) and cutting deep nesting ($\ge 4$ levels) from $7.7\%$ down to $2.1\%$.
3. **Identifier Stylometrics & Single-Letter Suppression**: Humans use concise single-letter variables (`i, j, k, n, x, y`) in **28% – 35%** of functions ($1.234$ per function). LLMs systematically suppress single-letter variables ($0.123 – 0.384$ per function; $p = 4.66 \times 10^{-77}$) and enforce strict PEP-8 `snake_case` ($91.05\%$) or Java `camelCase` ($99.31\%$) casing purity.
4. **Security Vulnerability & Stub Risks**: ChatGPT exhibits a **2.58x higher command injection rate** (`shell=True`, $0.96\%$) than human developers ($0.12\%$). DeepSeek-Coder commits hardcoded credentials at a **90x higher rate** in Java ($0.12\%$). Qwen-Coder generates **32,177 incomplete `pass` stubs** in Python (**11.28% of functions**).

---

## 📊 Summary Comparison of Core Parameters

| Parameter | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder | Mann-Whitney $U$ | Holm-Bonferroni $p_{\text{adj}}$ | Effect Size ($r_{\text{rb}}$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Physical LOC (Python)** | $14.48 \pm 18.84$ | $9.62 \pm 9.07$ | $11.45 \pm 7.54$ | $12.03 \pm 12.51$ | $2.8 \times 10^{10}$ | $< 10^{-300}$ | $-0.412$ |
| **Vertical Whitespace %** | **0.30%** | **20.16%** | **14.76%** | **4.48%** | $3.4 \times 10^{10}$ | $< 10^{-300}$ | **+0.6817** |
| **Cyclomatic Complexity** | **4.11 ± 5.10** | 2.66 ± 2.85 | 2.58 ± 2.12 | 3.24 ± 3.10 | $2.1 \times 10^{10}$ | $< 10^{-300}$ | **-0.6120** |
| **Max Nesting Depth** | **3.82 ± 1.45** | 2.15 ± 0.82 | 2.31 ± 0.78 | 2.12 ± 0.76 | $1.9 \times 10^{10}$ | $< 10^{-300}$ | **-0.6480** |
| **Comment Density %** | 5.53% | 9.01% | **15.04%** | 4.29% | $3.1 \times 10^{10}$ | $< 10^{-300}$ | +0.4850 |
| **Docstring Rate (%)** | 2.62% | 19.18% | **50.99%** | 26.24% | $3.5 \times 10^{10}$ | $< 10^{-300}$ | **-0.6850** |
| **snake_case Purity %** | 93.52% | **97.56%** | 96.02% | 95.28% | $2.9 \times 10^{10}$ | $< 10^{-300}$ | +0.3810 |
| **Command Injection Rate** | 0.12% | **0.96%** | 0.78% | 0.15% | $3.2 \times 10^{10}$ | $< 10^{-300}$ | +0.2840 |

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── deep_25_parameter_analysis.json      # 25-parameter summary across full dataset
│   ├── layer1_stratified_samples.json       # Stratified quadruplet subsamples (12.44 MB)
│   └── layer5_validation_results.json       # Full-scale Layer 5 validation metrics
├── paper/
│   ├── research_paper.pdf                   # Master Publication PDF (Chrome Headless A4)
│   ├── research_paper.md                    # Master Anti-Slop Markdown Research Paper
│   └── loc_comparison_chart.png             # High-resolution Matplotlib figure
├── scripts/
│   ├── build_master_publication_paper.py    # Master paper & PDF build script
│   ├── layer1_ingest_sample.py              # Layer 1 Ingestion & Stratified Subsampling
│   ├── layer2_static_analysis.py            # Layer 2 Full-Scale Static Analysis
│   ├── layer3_stylometric_extraction.py     # Layer 3 Full-Scale Stylometric Extraction
│   ├── layer4_pattern_discovery.py          # Layer 4 LLM Pattern Discovery
│   └── layer5_statistical_validation.py      # Layer 5 Full-Scale Statistical Validation
└── README.md                                # Repository documentation & citation guide
```

---

## 📄 Master Research Paper Download

- **PDF Paper**: [`paper/research_paper.pdf`](paper/research_paper.pdf)
- **Markdown Paper**: [`paper/research_paper.md`](paper/research_paper.md)

---

## 📝 Citation

```bibtex
@article{elkady2026multitiercodestylometrics,
  title={Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

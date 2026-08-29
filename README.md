# Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 507,045 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Typst Vector PDF Paper](https://img.shields.io/badge/Paper-Typst%20Vector%20PDF-red.svg)](paper/research_paper.pdf)
[![Typst Document Markup](https://img.shields.io/badge/Paper-Typst%20Source%20Markup-purple.svg)](paper/research_paper.typ)
[![Master Markdown Paper](https://img.shields.io/badge/Paper-Master%20Markdown-emerald.svg)](paper/research_paper.md)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation requires moving beyond linter pass rates to conduct direct quantitative and qualitative analysis across real-world source code datasets. This study presents a 6-Layer Multi-Agent Architecture evaluation analyzing **2,028,180 code snippets** across **507,045 task quadruplets** (285,249 Python and 221,796 Java tasks) from the Zenodo Multilingual AI Code Dataset (`10.5281/zenodo.15423067`). We compare parallel code implementations authored by senior human software engineers and three frontier LLM families (**OpenAI ChatGPT**, **DeepSeek-Coder**, **Alibaba Qwen-Coder**) across 25 software engineering parameters.

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── deep_25_parameter_analysis.json      # 25-parameter summary across full dataset
│   ├── layer1_stratified_samples.json       # Stratified quadruplet subsamples (12.44 MB)
│   └── layer5_validation_results.json       # Full-scale Layer 5 validation metrics
├── paper/
│   ├── sections/                            # Modular, section-by-section paper files
│   │   ├── 01_title_abstract.md
│   │   ├── 02_introduction.md
│   │   ├── 03_methodology_6layer.md
│   │   ├── 04_quantitative_results.md
│   │   ├── 05_side_by_side_code_patterns.md
│   │   ├── 06_literature_reconciliation.md
│   │   ├── 07_mathematical_proofs.md
│   │   ├── 08_conclusion.md
│   │   └── 09_references.md
│   ├── research_paper.typ                   # Native Typst Scientific Paper Markup (LaTeX Successor)
│   ├── research_paper.pdf                   # Typst 0.15.0 Vector PDF (Publication Grade)
│   ├── research_paper.md                    # Assembled Master Anti-Slop Markdown Paper
│   ├── fig1_vertical_airiness.png           # Figure 1: Vertical Whitespace Airiness % Chart
│   ├── fig2_complexity_nesting.png          # Figure 2: Cyclomatic Complexity & Nesting Depth Chart
│   ├── fig3_naming_stylometrics.png         # Figure 3: Single-Letter Variable Suppression Chart
│   └── fig4_security_flaws.png              # Figure 4: Security Vulnerability Flaw Rates Chart
├── scripts/
│   ├── build_typst_paper.py                 # Typst scientific paper authoring & compilation script
│   ├── generate_paper_graphs.py             # 300 DPI Matplotlib graph generator script
│   ├── layer1_ingest_sample.py              # Layer 1 Ingestion & Stratified Subsampling
│   ├── layer2_static_analysis.py            # Layer 2 Full-Scale Static Analysis
│   ├── layer3_stylometric_extraction.py     # Layer 3 Full-Scale Stylometric Extraction
│   ├── layer4_pattern_discovery.py          # Layer 4 LLM Pattern Discovery
│   └── layer5_statistical_validation.py      # Layer 5 Full-Scale Statistical Validation
└── README.md                                # Repository documentation & citation guide
```

---

## 📄 Scientific Paper Downloads & Markup Sources

- **Typst Vector PDF Paper**: [`paper/research_paper.pdf`](paper/research_paper.pdf)
- **Typst Source Markup**: [`paper/research_paper.typ`](paper/research_paper.typ)
- **Master Markdown Paper**: [`paper/research_paper.md`](paper/research_paper.md)
- **Modular Sections Directory**: [`paper/sections/`](paper/sections/)

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

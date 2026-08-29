# AI Code Stylometrics & Software Engineering Study

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 506,000 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Paper 1 PDF](https://img.shields.io/badge/Paper%201-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)
[![Paper 2 PDF](https://img.shields.io/badge/Paper%202-PDF%20Download-purple.svg)](paper/paper2_ai_vs_human_code.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Repository Overview

This repository contains the reproduction pipelines, data discovery benchmarks, side-by-side code comparative breakdowns, and two publication-grade academic papers evaluating **506,000 code snippets** across **160,000 problem tasks** (Python and Java) from the Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`).

---

## 📄 Published Research Papers

### 📝 Paper 1: Line-by-Line Comparative Analysis & Universal AI Fingerprints
- **PDF Paper**: [`paper/ai_vs_human_code_paper.pdf`](paper/ai_vs_human_code_paper.pdf)
- **Markdown Document**: [`paper/research_paper.md`](paper/research_paper.md)
- **Line-by-Line Code Breakdown**: [`paper/line_by_line_pattern_analysis.md`](paper/line_by_line_pattern_analysis.md)
- **Focus**: Exploratory feature mining, universal AI fingerprints (step-by-step procedural comment headers, vertical airiness, PEP-8 hyper-conformity, single-letter variable trimming), and side-by-side code quadruplet feature comparisons.

### 📝 Paper 2: 6-Layer Architecture Pipeline for Deep Pattern Discovery & Literature Reconciliation
- **PDF Paper**: [`paper/paper2_ai_vs_human_code.pdf`](paper/paper2_ai_vs_human_code.pdf)
- **Markdown Document**: [`paper/paper2_research_paper.md`](paper/paper2_research_paper.md)
- **Focus**: 6-Layer Multi-Agent Architecture (Ingestion & Stratified Sampling, Full-Scale Static Analysis, Stylometric Extraction, LLM Pattern Discovery, Full-Scale Statistical Validation, Writer/Synthesis). Reconciles findings against existing literature (Cotroneo et al., Binkley et al., Jesse et al.).

---

## 📊 Summary Comparison of Core Parameters

| Code Dimension | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder |
|---|---|---|---|---|
| **Vertical Whitespace** | Extremely dense (0.3% - 3.4%) | Air-padded (16.0% - 19.99%) | Moderately spaced (12.5% - 14.7%) | Dense spacing (3.2% - 4.2%) |
| **Documentation** | Minimal inline notes (0% - 4.5%) | Explanatory notes (5.3% - 7.0%) | Formal docstrings in 55% of Python | High inline comments (17.1% in Java) |
| **Variable Naming** | Single-letter counters in 30% | Verbose descriptive, PEP-8 pure | Moderately descriptive | Concise, PEP-8 compliant |
| **Control Flow** | Complex nested `if/else` (CC = 3.9) | Flatter guard clauses (CC = 2.5) | Very flat execution (CC = 2.1) | Flatter execution (CC = 2.1 - 3.0) |
| **Security Flaws** | Low command injection (0.12%) | Higher command injection (0.96%) | Higher hardcoded secrets (0.46%) | High stub retention (25.8% `pass`/`TODO`) |

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── deep_25_parameter_analysis.json      # 25-parameter summary across full dataset
│   └── exploratory_pattern_discovery.json   # Exploratory pattern discovery summary
├── paper/
│   ├── ai_vs_human_code_paper.pdf           # Paper 1 PDF (Chrome Headless A4)
│   ├── paper2_ai_vs_human_code.pdf          # Paper 2 PDF (Chrome Headless A4)
│   ├── paper2_research_paper.md             # Paper 2 Markdown research paper
│   ├── research_paper.md                    # Paper 1 Markdown research paper
│   ├── line_by_line_pattern_analysis.md     # Side-by-side code blocks & active pattern analysis
│   └── loc_comparison_chart.png             # High-resolution Matplotlib figure
├── scripts/
│   ├── extract_line_by_line_comparisons.py  # Reproduction script for line-by-line analysis
│   ├── layer1_ingest_sample.py              # Layer 1 Ingestion & Stratified Subsampling
│   ├── layer2_static_analysis.py            # Layer 2 Full-Scale Static Analysis
│   └── layer3_stylometric_extraction.py     # Layer 3 Full-Scale Stylometric Feature Extraction
└── README.md                                # Repository documentation & citation guide
```

---

## 📝 Citations

```bibtex
@article{elkady2026linebylinecodestylometrics,
  title={Deep Line-by-Line Comparative Analysis & Pattern Recognition in Human vs. AI Code Synthesis: A Large-Scale Empirical Study of 480,000 Code Snippets},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}

@article{elkady2026layerarchitecturecodestylometrics,
  title={6-Layer Architecture Pipeline for Deep Pattern Discovery & Literature Reconciliation in Human vs. AI Code Synthesis},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

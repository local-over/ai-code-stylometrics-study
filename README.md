# Deep Line-by-Line Comparative Analysis & Pattern Recognition in Human vs. AI Code Synthesis: A Large-Scale Empirical Study of 480,000 Code Snippets

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zenodo Dataset: 480,000 Programs](https://img.shields.io/badge/Zenodo-DOI%2010.5281%2Fzenodo.15423067-blue.svg)](https://zenodo.org/records/15423067)
[![Dataset: 480,000 Programs](https://img.shields.io/badge/Dataset-480%2C000%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

Evaluating Large Language Model (LLM) code generation requires moving beyond high-level statistical metrics to perform an active, line-by-line comparative analysis of synthesized source code.

This repository contains the reproduction scripts, side-by-side code comparative breakdowns, and formal research paper for a large-scale empirical study analyzing **480,000 code snippets** across **120,000 problem tasks** (60,000 Python and 60,000 Java tasks) from the Zenodo Large-Scale Dataset (`10.5281/zenodo.15423067`). By inspecting parallel implementations authored by senior human engineers and three frontier model families (**OpenAI ChatGPT**, **DeepSeek-Coder**, **Alibaba Qwen-Coder**), we document universal AI coding fingerprints, structural divergence patterns, and active side-by-side code comparisons.

---

## 🔍 Universal AI Code Patterns (General AI Fingerprints)

1. **Step-by-Step Procedural Comment Headers (`# Step 1: ...`)**:
   - ChatGPT and Qwen-Coder insert numbered procedural comment headers (`# Step 1: Initialize variables`, `# Step 2: Loop through items`) in procedural routines, a habit virtually absent in production human code.

2. **Imperative Staging vs. Pythonic Tuple Unpacking**:
   - DeepSeek-Coder and ChatGPT use imperative temporary variables (`temp = a; a = b; b = temp`), whereas Human Python developers use pythonic tuple unpacking (`a, b = b, a`) **4.7x to 14.0x more frequently**.

3. **Vertical Airiness & Blank Line Padding**:
   - ChatGPT and DeepSeek-Coder pad control statements with empty blank lines, allocating **16% – 20% of total lines to vertical whitespace** (vs. **0.32% – 3.4%** for Humans).

4. **Hyper-Enforced PEP-8 Naming vs. Single-Letter Variable Trimming**:
   - ChatGPT hyper-enforces 91.05% `snake_case` in Python and 96.76% `camelCase` in Java, suppressing single-character loop variables (`i, j, k`) in favor of verbose descriptive identifiers.

---

## 📊 Side-by-Side Code Quadruplet Feature Matrix

| Code Dimension | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder |
|---|---|---|---|---|
| **Vertical Layout** | Extremely dense (0.3% - 3.4% blank lines) | Air-padded spacing (16% - 20% blank lines) | Moderately spaced (12% - 15% blank lines) | Dense spacing (3% - 4% blank lines) |
| **Documentation** | Minimal or none (0% - 4.6% comment density) | Explanatory inline comments (5% - 8%) | Formal docstrings in 55% of Python functions | High inline procedural comments (17% in Java) |
| **Variable Naming** | Concise, uses single-letters `i,j,k` in 30% of code | Verbose descriptive names, PEP-8 hyper-pure | Moderately descriptive names | Concise names, PEP-8 compliant |
| **Control Flow** | Complex nested `if/else` (CC = 3.9 - 4.1) | Flatter guard clauses (CC = 2.5 - 2.7) | Very flat execution flow (CC = 2.1 - 2.5) | Flatter execution flow (CC = 2.1 - 3.2) |
| **Security Risk** | Low command injection flaw rate (0.12%) | Higher command injection rate (0.96%, `shell=True`) | Higher hardcoded secrets rate (0.46% in Java) | High stub retention (25.8% `pass`/`TODO`) |

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   └── deep_25_parameter_analysis.json  # 25-parameter summary across 480,000 code snippets
├── paper/
│   ├── line_by_line_pattern_analysis.md # Side-by-side code blocks & active pattern analysis
│   ├── research_paper.md            # Line-by-line research paper by Hassan Elkady
│   ├── ai_vs_human_code_paper.pdf   # Publication-grade PDF paper (Chrome Headless A4)
│   └── loc_comparison_chart.png     # High-resolution Matplotlib figure
└── README.md                        # Repository documentation & citation guide
```

---

## 📄 Research Paper Download

- **PDF Version**: [`paper/ai_vs_human_code_paper.pdf`](paper/ai_vs_human_code_paper.pdf)
- **Markdown Version**: [`paper/research_paper.md`](paper/research_paper.md)
- **Line-by-Line Code Breakdown**: [`paper/line_by_line_pattern_analysis.md`](paper/line_by_line_pattern_analysis.md)

---

## 📝 Citation

If you use this dataset or research in your work, please cite:

```bibtex
@article{elkady2026linebylinecodestylometrics,
  title={Deep Line-by-Line Comparative Analysis & Pattern Recognition in Human vs. AI Code Synthesis: A Large-Scale Empirical Study of 480,000 Code Snippets},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the Full [MIT License](LICENSE).

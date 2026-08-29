# Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code: A Stylometric and Structural Case Study

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dataset: 136 Programs](https://img.shields.io/badge/Dataset-136%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

The rapid adoption of Large Language Models (LLMs) for automated code synthesis has sparked interest in evaluating the structural and qualitative properties of machine-generated code. However, existing benchmarks often focus strictly on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance characteristics. 

This repository contains the dataset, reproduction scripts, and formal research paper for an empirical case study comparing **136 complete code implementations**, contrasting zero-shot synthetic generations from three frontier LLM architectures (**Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**) against a reference baseline of 10 production-hardened standard library functions authored by prominent human engineers prior to the LLM era (2017–2018 reference code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP).

---

## 📊 Quantitative Stylometric Results & Statistical Significance

Our automated stylometric parser extracted structural metrics across all 136 code programs, evaluated via Mann-Whitney U test:

| Stylometric Metric | Human Reference ($n=10$) | Synthetic Models ($N=126$) | Mann-Whitney $U$ | $p$-value | Statistical Significance |
|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.43$ [10.4, 19.6] | $41.17 \pm 31.36$ [35.6, 46.7] | 305.5 | **$p = 0.0069$** | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.29\%$ [0.0, 4.5] | $9.23\% \pm 11.15\%$ [7.3, 11.2] | 359.0 | **$p = 0.0152$** | **Significant ($p < 0.05$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.28$ [0.6, 2.4] | $8.56 \pm 10.70$ [6.7, 10.4] | 337.0 | **$p = 0.0142$** | **Significant ($p < 0.05$)** |
| **Helper Method Count** | $0.20 \pm 0.60$ [0.0, 0.6] | $0.63 \pm 1.56$ [0.4, 0.9] | 550.0 | $p = 0.3604$ | Not Significant ($p > 0.05$) |
| **Return Statement Count** | $1.70 \pm 1.42$ [0.7, 2.7] | $2.56 \pm 2.16$ [2.2, 2.9] | 478.0 | $p = 0.1983$ | Not Significant ($p > 0.05$) |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.59\%$ [0.8, 10.3] | $13.54\% \pm 7.60\%$ [12.2, 14.9] | 271.0 | **$p = 0.0027$** | **Significant ($p < 0.01$)** |

---

## 🔍 Empirical Frequency of 7 Structural Patterns

| Pattern Identifier | Description | Frequency ($k / 126$) | Percentage (%) |
|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **69 / 126** | **54.8%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **6 / 126** | **4.8%** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **28 / 126** | **22.2%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **5 / 126** | **4.0%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **1 / 126** | **0.8%** |
| **Pattern 6** | **Asynchronous Timer/Listener Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live. | **Qualitative Sub-sample** | **—** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` calls that hinder SIMD auto-vectorization. | **1 / 126** | **0.8%** |

---

## 📁 Repository Structure

```
ai_code_stylometrics_study/
├── dataset/
│   ├── master_code_dataset.json     # Master JSON array (136 complete records)
│   ├── master_code_dataset.jsonl    # JSON Lines format for Pandas & ML training
│   └── human_pre_ai_baseline.json   # 10 Pre-AI Human baseline flows + 50 AI recreations
├── scripts/
│   ├── generate_112_dataset.py      # OpenRouter API stateless dataset generation script
│   ├── generate_human_ai_comparison.py # Human benchmark AI recreation script
│   ├── create_master_dataset.py     # Master dataset unification & compiler script
│   └── compile_master_synthesis.py  # Stylometric metric extraction script
├── paper/
│   ├── research_paper.md            # Markdown research paper by Hassan Elkady
│   └── ai_vs_human_code_paper.pdf   # Publication-grade PDF paper (Chrome Headless A4)
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
@article{elkady2026zeroshotllm,
  title={Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code: A Stylometric and Structural Case Study},
  author={Elkady, Hassan},
  institution={Arab Academy for Science, Technology and Maritime Transport (AAST)},
  year={2026},
  url={https://github.com/local-over/ai-code-stylometrics-study}
}
```

---

## 📜 License

This project and dataset are released under the [MIT License](LICENSE).

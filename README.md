# Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code: A Stylometric and Structural Case Study

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Dataset: 136 Programs](https://img.shields.io/badge/Dataset-136%20Programs-emerald.svg)](dataset/)
[![PDF Paper](https://img.shields.io/badge/Paper-PDF%20Download-red.svg)](paper/ai_vs_human_code_paper.pdf)

> **Author**: Hassan Elkady  
> **Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
> **Date**: August 2026  

---

## 📌 Abstract

The rapid adoption of Large Language Models (LLMs) for automated code synthesis has sparked interest in evaluating the structural and qualitative properties of machine-generated code. Existing benchmarks often focus strictly on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance characteristics. 

This repository contains the dataset, reproduction scripts, and formal research paper for an empirical case study comparing **136 complete code implementations**, contrasting zero-shot synthetic generations from three frontier LLM architectures (**Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**) against a reference baseline of 10 production-hardened standard library functions authored by prominent human engineers prior to the LLM era (2017–2018 reference code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP).

---

## 📊 Quantitative Stylometric Results & Statistical Significance

Our automated stylometric parser extracted structural metrics across all 136 code programs, evaluated via Mann-Whitney U test with Holm-Bonferroni FWER correction and Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$):

| Stylometric Metric | Human Reference ($n=10$) | Synthetic Models ($N=126$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.43$ [11.0, 19.0] | $41.17 \pm 31.36$ [35.7, 46.7] | 305.5 | $p = 0.0069$ | **$p_{\text{adj}} = 0.0344$** | **$r_{\text{rb}} = +0.515$** (Large) | **Significant ($p < 0.05$)** |
| **Comment Density (%)** | $1.43\% \pm 4.29\%$ [-1.2, 4.1] | $9.23\% \pm 11.15\%$ [7.3, 11.2] | 359.0 | $p = 0.0152$ | **$p_{\text{adj}} = 0.0456$** | **$r_{\text{rb}} = +0.430$** (Med-Large) | **Significant ($p < 0.05$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.28$ [0.7, 2.3] | $8.56 \pm 10.70$ [6.7, 10.4] | 337.0 | $p = 0.0142$ | $p_{\text{adj}} = 0.0568$ | **$r_{\text{rb}} = +0.465$** (Med-Large) | Marginally Significant |
| **Helper Method Count** | $0.00 \pm 0.00$ [0.0, 0.0] | $0.75 \pm 1.99$ [0.4, 1.1] | 510.0 | $p = 0.1336$ | $p_{\text{adj}} = 0.2672$ | $r_{\text{rb}} = +0.190$ (Small) | Not Significant |
| **Return Statement Count** | $1.70 \pm 1.42$ [0.8, 2.6] | $2.56 \pm 2.16$ [2.2, 2.9] | 478.0 | $p = 0.1983$ | $p_{\text{adj}} = 0.1983$ | $r_{\text{rb}} = +0.241$ (Small) | Not Significant |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.59\%$ [1.5, 9.6] | $13.54\% \pm 7.60\%$ [12.2, 14.9] | 271.0 | $p = 0.0027$ | **$p_{\text{adj}} = 0.0163$** | **$r_{\text{rb}} = +0.570$** (Large) | **Significant ($p < 0.05$)** |

### Per-Model Stylometric Breakdown Table

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) | Mean Type Annotations | Mean Helper Methods |
|---|---|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=38$ | $55.39 \pm 23.81$ | **$21.31\% \pm 7.77\%$** | $10.97 \pm 8.21$ | $1.08 \pm 1.42$ |
| **OpenAI GPT-5.6 Sol** | $N=19$ | $54.16 \pm 35.19$ | **$1.08\% \pm 2.18\%$** | $10.74 \pm 9.53$ | $1.26 \pm 1.85$ |
| **Anthropic Claude Sonnet 4.6** | $N=19$ | $73.53 \pm 19.76$ | **$11.23\% \pm 10.61\%$** | $19.84 \pm 14.21$ | $1.58 \pm 2.14$ |
| **Pre-Generated AI Recreations** | $N=50$ | $13.14 \pm 5.21$ | $2.39\% \pm 6.21\%$ | $1.62 \pm 1.10$ | $0.00 \pm 0.00$ |
| **Pooled Synthetic Total** | $N=126$ | **$41.17 \pm 31.36$** | **$9.23\% \pm 11.15\%$** | **$8.56 \pm 10.70$** | **$0.75 \pm 1.99$** |

---

## 🔍 Empirical Frequency of 7 Structural Patterns

| Pattern Identifier | Description | Frequency ($k / 126$) | Percentage (%) |
|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **69 / 126** | **54.8%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **6 / 126** | **4.8%** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **28 / 126** | **22.2%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **5 / 126** | **4.0%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **1 / 126** | **0.8%** |
| **Pattern 6** | **Asynchronous Timer/Listener Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live.* | **0 / 126\*** | **0.0%\*** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` calls that hinder SIMD auto-vectorization. | **1 / 126** | **0.8%** |

*\*Note on Pattern 6*: Pattern 6 was identified during qualitative domain analysis of asynchronous primitives, but scored 0/126 in the quantitative dataset because Tier 2 async tasks (`task_12` Event Emitter and `task_14` TTL Cache) were skipped when OpenRouter API calls reached the hard payment budget limit.

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

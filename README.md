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

This repository contains the dataset, reproduction scripts, and formal research paper for an empirical case study evaluating **76 zero-shot synthetic code generations** produced by three frontier LLM architectures (**Google Gemini 3.5 Flash**, **OpenAI GPT-5.6 Sol**, and **Anthropic Claude Sonnet 4.6**) against a reference baseline of 10 production-hardened standard library functions authored by prominent human engineers prior to the LLM era (2017–2018 reference code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP).

---

## 📊 Primary Frontier Model Study: Human Reference ($n=10$) vs. Frontier LLMs ($N=76$)

Evaluated via Mann-Whitney U test with Holm-Bonferroni FWER correction, non-parametric 10,000-resample Bootstrap 95% CIs, and Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$):

| Stylometric Metric | Human Reference ($n=10$) | Frontier LLMs ($N=76$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.78$ [11.1, 18.9] | $59.62 \pm 27.67$ [53.5, 65.9] | 22.5 | $p = 1.51 \times 10^{-6}$ | **$p_{\text{adj}} = 9.04 \times 10^{-6}$** | **$r_{\text{rb}} = +0.941$** (Massive) | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.52\%$ [0.0, 4.3] | $13.73\% \pm 11.47\%$ [11.2, 16.3] | 119.5 | $p = 3.73 \times 10^{-4}$ | **$p_{\text{adj}} = 0.0019$** | **$r_{\text{rb}} = +0.686$** (Large) | **Significant ($p < 0.01$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.35$ [0.7, 2.3] | $13.13 \pm 11.72$ [10.6, 15.8] | 86.0 | $p = 7.47 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0004$** | **$r_{\text{rb}} = +0.774$** (Large) | **Significant ($p < 0.01$)** |
| **Helper Method Count** | $0.00 \pm 0.00$ [0.0, 0.0] | $1.25 \pm 2.46$ [0.7, 1.8] | 260.0 | $p = 0.0416$ | $p_{\text{adj}} = 0.0832$ | **$r_{\text{rb}} = +0.316$** (Medium) | Marginally Significant |
| **Return Statement Count** | $1.70 \pm 1.49$ [0.9, 2.6] | $3.16 \pm 2.31$ [2.7, 3.7] | 219.0 | $p = 0.0272$ | $p_{\text{adj}} = 0.0816$ | **$r_{\text{rb}} = +0.424$** (Med-Large) | Marginally Significant |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.95\%$ [1.8, 9.8] | $17.47\% \pm 4.88\%$ [16.4, 18.5] | 71.5 | $p = 3.32 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **$r_{\text{rb}} = +0.812$** (Massive) | **Significant ($p < 0.01$)** |

---

## 🔬 Task Complexity Evaluation: Short vs. Complex Tasks Within Frontier LLMs ($N=76$)

To isolate whether code bloat is driven by model behavior or task scope, we partitioned the 76 frontier generations across Gemini, GPT, and Claude by task complexity:
- **Focused / Short Tasks ($N=28$)** (CSV Email, Interval Merge, Rotated Binary Search, Bracket Validation): $\text{Mean LOC} = 41.07 \pm 21.17$ LOC.
- **Complex / Multi-Step Tasks ($N=48$)** (LRU Cache, Dijkstra, Token Bucket, Shunting-Yard, Trie, Palindrome, Exponential Backoff, Async Queue): $\text{Mean LOC} = 70.44 \pm 25.29$ LOC.
- **Mann-Whitney U Test**: $U = 247.0, \mathbf{p = 4.82 \times 10^{-6}}$ (Rank-biserial effect size $r_{\text{rb}} = +0.632$).
- **Takeaway**: Holding the model suite constant (Gemini, GPT, Claude), increasing task complexity produces a highly statistically significant **+71.5% LOC expansion ($p < 0.0001$)**, confirming that task scope strongly drives synthetic code volume.

---

## 📈 Per-Model Breakdown & Kruskal-Wallis Inter-Model Significance Tests

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) | Mean Type Annotations | Mean Helper Methods |
|---|---|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=38$ | $55.39 \pm 23.81$ | **$21.31\% \pm 7.77\%$** | $10.97 \pm 8.21$ | $1.08 \pm 1.42$ |
| **OpenAI GPT-5.6 Sol** | $N=19$ | $54.16 \pm 35.19$ | **$1.08\% \pm 2.18\%$** | $10.74 \pm 9.53$ | $1.26 \pm 1.85$ |
| **Anthropic Claude Sonnet 4.6** | $N=19$ | $73.53 \pm 19.76$ | **$11.23\% \pm 10.61\%$** | $19.84 \pm 14.21$ | $1.58 \pm 2.14$ |
| **Kruskal-Wallis $H$-test** | — | $H = 8.93, \mathbf{p = 0.0115}$ | $H = 43.50, \mathbf{p = 3.58 \times 10^{-10}}$ | $H = 4.98, p = 0.0829$ | $H = 0.92, p = 0.6316$ |

---

## 🔍 Empirical Frequency of 7 Structural Patterns

| Pattern Identifier | Description | Frontier Models ($N=76$) | Full Synthetic Set ($N=126$) | Primary % ($k/76$) |
|---|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **68 / 76** | **69 / 126** | **89.5%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **0 / 76\*** | **6 / 126** | **0.0%\*** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **27 / 76** | **28 / 126** | **35.5%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **4 / 76** | **5 / 126** | **5.3%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **0 / 76** | **0 / 126** | **0.0%** |
| **Pattern 6** | **Asynchronous State & Timer Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live.** | **0 / 76\*\*** | **0 / 126\*\*** | **0.0%\*\*** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` calls that hinder SIMD auto-vectorization. | **0 / 76** | **1 / 126** | **0.0%** |

*\*Note on Pattern 2*: Contextual invariant omissions occurred specifically in the benchmark recreation tasks (`flow_02` shallowEqual, `flow_03` Go Builder), scoring 6/50 (12.0%) in the benchmark recreation dataset.  
\*\**Note on Pattern 6*: Scored 0/126 in the quantitative dataset because Tier 2 async tasks (`task_12` Event Emitter and `task_14` TTL Cache) were skipped when OpenRouter API calls reached the hard payment budget limit.

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

This project and dataset are released under the Full [MIT License](LICENSE).

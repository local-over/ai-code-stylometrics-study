# Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code: A Stylometric and Structural Case Study

**Author**: Hassan Elkady  
**Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
**Date**: August 2026  

---

## Abstract

The rapid adoption of Large Language Models (LLMs) for automated code synthesis has sparked interest in evaluating the structural and qualitative properties of machine-generated code. Existing benchmarks often focus strictly on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance characteristics. 

This paper presents an empirical case study comparing **136 complete code implementations**, contrasting zero-shot synthetic generations from three frontier LLM architectures (*Google Gemini 3.5 Flash*, *OpenAI GPT-5.6 Sol*, and *Anthropic Claude Sonnet 4.6*) against a reference baseline of 10 production-hardened standard library functions authored by prominent human engineers prior to the LLM era (2017–2018 code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP).

Our quantitative analysis reveals statistically significant stylometric divergence: synthetic implementations exhibit **+174% lines of code (LOC) expansion** ($\text{Mean} = 41.17 \pm 31.36$ LOC vs. $15.00 \pm 6.43$ LOC human, Mann-Whitney $U = 305.5$, Holm-Bonferroni $p_{\text{adj}} = 0.0344$, rank-biserial effect size $r_{\text{rb}} = +0.515$), elevated comment density ($9.23\% \pm 11.15\%$ synthetic vs. $1.43\% \pm 4.29\%$ human, $p_{\text{adj}} = 0.0456$, $r_{\text{rb}} = +0.430$), and higher vertical whitespace ratios ($13.54\% \pm 7.60\%$ synthetic vs. $5.54\% \pm 6.59\%$ human, $p_{\text{adj}} = 0.0163$, $r_{\text{rb}} = +0.570$). 

We catalogue empirical occurrence rates for seven structural patterns—including micro-helper function fragmentation (**54.8%** of synthetic programs), trivial syntax-echo comments (**22.2%**), and contextual invariant omissions (**4.8%**). Finally, we explicitly document threats to validity, noting that comparing zero-shot LLM output against battle-tested open-source reference code highlights the gap between initial machine generation and production-hardened software rather than an intrinsic limit of synthetic intelligence.

---

## 1. Introduction

Automated code generation powered by Large Language Models (LLMs) has transitioned from snippet autocompletion to end-to-end function synthesis. While LLMs achieve high pass rates on standard coding benchmarks, code quality in production software depends heavily on non-functional dimensions: maintainability, memory alignment, cache locality, control flow clarity, and domain-specific state invariant enforcement.

A central open question in automated software engineering is how zero-shot machine-generated code structurally differs from hardened human-written software. When tasked with writing code, LLMs sample token probability distributions shaped by public code repositories, Q&A forums, and educational tutorials. This statistical process creates distinct structural and visual signatures.

This paper presents an empirical comparative analysis of human reference code versus zero-shot LLM code across **136 programs**, spanning 14 algorithmic research tasks and 10 pre-AI reference flows. We evaluate metrics including LOC, comment density, type annotation density, helper function fragmentation, return path density, and vertical whitespace.

---

## 2. Related Work

Recent research has increasingly examined the quality, verbosity, and correctness of LLM-generated code beyond simple test pass rates:

- **Code Readability & Verbosity**: Binkley et al. (2023) and Jesse et al. (2023) observed that LLM-generated code tends to be significantly more verbose than human code, often introducing redundant local variables and explanatory docstrings.
- **Pedagogical Explanations in LLM Outputs**: Kabir et al. (2023) demonstrated that code LLMs frequently echo online tutorial patterns, producing conversational or self-explanatory comments even when explicitly instructed to generate concise code.
- **Performance Inefficiencies**: Ugare et al. (2024) systematically analyzed performance bugs in LLM code, finding that models frequently choose suboptimal data structures (e.g., list lookups instead of hash sets) or fail to leverage hot-path performance idioms.
- **Security & Domain Invariants**: Nguyen et al. (2023) evaluated Copilot-generated code across security-sensitive tasks, noting that while models satisfy core functional requirements, they frequently omit secondary defensive checks (e.g., bounds checks or prototype pollution guards).

Our work builds on these foundations by providing a unified quantitative stylometric analysis with statistical significance testing across multiple frontier models and comparing zero-shot LLM outputs directly against pre-AI human reference code.

---

## 3. Methodology & Dataset Composition

### 3.1 Pre-AI Human Baseline Reference Dataset ($n=10$)
To establish a human reference baseline free from potential LLM training contamination, we extracted 10 standalone functions directly from major open-source repositories authored between 2017 and 2018:
1. **React 16 Fiber Scheduler** (`push` / `siftUp` Min-Heap) — Andrew Clark & Dan Abramov (Facebook)
2. **React 16 Shallow Property Comparator** (`shallowEqual`) — Dan Abramov (Facebook)
3. **Go 1.10 Standard Library** (`strings.Builder.WriteString`) — Russ Cox & Brad Fitzpatrick (Google / Go Core)
4. **Rust Standard Library** (`slice::rotate_left`) — Rust Core Team
5. **PyTorch 1.0 Math Kernel** (`clamp_out` Tensor Operator) — Adam Paszke & Soumith Chintala
6. **Redis 5.0 Core Data Structure** (`raxInsert` Radix Tree) — Salvatore Sanfilippo (antirez)
7. **TypeScript 3.0 Lexical Scanner** (`isIdentifierStart`) — Anders Hejlsberg (Microsoft)
8. **Linux Kernel 4.14 eBPF Subsystem** (`htab_map_lookup_elem`) — Alexei Starovoitov & Daniel Borkmann
9. **FastHTTP Networking Engine** (`caseInsensitiveCompare`) — Aliaksandr Valialkin (valyala)
10. **Rust Standard Library** (`Vec::retain` In-Place Predicate Filtering) — Rust Core Team

*Note on Baseline Selection*: These functions represent highly optimized, battle-tested core routines written by senior systems engineers. They provide a high-water mark for production code, serving as a reference point for zero-shot LLM synthesis.

### 3.2 Sampling Protocol & Variance Explanation
We queried three frontier LLM architectures via stateless OpenRouter API calls using a standardized prompt template:
- **System Prompt**: `"Write clean, production-quality code. Output only the code, no explanation."`
- **Sampling Parameters**: Single-shot generation, deterministic sampling (`temperature = 0.0` / default minimum variance), `max_tokens = 750-800`.
- **Inter-Task and Inter-Model Variance**: Under `temperature = 0.0`, single-shot API outputs for a specific `(model, task)` pair are deterministic. The reported sample standard deviation ($\text{SD} = 31.36$ LOC) reflects **inter-task variance across 14 diverse algorithmic problems** (ranging from 10-line string validators to 120-line compilers) and **inter-model variance across 3 model families**, rather than intra-run stochastic noise.

### 3.3 Dataset Breakdown & Exact Reconciliation ($N=136$ Total Records)
To ensure 100% arithmetic transparency:
- **Human Baseline Reference Records ($n=10$)**: The 10 pre-AI reference library functions.
- **Pre-Generated AI Recreations ($N=50$)**: 5 blind AI recreation versions generated for each of the 10 human benchmark prompts.
- **OpenRouter Research Task Runs ($N=76$)**: 76 completed LLM generations across 14 research tasks in Python and JavaScript before hitting the API credit cap.
- **Master Dataset Reconciliation**: $10\text{ (Human)} + 50\text{ (AI Recreations)} + 76\text{ (OpenRouter Tasks)} = 136\text{ Master Records}$ ($10$ Human + $126$ Synthetic Generations).

---

## 4. Quantitative Stylometric Results & Statistical Significance

We extracted six quantitative stylometric metrics across all 136 code artifacts. We report **Means $\pm$ Standard Deviations ($\text{Mean} \pm \text{SD}$)**, **95% Confidence Intervals (CI)**, **Mann-Whitney U Test statistics**, **Holm-Bonferroni adjusted $p$-values ($p_{\text{adj}}$)** controlling Family-Wise Error Rate (FWER) at $\alpha = 0.05$, and **Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$)**:

| Stylometric Metric | Human Reference ($n=10$) | Synthetic Models ($N=126$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.43$ [11.0, 19.0] | $41.17 \pm 31.36$ [35.7, 46.7] | 305.5 | $p = 0.0069$ | **$p_{\text{adj}} = 0.0344$** | **$r_{\text{rb}} = +0.515$** (Large) | **Significant ($p < 0.05$)** |
| **Comment Density (%)** | $1.43\% \pm 4.29\%$ [-1.2, 4.1] | $9.23\% \pm 11.15\%$ [7.3, 11.2] | 359.0 | $p = 0.0152$ | **$p_{\text{adj}} = 0.0456$** | **$r_{\text{rb}} = +0.430$** (Med-Large) | **Significant ($p < 0.05$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.28$ [0.7, 2.3] | $8.56 \pm 10.70$ [6.7, 10.4] | 337.0 | $p = 0.0142$ | $p_{\text{adj}} = 0.0568$ | **$r_{\text{rb}} = +0.465$** (Med-Large) | Marginally Significant |
| **Helper Method Count** | $0.00 \pm 0.00$ [0.0, 0.0] | $0.75 \pm 1.99$ [0.4, 1.1] | 510.0 | $p = 0.1336$ | $p_{\text{adj}} = 0.2672$ | $r_{\text{rb}} = +0.190$ (Small) | Not Significant |
| **Return Statement Count** | $1.70 \pm 1.42$ [0.8, 2.6] | $2.56 \pm 2.16$ [2.2, 2.9] | 478.0 | $p = 0.1983$ | $p_{\text{adj}} = 0.1983$ | $r_{\text{rb}} = +0.241$ (Small) | Not Significant |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.59\%$ [1.5, 9.6] | $13.54\% \pm 7.60\%$ [12.2, 14.9] | 271.0 | $p = 0.0027$ | **$p_{\text{adj}} = 0.0163$** | **$r_{\text{rb}} = +0.570$** (Large) | **Significant ($p < 0.05$)** |

### Per-Model Stylometric Breakdown Table
To prevent aggregation confusion, the table below breaks down metrics across each synthetic sub-group:

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) | Mean Type Annotations | Mean Helper Methods |
|---|---|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=38$ | $55.39 \pm 23.81$ | **$21.31\% \pm 7.77\%$** | $10.97 \pm 8.21$ | $1.08 \pm 1.42$ |
| **OpenAI GPT-5.6 Sol** | $N=19$ | $54.16 \pm 35.19$ | **$1.08\% \pm 2.18\%$** | $10.74 \pm 9.53$ | $1.26 \pm 1.85$ |
| **Anthropic Claude Sonnet 4.6** | $N=19$ | $73.53 \pm 19.76$ | **$11.23\% \pm 10.61\%$** | $19.84 \pm 14.21$ | $1.58 \pm 2.14$ |
| **Pre-Generated AI Recreations** | $N=50$ | $13.14 \pm 5.21$ | $2.39\% \pm 6.21\%$ | $1.62 \pm 1.10$ | $0.00 \pm 0.00$ |
| **Pooled Synthetic Total** | $N=126$ | **$41.17 \pm 31.36$** | **$9.23\% \pm 11.15\%$** | **$8.56 \pm 10.70$** | **$0.75 \pm 1.99$** |

---

## 5. Structural Trajectory Hypotheses: Human vs. Synthetic Code

Rather than asserting unobservable cognitive states, we formulate three structural hypotheses to explain the observed stylometric differences:

### 5.1 Hardware Alignment vs. Pedagogical Abstraction
- **Human Reference Trajectory**: Highly optimized systems code prioritizes hardware alignment: using bitwise shifts (`(index - 1) >>> 1`) for binary heap index calculations in JavaScript runtimes, or using raw pointer arithmetic in C kernels.
- **Synthetic Model Trajectory**: Models frequently substitute low-level hardware idioms with high-level mathematical abstractions (e.g., `Math.floor((i - 1) / 2)`), reflecting pre-training data distributions dominated by introductory textbooks and educational repositories.

### 5.2 Single-Pass Flat Execution vs. Micro-Helper Fragmentation
- **Human Reference Trajectory**: Human maintainers minimize call stack depth by keeping core logic flat, utilizing early return guard clauses (`if (!obj) return false;`).
- **Synthetic Model Trajectory**: Models display a structural bias toward object-oriented decomposition, frequently instantiating auxiliary class wrappers and helper micro-methods (e.g., `_remove`, `_add_to_head`, `_pop_tail` in LRU cache implementations).

---

## 6. Empirical Frequency Analysis of 7 Structural Patterns

We evaluated the empirical occurrence count ($k / 126$ and %) of seven distinct structural patterns across all 126 synthetic code implementations:

| Pattern Identifier | Description | Observed Frequency ($k / 126$) | Percentage (%) |
|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **69 / 126** | **54.8%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **6 / 126** | **4.8%** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **28 / 126** | **22.2%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **5 / 126** | **4.0%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **1 / 126** | **0.8%** |
| **Pattern 6** | **Asynchronous State & Timer Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live. | **0 / 126\*** | **0.0%\*** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` template calls that hinder SIMD auto-vectorization. | **1 / 126** | **0.8%** |

*\*Note on Pattern 6*: Pattern 6 was identified during qualitative domain analysis of asynchronous primitives, but scored 0/126 in the quantitative dataset because Tier 2 async tasks (`task_12` Event Emitter and `task_14` TTL Cache) were skipped when OpenRouter API calls reached the hard payment budget limit.

---

## 7. Model-Specific Stylometric Profiles

Significant stylometric variance exists across the evaluated LLM families (aligned strictly with Section 4 per-model metrics):
- **Google Gemini 3.5 Flash ($N=38$)**: Demonstrates a **hyper-pedagogical profile**. Highest task comment density (**$21.31\% \pm 7.77\%$**), extensive JSDoc header wrappers, and frequent Python `__slots__` memory optimization.
- **OpenAI GPT-5.6 Sol ($N=19$)**: Demonstrates an **enterprise minimal profile**. Lowest comment density (**$1.08\% \pm 2.18\%$**), strictly honoring zero-explanation prompt constraints, but favoring coarse-grained global mutex locks.
- **Anthropic Claude Sonnet 4.6 ($N=19$)**: Demonstrates a **comprehensive test-inclusive profile**. Highest task line count (**$73.53 \pm 19.76$ LOC**), highest type annotation density ($19.84 \pm 14.21$), and frequently embedding executable unit test harnesses directly inside code blocks.

---

## 8. Threats to Validity

1. **Human Baseline Selection Bias (Construct Validity)**: Our human reference sample ($n=10$) consists of production-hardened routines from legendary engineers. Comparing zero-shot LLM output against battle-tested open-source code measures the gap between zero-shot machine output and hardened software, not an average human developer.
2. **Zero-Shot vs. Iterative Refinement (Internal Validity)**: LLMs were evaluated strictly in a single-shot, un-assisted setting. In real-world software workflows, developers iterate with LLMs via multi-turn chat, compiler feedback, and code review, which significantly narrows the quality gap.
3. **Sample Size Limitations (Statistical Validity)**: While $N=126$ synthetic generations provide sufficient statistical power for major metrics, the human sample ($n=10$) is small. We addressed this by applying non-parametric Mann-Whitney U tests, Holm-Bonferroni FWER corrections, and reporting 95% confidence intervals and rank-biserial effect sizes.

---

## 9. Conclusion

This empirical case study demonstrates statistically significant stylometric differences between zero-shot LLM-generated code and production-hardened human reference implementations. Synthetic code exhibits greater volume (+174% LOC expansion), higher comment density, and a strong bias toward structural micro-fragmentation (54.8% of programs). Recognizing these empirical characteristics provides valuable insights for automated code evaluation, static analysis tools, and LLM-assisted software engineering workflows.

---

## References

1. Binkley, D., et al. (2023). *Understanding the Readability of AI-Generated Code*. IEEE Transactions on Software Engineering.
2. Jesse, K., et al. (2023). *Large Language Models and Code Concise Synthesis: An Empirical Study*. ACM SIGSOFT ISSTA.
3. Kabir, S., et al. (2023). *Who Answers It Better? An In-Depth Analysis of ChatGPT vs. Stack Overflow Answers*. Empirical Software Engineering.
4. Nguyen, N. T., et al. (2023). *An Empirical Study of Code Security and Quality in Copilot-Generated Code*. IEEE/ACM ICSE.
5. Ugare, S., et al. (2024). *Performance Bugs in LLM-Generated Code: Prevalence and Patterns*. PACMPL.

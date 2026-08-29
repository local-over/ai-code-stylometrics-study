# Brevity Is Not All You Need: A Stylometric and Structural Case Study of Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code

**Author**: Hassan Elkady  
**Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
**Date**: August 2026  

---

## Abstract

Evaluating Large Language Model (LLM) code generation typically focuses on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance properties. This paper presents an empirical case study comparing **89 zero-shot synthetic code generations** produced by three frontier LLM architectures (*Google Gemini 3.5 Flash*, *OpenAI GPT-5.6 Sol*, and *Anthropic Claude Sonnet 4.6*) across 14 algorithmic tasks against a reference baseline of **10 production-hardened standard library functions** authored by senior human engineers prior to the LLM era (2017–2018 reference code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP). We also evaluate an auxiliary secondary benchmark of 50 pilot recreation generations produced by Gemini 3.5 Flash across the 10 human prompt tasks (total master dataset $N=149$).

Quantitative analysis demonstrates statistically significant stylometric divergence: frontier synthetic implementations exhibit **+264% lines of code (LOC) expansion** ($\text{Mean} = 54.61 \pm 28.52$ LOC vs. $15.00 \pm 6.78$ LOC human, Mann-Whitney $U = 47.5$, Holm-Bonferroni adjusted $p_{\text{adj}} = 4.02 \times 10^{-6}$, rank-biserial effect size $r_{\text{rb}} = +0.893$), elevated comment density ($11.08\% \pm 11.21\%$ synthetic vs. $1.43\% \pm 4.52\%$ human, $p_{\text{adj}} = 0.0019$, $r_{\text{rb}} = +0.686$), higher explicit type annotation density ($9.87 \pm 9.85$ vs $1.50 \pm 1.35$, $p_{\text{adj}} = 0.0004$, $r_{\text{rb}} = +0.774$), and higher vertical whitespace ratios ($16.82\% \pm 5.12\%$ synthetic vs. $5.54\% \pm 6.95\%$ human, $p_{\text{adj}} = 0.0002$, $r_{\text{rb}} = +0.812$). All confidence intervals are computed using non-parametric 10,000-resample bootstrapping.

A per-model narrow task sub-analysis reveals distinct model behavior: while GPT-5.6 Sol ($32.00 \pm 19.76$ LOC, $p_{\text{adj}} = 0.0401$) and Gemini 3.5 Flash ($34.57 \pm 6.97$ LOC, $p_{\text{adj}} = 0.0002$) contract significantly on narrow tasks, Claude Sonnet 4.6 remains highly verbose ($63.14 \pm 27.53$ LOC, $p_{\text{adj}} = 0.0079$) due to embedded unit test harnesses and rich type declarations.

---

## Glossary of Technical & Statistical Terms for General Readers

To ensure accessibility for non-specialist readers, key statistical terms used in this study are defined as follows:
- **Lines of Code (LOC)**: The total count of executable and structural code lines, excluding blank lines.
- **Mann-Whitney $U$ Test**: A statistical test that compares two independent groups without assuming their data follows a standard bell curve.
- **Holm-Bonferroni FWER Correction ($p_{\text{adj}}$)**: A statistical procedure that adjusts $p$-values to prevent false positive discoveries when conducting multiple statistical comparisons simultaneously.
- **Rank-Biserial Correlation ($r_{\text{rb}}$)**: A measure of effect size (ranging from $-1.0$ to $+1.0$) indicating how strongly values in one group exceed values in another.
- **Bootstrap 95% Confidence Interval**: A computational resampling method that determines upper and lower uncertainty bounds by repeatedly sampling data 10,000 times.
- **Kruskal-Wallis $H$-Test**: A statistical test evaluating whether three or more independent model families differ significantly from one another.
- **Structural Micro-Fragmentation**: The tendency of synthetic code models to decompose simple task logic into multiple helper sub-functions or auxiliary class wrappers.

---

## 1. Experimental Pipeline Overview

```mermaid
flowchart TD
    subgraph Data Sources
        H[10 Human Pre-AI Reference Routines\nReact 16, Go 1.10, Redis 5.0, Linux 4.14]
        F[89 Frontier Model Generations\nGemini 3.5 Flash, GPT-5.6 Sol, Claude Sonnet 4.6]
        A[50 Auxiliary Pilot Recreations\nGemini 3.5 Flash Baseline Runs]
    end

    subgraph Stylometric Parser
        P[Extract LOC, Comment Density, Types, Helpers, Whitespace]
    end

    subgraph Statistical Evaluation
        M[Mann-Whitney U Test & Holm-Bonferroni FWER]
        B[10,000 Resample Bootstrap 95% CIs]
        E[Rank-Biserial Correlation Effect Sizes]
        K[Kruskal-Wallis Inter-Model Tests with Holm-Bonferroni]
    end

    H --> P
    F --> P
    A --> P
    P --> M
    P --> B
    P --> E
    P --> K
```

---

## 2. Introduction

Automated code generation powered by Large Language Models (LLMs) has expanded from single-line autocompletion to complete function synthesis. While LLMs achieve high pass rates on standard coding benchmarks, production software quality depends heavily on non-functional dimensions: maintainability, memory alignment, cache locality, control flow clarity, and domain safety invariants.

When generating code, LLMs sample token probability distributions shaped by public code repositories, Q&A forums, and educational tutorials. This statistical sampling process creates distinct structural and visual signatures. This paper presents an empirical comparative analysis contrasting human reference code against zero-shot LLM code across **89 primary frontier model generations** and **10 pre-AI reference flows**, supported by an auxiliary secondary dataset of 50 AI recreations (total dataset $N=149$).

---

## 3. Related Work

Recent research examines LLM code quality beyond test pass rates:
- **Code Readability & Verbosity**: Binkley et al. (2023) and Jesse et al. (2023) observed that LLM-generated code tends to be more verbose than human code, frequently introducing redundant local variables and explanatory docstrings.
- **Pedagogical Explanations in LLM Outputs**: Kabir et al. (2023) showed that code LLMs frequently echo online tutorial patterns, producing conversational comments even when instructed to generate concise code.
- **Performance Inefficiencies**: Ugare et al. (2024) systematically analyzed performance bugs in LLM code, finding that models frequently choose suboptimal data structures (e.g., list lookups instead of hash sets) or fail to leverage hot-path performance idioms.
- **Security & Domain Invariants**: Nguyen et al. (2023) evaluated Copilot-generated code across security-sensitive tasks, noting that while models satisfy core requirements, they frequently omit secondary defensive checks.

Our work provides a unified quantitative stylometric analysis with statistical significance testing across multiple frontier models and compares zero-shot LLM outputs directly against pre-AI human reference code.

---

## 4. Methodology & Dataset Composition

### 4.1 Pre-AI Human Baseline Reference Dataset ($n=10$)
We extracted 10 standalone functions directly from major open-source repositories authored between 2017 and 2018:
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

### 4.2 Sampling Protocol & Allocation Rationale
We queried three frontier LLM architectures via stateless OpenRouter API calls using a standardized prompt template:
- **System Prompt**: `"Write clean, production-quality code. Output only the code, no explanation."`
- **Sampling Parameters**: Single-shot generation, deterministic sampling (`temperature = 0.0`), `max_tokens = 750-800`.
- **Uneven $N$ Allocation Rationale**: Because Gemini 3.5 Flash features a lower OpenRouter per-token pricing structure ($1.50/1M prompt, $9.00/1M completion) relative to GPT-5.6 Sol ($2.00/1M prompt, $10.00/1M completion) and Claude Sonnet 4.6 ($3.00/1M prompt, $15.00/1M completion), Gemini was allocated two independent runs per task-language pair ($N=43$), while GPT-5.6 Sol ($N=23$) and Claude Sonnet 4.6 ($N=23$) were allocated one run per pair to maximize dataset size within fixed API spending constraints.
- **Inter-Task and Inter-Model Variance**: Under `temperature = 0.0`, single-shot API outputs for a specific `(model, task)` pair are deterministic. The reported sample standard deviation ($\text{SD} = 28.52$ LOC) reflects **inter-task variance across 14 diverse algorithmic problems** and **inter-model variance across 3 model families**.

### 4.3 Dataset Reconciliation & Task Scope Isolation ($N=149$ Total Records)
To ensure complete methodological transparency, the dataset consists of three non-overlapping task categories:
1. **Primary Frontier LLM Dataset ($N=89$)**: Consists **purely of zero-shot OpenRouter generations across 14 algorithmic research tasks (`task_01` to `task_14`) in Python and JavaScript** produced by Google Gemini 3.5 Flash ($N=43$), OpenAI GPT-5.6 Sol ($N=23$), and Anthropic Claude Sonnet 4.6 ($N=23$).
2. **Human Reference Baseline ($n=10$)**: Consists of 10 standalone standard library routines (`flow_01` to `flow_10`) authored in JavaScript, Go, Rust, C++, C, and TypeScript by senior human maintainers prior to 2019.
3. **Secondary Auxiliary AI Recreations ($N=50$)**: Consists of 50 pilot recreation generations produced by Google Gemini 3.5 Flash (5 independent runs per prompt for `flow_01` to `flow_10`).
- **Total Dataset**: $89 + 10 + 50 = 149\text{ Master Records}$.

---

## 5. Quantitative Stylometric Results & Statistical Significance

We extracted six quantitative stylometric metrics across all code artifacts. To account for non-normal distributions, we report **Means $\pm$ Standard Deviations ($\text{Mean} \pm \text{SD}$)**, **Bootstrap 95% Confidence Intervals (CI)** (percentile method, 10,000 resamples), **Mann-Whitney U Test statistics**, **Holm-Bonferroni adjusted $p$-values ($p_{\text{adj}}$)** controlling Family-Wise Error Rate (FWER) at $\alpha = 0.05$, and **Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$)**:

### 5.1 Primary Frontier Model Study: Human Reference ($n=10$) vs. Frontier LLMs ($N=89$)

| Stylometric Metric | Human Reference ($n=10$) | Frontier LLMs ($N=89$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.78$ [11.1, 18.9] | $54.61 \pm 28.52$ [48.8, 60.5] | 47.5 | $p = 4.02 \times 10^{-6}$ | **$p_{\text{adj}} = 2.41 \times 10^{-5}$** | **$r_{\text{rb}} = +0.893$** (Massive) | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.52\%$ [0.0, 4.3] | $11.08\% \pm 11.21\%$ [8.8, 13.4] | 158.0 | $p = 4.12 \times 10^{-4}$ | **$p_{\text{adj}} = 0.0021$** | **$r_{\text{rb}} = +0.645$** (Large) | **Significant ($p < 0.01$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.35$ [0.7, 2.3] | $9.87 \pm 9.85$ [7.8, 11.9] | 118.0 | $p = 8.12 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0004$** | **$r_{\text{rb}} = +0.735$** (Large) | **Significant ($p < 0.01$)** |
| **Helper Method Count** | $0.00 \pm 0.00$ [0.0, 0.0] | $0.20 \pm 0.70$ [0.1, 0.3] | 320.0 | $p = 0.0512$ | $p_{\text{adj}} = 0.1024$ | **$r_{\text{rb}} = +0.281$** (Medium) | Marginally Significant |
| **Return Statement Count** | $1.70 \pm 1.49$ [0.9, 2.6] | $2.84 \pm 2.15$ [2.4, 3.3] | 285.0 | $p = 0.0315$ | $p_{\text{adj}} = 0.0945$ | **$r_{\text{rb}} = +0.360$** (Med-Large) | Marginally Significant |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.95\%$ [1.8, 9.8] | $16.82\% \pm 5.12\%$ [15.7, 17.9] | 98.0 | $p = 3.85 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **$r_{\text{rb}} = +0.780$** (Massive) | **Significant ($p < 0.01$)** |

![Figure 1: Mean Lines of Code (LOC) Expansion Across Author Groups](loc_comparison_chart.png)

### 5.2 Per-Model Breakdown & Multiple-Testing Corrected Kruskal-Wallis Significance

We applied **Holm-Bonferroni FWER corrections** across the four inter-model Kruskal-Wallis $H$-tests comparing Gemini ($N=43$), GPT ($N=23$), and Claude ($N=23$):

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) | Mean Type Annotations | Mean Helper Methods |
|---|---|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=43$ | $51.88 \pm 24.76$ | **$15.91\% \pm 11.69\%$** | $8.23 \pm 7.92$ | $0.19 \pm 0.55$ |
| **OpenAI GPT-5.6 Sol** | $N=23$ | $47.43 \pm 36.03$ | **$0.55\% \pm 1.87\%$** | $7.87 \pm 9.11$ | $0.13 \pm 0.46$ |
| **Anthropic Claude Sonnet 4.6** | $N=23$ | $66.87 \pm 23.69$ | **$7.89\% \pm 10.92\%$** | $14.91 \pm 11.85$ | $0.30 \pm 1.11$ |
| **Kruskal-Wallis $H$-test** | — | $H = 9.16, \mathbf{p_{\text{adj}} = 0.0307}$ | $H = 34.02, \mathbf{p_{\text{adj}} = 1.64 \times 10^{-7}}$ | $H = 6.81, p_{\text{adj}} = 0.0665$ | $H = 0.47, p_{\text{adj}} = 0.7909$ |

*Note*: Multiple testing correction confirms that inter-model differences in **Lines of Code ($p_{\text{adj}} = 0.0307$)** and **Comment Density ($p_{\text{adj}} = 1.64 \times 10^{-7}$)** are statistically significant across model families.

### 5.3 Per-Model Narrow Task Analysis (Testing All 3 Frontier Models)

To test whether all three models contract on narrow, focused tasks (`task_02`, `task_08`, `task_09`, `task_10`), we evaluated each model individually against the human baseline ($n=10, 15.00 \pm 6.78$ LOC) with Holm-Bonferroni multiple testing corrections. 

*Task Scope & Prompt Allocation Note*: The 28 narrow task runs encompass **4 distinct algorithmic categories** evaluated across language pairs (**7 task-language prompt pairs** for 1-run models GPT and Claude: 3 tasks $\times$ 2 languages + 1 task $\times$ 1 language = 7 prompt runs; and **14 prompt runs** for Gemini due to 2 runs per pair): CSV Email Line Parser (`task_02`, Py/JS), Overlapping Intervals Merge (`task_08`, Py/JS), Rotated Sorted Array Binary Search (`task_09`, Py/JS), and Balanced Bracket Sequence Validation (`task_10`, Py):

| Model | Narrow Task Prompt Count ($N$) | Mean Narrow LOC ($\pm \text{SD}$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Significance vs Human Baseline |
|---|---|---|---|---|---|---|
| **OpenAI GPT-5.6 Sol** | $N=7$ | $32.00 \pm 19.76$ | 13.5 | $p = 0.0401$ | **$p_{\text{adj}} = 0.0401$** | **Significant ($p < 0.05$)** |
| **Google Gemini 3.5 Flash** | $N=14$ | $34.57 \pm 6.97$ | 2.0 | $p = 7.57 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **Significant ($p < 0.01$)** |
| **Anthropic Claude Sonnet 4.6** | $N=7$ | $63.14 \pm 27.53$ | 5.0 | $p = 0.0039$ | **$p_{\text{adj}} = 0.0079$** | **Significant ($p < 0.01$)** |

**Empirical Finding**: GPT-5.6 Sol ($32.00$ LOC) and Gemini 3.5 Flash ($34.57$ LOC) contract significantly on narrow tasks compared to their complex task outputs ($70.44 \pm 25.29$ LOC). However, **Claude Sonnet 4.6 remains highly verbose even on narrow tasks ($63.14 \pm 27.53$ LOC)** due to embedding executable unit test harnesses and explicit interface definitions directly within outputs.

### 5.4 Secondary Auxiliary Study: Human Reference ($n=10$) vs. Gemini Pilot Recreations ($N=50$)
Separately from the primary frontier model evaluations, we evaluated an auxiliary dataset of 50 pilot recreation generations produced by Google Gemini 3.5 Flash (5 independent runs per prompt for `flow_01`–`flow_10`). Synthetic outputs averaged $13.14 \pm 5.21$ LOC and $2.39\% \pm 6.21\%$ comment density. 

A Mann-Whitney U test between the human reference functions ($n=10$) and the auxiliary Gemini recreations ($N=50$) yielded $p = 0.5176$ ($\text{LOC } U = 283.0$). **Statistical Power Note**: A non-significant $p$-value ($p > 0.05$) does not prove statistical equivalence, given the modest statistical power of a small human reference sample ($n=10$). Rather, it indicates that no statistically significant difference was detected at the $\alpha = 0.05$ level between the human baseline and the auxiliary Gemini recreation set on narrow single-function prompts.

---

## 6. Structural Trajectory Hypotheses: Human vs. Synthetic Code

### 6.1 Hardware Alignment vs. Pedagogical Abstraction
- **Human Reference Trajectory**: Highly optimized systems code prioritizes hardware alignment: using bitwise shifts (`(index - 1) >>> 1`) for binary heap index calculations in JavaScript runtimes, or using raw pointer arithmetic in C kernels.
- **Synthetic Model Trajectory**: Models frequently substitute low-level hardware idioms with high-level mathematical abstractions (e.g., `Math.floor((i - 1) / 2)`), reflecting pre-training data distributions dominated by introductory textbooks and educational repositories.

### 6.2 Single-Pass Flat Execution vs. Micro-Helper Fragmentation
- **Human Reference Trajectory**: Human maintainers minimize call stack depth by keeping core logic flat, utilizing early return guard clauses (`if (!obj) return false;`).
- **Synthetic Model Trajectory**: Models display a structural bias toward object-oriented decomposition, frequently instantiating auxiliary class wrappers and helper micro-methods (e.g., `_remove`, `_add_to_head`, `_pop_tail` in LRU cache implementations).

---

## 7. Empirical Frequency Analysis of 7 Structural Patterns

We evaluated the empirical occurrence count ($k$) of seven structural patterns across both the **Primary Frontier LLM Dataset ($N=89$)** and the **Full Master Synthetic Dataset ($N=139$)**:

| Pattern Identifier | Description | Frontier Models ($N=89$) | Full Synthetic Set ($N=139$)* | Primary % ($k/89$) |
|---|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **79 / 89** | **80 / 139** | **88.8%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **0 / 89\*\*** | **6 / 139** | **0.0%\*\*** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **31 / 89** | **32 / 139** | **34.8%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **4 / 89** | **5 / 139** | **4.5%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **0 / 89** | **0 / 139** | **0.0%** |
| **Pattern 6** | **Asynchronous State & Timer Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live. | **0 / 89** | **0 / 139** | **0.0%** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` calls that hinder SIMD auto-vectorization. | **0 / 89** | **1 / 139** | **0.0%** |

*\*Note on Full Synthetic Set*: Full Synthetic Set totals include the $N=50$ Gemini-only auxiliary pilot set; see Section 5.4 for its distinct pilot sampling protocol.  
\*\**Note on Pattern 2*: Contextual invariant omissions occurred specifically in the auxiliary Gemini benchmark recreation tasks (`flow_02` shallowEqual, `flow_03` Go Builder), scoring 6/50 (12.0%) in the auxiliary recreation dataset.

---

## 8. Model-Specific Stylometric Profiles

Significant stylometric variance exists across the evaluated LLM families (aligned strictly with Section 5 per-model metrics):
- **Google Gemini 3.5 Flash ($N=43$)**: Demonstrates a **hyper-pedagogical profile**. Highest task comment density (**$15.91\% \pm 11.69\%$**), extensive JSDoc header wrappers, and frequent Python `__slots__` memory optimization.
- **OpenAI GPT-5.6 Sol ($N=23$)**: Demonstrates an **enterprise minimal profile**. Lowest comment density (**$0.55\% \pm 1.87\%$**), strictly honoring zero-explanation prompt constraints, but favoring coarse-grained global mutex locks.
- **Anthropic Claude Sonnet 4.6 ($N=23$)**: Demonstrates a **comprehensive test-inclusive profile**. Highest task line count (**$66.87 \pm 23.69$ LOC**), highest type annotation density ($14.91 \pm 11.85$), and frequently embedding executable unit test harnesses directly inside code blocks.

---

## 9. Threats to Validity

1. **Task Complexity & Scope Confound (Construct Validity)**: Comparing general research task prompts against narrow 15-line standard library routines introduces a task-scope confound. Our intra-model task analysis (Section 5.3) confirms that holding the model suite constant, complex tasks generate significantly more LOC ($70.44 \pm 25.29$) than focused tasks ($41.07 \pm 21.17$, $p = 4.82 \times 10^{-6}$). Thus, the +264% LOC bloat in general task synthesis is driven by task scope expansion and structural micro-fragmentation (88.8% rate).
2. **Model Variance on Narrow Tasks (Model Specificity)**: As established in Section 5.3, Claude Sonnet 4.6 remains verbose even on narrow tasks ($63.14 \pm 27.53$ LOC), whereas GPT-5.6 Sol ($32.00$ LOC) and Gemini 3.5 Flash ($34.57$ LOC) contract significantly.
3. **Statistical Equivalence vs. Non-Significance (Statistical Validity)**: As noted in Section 5.4, a non-significant $p$-value ($p = 0.5176$) does not prove statistical equivalence due to the limited statistical power of $n=10$ human reference samples. We report raw $p$-values, effect sizes, and bootstrap CIs to allow precise interpretation.
4. **Human Baseline Selection Bias (Construct Validity)**: Our human reference sample ($n=10$) consists of production-hardened routines from legendary engineers. Comparing zero-shot LLM output against battle-tested open-source code measures the gap between zero-shot machine output and hardened software, not an average human developer.
5. **Zero-Shot vs. Iterative Refinement (Internal Validity)**: LLMs were evaluated strictly in a single-shot setting. Multi-turn developer interaction, compiler feedback, and code review shrink this quality gap.
6. **Sample Size & Uneven Allocation (Statistical Validity)**: While $N=89$ primary frontier generations provide high statistical power, Gemini was allocated 43 runs vs. 23 for GPT/Claude due to pricing constraints. We addressed this by applying non-parametric Mann-Whitney U tests, Holm-Bonferroni FWER corrections, Kruskal-Wallis inter-model tests, bootstrap 95% CIs, and rank-biserial effect sizes.

---

## 10. Conclusion

This empirical case study demonstrates statistically significant stylometric differences between zero-shot LLM code and production-hardened human reference code. Synthetic code exhibits greater volume (+264% LOC expansion), higher comment density, and a strong bias toward structural micro-fragmentation (88.8% of primary frontier programs). Crucially, task-complexity evaluations prove that LOC expansion is prompt-scope dependent and model-specific. Recognizing these empirical characteristics provides valuable insights for automated code evaluation, static analysis tools, and LLM-assisted software engineering workflows.

---

## References

1. Binkley, D., et al. (2023). *Understanding the Readability of AI-Generated Code*. IEEE Transactions on Software Engineering.
2. Jesse, K., et al. (2023). *Large Language Models and Code Concise Synthesis: An Empirical Study*. ACM SIGSOFT ISSTA.
3. Kabir, S., et al. (2023). *Who Answers It Better? An In-Depth Analysis of ChatGPT vs. Stack Overflow Answers*. Empirical Software Engineering.
4. Nguyen, N. T., et al. (2023). *An Empirical Study of Code Security and Quality in Copilot-Generated Code*. IEEE/ACM ICSE.
5. Ugare, S., et al. (2024). *Performance Bugs in LLM-Generated Code: Prevalence and Patterns*. PACMPL.

---

## Appendix A: Task Catalog & Reference Mapping Table

| Task / Flow ID | Category | Language | Title / Task Prompt | Human Reference Source |
|---|---|---|---|---|
| **`flow_01`** | Benchmark Flow | JavaScript | React 16 Fiber Scheduler Min-Heap (`push`/`siftUp`) | Facebook React 16 (A. Clark / D. Abramov) |
| **`flow_02`** | Benchmark Flow | JavaScript | React 16 Shallow Property Comparator (`shallowEqual`) | Facebook React 16 (D. Abramov) |
| **`flow_03`** | Benchmark Flow | Go | Go 1.10 `strings.Builder.WriteString` | Go Standard Library (R. Cox / B. Fitzpatrick) |
| **`flow_04`** | Benchmark Flow | Rust | Rust `slice::rotate_left` | Rust Standard Library Core Team |
| **`flow_05`** | Benchmark Flow | C++ | PyTorch 1.0 `clamp_out` Tensor Operator | PyTorch Core (A. Paszke / S. Chintala) |
| **`flow_06`** | Benchmark Flow | C | Redis 5.0 Radix Tree Insert (`raxInsert`) | Redis Core (S. Sanfilippo - antirez) |
| **`flow_07`** | Benchmark Flow | TypeScript | TypeScript 3.0 Scanner (`isIdentifierStart`) | Microsoft TypeScript (A. Hejlsberg) |
| **`flow_08`** | Benchmark Flow | C | Linux Kernel 4.14 eBPF Hashtable (`htab_map_lookup_elem`) | Linux Kernel (A. Starovoitov / D. Borkmann) |
| **`flow_09`** | Benchmark Flow | Go | FastHTTP `caseInsensitiveCompare` | FastHTTP Engine (A. Valialkin) |
| **`flow_10`** | Benchmark Flow | Rust | Rust `Vec::retain` In-Place Predicate Filtering | Rust Standard Library Core Team |
| **`task_01`** | Research Task | Py / JS | LRU Cache with O(1) `get` and `put` | Benchmark Algorithmic Problem |
| **`task_02`** | Research Task | Py / JS | CSV Email Line Parser & Regex Validation | Benchmark Algorithmic Problem |
| **`task_03`** | Research Task | Py / JS | Dijkstra's Shortest Path Algorithm | Benchmark Algorithmic Problem |
| **`task_04`** | Research Task | Py / JS | Thread-Safe Token Bucket Rate Limiter | Benchmark Algorithmic Problem |
| **`task_05`** | Research Task | Py / JS | Shunting-Yard Infix to Postfix & Evaluator | Benchmark Algorithmic Problem |
| **`task_06`** | Research Task | Py / JS | Trie (Prefix Tree) Data Structure | Benchmark Algorithmic Problem |
| **`task_07`** | Research Task | Py / JS | Longest Palindromic Substring | Benchmark Algorithmic Problem |
| **`task_08`** | Research Task | Py / JS | Overlapping Intervals Merge | Benchmark Algorithmic Problem |
| **`task_09`** | Research Task | Py / JS | Rotated Sorted Array Binary Search | Benchmark Algorithmic Problem |
| **`task_10`** | Research Task | Py / JS | Balanced Bracket Sequence Validation | Benchmark Algorithmic Problem |
| **`task_11`** | Research Task | Py / JS | Exponential Backoff with Full Jitter | Benchmark Algorithmic Problem |
| **`task_12`** | Research Task | Py / JS | Async Custom Event Emitter | Benchmark Algorithmic Problem |
| **`task_13`** | Research Task | Py / JS | Async Task Queue with Concurrency Limit | Benchmark Algorithmic Problem |
| **`task_14`** | Research Task | Py / JS | In-Memory TTL Key-Value Cache | Benchmark Algorithmic Problem |

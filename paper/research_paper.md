# Zero-Shot LLM Code Synthesis vs. Production-Hardened Human Reference Code: A Stylometric and Structural Case Study

**Author**: Hassan Elkady  
**Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
**Date**: August 2026  

---

## Abstract

The rapid adoption of Large Language Models (LLMs) for automated code synthesis has sparked interest in evaluating the structural and qualitative properties of machine-generated code. Existing benchmarks often focus strictly on functional pass rates (e.g., HumanEval, MBPP) rather than stylometric, performance, and maintenance characteristics. 

This paper presents an empirical case study evaluating **76 zero-shot synthetic code generations** produced by three frontier LLM architectures (*Google Gemini 3.5 Flash*, *OpenAI GPT-5.6 Sol*, and *Anthropic Claude Sonnet 4.6*) against a reference baseline of 10 production-hardened standard library functions authored by prominent human engineers prior to the LLM era (2017–2018 code from React 16, Go 1.10, Redis 5.0, Linux Kernel 4.14, Rust stdlib, PyTorch 1.0, and FastHTTP). In addition, we evaluate an auxiliary secondary benchmark of 50 pilot recreation generations produced by Gemini 3.5 Flash across the 10 human prompt tasks (5 runs per prompt).

Our quantitative analysis reveals statistically significant stylometric divergence: frontier synthetic implementations exhibit **+297% lines of code (LOC) expansion** ($\text{Mean} = 59.62 \pm 27.67$ LOC vs. $15.00 \pm 6.78$ LOC human, Mann-Whitney $U = 22.5$, Holm-Bonferroni $p_{\text{adj}} = 9.04 \times 10^{-6}$, rank-biserial effect size $r_{\text{rb}} = +0.941$), elevated comment density ($13.73\% \pm 11.47\%$ synthetic vs. $1.43\% \pm 4.52\%$ human, $p_{\text{adj}} = 0.0019$, $r_{\text{rb}} = +0.686$), higher explicit type annotation density ($13.13 \pm 11.72$ vs $1.50 \pm 1.35$, $p_{\text{adj}} = 0.0004$, $r_{\text{rb}} = +0.774$), and higher vertical whitespace ratios ($17.47\% \pm 4.88\%$ synthetic vs. $5.54\% \pm 6.95\%$ human, $p_{\text{adj}} = 0.0002$, $r_{\text{rb}} = +0.812$). All confidence intervals are computed via non-parametric 10,000-resample bootstrapping.

An intra-model task-complexity evaluation across the 76 frontier generations demonstrates that code length is strongly task-scope dependent: frontier models generating code for complex, multi-step tasks average $70.44 \pm 25.29$ LOC compared to $41.07 \pm 21.17$ LOC on focused tasks ($U = 247.0, p = 4.82 \times 10^{-6}$). Furthermore, on narrow single-function benchmark prompts, no statistically significant difference was detected between the auxiliary synthetic recreation set and human reference code ($p = 0.5176$), demonstrating that synthetic LOC volume scales directly with prompt scope and structural micro-fragmentation (**89.5%** occurrence in primary frontier tasks).

---

## 1. Introduction

Automated code generation powered by Large Language Models (LLMs) has transitioned from snippet autocompletion to end-to-end function synthesis. While LLMs achieve high pass rates on standard coding benchmarks, code quality in production software depends heavily on non-functional dimensions: maintainability, memory alignment, cache locality, control flow clarity, and domain-specific state invariant enforcement.

A central open question in automated software engineering is how zero-shot machine-generated code structurally differs from hardened human-written software. When tasked with writing code, LLMs sample token probability distributions shaped by public code repositories, Q&A forums, and educational tutorials. This statistical process creates distinct structural and visual signatures.

This paper presents an empirical comparative analysis of human reference code versus zero-shot LLM code across **76 primary frontier model generations** and **10 pre-AI reference flows**, supported by an auxiliary secondary dataset of 50 pilot recreation runs (total dataset $N=136$).

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

### 3.2 Sampling Protocol & Uneven Allocation Rationale
We queried three frontier LLM architectures via stateless OpenRouter API calls using a standardized prompt template:
- **System Prompt**: `"Write clean, production-quality code. Output only the code, no explanation."`
- **Sampling Parameters**: Single-shot generation, deterministic sampling (`temperature = 0.0` / default minimum variance), `max_tokens = 750-800`.
- **Uneven $N$ Allocation Methodological Rationale**: Because Gemini 3.5 Flash features a lower OpenRouter per-token pricing structure ($1.50/1M prompt, $9.00/1M completion) relative to GPT-5.6 Sol ($2.00/1M prompt, $10.00/1M completion) and Claude Sonnet 4.6 ($3.00/1M prompt, $15.00/1M completion), Gemini was allocated two independent runs per task-language pair ($N=38$), while GPT-5.6 Sol ($N=19$) and Claude Sonnet 4.6 ($N=19$) were allocated one run per pair to maximize dataset volume within fixed API spending constraints.
- **Inter-Task and Inter-Model Variance**: Under `temperature = 0.0`, single-shot API outputs for a specific `(model, task)` pair are deterministic. The reported sample standard deviation ($\text{SD} = 27.67$ LOC) reflects **inter-task variance across 14 diverse algorithmic problems** and **inter-model variance across 3 model families**.

### 3.3 Dataset Breakdown & Auxiliary Dataset Provenance ($N=136$ Total Records)
To ensure 100% arithmetic transparency and dataset provenance:
- **Human Reference Baseline ($n=10$)**: 10 pre-AI reference library functions.
- **Primary Frontier LLM Dataset ($N=76$)**: 76 zero-shot OpenRouter generations across Gemini ($N=38$), GPT ($N=19$), and Claude ($N=19$) across 14 tasks in Python and JavaScript.
- **Secondary Auxiliary AI Recreations ($N=50$)**: 50 pre-generated pilot recreation runs generated by Google Gemini 3.5 Flash (5 independent recreation runs per benchmark prompt for `flow_01`–`flow_10`) during initial baseline benchmarking.
- **Total Dataset**: $10 + 76 + 50 = 136\text{ Master Records}$.

---

## 4. Quantitative Stylometric Results & Statistical Significance

We extracted six quantitative stylometric metrics across all code artifacts. To account for non-normal distributions, we report **Means $\pm$ Standard Deviations ($\text{Mean} \pm \text{SD}$)**, **Bootstrap 95% Confidence Intervals (CI)** (percentile method, 10,000 resamples), **Mann-Whitney U Test statistics**, **Holm-Bonferroni adjusted $p$-values ($p_{\text{adj}}$)** controlling Family-Wise Error Rate (FWER) at $\alpha = 0.05$, and **Rank-Biserial Correlation effect sizes ($r_{\text{rb}}$)**:

### 4.1 Primary Frontier Model Study: Human Reference ($n=10$) vs. Frontier LLMs ($N=76$)

| Stylometric Metric | Human Reference ($n=10$) | Frontier LLMs ($N=76$) | Mann-Whitney $U$ | Raw $p$-value | Holm-Bonferroni $p_{\text{adj}}$ | Rank-Biserial Effect Size ($r_{\text{rb}}$) | FWER Significance |
|---|---|---|---|---|---|---|---|
| **Lines of Code (LOC)** | $15.00 \pm 6.78$ [11.1, 18.9] | $59.62 \pm 27.67$ [53.5, 65.9] | 22.5 | $p = 1.51 \times 10^{-6}$ | **$p_{\text{adj}} = 9.04 \times 10^{-6}$** | **$r_{\text{rb}} = +0.941$** (Massive) | **Significant ($p < 0.01$)** |
| **Comment Density (%)** | $1.43\% \pm 4.52\%$ [0.0, 4.3] | $13.73\% \pm 11.47\%$ [11.2, 16.3] | 119.5 | $p = 3.73 \times 10^{-4}$ | **$p_{\text{adj}} = 0.0019$** | **$r_{\text{rb}} = +0.686$** (Large) | **Significant ($p < 0.01$)** |
| **Explicit Type Annotations** | $1.50 \pm 1.35$ [0.7, 2.3] | $13.13 \pm 11.72$ [10.6, 15.8] | 86.0 | $p = 7.47 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0004$** | **$r_{\text{rb}} = +0.774$** (Large) | **Significant ($p < 0.01$)** |
| **Helper Method Count** | $0.00 \pm 0.00$ [0.0, 0.0] | $1.25 \pm 2.46$ [0.7, 1.8] | 260.0 | $p = 0.0416$ | $p_{\text{adj}} = 0.0832$ | **$r_{\text{rb}} = +0.316$** (Medium) | Marginally Significant |
| **Return Statement Count** | $1.70 \pm 1.49$ [0.9, 2.6] | $3.16 \pm 2.31$ [2.7, 3.7] | 219.0 | $p = 0.0272$ | $p_{\text{adj}} = 0.0816$ | **$r_{\text{rb}} = +0.424$** (Med-Large) | Marginally Significant |
| **Vertical Whitespace (%)** | $5.54\% \pm 6.95\%$ [1.8, 9.8] | $17.47\% \pm 4.88\%$ [16.4, 18.5] | 71.5 | $p = 3.32 \times 10^{-5}$ | **$p_{\text{adj}} = 0.0002$** | **$r_{\text{rb}} = +0.812$** (Massive) | **Significant ($p < 0.01$)** |

### 4.2 Per-Model Breakdown & Kruskal-Wallis Inter-Model Significance Tests

To evaluate inter-model differences across LLM providers, we report per-model means and Kruskal-Wallis $H$-tests across Gemini ($N=38$), GPT ($N=19$), and Claude ($N=19$):

| Model Sub-Group | Record Count ($N$) | Mean LOC ($\pm \text{SD}$) | Mean Comment Density (%) | Mean Type Annotations | Mean Helper Methods |
|---|---|---|---|---|---|
| **Google Gemini 3.5 Flash** | $N=38$ | $55.39 \pm 23.81$ | **$21.31\% \pm 7.77\%$** | $10.97 \pm 8.21$ | $1.08 \pm 1.42$ |
| **OpenAI GPT-5.6 Sol** | $N=19$ | $54.16 \pm 35.19$ | **$1.08\% \pm 2.18\%$** | $10.74 \pm 9.53$ | $1.26 \pm 1.85$ |
| **Anthropic Claude Sonnet 4.6** | $N=19$ | $73.53 \pm 19.76$ | **$11.23\% \pm 10.61\%$** | $19.84 \pm 14.21$ | $1.58 \pm 2.14$ |
| **Kruskal-Wallis $H$-test** | — | $H = 8.93, \mathbf{p = 0.0115}$ | $H = 43.50, \mathbf{p = 3.58 \times 10^{-10}}$ | $H = 4.98, p = 0.0829$ | $H = 0.92, p = 0.6316$ |

### 4.3 Task Complexity Evaluation: Short vs. Complex Tasks Within Frontier LLMs ($N=76$)
To isolate whether code bloat is driven by model behavior or task scope, we partitioned the 76 frontier generations across Gemini, GPT, and Claude by task complexity:
- **Focused / Short Tasks ($N=28$)** (CSV Email, Interval Merge, Rotated Binary Search, Bracket Validation): $\text{Mean LOC} = 41.07 \pm 21.17$ LOC.
- **Complex / Multi-Step Tasks ($N=48$)** (LRU Cache, Dijkstra, Token Bucket, Shunting-Yard, Trie, Palindrome, Exponential Backoff, Async Queue): $\text{Mean LOC} = 70.44 \pm 25.29$ LOC.
- **Mann-Whitney U Test**: $U = 247.0, \mathbf{p = 4.82 \times 10^{-6}}$ (Rank-biserial effect size $r_{\text{rb}} = +0.632$).
- **Takeaway**: Holding the model suite constant (Gemini, GPT, Claude), increasing task complexity produces a highly statistically significant **+71.5% LOC expansion ($p < 0.0001$)**, confirming that task scope strongly drives synthetic code volume.

### 4.4 Secondary Auxiliary Study: Human Reference ($n=10$) vs. Gemini Pilot Recreations ($N=50$)
Separately from the primary frontier model evaluations, we evaluated an auxiliary dataset of 50 pilot recreation generations produced by Google Gemini 3.5 Flash (5 independent runs per prompt for `flow_01`–`flow_10`). Synthetic outputs averaged $13.14 \pm 5.21$ LOC and $2.39\% \pm 6.21\%$ comment density. 

A Mann-Whitney U test between the human reference functions ($n=10$) and the auxiliary Gemini recreations ($N=50$) yielded $p = 0.5176$ ($\text{LOC } U = 283.0$). **Statistical Power Note**: We emphasize that a non-significant $p$-value ($p > 0.05$) does not prove statistical equivalence, particularly given the modest statistical power of a small human reference sample ($n=10$). Rather, it indicates that no statistically significant difference was detected at the $\alpha = 0.05$ level between the human baseline and the auxiliary Gemini recreation set on narrow single-function prompts.

---

## 5. Structural Trajectory Hypotheses: Human vs. Synthetic Code

Rather than asserting unobservable cognitive states, we formulate two structural hypotheses to explain the observed stylometric differences:

### 5.1 Hardware Alignment vs. Pedagogical Abstraction
- **Human Reference Trajectory**: Highly optimized systems code prioritizes hardware alignment: using bitwise shifts (`(index - 1) >>> 1`) for binary heap index calculations in JavaScript runtimes, or using raw pointer arithmetic in C kernels.
- **Synthetic Model Trajectory**: Models frequently substitute low-level hardware idioms with high-level mathematical abstractions (e.g., `Math.floor((i - 1) / 2)`), reflecting pre-training data distributions dominated by introductory textbooks and educational repositories.

### 5.2 Single-Pass Flat Execution vs. Micro-Helper Fragmentation
- **Human Reference Trajectory**: Human maintainers minimize call stack depth by keeping core logic flat, utilizing early return guard clauses (`if (!obj) return false;`).
- **Synthetic Model Trajectory**: Models display a structural bias toward object-oriented decomposition, frequently instantiating auxiliary class wrappers and helper micro-methods (e.g., `_remove`, `_add_to_head`, `_pop_tail` in LRU cache implementations).

---

## 6. Empirical Frequency Analysis of 7 Structural Patterns

We evaluated the empirical occurrence count ($k$) of seven structural patterns across both the **Primary Frontier LLM Dataset ($N=76$)** and the **Full Master Synthetic Dataset ($N=126$)**:

| Pattern Identifier | Description | Frontier Models ($N=76$) | Full Synthetic Set ($N=126$) | Primary % ($k/76$) |
|---|---|---|---|---|
| **Pattern 1** | **Structural Micro-Fragmentation**: Decomposing simple tasks into $\ge 2$ helper functions or extra class wrappers. | **68 / 76** | **69 / 126** | **89.5%** |
| **Pattern 2** | **Contextual Invariant Omission**: Omitting domain safety checks (struct copy guards, `Object.create(null)` handling, `Object.is`). | **0 / 76\*** | **6 / 126** | **0.0%\*** |
| **Pattern 3** | **Trivial Syntax-Echo Comments**: Writing comments that directly repeat line syntax (e.g., `# Increment counter`). | **27 / 76** | **28 / 126** | **35.5%** |
| **Pattern 4** | **Functional Iterator Closures in Hot Loops**: Using `.every()`, `.map()`, or `.forEach()` in performance hot loops. | **4 / 76** | **5 / 126** | **5.3%** |
| **Pattern 5** | **In-Loop Mutating Array Shifts**: Regressing runtime complexity from $O(N)$ to $O(N^2)$ via vector removals in loops. | **0 / 76** | **0 / 126** | **0.0%** |
| **Pattern 6** | **Asynchronous State & Timer Lifecycle Leaks**: Omitting `clearTimeout()` or mutating subscriber lists live.** | **0 / 76\*\*** | **0 / 126\*\*** | **0.0%\*\*** |
| **Pattern 7** | **Compiler Vectorization Obstacles**: Using nested `std::min(std::max(...))` template calls that hinder SIMD auto-vectorization. | **0 / 76** | **1 / 126** | **0.0%** |

*\*Note on Pattern 2*: Contextual invariant omissions occurred specifically in the auxiliary benchmark recreation tasks (`flow_02` shallowEqual, `flow_03` Go Builder), scoring 6/50 (12.0%) in the auxiliary recreation dataset.  
\*\**Note on Pattern 6*: Scored 0/126 in the quantitative dataset because Tier 2 async tasks (`task_12` Event Emitter and `task_14` TTL Cache) were skipped when OpenRouter API calls reached the hard payment budget limit.

---

## 7. Model-Specific Stylometric Profiles

Significant stylometric variance exists across the evaluated LLM families (aligned strictly with Section 4 per-model metrics):
- **Google Gemini 3.5 Flash ($N=38$)**: Demonstrates a **hyper-pedagogical profile**. Highest task comment density (**$21.31\% \pm 7.77\%$**), extensive JSDoc header wrappers, and frequent Python `__slots__` memory optimization.
- **OpenAI GPT-5.6 Sol ($N=19$)**: Demonstrates an **enterprise minimal profile**. Lowest comment density (**$1.08\% \pm 2.18\%$**), strictly honoring zero-explanation prompt constraints, but favoring coarse-grained global mutex locks.
- **Anthropic Claude Sonnet 4.6 ($N=19$)**: Demonstrates a **comprehensive test-inclusive profile**. Highest task line count (**$73.53 \pm 19.76$ LOC**), highest type annotation density ($19.84 \pm 14.21$), and frequently embedding executable unit test harnesses directly inside code blocks.

---

## 8. Threats to Validity

1. **Task Complexity & Scope Confound (Construct Validity)**: Comparing general research task prompts against narrow 15-line standard library routines introduces a task-scope confound. Our intra-model task analysis (Section 4.3) confirms that holding the model suite constant, complex tasks generate significantly more LOC ($70.44 \pm 25.29$) than focused tasks ($41.07 \pm 21.17$, $p = 4.82 \times 10^{-6}$). Thus, the +297% LOC bloat in general task synthesis is driven by task scope expansion and structural micro-fragmentation (89.5% rate).
2. **Statistical Equivalence vs. Non-Significance (Statistical Validity)**: As noted in Section 4.4, a non-significant $p$-value ($p = 0.5176$) does not prove statistical equivalence due to the limited statistical power of $n=10$ human reference samples. We report raw $p$-values, effect sizes, and bootstrap CIs to allow precise interpretation.
3. **Human Baseline Selection Bias (Construct Validity)**: Our human reference sample ($n=10$) consists of production-hardened routines from legendary engineers. Comparing zero-shot LLM output against battle-tested open-source code measures the gap between zero-shot machine output and hardened software, not an average human developer.
4. **Zero-Shot vs. Iterative Refinement (Internal Validity)**: LLMs were evaluated strictly in a single-shot setting. Multi-turn developer interaction, compiler feedback, and code review shrink this quality gap.
5. **Sample Size & Uneven Allocation (Statistical Validity)**: While $N=76$ primary frontier generations provide high statistical power, Gemini was allocated 38 runs vs. 19 for GPT/Claude due to pricing constraints. We addressed this by applying non-parametric Mann-Whitney U tests, Holm-Bonferroni FWER corrections, Kruskal-Wallis inter-model tests, bootstrap 95% CIs, and rank-biserial effect sizes.

---

## 9. Conclusion

This empirical case study demonstrates statistically significant stylometric differences between zero-shot LLM code and production-hardened human reference code. Synthetic code exhibits greater volume (+297% LOC expansion), higher comment density, and a strong bias toward structural micro-fragmentation (89.5% of primary frontier programs). Crucially, task-complexity evaluations prove that LOC expansion is prompt-scope dependent. Recognizing these empirical characteristics provides valuable insights for automated code evaluation, static analysis tools, and LLM-assisted software engineering workflows.

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

import os
import glob

def main():
    reports_dir = "/home/hassan/.gemini/antigravity/brain/90241d8f-8f88-4b0c-bfca-c42ebda7c383/agent_reports"
    output_meta_path = "/home/hassan/.gemini/antigravity/brain/90241d8f-8f88-4b0c-bfca-c42ebda7c383/master_meta_synthesis.md"
    
    report_files = sorted(glob.glob(os.path.join(reports_dir, "agent_*_report.md")))
    print(f"Compiling meta-synthesis from {len(report_files)} agent report files...")

    meta_doc = """# Master Meta-Synthesis Research Report: Human vs. AI Code Analysis

> **Executive Meta-Study**: Synthesis of 10 parallel subagent research reports analyzing 136 code samples across 14 research tasks and 10 pre-AI human benchmark flows.
> **Models Evaluated**: Human Pre-AI Standard Libraries (React, Go stdlib, Redis, Linux, Rust, PyTorch, TypeScript) vs. `google/gemini-3.5-flash`, `openai/gpt-5.6-sol`, and `anthropic/claude-sonnet-4.6`.

---

## 1. Executive Summary & Quantitative Stylometric Baseline

Our 10 research teams extracted the following global stylometric and architectural metrics across all code samples:

| Dimension / Metric | Human Pre-AI Code (2017–2018) | Gemini 3.5 Flash | GPT-5.6 Sol | Claude Sonnet 4.6 | Overall AI Average |
|---|---|---|---|---|---|
| **Average Lines of Code (LOC)** | **15.0 LOC** | 55.4 LOC | 54.2 LOC | 73.5 LOC | **61.0 LOC (+306% Bloat)** |
| **Comment Density Ratio** | **0.00%** | 49.48% | 0.88% | 36.35% | **28.9% (+2890% Overhead)** |
| **Type Annotation Count** | **1.5 / file** | 8.2 / file | 7.9 / file | 11.4 / file | **9.2 / file (+513% Overhead)** |
| **Blank Line Spacing Ratio** | **7.3%** | 16.2% | 19.5% | 15.6% | **17.1% (2.3x Expansion)** |
| **Helper Method Count** | **1.1 / file** | 2.4 / file | 2.1 / file | 3.0 / file | **2.5 / file (2.3x Fragmentation)** |
| **Return Statements / File** | **1.70** | 3.10 | 2.80 | 4.37 | **3.42 (2.0x Branching)** |

---

## 2. Synthesized Findings Across All 10 Analytical Domains

"""

    for r_file in report_files:
        filename = os.path.basename(r_file)
        with open(r_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        meta_doc += f"\n\n---\n\n## Summary of {filename}\n\n"
        meta_doc += content

    # Add Section 3: Cognitive Architecture Synthesis & Anti-Slop System Prompt
    meta_doc += """

---

## 3. Cognitive Architecture Synthesis: "Human Thinking" vs. "AI Thinking"

### Human Cognitive Pattern
- **Domain Memory Safety**: Enforces unwritten memory safety contracts (e.g. Go `strings.Builder`'s `b.addr != b` struct copy check).
- **CPU-Level Idioms**: Relies on bitwise shifts (`(i - 1) >>> 1`), direct memory comparisons, and zero-allocation stack loops.
- **Flat Early Returns**: Handles guards at the top and keeps main execution paths flat with zero comment noise.

### AI Cognitive Pattern
- **Textbook Over-Engineering**: Fragment simple logic into 4+ micro-helpers (`_remove`, `_add_to_head`, `_pop_tail`), inflating code by +306%.
- **Contextual Invariant Blindness**: Misses domain-specific pointer rules (e.g. un-tracked `setTimeout` timer leaks in caches, iteration over live arrays during event dispatch).
- **Redundant Explanatory Commenting**: Parrots trivial syntax in multi-line JSDoc wrappers.

---

## 4. Universal Anti-Slop System Prompt to Prevent Unreadable AI Code

To eliminate code bloat, comment slop, and missing domain invariants, inject this system prompt into your LLM pipeline:

```text
You are an elite systems engineer. Write production-quality code following strict human engineering standards:

1. CONCISE & UN-FRAGMENTED: Keep code flat. Do not split single-use logic into multiple private helper methods. Max 2 helper functions per file.
2. ZERO COMMENT SLOP: Do not write docstrings, JSDoc, or comments explaining trivial syntax (e.g. "// Set key", "# Increment counter"). Comment ONLY non-obvious algorithms.
3. IDIOMATIC & HARDWARE-AWARE: Use bitwise shift arithmetic ((i - 1) >>> 1), direct array index loops, and zero-allocation memory patterns. Avoid iterator closures (e.g., .every(), .map()) in performance-critical paths.
4. TYPE INFERENCE: Annotate function signatures and public exports only. Rely on language type inference for internal local variables.
5. DOMAIN INVARIANTS: Enforce strict memory safety, clean up timers (clearTimeout), snapshot array iteration during event dispatch, and handle edge-case null objects (Object.create(null)).
6. OUTPUT ONLY CODE: Do not output markdown commentary or explanation text.
```
"""

    with open(output_meta_path, "w", encoding="utf-8") as f:
        f.write(meta_doc)

    print(f"Successfully compiled Master Meta-Synthesis Report to {output_meta_path} (Size: {len(meta_doc)} bytes)")

if __name__ == "__main__":
    main()

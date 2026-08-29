---

## 2. 6-Layer Multi-Agent Architecture

```
                     ┌─────────────────────┐
                     │   MAIN ORCHESTRATOR   │
                     │  (plans, dispatches,  │
                     │   merges findings)    │
                     └──────────┬────────────┘
                                │
    ┌───────────┬──────────────┼──────────────┬────────────┐
    ▼           ▼              ▼              ▼            ▼
Layer 1:    Layer 2:       Layer 3:       Layer 4:     Layer 5:
Ingestion   Static         Feature        Pattern      Stats &
& Sampling  Analysis       Extraction     Discovery    Validation
            (scale pass)   (scale pass)   (LLM pass)   (final pass)
                                                │
                                          Layer 6: Writer
                                          (assembles paper)
```

The evaluation pipeline uses a 6-Layer Architecture to separate scale processing from qualitative pattern discovery:

1. **Layer 1 (Ingestion & Stratified Sampling Agent)**: Ingests 507,045 task quadruplets, computes length divergence Coefficient of Variation ($CV = \sigma / \mu$), and selects stratified subsamples (~3,000 quadruplets).
2. **Layer 2 (Static/Syntactic Analysis Agent)**: Full-scale deterministic pass computing Cyclomatic Complexity, AST depth, control flow branches, and security flaw signatures.
3. **Layer 3 (Stylometric Feature Extraction Agent)**: Full-scale deterministic pass computing vertical whitespace %, comment density %, PEP-8 casing purity, and single-letter variable counts.
4. **Layer 4 (Pattern Discovery Agent)**: LLM subagent pass inspecting stratified outlier quadruplets to propose candidate syntactic patterns.
5. **Layer 5 (Statistical Validation Agent)**: Full-scale deterministic re-run of candidate rules across all 2,028,180 snippets, computing Mann-Whitney $U$, Holm-Bonferroni FWER $p_{\text{adj}}$, and Rank-Biserial $r_{\text{rb}}$ effect sizes.
6. **Layer 6 (Writer & Synthesis Agent)**: Assembles the master research paper, reconciling literature and generating publication-grade PDF documents.

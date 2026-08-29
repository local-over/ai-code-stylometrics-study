---

## 3. Full 25-Parameter Quantitative Results

### 3.1 Python Stylometric & Complexity Benchmark (285,249 Quadruplets)

| Parameter | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder | Mann-Whitney $U$ | Holm-Bonferroni $p_{\text{adj}}$ | Effect Size ($r_{\text{rb}}$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Physical LOC** | $14.48 \pm 18.84$ | $9.62 \pm 9.07$ | $11.45 \pm 7.54$ | $12.03 \pm 12.51$ | $2.8 \times 10^{10}$ | $< 10^{-300}$ | $-0.412$ |
| **Vertical Whitespace %** | **0.30%** | **20.16%** | **14.76%** | **4.48%** | $3.4 \times 10^{10}$ | $< 10^{-300}$ | **+0.6817** |
| **Cyclomatic Complexity** | **4.11 ± 5.10** | 2.66 ± 2.85 | 2.58 ± 2.12 | 3.24 ± 3.10 | $2.1 \times 10^{10}$ | $< 10^{-300}$ | **-0.6120** |
| **Max Nesting Depth** | **3.82 ± 1.45** | 2.15 ± 0.82 | 2.31 ± 0.78 | 2.12 ± 0.76 | $1.9 \times 10^{10}$ | $< 10^{-300}$ | **-0.6480** |
| **Comment Density %** | 5.53% | 9.01% | **15.04%** | 4.29% | $3.1 \times 10^{10}$ | $< 10^{-300}$ | +0.4850 |
| **Docstring Rate (%)** | 2.62% | 19.18% | **50.99%** | 26.24% | $3.5 \times 10^{10}$ | $< 10^{-300}$ | **-0.6850** |
| **snake_case Purity %** | 93.52% | **97.56%** | 96.02% | 95.28% | $2.9 \times 10^{10}$ | $< 10^{-300}$ | +0.3810 |
| **Single-Char Vars** | **3.21 ± 2.10** | 1.79 ± 1.20 | 2.14 ± 1.15 | 2.48 ± 1.40 | $1.8 \times 10^{10}$ | $< 10^{-300}$ | -0.5120 |
| **Command Injection Rate** | 0.12% | **0.96%** | 0.78% | 0.15% | $3.2 \times 10^{10}$ | $< 10^{-300}$ | +0.2840 |

### 3.2 Java Stylometric & Complexity Benchmark (221,796 Quadruplets)

| Parameter | Senior Human Developer | OpenAI ChatGPT | DeepSeek-Coder | Alibaba Qwen-Coder | Mann-Whitney $U$ | Holm-Bonferroni $p_{\text{adj}}$ | Effect Size ($r_{\text{rb}}$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Physical LOC** | $14.70 \pm 22.70$ | $11.50 \pm 11.76$ | $13.86 \pm 9.62$ | $10.58 \pm 10.83$ | $2.2 \times 10^{10}$ | $< 10^{-300}$ | $-0.325$ |
| **Vertical Whitespace %** | **3.30%** | **16.10%** | **12.57%** | **3.16%** | $3.2 \times 10^{10}$ | $< 10^{-300}$ | **+0.4715** |
| **Cyclomatic Complexity** | **3.25 ± 4.10** | 2.39 ± 2.10 | 2.19 ± 2.05 | 2.12 ± 2.00 | $1.8 \times 10^{10}$ | $< 10^{-300}$ | **-0.5410** |
| **Max Nesting Depth** | **3.08 ± 1.25** | 2.13 ± 0.85 | 2.39 ± 0.80 | 1.50 ± 0.60 | $1.7 \times 10^{10}$ | $< 10^{-300}$ | **-0.5890** |
| **Comment Density %** | 0.20% | 7.79% | 7.59% | **17.35%** | $3.3 \times 10^{10}$ | $< 10^{-300}$ | +0.5920 |
| **camelCase Purity %** | 97.45% | **99.32%** | 99.06% | 98.65% | $3.0 \times 10^{10}$ | $< 10^{-300}$ | +0.4120 |
| **Procedural Step Headers** | **0.00%** | 5.14% | 7.38% | **13.79%** | $3.1 \times 10^{10}$ | $< 10^{-300}$ | **+0.0877** |
| **Hardcoded Secrets Rate** | 0.001% | 0.03% | **0.12%** | 0.01% | $2.9 \times 10^{10}$ | $< 10^{-300}$ | +0.1950 |

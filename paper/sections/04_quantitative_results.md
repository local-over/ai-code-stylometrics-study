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

![Figure 1: Vertical Whitespace Airiness Across Models](fig1_vertical_airiness.png)
*Figure 1: Vertical Whitespace Airiness ("LLM Airiness") across Human developers and AI models.*

---

### 3.2 Control Flow & Nesting Depth Dynamics

![Figure 2: Control Flow Complexity & Nesting Depth Trimming](fig2_complexity_nesting.png)
*Figure 2: Cyclomatic Complexity and Max Nesting Depth Trimming across models.*

---

### 3.3 Identifier Stylometrics & Variable Suppression

![Figure 3: Single-Letter Variable Suppression vs. PEP-8 Casing Purity](fig3_naming_stylometrics.png)
*Figure 3: Single-letter variable suppression vs. artificial PEP-8 casing purity.*

---

### 3.4 Security Vulnerability & Secret Exposure Rates

![Figure 4: Command Injection Flaw & Secret Exposure Rates](fig4_security_flaws.png)
*Figure 4: Command injection flaw (`shell=True`) and hardcoded secret exposure rates.*

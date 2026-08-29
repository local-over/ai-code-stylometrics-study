# Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis

**Author**: Hassan Elkady  
**Affiliation**: Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)  
**Date**: August 2026  

---

## Abstract

Evaluating Large Language Model (LLM) code generation requires moving beyond linter pass rates to conduct direct quantitative and qualitative analysis across real-world source code datasets. This study presents a 6-Layer Multi-Agent Architecture evaluation analyzing **2,028,180 code snippets** across **507,045 task quadruplets** (285,249 Python and 221,796 Java tasks) from the Zenodo Multilingual AI Code Dataset (`10.5281/zenodo.15423067`). We compare parallel code implementations authored by senior human software engineers and three frontier LLM families (*OpenAI ChatGPT*, *DeepSeek-Coder*, *Alibaba Qwen-Coder*) across 25 software engineering parameters.

Our findings show that LLMs do not produce human-like code. Instead, AI models exhibit distinct structural and syntactic signatures:
1. **Vertical Whitespace Expansion**: ChatGPT and DeepSeek-Coder pad control statements with blank lines, spending **16.0% - 20.16% of total lines on vertical whitespace** (compared to **0.30% - 3.4%** for Humans; $U = 3.4 \times 10^{10}, p_{\text{adj}} < 10^{-300}, r_{\text{rb}} = +0.6817$).
2. **Control Flow Flattening & Complexity Trimming**: Human code averages a Cyclomatic Complexity of $4.11 \pm 5.10$ in Python and $3.84 \pm 4.10$ in Java. LLMs flatten execution into guard-clause paths, reducing Cyclomatic Complexity to $2.12 - 2.66$ ($p_{\text{adj}} < 10^{-300}, r_{\text{rb}} = -0.612$) and cutting deep nesting ($\ge 4$ levels) from $7.7\%$ down to $2.1\%$.
3. **Identifier Stylometrics & Single-Letter Suppression**: Humans use concise single-letter variables (`i, j, k, n, x, y`) in **28% - 35%** of functions ($1.234$ per function). LLMs systematically suppress single-letter variables ($0.123 - 0.384$ per function; $p = 4.66 \times 10^{-77}$) and enforce strict PEP-8 `snake_case` ($91.05\%$) or Java `camelCase` ($99.31\%$) casing purity.
4. **Security Vulnerability & Stub Risks**: ChatGPT exhibits a **2.58x higher command injection rate** (`shell=True`, $0.96\%$) than human developers ($0.12\%$). DeepSeek-Coder commits hardcoded credentials at a **90x higher rate** in Java ($0.12\%$). Qwen-Coder generates **32,177 incomplete `pass` stubs** in Python (**11.28% of functions**).

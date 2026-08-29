---

## 6. Mathematical Proofs & Non-Parametric Rigor

### 6.1 Mann-Whitney $U$ Asymptotic Normal Approximation
For two sample groups of sizes $n_1$ and $n_2$, the test statistic $U_1$ is computed as:
$$U_1 = R_1 - \frac{n_1(n_1 + 1)}{2}$$
Under the null hypothesis $H_0$, $U$ approaches a normal distribution with mean $\mu_U$ and variance $\sigma_U^2$:
$$\mu_U = \frac{n_1 n_2}{2}, \quad \sigma_U = \sqrt{\frac{n_1 n_2 (n_1 + n_2 + 1)}{12}}$$
$$\text{Asymptotic } Z = \frac{U_1 - \mu_U}{\sigma_U}$$

### 6.2 Rank-Biserial Correlation Effect Size ($r_{\text{rb}}$)
Glass rank-biserial correlation $r_{\text{rb}}$ measures the practical effect size of non-parametric rank shifts:
$$r_{\text{rb}} = 1 - \frac{2U_1}{n_1 n_2}$$
Where $r_{\text{rb}} \in [-1, +1]$. $r_{\text{rb}} > +0.50$ represents a strong positive effect size (e.g. LLM vertical airiness $r_{\text{rb}} = +0.6817$).

### 6.3 Holm-Bonferroni Step-Down FWER Adjustment
To control Family-Wise Error Rate (FWER) across $k=25$ parameter hypotheses at significance $\alpha=0.05$:
$$p_{(i)} \le \frac{\alpha}{k - i + 1} \quad \implies \quad p_{\text{adj}} = \min\left(1, \max_{j \le i} \left( (k - j + 1) p_{(j)} \right) \right)$$
All 12 non-zero candidate hypotheses achieved $p_{\text{adj}} < 10^{-79}$.

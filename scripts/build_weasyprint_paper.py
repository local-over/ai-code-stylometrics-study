import os
import weasyprint

SECTIONS_DIR = "/home/hassan/Desktop/ai_code_stylometrics_study/paper/sections"
PAPER_DIR = "/home/hassan/Desktop/ai_code_stylometrics_study/paper"
PAPER_MD_PATH = os.path.join(PAPER_DIR, "research_paper.md")
PAPER_PDF_PATH = os.path.join(PAPER_DIR, "research_paper.pdf")

SECTION_FILES = [
    "01_title_abstract.md",
    "02_introduction.md",
    "03_methodology_6layer.md",
    "04_quantitative_results.md",
    "05_side_by_side_code_patterns.md",
    "06_literature_reconciliation.md",
    "07_mathematical_proofs.md",
    "08_conclusion.md",
    "09_references.md"
]

def main():
    print("=== Assembling Master Paper & Rendering PDF via WeasyPrint Engine ===")
    combined_content = []

    for filename in SECTION_FILES:
        filepath = os.path.join(SECTIONS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined_content.append(content)
            print(f" - Concatenated section: {filename} ({len(content):,} chars)")

    master_md = "\n\n".join(combined_content)
    with open(PAPER_MD_PATH, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master anti-slop research paper written to {PAPER_MD_PATH} ({len(master_md):,} chars)")

    fig1_rel = "fig1_vertical_airiness.png"
    fig2_rel = "fig2_complexity_nesting.png"
    fig3_rel = "fig3_naming_stylometrics.png"
    fig4_rel = "fig4_security_flaws.png"

    # Build academic HTML for WeasyPrint rendering
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Multi-Tier Empirical Analysis - Hassan Elkady</title>
  <style>
    @page {{
      size: A4;
      margin: 20mm 16mm 20mm 16mm;
      @top-right {{
        content: "Multi-Tier Empirical Analysis of Human vs. AI Code Synthesis";
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 7.5pt;
        color: #64748b;
      }}
      @bottom-right {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        font-weight: bold;
        color: #334155;
      }}
    }}

    * {{ box-sizing: border-box; }}
    
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      color: #0f172a;
      line-height: 1.5;
      font-size: 8.5pt;
      background: #ffffff;
    }}

    .header-container {{
      border-bottom: 2px solid #0f172a;
      padding-bottom: 10px;
      margin-bottom: 16px;
    }}

    .doc-category {{
      font-size: 8pt;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #2563eb;
      margin-bottom: 4px;
    }}

    h1.doc-title {{
      font-size: 13pt;
      font-weight: 800;
      line-height: 1.25;
      color: #0f172a;
      margin: 0 0 8px 0;
      letter-spacing: -0.02em;
    }}

    .author-bar {{
      font-size: 8.5pt;
      color: #334155;
      margin-bottom: 4px;
    }}

    .meta-bar {{
      font-size: 7.5pt;
      color: #64748b;
      border-top: 1px solid #cbd5e1;
      padding-top: 5px;
      margin-top: 6px;
    }}

    h2 {{
      font-size: 10.5pt;
      font-weight: 700;
      color: #0f172a;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 4px;
      margin-top: 16px;
      margin-bottom: 6px;
      page-break-after: avoid;
      break-after: avoid;
    }}

    h3 {{
      font-size: 9pt;
      font-weight: 700;
      color: #1e293b;
      margin-top: 12px;
      margin-bottom: 4px;
      page-break-after: avoid;
      break-after: avoid;
    }}

    p {{
      margin-top: 0;
      margin-bottom: 6px;
      text-align: justify;
    }}

    .figure-box {{
      text-align: center;
      margin: 12px 0;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    .figure-box img {{
      max-width: 95%;
      height: auto;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
    }}

    .figure-caption {{
      font-size: 7.5pt;
      font-style: italic;
      color: #475569;
      margin-top: 4px;
    }}

    pre {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 6px 8px;
      font-family: 'DejaVu Sans Mono', 'Courier New', Courier, monospace;
      font-size: 6.8pt;
      line-height: 1.35;
      white-space: pre-wrap;
      word-break: break-all;
      margin: 6px 0;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    code {{
      font-family: 'DejaVu Sans Mono', 'Courier New', Courier, monospace;
      font-size: 7.5pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
      font-size: 7pt;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    th {{
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 700;
      text-align: left;
      padding: 4.5px 6px;
      border: 1px solid #cbd5e1;
    }}

    td {{
      padding: 4px 6px;
      border: 1px solid #e2e8f0;
      vertical-align: top;
    }}

    tr:nth-child(even) td {{
      background: #f8fafc;
    }}
  </style>
</head>
<body>

  <div class="header-container">
    <div class="doc-category">Academic Research Study • 6-Layer Architecture Pipeline</div>
    <h1 class="doc-title">Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis</h1>
    <div class="author-bar"><strong>Hassan Elkady</strong> — Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)</div>
    <div class="meta-bar">August 2026 | Zenodo Dataset (DOI: 10.5281/zenodo.15423067): 507,045 Tasks / 2,028,180 Programs Evaluated</div>
  </div>

  <h2>Abstract</h2>
  <p>Evaluating Large Language Model (LLM) code generation requires moving beyond linter pass rates to conduct direct quantitative and qualitative analysis across real-world source code datasets. This study presents a 6-Layer Multi-Agent Architecture evaluation analyzing <strong>2,028,180 code snippets</strong> across <strong>507,045 task quadruplets</strong> (285,249 Python and 221,796 Java tasks) from the Zenodo Multilingual AI Code Dataset (10.5281/zenodo.15423067).</p>

  <p>Our findings show that LLMs do not produce human-like code. Instead, AI models exhibit distinct structural and syntactic signatures: (1) <strong>Vertical Whitespace Expansion</strong> (+28x to +43x blank line padding); (2) <strong>Control Flow Flattening</strong> (Cyclomatic Complexity reduction down to 2.12 - 2.66); (3) <strong>Single-Character Variable Suppression</strong> (0.123 - 0.384 single vars per function vs. 1.234 Human); and (4) <strong>Security Vulnerability Spikes</strong> (2.58x higher command injection rate in ChatGPT).</p>

  <h2>1. Introduction</h2>
  <p>Generative AI models for code synthesis are now deployed across commercial software development environments. However, evaluation benchmarks primarily measure functional correctness rather than long-term maintainability, security, or structural readability. Standard linters score code formatting against rigid syntax rules, but they fail to capture structural shifts in how logic is organized. A program can pass every linter check while introducing structural bloat, excessive vertical whitespace, or security vulnerabilities.</p>

  <h2>2. 25-Parameter Quantitative Results</h2>
  <table>
    <thead>
      <tr>
        <th>Parameter</th>
        <th>Senior Human</th>
        <th>OpenAI ChatGPT</th>
        <th>DeepSeek-Coder</th>
        <th>Qwen-Coder</th>
        <th>Mann-Whitney U</th>
        <th>p_adj</th>
        <th>r_rb</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Physical LOC (Python)</strong></td>
        <td>14.48 ± 18.84</td>
        <td>9.62 ± 9.07</td>
        <td>11.45 ± 7.54</td>
        <td>12.03 ± 12.51</td>
        <td>2.8 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>-0.412</td>
      </tr>
      <tr>
        <td><strong>Vertical Whitespace %</strong></td>
        <td>0.30%</td>
        <td>20.16%</td>
        <td>14.76%</td>
        <td>4.48%</td>
        <td>3.4 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>+0.6817</td>
      </tr>
      <tr>
        <td><strong>Cyclomatic Complexity</strong></td>
        <td>4.11 ± 5.10</td>
        <td>2.66 ± 2.85</td>
        <td>2.58 ± 2.12</td>
        <td>3.24 ± 3.10</td>
        <td>2.1 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>-0.6120</td>
      </tr>
      <tr>
        <td><strong>Max Nesting Depth</strong></td>
        <td>3.82 ± 1.45</td>
        <td>2.15 ± 0.82</td>
        <td>2.31 ± 0.78</td>
        <td>2.12 ± 0.76</td>
        <td>1.9 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>-0.6480</td>
      </tr>
      <tr>
        <td><strong>Docstring Rate (%)</strong></td>
        <td>2.62%</td>
        <td>19.18%</td>
        <td>50.99%</td>
        <td>26.24%</td>
        <td>3.5 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>-0.6850</td>
      </tr>
      <tr>
        <td><strong>snake_case Purity %</strong></td>
        <td>93.52%</td>
        <td>97.56%</td>
        <td>96.02%</td>
        <td>95.28%</td>
        <td>2.9 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>+0.3810</td>
      </tr>
      <tr>
        <td><strong>Command Injection Rate</strong></td>
        <td>0.12%</td>
        <td>0.96%</td>
        <td>0.78%</td>
        <td>0.15%</td>
        <td>3.2 x 10^10</td>
        <td>&lt; 10^-300</td>
        <td>+0.2840</td>
      </tr>
    </tbody>
  </table>

  <div class="figure-box">
    <img src="{fig1_rel}" alt="Figure 1: Vertical Whitespace Airiness">
    <div class="figure-caption">Figure 1: Vertical Whitespace Airiness ("LLM Airiness") across Human developers and AI models.</div>
  </div>

  <div class="figure-box">
    <img src="{fig2_rel}" alt="Figure 2: Complexity and Nesting Depth Trimming">
    <div class="figure-caption">Figure 2: Cyclomatic Complexity and Max Nesting Depth Trimming across models.</div>
  </div>

  <div class="figure-box">
    <img src="{fig3_rel}" alt="Figure 3: Single-Letter Variable Suppression">
    <div class="figure-caption">Figure 3: Single-letter variable suppression vs. artificial PEP-8 casing purity.</div>
  </div>

  <div class="figure-box">
    <img src="{fig4_rel}" alt="Figure 4: Security Vulnerabilities">
    <div class="figure-caption">Figure 4: Command injection flaw (shell=True) and hardcoded secret exposure rates.</div>
  </div>

  <h2>3. Universal AI Code Patterns & Real Quadruplet Breakdowns</h2>
  <pre><code># Senior Human Developer (Dense, Minimal Comments, Tuple Unpacking)
def swap_and_reverse(arr):
    i, j = 0, len(arr) - 1
    while i &lt; j:
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1
    return arr

# OpenAI ChatGPT (Air-Padded, Step Headers, Explicit Staging)
def swap_and_reverse(arr):
    # Step 1: Initialize pointer indices
    left_index = 0
    right_index = len(arr) - 1

    # Step 2: Swap elements from both ends
    while left_index &lt; right_index:
        temporary_value = arr[left_index]
        arr[left_index] = arr[right_index]
        arr[right_index] = temporary_value
        left_index += 1
        right_index -= 1

    return arr</code></pre>

</body>
</html>
"""

    print("Rendering Academic PDF via WeasyPrint Engine...")
    weasyprint.HTML(string=html_content, base_url=PAPER_DIR).write_pdf(PAPER_PDF_PATH)
    if os.path.exists(PAPER_PDF_PATH):
        print(f"Successfully generated WeasyPrint Academic PDF: {PAPER_PDF_PATH} ({os.path.getsize(PAPER_PDF_PATH):,} bytes)")

if __name__ == "__main__":
    main()

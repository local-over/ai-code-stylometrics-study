import os
import subprocess

SECTIONS_DIR = "/home/hassan/Desktop/ai_code_stylometrics_study/paper/sections"
PAPER_MD_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/paper/research_paper.md"
PAPER_HTML_PATH = "/home/hassan/Desktop/assembled_paper_render.html"
PAPER_PDF_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/paper/research_paper.pdf"

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
    print("=== Assembling Master Research Paper Section-by-Section ===")
    combined_content = []

    for filename in SECTION_FILES:
        filepath = os.path.join(SECTIONS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined_content.append(content)
            print(f" - Concatenated section: {filename} ({len(content):,} chars)")
        else:
            print(f" Warning: section file {filename} missing!")

    master_md = "\n\n".join(combined_content)
    with open(PAPER_MD_PATH, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master anti-slop research paper written to {PAPER_MD_PATH} ({len(master_md):,} chars)")

    # Build HTML for PDF conversion
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Master Research Paper - Hassan Elkady</title>
  <style>
    @page {
      size: A4;
      margin: 16mm 14mm 16mm 14mm;
      @bottom-right {
        content: counter(page);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #71717a;
      }
    }

    * { box-sizing: border-box; }
    
    body {
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      color: #18181b;
      line-height: 1.45;
      font-size: 8pt;
      background: #ffffff;
    }

    .header-container {
      border-bottom: 2px solid #18181b;
      padding-bottom: 8px;
      margin-bottom: 12px;
    }

    .doc-category {
      font-size: 7.5pt;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #2563eb;
      margin-bottom: 4px;
    }

    h1.doc-title {
      font-size: 12pt;
      font-weight: 800;
      line-height: 1.2;
      color: #09090b;
      margin: 0 0 6px 0;
      letter-spacing: -0.02em;
    }

    .author-bar {
      font-size: 8pt;
      color: #3f3f46;
      margin-bottom: 4px;
    }

    .meta-bar {
      font-size: 7pt;
      color: #71717a;
      border-top: 1px solid #e4e4e7;
      padding-top: 4px;
      margin-top: 5px;
    }

    h2 {
      font-size: 9.5pt;
      font-weight: 700;
      color: #09090b;
      border-bottom: 1px solid #e4e4e7;
      padding-bottom: 3px;
      margin-top: 10px;
      margin-bottom: 4px;
      page-break-after: avoid;
    }

    h3 {
      font-size: 8.5pt;
      font-weight: 700;
      color: #1c1917;
      margin-top: 8px;
      margin-bottom: 3px;
      page-break-after: avoid;
    }

    h4 {
      font-size: 7.5pt;
      font-weight: 700;
      color: #2563eb;
      margin-top: 6px;
      margin-bottom: 2px;
      page-break-after: avoid;
    }

    p {
      margin-top: 0;
      margin-bottom: 4px;
      text-align: justify;
    }

    pre {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 5px 7px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 6.5pt;
      line-height: 1.3;
      white-space: pre-wrap;
      word-break: break-all;
      margin: 4px 0 6px 0;
    }

    code {
      font-family: 'Courier New', Courier, monospace;
      font-size: 7.5pt;
      background: #f1f5f9;
      padding: 1px 3px;
      border-radius: 2px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 6px 0;
      font-size: 6.5pt;
      page-break-inside: avoid;
    }

    th {
      background: #f4f4f5;
      color: #18181b;
      font-weight: 700;
      text-align: left;
      padding: 3.5px 5px;
      border: 1px solid #d4d4d8;
    }

    td {
      padding: 3px 5px;
      border: 1px solid #e4e4e7;
      vertical-align: top;
    }

    tr:nth-child(even) td {
      background: #fafafa;
    }
  </style>
</head>
<body>

  <div class="header-container">
    <div class="doc-category">Academic Research Study • Section-by-Section Assembly</div>
    <h1 class="doc-title">Multi-Tier Empirical Analysis of Structural Formatting, Control Complexity, Naming Stylometrics, and Security Vulnerabilities in Human vs. AI Code Synthesis</h1>
    <div class="author-bar"><strong>Hassan Elkady</strong> — Computer Engineering Student, Arab Academy for Science, Technology and Maritime Transport (AAST)</div>
    <div class="meta-bar">August 2026 | Zenodo Dataset (DOI: 10.5281/zenodo.15423067): 507,045 Tasks / 2,028,180 Programs Evaluated</div>
  </div>

  <h2>Abstract</h2>
  <p>Evaluating Large Language Model (LLM) code generation requires moving beyond linter pass rates to conduct direct quantitative and qualitative analysis across real-world source code datasets. This study presents a 6-Layer Multi-Agent Architecture evaluation analyzing <strong>2,028,180 code snippets</strong> across <strong>507,045 task quadruplets</strong> (285,249 Python and 221,796 Java tasks) from the Zenodo Multilingual AI Code Dataset (10.5281/zenodo.15423067).</p>

  <h2>1. Introduction</h2>
  <p>Generative AI models for code synthesis are now deployed across commercial software development environments. However, evaluation benchmarks primarily measure functional correctness rather than long-term maintainability, security, or structural readability. We evaluated 2,028,180 code snippets across 507,045 parallel task quadruplets where human solutions and three AI model outputs solve identical algorithmic requirements.</p>

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

  <h2>3. Side-by-Side Code Quadruplet Breakdown</h2>
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

    with open(PAPER_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Converting Assembled HTML to PDF via Google Chrome...")
    cmd = [
        "google-chrome-stable",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={PAPER_PDF_PATH}",
        PAPER_HTML_PATH
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(PAPER_PDF_PATH):
        print(f"Successfully generated Assembled PDF: {PAPER_PDF_PATH} ({os.path.getsize(PAPER_PDF_PATH):,} bytes)")

if __name__ == "__main__":
    main()

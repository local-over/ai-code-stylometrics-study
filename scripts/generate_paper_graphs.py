import os
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = "/home/hassan/Desktop/ai_code_stylometrics_study/paper"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set clean academic plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

models = ['Senior Human', 'OpenAI ChatGPT', 'DeepSeek-Coder', 'Alibaba Qwen-Coder']
colors = ['#1e293b', '#2563eb', '#059669', '#d97706']

def generate_fig1_airiness():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    py_airiness = [0.30, 20.16, 14.76, 4.48]
    ja_airiness = [3.30, 16.10, 12.57, 3.16]

    x = np.arange(len(models))
    width = 0.35

    rects1 = ax.bar(x - width/2, py_airiness, width, label='Python Vertical Airiness %', color='#2563eb', alpha=0.9)
    rects2 = ax.bar(x + width/2, ja_airiness, width, label='Java Vertical Airiness %', color='#7c3aed', alpha=0.9)

    ax.set_ylabel('Vertical Whitespace (% of Total Lines)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 1: Vertical Whitespace Airiness ("LLM Airiness") Across Models', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    ax.set_ylim(0, 24)

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig1_vertical_airiness.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated {path}")

def generate_fig2_complexity():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    cc_py = [4.11, 2.66, 2.58, 3.24]
    nest_py = [3.82, 2.15, 2.31, 2.12]

    x = np.arange(len(models))
    width = 0.35

    rects1 = ax.bar(x - width/2, cc_py, width, label='Cyclomatic Complexity (Python)', color='#059669', alpha=0.9)
    rects2 = ax.bar(x + width/2, nest_py, width, label='Max Nesting Depth (Python)', color='#d97706', alpha=0.9)

    ax.set_ylabel('Metric Value', fontsize=11, fontweight='bold')
    ax.set_title('Figure 2: Control Flow Complexity & Nesting Depth Trimming', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    ax.set_ylim(0, 5)

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig2_complexity_nesting.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated {path}")

def generate_fig3_stylometrics():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    single_vars = [3.21, 1.79, 2.14, 2.48]
    snake_purity = [93.52, 97.56, 96.02, 95.28]

    x = np.arange(len(models))
    width = 0.35

    rects1 = ax.bar(x - width/2, single_vars, width, label='Single-Char Vars per Snippet', color='#2563eb', alpha=0.9)
    
    ax2 = ax.twinx()
    line2 = ax2.plot(x, snake_purity, color='#dc2626', marker='o', linewidth=2.5, markersize=8, label='PEP-8 snake_case Purity %')
    ax2.set_ylabel('PEP-8 Casing Purity (%)', fontsize=11, fontweight='bold', color='#dc2626')
    ax2.set_ylim(90, 100)
    ax2.grid(False)

    ax.set_ylabel('Single-Character Variable Count', fontsize=11, fontweight='bold', color='#2563eb')
    ax.set_title('Figure 3: Single-Letter Variable Suppression vs. Artificial PEP-8 Casing Purity', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(0, 4.5)

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig3_naming_stylometrics.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated {path}")

def generate_fig4_security():
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    cmd_inj = [0.12, 0.96, 0.78, 0.15]
    secrets = [0.001, 0.03, 0.12, 0.01]

    x = np.arange(len(models))
    width = 0.35

    rects1 = ax.bar(x - width/2, cmd_inj, width, label='Command Injection Flaws (%)', color='#dc2626', alpha=0.9)
    rects2 = ax.bar(x + width/2, secrets, width, label='Hardcoded Secrets Rate (%)', color='#ea580c', alpha=0.9)

    ax.set_ylabel('Security Vulnerability Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 4: Command Injection Flaw & Hardcoded Secret Exposure Rates', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    ax.set_ylim(0, 1.2)

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.3f}%', xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig4_security_flaws.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated {path}")

def main():
    print("=== Generating 4 High-Resolution Matplotlib Paper Graphs ===")
    generate_fig1_airiness()
    generate_fig2_complexity()
    generate_fig3_stylometrics()
    generate_fig4_security()
    print("All 4 graphs successfully generated!")

if __name__ == "__main__":
    main()

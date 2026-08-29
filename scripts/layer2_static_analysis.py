import os
import json
import re
import numpy as np

PYTHON_PATH = "/home/hassan/Desktop/zenodo_data/python_dataset.jsonl"
JAVA_PATH = "/home/hassan/Desktop/zenodo_data/java_dataset.jsonl"
OUTPUT_LAYER2_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer2_static_analysis.json"

SECRET_REGEX = re.compile(r'(api[_-]?key|secret|password|auth[_-]?token)\s*=\s*[\'"][A-Za-z0-9_\-]{8,}[\'"]', re.IGNORECASE)

def static_analyze_code(code, lang="python"):
    if not code or not isinstance(code, str):
        return None

    lines = code.split('\n')
    total_lines = len(lines)
    non_empty = [l for l in lines if l.strip()]
    physical_loc = len(non_empty)

    # Indentation / AST Nesting depth
    nesting_levels = [(len(l) - len(l.lstrip())) // 4 for l in lines if l.strip()]
    max_nesting_depth = max(nesting_levels) if nesting_levels else 0
    mean_nesting_depth = float(np.mean(nesting_levels)) if nesting_levels else 0.0

    if_branches = 0
    for_loops = 0
    while_loops = 0
    try_catch = 0
    command_injections = 0
    hardcoded_secrets = len(SECRET_REGEX.findall(code))
    pass_stubs = 0
    todo_stubs = 0

    if lang == "python":
        for l in lines:
            s = l.strip()
            if not s: continue
            if 'if ' in s or 'elif ' in s: if_branches += 1
            if 'for ' in s and ' in ' in s: for_loops += 1
            if 'while ' in s: while_loops += 1
            if s.startswith('try:') or 'except' in s: try_catch += 1
            if s == 'pass' or ' pass ' in s: pass_stubs += 1
            if 'todo' in s.lower() or 'fixme' in s.lower(): todo_stubs += 1
            if 'shell=True' in s or 'os.system(' in s or 'subprocess.call(' in s: command_injections += 1
    else:
        for l in lines:
            s = l.strip()
            if not s: continue
            if 'if (' in s or 'if(' in s or 'else if' in s: if_branches += 1
            if 'for (' in s or 'for(' in s: for_loops += 1
            if 'while (' in s or 'while(' in s: while_loops += 1
            if 'try {' in s or 'catch (' in s: try_catch += 1
            if 'todo' in s.lower() or 'fixme' in s.lower() or 'unimplemented' in s.lower(): todo_stubs += 1
            if 'Runtime.getRuntime().exec' in s or 'ProcessBuilder' in s: command_injections += 1

    cyclomatic_complexity = 1 + if_branches + for_loops + while_loops + try_catch

    return {
        "loc": physical_loc,
        "total_lines": total_lines,
        "cyclomatic_complexity": cyclomatic_complexity,
        "max_nesting_depth": max_nesting_depth,
        "mean_nesting_depth": round(mean_nesting_depth, 2),
        "command_injections": command_injections,
        "hardcoded_secrets": hardcoded_secrets,
        "pass_stubs": pass_stubs,
        "todo_stubs": todo_stubs
    }

def run_layer2(limit_per_lang=30000):
    print("=== LAYER 2: Static/Syntactic Analysis Agent (Classical Full-Scale Pass) ===")
    results = {}

    for path, lang in [(PYTHON_PATH, "python"), (JAVA_PATH, "java")]:
        if not os.path.exists(path):
            continue

        print(f"Executing Layer 2 Classical Static Pass on {lang.upper()} dataset...")
        groups = ["human", "chatgpt", "dsc", "qwen"]
        metrics = {g: {"loc": [], "cyclomatic_complexity": [], "max_nesting_depth": [], "command_injections": [], "hardcoded_secrets": [], "todo_stubs": []} for g in groups}

        count = 0
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip(): continue
                try: rec = json.loads(line)
                except: continue

                for g_name, code_key in [("human", "human_code"), ("chatgpt", "chatgpt_code"), ("dsc", "dsc_code"), ("qwen", "qwen_code")]:
                    code = rec.get(code_key, "")
                    feat = static_analyze_code(code, lang)
                    if feat is None: continue
                    for k in metrics[g_name].keys():
                        metrics[g_name][k].append(feat[k])

                count += 1
                if limit_per_lang and count >= limit_per_lang:
                    break

        lang_sum = {"record_count": count, "snippet_count": count * 4, "groups": {}}
        for g in groups:
            lang_sum["groups"][g] = {}
            for k in metrics[g].keys():
                arr = np.array(metrics[g][k])
                lang_sum["groups"][g][k] = {
                    "mean": round(float(np.mean(arr)), 2),
                    "median": round(float(np.median(arr)), 2),
                    "p95": round(float(np.percentile(arr, 95)), 2)
                }

        results[lang] = lang_sum
        print(f"Layer 2 complete for {lang.upper()} ({count:,} tasks / {count*4:,} snippets).")

    os.makedirs(os.path.dirname(OUTPUT_LAYER2_PATH), exist_ok=True)
    with open(OUTPUT_LAYER2_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_layer2()

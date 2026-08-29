import os
import json
import re
import numpy as np

PYTHON_PATH = "/home/hassan/Desktop/zenodo_data/python_dataset.jsonl"
JAVA_PATH = "/home/hassan/Desktop/zenodo_data/java_dataset.jsonl"
OUTPUT_LAYER3_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer3_stylometric_extraction.json"

def stylometric_extract_code(code, lang="python"):
    if not code or not isinstance(code, str):
        return None

    lines = code.split('\n')
    total_lines = len(lines)
    non_empty = [l for l in lines if l.strip()]
    loc = len(non_empty)
    if total_lines == 0 or loc == 0: return None

    blank_lines = total_lines - loc
    whitespace_pct = round((blank_lines / total_lines * 100), 2)

    words = re.findall(r'\b[A-Za-z_]\w*\b', code)
    identifiers = [w for w in words if not w.isupper()]
    single_char_vars = sum(1 for w in identifiers if len(w) == 1 and w.isalpha())
    mean_var_len = float(np.mean([len(w) for w in identifiers])) if identifiers else 0.0
    snake_case_vars = sum(1 for w in identifiers if '_' in w and w.islower())
    camel_case_vars = sum(1 for w in identifiers if not '_' in w and any(c.isupper() for c in w[1:]))

    comment_lines = 0
    docstring_present = 0
    func_count = 0
    list_comps = 0
    lambdas = 0

    if lang == "python":
        if '"""' in code or "'''" in code: docstring_present = 1
        for l in lines:
            s = l.strip()
            if not s: continue
            if s.startswith('#'): comment_lines += 1
            if s.startswith('def '): func_count += 1
            if '[' in s and ' for ' in s and ' in ' in s and ']' in s: list_comps += 1
            if 'lambda ' in s: lambdas += 1
    else:
        if '/*' in code or '/**' in code: docstring_present = 1
        for l in lines:
            s = l.strip()
            if not s: continue
            if s.startswith('//') or s.startswith('*') or s.startswith('/*'): comment_lines += 1
            if ('public ' in s or 'private ' in s or 'static ' in s) and '(' in s and ')' in s and not s.endswith(';'): func_count += 1
            if '->' in s: lambdas += 1

    comment_density = round((comment_lines / loc * 100), 2)

    return {
        "whitespace_pct": whitespace_pct,
        "comment_density": comment_density,
        "docstring_present": docstring_present,
        "mean_var_len": round(mean_var_len, 2),
        "single_char_vars": single_char_vars,
        "snake_case_vars": snake_case_vars,
        "camel_case_vars": camel_case_vars,
        "func_count": func_count,
        "list_comps": list_comps,
        "lambdas": lambdas
    }

def run_layer3(limit_per_lang=30000):
    print("=== LAYER 3: Stylometric Feature Extraction Agent (Classical Full-Scale Pass) ===")
    results = {}

    for path, lang in [(PYTHON_PATH, "python"), (JAVA_PATH, "java")]:
        if not os.path.exists(path):
            continue

        print(f"Executing Layer 3 Stylometric Extraction on {lang.upper()} dataset...")
        groups = ["human", "chatgpt", "dsc", "qwen"]
        metrics = {g: {"whitespace_pct": [], "comment_density": [], "docstring_present": [], "mean_var_len": [], "single_char_vars": [], "snake_case_vars": [], "camel_case_vars": [], "func_count": [], "list_comps": []} for g in groups}

        count = 0
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip(): continue
                try: rec = json.loads(line)
                except: continue

                for g_name, code_key in [("human", "human_code"), ("chatgpt", "chatgpt_code"), ("dsc", "dsc_code"), ("qwen", "qwen_code")]:
                    code = rec.get(code_key, "")
                    feat = stylometric_extract_code(code, lang)
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
                    "median": round(float(np.median(arr)), 2)
                }

        results[lang] = lang_sum
        print(f"Layer 3 complete for {lang.upper()} ({count:,} tasks / {count*4:,} snippets).")

    os.makedirs(os.path.dirname(OUTPUT_LAYER3_PATH), exist_ok=True)
    with open(OUTPUT_LAYER3_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_layer3()

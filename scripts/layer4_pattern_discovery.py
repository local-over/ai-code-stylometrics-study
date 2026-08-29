import json
import re
import ast
import numpy as np
from collections import defaultdict, Counter

INPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/stratified_outliers.json"
OUTPUT_ANALYSIS_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer4_discovered_patterns.json"

def analyze_patterns():
    print("Loading stratified outliers...")
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} quadruplets.")

    results = {
        "python": defaultdict(lambda: defaultdict(int)),
        "java": defaultdict(lambda: defaultdict(int)),
        "total_counts": defaultdict(lambda: defaultdict(int)),
        "examples": defaultdict(list)
    }

    # Regex patterns
    step_comment_re = re.compile(r'(#|\/\/)\s*(Step\s*\d+|[0-9]+\.\s+|Phase\s*\d+|Initializ|Calculate|Process|Return)', re.IGNORECASE)
    temp_swap_re = re.compile(r'(\b\w+\b)\s*=\s*(\b\w+\b)\s*;?\s*(\b\w+\b)\s*=\s*(\b\w+\b)\s*;?\s*(\b\w+\b)\s*=\s*\1')
    tuple_unpack_re = re.compile(r'(\w+)\s*,\s*(\w+)\s*=\s*(\w+)\s*,\s*(\w+)')
    temp_staging_return_re = re.compile(r'(\w+)\s*=\s*[^;\n]+\n\s*return\s+\1\b')
    nested_list_aliasing_re = re.compile(r'\[\s*\[.*?\]\s*\]\s*\*\s*\w+|\[\s*[^\]]*?\s*\]\s*\*\s*\w+')
    defensive_null_check_re = re.compile(r'if\s*\(\s*\w+\s*==\s*null|if\s+\w+\s+is\s+None')
    bare_except_re = re.compile(r'except\s*(Exception)?:|catch\s*\(\s*Exception\s+\w+\s*\)')

    models = ['human_code', 'chatgpt_code', 'dsc_code', 'qwen_code']

    for rec in data:
        lang = rec.get("lang", "python")
        results["total_counts"][lang]["total"] += 1

        for model in models:
            code = rec.get(model, "")
            if not code:
                continue

            results["total_counts"][lang][model] += 1

            # 1. Procedural Comment Headers
            step_matches = step_comment_re.findall(code)
            if step_matches:
                results[lang]["procedural_comments"][model] += 1
                if len(results["examples"]["procedural_comments"]) < 5 and model == "chatgpt_code":
                    results["examples"]["procedural_comments"].append({
                        "lang": lang, "model": model, "code": code[:300]
                    })

            # 2. Temp Swapping vs Tuple Unpacking (Python)
            if lang == "python":
                if temp_swap_re.search(code):
                    results[lang]["temp_swap"][model] += 1
                if tuple_unpack_re.search(code):
                    results[lang]["tuple_unpack"][model] += 1

            # 3. Temp Staging Before Return (`res = expr; return res`)
            if temp_staging_return_re.search(code):
                results[lang]["temp_staging_return"][model] += 1
                if len(results["examples"]["temp_staging_return"]) < 5 and model in ["chatgpt_code", "dsc_code"]:
                    results["examples"]["temp_staging_return"].append({
                        "lang": lang, "model": model, "code": code[-300:]
                    })

            # 4. Nested List Aliasing / Multiplication (`[[]] * n`)
            if nested_list_aliasing_re.search(code):
                results[lang]["list_multiplication_aliasing"][model] += 1
                if len(results["examples"]["list_multiplication_aliasing"]) < 5:
                    results["examples"]["list_multiplication_aliasing"].append({
                        "lang": lang, "model": model, "code": code
                    })

            # 5. Defensive Null / None Validation at Start
            if defensive_null_check_re.search(code):
                results[lang]["defensive_null_checks"][model] += 1

            # 6. Broad Exception Catching (`except Exception:` / `catch (Exception e)`)
            if bare_except_re.search(code):
                results[lang]["broad_exception_catch"][model] += 1

    print("Pattern extraction complete. Saving summary...")
    with open(OUTPUT_ANALYSIS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Results summary:")
    for lang in ["python", "java"]:
        print(f"\n--- {lang.upper()} ---")
        total = results["total_counts"][lang]["total"]
        print(f"Total quadruplets: {total}")
        for pattern, mdict in results[lang].items():
            print(f"Pattern: {pattern}")
            for m, cnt in mdict.items():
                pct = (cnt / (results["total_counts"][lang][m] or 1)) * 100
                print(f"  {m}: {cnt} ({pct:.2f}%)")

if __name__ == "__main__":
    analyze_patterns()

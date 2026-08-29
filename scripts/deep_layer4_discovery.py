import json
import re
import ast
from collections import defaultdict

INPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/stratified_outliers.json"
OUTPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer4_deep_analysis.json"

def deep_analyze():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    examples = defaultdict(list)
    total_quads = {"python": 0, "java": 0}

    # Regex definitions for exact detection rules
    patterns_regex = {
        # 1. Procedural comment headers
        "procedural_comments": re.compile(r'(#|\/\/)\s*(Step\s*\d+|[0-9]+\.\s+|Phase\s*\d+|Step\s+[A-Z]|Initialize|Compute|Return the|Process the)', re.IGNORECASE),
        "numbered_step_comments": re.compile(r'(#|\/\/)\s*(Step\s*\d+|[0-9]+\.\s+)', re.IGNORECASE),
        
        # 2. Swapping & staging
        "temp_variable_swap": re.compile(r'(\b\w+\b)\s*=\s*(\b\w+\b)\s*;?\s*\n\s*\2\s*=\s*(\b\w+\b)\s*;?\s*\n\s*\3\s*=\s*\1'),
        "tuple_unpack_swap": re.compile(r'(\b\w+\b)\s*,\s*(\b\w+\b)\s*=\s*\2\s*,\s*\1'),
        "temp_staging_return": re.compile(r'(\b\w+\b)\s*=\s*[^;\n]+\n\s*return\s+\1\b'),
        
        # 3. Aliasing bugs & mutability
        "shallow_grid_multiplication": re.compile(r'\[\s*\[\s*0\s*\]\s*\*\s*\w+\s*\]\s*\*\s*\w+|\[\s*\[\s*None\s*\]\s*\*\s*\w+\s*\]\s*\*\s*\w+|\[\s*\[.*?\]\s*\]\s*\*\s*\w+'),
        
        # 4. Defensive guards
        "null_or_empty_head_guard": re.compile(r'if\s+(\b\w+\b)\s+is\s+None\s+or\s+len\(\1\)\s*==\s*0:|if\s*\(\s*(\b\w+\b)\s*==\s*null\s*\|\|\s*\2\.length\(\)\s*==\s*0\)', re.IGNORECASE),
        "defensive_guard_clause": re.compile(r'^\s*if\s+.*:\s*\n\s*return\b|^\s*if\s*\(.*\)\s*\{\s*return\b', re.MULTILINE),
        
        # 5. Type hints (Python)
        "python_type_annotations": re.compile(r'def\s+\w+\s*\(.*:\s*(int|str|List|Dict|Tuple|Optional|Any|bool).*?\)\s*->'),
        
        # 6. Range len iteration vs direct
        "range_len_iteration": re.compile(r'for\s+\w+\s+in\s+range\(\s*len\('),
        "enumerate_iteration": re.compile(r'for\s+\w+\s*,\s*\w+\s+in\s+enumerate\('),
        
        # 7. Docstring formatting
        "docstring_google_sphinx": re.compile(r'"""[\s\S]*?(Args:|Returns:|Parameters:|Raises:)[\s\S]*?"""'),
        
        # 8. Import overhead
        "typing_imports": re.compile(r'from\s+typing\s+import\s+'),
        "sys_import": re.compile(r'import\s+sys'),
    }

    models = ['human_code', 'chatgpt_code', 'dsc_code', 'qwen_code']

    for rec in data:
        lang = rec.get("lang", "python")
        total_quads[lang] += 1
        hm_id = rec.get("hm_index", 0)

        for model in models:
            code = rec.get(model, "")
            if not code: continue

            for pname, ptarget in patterns_regex.items():
                match = ptarget.search(code)
                if match:
                    metrics[lang][pname][model] += 1
                    
                    # Store up to 3 concrete quadruplet examples per pattern
                    if len(examples[pname]) < 3 and model in ['chatgpt_code', 'dsc_code', 'qwen_code']:
                        # Check if human code is available for comparison
                        examples[pname].append({
                            "hm_index": hm_id,
                            "lang": lang,
                            "model": model,
                            "matched_snippet": match.group(0),
                            "full_code_ai": code[:400],
                            "full_code_human": rec.get("human_code", "")[:400]
                        })

    print("Analysis finished. Saving detailed outputs...")
    summary = {
        "total_quadruplets": total_quads,
        "metrics": metrics,
        "examples": examples
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved summary to {OUTPUT_PATH}")

if __name__ == "__main__":
    deep_analyze()

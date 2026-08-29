import json

INPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/stratified_outliers.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find examples for key patterns
examples = {}

for rec in data:
    lang = rec.get("lang")
    hm = rec.get("human_code", "")
    cg = rec.get("chatgpt_code", "")
    ds = rec.get("dsc_code", "")
    qw = rec.get("qwen_code", "")

    # Pattern 1: Procedural Comments in Java / Python
    if "procedural_comments" not in examples and ("Step 1:" in cg or "Step 1:" in qw or "Step 1:" in ds or "// Step" in cg or "# Step" in cg):
        examples["procedural_comments"] = {
            "hm_index": rec.get("hm_index"),
            "lang": lang,
            "human": hm,
            "chatgpt": cg,
            "deepseek": ds,
            "qwen": qw
        }

    # Pattern 2: Type Annotations in Python
    if "type_annotations" not in examples and lang == "python" and "def " in cg and "->" in cg and "from typing import" in cg and "->" not in hm:
        examples["type_annotations"] = {
            "hm_index": rec.get("hm_index"),
            "lang": lang,
            "human": hm,
            "chatgpt": cg,
            "deepseek": ds,
            "qwen": qw
        }

    # Pattern 3: List Comprehension vs Imperative Loop in Python
    if "list_comp" not in examples and lang == "python" and "[" in hm and "for " in hm and "]" in hm and ".append(" in cg:
        examples["list_comp"] = {
            "hm_index": rec.get("hm_index"),
            "lang": lang,
            "human": hm,
            "chatgpt": cg,
            "deepseek": ds,
            "qwen": qw
        }

    # Pattern 4: Staging return vs Direct Return
    if "temp_return" not in examples and ("return res" in cg or "return result" in cg) and ("return " in hm and "res" not in hm):
        examples["temp_return"] = {
            "hm_index": rec.get("hm_index"),
            "lang": lang,
            "human": hm,
            "chatgpt": cg,
            "deepseek": ds,
            "qwen": qw
        }

    # Pattern 5: Enumerate vs range len
    if "enumerate" not in examples and lang == "python" and "enumerate(" in hm and "range(len(" in cg:
        examples["enumerate"] = {
            "hm_index": rec.get("hm_index"),
            "lang": lang,
            "human": hm,
            "chatgpt": cg,
            "deepseek": ds,
            "qwen": qw
        }

print(f"Extracted {len(examples)} quadruplet examples.")
with open("/home/hassan/Desktop/ai_code_stylometrics_study/dataset/extracted_quadruplet_examples.json", "w") as f:
    json.dump(examples, f, indent=2)


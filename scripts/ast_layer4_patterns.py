import json
import ast
from collections import defaultdict

INPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/stratified_outliers.json"
OUTPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/ast_layer4_results.json"

class ASTPatternVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stats = {
            "list_comps": 0,
            "dict_comps": 0,
            "set_comps": 0,
            "lambda_count": 0,
            "if_exp_count": 0, # Ternary
            "append_calls": 0,
            "type_comments": 0,
            "multi_assign": 0, # a = b = 0
            "var_name_lens": [],
            "single_char_vars": 0,
            "snake_case_vars": 0,
            "camel_case_vars": 0
        }

    def visit_ListComp(self, node):
        self.stats["list_comps"] += 1
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.stats["dict_comps"] += 1
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.stats["set_comps"] += 1
        self.generic_visit(node)

    def visit_Lambda(self, node):
        self.stats["lambda_count"] += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.stats["if_exp_count"] += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        if len(node.targets) > 1:
            self.stats["multi_assign"] += 1
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'append':
            self.stats["append_calls"] += 1
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Param)):
            name = node.id
            self.stats["var_name_lens"].append(len(name))
            if len(name) == 1:
                self.stats["single_char_vars"] += 1
            if '_' in name and not name.startswith('_'):
                self.stats["snake_case_vars"] += 1
            elif any(c.isupper() for c in name) and not name.isupper():
                self.stats["camel_case_vars"] += 1
        self.generic_visit(node)

def analyze_ast():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    models = ['human_code', 'chatgpt_code', 'dsc_code', 'qwen_code']
    ast_metrics = defaultdict(lambda: defaultdict(list))
    total_valid = defaultdict(int)

    for rec in data:
        if rec.get("lang") != "python":
            continue

        for model in models:
            code = rec.get(model, "")
            if not code: continue

            try:
                tree = ast.parse(code)
                visitor = ASTPatternVisitor()
                visitor.visit(tree)
                
                total_valid[model] += 1
                for k, v in visitor.stats.items():
                    if k == "var_name_lens":
                        avg_len = sum(v) / len(v) if v else 0
                        ast_metrics[model]["avg_var_len"].append(avg_len)
                    else:
                        ast_metrics[model][k].append(v)
            except Exception:
                continue

    summary = {}
    for model in models:
        summary[model] = {
            "valid_samples": total_valid[model],
            "total_list_comps": sum(ast_metrics[model]["list_comps"]),
            "avg_list_comps_per_func": sum(ast_metrics[model]["list_comps"]) / total_valid[model] if total_valid[model] else 0,
            "total_append_calls": sum(ast_metrics[model]["append_calls"]),
            "avg_append_calls_per_func": sum(ast_metrics[model]["append_calls"]) / total_valid[model] if total_valid[model] else 0,
            "total_ternary_ifexp": sum(ast_metrics[model]["if_exp_count"]),
            "total_lambdas": sum(ast_metrics[model]["lambda_count"]),
            "total_multi_assign": sum(ast_metrics[model]["multi_assign"]),
            "avg_var_length": sum(ast_metrics[model]["avg_var_len"]) / total_valid[model] if total_valid[model] else 0,
            "total_single_char_vars": sum(ast_metrics[model]["single_char_vars"]),
            "avg_single_char_vars_per_func": sum(ast_metrics[model]["single_char_vars"]) / total_valid[model] if total_valid[model] else 0,
            "snake_case_vars": sum(ast_metrics[model]["snake_case_vars"]),
            "camel_case_vars": sum(ast_metrics[model]["camel_case_vars"]),
        }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("AST Analysis finished:")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    analyze_ast()

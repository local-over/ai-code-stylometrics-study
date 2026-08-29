import json
import math
import re
import sys
import time
import numpy as np
from scipy import stats

def compile_detectors():
    """Compile optimized regex patterns for Python and Java candidate patterns."""
    py_patterns = {
        'procedural_headers': re.compile(
            r'^\s*#\s*(?:Step\s+\d+|[0-9]+\.|\=\=\=|---|Initialize|Process|Check|Return|Helper|Calculate|Step\s+[A-Z])',
            re.MULTILINE | re.IGNORECASE
        ),
        'temp_staging': re.compile(
            r'\b(?:temp|_temp|tmp|_tmp)\s*=\s*[\w\.\(\)]+;\s*[\w\.]+\s*=\s*[\w\.]+\s*;\s*[\w\.]+\s*=\s*(?:temp|_temp|tmp|_tmp)\b'
        ),
        'type_annotations': re.compile(
            r':\s*(?:int|str|float|bool|List|Dict|Tuple|Set|Any|Optional|Union)[\w\.\,\[\]\s]*|->\s*[\w\.\,\[\]\s]+'
        ),
        'defensive_guards': re.compile(
            r'^\s*if\s+(?:[\w\.]+\s+is\s+None|not\s+[\w\.]+)\s*:\s*return\b',
            re.MULTILINE
        ),
        'pass_todo_stubs': re.compile(
            r'^\s*pass\b|#\s*(?:TODO|FIXME|XXX)\b',
            re.MULTILINE
        ),
        'except_pass': re.compile(
            r'except\s*(?:Exception)?\s*:\s*(?:\n\s*)?pass\b'
        ),
        'single_char_vars': re.compile(
            r'\b[a-zA-Z]\b'
        )
    }
    
    java_patterns = {
        'procedural_headers': re.compile(
            r'^\s*(?://|/\*)\s*(?:Step\s+\d+|[0-9]+\.|\=\=\=|---|Initialize|Process|Check|Return|Helper|Calculate)',
            re.MULTILINE | re.IGNORECASE
        ),
        'null_guards': re.compile(
            r'^\s*if\s*\(\s*[\w\.]+\s*==\s*null\s*\)\s*(?:return|throw)\b',
            re.MULTILINE
        ),
        'redundant_alloc': re.compile(
            r'\bnew\s+(?:ArrayList|HashMap|HashSet|StringBuilder|String)\s*<[^>]*>\s*\('
        ),
        'catch_swallow': re.compile(
            r'catch\s*\(\s*(?:Exception|Throwable|RuntimeException)\s+\w+\s*\)\s*\{\s*\}'
        )
    }
    return py_patterns, java_patterns

def analyze_python_snippet(code, py_patterns):
    if not code:
        return None
    lines = code.split('\n')
    loc = len(lines)
    blank_lines = len([l for l in lines if not l.strip()])
    airiness = (blank_lines / loc * 100.0) if loc > 0 else 0.0
    
    has_proc = 1 if py_patterns['procedural_headers'].search(code) else 0
    has_temp = 1 if py_patterns['temp_staging'].search(code) else 0
    type_count = len(py_patterns['type_annotations'].findall(code))
    guard_count = len(py_patterns['defensive_guards'].findall(code))
    stub_count = len(py_patterns['pass_todo_stubs'].findall(code))
    except_pass_count = len(py_patterns['except_pass'].findall(code))
    single_char_count = len(py_patterns['single_char_vars'].findall(code))
    
    return {
        'loc': loc,
        'airiness': airiness,
        'procedural_headers': has_proc,
        'temp_staging': has_temp,
        'type_annotations': type_count,
        'defensive_guards': guard_count,
        'pass_todo_stubs': stub_count,
        'except_pass': except_pass_count,
        'single_char_vars': single_char_count
    }

def analyze_java_snippet(code, java_patterns):
    if not code:
        return None
    lines = code.split('\n')
    loc = len(lines)
    blank_lines = len([l for l in lines if not l.strip()])
    airiness = (blank_lines / loc * 100.0) if loc > 0 else 0.0
    
    has_proc = 1 if java_patterns['procedural_headers'].search(code) else 0
    null_guard_count = len(java_patterns['null_guards'].findall(code))
    alloc_count = len(java_patterns['redundant_alloc'].findall(code))
    catch_swallow_count = len(java_patterns['catch_swallow'].findall(code))
    
    return {
        'loc': loc,
        'airiness': airiness,
        'procedural_headers': has_proc,
        'null_guards': null_guard_count,
        'redundant_alloc': alloc_count,
        'catch_swallow': catch_swallow_count
    }

def compute_holm_bonferroni(p_vals):
    """Compute Holm-Bonferroni FWER adjusted p-values."""
    m = len(p_vals)
    sorted_indices = sorted(range(m), key=lambda i: p_vals[i])
    p_adj = [0.0] * m
    cum_max = 0.0
    for rank, idx in enumerate(sorted_indices):
        p_raw = p_vals[idx]
        adj = min(1.0, (m - rank) * p_raw)
        cum_max = max(cum_max, adj)
        p_adj[idx] = min(1.0, cum_max)
    return p_adj

def run_layer5_validation(py_dataset_path, java_dataset_path, max_records=None):
    start_time = time.time()
    py_patterns, java_patterns = compile_detectors()
    
    py_metrics = {'human': [], 'chatgpt': [], 'dsc': [], 'qwen': []}
    java_metrics = {'human': [], 'chatgpt': [], 'dsc': [], 'qwen': []}
    
    print(f"Ingesting and analyzing Python dataset: {py_dataset_path}...")
    with open(py_dataset_path, 'r', encoding='utf-8', errors='ignore') as f:
        count = 0
        for line in f:
            if not line.strip(): continue
            try:
                rec = json.loads(line)
            except:
                continue
            
            res_h = analyze_python_snippet(rec.get('human_code', ''), py_patterns)
            res_c = analyze_python_snippet(rec.get('chatgpt_code', ''), py_patterns)
            res_d = analyze_python_snippet(rec.get('dsc_code', ''), py_patterns)
            res_q = analyze_python_snippet(rec.get('qwen_code', ''), py_patterns)
            
            if res_h and res_c and res_d and res_q:
                py_metrics['human'].append(res_h)
                py_metrics['chatgpt'].append(res_c)
                py_metrics['dsc'].append(res_d)
                py_metrics['qwen'].append(res_q)
                count += 1
                if max_records and count >= max_records:
                    break
    
    print(f"Ingesting and analyzing Java dataset: {java_dataset_path}...")
    with open(java_dataset_path, 'r', encoding='utf-8', errors='ignore') as f:
        count = 0
        for line in f:
            if not line.strip(): continue
            try:
                rec = json.loads(line)
            except:
                continue
            
            res_h = analyze_java_snippet(rec.get('human_code', ''), java_patterns)
            res_c = analyze_java_snippet(rec.get('chatgpt_code', ''), java_patterns)
            res_d = analyze_java_snippet(rec.get('dsc_code', ''), java_patterns)
            res_q = analyze_java_snippet(rec.get('qwen_code', ''), java_patterns)
            
            if res_h and res_c and res_d and res_q:
                java_metrics['human'].append(res_h)
                java_metrics['chatgpt'].append(res_c)
                java_metrics['dsc'].append(res_d)
                java_metrics['qwen'].append(res_q)
                count += 1
                if max_records and count >= max_records:
                    break

    print(f"Processed {len(py_metrics['human'])} Python quadruplets and {len(java_metrics['human'])} Java quadruplets in {time.time() - start_time:.2f}s.")
    
    # Statistical computation engine
    results = {'python': {}, 'java': {}, 'fwer_summary': []}
    raw_p_values = []
    hypothesis_keys = []
    
    # Process Python Metrics
    py_metric_keys = list(py_metrics['human'][0].keys())
    for key in py_metric_keys:
        h_vals = np.array([d[key] for d in py_metrics['human']])
        c_vals = np.array([d[key] for d in py_metrics['chatgpt']])
        d_vals = np.array([d[key] for d in py_metrics['dsc']])
        q_vals = np.array([d[key] for d in py_metrics['qwen']])
        ai_pooled = np.concatenate([c_vals, d_vals, q_vals])
        
        # Frequencies (% containing > 0)
        h_freq = float(np.mean(h_vals > 0) * 100)
        c_freq = float(np.mean(c_vals > 0) * 100)
        d_freq = float(np.mean(d_vals > 0) * 100)
        q_freq = float(np.mean(q_vals > 0) * 100)
        ai_freq = float(np.mean(ai_pooled > 0) * 100)
        
        # Mann-Whitney U for Human vs Pooled AI
        u_stat, p_val = stats.mannwhitneyu(h_vals, ai_pooled, alternative='two-sided')
        n1, n2 = len(h_vals), len(ai_pooled)
        r_rb = 1.0 - (2.0 * u_stat / (n1 * n2))
        
        # Kruskal-Wallis H-test across Human, ChatGPT, DeepSeek, Qwen
        h_kw, p_kw = stats.kruskal(h_vals, c_vals, d_vals, q_vals)
        # KW across AI models
        h_kw_ai, p_kw_ai = stats.kruskal(c_vals, d_vals, q_vals)
        
        results['python'][key] = {
            'descriptive': {
                'human': {'mean': float(np.mean(h_vals)), 'std': float(np.std(h_vals)), 'median': float(np.median(h_vals)), 'freq_pct': h_freq},
                'chatgpt': {'mean': float(np.mean(c_vals)), 'std': float(np.std(c_vals)), 'median': float(np.median(c_vals)), 'freq_pct': c_freq},
                'dsc': {'mean': float(np.mean(d_vals)), 'std': float(np.std(d_vals)), 'median': float(np.median(d_vals)), 'freq_pct': d_freq},
                'qwen': {'mean': float(np.mean(q_vals)), 'std': float(np.std(q_vals)), 'median': float(np.median(q_vals)), 'freq_pct': q_freq},
                'pooled_ai': {'mean': float(np.mean(ai_pooled)), 'std': float(np.std(ai_pooled)), 'median': float(np.median(ai_pooled)), 'freq_pct': ai_freq}
            },
            'mann_whitney': {'u_stat': float(u_stat), 'p_val': float(p_val), 'r_rb': float(r_rb)},
            'kruskal_wallis': {'h_stat_4group': float(h_kw), 'p_val_4group': float(p_kw), 'h_stat_ai': float(h_kw_ai), 'p_val_ai': float(p_kw_ai)}
        }
        raw_p_values.append(p_val)
        hypothesis_keys.append(('python', key))
        
    # Process Java Metrics
    java_metric_keys = list(java_metrics['human'][0].keys())
    for key in java_metric_keys:
        h_vals = np.array([d[key] for d in java_metrics['human']])
        c_vals = np.array([d[key] for d in java_metrics['chatgpt']])
        d_vals = np.array([d[key] for d in java_metrics['dsc']])
        q_vals = np.array([d[key] for d in java_metrics['qwen']])
        ai_pooled = np.concatenate([c_vals, d_vals, q_vals])
        
        h_freq = float(np.mean(h_vals > 0) * 100)
        c_freq = float(np.mean(c_vals > 0) * 100)
        d_freq = float(np.mean(d_vals > 0) * 100)
        q_freq = float(np.mean(q_vals > 0) * 100)
        ai_freq = float(np.mean(ai_pooled > 0) * 100)
        
        u_stat, p_val = stats.mannwhitneyu(h_vals, ai_pooled, alternative='two-sided')
        n1, n2 = len(h_vals), len(ai_pooled)
        r_rb = 1.0 - (2.0 * u_stat / (n1 * n2))
        
        h_kw, p_kw = stats.kruskal(h_vals, c_vals, d_vals, q_vals)
        h_kw_ai, p_kw_ai = stats.kruskal(c_vals, d_vals, q_vals)
        
        results['java'][key] = {
            'descriptive': {
                'human': {'mean': float(np.mean(h_vals)), 'std': float(np.std(h_vals)), 'median': float(np.median(h_vals)), 'freq_pct': h_freq},
                'chatgpt': {'mean': float(np.mean(c_vals)), 'std': float(np.std(c_vals)), 'median': float(np.median(c_vals)), 'freq_pct': c_freq},
                'dsc': {'mean': float(np.mean(d_vals)), 'std': float(np.std(d_vals)), 'median': float(np.median(d_vals)), 'freq_pct': d_freq},
                'qwen': {'mean': float(np.mean(q_vals)), 'std': float(np.std(q_vals)), 'median': float(np.median(q_vals)), 'freq_pct': q_freq},
                'pooled_ai': {'mean': float(np.mean(ai_pooled)), 'std': float(np.std(ai_pooled)), 'median': float(np.median(ai_pooled)), 'freq_pct': ai_freq}
            },
            'mann_whitney': {'u_stat': float(u_stat), 'p_val': float(p_val), 'r_rb': float(r_rb)},
            'kruskal_wallis': {'h_stat_4group': float(h_kw), 'p_val_4group': float(p_kw), 'h_stat_ai': float(h_kw_ai), 'p_val_ai': float(p_kw_ai)}
        }
        raw_p_values.append(p_val)
        hypothesis_keys.append(('java', key))
        
    # Apply Holm-Bonferroni FWER correction
    adjusted_p_vals = compute_holm_bonferroni(raw_p_values)
    for idx, (lang, metric) in enumerate(hypothesis_keys):
        results[lang][metric]['mann_whitney']['p_adj'] = float(adjusted_p_vals[idx])
        results['fwer_summary'].append({
            'hypothesis': f"{lang}_{metric}",
            'raw_p': float(raw_p_values[idx]),
            'adj_p': float(adjusted_p_vals[idx]),
            'r_rb': float(results[lang][metric]['mann_whitney']['r_rb']),
            'significant': bool(adjusted_p_vals[idx] < 0.05)
        })
        
    return results

if __name__ == '__main__':
    py_path = '/home/hassan/Desktop/zenodo_data/python_dataset.jsonl'
    java_path = '/home/hassan/Desktop/zenodo_data/java_dataset.jsonl'
    
    res = run_layer5_validation(py_path, java_path)
    out_json = '/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer5_validation_results.json'
    with open(out_json, 'w') as f:
        json.dump(res, f, indent=2)
    print(f"Layer 5 validation complete! Results saved to {out_json}.")

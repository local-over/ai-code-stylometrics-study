import json
import math
import os
import re
import sys
import time
from multiprocessing import Pool
import numpy as np
from scipy import stats

# Precompile global regex patterns for worker processes
PY_PATTERNS = {
    'procedural_headers': re.compile(
        r'^\s*#\s*(?:Step\s+\d+|[0-9]+\.|\=\=\=|---|Initialize|Process|Check|Return|Helper|Calculate)',
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

JAVA_PATTERNS = {
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

def analyze_py_line(line):
    if not line.strip(): return None
    try:
        rec = json.loads(line)
    except:
        return None
        
    res = {}
    for role in ['human_code', 'chatgpt_code', 'dsc_code', 'qwen_code']:
        code = rec.get(role, '')
        if not code: return None
        lines = code.split('\n')
        loc = len(lines)
        blank = len([l for l in lines if not l.strip()])
        airiness = (blank / loc * 100.0) if loc > 0 else 0.0
        
        res[role] = {
            'loc': loc,
            'airiness': airiness,
            'procedural_headers': 1 if PY_PATTERNS['procedural_headers'].search(code) else 0,
            'temp_staging': 1 if PY_PATTERNS['temp_staging'].search(code) else 0,
            'type_annotations': len(PY_PATTERNS['type_annotations'].findall(code)),
            'defensive_guards': len(PY_PATTERNS['defensive_guards'].findall(code)),
            'pass_todo_stubs': len(PY_PATTERNS['pass_todo_stubs'].findall(code)),
            'except_pass': len(PY_PATTERNS['except_pass'].findall(code)),
            'single_char_vars': len(PY_PATTERNS['single_char_vars'].findall(code))
        }
    return res

def analyze_java_line(line):
    if not line.strip(): return None
    try:
        rec = json.loads(line)
    except:
        return None
        
    res = {}
    for role in ['human_code', 'chatgpt_code', 'dsc_code', 'qwen_code']:
        code = rec.get(role, '')
        if not code: return None
        lines = code.split('\n')
        loc = len(lines)
        blank = len([l for l in lines if not l.strip()])
        airiness = (blank / loc * 100.0) if loc > 0 else 0.0
        
        res[role] = {
            'loc': loc,
            'airiness': airiness,
            'procedural_headers': 1 if JAVA_PATTERNS['procedural_headers'].search(code) else 0,
            'null_guards': len(JAVA_PATTERNS['null_guards'].findall(code)),
            'redundant_alloc': len(JAVA_PATTERNS['redundant_alloc'].findall(code)),
            'catch_swallow': len(JAVA_PATTERNS['catch_swallow'].findall(code))
        }
    return res

def compute_holm_bonferroni(p_vals):
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

def run_multiprocess():
    t0 = time.time()
    num_workers = os.cpu_count() or 8
    print(f"Starting Layer 5 statistical validation using {num_workers} parallel workers...")
    
    py_path = '/home/hassan/Desktop/zenodo_data/python_dataset.jsonl'
    java_path = '/home/hassan/Desktop/zenodo_data/java_dataset.jsonl'
    
    # Process Python
    print(f"Reading {py_path}...")
    with open(py_path, 'r', encoding='utf-8', errors='ignore') as f:
        py_lines = f.readlines()
    print(f"Loaded {len(py_lines)} Python lines. Processing in parallel...")
    
    with Pool(num_workers) as pool:
        py_results = pool.map(analyze_py_line, py_lines, chunksize=1000)
    py_results = [r for r in py_results if r is not None]
    print(f"Parsed {len(py_results)} valid Python quadruplets.")
    
    # Process Java
    print(f"Reading {java_path}...")
    with open(java_path, 'r', encoding='utf-8', errors='ignore') as f:
        java_lines = f.readlines()
    print(f"Loaded {len(java_lines)} Java lines. Processing in parallel...")
    
    with Pool(num_workers) as pool:
        java_results = pool.map(analyze_java_line, java_lines, chunksize=1000)
    java_results = [r for r in java_results if r is not None]
    print(f"Parsed {len(java_results)} valid Java quadruplets.")
    
    # Aggregate data structures
    py_metrics = {'human': [], 'chatgpt': [], 'dsc': [], 'qwen': []}
    for item in py_results:
        py_metrics['human'].append(item['human_code'])
        py_metrics['chatgpt'].append(item['chatgpt_code'])
        py_metrics['dsc'].append(item['dsc_code'])
        py_metrics['qwen'].append(item['qwen_code'])
        
    java_metrics = {'human': [], 'chatgpt': [], 'dsc': [], 'qwen': []}
    for item in java_results:
        java_metrics['human'].append(item['human_code'])
        java_metrics['chatgpt'].append(item['chatgpt_code'])
        java_metrics['dsc'].append(item['dsc_code'])
        java_metrics['qwen'].append(item['qwen_code'])

    # Statistical computation engine
    final_output = {'python': {}, 'java': {}, 'fwer_summary': []}
    raw_p_values = []
    hypothesis_keys = []
    
    # Process Python Metrics
    py_keys = list(py_metrics['human'][0].keys())
    for key in py_keys:
        h_vals = np.array([d[key] for d in py_metrics['human']], dtype=float)
        c_vals = np.array([d[key] for d in py_metrics['chatgpt']], dtype=float)
        d_vals = np.array([d[key] for d in py_metrics['dsc']], dtype=float)
        q_vals = np.array([d[key] for d in py_metrics['qwen']], dtype=float)
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
        
        final_output['python'][key] = {
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
    java_keys = list(java_metrics['human'][0].keys())
    for key in java_keys:
        h_vals = np.array([d[key] for d in java_metrics['human']], dtype=float)
        c_vals = np.array([d[key] for d in java_metrics['chatgpt']], dtype=float)
        d_vals = np.array([d[key] for d in java_metrics['dsc']], dtype=float)
        q_vals = np.array([d[key] for d in java_metrics['qwen']], dtype=float)
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
        
        final_output['java'][key] = {
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
        
    adjusted_p_vals = compute_holm_bonferroni(raw_p_values)
    for idx, (lang, metric) in enumerate(hypothesis_keys):
        final_output[lang][metric]['mann_whitney']['p_adj'] = float(adjusted_p_vals[idx])
        final_output['fwer_summary'].append({
            'hypothesis': f"{lang}_{metric}",
            'raw_p': float(raw_p_values[idx]),
            'adj_p': float(adjusted_p_vals[idx]),
            'r_rb': float(final_output[lang][metric]['mann_whitney']['r_rb']),
            'significant': bool(adjusted_p_vals[idx] < 0.05)
        })
        
    out_json = '/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer5_validation_results.json'
    with open(out_json, 'w') as f:
        json.dump(final_output, f, indent=2)
    print(f"Layer 5 statistical validation completed in {time.time() - t0:.2f}s! Saved to {out_json}.")

if __name__ == '__main__':
    run_multiprocess()

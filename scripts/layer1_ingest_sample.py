import os
import json
import numpy as np
import time

PYTHON_PATH = "/home/hassan/Desktop/zenodo_data/python_dataset.jsonl"
JAVA_PATH = "/home/hassan/Desktop/zenodo_data/java_dataset.jsonl"
PRIMARY_OUTPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer1_stratified_samples.json"
METRICS_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer1_summary_metrics.json"

def process_ingestion_and_sampling():
    print("=== LAYER 1: Ingestion & Stratified Sampling Agent ===")
    t0 = time.time()
    all_samples = []
    summary = {}

    for path, lang in [(PYTHON_PATH, "python"), (JAVA_PATH, "java")]:
        t_start = time.time()
        records = []
        scores = []
        h_lens, c_lens, d_lens, q_lens = [], [], [], []

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue

                h_code = rec.get("human_code", "") or ""
                c_code = rec.get("chatgpt_code", "") or ""
                d_code = rec.get("dsc_code", "") or ""
                q_code = rec.get("qwen_code", "") or ""

                h_len, c_len, d_len, q_len = len(h_code), len(c_code), len(d_code), len(q_code)

                h_lens.append(h_len)
                c_lens.append(c_len)
                d_lens.append(d_len)
                q_lens.append(q_len)

                lens = [h_len, c_len, d_len, q_len]
                mean_len = float(np.mean(lens))
                std_dev = float(np.std(lens))
                cv = std_dev / (mean_len + 1e-5)

                rec_item = {
                    "hm_index": rec.get("hm_index"),
                    "lang": lang,
                    "docstring": rec.get("docstring", ""),
                    "human_code": h_code,
                    "chatgpt_code": c_code,
                    "dsc_code": d_code,
                    "qwen_code": q_code,
                    "outlier_score": round(cv, 4),
                    "h_len": h_len,
                    "c_len": c_len,
                    "d_len": d_len,
                    "q_len": q_len,
                    "mean_len": round(mean_len, 2),
                    "std_dev_len": round(std_dev, 2)
                }
                scores.append(cv)
                records.append(rec_item)

        t_end = time.time()
        dur = round(t_end - t_start, 2)
        scores_arr = np.array(scores)

        summary[lang] = {
            "total_tasks": len(records),
            "total_snippets": len(records) * 4,
            "ingestion_time_sec": dur,
            "outlier_score_mean": round(float(np.mean(scores_arr)), 4),
            "outlier_score_std": round(float(np.std(scores_arr)), 4),
            "outlier_score_median": round(float(np.median(scores_arr)), 4),
            "outlier_score_min": round(float(np.min(scores_arr)), 4),
            "outlier_score_max": round(float(np.max(scores_arr)), 4),
            "outlier_score_p90": round(float(np.percentile(scores_arr, 90)), 4),
            "outlier_score_p95": round(float(np.percentile(scores_arr, 95)), 4),
            "outlier_score_p99": round(float(np.percentile(scores_arr, 99)), 4),
            "avg_char_length": {
                "human": round(float(np.mean(h_lens)), 2),
                "chatgpt": round(float(np.mean(c_lens)), 2),
                "deepseek": round(float(np.mean(d_lens)), 2),
                "qwen": round(float(np.mean(q_lens)), 2)
            }
        }

        # Sort by outlier score descending
        records.sort(key=lambda x: x["outlier_score"], reverse=True)
        outliers = records[:1125]
        for r in outliers: r["sample_type"] = "outlier"

        remaining = records[1125:]
        ctrl_indices = np.linspace(0, len(remaining) - 1, 375, dtype=int)
        controls = [remaining[i] for i in ctrl_indices]
        for r in controls: r["sample_type"] = "control"

        lang_samples = outliers + controls
        all_samples.extend(lang_samples)
        print(f"{lang.upper()} ingested {len(records):,} records in {dur}s. Picked {len(outliers)} outliers and {len(controls)} controls.")

    os.makedirs(os.path.dirname(PRIMARY_OUTPUT_PATH), exist_ok=True)
    with open(PRIMARY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_samples, f)

    total_dur = round(time.time() - t0, 2)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "sample_count": len(all_samples), "total_time_sec": total_dur}, f, indent=2)

    print(f"Done! Saved {len(all_samples):,} stratified quadruplets in {total_dur}s.")
    return summary, all_samples

if __name__ == "__main__":
    process_ingestion_and_sampling()



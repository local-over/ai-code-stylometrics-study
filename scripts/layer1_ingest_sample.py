import os
import json
import numpy as np
import time

PYTHON_PATH = "/home/hassan/Desktop/zenodo_data/python_dataset.jsonl"
JAVA_PATH = "/home/hassan/Desktop/zenodo_data/java_dataset.jsonl"
PRIMARY_OUTPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer1_stratified_samples.json"
ALIAS_OUTPUT_PATH = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/stratified_outliers.json"

def process_ingestion_and_sampling(limit_per_lang=None):
    print("=== LAYER 1: Ingestion & Stratified Sampling Agent ===")
    t0 = time.time()
    all_stratified_samples = []
    dataset_summary = {}

    for path, lang in [(PYTHON_PATH, "python"), (JAVA_PATH, "java")]:
        if not os.path.exists(path):
            print(f"Dataset path {path} not found.")
            continue

        print(f"Ingesting {lang.upper()} dataset ({path})...")
        t_lang_start = time.time()
        rec_count = 0
        lang_records = []
        outlier_scores = []
        
        # Length accumulators
        h_lens, c_lens, d_lens, q_lens = [], [], [], []

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue

                rec_count += 1
                h_code = rec.get("human_code", "") or ""
                c_code = rec.get("chatgpt_code", "") or ""
                d_code = rec.get("dsc_code", "") or ""
                q_code = rec.get("qwen_code", "") or ""

                h_len = len(h_code)
                c_len = len(c_code)
                d_len = len(d_code)
                q_len = len(q_code)

                h_lens.append(h_len)
                c_lens.append(c_len)
                d_lens.append(d_len)
                q_lens.append(q_len)

                # Outlier score based on length divergence across models (CV = std / mean)
                lens = [h_len, c_len, d_len, q_len]
                mean_len = float(np.mean(lens))
                std_dev = float(np.std(lens))
                divergence_ratio = std_dev / (mean_len + 1e-5)

                rec["lang"] = lang
                rec["outlier_score"] = round(divergence_ratio, 4)
                rec["h_len"] = h_len
                rec["c_len"] = c_len
                rec["d_len"] = d_len
                rec["q_len"] = q_len
                rec["mean_len"] = round(mean_len, 2)
                rec["std_dev_len"] = round(std_dev, 2)

                outlier_scores.append(divergence_ratio)
                lang_records.append(rec)

                if limit_per_lang and rec_count >= limit_per_lang:
                    break

        t_lang_end = time.time()
        print(f"Loaded {len(lang_records):,} {lang.upper()} records in {t_lang_end - t_lang_start:.2f}s.")

        # Compute dataset stats
        scores_arr = np.array(outlier_scores)
        summary_stats = {
            "total_records": rec_count,
            "total_snippets": rec_count * 4,
            "ingestion_time_sec": round(t_lang_end - t_lang_start, 2),
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
        dataset_summary[lang] = summary_stats

        # Stratified sampling: 1,500 total per language (1,125 top outliers + 375 stratified controls)
        lang_records.sort(key=lambda x: x["outlier_score"], reverse=True)
        top_outliers = lang_records[:1125]
        for r in top_outliers:
            r["sample_type"] = "outlier"

        remaining_records = lang_records[1125:]
        indices = np.linspace(0, len(remaining_records) - 1, 375, dtype=int)
        controls = [remaining_records[i] for i in indices]
        for r in controls:
            r["sample_type"] = "control"

        lang_samples = top_outliers + controls
        all_stratified_samples.extend(lang_samples)

        print(f"Selected {len(lang_samples):,} stratified quadruplet records for {lang.upper()} (1,125 Outliers + 375 Controls).")

    # Save output
    for out_path in [PRIMARY_OUTPUT_PATH, ALIAS_OUTPUT_PATH]:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_stratified_samples, f)
        print(f"Saved {len(all_stratified_samples):,} stratified samples to {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")

    total_time = round(time.time() - t0, 2)
    print(f"=== Layer 1 Ingestion & Sampling Complete in {total_time}s ===")

    # Write execution summary JSON alongside
    summary_path = "/home/hassan/Desktop/ai_code_stylometrics_study/dataset/layer1_summary_metrics.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"summary": dataset_summary, "sample_count": len(all_stratified_samples), "total_time_sec": total_time}, f, indent=2)

    return dataset_summary, len(all_stratified_samples)

if __name__ == "__main__":
    process_ingestion_and_sampling()


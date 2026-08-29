import json
import os

def main():
    human_json_path = "/home/hassan/Desktop/tot/dataset_samples/dataset_2017_2019.json"
    ai_jsonl_path = "/home/hassan/Desktop/dataset.jsonl"
    
    master_json_path = "/home/hassan/Desktop/master_code_dataset.json"
    master_jsonl_path = "/home/hassan/Desktop/master_code_dataset.jsonl"
    
    master_records = []
    record_counter = 1

    # 1. Process Pre-AI Human Benchmark Dataset & AI Recreations
    if os.path.exists(human_json_path):
        with open(human_json_path, "r", encoding="utf-8") as f:
            human_flows = json.load(f)

        for flow_idx, flow in enumerate(human_flows):
            flow_id = f"flow_{flow_idx+1:02d}"
            title = flow.get("title", "")
            lang = flow.get("language", "")
            prompt = flow.get("english_prompt", "")
            source_proj = flow.get("source_project", "")
            pre_ai_date = flow.get("pre_ai_date", "")

            # Human code record
            human_code = flow.get("human_pre_ai_code", "")
            if human_code:
                human_record = {
                    "id": f"master_{record_counter:04d}",
                    "dataset_category": "human_vs_ai_benchmark",
                    "task_id": flow_id,
                    "title": title,
                    "tier": "Benchmark Flow",
                    "language": lang,
                    "task_prompt": prompt,
                    "author_type": "human",
                    "model": f"human_pre_ai ({source_proj})",
                    "run_id": 1,
                    "source_project": source_proj,
                    "pre_ai_date": pre_ai_date,
                    "code": human_code,
                    "line_count": len(human_code.split("\n")),
                    "actual_cost_usd": 0.0
                }
                master_records.append(human_record)
                record_counter += 1

            # AI recreation versions for the same human flow
            ai_vers = flow.get("ai_versions", {})
            for v_name, v_code in ai_vers.items():
                v_num = int(v_name.replace("version_", "")) if "version_" in v_name else 1
                ai_rec_record = {
                    "id": f"master_{record_counter:04d}",
                    "dataset_category": "human_vs_ai_benchmark",
                    "task_id": flow_id,
                    "title": title,
                    "tier": "Benchmark Flow",
                    "language": lang,
                    "task_prompt": prompt,
                    "author_type": "ai",
                    "model": f"ai_recreation_{v_name}",
                    "run_id": v_num,
                    "source_project": f"AI Blind Recreation of {source_proj}",
                    "pre_ai_date": None,
                    "code": v_code,
                    "line_count": len(v_code.split("\n")),
                    "actual_cost_usd": 0.0
                }
                master_records.append(ai_rec_record)
                record_counter += 1

    # 2. Process Research Tasks OpenRouter AI Dataset (112 generations)
    if os.path.exists(ai_jsonl_path):
        with open(ai_jsonl_path, "r", encoding="utf-8") as f:
            ai_lines = [json.loads(line) for line in f]

        for item in ai_lines:
            code = item.get("raw_output", "")
            ai_research_record = {
                "id": f"master_{record_counter:04d}",
                "dataset_category": "openrouter_ai_research_tasks",
                "task_id": item.get("task_id", ""),
                "title": f"{item.get('task_id', '').upper()} Code Generation",
                "tier": item.get("tier", "Tier 1"),
                "language": item.get("language", ""),
                "task_prompt": item.get("task_prompt", ""),
                "author_type": "ai",
                "model": item.get("model", ""),
                "run_id": item.get("run_id", 1),
                "source_project": "OpenRouter API Generation",
                "pre_ai_date": None,
                "code": code,
                "line_count": len(code.split("\n")),
                "actual_cost_usd": item.get("actual_cost_usd", 0.0)
            }
            master_records.append(ai_research_record)
            record_counter += 1

    # 3. Save Master JSON (pretty-printed JSON array)
    with open(master_json_path, "w", encoding="utf-8") as f:
        json.dump(master_records, f, indent=2)

    # 4. Save Master JSONL (JSON Lines format)
    with open(master_jsonl_path, "w", encoding="utf-8") as f:
        for rec in master_records:
            f.write(json.dumps(rec) + "\n")

    print(f"\n==========================================")
    print(f"Master Code Dataset Successfully Created!")
    print(f"Total Records: {len(master_records)}")
    print(f"Human Baseline Records: {sum(1 for r in master_records if r['author_type'] == 'human')}")
    print(f"AI Generation Records: {sum(1 for r in master_records if r['author_type'] == 'ai')}")
    print(f"Saved JSON Array: {master_json_path}")
    print(f"Saved JSON Lines: {master_jsonl_path}")
    print(f"==========================================")

if __name__ == "__main__":
    main()

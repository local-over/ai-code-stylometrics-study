import os
import json
import time
import urllib.request
import re

API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SYSTEM_PROMPT = "Write clean, production-quality code. Output only the code, no explanation."

HUMAN_JSON_PATH = "../dataset/human_pre_ai_baseline.json"
OUTPUT_JSON_PATH = "../dataset/human_ai_benchmark.json"

MODELS = [
    {
        "id": "google/gemini-3.5-flash",
        "name": "Gemini 3.5 Flash",
        "reasoning": {"effort": "minimal"}
    },
    {
        "id": "openai/gpt-5.6-sol",
        "name": "GPT-5.6 Sol",
        "reasoning": {"effort": "none"}
    },
    {
        "id": "anthropic/claude-sonnet-4.6",
        "name": "Claude Sonnet 4.6"
    }
]

def strip_code_fences(text):
    if not text:
        return ""
    pattern = r"```(?:[a-zA-Z0-9_+-]+)?\n?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return "\n\n".join(m.strip() for m in matches)
    return text.strip()

def call_openrouter(model_cfg, prompt, language):
    model_id = model_cfg["id"]
    full_prompt = f"Language: {language}\n\nTask: {prompt}"
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 800
    }
    if "reasoning" in model_cfg:
        payload["reasoning"] = model_cfg["reasoning"]
    
    req = urllib.request.Request(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://code-research.org",
            "X-Title": "Human vs AI Code Comparison"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
    
    content = res_data["choices"][0]["message"]["content"]
    usage = res_data.get("usage", {})
    cost = usage.get("cost", 0.003)
    return content, cost

def main():
    if not os.path.exists(HUMAN_JSON_PATH):
        print(f"Error: {HUMAN_JSON_PATH} not found.")
        return

    with open(HUMAN_JSON_PATH, "r", encoding="utf-8") as f:
        human_flows = json.load(f)

    benchmark_data = []
    total_cost = 0.0

    print(f"Generating AI recreations for {len(human_flows)} Human Benchmark Flows...")

    for idx, flow in enumerate(human_flows):
        flow_id = f"flow_{idx+1:02d}"
        title = flow.get("title", "")
        lang = flow.get("language", "")
        prompt = flow.get("english_prompt", "")
        human_code = flow.get("human_pre_ai_code", "")
        source_proj = flow.get("source_project", "")
        pre_ai_date = flow.get("pre_ai_date", "")

        flow_entry = {
            "flow_id": flow_id,
            "title": title,
            "language": lang,
            "source_project": source_proj,
            "pre_ai_date": pre_ai_date,
            "prompt": prompt,
            "human_code": human_code,
            "ai_models": {}
        }

        for model_cfg in MODELS:
            m_id = model_cfg["id"]
            m_name = model_cfg["name"]
            print(f"[{flow_id}] Generating {m_name} for '{title[:30]}...'...", end="", flush=True)
            try:
                raw_code, cost = call_openrouter(model_cfg, prompt, lang)
                clean_code = strip_code_fences(raw_code)
                total_cost += cost
                flow_entry["ai_models"][m_id] = {
                    "name": m_name,
                    "code": clean_code,
                    "cost": round(cost, 6)
                }
                print(f" DONE (${cost:.5f})")
                time.sleep(0.1)
            except Exception as e:
                print(f" ERROR: {e}")

        benchmark_data.append(flow_entry)

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    print(f"\n==========================================")
    print(f"Complete! Saved {len(benchmark_data)} flows to {OUTPUT_JSON_PATH}")
    print(f"Total spent on AI recreations: ${total_cost:.4f} USD")
    print(f"==========================================")

if __name__ == "__main__":
    main()

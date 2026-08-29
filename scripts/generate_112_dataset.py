import os
import json
import time
import urllib.request
import re

API_KEY = os.environ.get("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
SYSTEM_PROMPT = "Write clean, production-quality code. Output only the code, no explanation."

OUTPUT_JSONL = "../dataset/master_code_dataset.jsonl"
SUMMARY_JSON = "../dataset/summary.json"
COST_HARD_CAP = 0.595

TASKS = [
    {"id": "task_01", "tier": "Tier 1", "prompt": "Implement an LRU Cache data structure with get(key) and put(key, value) in O(1) time complexity."},
    {"id": "task_02", "tier": "Tier 1", "prompt": "Parse a multi-line string containing CSV data of users (id, name, email) and validate emails using strict regex."},
    {"id": "task_03", "tier": "Tier 1", "prompt": "Implement Dijkstra's algorithm to find the shortest path in a weighted graph from a start node to all nodes."},
    {"id": "task_04", "tier": "Tier 1", "prompt": "Implement a thread-safe Token Bucket rate limiter that allows up to N requests per second."},
    {"id": "task_05", "tier": "Tier 1", "prompt": "Implement the Shunting-Yard algorithm to convert an infix mathematical expression to postfix (RPN) and evaluate it."},
    {"id": "task_06", "tier": "Tier 1", "prompt": "Implement a Trie (Prefix Tree) with insert, search, and startsWith methods."},
    {"id": "task_07", "tier": "Tier 1", "prompt": "Find the longest palindromic substring in a given string in O(N^2) or better time complexity."},
    {"id": "task_08", "tier": "Tier 1", "prompt": "Given an array of interval tuples [start, end], merge all overlapping intervals and return the sorted result."},
    {"id": "task_09", "tier": "Tier 1", "prompt": "Search for a target value in a rotated sorted array in O(log N) time complexity."},
    {"id": "task_10", "tier": "Tier 1", "prompt": "Validate whether a string containing brackets '()[]{}' is balanced and properly nested."},
    {"id": "task_11", "tier": "Tier 1", "prompt": "Implement an exponential backoff with full jitter algorithm for retrying failed network requests."},
    {"id": "task_12", "tier": "Tier 2", "prompt": "Implement a custom Event Emitter class supporting on, off, once, and emit methods."},
    {"id": "task_13", "tier": "Tier 2", "prompt": "Implement an asynchronous task queue with concurrency limit C that processes tasks in FIFO order."},
    {"id": "task_14", "tier": "Tier 2", "prompt": "Implement an in-memory key-value store with Time-To-Live (TTL) expiration per key."}
]

LANGUAGES = ["python", "javascript"]

MODELS = [
    {
        "id": "google/gemini-3.5-flash",
        "name": "Gemini 3.5 Flash",
        "runs": 2,
        "reasoning": {"effort": "minimal"}
    },
    {
        "id": "openai/gpt-5.6-sol",
        "name": "GPT-5.6 Sol",
        "runs": 1,
        "reasoning": {"effort": "none"}
    },
    {
        "id": "anthropic/claude-sonnet-4.6",
        "name": "Claude Sonnet 4.6",
        "runs": 1
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

def call_openrouter(model_cfg, task, language):
    model_id = model_cfg["id"]
    full_prompt = f"Language: {language}\n\nTask: {task['prompt']}"
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 750
    }
    if "reasoning" in model_cfg:
        payload["reasoning"] = model_cfg["reasoning"]
    
    req = urllib.request.Request(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://code-research.org",
            "X-Title": "Code Research Benchmark"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    
    with urllib.request.urlopen(req) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
    
    content = res_data["choices"][0]["message"]["content"]
    usage = res_data.get("usage", {})
    cost = usage.get("cost", 0.0)
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    
    return content, cost, prompt_tokens, completion_tokens

def main():
    print("Dataset generation script loaded.")

if __name__ == "__main__":
    main()

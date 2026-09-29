"""Synthetic local Ollama probes. No agent tools, memory, or external messages."""

import argparse
import datetime
import json
import pathlib
import time
import urllib.request

CASES = [
    {
        "id": "exact_instruction",
        "prompt": "Return exactly ACK_PORTFOLIO and no other text.",
        "expected": "ACK_PORTFOLIO",
    },
    {
        "id": "strict_json",
        "prompt": 'Return only a JSON object, without Markdown or explanation. Use exactly these keys and values: ticket="T-29", status="READY", owner="Mira".',
        "expected": {"ticket": "T-29", "status": "READY", "owner": "Mira"},
    },
    {
        "id": "arithmetic",
        "prompt": "A team has 18 tasks. It completes 7 and then receives 4 new tasks. Return only the integer count remaining.",
        "expected": "15",
    },
    {
        "id": "native_tool",
        "prompt": "Look up ticket T-29 using the provided lookup_ticket tool. Do not invent its status.",
        "expected": {"ticket_id": "T-29"},
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "lookup_ticket",
                    "description": "Read a synthetic ticket by its exact ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {"ticket_id": {"type": "string"}},
                        "required": ["ticket_id"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
    },
]


def request(base, route, body=None, timeout=180):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        base + route, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--base-url", default="http://localhost:11434")
    ap.add_argument("--context", type=int, default=65536)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    report = {
        "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runtime": request(args.base_url, "/api/version"),
        "context_requested": args.context,
        "temperature": 0,
        "think": False,
        "num_predict": 180,
        "trials_per_case": 1,
        "cases": CASES,
        "results": [],
    }
    for model in args.models:
        try:
            for case in CASES:
                body = {
                    "model": model,
                    "messages": [{"role": "user", "content": case["prompt"]}],
                    "stream": False,
                    "think": False,
                    "keep_alive": "5m",
                    "options": {
                        "temperature": 0,
                        "num_ctx": args.context,
                        "num_predict": 180,
                    },
                }
                if "tools" in case:
                    body["tools"] = case["tools"]
                started = time.perf_counter()
                try:
                    d = request(args.base_url, "/api/chat", body)
                    msg = d.get("message", {})
                    content = msg.get("content", "")
                    calls = msg.get("tool_calls", [])
                    if case["id"] == "strict_json":
                        try:
                            passed = json.loads(content) == case["expected"]
                        except ValueError:
                            passed = False
                    elif case["id"] == "native_tool":
                        passed = (
                            len(calls) == 1
                            and calls[0].get("function", {}).get("name")
                            == "lookup_ticket"
                            and calls[0].get("function", {}).get("arguments")
                            == case["expected"]
                        )
                    else:
                        passed = content.strip() == case["expected"]
                    ps = request(args.base_url, "/api/ps")
                    loaded = [
                        {
                            k: m.get(k)
                            for k in ["name", "size", "size_vram", "context_length"]
                        }
                        for m in ps.get("models", [])
                    ]
                    row = {
                        "model": model,
                        "case": case["id"],
                        "pass": passed,
                        "elapsed_seconds": round(time.perf_counter() - started, 3),
                        "content": content,
                        "tool_calls": calls,
                        "finish_reason": d.get("done_reason"),
                        "prompt_tokens": d.get("prompt_eval_count"),
                        "output_tokens": d.get("eval_count"),
                        "load_seconds": round(d.get("load_duration", 0) / 1e9, 3),
                        "generation_tokens_per_second": round(
                            d.get("eval_count", 0) / (d.get("eval_duration", 1) / 1e9),
                            2,
                        )
                        if d.get("eval_duration")
                        else None,
                        "loaded_runtime": loaded,
                    }
                except Exception as e:
                    row = {
                        "model": model,
                        "case": case["id"],
                        "pass": False,
                        "error": type(e).__name__,
                        "elapsed_seconds": round(time.perf_counter() - started, 3),
                    }
                report["results"].append(row)
                print(json.dumps(row), flush=True)
                pathlib.Path(args.output).write_text(
                    json.dumps(report, indent=2), encoding="utf-8"
                )
        finally:
            request(args.base_url, "/api/generate", {"model": model, "keep_alive": 0})


if __name__ == "__main__":
    main()

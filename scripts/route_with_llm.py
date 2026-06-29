#!/usr/bin/env python3
"""Model-in-the-loop skill router: ask an LLM which skill(s) would fire per prompt.

This implements layer-(A) STEP 3 of the testing playbook: give a model ONLY the
pre-load skill catalog (name + description) and a user prompt, and capture which
skill(s) it would invoke. The output JSONL (one line per trial) feeds straight
into evaluate_skill_triggers.py --predictions for precision/recall/F1/pass^k.

Defaults to the OpenAI-compatible DeepSeek endpoint via DEEPSEEK_BASE_URL /
DEEPSEEK_API_KEY, but works against any OpenAI-compatible chat API.

Usage:
  uv run scripts/route_with_llm.py --model deepseek-v4-pro --trials 3 \
      --out predictions.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate_skill_triggers import load_cases, load_skills  # noqa: E402


def build_system_prompt(skills: dict) -> str:
    """Render the skill catalog into the router's system instruction."""
    lines = [
        "You are the skill ROUTER for an AI coding agent. Before doing any task the",
        "agent sees this catalog of available skills (name + one-line description) and",
        "must decide which skill(s) to invoke. Invoking a skill loads its full",
        "instructions, so invoke only when the description genuinely matches the task.",
        "Invoking NONE is correct and common when no skill fits.",
        "",
        "CATALOG:",
    ]
    for name in sorted(skills):
        lines.append(f"- {name}: {skills[name].description}")
    lines += [
        "",
        "Decide which skill(s) you would invoke for the user's message. Prefer",
        'precision over recall. Reply with STRICT JSON only: {"skills": ["exact-name", ...]}.',
        'Use {"skills": []} when no skill should fire.',
    ]
    return "\n".join(lines)


def call_chat(base_url: str, api_key: str, model: str, system: str, user: str, temperature: float) -> str:
    """POST one OpenAI-compatible chat completion and return the raw content string."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def parse_skills(content: str, valid: set[str]) -> list[str]:
    """Extract a clean list of known skill names from the model's JSON reply."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        start, end = content.find("{"), content.rfind("}")
        data = json.loads(content[start : end + 1]) if start != -1 and end != -1 else {}
    raw = data.get("skills", []) if isinstance(data, dict) else []
    return [s for s in raw if isinstance(s, str) and s in valid]


def main(argv=None) -> int:
    """Route every golden case k times through the model and write predictions JSONL."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="deepseek-v4-pro")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-url-env", default="DEEPSEEK_BASE_URL")
    parser.add_argument("--api-key-env", default="DEEPSEEK_API_KEY")
    args = parser.parse_args(argv)

    base_url = os.environ[args.base_url_env]
    api_key = os.environ[args.api_key_env]
    skills = load_skills()
    cases = load_cases()
    valid = set(skills)
    system = build_system_prompt(skills)

    jobs = [(c, t) for c in cases for t in range(args.trials)]

    def run_one(job):
        """Route a single (case, trial) and return its prediction record."""
        case, _ = job
        try:
            content = call_chat(base_url, api_key, args.model, system, case.prompt, args.temperature)
            fired = parse_skills(content, valid)
            return {"id": case.id, "actual_skills": fired}
        except (urllib.error.URLError, KeyError, ValueError) as exc:
            return {"id": case.id, "actual_skills": [], "error": str(exc)[:120]}

    results = []
    errors = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_one, job): job for job in jobs}
        for done, future in enumerate(as_completed(futures), start=1):
            record = future.result()
            if "error" in record:
                errors += 1
            results.append(record)
            if done % 20 == 0:
                print(f"  {done}/{len(jobs)} routed ({errors} errors)", file=sys.stderr)

    args.out.write_text(
        "\n".join(json.dumps({"id": r["id"], "actual_skills": r["actual_skills"]}, ensure_ascii=False) for r in results)
        + "\n"
    )
    print(f"wrote {len(results)} predictions to {args.out} ({errors} errors) using {args.model}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

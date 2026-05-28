"""
Day 1 - LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1
"""

import os
import sys
import time
from typing import Any, Callable


COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


def _load_local_env() -> None:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def _get_openai_client():
    from openai import OpenAI

    _load_local_env()
    openai_key = os.getenv("OPENAI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    if openai_key:
        return OpenAI(api_key=openai_key), OPENAI_MODEL, OPENAI_MINI_MODEL
    if openrouter_key:
        return (
            OpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
            ),
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
        )

    if os.getenv("PYTEST_CURRENT_TEST"):
        return OpenAI(api_key="test-key"), OPENAI_MODEL, OPENAI_MINI_MODEL

    raise RuntimeError(
        "Missing API key. Create solution/.env with OPENAI_API_KEY or OPENROUTER_API_KEY."
    )


def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """Call the OpenAI Chat Completions API and return text plus latency."""
    client, default_model, _ = _get_openai_client()
    api_model = default_model if model == OPENAI_MODEL else model

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=api_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.perf_counter() - start

    content = response.choices[0].message.content or ""
    return content, max(latency, 1e-9)


def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """Call the OpenAI Chat Completions API using gpt-4o-mini."""
    _, _, mini_model = _get_openai_client()
    return call_openai(
        prompt,
        model=mini_model,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


def _estimate_output_cost(text: str, model: str) -> float:
    estimated_tokens = len(text.split()) / 0.75
    return estimated_tokens / 1000 * COST_PER_1K_OUTPUT_TOKENS[model]


def compare_models(prompt: str) -> dict:
    """Compare gpt-4o and gpt-4o-mini on the same prompt."""
    gpt4o_response, gpt4o_latency = call_openai(prompt, model=OPENAI_MODEL)
    mini_response, mini_latency = call_openai_mini(prompt)

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": _estimate_output_cost(gpt4o_response, OPENAI_MODEL),
    }


def streaming_chatbot() -> None:
    """Run an interactive streaming chatbot in the terminal."""
    client, default_model, _ = _get_openai_client()
    history: list[dict[str, str]] = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        messages = history[-6:]
        assistant_reply = ""

        stream = client.chat.completions.create(
            model=default_model,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=256,
            stream=True,
        )

        print("Assistant: ", end="", flush=True)
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            assistant_reply += delta
            print(delta, end="", flush=True)
        print()

        history.append({"role": "assistant", "content": assistant_reply})
        history = history[-6:]


def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """Call fn(), retrying failures with exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(base_delay * (2**attempt))

    raise last_error


def batch_compare(prompts: list[str]) -> list[dict]:
    """Run compare_models on each prompt in the list."""
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


def _truncate(text: Any, width: int = 40) -> str:
    value = str(text)
    return value if len(value) <= width else value[: width - 3] + "..."


def format_comparison_table(results: list[dict]) -> str:
    """Format compare_models results as a readable text table."""
    headers = [
        "Prompt",
        "GPT-4o Response",
        "Mini Response",
        "GPT-4o Latency",
        "Mini Latency",
    ]
    rows = []
    for result in results:
        rows.append(
            [
                _truncate(result.get("prompt", "")),
                _truncate(result.get("gpt4o_response", "")),
                _truncate(result.get("mini_response", "")),
                f"{result.get('gpt4o_latency', 0):.3f}s",
                f"{result.get('mini_latency', 0):.3f}s",
            ]
        )

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    def format_row(row: list[str]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row))

    separator = "-+-".join("-" * width for width in widths)
    table = [format_row(headers), separator]
    table.extend(format_row(row) for row in rows)
    return "\n".join(table)


_PATCHABLE_MODULE_NAME = "day01_lab_solution"
sys.modules[_PATCHABLE_MODULE_NAME] = sys.modules[__name__]
for _fn in (
    call_openai,
    call_openai_mini,
    compare_models,
    streaming_chatbot,
    retry_with_backoff,
    batch_compare,
    format_comparison_table,
):
    _fn.__module__ = _PATCHABLE_MODULE_NAME


if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()

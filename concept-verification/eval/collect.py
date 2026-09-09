"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Workload collector."""

from __future__ import annotations

import argparse
import http.client
import json
import time
from pathlib import Path
from urllib.parse import urlparse

WORKLOADS = (
    (
        "slovenian-explanation",
        "V slovenščini na kratko razloži razliko med glagolskim vidom in časom.",
    ),
    ("slovenian-summary", "V dveh stavkih povzemite pomen varovanja izvirnega besedila."),
    (
        "technical-english",
        "Explain in English why a buffered response must preserve event ordering.",
    ),
    ("markdown-code", "Pripravi kratek Markdown primer s kodo, ki izpiše zdravo."),
    (
        "commands-paths",
        "Naštej varne, suhe ukaze za pregled poti /tmp/project brez izvajanja sprememb.",
    ),
    ("mixed-language", "Primerjaj izraza endpoint in končna točka v tehničnem besedilu."),
    (
        "tool-loop",
        "Predlagaj pregled datoteke v owned disposable directory, nato počakaj na orodje.",
    ),
    ("ordinary-coding", "V slovenščini opiši majhen test za nespremenjenost zaščitenih odsekov."),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=8)
    parser.add_argument("--proxy", default="http://127.0.0.1:18024/v1")
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    if not 1 <= args.cases <= 8:
        raise SystemExit("workload bound must be one through eight")
    parsed = urlparse(args.proxy)
    if parsed.hostname != "127.0.0.1":
        raise SystemExit("workload proxy must be loopback")
    args.results.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, object]] = []
    for name, prompt in WORKLOADS[: args.cases]:
        start = time.monotonic()
        record: dict[str, object] = {"id": name, "status": "BLOCKED", "human_label": ""}
        body = json.dumps(
            {
                "model": "qwen3.8-27b",
                "stream": True,
                "store": False,
                "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
            }
        ).encode()
        connection = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=args.timeout)
        try:
            connection.request(
                "POST",
                f"{parsed.path.rstrip('/')}/responses",
                body=body,
                headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
            )
            response = connection.getresponse()
            payload = response.read(8_000_001)
            if response.status == 200 and len(payload) <= 8_000_000:
                (args.results / f"{name}.sse").write_bytes(payload)
                record["status"] = "COMPLETED"
                record["bytes"] = len(payload)
            else:
                record["failure"] = "upstream_or_capture_failure"
        except (OSError, TimeoutError):
            record["failure"] = "external_endpoint_unavailable"
        finally:
            connection.close()
        record["latency_seconds"] = round(time.monotonic() - start, 6)
        summary.append(record)
    (args.results / "summary.json").write_text(
        json.dumps({"responses": summary, "human_review": "AWAITING_HUMAN_REVIEW"}, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "responses": len(summary),
                "completed": sum(item["status"] == "COMPLETED" for item in summary),
                "output": str(args.results / "summary.json"),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

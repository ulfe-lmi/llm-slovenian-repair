# Quickstart

This runs one synthetic Responses call through the local proxy. It assumes a
**configured lab instance**: the external statistics, the read-only SQLite index,
the mandatory pinned Pandoc, and your authorized Qwen endpoint. If you have not
installed those yet, follow **[INSTALL.md](INSTALL.md)** first — the steps below
reuse the same environment variables and paths.

A successful quickstart is a **completed** round trip. An answer that comes back
unchanged is a valid result: with no eligible suspicion the proxy makes zero
reviewer calls. The quickstart proves a working path, not an accepted correction
and not any linguistic quality.

## 1. Start the proxy in the foreground

From the repository root, in a dedicated Bash terminal:

```bash
set -euo pipefail
umask 077
export CONCEPT_INDEX="$HOME/.local/share/llm-slovenian-repair/data/index.sqlite"
export CONCEPT_PANDOC="$HOME/.local/share/llm-slovenian-repair/pandoc-3.7.0.2/bin/pandoc"
export CONCEPT_UPSTREAM_URL='https://YOUR-QWEN-HOST:PORT/v1'
export CONCEPT_REVIEWER_URL="$CONCEPT_UPSTREAM_URL"
export CONCEPT_REVIEWER_MODEL='qwen3.8-27b-rtx3090'
unset CONCEPT_REVIEWER_PROFILE CONCEPT_TRACE_DIR
read -r -s -p 'Reviewer API key: ' QWEN_API_KEY; printf '\n'; export QWEN_API_KEY
python3.12 -B concept-verification/proxy.py
```

The process stays in the foreground and listens at **`127.0.0.1:18024`**. Keep it
running in this terminal.

## 2. Send one synthetic request

In a **second** terminal, from the repository root:

```bash
python3.12 -B - <<'PY'
import getpass, json, urllib.error, urllib.request

payload = {
    "model": "qwen3.8-27b-rtx3090", "store": False, "stream": False,
    "max_output_tokens": 4096,
    "input": [{"role": "user", "content": [
        {"type": "input_text", "text": "Napiši en kratek stavek o sončnem dnevu."}
    ]}],
}
key = getpass.getpass("Main upstream API key: ")
request = urllib.request.Request(
    "http://127.0.0.1:18024/v1/responses",
    data=json.dumps(payload).encode(), method="POST",
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
)
try:
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)
except urllib.error.HTTPError as exc:
    raise SystemExit(f"Smoke failed: HTTP {exc.code}") from None
assert result.get("status") == "completed", "Upstream did not complete"
parts = [part for item in result.get("output", []) if item.get("type") == "message"
         for part in item.get("content", []) if part.get("type") == "output_text"]
assert parts and all(isinstance(part.get("text"), str) for part in parts)
assert all("logprobs" not in part for part in parts)
print("Quickstart passed: completed; output code points:",
      sum(len(p["text"]) for p in parts))
PY
```

## 3. What you are looking at

- **`status: "completed"`** — the upstream answer finished before any repair work.
- **No `logprobs` in the answer** — the proxy never returns token probabilities.
- **An unchanged answer is correct** — no eligible suspicion means zero reviewer
  calls and an answer text identical to the completed original; JSON/SSE metadata
  may still be normalized (for example defined `logprobs` removal).

Use `POST /v1/responses`, stateless text input and `store: false`. Chat
Completions, stored conversations and tools are outside the supported request
profile, and there is no health or models-list passthrough. See
**[INSTALL.md](INSTALL.md)** for the full setup and troubleshooting, and
**[ARCHITECTURE.md](ARCHITECTURE.md)** for what the proxy does with a response.

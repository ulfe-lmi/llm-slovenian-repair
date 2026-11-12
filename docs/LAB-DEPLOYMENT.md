# Runnable proxy: lab installation

Use this guide for the runnable proxy in `concept-verification/`, rather than
the historical research commands or the separate `src/` library scaffold.
Functional software and native Qwen compatibility are demonstrated in the
[current readiness audit](../oap/audit/results/036-current-functional-proxy-readiness-audit.md).
Linguistic benefit is unmeasured; no separate human evaluation dataset is required.
These instructions prepare a foreground, loopback-only lab instance. They do not
install a public service or change the model server, GPU, firewall or gateway.

## Prerequisites and locations

Use Linux x86-64, Bash, Python **3.12** with its standard-library SQLite module,
`curl`, `tar`, `sha256sum` and an existing Responses-compatible Qwen endpoint.
The pinned Pandoc installer below targets Linux amd64. The proxy itself needs no
third-party Python packages and no `pip install` of this repository.

For a new checkout:

```bash
git clone https://github.com/ulfe-lmi/llm-slovenian-repair.git
cd llm-slovenian-repair
```

Otherwise enter the existing repository root. Use a dedicated Bash terminal. All
following shell blocks run from that root in the same shell unless stated otherwise.
Do not enable shell tracing (`set -x`) when loading credentials.

```bash
set -euo pipefail
umask 077
export REPO_ROOT="$(pwd -P)"
export DATA_HOME="$HOME/.local/share/llm-slovenian-repair/data"
export PANDOC_HOME="$HOME/.local/share/llm-slovenian-repair/pandoc-3.7.0.2"
mkdir -p "$DATA_HOME"
python3.12 -B -c 'import sys, sqlite3; assert sys.version_info[:2] == (3, 12); print("Python", sys.version.split()[0], "SQLite", sqlite3.sqlite_version)'
```

Keep data, credentials and response captures outside the checkout. Use an owned
private directory, not a shared or symlinked destination. Record the deployed
revision with `git rev-parse HEAD`.

## Statistics: licence and exact downloads

**The real unigram, bigram and trigram statistics and the runtime SQLite index
are not bundled in Git.** The checked-in synthetic fixtures are not substitutes.
Both publisher records were checked on 2026-11-12 and identify **CC BY-SA 4.0**:

| Dataset | Authors | Publisher record |
| --- | --- | --- |
| Frequency lists of words from the Gigafida 2.0 corpus | Jaka Čibej, Špela Arhar Holdt, Kaja Dobrovoljc, Simon Krek | [CLARIN.SI 11356/1273](https://www.clarin.si/repository/xmlui/handle/11356/1273?show=full) |
| Frequency lists of word-level n-grams from the Gigafida 2.0 corpus | Jaka Čibej, Špela Arhar Holdt, Kaja Dobrovoljc, Simon Krek | [CLARIN.SI 11356/1274](https://www.clarin.si/repository/xmlui/handle/11356/1274?show=full) |

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) permits reuse,
including commercial reuse and redistribution, subject to attribution and its
other terms; adaptations distributed to others carry ShareAlike obligations.
It is not an Apache-style permissive licence. The project therefore keeps these
data external instead of bundling them under the code's Apache-2.0 licence.
Retain the dataset titles, authors, source links and licence with transferred
data. The SQLite import selects lowercase word-form and 2/3-gram tables and
builds a middle-word lookup; describe these transformations if sharing the index.
The code licence does not relicense these data. No Gigafida 2.2 query account or
Sloleks download is needed for this runnable proxy.

The following are the exact archives accepted by
[`config.py`](../concept-verification/config.py) and the importer. A changed
publisher artifact must be investigated rather than accepted by changing a hash.

| Archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `GF2.0-words-all.zip` | 115865656 | `77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a` |
| `GF2.0-word_sets.zip` | 22327366 | `782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40` |

Download once into the external directory. This refuses existing archive or
partial-file destinations, checks exact size and SHA-256 before renaming, and
does not extract the ZIPs. A failed download leaves only its named `.part` file;
inspect/remove that partial file before retrying.

```bash
fetch_statistics() {
    local name="$1" size="$2" digest="$3" url="$4"
    local part="$DATA_HOME/$name.part" final="$DATA_HOME/$name"
    if [ -e "$part" ] || [ -L "$part" ] || [ -e "$final" ] || [ -L "$final" ]; then
        printf 'Refusing existing destination: %s\n' "$name" >&2
        return 1
    fi
    curl --fail --silent --show-error --location \
      --proto '=https' --proto-redir '=https' \
      --connect-timeout 10 --max-time 600 --max-filesize "$size" \
      --output "$part" "$url"
    test "$(wc -c < "$part")" -eq "$size"
    printf '%s  %s\n' "$digest" "$part" | sha256sum --check --strict
    mv -- "$part" "$final"
}
fetch_statistics GF2.0-words-all.zip 115865656 \
  77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a \
  'https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1273/GF2.0-words-all.zip?sequence=4&isAllowed=y'
fetch_statistics GF2.0-word_sets.zip 22327366 \
  782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40 \
  'https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1274/GF2.0-word_sets.zip?sequence=1&isAllowed=y'
cp -- docs/LAB-DEPLOYMENT.md "$DATA_HOME/SOURCES-AND-INSTALLATION.md"
```

## Build and verify the runtime index

Build into a **new** output path. The importer clears tables in an existing
database, so the guard below deliberately refuses an existing output. It also
checks archive ownership, file type, link count, MD5/SHA-256, member identities
and source format. Do not unpack or edit the TSVs first.

```bash
export CONCEPT_INDEX="$DATA_HOME/index.sqlite"
if [ -e "$CONCEPT_INDEX" ] || [ -L "$CONCEPT_INDEX" ]; then
    printf 'Choose a new index path; the importer clears existing tables.\n' >&2
    exit 1
fi
python3.12 -B concept-verification/corpus.py prepare \
  --words-archive "$DATA_HOME/GF2.0-words-all.zip" \
  --ngrams-archive "$DATA_HOME/GF2.0-word_sets.zip" \
  --output "$CONCEPT_INDEX"
```

If an import fails, do not use its partial output. Inspect/remove only that new
output before retrying, or choose another new path; retain any previous working
index. `SOURCES-AND-INSTALLATION.md` alongside the data preserves this guide's
attribution and licence links.

Verify the prepared database without printing corpus rows:

```bash
python3.12 -B - <<'PY'
import os, sqlite3, sys
from pathlib import Path
sys.path.insert(0, "concept-verification")
from config import WORDS, NGRAMS, WORDS_MEMBER, BIGRAM_MEMBER, TRIGRAM_MEMBER

path = Path(os.environ["CONCEPT_INDEX"]).resolve(strict=True)
expected_counts = {"unigram": 141162, "bigram": 37720,
                   "trigram": 10930, "middle": 10930}
with sqlite3.connect(path.as_uri() + "?mode=ro", uri=True) as db:
    assert db.execute("PRAGMA quick_check").fetchone() == ("ok",)
    assert db.execute("PRAGMA journal_mode").fetchone() == ("delete",)
    counts = {table: db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
              for table in expected_counts}
    assert counts == expected_counts, counts
    meta = dict(db.execute("SELECT key, value FROM meta"))
    expected_meta = {
        "words_archive_sha256": WORDS.sha256,
        "ngrams_archive_sha256": NGRAMS.sha256,
        "words_member": WORDS_MEMBER, "bigram_member": BIGRAM_MEMBER,
        "trigram_member": TRIGRAM_MEMBER,
        "unigram_absence": "UNAVAILABLE", "ngram_absence": "CENSORED",
        "ngram_cutoff": "2 per million; denominator unknown",
    }
    assert all(meta.get(k) == v for k, v in expected_meta.items())
print("Verified runtime index:", counts)
PY
```

At runtime **only this SQLite file** is needed: `CONCEPT_INDEX` is its absolute
path, opened read-only for evidence lookup. The raw ZIPs may remain as installation
inputs outside Git. Alternatively, securely copy an already prepared index and
its source/licence notice from a trusted installation, then run the same checks.
Do not copy an active database or convert it to WAL mode; runtime rejects WAL
and does not create journal sidecars. Preserve a previous working index when
rebuilding; stop the proxy before replacing the selected database.

The selected word list is the publisher's `taxonomy-short` table. N-grams have
a 2-per-million publication cutoff with an unknown denominator. Missing words
are `UNAVAILABLE`; missing n-grams are `CENSORED`, **never exact zero**. These
are release-specific evidence tables, not an uncensored full-corpus denominator.

## Install mandatory Pandoc

```bash
bash concept-verification/install_pandoc.sh "$PANDOC_HOME"
export CONCEPT_PANDOC="$PANDOC_HOME/bin/pandoc"
"$CONCEPT_PANDOC" --version
```

The installer pins Pandoc **3.7.0.2**, archive size and SHA-256 in
[`pandoc-dependency.json`](../concept-verification/pandoc-dependency.json).
Startup checks version and positioned-JSON capability **before binding**.
No runtime download, historical-directory search or weaker parser fallback is
used. Corrections patch exact original spans; Pandoc never renders the answer.

## Configure and run in the foreground

Set both endpoint bases explicitly, including `/v1` once. Use your authorized
endpoint in place of the placeholder. The RTX 3090 model is the preferred lab
target; a server using another model ID needs that server's exact ID.

```bash
export CONCEPT_UPSTREAM_URL='https://YOUR-QWEN-HOST:PORT/v1'
export CONCEPT_REVIEWER_URL="$CONCEPT_UPSTREAM_URL"
export CONCEPT_REVIEWER_MODEL='qwen3.8-27b-rtx3090'
unset CONCEPT_REVIEWER_PROFILE CONCEPT_TRACE_DIR
export CONCEPT_USAGE_OBSERVER=stderr
read -r -s -p 'Reviewer API key: ' QWEN_API_KEY; printf '\n'
export QWEN_API_KEY
python3.12 -B concept-verification/proxy.py
```

The process remains in the foreground and listens at **`127.0.0.1:18024`**.
If that port is occupied, stop and identify its owner; do not kill another
service. To stop this instance, use Ctrl-C in its own terminal and wait for
owned-worker cleanup before restarting. No extra model process is launched.

There are **two authentication hops**. Incoming client `Authorization` is
forwarded to the main upstream. `QWEN_API_KEY` authenticates the isolated
reviewer call; it does not supply the main request's credentials. Use the same
authorized key for both only when the provider permits it. Keep keys out of
Git, command arguments, logs and committed environment files.

Tracing is disabled by leaving `CONCEPT_TRACE_DIR` unset. Setting it writes
full text and review material and is not part of this lab procedure.
`CONCEPT_USAGE_OBSERVER=stderr` emits bounded content-free usage records.
The reviewer whole-exchange timeout defaults to 15 seconds; set
`CONCEPT_REVIEWER_TIMEOUT` to a finite positive number of seconds before startup
if needed for a busy endpoint. It remains independent of the 30-second defaults
for upstream socket/body (`CONCEPT_TIMEOUT`), response headers
(`CONCEPT_HEADER_TIMEOUT`), upstream setup (`CONCEPT_SETUP_TIMEOUT`), incoming
request (`CONCEPT_REQUEST_TIMEOUT`) and final delivery (`CONCEPT_DELIVERY_TIMEOUT`).
Increasing one budget does not increase the others or enable retries.

## Owned synthetic smoke request

In a **second** terminal, from the checkout root, run this stdlib client. It
prompts for the main upstream key without echo, sends one project-authored text
request and prints only completion status and output length. No response file
or full-text log is created. Change `model` if your provider uses a different ID.

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
print("Smoke passed: completed; output code points:", sum(len(p["text"]) for p in parts))
PY
```

An unchanged answer is a valid result: no eligible suspicion means zero reviewer
calls. This smoke proves a completed round trip, not an accepted correction or
linguistic quality. Existing integration tests cover accepted edits and zero-review
paths; the readiness audit links bounded native evidence for both.

Use **POST `/v1/responses`**, stateless text input and `store:false`. The native
qualified profile uses message-array input and JSON output as above. Chat
Completions, stored conversations and tools are outside this proxy's supported
request profile; there is no health endpoint or models-list passthrough. Software
also supports the documented delayed SSE profile, which captures completion
before optional repair; it does not provide token-by-token delivery during generation.
See the [request contract](../concept-verification/responses_contract.py) for exact
request and envelope limits.

The proxy **does not provide token probabilities**: defined API `logprobs`
metadata is always removed. Even without repair, response JSON may change through
metadata removal while answer text remains identical. With repair, only approved
exact original text spans change. Citations, annotations, usage, IDs and completion
status retain their defined handling. Optional repair failure after safe main
completion returns the original text; main errors, malformed/incomplete responses,
capture-limit failures and cancellation retain failure semantics. A missing index
can cause repair to bypass rather than fail startup, so the index checks above
are essential before calling an instance ready.

For a client on another lab host, use an authenticated SSH tunnel to this
loopback listener under your normal lab access policy; do not change the proxy
to a public bind address. For example, on the client host:

```bash
ssh -N -L 18024:127.0.0.1:18024 YOUR-LAB-HOST
```

Then use the same local client URL, with an unused local port if necessary.

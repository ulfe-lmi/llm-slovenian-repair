# Installation

This prepares a **foreground, loopback-only** instance of the runnable proxy
in `concept-verification/`. It does not install a public service and does not
change the model server, GPU, firewall or gateway. For the shortest path to a first
request once this is set up, see **[QUICKSTART.md](QUICKSTART.md)**.

On this page: [Prerequisites](#prerequisites-and-locations) · [Statistics
and downloads](#statistics-licence-and-exact-downloads) · [Runtime
index](#build-and-verify-the-runtime-index) · [Pandoc](#install-mandatory-pandoc)
· [Configure and run](#configure-and-run-in-the-foreground) ·
[SSH tunnel](#remote-client-ssh-tunnel) · [Stopping](#stopping-the-instance) ·
[Upgrading](#upgrading) · [Recovery](#recovery) ·
[Troubleshooting](#troubleshooting)

## Prerequisites and locations

Use Linux x86-64, Bash, Python **3.12** with its standard-library SQLite module,
`curl`, `tar`, `sha256sum`, and an existing Responses-compatible Qwen endpoint.
The pinned Pandoc installer targets Linux amd64. The proxy itself needs no
third-party Python packages and no `pip install` of this repository.

For a new checkout:

```bash
git clone https://github.com/ulfe-lmi/llm-slovenian-repair.git
cd llm-slovenian-repair
```

Otherwise enter the existing repository root. Use a dedicated Bash terminal; all
shell blocks below run from that root in the same shell unless stated otherwise.
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

Keep data, credentials and response captures outside the checkout, in an owned
private directory (not a shared or symlinked destination). Record the deployed
revision with `git rev-parse HEAD`.

## Statistics: licence and exact downloads

**The real unigram, bigram and trigram statistics and the runtime SQLite index are
not bundled in Git.** The checked-in synthetic fixtures are not substitutes. Both
publisher records were checked on 2026-11-12 and identify **CC BY-SA 4.0**:

| Dataset | Authors | Publisher record |
| --- | --- | --- |
| Frequency lists of words from the Gigafida 2.0 corpus | Jaka Čibej, Špela Arhar Holdt, Kaja Dobrovoljc, Simon Krek | [CLARIN.SI 11356/1273](https://www.clarin.si/repository/xmlui/handle/11356/1273?show=full) |
| Frequency lists of word-level n-grams from the Gigafida 2.0 corpus | Jaka Čibej, Špela Arhar Holdt, Kaja Dobrovoljc, Simon Krek | [CLARIN.SI 11356/1274](https://www.clarin.si/repository/xmlui/handle/11356/1274?show=full) |

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) permits reuse,
including commercial reuse and redistribution, subject to attribution and its other
terms; adaptations distributed to others carry ShareAlike obligations. It is not an
Apache-style permissive licence, so the project keeps these data **external**
instead of bundling them under the code's Apache-2.0 licence. Retain the dataset
titles, authors, source links and licence with any transferred data. The SQLite
import selects the lowercase word-form and 2/3-gram tables and builds a middle-word
lookup; describe those transformations if you share the index. The code licence
does not relicense the data. No Gigafida 2.2 query account or Sloleks download is
needed for this proxy.

The following are the exact archives accepted by
[`config.py`](concept-verification/config.py) and the importer. A changed publisher
artifact must be investigated, not accepted by changing a hash.

| Archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `GF2.0-words-all.zip` | 115865656 | `77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a` |
| `GF2.0-word_sets.zip` | 22327366 | `782da9dd7909bfeefde5e7ee973b6031128167eec05868147d9dbfd22dc8cf40` |

Download once into the external directory. This refuses an existing archive or
partial-file destination, checks exact size and SHA-256 before renaming, and does
not extract the ZIPs. A failed download leaves only its named `.part` file; inspect
and remove that partial file before retrying.

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
cp -- INSTALL.md "$DATA_HOME/SOURCES-AND-INSTALLATION.md"
```

## Build and verify the runtime index

Build into a **new** output path. The importer clears tables in an existing
database, so the guard below deliberately refuses an existing output. It also
checks archive ownership, file type, link count, MD5/SHA-256, member identities and
source format. Do not unpack or edit the TSVs first.

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

If an import fails, do not use its partial output. Inspect and remove only that new
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
inputs outside Git. Alternatively, securely copy an already prepared index and its
source/licence notice from a trusted installation, then run the same checks. Do not
copy an active database or convert it to WAL mode; the runtime rejects WAL and does
not create journal sidecars. Preserve a previous working index when rebuilding, and
stop the proxy before replacing the selected database.

The selected word list is the publisher's `taxonomy-short` table. N-grams have a
2-per-million publication cutoff with an unknown denominator. Missing words are
`UNAVAILABLE`; missing n-grams are `CENSORED`, **never exact zero**. These are
release-specific evidence tables, not an uncensored full-corpus denominator.

## Install mandatory Pandoc

```bash
bash concept-verification/install_pandoc.sh "$PANDOC_HOME"
export CONCEPT_PANDOC="$PANDOC_HOME/bin/pandoc"
"$CONCEPT_PANDOC" --version
```

The installer pins Pandoc **3.7.0.2**, archive size and SHA-256 in
[`pandoc-dependency.json`](concept-verification/pandoc-dependency.json). Startup
checks the version and positioned-JSON capability **before binding**. There is no
runtime download, historical-directory search, or weaker parser fallback.
Corrections patch exact original spans; Pandoc never renders the answer.

## Configure and run in the foreground

Set both endpoint bases explicitly, including `/v1` once. Use your authorized
endpoint in place of the placeholder. The example below uses the RTX 3090 model
from the project's test environment; replace its model ID with the exact ID
provided by your server.

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
Set `CONCEPT_PORT` before launch to choose another port. The normal launcher
forwards other API traffic transparently and repairs only eligible completed
Responses text. See [proxy chaining](docs/PROXY-CHAINING.md) for a complete
`18023 → 18021` example, passthrough behavior and timeout settings.

There are **two authentication hops**. The incoming client `Authorization` is
forwarded to the main upstream. `QWEN_API_KEY` authenticates the isolated reviewer
call and does not supply the main request's credentials. Use the same authorized
key for both only when the provider permits it. Keep keys out of Git, command
arguments, logs and committed environment files.

Tracing is disabled by leaving `CONCEPT_TRACE_DIR` unset; setting it writes full
text and review material and is not part of this setup procedure.
`CONCEPT_USAGE_OBSERVER=stderr` emits bounded content-free usage records. The
six independent phase budgets below never extend one another, and none of them
enables retries. Set `CONCEPT_REVIEWER_TIMEOUT` to a finite positive number of
seconds before startup if needed for a busy endpoint.

| Phase | Variable | Default |
| --- | --- | ---: |
| Upstream socket/body capture | `CONCEPT_TIMEOUT` | 30 s |
| Response headers | `CONCEPT_HEADER_TIMEOUT` | 30 s |
| Upstream setup | `CONCEPT_SETUP_TIMEOUT` | 30 s |
| Incoming request intake | `CONCEPT_REQUEST_TIMEOUT` | 30 s |
| Final delivery | `CONCEPT_DELIVERY_TIMEOUT` | 30 s |
| Reviewer whole exchange | `CONCEPT_REVIEWER_TIMEOUT` | 15 s |

Send the first request from a second terminal, as in
**[QUICKSTART.md](QUICKSTART.md#2-send-one-synthetic-request)**.

## Remote client (SSH tunnel)

For a client on another host, use an authenticated SSH tunnel to this loopback
listener under your normal access policy; do not change the proxy to a public
bind address. On the client host:

```bash
ssh -N -L 18024:127.0.0.1:18024 YOUR-PROXY-HOST
```

Then use the same local client URL, with an unused local port if necessary.

## Stopping the instance

Use **Ctrl-C** in the proxy's own terminal and wait for the owned workers to finish
cleaning up before restarting. The proxy closes its listener, cancels and closes any
waiting accepted connections, and joins its owned workers on every exit path. No
extra model process is launched, so there is nothing else to stop. If the
`127.0.0.1:18024` port is already occupied, identify the service that owns it
(for example `ss -ltnp` on Linux); do not stop a service you do not own.

## Upgrading

1. Stop the proxy (Ctrl-C) and confirm the port is free.
2. Record the current revision with `git rev-parse HEAD`.
3. Update the checkout to the target revision.
4. Re-run the statistics and index steps **only if the data or importer changed**;
   otherwise keep the existing index. Rebuild into a new path and verify before
   switching `CONCEPT_INDEX`.
5. Re-run the Pandoc step only if the pinned version changed.
6. Restart the proxy and run the [quickstart](QUICKSTART.md) round trip.

## Recovery

- **Failed download** — a refused or failed fetch leaves only its `.part` file.
  Inspect and remove that partial file, then retry; do not delete a completed
  archive.
- **Failed index import** — do not use a partial database. Inspect and remove only
  that new output (or choose a new path) and retry; retain the previous working
  index.
- **Missing index at runtime** — a missing or incompatible index makes repair
  bypass rather than fail startup, so the instance can run with reduced capability.
  The index checks above are essential before calling an instance ready.
- **Wrong or absent Pandoc** — startup rejects the proxy before any traffic is
  accepted. Re-run the Pandoc step and confirm `$CONCEPT_PANDOC --version` prints
  `pandoc 3.7.0.2`.

## Troubleshooting

- **Port already in use** — first stop your own stale proxy if you have one
  (Ctrl-C in its terminal). If another service owns `127.0.0.1:18024`, identify
  and contact its owner; do not stop a service you do not own. The proxy
  binds a fixed loopback address, so do not change it to a public one.
- **Startup rejected** — the proxy checks Pandoc presence, exact version and
  positioned-JSON capability before binding, and validates the configuration
  defaults before any listener is created. A failure message names the finite
  reason; fix that specific cause.
- **A request returns `400`** — the request contract rejects unsupported
  capabilities (for example a request `logprobs` or `include` key) before any
  forward. Adjust the request to the supported text profile.
- **Answer unchanged** — expected when there is no eligible suspicion: zero
  reviewer calls. The returned answer text is identical to the completed
  original, while JSON/SSE metadata may still be normalized (for example
  defined `logprobs` removal).
- **A correction is not applied** — the review may decline a span, or the CPU
  evidence may be insufficient for it: that span is simply left unchanged while
  other independently accepted spans in the same answer are still applied. Only a
  technical failure or an unprovable composed validation mapping makes the
  whole optional pass fall back to the completed original; a rejected
  interacting conflict group reverts only its own spans while independently
  supported edits elsewhere are still applied. The proxy never masks a
  failure as a success.
- **Busy endpoint timeouts** — raise the specific `CONCEPT_*` budget for the phase
  that is timing out; the budgets are independent and none of them enables retries.

The proxy **does not provide token probabilities**: defined API `logprobs` metadata
is always removed, so even an unchanged answer may change through metadata removal
while the answer text stays identical. With a repair, only approved exact original
spans change. Citations, annotations, usage, IDs and completion status retain their
defined handling.

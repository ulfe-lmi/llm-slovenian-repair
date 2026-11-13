# Data sources

Acquisition boundaries, evidence semantics and the dated source inventory for
this project. For the **current runnable-proxy installation**, the canonical
procedure is the root [INSTALL.md](../INSTALL.md) — the one installation
recipe. [LAB-DEPLOYMENT.md](LAB-DEPLOYMENT.md) is a compatibility pointer to
that procedure. Real statistics are **not bundled** with the Apache-2.0 code.

## Current runtime data

- The proxy loads one **external read-only SQLite index** built from the two
  required Gigafida 2.0 archives (word lists + word n-grams, CC BY-SA 4.0).
- The archives and index are **external local data**: the project stores them
  outside the repository by design — a storage choice, not a confidentiality
  claim — and never stages, commits or packages them.
- Word absence is `UNAVAILABLE`. Missing n-grams are `CENSORED` with an unknown
  denominator, never exact zero; the published 2-per-million retention cutoff
  explains the censored missing entries but is not the context denominator
  itself.
- The Apache-2.0 code licence does not relicense external data; attribution and
  ShareAlike obligations remain on the data.

The dated inventory and objective-specific acquisition receipts below preserve
historical state; their `NOT_ACQUIRED` labels are historical objective state,
not current installation status.

## Dated source inventory

Committed snapshot observed 2026-09-08T09:13:23Z:
[source inventory](../resources/source-inventory-v1.json). It records three
publisher-labelled, derived ZIP artifacts and one Gigafida 2.2 query interface,
contains no source bytes, and grants no bulk/API access, redistribution, legal
or release decision.

- **Gigafida 2.0 word lists** — objective 006; published derived archive,
  `NOT_ACQUIRED`. Evidence boundary: word-list values can be exact only within
  the declared release/list/query scope after a controlled import.
- **Gigafida 2.0 word n-grams** — objective 007; published derived archive,
  `NOT_ACQUIRED`. Evidence boundary: the 2-per-million minimum makes missing
  entries `CENSORED`, never exact zero; retained n-grams are not a complete
  context denominator.
- **Sloleks 3.1** — objective 027; published derived archive,
  `NOT_ACQUIRED`. Evidence boundary: the lexical, frequency and morphology
  scope is distinct and cannot be silently combined with Gigafida.
- **Gigafida 2.2 query interface** — none, not a fallback;
  `UNKNOWN_UNVERIFIED`, no artifact. The page states provider-agreement terms;
  public interactive query access is not bulk/API or redistribution permission.

The first three records identify `CC BY-SA 4.0` publisher labels. The Apache-2.0
license for project code does not relicense external data. Attribution, ShareAlike
obligations, release packaging, compatible terms, and redistribution approval remain
separate review gates. The repository MD5 values are publisher transport metadata;
they are checked together with HTTPS and exact size, but are not project identity.
In the dated snapshot the project SHA-256 is null because no fetch had occurred at
observation time; that null is part of the frozen record — operators do not
mutate the snapshot after installation, and the current fixed hashes are in
[INSTALL.md](../INSTALL.md).

## Controlled offline verification

The executable boundary is `scripts/verify_source_artifact.py`. It validates the
inventory with only the Python standard library and, when explicitly given a local
regular ZIP, streams its exact size, publisher MD5, and project SHA-256. It inspects
member metadata without extraction, rejects unsafe names, duplicate/encrypted/
symlink/non-regular members, and applies source-specific member, total-size, and
compression-ratio limits. It emits only an ID, sizes, counts, and hashes. It never
opens an inventory URL, downloads, extracts, or writes an artifact.

Validate the committed metadata offline (Python 3.12 per
[DEVELOPMENT.md](DEVELOPMENT.md)):

```text
python3.12 scripts/verify_source_artifact.py \
  --inventory resources/source-inventory-v1.json --validate-only
```

### Historical objective-005 acquisition template (not a current prerequisite)

Under the historical objective-005 order, acquisition was an operator-controlled
manual step under that order's own authorization; the current installation does
not use it and has no such extra approval gate. The template below is preserved
from that procedure for inspection — it is not a command run by this project
or CI:

```text
selected_id='gigafida-2.0-words'
selected_url_and_size="$(python3.12 - "$selected_id" <<'PY'
import sys
from pathlib import Path

from scripts.verify_source_artifact import load_inventory

source_id = sys.argv[1]
inventory = load_inventory(Path("resources/source-inventory-v1.json"))
entry = next(item for item in inventory["entries"] if item["id"] == source_id)
artifact = entry["artifact"]
assert isinstance(artifact, dict)
print(artifact["url"], artifact["byte_size"], sep="\t")
PY
)"
IFS=$'\t' read -r selected_url selected_size <<< "$selected_url_and_size"
part_path="/owned/staging/${selected_id}.zip.part"
curl --fail --silent --show-error --location \
  --proto '=https' --proto-redir '=https' --connect-timeout 10 --max-time 600 \
  --max-filesize "$selected_size" --output "$part_path" "$selected_url"
python3.12 scripts/verify_source_artifact.py \
  --inventory resources/source-inventory-v1.json \
  --source-id "$selected_id" --artifact "$part_path"
# In that historical procedure the rename required the order's own authorization
# and a successful verification:
mv -- "$part_path" "/owned/staging/${selected_id}.zip"
```

The offline verifier checks the exact selected byte size and publisher MD5, and
emits the computed project SHA-256. Only a successful result with that recorded
SHA-256 could support a later import order. A failed or partial file must not be
renamed into an accepted location.
No source artifact was fetched, extracted, imported, or added to this repository
for objective 005.

## Evidence limits

The records preserve `EXACT`/`CENSORED`/`UNAVAILABLE` distinctions for later source
and query evidence. A publisher archive label is not a measurement of Slovenian
repair benefit, model compatibility, legal advice, release readiness, or deployment
authority. Real source bytes, raw samples, query results, credentials, and private
evaluation text remain outside Git and outside operational logs.

## Objective 006 importer boundary

The importer in `src/llm_slovenian_repair/unigram_importer.py` accepts a
caller-owned binary or text stream only; acquisition, ZIP verification, and
member selection remain outside its entry point. Version 1 is bound to the
lower-case form/lemma/POS member
`GF2.0-words-all-lowercase_forms-lemmas-parts_of_speech-taxonomy-entire.tsv`,
the 28-field all-quoted tab header, UTF-8, and CRLF. The header has no terminal
tab; each data row has either the 28 quoted fields ending immediately before CRLF
or those fields plus one empty terminal tab before CRLF, recorded as
`data_record_terminator=OPTIONAL_SINGLE_EMPTY_TAB_BEFORE_CRLF`. The optional tab
is not a semantic field; additional tabs, whitespace, or semantic fields are
rejected.
It reads incrementally under finite byte/row/line/field limits and emits immutable records plus a canonical
hash summary. Exact source fields are retained; `NFC_CASEFOLD` is an exposed
derived lookup transform. Counts are strict nonnegative integers, published
relative values use `Decimal` and their original text, and zero is accepted only
when the explicit query scope is complete. Source, query, and import completeness
are separate states, so a bounded prefix is never upgraded to a complete
vocabulary or denominator.

The checked-in `tests/fixtures/unigram/` data is project-authored synthetic data
under the repository `LICENSE`; it is not a Gigafida sample and is excluded from
the runtime package. The versioned receipts under
`resources/source-acquisitions/` preserve the 006-a recovery handoff and the
006-b controlled attempt, and the 006-c bounded corrective smoke. The former
blocked at the source-specific terminal tab. 006-c binds exactly one such tab
without admitting an optional 29th field, but its first-32-row structural sampler
stopped before importer execution. No external bytes or rows from those rounds
entered Git, the repository, the package or public records, and neither receipt
authorizes redistribution or a release claim.
Rounds 006-a through 006-l iterated that verifier-first boundary: the recovery
handoff and blocked real smoke (006-a/b/c), the content-free row-structure
classifier (006-d), the corrected 32-row stream routing (006-e), the
evidence-fixed optional single empty terminal tab (006-f), the bounded
prefix smoke with its blocked member access (006-g), the artifact-free
`--preflight` mode (006-h), the numeric syntax diagnostics (006-i/j), and the
cache promotion outside the repository and package with
`redistribution_ready=false` (006-k/l). The versioned receipts under
`resources/source-acquisitions/` and the immutable round reports under
`oap/reports/` are the authoritative record. No external bytes or rows entered
Git, the repository, the package or public records; 006-l expressly retained an
external canonical cache outside the repository for reuse, which is a storage
choice, not a redistribution. No receipt authorizes redistribution, release or
deployment.

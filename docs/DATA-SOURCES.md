# Data source inventory

The committed [source inventory](../resources/source-inventory-v1.json) is a dated
metadata snapshot observed at `2026-09-08T09:13:23Z`. It records three publisher-labelled,
derived ZIP artifacts and one Gigafida 2.2 query interface. It does not contain
source bytes, grant bulk/API access, settle redistribution, or authorize a legal
or release decision.

## Current inventory

| Source | Selected use | Access and state | Evidence boundary |
| --- | --- | --- | --- |
| Gigafida 2.0 word lists | Objective 006 | Published derived archive; `NOT_ACQUIRED` | Word-list values can be exact only within the declared release/list/query scope after a controlled import. |
| Gigafida 2.0 word n-grams | Objective 007 | Published derived archive; `NOT_ACQUIRED` | The 2-per-million minimum makes missing entries `CENSORED`, never exact zero; retained n-grams are not a complete context denominator. |
| Sloleks 3.1 | Objective 027 | Published derived archive; `NOT_ACQUIRED` | The lexical, frequency, and morphology scope is distinct and cannot be silently combined with Gigafida. |
| Gigafida 2.2 query interface | None; not a fallback | `UNKNOWN_UNVERIFIED`; no artifact | The page states provider-agreement terms. Public interactive query access is not bulk/API or redistribution permission. |

The first three records identify `CC BY-SA 4.0` publisher labels. The Apache-2.0
license for project code does not relicense external data. Attribution, ShareAlike
obligations, release packaging, compatible terms, and redistribution approval remain
separate review gates. The repository MD5 values are publisher transport metadata;
they are checked together with HTTPS and exact size, but are not project identity.
The inventory leaves project SHA-256 null until an operator performs a controlled
fetch and records the verifier result.

## Controlled offline verification

The executable boundary is `scripts/verify_source_artifact.py`. It validates the
inventory with only the Python standard library and, when explicitly given a local
regular ZIP, streams its exact size, publisher MD5, and project SHA-256. It inspects
member metadata without extraction, rejects unsafe names, duplicate/encrypted/
symlink/non-regular members, and applies source-specific member, total-size, and
compression-ratio limits. It emits only an ID, sizes, counts, and hashes. It never
opens an inventory URL, downloads, extracts, or writes an artifact.

Validate the committed metadata offline:

```text
python3.12 scripts/verify_source_artifact.py \
  --inventory resources/source-inventory-v1.json --validate-only
```

An operator-controlled acquisition, if separately authorized, is intentionally a
manual staging step. Resolve the selected URL and exact byte size from the canonical
inventory, write only to an owned `*.part` path, require HTTPS for the initial request
and redirects, and verify before accepting the file. The following is an inspectable
template, not a command run by this project or CI:

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
# Only after separate authorization and successful verification:
mv -- "$part_path" "/owned/staging/${selected_id}.zip"
```

The offline verifier checks the exact selected byte size and publisher MD5, and emits
the computed project SHA-256. Only a successful result with that recorded SHA-256 can
support a later import order. A failed or partial file must not be renamed into an
accepted location; the final `mv` remains separately authorized.
No source artifact was fetched, extracted, imported, or added to this repository for
objective 005.

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
stopped before importer execution. No external bytes or rows are retained, and
neither receipt authorizes redistribution or a release claim.
Round 006-d adds a content-free structural classifier and synthetic contract
tests. Its one verifier-first archive fetch passed exact artifact verification,
but the bounded member-prefix handoff failed before 32 complete rows reached the
classifier. The 006-d receipt records the exact archive/header identities,
`BLOCKED_ROW_DIAGNOSTIC_INPUT`, null aggregate diagnosis, no importer execution,
cleanup, and no retained source bytes. It does not select an importer format or
authorize redistribution.
Round 006-e corrects that handoff with a single public stream-routing boundary
and synthetic ZIP-member tests. Its one verifier-first fetch reached exactly 32
rows; the aggregate records 31 28-field rows and one empty terminal 29th field,
without retaining content or running an importer smoke. This remains bounded
format evidence, not importer compatibility or redistribution authorization.
Round 006-f supersedes the 006-c mandatory-tab documentation with the
evidence-fixed optional single empty terminal tab contract. Offline tests prove
both accepted shapes and reject wider extensions. Its one archive fetch passed
verification, but the bounded smoke harness failed before member access, so no
real importer compatibility evidence was obtained; neither it nor the earlier
structural sample is a full-source, linguistic-quality, rights, release, or
deployment claim.
Round 006-g adds `scripts/smoke_unigram_prefix.py` as the verifier-first
compatibility boundary. After successful canonical verification it opens the
selected member once, captures exactly 14 preamble lines, the 834-byte header,
and 32 data rows within a 4 MiB envelope, checks aggregate-only structure, and
calls the public importer twice on fresh streams. A successful result is only a
bounded prefix with `source/query=COMPLETE` and `import=PARTIAL`; it does not
retain source data or establish full archive import, lookup readiness, language
quality, rights, redistribution, release, deployment, or acceptance.
The one ordered 006-g GET passed canonical verification, but the committed CLI
stopped before member access because the direct interpreter could not resolve the
checkout `src` path. The helper now bootstraps that path and its offline contract
is green; the acquired tree was deleted with no retry, so the 006-g receipt keeps
member, structural, and importer observations null. This remains a blocked
compatibility attempt, not a full-source import or release/rights decision.
Round 006-h adds an artifact-free `--preflight` mode to close that invocation
boundary. It loads the canonical inventory entry, validates the exact 834-byte
header and 28-field count, constructs real source/query `COMPLETE` and import
`PARTIAL` provenance, and imports the public importer entry point and bounded
limits. Preflight and artifact arguments are mutually exclusive, and its `READY`
summary is limited to identities, counts, completeness, hashes, and contract
labels; it does not emit header or row content. The earlier system-Python
dependency failure remains historical evidence, not a readiness claim.
The exact 006-h preflight passed in an owned isolated environment. Its one direct
GET passed canonical verification and the bounded 32-row structural aggregate,
but the first real importer invocation stopped at `import-invalid-count`; the
helper made no second run or GET. Cleanup removed and verified the exact source
and environment, and the receipt records cumulative ten GETs, null importer
hashes, no retained source content, and no redistribution authorization.

Round 006-i adds a mutually exclusive numeric diagnostic path after the same
preflight, canonical verifier, selected-member capture, and structural aggregate.
It classifies the eight absolute-count and sixteen published-decimal columns into
a fixed closed syntax enum, counts current-parser-compatible cells by semantic
kind, and records the first incompatible row/column/category. The one diagnostic
profile covered 32 rows and 768 numeric cells; it observed 248 compatible count
cells and 4 compatible decimal cells, with the first incompatibility at row 1,
column 5 (`OTHER_ASCII`). The current importer was called exactly once and
returned `invalid-count:5`. These are content-free syntax observations: they do
not infer locale, grouping, numeric meaning, conversion, denominator completeness,
full-import compatibility, or redistribution authority. The 006-i receipt records
one GET (cumulative eleven), preserved 006-f/g/h failures, and exact cleanup.

Round 006-j keeps this verifier-first boundary and adds only content-free
row-1 refinement. Its fixed marker categories report 24 distinct
`ASCII_MIXED_OTHER` markers, no same-column recurrence, and column-specific
absolute/share/relative families. The first four identity fields produce a fixed
category/equality/NFC-casefold profile that is an outlier against rows 2–32; this
does not identify metadata, units, missing lexical values, or a permitted skip.
The helper then builds an in-memory envelope with the original preamble/header and
rows 2–32, invokes the unchanged importer exactly once with `max_rows=31`, and
records only the safe `invalid-decimal:6` boundary. One new direct GET brings the
cumulative objective-006 count to twelve. No source content is retained, and no
conversion, full import, rights, redistribution, release, or deployment claim is
made.

Round 006-k attempted to retain the verified archive in the owner-selected strategic
cache but stopped at the selected filesystem's hardlink boundary; its exact part was
removed and cumulative GETs reached thirteen. Round 006-l completes the handoff with
the cache outside the repository and package, fixed canonical names and source
identity, and promotion only after the existing inventory-bound ZIP verifier passes.
Plan and validation are network-free; promotion has no downloader and consumes one
caller-owned part through a lock-protected same-directory `os.replace`. The renamed
final is reopened, reverified, written with exclusive metadata, and inspected again.
One new GET brings cumulative objective-006 GETs to fourteen; two sequential
content-free diagnostic consumers reuse the same generation with three validations.
The receipt records the prior failure, exact generation, retention lifecycle, and
`redistribution_ready=false`.

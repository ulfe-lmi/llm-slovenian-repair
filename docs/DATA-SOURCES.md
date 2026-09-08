# Data source inventory

The committed [source inventory](../resources/source-inventory-v1.json) is a dated
metadata snapshot observed on 2026-09-08. It records three publisher-labelled,
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
manual staging step. Use an owned staging path, HTTPS-only redirects, a timeout and
the inventory's exact maximum, then verify before accepting the file. The following
is an inspectable template, not a command run by this project or CI:

```text
curl --fail --silent --show-error --location \
  --proto '=https' --proto-redir '=https' --connect-timeout 10 --max-time 600 \
  --output /owned/staging/source.zip 'PASTE_THE_INVENTORY_ARTIFACT_URL'
python3.12 scripts/verify_source_artifact.py \
  --inventory resources/source-inventory-v1.json \
  --source-id SELECTED_DOWNLOADABLE_SOURCE_ID \
  --artifact /owned/staging/source.zip
```

Only a successful verification result and its recorded SHA-256 can support a later
import order. A failed or partial file must not be renamed into an accepted location.
No source artifact was fetched, extracted, imported, or added to this repository for
objective 005.

## Evidence limits

The records preserve `EXACT`/`CENSORED`/`UNAVAILABLE` distinctions for later source
and query evidence. A publisher archive label is not a measurement of Slovenian
repair benefit, model compatibility, legal advice, release readiness, or deployment
authority. Real source bytes, raw samples, query results, credentials, and private
evaluation text remain outside Git and outside operational logs.

# Status

Bootstrap infrastructure is owner-published and accepted for continued development;
role operation is qualified and the development loop has been deliberately started.
Query current protocol state from `oap/active` or with
`python3 oap/bin/check_state.py --repo-root . --repository
ulfe-lmi/llm-slovenian-repair`. The first typed contract/policy seam is implemented:
strict frozen models represent original-coordinate spans, explicit evidence
uncertainty, narrow proposals, edits, results, and bounded v1 policy defaults.
Detection, review, acceptance, patching, and product functionality remain PLANNED,
linguistic
evaluation NOT RUN, Qwen compatibility UNVERIFIED, and ICA NOT RUN. Human
milestone acceptance is NONE; release and deployment approval are not established.
56 inert draft objectives are a coverage hypothesis. No completion percentage is
derived from generated files. The owner created `ulfe-lmi/llm-slovenian-repair`
and supplied the unchanged Apache License 2.0 LICENSE. Live repair testing is
disabled.

The source-manifest seam is implemented for objective 004: frozen manifests and
synthetic count records verify a bounded local JSON/JSONL payload with exact size
and SHA-256 checks. Manifest records use canonical fields, exact `UTF-8` and
matched JSON media/record formats; compatibility aliases are rejected. The
checked-in payload is project-authored synthetic fixture evidence only, scoped
to `local synthetic tests only`, with repository `LICENSE` terms,
`NOT_APPLICABLE_SYNTHETIC_FIXTURE` importer metadata, and corrected censored
wording: values at/below synthetic cutoff 4 are represented only by `[0,4]`.
No importer, real corpus bytes, external rights/access, linguistic benefit, or
source release facts are established.

Objective 005 records a dated metadata-only inventory in
[`resources/source-inventory-v1.json`](resources/source-inventory-v1.json) and a
standard-library offline ZIP verifier in
[`scripts/verify_source_artifact.py`](scripts/verify_source_artifact.py). Three
derived publisher archives are selected for future objectives 006, 007, and 027;
all remain `NOT_ACQUIRED`. Gigafida 2.2 is query-interface evidence only with
`UNKNOWN_UNVERIFIED` bulk/API and redistribution status. No source bytes were
downloaded, extracted, imported, or added to the package.

Objective 006 implements the bounded frozen `unigram_importer` parser for the
observed Gigafida 2.0 lower-case form/lemma/POS header. It retains exact 28
source fields and lossless numeric views, uses shared `EvidenceCompleteness`,
binds exact real versus project-synthetic provenance, preserves morphology
ambiguity, derives NFC/casefold lookup values without rewriting source text, and
rejects malformed UTF-8, controls, counts, zero-without-complete-query,
duplicates, bad quoting, truncation, and resource-limit violations. Objective-006
symbols are available only from the lazy submodule's `import_unigrams` seam. The
source format distinguishes the delimiter-free header from data rows with exactly
one terminal tab before CRLF (`TAB_BEFORE_CRLF`), consumed as a record terminator
and not a 29th field.

The 006-a recovery receipt remains a historical partial handoff with three prior
GETs and a false exact-one condition. The 006-b receipt records one verified GET,
accepted archive verification, and successful cleanup, but its bounded real smoke
is `BLOCKED`: the first data row has a trailing empty 29th field, outside the
exact 28-field parser contract. The 006-c receipt records one additional verified
GET and cleanup, but its bounded structural sample stopped before importer
execution on a row-shape mismatch. No real importer output, external archive, or
row is retained, committed, or packaged; real compatibility acceptance is not
claimed.
Round 006-d adds only a content-free, standard-library row classifier and
synthetic tests. Its single verifier-first fetch passed archive verification but
stopped before 32 complete member rows reached the classifier, so its receipt is
`BLOCKED_ROW_DIAGNOSTIC_INPUT` with null diagnosis aggregates and no importer
execution. No format correction or compatibility claim is made.
Round 006-e corrects that diagnostic prefix handoff with a public
`classify_stream` function, exact 15-line routing, and synthetic ZIP-member
coverage. Its one verifier-first fetch reached 32 rows and produced a
content-free aggregate: 31 rows had 28 fields and one had an empty terminal
29th field. This is bounded format evidence only; importer compatibility,
format correction, redistribution, release, and deployment remain unclaimed.
Round 006-g adds a verifier-first bounded prefix smoke helper and synthetic
contract suite. The helper opens the canonical member once, captures 14 preamble
lines plus the exact header and 32 rows within a 4 MiB envelope, checks the
aggregate without the optional parser probe, and runs two fresh public importer
calls under real `source/query=COMPLETE`, `import=PARTIAL` provenance. Real
acquisition evidence is not recorded until the one ordered fetch is performed;
full-source import, lookup readiness, linguistic benefit, rights, release,
deployment, and acceptance remain unclaimed.

Round 006-h adds the mutually exclusive `--preflight` CLI mode. It validates the
canonical inventory entry, the exact 834-byte/28-field header contract, and the
installed `import_unigrams` runtime plus bounded limits before any artifact is
opened. Its output is a finite `READY` summary with no header or row content.
The prior 006-g real attempt passed canonical verification but stopped before
member access because its direct system-Python invocation lacked the dependency
closure; the committed source-path correction did not alter that historical
result. A clean isolated preflight is now the required boundary before the one
remaining 006-h source action.

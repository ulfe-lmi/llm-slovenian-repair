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
result. The exact 006-h preflight then passed in its
lock-derived isolated environment; its one direct GET passed canonical
verification, prefix capture, and structural aggregation, but the first real
importer invocation stopped at `import-invalid-count`. The exact source and
environment were removed and verified absent, no retry occurred, and cumulative
objective-006 GETs are ten. Real importer compatibility remains blocked.

Round 006-i adds a mutually exclusive numeric diagnostic path to the committed
verifier-first helper. After the same canonical verification, one selected-member
capture, and the established 32-row structural aggregate, it profiles all 768
numeric cells across the eight absolute-count and sixteen published-decimal
columns using fixed syntax categories. The profile records 248/256 count cells
and 4/512 decimal cells accepted by the current parser, with the first bounded
incompatibility at row 1, column 5, category `OTHER_ASCII`; these are syntax
observations only and do not select locale, grouping, decimal, or conversion
semantics. One importer call then returned the safe `invalid-count:5` boundary.
The 006-i receipt records one GET (cumulative eleven), preserved prior failures,
exact cleanup, no retained source data, and no redistribution or compatibility
acceptance claim.

Round 006-j refines only the content-free numeric diagnostic. It classifies each
row-1 `OTHER_ASCII` marker into a fixed enum, reports distinctness and uniformity
within absolute/share/relative families, checks same-column recurrence, and profiles
the first four identity fields using fixed categories, equality partitions, and
NFC-casefold booleans. The observed 24 markers are all distinct
`ASCII_MIXED_OTHER` values, with no same-column recurrence; the row-1 identity
profile is an outlier and no row-role or unit meaning is selected. A fresh in-memory
envelope retaining the 14-line preamble and header but omitting row 1 made exactly
one importer call with `max_rows=31`, reaching `invalid-decimal:6`; the original
diagnostic call remains `invalid-count:5`. The 006-j receipt records one GET
(cumulative twelve), exact cleanup, no retained source data, and no redistribution,
full-import, conversion, release, or deployment authorization.

Round 006-k is the process-integrity correction. The executable report-history guard
scans all report paths through the selected Git revision, enforces add-once
report-only SELF ancestry, and returns an explicit
`KNOWN_HISTORICAL_VIOLATION_FROZEN` result for only the exact 006-a and 006-c
sequences. Transcript/report verification and the named `OAP report history` CI
check use the same guard; strategic review requires that check at the reviewed head.

The round adds an external objective-006 cache lifecycle with fixed names,
ownership/type/symlink/hardlink checks, canonical inventory verification, atomic
promotion, offline reuse, and gated cleanup. The cache is outside Git and the wheel;
receipts keep the twelve legacy GETs distinct from the current generations, record
network GET and consumer/revalidation counts, and retain redistribution as false.
006-k records the failed hardlink boundary at cumulative thirteen. 006-l completes
one same-directory rename-only promotion, two content-free diagnostic consumers and
three revalidations at cumulative fourteen, retaining the verified generation for
concept verification. Product numeric semantics remain unchanged and blocked; no
merge, release, deployment, or milestone acceptance is claimed.

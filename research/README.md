# Preserved Slovenian-repair research

This directory is the public, data-free research trail for objective 007. It
records the experiments that actually ran, the attempts that stopped, the
replacement/recovery executions, and the final local campaign. It is not the
production application, a linguistic acceptance claim, a replication claim, a
license grant, or permission to merge or deploy.

## Start here

- [`registry/experiments.json`](registry/experiments.json) is the evidence-backed
  catalog. Each record contains its question, authorized variation, frozen
  choices, status, safe numeric metrics, top-level private evidence identities,
  stable child-run/phase records, readable report/config links, conclusion, and
  pending evidence. A child status is never inferred from an old RUNNING snapshot.
- [`reports/`](reports/) and [`configs/`](configs/) contain one data-free,
  human-readable configuration/result projection per root, including recovery
  executions, stopped trials, campaign phases, audit views, and the diagnostic.
  Filled prompts, dataset/gold strings, response bodies, credentials, and private
  paths are excluded.
- [`registry/source-manifest.json`](registry/source-manifest.json) maps the actual
  frozen source closure to curated copies and records portability transformations.
- [`registry/file-census.json`](registry/file-census.json) summarizes the complete
  225,757-entry file census; exact SHA-256 entries are in
  [`registry/file-census.json.gz`](registry/file-census.json.gz). Dataset rows,
  traces, responses, indexes, archives, and credentials remain private-only.
- [`results/`](results/) contains deterministic gzip projections of the final
  campaign's per-case numeric metrics, category/type summaries, retry ablations,
  paired uncertainty, and the complete safe trial/case/phase projection in
  `study-evidence.json.gz`. Text, replacements, response bodies, and private
  result-path keys are removed by an allowlist.
- [`curated/`](curated/) contains faithful source seams: protected spans,
  Gigafida evidence states, the ASCII-hyphen detector view, English eligibility,
  contextual/retry schemas, initial-case restoration, unigram gating, exact
  patching, adapters, scoring, and offline replay boundaries.

## Timeline and catalog

The two 007-b recovery executions precede the isolated variants. The studies
retain scheduled, completed, and stopped trials separately. `full-hyphen-case-low`
is the one-way initial-case stage; the subsequent ten-run study is the symmetric
rule. The Levenshtein item is a single read-only diagnostic, not a benchmark.

| Record | Historical variation | Evidence status |
| --- | --- | --- |
| `007-b-replacement` | owner-authorized replacement execution | failed before proxy contact |
| `007-b-timeout300` | timeout-300 controlled replacement | controlled output preserved; case/trace association invalid |
| `nonthinking-mechanical` | direct reviewer, reasoning disabled | completed |
| `low-thinking-mechanical` | direct reviewer, low reasoning | completed |
| `high-thinking-mechanical` | direct reviewer, high reasoning | stopped |
| `xhigh-thinking-mechanical` | direct reviewer, xhigh reasoning | completed |
| `low-plus-validator` | frozen low pass plus validator | completed |
| `low-unigram-retry` | one contextual JSON unigram retry | completed |
| `low-word-only-retry` | stopped word-only retry and whitespace continuation | stopped/continued from saved response |
| `full-hyphen-space-low` | ASCII hyphen-to-space detector view | completed |
| `full-hyphen-case-low` | first one-way initial-case preservation | completed |
| `ten-run-initial-case-low` | ten symmetric initial-case trials | 8 complete, 2 stopped |
| `ten-run-expression-retry-low` | ten expression-retry trials | 9 complete, 1 stopped |
| `ten-run-english-preserve-low` | ten English-preservation trials | all 10 complete |
| `large-evaluation-capped` | capped external campaign preparation | inference started, not completed |
| `large-evaluation-uncapped` | owner-directed uncapped campaign | paused by human relevance change |
| `dassle-spelling-preparation` | DASSLE spelling preparation and controlled run | local evidence complete with incidents |
| `dassle-uv-audit` | exhaustive u/v audit and random-20 sample | complete mechanical audit |
| `full-campaign8` | final eight-worker A100 campaign | local campaign complete; remote scoring pending |
| `prijigrala-retry10` | one-target retry-limit-ten case | complete |
| `levenshtein-lookup-diagnostic` | one read-only lookup observation | not a benchmark |

The registry is the record for every root and its nested artifacts; it does not
flatten a stopped trial into a success. The private archive catalog records the
ten verified native relocations and reports zero source-byte deletions with no
remaining matching temporary roots.

One interrupted diagnostic shell briefly created four small OAP streams under
`/tmp`; strategy moved those exact files into the persistent private
`round-007-e-tmp/interrupted-tmp-diagnostics` record and verified all identified
temporary names absent. No dataset, model, response, or scientific content was
involved. The immutable 007-e report is preserved; this is its forward archival
correction.

## What was measured

The small direct studies retain their original 32-case counts and exact-gold
alignment counts. The ten-run studies retain trial-by-trial metrics, call counts,
partial/stopped status, and timing/token metadata in the private evidence
identities and the safe catalog fields. The final campaign is derived from its
phase completion records: 16,375 cases, 65,500 method records, 39,184 distinct
calls (31,916 new and 7,268 inherited), 1,419 verified checkpoints, eight
workers, and nine completed local phases. Deployment B was excluded by owner
override. Scribendi/remote scoring was access-blocked; no replication or GO is
manufactured.

The numeric projections use the campaign's custom token-coordinate alignment:
source/reference edits are aligned with the frozen tokenizer, exact-reference
success is separate from semantic judgment, and a non-reference change is not
called harmful. DASSLE categories and problem types remain distinct. Preservation
and detector-only fields retain their denominators and `EXACT`, `CENSORED`, and
`UNAVAILABLE` meanings. Paired intervals are over complete examples/documents,
not individual tokens.

The source closure retains the actual path through the final pipeline:

```text
original-coordinate protected spans
  -> hyphen-view local-context detector and corpus evidence
  -> original-target English eligibility/suppression
  -> frozen contextual JSON proposal
  -> symmetric initial-case restoration
  -> mechanical gate and exact Slovene-unigram gate
  -> at most one context-free expression retry on unigram uncertainty
  -> exact original-coordinate patch
```

M0/RAW, direct/translation, targeted M2, and no-retry M3 remain separate. The
curated code externalizes data/index/output roots and never pretends to be the
byte-identical historical driver. Historical absolute paths, private prompts
with filled examples, model responses, reasoning, dataset text, corpus/index
bytes, and credentials are not published.

## Offline reproduction

All default commands are CPU-only and offline. Use the inherited persistent
`TMPDIR`; do not substitute a system temporary directory.

```sh
python3 -B -m unittest discover -s research/tests -v
python3 -B -m research.tools.rebuild_tables --check
python3 -B -m research.tools.replay --scratch "$TMPDIR/007-c-replay"
```

The replay command executes the actual detector, English policy, case rule,
unigram gate, proposal parser, and patcher against a synthetic corpus with zero
network/model calls. A private replay is deliberately explicit and uses one
preserved case plus a persistent index, for example:

```sh
python3 -B -m research.tools.replay \
  --private-case PRIVATE_VARIANT_ROOT/runs/01/cases/h01.json \
  --index PRIVATE_INDEX.sqlite
```

Campaign saved samples use the same fail-closed path and must carry the
`input`/decision envelope, first and retry proposal stages, the frozen detector
cap (or an explicit null for uncapped), and numeric English evidence:

```sh
python3 -B -m research.tools.replay \
  --saved-record PRIVATE_CAMPAIGN_SAMPLE.json \
  --index PRIVATE_INDEX.sqlite
```

The private case record is read-only; replay verifies the saved output and emits
only counts and an output hash. It does not reconstruct a missing response or
resample a model. Dataset preparation/adapters and official scorer command
records accept explicit private roots and are never run on import.

Missing English evidence never becomes frequency zero; missing detector limits,
proposal stages, expected final values, or a malformed record abort the replay.
Both small-study `original/decisions` and campaign `input/decisions/first/retry`
schemas are accepted. Receipts contain counts and hashes only.

Historical reproduction plans are executable as a no-side-effect contract:
`python3 -B -m research.tools.reproduce --variant VARIANT ...` validates explicit
input/index/result roots, credential reference, endpoint/model fields and a
bounded budget, then emits a plan. It does not run a model. Live execution is a
separate future authorization boundary; no tree import or default command
acquires data, launches a model, or accesses a service.

## Publication boundary and retention

`registry/file-census.json.gz` is an exact file-level disposition ledger. Every
enumerated root and nested file has its logical relative path, SHA-256, size when
available, classification, and destination/reason. Source/result projections
are marked curated/redacted; unprojected source, raw rows, call/response files,
archives, traces, submissions, and private indexes are private-only. Duplicate
bytes are linked to an exact identity. Missing sources are visible as
`genuinely-missing`; no filename is treated as safe merely because it is called
`REPORT` or `RESULTS`.

The original native trees and archive receipts remain in the owner-selected
strategic workspace, with the relocation map and reconstruction guide. They are
not dependencies of a fresh public checkout. `registry/archive-catalog.json`
records verified archive identities and `registry/file-census.json.gz` keeps the
full logical-root/relative-path/hash disposition. The publication guard validates
the actual intended tree, allowlists only the compressed census and numeric
projections, checks JSON schemas/forbidden fields, refuses symlink/traversal and
overwrite exports, and can hash short and 16-token private-source windows from
explicit prepared sources without printing either side.

```sh
python3 -B -m research.tools.publication_guard --root research \
  --private-root PRIVATE_PREPARED_SOURCE_ROOT
```

For private identity replay, pass the compressed ledger and explicit
logical-root-to-current-private-root mappings; do not pass the compact summary:

```sh
python3 -B -m research.tools.replay \
  --manifest research/registry/file-census.json.gz \
  --root-map 'experiments/=/PRIVATE_EXPERIMENT_ROOT' \
  --root-map 'recovery-executions/=/PRIVATE_RECOVERY_ROOT'
```

No dataset, corpus, model, response, credential, human semantic label, or
production readiness claim is implied by this research publication.

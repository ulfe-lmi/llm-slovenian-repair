# LLM Slovenian Repair

Owner-published bootstrap baseline, accepted for continued development. Role
operation is qualified and the development loop has been deliberately started.
Query current protocol state with `python3 oap/bin/check_state.py --repo-root .
--repository ulfe-lmi/llm-slovenian-repair` and inspect `oap/active`.

Product PLANNED / NOT RUN. The implemented v1 seam provides strict frozen
`SpanSelection`/`SelectionBatch`, `EvidenceRecord`, `ReviewProposal`,
`OriginalCoordinateEdit`, `RepairResult`, and `PolicyConfig` models. Span offsets
are Python Unicode code-point offsets into the immutable original string; evidence
states are `EXACT`, `CENSORED`, or `UNAVAILABLE`, and the default policy is
`detect_only` with finite conservative limits.

Objective 004 adds the frozen `SourceManifest` and `SyntheticCountRecord`
provenance seam plus the canonical `verify_manifest_payload` boundary. The
manifest schema accepts only exact `UTF-8` encoding and `jsonl`/`json` records,
matched to `application/jsonl`/`application/json`. The checked-in
`tests/fixtures/corpus/synthetic-manifest.json` and JSONL payload are tiny,
project-authored synthetic schema fixtures only. Their authorized use scope is
`local synthetic tests only`, terms reference the repository `LICENSE`, and
`importer_schema_version` is `NOT_APPLICABLE_SYNTHETIC_FIXTURE`; no importer or
external corpus permission is claimed. They demonstrate checksum, bounded
loading, explicit denominator knowledge, and exact/censored/unavailable
evidence. The censored fixture records that values at/below synthetic cutoff 4
are represented only by `[0,4]`. Real candidate sources, rights, access, formats,
and release facts remain UNVERIFIED, and the fixture is excluded from the
installed package.

Detection, review calls, strict acceptance, patch composition, live compatibility,
and linguistic quality remain unimplemented or unproven. The intended library captures
a complete Slovenian model answer, selects suspicious local spans on CPU, optionally
asks the existing Qwen in an isolated context, validates independent evidence and
patches approved spans exactly. No repair application is implemented here.

Start with [development](docs/DEVELOPMENT.md), [runbook](docs/OAP-RUNBOOK.md),
[role setup](docs/CODEX-ROLE-SETUP.md),
[readiness](docs/READINESS.md) and [testing](TESTING.md). Full product agreement is
[PLAN](PLAN.md), implementation baseline [architecture](ARCHITECTURE.md), and
sole live judgment register [CRITICAL](CRITICAL.md). Coding uses the root router
and compact law; strategy reads full sources from its separate private workspace.

The repository is `ulfe-lmi/llm-slovenian-repair`; the owner's [LICENSE](LICENSE)
contains Apache License 2.0 and is preserved unchanged. Live repair testing is
disabled. Qwen compatibility, linguistic quality, ICA, milestone acceptance,
release, and deployment approval are not established.
Do not execute the [draft roadmap](oap/strategic-instructions/INITIAL-ROADMAP.md)
without strategic reconciliation and deliberate owner activation.

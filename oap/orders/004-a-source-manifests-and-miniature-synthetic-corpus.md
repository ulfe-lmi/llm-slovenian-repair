# Work order 004-a — Source manifests and miniature synthetic corpus

Status: FINAL

```oap-metadata
{
  "id": "004-a",
  "title": "Source manifests and miniature synthetic corpus",
  "objective": "004",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": ["003"],
  "local_work": "Clean main at remote accepted merge dac4789f52c9e82aec90d1cf92ce9f1194cc103a; preserve ignored local environments, private strategic state and all prior transcript history.",
  "prior_review": "Objective 003 completed through corrective 003-b and PR #4 merged as dac4789f52c9e82aec90d1cf92ce9f1194cc103a after exact-head review; no open PR remains.",
  "provenance": [
    {"kind": "H", "reference": "PLAN.md §§6.2–6.3 and D02"},
    {"kind": "A", "reference": "ARCHITECTURE.md §§8.1–8.2 and compact A-CORPUS-01/A-CORPUS-02/A-SECURITY-01"},
    {"kind": "E", "reference": "Accepted main contains strict EvidenceRecord/ContextDenominatorState contracts but no source-manifest module, corpus payload or corpus access; CRITICAL is empty and live repair tests are disabled."}
  ],
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "lr": ["LR-008", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

004-a is the first round of numeric objective 004. Create one new branch/PR from
accepted main `dac4789f52c9e82aec90d1cf92ce9f1194cc103a`. Recovery adopts that
same verified branch/PR and ID; never create a replacement PR after interruption.

## Provenance

- H: PLAN requires sparse reproducible corpus inputs and manifests naming source/
  release, checksum, license, cutoff, normalization, completeness and importer.
  Public query access is not bulk-download or redistribution permission.
- A: Architecture adds acquisition reference, format, annotation conventions,
  rights status, deterministic parameters and explicit synthetic labels. Candidate
  real resources are not bundled data or current-access claims.
- E: The accepted typed seam can represent exact/censored/unavailable query evidence
  and denominator knowledge, but there is no source-manifest or checked payload
  boundary yet. This order uses only new project-authored synthetic fixtures.

## Current verified state

Local and remote `main` are clean and equal at accepted merge
`dac4789f52c9e82aec90d1cf92ce9f1194cc103a`. Objective 003's history through
003-b is merged; remote active is exact `003-b\n`. There are no open PRs.
Accepted governance validates with unchanged PLAN
`d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0`,
ARCHITECTURE `a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7`
and empty CRITICAL `a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e`.

No real corpus release, URL, format, checksum, terms, rights, local availability or
access method has been verified. Live repair testing remains disabled. No model,
GPU, service, network, release or deployment authority is implied.

## Governance

Preserve accepted governance/CRITICAL and all prior transcript bytes. LR-008 keeps
missing thresholded data distinct from exact zero and denominators explicit.
LR-013 requires honest evidence layers; synthetic fixtures prove schema/checksum
software only. LR-014 forbids raw customer/model/review text and unapproved data.

Rights status cannot authorize itself. The schema may represent unknown/prohibited
real-source rights but must fail closed for any readiness/use flag. Only the exact
new project-authored synthetic fixture is permitted in Git. D0/NONE.

## Goal and dependencies

Add a strict versioned source-manifest and bounded payload-verification seam plus a
tiny deterministic project-authored synthetic corpus fixture. Prove provenance,
rights status, normalization/annotation, format, checksum, cutoff/completeness,
denominator meaning and synthetic labelling without implementing acquisition,
importing, indexing or real corpus access.

Objective 003 supplies strict evidence types. Later acquisition/import/index work
must consume this seam rather than inventing metadata ad hoc.

## Scope

1. Add strict frozen manifest and synthetic-record models in one focused package
   module, such as `source_manifest.py` or `resources.py`.
2. Add an explicit local loader/verifier for bounded manifest JSON and payload bytes.
3. Add tiny UTF-8 JSON/JSONL synthetic fixture payloads and matching manifests under
   `tests/fixtures/corpus/` or an equivalently clear test-only path.
4. Add focused tests against the real model/loader/checksum boundary.
5. Update direct exports, README/status/development docs, package/inventory assertions
   only where needed; keep fixtures out of installed runtime wheel unless justified.
6. Publish exact 004-a order/active/report on one new PR.

## Non-goals

No Gigafida, Sloleks, CLASSLA, collocation or other external data download/query/
scrape/copy; no guessed real release, checksum, URL, format, terms or license. No
corpus importer, SQLite/index, runtime lookup, normalization transform, aggregation,
ratio/probability, detector, reviewer, patcher, pipeline, API or CLI.

No new dependency, live test, customer/model text, private data, credentials, model/
GPU/service/port/network/gateway/GitHub-setting mutation, merge, release or deployment.

## Files and boundaries

Expected paths are one new package manifest module, focused
`tests/contract/test_objective_004.py`, bounded files under
`tests/fixtures/corpus/`, direct `__init__.py` exports and necessary README/STATUS/
development/inventory/package-payload assertions. Do not touch product governance,
CRITICAL, existing 003 contract semantics or unrelated OAP code.

The named boundary is the real strict manifest/record model and explicit local
verification function. Tests must load the checked-in manifest, validate the exact
payload bytes/checksum and parse each bounded synthetic record through the public
model. Manual test-only dict checks are insufficient.

## Requirements

1. Define immutable, extra-forbid, strict Pydantic v2 schema version 1. A source
   manifest records nonempty source identity/name, release/version, acquisition
   reference, payload relative path, lowercase SHA-256, byte size, media/record
   format, encoding, normalization, annotation/tagging convention, source/distribution
   completeness, cutoff/threshold metadata, rights status, license/terms reference,
   attribution/redistribution conditions, importer/schema version and deterministic
   build parameters.
2. Use finite public rights values covering at least project-authored synthetic,
   verified permitted, unknown/unverified and prohibited/restricted. Unknown or
   restricted rights may be represented for inventory but must have redistribution/
   use readiness false. Synthetic status requires `synthetic=true`, a repository-
   local acquisition reference and explicit project-authored fixture attribution.
   Non-synthetic status cannot masquerade as synthetic. Missing/blank rights or terms
   metadata fails validation.
3. Completeness and cutoff are coherent: COMPLETE may have null cutoff; PARTIAL must
   explain a nonempty cutoff/omission rule; UNKNOWN cannot claim complete coverage.
   Do not hardcode PLAN's reported approximate Gigafida threshold as universal.
   Manifest denominator knowledge is explicit and cannot be inferred by summing
   retained records.
4. Payload path is normalized repository-relative UTF-8 text: reject absolute paths,
   `..`, empty/dot paths, NUL/control characters, symlinks, directories and paths
   outside the caller-supplied fixture root. Verification reads with a finite default
   manifest/payload byte cap, requires regular files, checks exact size and SHA-256,
   and returns typed data without writing, executing content, following URLs or
   performing network/environment/service discovery.
5. Define a strict synthetic count-record model with `synthetic=true`, stable local
   record ID, finite query kind (word/bigram/trigram is sufficient), nonempty tuple of
   one/two/three tokens matching kind, and an embedded or referenced objective-003
   `EvidenceRecord`. Every numeric count/bound/denominator is therefore covered by
   an explicitly synthetic evidence source/scope and existing uncertainty rules.
   Reject wrong arity, duplicate record IDs, blank tokens, false/missing synthetic
   label and unknown fields/types.
6. Provide a tiny deterministic payload containing enough clearly artificial
   Slovenian-like tokens to exercise: exact positive, justified exact zero from a
   complete synthetic query, censored threshold-bound evidence with unknown
   denominator, and unavailable evidence without invented values. Mark every source,
   scope, count and manifest synthetic; include no copied sentence or real count.
7. The manifest's checksum and byte size match the exact committed payload.
   Deterministic load/serialize/load preserves model meaning and stable record order.
   A disposable copied fixture with one-byte payload change, wrong size/checksum,
   traversal/absolute/symlink path, oversized JSON/payload, duplicate ID or malformed
   JSON/UTF-8 fails with a bounded safe error.
8. Error messages use finite reason labels or bounded metadata and never echo payload
   contents, secrets or arbitrary paths beyond a safe caller-owned relative name.
   No import-time I/O. Public functions perform I/O only when explicitly called.
9. Document exactly that fixtures are project-authored synthetic schema evidence,
   not language-quality/corpus evidence; real candidate sources and all rights/access/
   format facts remain UNVERIFIED. Do not call source rights resolved by repository
   Apache code licensing.
10. Preserve locked dependencies and all 003 evidence/policy tests. Force-stage exact
    `004-a\n`, prove transcript index/implementation/report blobs, and make the report
    the sole final commit.

## Acceptance criteria

1. The committed synthetic manifest and payload verify through the public loader at
   their exact bytes; all records validate and round-trip in stable order.
2. Table-driven negatives reject missing/blank rights/terms/source fields, invalid
   checksum/size, rights/readiness contradictions, cutoff/completeness contradictions,
   false synthetic labels, wrong token arity and evidence-state contradictions.
3. Disposable filesystem tests reject traversal, absolute/outside paths, symlinks,
   non-files, oversized/malformed/invalid-UTF-8 manifests or payloads, checksum drift
   and duplicate records without logging content.
4. No external corpus bytes, invented real-source fact, network call, import-time I/O,
   new dependency or installed-wheel fixture payload is introduced.
5. Focused and broad product tests, `ruff check src scripts tests`, mypy, full OAP
   suite, native locked/offline baseline, transcript/governance/protected-source checks
   and both required final-head CI checks pass at exact SHAs.
6. The sole new objective PR remains open/unmerged during coding; remote SELF report
   verifies. Live/model/corpus-quality/ICA/release/deployment evidence remains absent.

## Verification

Use the frozen lock and an owned native temporary environment. Run/report:

```text
pytest tests/contract/test_objective_004.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-a
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-a
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a
git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD
git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication strategy independently verifies remote SELF, exact active
bytes and both checks at the literal final head. This is only schema/checksum and
synthetic software evidence—not source rights/access, linguistic benefit, live Qwen,
ICA, milestone, release or deployment evidence.

## Local setup and constraints

Use only committed lock data and owned native temporary environments/caches. Do not
mutate/depend on repository `.venv`. All fixtures are deliberately tiny, synthetic,
UTF-8 and non-sensitive. No access to external corpus URLs or services is permitted;
even a URL-looking acquisition reference is inert data and must never be fetched.

No credentials/customer/model text/prompts/replacements/reviewer responses in source,
tests, reports or logs. No protected model/GPU/service/network/neighbor mutation.
Live tests, release and deployment remain disabled/separately gated.

## Documentation

Document public manifest/record/checker names, exact fixture location, checksum
verification API and limitations. Clearly mark all counts synthetic and all real
resource facts/rights/access unverified. Preserve existing product-status and
objective-003 limitations.

## Git and report publication

Create only `oap/004-source-manifests-and-miniature-synthetic-corpus` from exact
accepted main and one new PR. Commit/push all non-report work, exact immutable order
and force-staged active before the report. Create/adopt the PR, run implementation-
head CI and record the literal implementation SHA.

Then create only
`oap/reports/004-a-source-manifests-and-miniature-synthetic-corpus.md`. Its SELF
commit has the implementation head as sole parent and changes only that report.
Push, verify remote head/bytes/parent/path and active blobs, send exact `OK`, and exit
without later mutation. Report-head checks remain PENDING inside the report.

## Decision classification

D0. Strict local schemas, safe bounded file verification and project-authored
synthetic fixtures are reversible development choices within explicit architecture.
No real-source right or access is selected, no external obligation is incurred and
no protected or production boundary is crossed.

## Deferred human adjudication
- Decision: NONE

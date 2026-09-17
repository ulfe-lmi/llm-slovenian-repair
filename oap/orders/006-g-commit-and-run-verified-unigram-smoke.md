# Work order 006-g — Commit and run verified unigram smoke

Status: FINAL

```oap-metadata
{
  "id": "006-g",
  "title": "Commit and run verified unigram smoke",
  "objective": "006",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/006-unigram-lexicon-importer",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "dependencies": ["003", "004", "005"],
  "local_work": "Clean branch at remote 006-f blocked report head c5772a4433f78b1e73a1cd74713714279b9207fc; report/transcript/final CI/fsck verified; no source temp or disposable 006-f environment remains.",
  "prior_review": "006-f parser correction passes complete offline evidence, but its one verifier-first GET stopped at an ad-hoc smoke-harness syntax error before selected-member access; zero importer attempts, cumulative GETs eight. Independent review also stopped a lingering broad filename scan and found historical active-pointer Git mode 100755.",
  "provenance": [
    {"kind": "E", "reference": "006-f receipt/report: canonical artifact verifier PASSED, member access false, smoke harness syntax failure, importer attempts zero, all unobserved fields null, cleanup/non-retention true, one 006-f GET and cumulative eight."},
    {"kind": "I", "reference": "Independent diff/CI review accepts the finite optional-terminal-tab implementation offline; the earliest missing boundary is reusable tested orchestration from verified archive to the actual importer, not another parser change."},
    {"kind": "A", "reference": "ARCHITECTURE §8, S-DIAGNOSE-01 and S-EVIDENCE-01 require the actual named entry point, source fidelity, finite evidence labels and a smallest experiment after the pre-product harness failure."}
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
  "lr": ["LR-008"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

006-g is the execution-boundary correction on existing PR #7. Preserve every 006-a–f
order/report/receipt, invalid-publication recovery, request count and Git incident.

## Provenance

- E: 006-f verified the artifact and failed before member access solely because its
  ephemeral harness was syntactically invalid.
- I: A committed helper exercised on a synthetic ZIP before network access removes that
  pre-product ambiguity and makes the same exact action reproducible.
- A: The importer cannot be accepted without actual bounded source-entry-point evidence.

## Current verified state

Accepted main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is open at valid
006-f BLOCKED SELF `c5772a4433f78b1e73a1cd74713714279b9207fc`, whose implementation
head is `2a967fecaf650faa9c8459bf1b1913647384d274`; final checks and fsck pass.
The optional-tab parser is supported only by synthetic/offline evidence. Exactly one
006-f GET was consumed, cumulative eight; no archive, source tree or owned environment
remains. CRITICAL is empty.

GitHub branch protection returns 404 and repository rulesets are empty. The development
gate depends on OAP/agent procedure, not server refusal. Do not change settings. The
active pointer has exact 006-g worktree bytes after publication but historical branch
index mode 100755; normalize the current commit to 100644 without rewriting history.
No live repair, milestone, release or deployment gate is authorized.

## Governance

Compact law, LR-008, security/testing and source inventory. D0/NONE. Treat the source
as read-only untrusted external bytes; output aggregates/hashes only.

## Goal and dependencies

Replace the failed ephemeral harness with a committed and tested bounded verification/
member/import utility, then use it once on a newly acquired verified archive to finish
the 32-row real compatibility proof.

## Scope

1. Add one reusable source-smoke script/helper and focused synthetic ZIP tests.
2. Run one verifier-first 006-g acquisition and the helper; publish a new receipt.
3. Normalize only current `oap/active` Git tree mode to 100644.
4. Complete sequential verification and report on PR #7.

## Non-goals

No new parser semantics unless a focused test exposes a bug; no full archive import,
index/database/lookup/detector, n-grams/other source, automatic downloader, committed
source row/archive, broad filesystem search, root export/dependency change, history
rewrite, GitHub setting, merge, live Qwen, release, deployment, ICA or milestone claim.

## Files and boundaries

One new script, its objective-006 tests, direct docs/status, new 006-g receipt, exact
active/order, generated inventories and report. Touch importer only for a demonstrated
helper-integration defect and document the exact reason. Do not rewrite older evidence.

## Requirements

1. Add a committed importable CLI such as `scripts/smoke_unigram_prefix.py`. Its real
   path accepts only explicit canonical inventory/source/artifact arguments, invokes
   `verify_source_artifact.verify_artifact` successfully before selected-member access,
   and fails closed with finite non-content reasons. It never downloads or extracts.
2. After verifier success, require the canonical byte size, MD5, archive SHA-256, five
   members and total uncompressed size. Open the exact selected ZIP member once. Read
   with capped `readline` calls exactly 14 preamble lines, the exact 834-byte line-15
   header and 32 complete data rows into a <=4 MiB in-memory envelope. Reject missing/
   duplicate/wrong member, short/long line, incomplete prefix, bad header and changed
   artifact identity without including source bytes in an error.
3. Classify exactly those 32 data rows through the existing content-free classifier and
   require the 006-e aggregate: UTF-8/CRLF 32; fields 28:31 and 29:1; terminal tabs 0:31,
   1:1 and 2+:0; empty-final one; nonempty-after-28, embedded-tab, quote error and first
   structural failure zero/null. Do not rely on the optional parser-probe histogram.
4. Construct exact real `UnigramProvenance` with source/query COMPLETE and import
   PARTIAL, then call public `import_unigrams` twice on fresh streams over the same
   envelope. Require two completed attempts, immutable equality, 32 records, and equal
   nonnull input/output SHA-256 and summary bindings. Emit only finite status, counts,
   canonical verification facts, aggregates and result hashes; never header/row values,
   record dumps or per-row hashes.
5. Synthetic tests invoke the actual helper boundary on an in-memory or owned temporary
   ZIP containing exactly 14 preamble lines, the exact header and 32 project-authored
   rows spanning both accepted terminators. Prove one member open/prefix read, aggregate,
   twice-import determinism and no output content. Negative tests cover verifier stop,
   path/symlink/nonregular input, member ambiguity/missing member, prefix/header/line/
   byte bounds, structural mismatch and importer finite failure. Fakes may supply prior
   verifier evidence outside the member/import boundary; they may not replace it.
6. Exercise CLI serialization/error handling offline. Do not construct the real action
   as inline Python or an uncommitted here-document. Run focused objective-005/006 and
   complete supported baseline sequentially before source access. Use an owned `/tmp`
   environment or system closure; never use/repair repository `.venv`.
7. Only after offline green, create one exact owned `/tmp/...006-g-source...` directory
   and retain its literal path. Do not scan `/tmp`, the workspace or home for archives.
   Perform exactly one 006-g GET with `curl --disable`, direct HTTPS/no redirect/no
   credentials/options, fail, connect <=10s, total <=900s, max-filesize 115865656 and
   a single `.part` target. No retry under this suffix.
8. Invoke only the committed helper/CLI on that exact part path. On any verifier, member,
   aggregate or importer failure, stop with null unobserved fields and no second GET.
   Delete the literal source tree in a guaranteed cleanup path and verify only that exact
   path is absent. Do not overlap broad tests, OAP, Git, acquisition or cleanup commands.
9. Add `resources/source-acquisitions/gigafida-2.0-words-006-g.json`. Record exact UTC,
   canonical inventory/verifier facts, one 006-g GET and cumulative nine, 006-f harness
   failure and zero attempts, helper identity, structural aggregate, smoke attempts/runs/
   count/equality/hashes, PARTIAL import, no content/retention/temp and redistribution
   false. Use null for anything unobserved and never guess a future commit.
10. Receipt tests validate exact schema/counts/hashes/status, prior history and forbidden
    content fields. Docs distinguish bounded compatibility from full archive import,
    lookup readiness, linguistic benefit, rights, release, deployment and acceptance.
11. Preserve 006-f parser/tests, lock/dependencies, objective-001 source/wheel root
    laziness, 003–005 contracts, source inventory, all history and protected governance.
    Explicitly stage active bytes with `git add -f`, then set only its index mode to
    non-executable and prove `git ls-files --stage oap/active` is 100644 plus exact
    `006-g\n`; do not change historical commits or physical sync-mount assumptions.
12. Remove owned disposable environments. Run focused/all contract/full pytest, Ruff,
    mypy, OAP, native baseline, transcript, governance, diff/fsck and both required CI
    sequentially. Report criteria is a string; name every implementation/correction SHA,
    the real evidence boundary and any strategic-stopped scan; sole SELF report, no
    future-CI, retry, merge, live, release, deployment or milestone claim.

## Acceptance criteria

1. The committed tested helper enforces verifier-first, one-member/finite-prefix routing,
   exact aggregate and two actual importer calls without content disclosure.
2. Exactly one 006-g fetch (cumulative nine) yields 32 equal deterministic real-prefix
   records/hashes under explicit PARTIAL import evidence, or reports the earliest finite
   boundary truthfully without retry.
3. The receipt proves cleanup/non-retention and preserves all prior failures; source,
   wheel and governance regressions stay green and active is committed mode 100644.
4. Final local and report-head checks/fsck pass; PR #7 remains unmerged during coding.

## Verification

```text
pytest tests/contract/test_objective_005.py -q
pytest tests/contract/test_objective_006.py -q
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-g
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-g
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git ls-files --stage oap/active
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also run exactly one real acquisition followed by the committed CLI and exact cleanup.

## Local setup and constraints

One new 006-g request only after offline green. Exact owned paths, no broad `find`, no
repository `.venv`, no concurrent checks/Git, explicit Git maintenance disabled. Preserve
the private recovery backup. No raw external text, credentials or protected host change.

## Documentation

Document reusable helper, bounded real-smoke outcome and evidence limits. Historical
006-f remains blocked and immutable even if 006-g succeeds.

## Git and report publication

Same PR #7. New commits only; no amend/force. Push non-report work and wait for CI; sole
`oap/reports/006-g-commit-and-run-verified-unigram-smoke.md` SELF commit with literal
implementation head parent, remote verify, exact OK, exit. No merge.

## Decision classification

D0. A contained reproducibility correction and bounded public-source compatibility
probe; no rights, intent, live-service, release or deployment decision.

## Deferred human adjudication
- Decision: NONE

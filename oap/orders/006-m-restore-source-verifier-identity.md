# Work order 006-m — Restore objective-005 verifier identity

Status: FINAL

```oap-metadata
{
  "id": "006-m",
  "title": "Restore objective-005 verifier identity",
  "objective": "006",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/006-unigram-lexicon-importer",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "dependencies": ["000", "001", "002", "003", "004", "005"],
  "local_work": "Clean branch and remote PR #7 at verified 006-l COMPLETE report 53defa605970b6413f44f9e3d477f08247469c1c; three report-head checks green; verified external word archive cache retained; recovery refs and dangling blob bbca830666fc43fb89081d1c5a11cf1c5e37f606 must be preserved.",
  "prior_review": "Independent final review confirmed report-history/cache correction, all 20 focused negatives, complete native baseline, source/wheel root-import isolation and zero-GET cache reuse. It also found scripts/verify_source_artifact.py differs from accepted objective-005 main by an unauthorized local-variable rename introduced in 006-g; the immutable 006-g report misattributes that change to its later correction commit.",
  "provenance": [
    {"kind": "H", "reference": "Human-owner requires objective-005 source inventory and verifier identities unchanged before PR #7 merge and requires a same-PR corrective suffix for any material final-review defect."},
    {"kind": "E", "reference": "Direct diff ee2d1b4..53defa6 shows only info -> path_info at scripts/verify_source_artifact.py lines 589-594, introduced by 21e053d9; inventory is byte-identical and full tests pass."},
    {"kind": "I", "reference": "The change is runtime-equivalent but violates 006-g requirement 11 to preserve the verifier and the owner's exact cross-objective identity gate; 006-g report says b7bd642 corrected the shadow although the actual verifier change is in 21e053d."},
    {"kind": "C", "reference": "Restore accepted-main verifier bytes with a new commit, never mutate the immutable 006-g report, and record its limited inaccurate attribution in the new 006-m report."},
    {"kind": "A", "reference": "S-ORDER-03 and the intervention require the next same-PR suffix rather than merge with a known contradiction; all unrelated 006 work and concept-first priority remain preserved."}
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
  "required_checks": ["OAP bootstrap acceptance", "OAP report history", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

006-m is the sole final-review correction to 006-l on existing PR #7. It restores an
accepted cross-objective file identity and records an immutable-report inaccuracy. It
does not resume product importer refinement or begin concept implementation.

## Provenance

- H/E: The owner requires exact objective-005 verifier identity; direct Git history
  proves the sole three-line rename and its introducing commit.
- I/C: Runtime equivalence does not cure unauthorized scope. Restore accepted bytes in
  a new commit and correct the report attribution only through this new suffix.
- A: Keep all completed 006 evidence and the concept-first priority intact.

## Current verified state

Accepted main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is open,
non-draft, mergeable and clean at report head
`53defa605970b6413f44f9e3d477f08247469c1c`; Application baseline, OAP bootstrap
acceptance and OAP report history are green there. CRITICAL is empty. Active ruleset
22590837 blocks deletion/non-fast-forward changes but does not require status checks or
reviews; legacy branch protection remains absent. Do not change GitHub settings.

Direct review established:

- source and built-wheel bare root imports load neither Pydantic nor HTTPX;
- the complete owned baseline and all 20 report/cache history tests pass;
- the external word archive is VERIFIED_REUSABLE twice with zero network GETs;
- only frozen RHI-0001/RHI-0002 are accepted as limited historical incidents;
- PLAN, ARCHITECTURE, CRITICAL, source inventory, lock and objective-003 root contracts
  are unchanged from accepted main;
- `scripts/verify_source_artifact.py` alone violates the required objective-005 identity:
  commit `21e053d9b518ef5826ef560d6fd144c05b69eee5` renamed local `info` to
  `path_info`; no runtime semantics were intended or required;
- immutable 006-g says commit `b7bd6421f969d1ac09bdd4032c3d462ea7bc3e64`
  made that correction, but its actual diff did not. Do not edit that report.

## Governance

Existing human/OAP law. D0/NONE. Exact accepted-byte restoration only. Historical
artifacts, source data, live systems and all D2 gates remain untouched.

## Goal and dependencies

Dependencies 000–005 remain accepted. Close the one final-review identity contradiction,
then return PR #7 for the already-authorized development-only merge review.

## Scope

Restore the exact accepted-main verifier bytes, prove that the restoration preserves all
objective-005/006 behavior and mandatory integrity/cache guards, publish one truthful new
report, and return the same exact PR head for strategic merge adjudication.

## Files and boundaries

Allowed paths are the current active pointer, this exact new order/report, the verifier
file, and only generated metadata whose verifier hash mechanically requires refresh. PR
body metadata may be updated without a repository commit. No other source, test, receipt,
history, cache, documentation, governance or product file is authorized to change.

## Non-goals

No rewrite/amend/force-push; no edit to any prior order/report/receipt; no new incident
exception; no test weakening, skip or expectation inversion; no importer/numeric/source
semantics; no corpus GET or cache mutation/cleanup; no concept subtree yet; no objective
007; no Git prune/gc/clean/stash/reset; no Qwen/service/network/GitHub-setting change;
no merge by coding; no live test, milestone, release or deployment claim.

## Requirements

1. Restore `scripts/verify_source_artifact.py` byte-for-byte from accepted main
   `ee2d1b479719009ff1d07829478f241e3f395f7c`. Do not manually approximate the diff.
   After the implementation commit, `git diff --exit-code ee2d1b4 --` for this path must
   pass and its SHA-256 must equal the accepted-main blob's content SHA-256.
2. Do not alter `resources/source-inventory-v1.json`, any `src/**` file, `uv.lock`, any
   existing test, any previous order/report/receipt, or `oap/REPORT-HISTORY-INCIDENTS.json`.
   If the restored verifier exposes a test/type failure, stop and report the exact earliest
   failure; do not reapply the rename or weaken a check without a new strategic decision.
3. Re-run objective-005 artifact-verifier tests and objective-006 smoke/cache tests through
   their real entry points. Verify the canonical retained cache against the restored
   verifier at least twice; both validations must be VERIFIED_REUSABLE with zero GET and
   no source rows/raw values/private cache path in output. Do not consume or modify it.
4. Re-run the root source and independently built-wheel fresh-process probes. Bare
   `import llm_slovenian_repair` must load neither Pydantic nor HTTPX and wheel contents
   must contain no archive/cache/source rows/database.
5. Re-run focused/full pytest, Ruff, mypy, all OAP tests, the native locked/offline
   development baseline, transcript index/revision, report-history/acquisition-history,
   accepted governance, protected-source diff, package scan, `git diff --check`, and
   `git fsck --full --no-reflogs`. The preserved dangling blob may remain; never prune it.
6. Confirm the 006-g report remains byte-identical and explicitly state in 006-m that its
   type-shadow attribution is inaccurate: verifier change commit was `21e053d9`, not
   `b7bd642`; it remains usable for its bounded smoke/failure facts but not for that commit
   attribution. This is a new corrective record, not an edit or generic incident allowlist.
7. Update PR #7 body through GitHub metadata only to current 006-m and the verified
   restoration. Preserve the concept-first next priority, partial/fail-closed importer
   status, cumulative fourteen GETs, verified external cache, no merge/release/deployment
   claim, and real Markdown newlines.
8. Push the non-report implementation and wait for all three exact-head GitHub checks.
   Then publish the sole report-only SELF commit with literal implementation parent. Run
   report/transcript/history verification against the remote report head and require all
   three checks green again. Coding must not merge or select the next objective.

## Acceptance criteria

1. `scripts/verify_source_artifact.py` and `resources/source-inventory-v1.json` are both
   byte-identical to accepted main while objective-005/006 verifier/cache tests remain
   green.
2. No test expectation or prior immutable artifact changed; all report-history negatives
   and exact frozen incidents remain enforced.
3. Root import isolation, source/wheel agreement, fail-closed importer behavior, external
   cache reuse with zero GET, no archive packaging and complete baseline remain green.
4. The new immutable report truthfully corrects the 006-g attribution and the exact final
   PR head has all three required checks green for a fresh strategic review.

## Verification

```text
pytest tests/contract/test_objective_001.py -q
pytest tests/contract/test_objective_003.py -q
pytest tests/contract/test_objective_004.py -q
pytest tests/contract/test_objective_005.py -q
pytest tests/contract/test_objective_006.py -q
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract/test_objective_006_smoke.py -q
pytest tests/contract -q
pytest -q --ignore=.venv
ruff check src scripts tests
mypy src scripts tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 006-m
python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-m
python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest
python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD
python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- scripts/verify_source_artifact.py resources/source-inventory-v1.json
git diff --exit-code 53defa605970b6413f44f9e3d477f08247469c1c -- src tests uv.lock oap/REPORT-HISTORY-INCIDENTS.json resources/source-acquisitions oap/orders/006-a-unigram-lexicon-importer.md oap/reports/006-g-commit-and-run-verified-unigram-smoke.md
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git fsck --full --no-reflogs
```

Also run the restored-verifier cache validation twice, direct source/wheel lazy-import
probes, archive/package scan, exact PR metadata check and all three final-head CI checks.

## Local setup and constraints

Use only owned `/tmp` dependency/build environments and the exact existing external cache
for read-only validation. No source download, broad scan/delete, repository `.venv`,
concurrent duplicate checks, raw source/customer text, credential output or Git object
cleanup. Preserve recovery refs, dangling evidence and unrelated work.

## Documentation

Keep product documentation unchanged. Update only PR metadata and the new 006-m report
with the accepted-byte restoration, exact historical attribution correction, verified
cache/no-GET state, concept-first next priority and bounded no-deployment meaning.

## Git and report publication

Same branch and PR #7. New commits only. The verifier restoration is implementation, not
history rewriting. Push implementation, wait exact-head CI, then one immutable
`oap/reports/006-m-restore-source-verifier-identity.md` SELF report-only commit. Verify
the remote report head and return exact `OK`. No coding merge/auto-merge.

## Decision classification

D0. This restores accepted bytes under an explicit owner cross-objective invariant. It
does not select product meaning, alter rights/security posture, or cross a live/release/
deployment boundary.

## Deferred human adjudication

- Decision: NONE

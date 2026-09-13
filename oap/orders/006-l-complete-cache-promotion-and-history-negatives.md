# Work order 006-l — Complete cache promotion and history negatives

Status: FINAL

```oap-metadata
{
  "id": "006-l",
  "title": "Complete cache promotion and history negatives",
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
  "local_work": "Clean branch at verified 006-k PARTIAL report 98f26097ebe5f848d700e9de308aada1eeae5cfa; all three report-head CI checks green; cache root exists empty after failed exact cleanup; local recovery refs and dangling blob bbca830666fc43fb89081d1c5a11cf1c5e37f606 must be preserved.",
  "prior_review": "006-k fully enforces/freeze-labels report history but omitted two explicit negative cases. One canonical GET (cumulative thirteen) verified, then hardlink promotion failed; fallback is offline-only, final cache absent. Helper still attempts hardlink and has broad catches.",
  "provenance": [
    {"kind": "H", "reference": "Human-owner requires immutable-report negatives and one verified reusable external cache before PR #7 merge review, followed by concept verification rather than production numeric refinement."},
    {"kind": "E", "reference": "006-k receipt/report: one GET/cumulative thirteen, verifier PASSED, FAILED_HARDLINK_BOUNDARY, exact part removed, consumer/revalidation zero, cache MISSING; report-history and three CI checks pass."},
    {"kind": "I", "reference": "Independent code review finds promotion still tries os.link before fallback and broad exception catches remain; focused tests omit later implementation_head mutation, same-path bad-report repair and exact known-history third-touch cases."},
    {"kind": "A", "reference": "Human intervention plus S-EVIDENCE-01 require actual sync-path promotion/reuse and explicit history negatives; S-RECOVER-01 preserves dangling/recovery evidence and forbids history cleanup."}
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

006-l is the sole material correction to 006-k on existing PR #7. It completes the
mandatory human integrity/cache intervention; it does not resume product numeric work.

## Provenance

- H/E: One necessary new acquisition is authorized because 006-k verified then removed
  the only bytes after actual promotion failure.
- I: Eliminate the failed mechanism, exercise exact sync path, and close explicit test gaps.
- A: Preserve all history/local evidence and proceed to concept verification after review.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`; PR #7 open at valid
006-k PARTIAL report `98f26097ebe5f848d700e9de308aada1eeae5cfa`, implementation
`fb057b3cf98c509ba84ffbbd8122995d62e7f2e9`; Application baseline, OAP bootstrap
acceptance and OAP report history are green. History guard explicitly freezes only
RHI-0001/RHI-0002. Cache state MISSING/empty; GET cumulative thirteen. CRITICAL empty.

GitHub legacy protection is 404; active ruleset 22590837 blocks deletion and non-fast-
forward with no bypass but has no required-status/review rule. Do not change it. PR body
must retain concept-first priority. No live, milestone, release or deployment action.

## Governance

Existing human/OAP law. D0/NONE. Cache-mechanism/test completion only; product and
historical artifacts immutable. Do not prune or delete any Git/recovery evidence.

## Goal and dependencies

Close the exact 006-k cache promotion/test gaps, establish and prove reusable verified
concept cache with one minimum new GET, then return PR #7 for strongest merge review.

## Scope

1. Direct locked atomic-rename promotion and narrowed cache errors.
2. Complete report-history/cache/acquisition negative tests.
3. One cache establishment GET, two zero-GET consumers and persistent verified receipt.
4. Full cross-objective/final-head evidence and current PR metadata; no merge in coding.

## Non-goals

No report/order/receipt rewrite, new incident exception, hardlink promotion, Git prune/gc/
clean/stash/reset, product importer/numeric/row-role changes, concept subtree yet,
objective 007 implementation, source redistribution/Git/package inclusion, Qwen/service/
network setting, ruleset change, merge, live test, milestone, release or deployment.

## Files and boundaries

Cache/acquisition helpers and focused tests, report-history tests only as needed, new
006-l receipt, current docs/status/generated projections, active/order/report. Exact
external cache subtree only. `src/**`, source inventory/verifier, incident JSON/code
identities, prior reports/receipts, governance and lock are inspect-only.

## Requirements

1. Replace promotion's hardlink/fallback branch with one lock-protected same-directory
   `os.replace(part, final)` after canonical part verification and final/metadata absence
   checks. Never call `os.link`. Flush/fsync the part and directory where supported;
   best-effort read-only chmod remains advisory on the selected sync mount.
2. Immediately reopen the renamed final, require owner/regular/non-symlink/link-count-one,
   repeat size/MD5/SHA-256 and accepted inventory ZIP verification, then write metadata
   exclusively and fsync. Only after a full `inspect` returns VERIFIED_REUSABLE may
   promotion succeed. Any rename/post-verify/metadata failure removes only exact part/
   final/metadata under the lock, leaves MISSING/INVALID truthfully, and never retries.
3. Remove broad `except Exception` from cache verification and exclusive-write paths.
   Catch/map only documented expected OSError, inventory/artifact verifier and JSON/type
   failures. Unexpected programming errors remain visible and cannot become evidence.
4. Add explicit real Git-history negatives for: changing `implementation_head` after
   publication; repairing an invalid report at the same path; modifying/deleting/readding
   a report; and adding a manifest exception. Add a real current-history fixture proving
   exact RHI-0001/RHI-0002 pass with incident status while a third touch to either path
   fails. A new suffix path must still succeed. Never modify real historical reports.
5. Expand cache negatives to cover corrupt size, MD5, SHA-256, stale/duplicate metadata,
   symlink, hardlink, nonregular, wrong-owner seam, wrong root, unexpected file, existing
   final overwrite, rename/metadata failure cleanup, invalid exact repair and lifecycle-
   gated cleanup. Tests assert `os.link` is never invoked and `os.replace` is the atomic
   boundary. Fakes remain outside accepted verifier/cache consumer boundary.
6. Extend acquisition-history guard for immutable 006-k BLOCKED cumulative thirteen and
   one new 006-l ESTABLISHED_VERIFIED or REUSED_VERIFIED receipt. With current MISSING,
   allow exactly one network GET/cumulative fourteen; later active generation receipts
   require zero GET and same digest unless exact INVALID/MISSING deletion is recorded.
   Test monotonic counts, prior receipt immutability and accidental refetch rejection.
7. Before network, run focused OAP/history/cache, objectives 001/003/004/005/006 and full
   supported tests in owned `/tmp` environments; every uv target/cache explicit, never
   repository `.venv`. Direct fresh source and built-wheel root imports must agree and
   load neither Pydantic nor HTTPX. `src/`, source inventory/verifier and lock unchanged.
8. From current empty exact cache root, plan must report MISSING/FETCH_REQUIRED with zero
   GET. Perform exactly one bounded canonical direct GET to fixed part, cumulative
   fourteen. No retry/second GET. Promote through the committed rename-only helper and
   require exact canonical identities plus VERIFIED_REUSABLE metadata.
9. Demonstrate reuse without network: validate cache; invoke the existing 006-j content-
   free diagnostic twice sequentially against the final cache artifact using one owned
   dependency interpreter, with identical safe aggregates/results; validate after each.
   Record consumer_count >=2, revalidation_count >=3, network_get_count 1 only for
   establishment and no source/raw/private-path output. Retain final for concept work.
10. Add immutable 006-l receipt with exact UTC, legacy twelve + 006-k one + 006-l one =
    cumulative fourteen, prior cache failure, rename-only promotion, verifier facts,
    generation, consumer/revalidation counts, retention until concept completion,
    no-content/Git/package/redistribution and retry false. Do not edit 006-k receipt.
11. Assert no archive/part/cache file in Git, repository, build or wheel. Cache final is
    external, owner-controlled, validated before every use, and cleanup remains gated to
    concept-complete/abandoned. Document retention/stale/corruption response and future
    zero-GET rule. Update PR body via REST metadata only to current 006-l + concept-first.
12. Run focused/full pytest, Ruff, mypy, all OAP tests, native baseline, transcript index/
    revision, report-history/acquisition-history, governance/protected diff, package scan,
    fsck and all three final-head CI checks sequentially. Fsck may report only preserved
    pre-existing dangling `bbca830666fc43fb89081d1c5a11cf1c5e37f606`; do not delete it.
    Report starting SHA `98f26097ebe5f848d700e9de308aada1eeae5cfa`, criteria string,
    no angle placeholders, sole SELF, no merge/live/release/deployment claim.

## Acceptance criteria

1. Direct atomic rename succeeds on the exact sync cache; post-rename verification and
   metadata/inspect bind identical canonical bytes, with no hardlink or broad catch.
2. Two diagnostic consumers and >=3 validations reuse the final with zero further GET;
   006-l receipt/history guard records cumulative fourteen and rejects future refetch.
3. Every owner-requested report-history negative passes; only exact frozen incidents are
   surfaced and a third touch/manifest self-exception fails.
4. Cross-objective/local/report-head checks pass, PR body is current/readable, no product/
   historical/source artifact changed, PR #7 remains unmerged for strategic review.

## Verification

```text
python3 -B -m unittest discover -s oap/tests -p 'test_report_history_cache.py' -v
python3 -B -m unittest discover -s oap/tests -p 'test_transcript_guard.py' -v
python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v
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
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-l
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-l
python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest
python3 oap/bin/acquisition_history.py --repo-root . --revision HEAD
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git diff --exit-code 98f26097ebe5f848d700e9de308aada1eeae5cfa...HEAD -- src resources/source-inventory-v1.json scripts/verify_source_artifact.py uv.lock oap/REPORT-HISTORY-INCIDENTS.json
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also run cache plan/fetch/promote/two-consumer/revalidate proof, source/wheel import
probes, archive package scan, PR-body newline/current-priority check and final CI.

## Local setup and constraints

Owned `/tmp` dependency environments only; exact external cache root only. One GET max,
no hardlinks, broad search/delete, repo `.venv`, concurrent checks, raw source, Git object
cleanup or setting changes. Preserve recovery refs/dangling/user work.

## Documentation

Record completed guard negatives, cache promotion/reuse/lifecycle, exact cumulative GETs,
prior failures and concept handoff without rewriting history or claiming product success.

## Git and report publication

Same PR #7. New commits only; no amend/force/history rewrite. Push non-report work, wait
all three CI checks, then sole
`oap/reports/006-l-complete-cache-promotion-and-history-negatives.md` SELF report with
literal implementation parent. Remote/history verify, exact OK, exit. No merge.

## Decision classification

D0. Exact correction of a tested cache mechanism and explicit human-required negatives;
no product meaning, rights expansion, live-service, release or deployment decision.

## Deferred human adjudication
- Decision: NONE

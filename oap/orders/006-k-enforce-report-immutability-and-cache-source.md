# Work order 006-k — Enforce report immutability and cache source

Status: FINAL

```oap-metadata
{
  "id": "006-k",
  "title": "Enforce report immutability and cache source",
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
  "local_work": "Clean branch at verified 006-j report head 2bc6007ec67ca3f58682cb3c14ac61a6545c0bb3; final report-head CI/transcript/fsck green; two leaked 006-j verification directories removed by strategy after exact validation; local 006-h recovery refs preserved; objective cache absent.",
  "prior_review": "Human intervention independently confirmed 006-a and 006-c report-path rewrites, twelve completed archive GETs through 006-j, stale malformed PR body, and missing history/cache guards. PR body is now readable/current via REST metadata only. A later human priority requires isolated concept verification after this correction; merge and numeric progression remain suspended.",
  "provenance": [
    {"kind": "H", "reference": "Human-owner interventions 2026-09-09 mandate immutable-report history enforcement, exact grandfathering only for known violations, efficient verified external source reuse, current PR metadata and full cross-objective review before merge; then prioritize isolated end-to-end concept verification over further production numeric work."},
    {"kind": "E", "reference": "Git history proves report 006-a blobs 1c6ae728... then 39eb8b6e... at commits e16c3303.../767062ac..., and report 006-c blobs 625e05a2... then 78f3a034... at 241d069a.../898ccbc...; no other M/D report path exists on current ancestry."},
    {"kind": "E", "reference": "Receipts record twelve 115865656-byte archive GETs through 006-j and deletion after each round; exact STRATEGIC_HOME/source-cache/concept-verification/gigafida-2.0-words is absent."},
    {"kind": "I", "reference": "Independent review finds verify_report/check_transcript use the last report-touch commit and do not scan path history, allowing a rewritten report to masquerade as its own implementation parent; strategic gate relies on caller-named green checks."},
    {"kind": "C", "reference": "006-j report claimed verification directories absent before strategy removed them and described cleanup after coding attempted broad git prune; preserve the report and correct only in new evidence."}
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

006-k is the mandatory human-ordered process-integrity correction on existing PR #7.
It supersedes the planned numeric follow-up. Preserve all repository/remote history.

## Provenance

- H: The owner explicitly requires these corrections before merge or numeric progress.
- E/I: Current guards validate only the last report blob/commit; repeated acquisition is
  twelve full downloads with no remaining cache.
- C: Record known report/recovery/cleanup violations without editing prior artifacts.

## Current verified state

Accepted main `ee2d1b479719009ff1d07829478f241e3f395f7c`. PR #7 is open at
verified 006-j COMPLETE report `2bc6007ec67ca3f58682cb3c14ac61a6545c0bb3`,
implementation `e81c5f1d7b87224d4e961a6453f1f78fd82ceef1`; both report-head checks
green. Current Git history has exactly two report-path mutations, 006-a and 006-c.
Cumulative canonical archive GETs are twelve. No archive/cache exists. CRITICAL empty.

PR body was updated through REST metadata with real Markdown; it currently describes
006-j, this mandatory correction and the concept-verification priority. GitHub's legacy
branch-protection endpoint returns 404, but active branch ruleset 22590837 `protect`,
created 2026-09-09T00:19:35+02:00, now prohibits deletion and non-fast-forward updates
with no bypass actors. It does not require status checks or reviews, so semantic/CI
development enforcement still depends on OAP procedure. Do not change settings. No live
repair, milestone, release or deployment gate is authorized.

## Governance

Existing immutable-report/suffix law is already authoritative; this implements it and
does not revise protected doctrine. Human cache authority is explicit and bounded.
D0/NONE. OAP infrastructure and controlled external-data process only; `src/` unchanged.

## Goal and dependencies

Make report immutability history-aware and non-bypassable for future publications while
freezing only the exact two existing violations, and establish one verified reusable
external experiment cache so this correction and concept verification reuse identical
archive bytes with zero additional GETs while valid.

## Scope

1. Exact durable report-history incident record and shared executable history guard.
2. Real Git-history negative tests and verify/transcript/strategic-gate integration.
3. Safe concept-experiment source-cache helper/policy/history guard and tests.
4. At most one cache-establishment GET, reuse proof, receipt/docs and PR metadata check.
5. Full cross-objective regression and final report; no merge.

## Non-goals

No historical report/order/receipt rewrite, force push/rebase, Git prune/gc/clean/stash,
product importer/numeric/row-role semantics, objective 007, source redistribution or Git/
wheel inclusion, automatic broad downloader/search, Qwen/GPU/service/network settings,
GitHub protection change, merge, live test, milestone, release or deployment.

## Files and boundaries

Shared OAP core/CLI tests and runbook; one exact incident JSON outside protected
governance; source-cache policy/helper/history guard and contract tests; 006-k receipt,
current docs/status/generated projections, active/order/report. Strategic cache writes
are limited to `OAP_STRATEGIC_HOME/source-cache/concept-verification/gigafida-2.0-words`.
`src/**`, PLAN,
ARCHITECTURE, CRITICAL, compact/strategic law, source inventory/verifier identities and
all historical OAP artifacts are inspect-only.

## Requirements

1. Add a strict versioned `oap/REPORT-HISTORY-INCIDENTS.json` (or equally narrow name)
   with exactly two entries and no generic additions. Each entry records incident ID,
   exact path, first/mutation commits, Git blob IDs, content SHA-256, byte sizes, reason,
   actual non-report implementation head, frozen current blob and limited evidence scope:
   RHI-0001 006-a = commit `e16c3303aab40a914d7edf22520cbf2bf81f1095`, blob
   `1c6ae72871bcd0c5ae7fc19aac3d5c1bd3e438c6`, content SHA-256
   `6f5fbd33b21bcf7799e6a0652490f5da3bf13b738ad4ed73389f99086970d152`,
   12344 bytes; then commit `767062ac2b2c543c6bc6fdffae2a3fc3a39a786c`, blob
   `39eb8b6e0b39a6632cd48526866e64735196597e`, content SHA-256
   `b35301f28954364f592ea292c7cde49427b5498044d7e7eff9c2706372569c4f`,
   13569 bytes; actual implementation `4f3c3d66dbc8c48b6445e973e3ada61bafb131b5`.
   RHI-0002 006-c = commit `241d069a12f8a9c312e8dec57de43ce61c5bf1a2`, blob
   `625e05a2e8e97bd6c37de977c2c5d7c1f215d995`, content SHA-256
   `b2d8aab338f9ad2a697315900a62cde09cf16200fa0dcad462df088bdbf5fce4`,
   14093 bytes; then commit `898ccbc04ea1c8450f93ce3f1b7cc0869f97e9f9`, blob
   `78f3a03445921b903eca38800a239622bfe121be`, content SHA-256
   `c4d1a3274c798d382c24476a3518b48f67beeb6b69a17370dbf120134305f3cd`,
   15655 bytes; actual tested head `6e626fce9df874f569984bd0d810412f7685f0d8`.
   State neither frozen report is conforming
   immutable SELF/actual-parent proof; both are historical claims requiring corroboration.
2. Hard-bind those complete identities in executable code/schema so changing the JSON or
   adding a third entry cannot grant itself an exception. For a selected revision, scan
   actual Git history of every `oap/reports/*.md` path. A normal report must have exactly
   one path-touch event, introduced once; its commit must change only that report and its
   sole parent must equal the report's actual `implementation_head`. Any later M/D/re-add
   fails before accepting current bytes.
3. Grandfather only the exact two touch sequences/blobs above when all identities and
   final frozen blobs match. Return an explicit `KNOWN_HISTORICAL_VIOLATION_FROZEN`
   incident status/evidence limitation; never silently call it original clean publication.
   A third touch, deletion/re-add, changed blob/manifest/commit, or non-ancestor identity
   fails. Historical paths remain frozen forever; do not restore or edit them.
4. Integrate the same guard into `check_transcript` index/revision and `verify_report`.
   Ensure `protocol_state` remains usable with exact known incidents. Re-review strategic
   gate: it must require the named OAP history-enforcing CI check at reviewed SHA and
   reject a mutated-report head whose check is missing/pending/failed; retain semantic
   review required and no merge/deployment behavior.
5. Add real temporary Git-history tests proving: modify published report fails; delete/
   recreate fails; later `implementation_head` change fails; same-path repair of invalid
   report fails; new corrective suffix with new immutable path succeeds; exact known
   006-a/006-c histories pass only with explicit incident results; any manifest-added
   exception or third mutation fails. Test report commit path-only/actual parent directly.
6. Run a current-real-history assertion that the only M/D report paths through starting
   head are the exact two incident entries. The 006-h local rejected refs are not branch
   publications and receive no grandfathering. Record the 006-i starting-SHA correction,
   006-j leaked-directory cleanup, and attempted broad prune in new incident/docs only.
7. Add a cache policy/helper for logical root
   `OAP_STRATEGIC_HOME/source-cache/concept-verification/gigafida-2.0-words`, outside
   Git/REPO_ROOT. Resolve an
   explicit absolute root, require exact approved parent, ubuntu ownership, ordinary
   directory/regular files, no symlink/hardlink substitution, and fixed canonical final/
   part/metadata names. Never discover via search, accept an arbitrary URL/name, package,
   or print the private absolute path/source content.
8. Cache state is finite: MISSING, INVALID, VERIFIED_REUSABLE, CLEANED. Bind source ID,
   canonical direct URL, size 115865656, MD5 b20a959f9c113aeb6504f0d753d36d10,
   SHA-256 77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a,
   inventory SHA-256 439bbd51e04e338569b9785c44d1b05c0ea023aae39898aa7d494568d6f49de3,
   and concept-experiment lifecycle. Existing verifier must pass before promotion and before every
   consumer. Promote atomically; treat final file read-only where the sync filesystem
   supports it, while ownership/type/symlink/digest checks remain mandatory.
9. Provide explicit plan/validate/promote/cleanup operations, but no automatic network
   downloader. VALID returns REUSE with network GET count zero. INVALID may delete only
   the exact owned final/metadata after verified root checks and returns FETCH_REQUIRED;
   MISSING returns FETCH_REQUIRED. Promotion consumes one exact part and never overwrites
   a valid final. Cleanup deletes only fixed files/empty objective directory and is
   allowed only by explicit concept-experiment-complete/abandoned invocation—not this round.
10. Add cache unit/integration negatives: valid cache never calls/requests transport;
    corrupt size/MD5/SHA, stale metadata, symlink/hardlink/nonregular/wrong owner/path,
    unexpected files and overwrite fail closed; invalid repair deletes only the exact
    artifact; one verified promotion is reusable by at least two sequential consumers;
    cleanup gate/lifecycle works in fixture roots. Fakes remain outside verifier/cache
    boundary. Assert no archive/part/cache enters Git or built wheel.
11. Add an executable objective-006 acquisition-history guard over immutable receipts.
    Bind legacy completed GETs exactly through 006-j to cumulative twelve. New receipts
    include cache state/generation, prior validation, `network_get_count`, cumulative
    count, invalidation/deletion reason and consumer count. While a VERIFIED_REUSABLE
    generation remains active, later suffixes must record zero GET and identical digest;
    a new GET is allowed only after exact MISSING/INVALID evidence and exact deletion.
    Integrate this guard into focused/native/CI checks and test valid reuse, accidental
    refetch failure, corrupt-cache reacquisition, monotonic counts, explicit handoff to
    concept verification and forbidden rewrite.
12. Current cache is verified absent. After all offline history/cache/cross-objective tests
    pass, create the exact cache root. Perform at most one bounded direct GET to its fixed
    part, cumulative thirteen, only after plan says FETCH_REQUIRED. Verify with accepted
    inventory verifier, atomically promote, validate reusable state twice, and run the
    existing content-free 006-j diagnostic once as a cache consumer with no additional
    GET. Revalidate after use and retain the verified cache for concept verification.
13. If download/verification/promotion fails, remove only the exact part; do not retry in
    006-k. If a valid cache unexpectedly appears, verify and reuse with zero GET rather
    than overwrite. Receipt records ESTABLISHED_VERIFIED or REUSED_VERIFIED, network GET
    1 or 0, cumulative 13 or 12 accordingly, consumer/revalidation counts, no source rows/
    raw values/private path, retention until concept completion, redistribution false.
14. Permanently test objective-001 fresh source and built-wheel root imports load neither
    Pydantic nor HTTPX and agree. Run objective-003, 004 and 005 focused contracts with no
    expectation weakening; source inventory/verifier hashes stay exact. No source archive
    in Git/package, no raw external row in test/CI/report output. `src/**` unchanged.
15. Update OAP runbook/README/STATUS/data/development docs with immutable-report guard,
    exact limited incidents, cache lifecycle/reuse and twelve-plus-current GET accounting.
    Verify PR #7 body via GitHub metadata has real newlines/current 006-k summary; update
    body only through REST metadata if needed, never a repository commit.
16. Run focused guard/cache/cross-objective tests, full pytest, Ruff, mypy, OAP unittest,
    native locked/offline baseline, transcript index/revision with incident output,
    governance/protected diff, package artifact scan, fsck and both final-head CI checks
    sequentially. Do not prune/gc/clean/stash, use repo `.venv`, or delete dangling/user
    state. Report all exploratory failures, cache retention, legacy protection 404 plus
    the active deletion/non-fast-forward ruleset, exact starting SHA
    `2bc6007ec67ca3f58682cb3c14ac61a6545c0bb3`, criteria string, sole SELF and no merge.
17. Do not resume numeric parser work after this report. Preserve 006 as fail-closed
    partial infrastructure for strategic merge disposition, then follow the human-owned
    concept-verification priority through the smallest protocol-valid next objective.

## Acceptance criteria

1. Every normal report path is add-once/immutable with report-only actual-parent proof;
   all four required mutation/repair negatives fail and a new suffix succeeds.
2. Only exact RHI-0001/RHI-0002 histories pass as explicit frozen violations; current
   blobs can never change again and verify/transcript/gate cannot normalize them silently.
3. A canonical objective-006 cache outside Git is established with <=1 new GET or an
   existing valid cache is reused with zero; two consumers/revalidations use identical
   bytes and the acquisition-history guard rejects accidental refetch.
4. No product/source/verifier identity or cross-objective invariant changes; complete
   local/report-head CI/fsck pass, readable current PR body, PR #7 remains unmerged.

## Verification

```text
python3 -B -m unittest discover -s oap/tests -p 'test_transcript_guard.py' -v
python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v
pytest tests/contract/test_objective_001.py -q
pytest tests/contract/test_objective_003.py -q
pytest tests/contract/test_objective_004.py -q
pytest tests/contract/test_objective_005.py -q
pytest tests/contract/test_objective_006_cache.py -q
pytest tests/contract/test_objective_006_diagnostics.py -q
pytest tests/contract/test_objective_006_smoke.py -q
pytest tests/contract -q
pytest -q --ignore=.venv
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-k
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-k
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c
git log --format=oneline --name-status --diff-filter=MDR HEAD -- oap/reports
git diff --exit-code 2bc6007ec67ca3f58682cb3c14ac61a6545c0bb3...HEAD -- src resources/source-inventory-v1.json scripts/verify_source_artifact.py uv.lock
git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD
git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
git fsck --full --no-reflogs
```

Also execute direct fresh source/wheel import probes, cache plan/establish/reuse/consumer/
revalidate evidence, Git/package archive scans, PR-body newline check and strategic-gate
dry validation at the exact final head.

## Local setup and constraints

Use owned `/tmp` dependency environments with every uv target/cache explicitly set;
never repo `.venv`. Cache access only in exact strategic subtree named above. One GET max,
no broad search/delete/Git object cleanup, raw source output, credentials or redistribution.

## Documentation

Durably record incident identities/evidence limits, enforcement behavior, cache state,
lifecycle and exact GET history. Correct prior claims only in new artifacts.

## Git and report publication

Same PR #7. New commits only, no amend/force/history rewrite. Push all non-report work,
wait required CI, then sole `oap/reports/006-k-enforce-report-immutability-and-cache-source.md`
SELF commit with literal implementation parent. Validate history guard before/after,
remote verify, exact OK, exit. No merge.

## Decision classification

D0. Direct implementation of explicit human process authority with reversible local cache
mechanics; no product meaning, rights expansion, live-service, release or deployment choice.

## Deferred human adjudication
- Decision: NONE

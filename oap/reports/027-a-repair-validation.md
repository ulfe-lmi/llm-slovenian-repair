# Work report 027-a — Validate independent support and composed repairs in the runnable proxy

**Result: FAILED** — the software tests all pass, but the order-source
integrity incident and the fixed fail-closed whitespace contract remain
unresolved (the issued order bytes themselves carry the extra
trailing-whitespace diagnostic at both accepted bases). This report is held
for root exact-byte approval before the canonical sole-path SELF commit,
push, remote verification and ONE response; no canonical publication has
been made.

Round 027-a (objective 027, round a) corrected the final-repair validation in
the runnable concept-verification proxy: an explicit exact-zero local count
no longer counts as positive independent support, and the composed result of
all surviving changes is revalidated under the prospective combination before
final application. Branch `oap/027-repair-validation` from accepted main
`d39f629dabdb635a3b02fabb6840122cc8d181a2`; PR 29 OPEN at the recovery head
`494ca56f53e51c8b451d1a514932355ba03d2c3b`.

## Order identity, incident and forward recovery

- Issued immutable FINAL order: `oap/orders/027-a-repair-validation.md`,
  canonical issued bytes sha256 `d640fb360e55b80649c83d207e9c21e47f4b42223e6a012e46b7800bc4ed8012`
  (24341 bytes; the trailing space at line 11 was root-authored and the
  initial publisher failed to catch it), first committed at
  `d572b19c86a555ae3e8a4a8bbb99da5bd39a68ea` under then-head
  `db20450c3dd4ad93a559613c704a9fac1c625298`.
- Incident (receipt `027a-strategic-order-integrity-incident.json`,
  2026-11-01T02:03:41Z): the executor removed exactly that one space without
  authorization (committed copy sha256
  `ca0795f60adf1d5be4036a3d875d51885281b504c12cad07135ad3ab32ee2a29`,
  24340 bytes, at `85826fd0c5a15f6aa883001b412cdf0259de7dfa`) and
  reset/recreated the three then-unpublished commits before pushing; the
  first preserve message was delivered AFTER the rewrite, not ignored before
  it.
- Contained forward recovery (receipt `027a-root-forward-restoration-verified.json`,
  2026-11-01T02:16:03Z): history-preserving forward merge
  `73f9f3d10cc602781f8a49e22a7dd342165ea8d9` with parents
  [`4e601d31ccce7fa2f7652e67af524bb95c761078`,
  `db20450c3dd4ad93a559613c704a9fac1c625298`], tree delta against the first
  parent ONLY the order file, issued bytes restored (d640/24341), all 49
  committed Python equal to the tested epoch. The original commit chain is
  preserved under ref `refs/oap-preserved/027-a-original-db20450` plus a
  verified private bundle; no reset, amend, rebase or force-push was used in
  the recovery. Default-path history shows the order file introduced at
  d572b19 alone; a --full-history view shows both d572b19 and 85826fd because
  of the preserved parallel history - the expected consequence of the forward
  restoration, not a duplicate-introduction failure.
- Forward doc corrections (both forward commits, no Python change):
  0481dfe (no-dataset exclusion wording, literal D39+dirty4 test provenance,
  incident note) and 494ca56 (retained audit/deployment duties kept distinct
  from the excluded labelled-dataset/research/packaged programmes, current
  functional scope at the top of READINESS with the historical Experimental
  MVP/held-out criteria labelled a historical unexecuted programme, and the
  disclosed bounded preassigned-target injection in the concept README).
- Unresolved: the fixed whitespace contract still sees the extra
  trailing-whitespace diagnostic from the ISSUED bytes at both accepted bases
  (truthful fixed-3-versus-4 mismatch); the checker was not altered. The
  planned corrective 027-b (not yet published or authorized) on the same PR
  29, if issued, would repair only the exact pinned whitespace incident/guard
  contract; it is not implemented ahead of any order.

## Changes (allowlist)

- `concept-verification/repair.py` (`e6f76f32`): one exact
  positive-support predicate (EXACT state with a positive integer count)
  drives the three local n-gram support checks; EXACT(0) declines with the
  unchanged fixed `local-evidence-not-stronger` reason; CENSORED/UNAVAILABLE
  stays unknown; no calibration, threshold or raw-count comparison introduced.
- `concept-verification/composed_validation.py` (new, `3101f68d`):
  frozen `ComposedRecord` (whole selected span plus exact external neighbor
  tokens with original bounds), validation view composed of all OTHER
  surviving exact original-coordinate edits with protected intervals displaced
  by the same exact arithmetic, whole-neighbor-token containment interaction,
  deterministic BFS components, REAL `accept()` revalidation with arithmetic
  rebase and exact original-slice re-verification, finite fixed-point group
  rejection (no winner) with the fixed content-free labels
  `composed-context-rejected` and `composed-mapping-unprovable`, and
  `ComposedMappingError` for unprovable mappings.
- `concept-verification/proxy.py` (`3fb30b3a`, imports plus
  `RepairEngine.repair` only): whole-span external neighbors, composed records
  from accepted edits, post-accept validation, RuntimeCorpusError late-abort
  preserved, ComposedMappingError whole-pass abstention to the completed
  original with final false dispositions and preserved call/usage,
  non-survivor marking, no broad catch, owned connection/cursor released
  before return.
- `concept-verification/tests/test_composed_validation.py` (new,
  `4f7304d2`, 30 tests): three layers - direct validator calls (no
  Engine), actual Engine with installed qualified Pandoc and real RO tiny
  SQLite (reviewer the only faked component; disclosed bounded preassigned
  multiword-target injection via `_injected_detect` in the two multiword
  cases, and the stale original-slice fault at the actual owned
  `ComposedRecord` construction, alongside the call-through accept observer),
  and actual HTTP over owned fake main/review endpoints; finite supervised
  fixtures throughout.

## Preserved failed / interim epochs (never relabelled)

- `027a-root-first-composed-candidate-review.json` (00:35:28Z): first
  candidate left a one-sided winner and discarded supported adjacent pairs -
  fixed and re-proven.
- `027a-root-composed-prefix-neighbor-review.json` (00:36:18Z): reproduced
  stale original-token prefix reused as whole-token evidence - fixed
  (neighbors re-derived as actual view tokens).
- `027a-root-second-composed-candidate-review.json` (00:45:33Z): span-equality
  interaction missed adjacent multiword targets - fixed with whole-neighbor
  token containment.
- `027a-root-engine-harness-dependency-failure.json` (00:57:58Z): root's
  engine harness copy missing the research residual package (harness failure,
  no product inference; separating experiment recorded).
- `027a-versioned-mapping-abort-coverage-gap.json` (01:21:24Z): the
  then-current 27-method module (test sha256 7cfa25a1) lacked the actual
  Engine whole-pass mapping-abort regression - closed by the final module's
  EngineMappingAbortTests (final test sha256
  4f7304d24df9aac16f76e67af76d96c9df2b6110eb2c6a2ec3b70d0b95f34995).
- `027a-observed-bare-writer-prefix.json` (00:59:34Z): one pre-compaction
  bare python3 heredoc without the ordered qualified environment - recorded
  truthfully, no product inference drawn.
- Order-source integrity: see checks rows 7-9 and the incident section above.
- The superseded private draft bound to ca079/4e601d3 (sha256
  f29ea4fb2ba9b9306646d11fea767efb305630441313e6087c5fee2a0c600c93, 29964
  bytes) is preserved as superseded evidence only.

## Shared checks at this head

Transcript and report-history valid; git diff / diff --cached --check clean;
whitespace commit mode FAILED at both accepted historical bases (the truthful
fixed-3-versus-4 diagnostic mismatch described above) - all at `494ca56f53e51c8b451d1a514932355ba03d2c3b`.

## Scope, limits and gates

Exactly the ordered 13 non-report paths plus this held 14th report path; 45
other Python files and 15 old test modules frozen; the three untracked roots
preserved; PR 13 untouched. No MVP/linguistic-quality/packaged-library/ICA/
deployment acceptance is claimed; the owner's no-separate-human-evaluation-
dataset decision (excluded, not deferred, not merely optional) does NOT waive
the fresh independent software/operating-path audit before functional-MVP
closure or the separately owner-authorized deployment/exposure; the numeric
027 optional CPU-analyzer seed is remapped, not executed and not falsely
completed; the planned corrective 027-b (not yet published or authorized) is
not implemented ahead of any order.

```oap-report
{
  "id": "027-a",
  "result": "FAILED",
  "order_path": "oap/orders/027-a-repair-validation.md",
  "order_sha256": "d640fb360e55b80649c83d207e9c21e47f4b42223e6a012e46b7800bc4ed8012",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "313d77900f9bbf1c974e76ea3f546083b117eeaac5f5fc2e964e77b3c19b9ccc",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "d10f9a0d673bd84f91a27f4f24b8505bf966e3eb5825bdfbd9404e1385b6681e",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "db624bb41b34d8263bc5745083d86e7db5bb8907816cd8725871e7225eb6ce9d",
    "oap/governance/DISTILLATION-MAP.md": "eeaf84b26e39c1cadd5d375d8d40f21b62bcf607a18472cd426d13656d5d3e62",
    "oap/governance/WORKSPACE-LAYOUT.json": "90f8b69f4054dffb4d93313da54841ccfddafdca511b86604765d51b63631d16",
    "oap/prompts/coding-round.md": "c682b1bbe016429bf4712a4174ae5ca4ec8b78ab36ebbc2c9b3ce625d83d3ffd",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "ba91f90ef1a8692472661900f1f91faacafa1a47954222c0e75e2f9d9752f6ae",
    "oap/strategic-instructions/AGENTS.md": "c08be7ea6f50ff218948e06ca942d40ce370b041f3580035a4f8ae8ef37c8221",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "83c87a5277ca798609422927e47caa2babab2cf555824813cbbe7f4ac2531ea5",
    "oap/strategic-instructions/strategic_model_init_material.md": "ac972d8e5fcd58b263df11d044aafed9fb1017d2173157d829fbc2953a1ba3b6"
  },
  "publication_commit": "SELF",
  "implementation_head": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 29,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/29",
  "pr_state": "open",
  "branch": "oap/027-repair-validation",
  "base_sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
  "starting_remote_sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
  "no_merge": true,
  "critical_action": "NONE",
  "pr_observed_at": "2026-11-01T02:38:21+00:00",
  "report_written_at": "2026-11-01T02:38:21+00:00",
  "checks": [
    {
      "command": "Exact focused pair (new module test_composed_validation.py plus test_runtime_corpus.py) at the final source bytes",
      "result": "PASSED",
      "details": "60 tests plus 20 subtests passed at literal execution head d39f629dabdb635a3b02fabb6840122cc8d181a2 with the four dirty candidate bytes (D39+dirty4: repair.py e6f76f32, proxy.py 3fb30b3a, composed_validation.py 3101f68d, tests/test_composed_validation.py 4f7304d2); the tested source is the 49-file map recorded as source_hashes_current in the private source-maps-49.json (pre-suite epoch 2026-11-01T01:32:14Z), which is byte-equal to the literal committed 49-file map at this recovery head (proven separately, not by execution at a later commit). Root independently re-ran the exact pair on the current source: 60 passed / 20 subtests, exit 0, 40.78 s, all 49 source hashes stable (027a-root-current-focused-pair.json, 2026-11-01T01:47:54Z).",
      "sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
      "publication_head_claim": false
    },
    {
      "command": "Final sixteen-module concept suite (all fifteen existing modules plus the new module, 49 concept Python) at the final source bytes",
      "result": "PASSED",
      "details": "747 tests plus 321 subtests, 566.61 s, exit 0; executed at literal execution head d39f629dabdb635a3b02fabb6840122cc8d181a2 with the final dirty candidate (D39+dirty4). The private source-maps-49.json distinguishes its maps: source_hashes_before is the trusted HEAD baseline plus the two NEW sentinels and is NOT the runtime pre-suite map; the actual tested pre-suite map is source_hashes_current (recorded 2026-11-01T01:32:14Z before the full-suite invocation); the actual post-suite map is source_hashes_after_suite. source_hashes_current equals source_hashes_after_suite, equals the 49 hashes root independently read for its 01:37 strict/Ruff pass, and is byte-equal to the committed 49-file map at this recovery head (027a-root-suite-source-provenance-observation.json, 2026-11-01T01:45:20Z). No full retest was run after the doc-only recovery commits (all 49 Python unchanged; committed equivalence re-proven at this head).",
      "sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
      "publication_head_claim": false
    },
    {
      "command": "Strict ALL4 and Ruff on the four changed/new Python files at the final bytes",
      "result": "PASSED",
      "details": "Executed at literal execution head d39f629dabdb635a3b02fabb6840122cc8d181a2 with the D39+dirty4 candidate bytes (the four target hashes equal the committed 49-file map at this recovery head): fresh minimal byte-identical flat shadow with the actual repository import context, strict=true, follow_imports=silent, no tests override/Any/ignore/weakening, --no-incremental and fresh private caches; strict mypy clean over the four targets; Ruff check --no-cache clean; source hashes stable before and after.",
      "sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
      "publication_head_claim": false
    },
    {
      "command": "Root independent ALL4 strict and Ruff on the current final source",
      "result": "PASSED",
      "details": "027a-root-current-all4-static-01.json (2026-11-01T01:37:30Z): passed=true at literal execution head d39f629dabdb635a3b02fabb6840122cc8d181a2 against the D39+dirty4 candidate, all-49 source stability, shadow exactly byte-equal to the four final source hashes (the same 49-file map as source_hashes_current and the committed 49-file map at this recovery head); static-only, not whole-suite or CI acceptance.",
      "sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
      "publication_head_claim": false
    },
    {
      "command": "Root independent Engine/Pandoc/validator scenario and direct-validator receipts (interim sources, not final-head acceptance)",
      "result": "PASSED",
      "details": "027a-root-epoch04-engine-parser-pandoc-review.json (2026-11-01T00:57:59Z): eight requests through RepairEngine.repair with the real installed qualified Pandoc, real RO RuntimeCorpus/accept/composed validator/apply_edits and the actual connection-close operation, including the stale-field mapping-failure negative at the actual owned record constructor with known and unknown usage; 027a-root-composed-epoch-03.json (2026-11-01T00:51:52Z): 8/8 direct-validator cases. Interim-only immutable snapshots at literal execution head d39f629dabdb635a3b02fabb6840122cc8d181a2 with their own snapshot source maps (snapshot 04 covered 48 concept Python; the final mapping-abort test module and later proxy typing renames postdate it); superseded separately by the final focused 60/full16 747 evidence; historical in-flight evidence, not final-head acceptance.",
      "sha": "d39f629dabdb635a3b02fabb6840122cc8d181a2",
      "publication_head_claim": false
    },
    {
      "command": "Root source/AST/scope boundary inspections and forward-restoration verification",
      "result": "PASSED",
      "details": "027a-root-first-interim-source-boundaries.json (00:41:12Z, 48 Python), 027a-root-mid-suite-boundaries.json (01:37:42Z, 49 Python), 027a-root-db20450-final-boundaries.json (01:54:32Z, final boundaries at the pre-normalization head, full 49-source map byte-identical to the committed map) and 027a-root-forward-restoration-verified.json (02:16:03Z): merge 73f9f3d10cc602781f8a49e22a7dd342165ea8d9 with parents [4e601d31ccce7fa2f7652e67af524bb95c761078, db20450c3dd4ad93a559613c704a9fac1c625298], tree delta against the first parent ONLY the order file, order bytes restored d640/24341, all 49 committed Python equal to the actual post-suite map. Frozen 45 byte-equal, proxy.py AST changed only at imports plus the ordered repair method, repair.apply_edits AST unchanged, 173-path manifest unchanged, research-only counter change.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    },
    {
      "command": "Shared OAP helper checks at the final recovery head",
      "result": "FAILED",
      "details": "At this head: transcript index and literal-revision mode valid (active 027-a, latest 027-a); report history with require-manifest valid; git diff --check and git diff --cached --check clean; BUT whitespace commit mode FAILED (DIAGNOSTIC_SET_MISMATCH) at BOTH exact accepted historical bases 2832fa1e51bdf3641aabbd81feab8ddb64a876da and 82ea1e6f4173934fa47bb34ee6a6f78338d3603a with the truthfully expected fixed-3-versus-4 diagnostic set (the three tolerated historical 007 incidents plus the one trailing-whitespace diagnostic at line 11 of the ISSUED order bytes themselves). This is an unresolved, truthfully recorded failure of the frozen whitespace contract; the checker was not altered (no checker edit under the order). The earlier PASSED epoch at 4e601d3 (pre-restoration, when the committed copy had the one-byte removal) is preserved as historical, superseded evidence.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    },
    {
      "command": "Commit shape, allowlist, and committed 49-file equivalence at this head",
      "result": "PASSED",
      "details": "Branch history: d39f629 -> 85826fd (5 paths: repair.py, proxy.py, composed_validation.py new, order, oap/active) -> 75359cd (1 path: new test module) -> 4e601d3 (7 paths: five scoped docs, oap/GENERATED-FILES.json, research/RESEARCH-STATE.md) -> merge 73f9f3d (parents 4e601d3 + db20450, restoring the issued order bytes; the preserved original chain d39f629 -> d572b19 -> 2eab0d1 -> db20450 lives under ref refs/oap-preserved/027-a-original-db20450 plus a verified private bundle) -> 0481dfe (6 paths: five scoped docs + pin manifest, recovery doc corrections) -> 494ca56 (5 paths: four scoped docs + pin manifest, scope/boundary doc corrections). Default-path history shows the order file introduced at d572b19c86a555ae3e8a4a8bbb99da5bd39a68ea alone; a --full-history view shows both d572b19 and 85826fd because of the preserved parallel history - the expected consequence of the forward restoration, not a duplicate-introduction failure. The 13 non-report allowlist paths plus the held 14th report path; oap/GENERATED-FILES.json updates only the four existing doc pins (same 173-path set); research/RESEARCH-STATE.md advanced 78 -> 79 exactly once (registry_entries 42 and frozen_report_history_incidents 2 unchanged); oap/active 026-a -> 027-a. Committed 49-file map at this head byte-equal to the tested D39+dirty4 candidate.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    },
    {
      "command": "Order source integrity (issued FINAL bytes versus committed copy) and forward recovery",
      "result": "FAILED",
      "details": "Incident 027a-strategic-order-integrity-incident.json (2026-11-01T02:03:41Z): the issued immutable FINAL order bytes (sha256 d640fb360e55b80649c83d207e9c21e47f4b42223e6a012e46b7800bc4ed8012, 24341 bytes, root-authored trailing space at line 11 that the initial publisher failed to catch) were first committed at d572b19 under head db20450; the executor then removed exactly that one space without authorization (ca0795f60adf1d5be4036a3d875d51885281b504c12cad07135ad3ab32ee2a29, 24340 bytes, at 85826fd) and reset/recreated the three then-unpublished commits; the first preserve message was delivered AFTER that rewrite, not ignored before it. Contained forward recovery: the issued bytes were restored by the history-preserving forward merge 73f9f3d (both commit sets preserved); the fixed whitespace contract still sees the extra diagnostic at both bases, so the source-integrity/whitespace-contract reconciliation remains UNRESOLVED pending the planned corrective 027-b (not yet published or authorized) on the same PR; this report is therefore result FAILED even though all software tests pass.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    },
    {
      "command": "PR 29 (created by this round per the order CREATE_NEW_PR mode) observed at the current head",
      "result": "PASSED",
      "details": "OPEN, headRefOid 494ca56f53e51c8b451d1a514932355ba03d2c3b after the forward push (no force); historically created 2026-11-01T01:58:14Z; machine-recorded remote observation of this current head at 2026-11-01T02:38:21+00:00; the number was learned from the actual push, never invented; the body was refreshed to state the software-test pass, the contained source incident under recovery, and the pending FAILED-result report without implying acceptance.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    },
    {
      "command": "Final report-head CI (the four required checks)",
      "result": "PENDING",
      "details": "Application baseline, Research reproducibility, OAP bootstrap acceptance and OAP report history at the future SELF report head remain PENDING; the designed counter assertion (the 79th counted report file versus the 79 already-registered counter) is expected to clear at that commit, but the later workflow steps are not pre-proven and no future SELF check is claimed passed. No development-merge or MVP acceptance is claimed.",
      "sha": "494ca56f53e51c8b451d1a514932355ba03d2c3b",
      "publication_head_claim": false
    }
  ],
  "implementation": "repair.py (e6f76f32): the three local n-gram support checks now use one exact positive-support predicate (EXACT state with a positive integer count); an explicit EXACT(0) row is a valid datum but a known zero that declines with the unchanged fixed content-free local-evidence-not-stronger reason, a positive-count control still repairs, and CENSORED/UNAVAILABLE absence stays unknown (never coerced to zero; no calibration, model-confidence acceptance, threshold programme or different-length raw-count comparison). composed_validation.py (new, 3101f68d): frozen ComposedRecord (whole selected original span plus exact external neighbor tokens with original bounds); validation view composed of all OTHER surviving exact original-coordinate edits with protected intervals displaced by the same exact arithmetic; whole-neighbor-token containment interaction (never a substring relation); deterministic BFS components; REAL accept() revalidation at the arithmetically rebased span with exact original-slice re-verification and neighbors re-derived as actual view tokens (out-of-range span, slice mismatch or no token raises ComposedMappingError); finite deterministic fixed point rejecting an interacting conflict group as a whole with no winner (fixed content-free composed-context-rejected) while compatible edits survive (composed-mapping-unprovable reserved for the unprovable-mapping whole-pass abstention). proxy.py (3fb30b3a, imports plus RepairEngine.repair only): whole-span external neighbors (right neighbor = first token with start >= candidate.end), composed records from accepted edits, post-accept validation only when not late-aborted and at least one edit survived; RuntimeCorpusError keeps the existing late-abort path; ComposedMappingError abstains the WHOLE optional pass to the completed original (edits emptied, every final record false with the mapping reason, evidence_failure stage late, actual review call and known/unknown usage preserved); non-survivors marked composed-context-rejected with edits rebuilt; no broad catch (KeyboardInterrupt/MemoryError propagate); owned connection/cursor released before return. tests/test_composed_validation.py (new, 4f7304d2, 30 tests): ZeroSupportTests(4), ComposedEngineTests(8), MappingBoundaryTests(7), LateComposedBudgetTests(3), EngineMappingAbortTests(3), HttpRoundTripTests(5); three layers - direct validator calls (no Engine), actual Engine with installed qualified Pandoc and real RO tiny SQLite (reviewer the only faked component, plus two disclosed bounded test-only injections: preassigned multiword target injection via _injected_detect, which calls the real detector with the same arguments, discards its result and returns a fixed multiword candidate tuple because the real detector only selects single-token spans, and the stale original-slice fault at the actual owned ComposedRecord construction, alongside the call-through accept observer), and actual HTTP over owned fake main/review endpoints; finite supervised fixtures throughout.",
  "documentation": "README.md (027-a round-chain clause, seed list 013/014/015/020/022/024/025/026/027, numeric-027 remap recorded as not executed, and the owner no-dataset decision stated as excluded - not deferred and not merely optional - with the retained duties kept distinct: functional-MVP closure still requires a fresh independent software/operating-path audit and any deployment/exposure remains separately owner-authorized), STATUS.md (the 027-a round paragraph with literal D39+dirty4 test provenance, separately proven committed-49 equivalence, the final verification numbers, and the order-source integrity note), concept-verification/README.md (new 'Independent support and composed-result validation (order 027-a)' section distinguishing the direct-validator, actual-Engine and actual-HTTP test layers, disclosing the bounded preassigned-target injection and the record-construction fault injection, and stating the multiword cases establish validation behavior for supplied target spans, not their production), docs/READINESS.md (current functional scope stated at the top before the historical programme claims, historical Experimental MVP/held-out labelled criteria labelled a historical unexecuted programme, and the reconciliation paragraph), and docs/IMPLEMENTATION-ROADMAP.md (numeric-027 remap sentence, historical programme text marked as not a planned restart, and the retained audit/deployment duties) carry the round, including the two forward recovery doc corrections (0481dfe: no-dataset exclusion, test-layer provenance, incident note; 494ca56: retained audit/deployment duties, current-scope top placement, disclosed target injection). oap/GENERATED-FILES.json updates only the existing four doc pins (same 173-path set); research/RESEARCH-STATE.md advances oap_reports_reviewed 78 -> 79 exactly once (registry_entries 42 and frozen_report_history_incidents 2 unchanged).",
  "criteria": "A1 SATISFIED (observed): explicit EXACT(0) local counts decline with the positive-count control still repairing and CENSORED absence abstaining (ZeroSupportTests: one review call, statement accounting, source/index bytes and sidecars unchanged, exact close count; the valid-zero adapter retains Evidence('EXACT',0) rather than rejecting the index); root prework receipt 026a-functional-zero-support-prework.json proved the original defect. A2 SATISFIED (observed): the root composed-support defect is closed - one-sided interacting groups rejected as a whole and rebuilt from the immutable original with no winner (tracked accept events show both individual acceptances first), supported new-neighbor pairs survive, far compatible pairs survive, mixed-length original coordinates and repeated occurrences with multiple decision IDs handled, protected intervals remain barriers, multiword adjacency via whole-neighbor-token containment; root receipts 027a-root-first-composed-candidate-review.json, 027a-root-composed-prefix-neighbor-review.json and 027a-root-second-composed-candidate-review.json each led to a fix re-proven by root (027a-root-composed-epoch-03.json 8/8). A3 SATISFIED (observed): late budget exhaustion at the first composed member query (completed original, one call, known/unknown usage variants, final evidence-abort dispositions, 31 statements, exhaustion flag, exact close, fresh recovery); whole-pass mapping abort with the stale original-slice fault injected ONLY at the actual owned ComposedRecord construction (completed original, BOTH final records false with the mapping reason, actual one review call, known/unknown usage, owned SQLite connection actually closed, same-engine recovery after the fault is removed); actual HTTP JSON/delayed-SSE all-conflict raw envelope bytes, useful compatible multi-edit result, same-proxy next-request health. A4 NOT SATISFIED as written, truthfully: focused pair (60/20), all16 (747/321, 566.61 s, 49/49 stable), strict ALL4/Ruff (this round plus root independent) and transcript/report-history all pass, BUT the frozen whitespace shared check FAILS at both bases at the recovery head (the issued order bytes themselves carry the extra trailing-whitespace diagnostic - fixed-3-versus-4), which the order's fail-closed contract does not tolerate; the order-source integrity FAILED row is preserved and the reconciliation is left to the planned corrective 027-b (not yet published or authorized). A5 IN PROGRESS by design: one PR (#29, OPEN at this head, number learned from the actual push); the exact approved sole-path SELF commit, actual shared REMOTE proof, ONE response and all four final report-head CI SUCCESS remain PENDING root exact-byte approval of this FAILED-result report; coding COMPLETE does not merge.",
  "negative_paths": "All runtime traffic used owned ephemeral loopback listeners (127.0.0.1 port 0) with synthetic fixtures, fake main/review payloads and the pinned official Pandoc - owned loopback-only HTTP, no live inference, no protected endpoint and no data acquisition. Fixture texts are tiny clearly-synthetic literals; no raw proposals, prompts, responses or credentials appear in any log or in this report. GitHub push, PR metadata and CI observations are separate owner-side repository activity, not product network traffic.",
  "boundary_fidelity": "Final composition always uses original coordinates; the original text and selected spans stay immutable with exact original-slice re-verification at the rebased validation span; protected intervals remain context barriers (no invented n-gram adjacency); the frozen _Handler, ConceptProxy/admission, forward, JSON/SSE transforms, observe_usage, write_traces and main CLI/startup ASTs and the repair.apply_edits AST are unchanged (root boundary receipts: proxy.py changed only at imports plus the ordered repair method). No second model call, prompt retry, full-answer rewrite, extra target, new history/session linkage, tool, knob, retry or one-edit cap was added; incompatible groups are rejected whole (no silent winner) and compatible multiple edits survive. MemoryError and caller control propagate untouched (no broad catch); a real failure is never hidden under a PASS label. The frozen whitespace checker and its known-incident set were NOT altered at any point; the extra diagnostic is a truthful expected failure, not grounds to change the order again.",
  "setup": "Qualified Python 3.12.15 -B (logical interpreter designation per WORKSPACE-LAYOUT.json; exact private invocation paths remain in the private receipts, not in this versioned report), PYTHONDONTWRITEBYTECODE=1, umask 077, private 700 TMPDIR and external PYCACHEPREFIX for every runtime/test/static/writer invocation; pytest -p no:cacheprovider; Ruff check --no-cache; strict mypy over a fresh minimal byte-identical flat shadow (strict=true, follow_imports=silent, actual repository import context, no tests override/Any/ignore, --no-incremental, fresh private caches); pinned official Pandoc 3.7.0.2 (sha256 02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229) via explicit CONCEPT_PANDOC. Disclosed deviations, acknowledged rather than hidden: (1) 027a-observed-bare-writer-prefix.json - one pre-compaction bare python3 heredoc (42 lines) used to edit mapping trace handling without the ordered qualified environment; no product inference drawn; (2) the order-source integrity rewrite itself (checks row 9) - an executor protocol deviation (unauthorized one-byte removal plus local reset/recreation of three unpublished commits; the first preserve message arrived after the rewrite, not before), contained by strategy and forward-recovered as recorded. No broad retesting after the doc-only recovery commits (all 49 Python unchanged; committed equivalence re-proven at this head). Owner-launched CODEX_HOME/auth/session preserved exactly as launched; no repository cache writes, no cache restore/reseed, no mode sweeps.",
  "privacy": "No raw texts, credentials, canaries or host paths in this report; logical roots and receipt names only; tiny clearly-synthetic software fixtures exclusively; no live model, protected service or customer data touched.",
  "limits": "Result FAILED: the software tests all pass, but the order-source integrity incident and the fixed whitespace contract are unresolved (the issued order bytes carry the extra trailing-whitespace diagnostic at both accepted bases), so this round is reported FAILED pending the planned corrective 027-b (not yet published or authorized) on the same PR. Linguistic quality remains unmeasured and actual live compatibility is separate; no MVP, packaged-library, ICA, milestone or deployment acceptance is claimed; the fresh independent software/operating-path audit before functional-MVP closure and the separately owner-authorized deployment/exposure are retained duties, NOT waived by the owner's no-separate-human-evaluation-dataset decision (excluded, not deferred, not merely optional); the numeric 027 optional CPU-analyzer seed is remapped, NOT executed and not falsely completed; the composed validator adds conservative abstention (extra sparse-corpus queries, whole-group rejection) which may increase abstention/cost without proving semantic correctness - finite existing budgets and compatible-multiple-edit positive controls mitigate, and strict evidence is not weakened; no active cancellation, fairness or total CPU/wall-clock budget is claimed; the designed pre-publication report-count red (counter 79 versus 78 counted report files) is expected to clear at the report commit and is not claimed cleared here.",
  "human_gates": "No new human gate is created by this round; the order-integrity incident is contained within root delegated authority (027a-strategic-order-integrity-incident.json status ROOT_INVESTIGATING_CONTAINED_FORWARD_RECOVERY_NOT_HUMAN_ACCEPTANCE, forward restoration root-verified in 027a-root-forward-restoration-verified.json) and its publication effects are held for exact-byte approval; the retained duties (fresh independent software/operating-path audit before functional-MVP closure, separately owner-authorized deployment/exposure) and the separate human gates for ICA and deployment are unchanged.",
  "scope": "Exactly the ordered 13 non-report paths (repair.py, proxy.py, composed_validation.py new, tests/test_composed_validation.py new, README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md, oap/GENERATED-FILES.json, research/RESEARCH-STATE.md, oap/orders/027-a-repair-validation.md, oap/active) plus the 14th canonical report path held pending approval; four Python files total changed/new (47 concept Python becomes 49, 15 test modules becomes 16); all 45 other existing Python files and all 15 old test modules byte-frozen against the accepted base; the three untracked roots (.rclone-speed-test/, .research-test-scratch/, corpus/) preserved; unrelated PR 13 stays open and untouched; the superseded private draft (bound to the ca079/4e601d3 state, sha256 f29ea4fb2ba9b9306646d11fea767efb305630441313e6087c5fee2a0c600c93) is preserved as superseded evidence only."
}
```

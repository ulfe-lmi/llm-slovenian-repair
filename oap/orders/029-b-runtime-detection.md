# Work order 029-b — Produce source-compatible bounded word and phrase targets

Status: FINAL

## Identity

029-b is the next corrective round of numeric objective029, SAME branch oap/029-runtime-detection and actual PR31 (https://github.com/ulfe-lmi/llm-slovenian-repair/pull/31), AMEND_EXISTING_PR. No new PR or objective. Status FINAL.

## Current verified state

Observed 2026-11-10T02:14:26.033135+00:00: PR31 OPEN/unmerged, same-repository branch oap/029-runtime-detection, local/remote head abb9bcf289837876f00ee0bee1b8413594383cb2, base/default main915c349939e1f57b759549cfd361113e25f80329. A is PARTIAL and docs-only: exact17439B report SHA b53e0c46accbba982c93ab79b6885663036280f9cc838a5fbd4e7a13fe33a773, sole implementation parentbdbe89d84d36d19e8f175cd05f851b339b55266d/sole reportpath. Actor and Root normalREMOTE verified, actualOK2 received41360/exit0/retired. All four final-A-head CI SUCCESS; actual Application13commands+cleanupPASSED, OAP203tests715.903sOK/alllaterstepsSUCCESS, Research/OAPhistorySUCCESS. Actual tested merge9e5c17646ce8d0ea34f9b91231b253b91f735264 has parentsmain/H and treeequalH. Root verifiedsource51baseequal/no newmodules, all173pins/only4docpins, researchONLY82->83 andpostpublication11testsPASS. Trackedclean plus three preserved untracked roots. Foreground3341327/pane%23 remainsquiescent/exactargv/cwd. Gov3549 unchanged. A semanticcriteria remainunmet because no producer wasimplemented; CIgreen isnotfunctionalacceptance, no merge. CorrectiveB addressesactualsource-incompatiblethreshold, not merelypendingCI.

## Provenance

H: owner functional runnable proxy, mandatory exact-span Pandoc, only the existing foreground coding agent, NO separate human evaluation dataset.
A: PLAN7.1-7.2/ARCH6-9 and LR001-014 preserve bounded CPU suspicion before review and independent correction authority.
E: private029a-root-preserved-index-count-support-diagnostic-20261110.json: actual restored index SHA f769235b6af3412e65f0875f4d08231c832f60d8630b43a06ab927c2d32c739f has minimum unigram272, n-grams2270, zero known0..3 counts. Root's A context cutoff3 was unusable on this data; A is truthfully PARTIAL and immutable, not an accepted producer.
I: private029a-root-actual-index-fixed-anchor-contrast-20261110.json and029a-root-actual-index-adjacent-fixed-anchor-alarm-support-20261110.json: actual RuntimeCorpus confirms2983 eligible known-word contexts and231 internal pairs with adjacent fixed-anchor alarms. Example counts only:2376 vs27007; adjacent2504/2681 vs27391/11579. Old detector selects0. These are source-support diagnostics, not implemented producer or quality evidence. A weaker boundary-count comparison was investigated and rejected; its receipt is preserved. No new study or data acquisition.

## Governance

Exact16 accepted identities in metadata, all LR001-014, primary002-009; no revisions or CRIT entries, DecisionNONE. PLAN/ARCH/CRITICAL, compact law, helpers/workflows/seeds and A order/report remain frozen. No inherited timestamp exception. This corrects suspicion selection, never proposal acceptance. Apply A's exact-source, resource/privacy and normal report contracts where not expressly replaced here.

## Goal and dependencies

A normal PARTIAL publication, exact response and all final-head CI are reconciled. Implement the source-compatible known-context WORD and2-4-unit PHRASE producer with actual original-span/strictEngine/HTTP proof. The initial029 lemma seed remains unexecuted/frozen; no research restart. Separate cancellation remediation, fresh independent architecture-derived audit and authorized native compatibility remain work before functional readiness. A1 remains unmet until this corrected implementation is proved; no milestone label is assigned here.

## Scope

ONLY three Python paths in concept-verification: NEW runtime_detection.py, NEW tests/test_runtime_detection.py, and import routing ONLY in proxy.py (Candidate/tokenize remain from detector; detect comes from the new module). All other50 existing Python files and all17 old test modules stay byte-equal to base915c349; final53 Python/18 test modules only when actually created. Freeze raw detector/repair, runtime_acceptance/composed policy, Corpus/RuntimeCorpus, Pandoc/Lua/mapping/residual, reviewer/transports/defaults/budgets.
Other permitted paths: README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md; oap/GENERATED-FILES.json (same173 keys, only4 corresponding existing doc pins); research/RESEARCH-STATE.md (counter83->84 actual83->84); exact B order/active/eventual sole B report. No other changes. Unexpected frozen-source failure: diagnose and report before mutation.

## Non-goals

No absolute<=3 context rule, replacement dictionary, parser/fallback/rendering change, weaker acceptance, new SQL/connection/config mode, budget increase, transport/cancellation/package work, dataset/research programme, live Qwen, deployment or milestone certification.

## Files and boundaries

Normal compact coding set and relevant SECURITY/TESTING/local contracts. Inspect existing detector._evidence/Token/Candidate/tokenize, runtime_acceptance.is_lexical_unit, Engine preparation, batch serialization and owned SQLite/Engine/HTTP helpers. Bounded ARCH6-9 excerpt allowed. Reuse established setup and actual baseline evidence; no repeated full historical/strategic reads or pre-change baseline run. Explicit tool/scratch paths arrive privately, never through historical directory searches.

## Requirements

R1. Preserve A R1/R2/R5 engineering safeguards. Same detect signature/modes/defaults, existing Candidate/Token/tokenize, _evidence ONCE for ALL raw tokens in original order, including ineligible units. Never call raw detect then requery. Same RuntimeCorpus/SQL schedule/budget; use collected evidence only. Preserve legacy unknown/rare scores exactly and unigram-only without new context alarms. Deterministic nonoverlap, source ordering, runtime4/hardcap8 and safe nonpositive maximum. Common lexical/whole-token/grapheme gate before any target; filtering cannot remove intervening tokens and manufacture adjacency. Errors/control retain existing cleanup/propagation.

R2. Replace A R3 entirely. New local-context word alarm requires original and BOTH immediate anchors to be lowercase lexical source units with EXACT unigram count>legacy threshold (default3). Both actual adjacent original bigrams must be EXACT POSITIVE. The centered original trigram must have EXACT known nonnegative count C, and already-fetched fixed-neighbor alternatives must contain a DISTINCT casefold middle lexical unit with positive count A>=2*max(C,1). Identical/casefold-identical or invalid lexical alternatives never support. CENSORED/UNAVAILABLE originals supply no signal; missing never means zero. No extra query, denominator/probability/entropy, alternative-unigram inference or automatic replacement. Source gaps must contain only ASCII spaces/tabs, no protection, newline/punctuation/removed token or unsafe grapheme boundary. Single context-only word score0.4. Do not send ranked alternatives/evidence to the reviewer.

R3. Replace A R4 entirely. Group maximal source-adjacent runs of actual R2 alarms BEFORE review. One-unit run stays a word; any run over128 original code points is skipped. A2-4-unit run within128 becomes ONE exact original slice including its horizontal whitespace, score0.45. Both anchors are outside the whole span. Over4/over128/ambiguous runs leave ALL their context-only alarms unchanged, never clip a subrun. Invalid/protected/rare/unknown intervening tokens cannot be removed to join alarms. Do not group mere low counts without fixed-anchor contrast. Deduplicate, prefer the complete phrase over overlapping context words, then apply bounded deterministic selection. No reviewer-chosen offsets, extension or second review.

R4. Keep A R5 and all existing strict acceptance/composed/patch, Pandoc/version/startup/mapping and transport boundaries unchanged. One fresh isolated batch, CPU IDs/offsets, no main history/tools/images/recursion. Keep/wider/unknown evidence abstain; optional failure returns only a safely completed original, with actual calls/known-or-unknown usage and owned cleanup. Main failure/hard-limit semantics remain failures.

R5. Replace A R6 fixture premises with SOURCE-SCALE synthetic evidence. Real WORD control: to alpha je, original/anchors unigrams100000, original bigrams/trigram3000, actual distinct fixed-anchor middle alternative6000, supported replacement with positive unigram and consistent contexts>=6000. Real PHRASE control: to alpha beta je, known units100000, original bigrams/centered trigrams3000, BOTH interior units with actual fixed-anchor alternatives6000. A useful proposal changes BOTH words with positive unigrams/internal/both external anchored contexts6000. Populate real middle-table rows, not injected evidence. Assert actual targets assigned before one review, exact whole-span/outer-byte integrity and accepted ordinary evidence route. No fake detect/Candidate/Corpus/protect/accept/compose/apply. Only external reviewer/upstream fixtures may be fake.

R6. Apply A R7/R8 source/limit/budget/actual HTTP proof obligations, using the new signal. New tests cover2x vs below2x, identity alternatives, unknown original context with huge alternatives, safe/no contrast zero calls, legacy modes,3/4-unit groups, over4/128 skip whole run, repetition/caps/determinism and lexical/protected/Unicode/barrier negatives BEFORE targets. Prove real Engine keep/wider/invalid/unsupported proposals and actual query schedule14/3tokens,19/4 including schema versus raw detect, unchanged index/close. Existing early/late budget/usage/recovery positive premises stay meaningful.
Actual ConceptProxy JSON word and genuinely held-main delayed-SSE phrase paths must run through admission/capture/Engine/Pandoc/ROCorpus/new selector/ResponsesReviewer child/parser/accept/compose/render. Only owned main/review loopback0 endpoints are fake. Capture exact review targets, assert one call after main completion, no provisional original leakage, consistent answer copies, same-proxy following safe zero-review response, usage isolation and joined cleanup. This is software proof, not native Qwen or quality evidence. Root's later actual preserved-index producer probe is additional evidence, not a preclaimed PASS.

## Acceptance criteria

A1 Actual default word and genuine phrase production before review, useful strict Engine/HTTP outcomes, source-scale fixed-anchor evidence; no absolute3 cutoff or injected targets.
A2 All lexical/source/protection/uncertainty/whole-run limits and legacy/budget/cleanup controls hold; same SQL, frozen50 other Python/17 old tests, unchanged parser/acceptance.
A3 Focused/new tests, strict3/Ruff3, stable full18 and shared checks pass on actual recorded bytes/revisions; negative controls remain nonvacuous.
A4 Accurate docs/history, same actual PR, exact source/report publication and all4 final-head CI plus independent review before development merge. No functional MVP/native/quality/deployment claim by coding.

## Verification

Qualified Python3.12.15 -B; explicitly installed Pandoc3.7.0.2/SHA02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229. Private TMPDIR/pycache, no bytecode/cacheprovider. A baseline273+117 is old-code evidence, not new producer success; no redundant baseline rerun.
Focused pytest: new test_runtime_detection.py plus test_runtime_acceptance.py, test_composed_validation.py, test_runtime_corpus.py, test_evidence_budget.py, test_review_batch.py, test_analysis_policy.py, test_pandoc_protection.py. Then ONE final stable full concept-verification/tests18 run, actual exit/no edits during run. Strict3: fresh byte-identical flat copies, minimal Python3.12 strict/follow_imports=silent, actual concept+repo imports, fresh cache/noincremental, no Any/ignore/relaxed overrides. Ruff actual3/cwdREPO_ROOT/explicit pyproject/--no-cache. Capture literal tested HEAD+dirty source53 before/after and later committed equivalence separately; preserve interim failures.
Shared accepted-runtime Gov3549, index+HEAD transcript, report-history require-manifest, both whitespace bases2832fa1e51bdf3641aabbd81feab8ddb64a876da/82ea1e6f4173934fa47bb34ee6a6f78338d3603a, research checks and173 valid pins/only4 authorized changes. Designed pre-report84vs83 counter failure stays FAILED until publication. Required final-head checks: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history ALL SUCCESS. No full unchanged local OAP suite. Actual baseline is51Python/17test modules and reviewed-report counter83; expected B53/18/counter84 must be proved, not inferred.

## Local setup and constraints

A's resource/privacy contract remains: only existing foreground codex --yolo --profile early-beta, explicit OAP_ROLE=coding, exact control consumed outside model once; no agents/background codex exec/new panes/provider/profile/home/auth changes or restart except actual death/exact argv. Finite owned test children/loopback0 allowed. Private700/600/umask077, preserve unrelated roots/work/history; no reset/clean/stash/amend/rebase/force/blanket chmod/repository caches. Protect Qwen/GPU/CUDA/services/ports/network/VPN/firewall/gateway/neighbors. No product live calls, customer data, acquisition/deployment/exposure, raw texts/prompts/responses/credentials in operational logs/public reports. Tiny explicit synthetic test literals allowed. Versioned prose uses logical roots.

## Documentation

Five current docs only. A remained PARTIAL, Root caught unusable cutoff before any Python write; B actual new behavior/uncalibrated limits/tests when proved. Preserve historical A report/order. Explain remaining cancellation/audit/native work, quality unmeasured, NO human dataset excluded not deferred. Same173 keys/only4 affected pins, research counter83->84 only, registry42/incidents2 unchanged. No new study or seed rewrite.

## Git and report publication

Same actual PR/branch, forward commits. Commit B non-report work/order/active before actual implementation head. Structured connector or REST exact JSON/readback for locally broken gh pr edit; no false persistence claim. Concise PRIVATE report and normal unpublished preflight; Root exact-byte approval before canonical sole-report SELF/sole implementation parent/push/normal REMOTE/ONE response/quiescence. Actual PR created_at<=actual observed_at<=actual written_at; inconsistent timestamps are diagnosed/waited, never fabricated or exempted by old authority. Pre-push report cannot claim its future publication or CI. Root alone reviews final head/all4CI/deployment effects and expected-head development merge; coding never merges/automerges. Forward rollback preserves history.

## Decision classification

D0 correction of Root's ordinary engineering error, no weaker acceptance/DHA. Strongest objection: stronger fixed-anchor alternatives do not prove the original wrong, and grouping can add inference or reduce useful coverage. Mitigate EXACT same-N/same-anchor evidence, known lexical source gates, finite whole groups/one call, reviewer keep/wider abstention and unchanged independent acceptance/composition. No calibrated correctness/benefit claim. Report real authority conflicts, never silently weaken law.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
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
  "lr": [
    "LR-001",
    "LR-002",
    "LR-003",
    "LR-004",
    "LR-005",
    "LR-006",
    "LR-007",
    "LR-008",
    "LR-009",
    "LR-010",
    "LR-011",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "id": "029-b",
  "title": "Produce source-compatible bounded word and phrase targets",
  "objective": "029",
  "status": "FINAL",
  "phase": "RUNTIME_SOURCE_COMPATIBLE_WORD_PHRASE_SELECTION",
  "base_sha": "915c349939e1f57b759549cfd361113e25f80329",
  "branch": "oap/029-runtime-detection",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 31,
  "dependencies": [
    "028"
  ],
  "local_work": "Currentlocal/remotePR31headabb9bcf289837876f00ee0bee1b8413594383cb2, trackedclean plus preserved .rclone-speed-test/, .research-test-scratch/, corpus/. Aexactorder/report andallhistoricalwork retained; all51Python equalbase915c349939e1f57b759549cfd361113e25f80329, no newmodules. SameforeGround3341327/ownerargv/cwd/home/auth, no newprocess orrestart. Previous41360responseCLOSED0/retired; freshBreader afternormalpublication only.",
  "prior_review": "Observed 2026-11-10T02:14:26.033135+00:00: PR31 OPEN/unmerged, same-repository branch oap/029-runtime-detection, local/remote head abb9bcf289837876f00ee0bee1b8413594383cb2, base/default main915c349939e1f57b759549cfd361113e25f80329. A is PARTIAL and docs-only: exact17439B report SHA b53e0c46accbba982c93ab79b6885663036280f9cc838a5fbd4e7a13fe33a773, sole implementation parentbdbe89d84d36d19e8f175cd05f851b339b55266d/sole reportpath. Actor and Root normalREMOTE verified, actualOK2 received41360/exit0/retired. All four final-A-head CI SUCCESS; actual Application13commands+cleanupPASSED, OAP203tests715.903sOK/alllaterstepsSUCCESS, Research/OAPhistorySUCCESS. Actual tested merge9e5c17646ce8d0ea34f9b91231b253b91f735264 has parentsmain/H and treeequalH. Root verifiedsource51baseequal/no newmodules, all173pins/only4docpins, researchONLY82->83 andpostpublication11testsPASS. Trackedclean plus three preserved untracked roots. Foreground3341327/pane%23 remainsquiescent/exactargv/cwd. Gov3549 unchanged. A semanticcriteria remainunmet because no producer wasimplemented; CIgreen isnotfunctionalacceptance, no merge. CorrectiveB addressesactualsource-incompatiblethreshold, not merelypendingCI.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner requests a functional runnable proxy, mandatory exact-span Pandoc, only the existing foreground coding agent, and NO separate human evaluation dataset."
    },
    {
      "kind": "A",
      "reference": "PLAN7.1-7.2/ARCH6-9: bounded CPU-selected original word/phrase targets, one isolated review, unchanged strict independent acceptance."
    },
    {
      "kind": "E",
      "reference": "029a-root-preserved-index-count-support-diagnostic-20261110.json: actual preserved index unigram minimum272 and n-gram minimum2270; no exact0..3 rows. Root halted A before Python mutation because its absolute context cutoff3 is unreachable on that source."
    },
    {
      "kind": "I",
      "reference": "029a-root-actual-index-fixed-anchor-contrast-20261110.json and 029a-root-actual-index-adjacent-fixed-anchor-alarm-support-20261110.json: actual RuntimeCorpus validates2983 eligible word contexts and231 adjacent alarm pairs from existing evidence. Source reachability only; no new producer/Engine/HTTP/linguistic proof."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

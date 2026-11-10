# Work order 029-a — Produce bounded original-span word and phrase targets in the runnable proxy

Status: FINAL

## Identity

Objective029, first round029-a; CREATE_NEW_PR on oap/029-runtime-detection. Learn the actual PR number only after creation; reuse it after interruption. One coherent selector change, no model/research programme.

## Current verified state

Accepted default/local main is 915c349939e1f57b759549cfd361113e25f80329. PR30 merged2026-11-10T00:40:16Z after all four required final-head checks succeeded and independent expected-head review; normal report/merge verification passed. The accepted tree equals the actual CI checkout. Governance remains3549de2a436f485a693730d0ee7d5f8c00aec0c0. Tracked clean before order publication; retain the three untracked roots and prior feature branches/history. Existing foreground coding PID3341327 is alive/quiescent, exact owner argv/cwd retained. No target029 branch/PR observed. This is a new development objective after accepted028, not a corrective replay or MVP acceptance.

## Provenance

H: owner current scope is functional runnable proxy, exact-original-span mandatory versioned Pandoc and sole existing foreground coding agent. There will be NO separate human evaluation dataset.
A: PLAN7.1-7.2 and ARCH6-9 require CPU-preassigned word/short-phrase spans, conservative uncertainty, barriers and bounded review. LR001-014 remain binding, particularly002-009.
E/I: private NEXT-runtime-producer-existing-evidence-reuse-probe.DRAFT.json and NEXT-root-known-phrase-evidence-and-consumer-20261109.DRAFT.json establish the actual gap: raw detector only produces rare/unknown single tokens; known words100 with weak EXACT contexts1 produce no target. Existing once-per-all-token evidence already supplies necessary facts at the same14SQL/3tokens and19SQL/4tokens including schema. Actual current acceptance supports a preassigned phrase, but that is consumer-only proof.
Remap: replace the unexecuted initial029 lemma-statistics seed with this functional selector objective. Historical seed/draft bytes stay frozen. Lemma calibration, morphology study and follow-on research seeds are not new prerequisites. After this objective: separate bounded cancellation remediation (Root actual client-RST orphan-review probe), fresh isolated architecture-derived readiness audit, then authorized native compatibility. Neither cancellation nor audit is silently claimed complete here.

## Governance

Exact sixteen accepted source/compact identities are in metadata and remain unchanged. PLAN, ARCH, CRITICAL, router/compact laws, prompts, helpers/workflows and historical source seeds are frozen. Empty live CRIT register, no relevant DHA gate, DecisionNONE. This D0 module/heuristic choice does not lower strict acceptance. The one-time028 temporal exception is resolved and does not apply here.

## Goal and dependencies

After accepted028, the runnable proxy must genuinely choose both a known but contextually suspicious WORD and a bounded multiword PHRASE from exact original source before review, then allow only the existing strict evidence/patch path to decide proposals. Preserve useful rare/unknown selection and zero-review unchanged answers without eligible suspicion. This is uncalibrated conservative suspicion, not measured error detection or linguistic correctness.

## Scope

Only three Python paths: NEW concept-verification/runtime_detection.py, NEW concept-verification/tests/test_runtime_detection.py, and IMPORT ROUTING ONLY in concept-verification/proxy.py. Split `from detector import Candidate, detect, tokenize` so Candidate/tokenize remain raw and detect comes from runtime_detection. All other50 existing Python files and all17 existing test modules are byte-frozen against the accepted base; resulting53 Python/18 test modules. In particular raw detector.py, raw repair.py, runtime_acceptance.py, composed_validation.py, Corpus/RuntimeCorpus, Pandoc/mapping/residual/Lua, reviewer/transports/defaults/policies are unchanged.
Other permitted paths: README.md, STATUS.md, concept-verification/README.md, docs/READINESS.md, docs/IMPLEMENTATION-ROADMAP.md (bounded actual029 behavior/status), oap/GENERATED-FILES.json (same173 keys, only corresponding existing4 doc pins), research/RESEARCH-STATE.md (oap_reports_reviewed82->83 only), this exact order/oap/active/eventual sole029-a report. No other mutation. Out-of-scope failure: diagnose earliest boundary, preserve evidence and report before expanding scope; do not silently repair frozen code/tests.

## Non-goals

No parser/AST rendering/fallback changes, acceptance/evidence weakening, budget/default increase, new SQL/connection schedule, transport/cancellation fix, new package/API mode, calibration/rights acquisition/research restart, human dataset, live model calls, GPU/service/network changes, deployment or milestone certification.

## Files and boundaries

Read coding compact set plus relevant SECURITY/TESTING and existing concept local contracts. Inspect actual detector.py, runtime_acceptance.is_lexical_unit, RepairEngine detection/preparation, batch serializer, existing miniature SQLite Engine/HTTP helpers and evidence-budget/analysis/protection tests. Bounded full-source excerpt authorized: ARCH6-9 only. Do not load full strategic law/research histories/old reports into the coding model; helpers validate hashes. Private resource handoff supplies qualified tools, scratch and evidence receipts, never historical-directory discovery.

## Requirements

R1. New runtime detect retains current signature/modes/default arguments and returns existing Candidate objects using exact original code-point slices. Reuse raw Token/Candidate/tokenize/_evidence; call _evidence ONCE per ALL raw tokens in original order, including tokens later ineligible for review, exactly as existing detect. Never call raw detect and then requery. Derive new signals from those already collected dictionaries; one existing RuntimeCorpus, same finite budget, no new queries/connection/write/cache/fallback. RuntimeCorpus errors/control exceptions propagate to the existing engine boundary. Historical raw detector/scientific callers remain byte-frozen.

R2. Preserve original unknown/rare scoring and mode behavior: UNAVAILABLE unigram1.0, known count<=threshold0.5, local-context subtract min(0.35,0.1*number of EXACT adjacent bigram/trigram records), round6, deterministic nonoverlap/source-ordered output, runtime maximum4/hardcap8. unigram-only gains no context-only alarms or phrases. Before assigning ANY target, every unit must satisfy the existing is_lexical_unit and maximal original token/grapheme boundaries; reject partial words adjoining combining marks, format/control characters, digits/underscore or machine fragments. Do not normalize/rebuild original source. Invalid tokens stay in the evidence/token sequence so filtering cannot manufacture adjacency. Define safe zero/negative maximum behavior without increasing runtime caps.

R3. Add the following explicit local-context-only known-word heuristic. Original and BOTH immediate external anchors must have EXACT unigram count>threshold and lower-case lexical source units for the new context-only route; both original adjacent bigrams AND centered trigram must be EXACT counts in [0,threshold]. Each source adjacency must be proven: only horizontal ASCII space/tab gap, no newline/punctuation/removed token/protected interval or unsafe grapheme boundary. With default threshold3, this selects the qualified known-word100/context1 control while an otherwise known word with censored/unavailable/strong context supplies no new alarm. Score0.4. These raw-count bounds are initial suspicion policy only: no probability/complete denominator, error verdict, normative suitability or automatic replacement inference. Do not use missing as zero, alternatives popularity or a hardcoded correction dictionary.

R4. Produce actual2-4-unit PHRASES before review. All units and both immediate external anchors satisfy R3 known-positive/lowercase/lexical/source-boundary constraints. A maximal consecutive weak internal chain has every internal adjacent bigram EXACT count in [0,threshold], while BOTH external boundary bigrams are EXACT count>threshold. Group that chain only if2-4 units and <=128 original code points; longer/ambiguous chains are left unchanged rather than clipped. Entire target is the exact original slice including its original horizontal whitespace. Both anchors remain external. No gap crosses protection, punctuation, newlines/paragraphs, malformed markup, numeric/invalid intervening units or unsafe graphemes. Score0.45. Deduplicate candidates, prefer the complete proved phrase over overlapping context-only word alarms, then apply unchanged bounded deterministic selection. No extension after reviewer response and no wholesale sentence targets. Legacy rare/unknown candidates remain eligible; phrase route never merges them into known-positive chains.

R5. Existing acceptance R4/R5, whole-span neighbor preparation, composed revalidation and exact apply_edits remain unchanged. One fresh bounded batch, CPU IDs/offsets assigned before it, no ranked replacements/evidence leaked into reviewer prompt, no main history/tools/images/recursion. Keep/uncertainty/wider edit/unknown-only evidence abstain through existing path. Unsupported proposal does not become approved because the detector found a suspicion. Parse/mapping/budget failure returns only safely completed original with actual calls/usage/cleanup intact.

R6. New tests prove actual producer first, not injected spans. Use owned synthetic read-only SQLite and qualified real Pandoc. Known WORD control: to alpha je, all unigrams100, both original bigrams and trigram1; replacement omega1000 with actual stronger anchored40 contexts and consistent internal facts. Assert actual selector target alpha and actual RepairEngine useful ordinary-route patch, one review, exact coordinates and unchanged outer bytes. PHRASE control: to alpha beta je, original units/anchors100, external boundary bigrams20, internal alpha-beta1 and original boundary trigrams1; use a useful two-word proposal changing BOTH original words with explicit positive unigrams/internal/both external contexts and >=2 matching original-context comparisons. Assert the2-unit target was assigned before reviewer and exact whole-span replacement. A preassigned Candidate or patched detect/accept/protect/corpus/compose/apply cannot establish these positive proofs. Test finite3/4-unit selection, over4/over128 abstention, repetition by exact occurrence, cap/nonoverlap/deterministic ordering and unigram-only/legacy rare/unknown behavior.

R7. Real Engine negatives: all-known strong/no context => zero calls/exact original; CENSORED/UNAVAILABLE context never low; known weaker/equal/unknown proposal evidence rejects; reviewer keep/wider/invalid response unchanged. Table-driven source negatives cover code/math/HTML/link/config/quoted/protected structures, paragraph/line/punctuation barriers, Unicode/NFD/emoji/CRLF/repetition, No/Nl/numeric/symbol/identifier/combining/format splits; ensure no illegal targets before review, not just later acceptance rejection. Use existing original tests unchanged. Prove actual query schedule against raw detect on owned fixtures (14 for3tokens/19 for4 including schema where unprotected), index bytes unchanged and exact owned close. Retain meaningful existing early-budget zero-review and late-accept-then-abort/all-final-false/actual-known-or-unknown-usage/recovery controls; never increase defaults to make tests pass.

R8. New actual HTTP round trips: actual ConceptProxy admission/forward/capture/RepairEngine/Pandoc/RuntimeCorpus/new selector/ResponsesReviewer child/strict parser/acceptance/composition/rendering. Only owned main/review endpoints on loopback port0 may be fake; tiny synthetic text and dummy key only. At least JSON known-word useful patch and delayed complete-main SSE genuine phrase patch, with exact target captured from the outbound review, at mostone actual review AFTER main completion, no provisional original leakage, all supported output copies consistent. Include same-proxy subsequent known-safe zero-review exact-original control and usage/isolation/cleanup. Held main must genuinely block review until complete; no injected engine result or target. This is software integration, never native Qwen/linguistic proof.

## Acceptance criteria

A1 Actual default runtime produces useful original word AND genuine2-unit phrase before review; unchanged strict policy accepts supported proposals end-to-end. No fake candidate injection for producer proofs.
A2 Conservative lexical/source/uncertainty gates, finite2-4/128/cap bounds, legacy modes, exact source/outer slices and negative/no-call/decline paths tested; same query schedule/budget/index lifecycle, all50 other Python and all17 old tests unchanged.
A3 New focused tests, actual broader18 modules, strict3/Ruff3 and shared checks pass on stable recorded candidate bytes. Original controls retain their actual positive premises, not vacuous abstention. Any failure stays truthfully classified and scoped.
A4 Concise accurate docs, exact order/active, same173manifest/4pins/counteronly, one actual new PR, truthful approved private report then normal sole-report SELF/REMOTE/ONE response. All four final-head CI and independent review precede development merge. No functional MVP/linguistic/native/deployment acceptance in this coding report.

## Verification

Qualified Python3.12.15 -B, explicitly installed Pandoc3.7.0.2 SHA02a59bd935b02364e6dee67093874532c096adcb60374a53a0f3ba5310ab1229. Use PYTHONDONTWRITEBYTECODE=1, private TMPDIR/pycache, pytest -p no:cacheprovider.
Focused: new test_runtime_detection.py plus existing test_runtime_acceptance.py, test_composed_validation.py, test_runtime_corpus.py, test_evidence_budget.py, test_review_batch.py, test_analysis_policy.py, test_pandoc_protection.py (confirm actual test filenames). Then ONE final stable `pytest -p no:cacheprovider -q concept-verification/tests` (all18), no edits during run, capture actual command exit without tail/pipeline masking.
Strict3: fresh byte-identical flat shadow of the three scoped paths, minimal python3.12/strict/follow_imports=silent configuration, actual concept AND repo import searchpaths, fresh cache/noincremental, no Any/ignore/overrides weakening. Ruff: ACTUAL three paths, cwdREPO_ROOT, explicit root pyproject.toml, --no-cache. No global config/import surgery. Record literal tested HEAD + dirty hashes, all53 before/after, later committed equivalence separately; preserve failed/interim epochs.
Shared: accepted-runtime governance3549; transcript index+HEAD; report history require-manifest; both accepted whitespace bases2832fa1e51bdf3641aabbd81feab8ddb64a876da and82ea1e6f4173934fa47bb34ee6a6f78338d3603a; research checks and all173manifest identities with only4approved doc pins. The designed pre-report83vs82 history-count failure stays FAILED until actual final publication clears it. No full local unchanged OAP suite required. Final-head required checks: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history, all SUCCESS; pending/missing/skipped/cancelled is not success. CI remains actual broad baseline including package/import checks, but no new packaging work is ordered.

## Local setup and constraints

Only existing owner foreground codex --yolo --profile early-beta in current coding pane, explicit OAP_ROLE=coding for helpers; dispatcher consumes exact control once outside model. No subagents/backgroundAI/codex exec/new pane/alternate provider/profile/home/auth/restart; actual process death alone allows exact recorded relaunch. Ordinary finite pytest/test children permitted. Use owned700scratch/600files/umask077; no in-repo caches, blanket chmod, reset/clean/stash/amend/rebase/force/history deletion. Preserve three untracked roots, accepted/preserved branches, archive/index/resources/drafts/histories. Do not mutate Qwen weights/quantization/vLLM/CUDA/GPU/services/occupiedports/network/VPN/firewall/gateway/neighbors. No model calls/customer data/acquisition/deployment/exposure. No text/prompts/replacements/raw responses/credentials in operational logs/public reports; owned tiny synthetic test fixtures may contain their explicit test literals. Versioned prose uses logical roots only.

## Documentation

Update only five current docs for actual029 behavior/uncalibrated thresholds/limits/tests and remaining cancellation/audit/native work; preserve historical028 narrative and reports as historical, avoid claiming PR30 still currently open. No separate human evaluation dataset is excluded, not deferred. Quality remains unmeasured. Re-pin only corresponding4 existing generated-doc entries with unchanged173 keys. research counter82->83 only, registry42/incidents2 unchanged; no study/registry entry. Do not rewrite seed029 or PLAN/ARCH.

## Git and report publication

Create new branch from exact accepted main; publish scoped non-report work/order/active and one actual PR before report. Reuse after interruption; no duplicate. `gh pr edit` is known locally broken by classic-Projects GraphQL: use structured connector where available or bounded REST gh api PATCH with exact JSON file/readback, not a false persistence claim or CLI reinstall. Keep metadata concise: actual selector behavior, limitations and observed tests.
Prepare a concise PRIVATE report at actual implementation head and run normal unpublished preflight. Synchronize with Root for exact-byte review/approval BEFORE canonical report copy/SELF/push/response; private review is not a new human gate. Report literal implementation SHA, actual command states/tested epochs/limits, publication_commit SELF/publication_verified false and actual chronological PR observation, not future CI/push. After exact approval, canonical sole029-a report commit with sole implementation parent; forward push; independently normal REMOTE verify exact head/parent/path/bytes; ONE responseOK then quiesce. Root owns semantic final-head review/CI/expected-head development merge. Coding never merges/enables auto-merge. Forward rollback preserves all OAP/history.

## Decision classification

D0 bounded runtime-only selector using existing data/query budget and strict downstream authority. Strongest objection: rare contexts are not proof of a wrong expression and these count thresholds may have low coverage or produce extra review. Mitigate with exact-only bounded two-sided known context, conservative source/case gates, <=4 targets/one call, keep/wider abstention and unchanged independent acceptance/composed checks. Document uncalibrated limitations; no precision/benefit claim. A real conflicting architecture/safety issue is reported with evidence, never solved by weakening law or self-authoring DHA.

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
  "id": "029-a",
  "title": "Produce bounded original-span word and phrase targets in the runnable proxy",
  "objective": "029",
  "status": "FINAL",
  "phase": "RUNTIME_CPU_WORD_PHRASE_SELECTION",
  "base_sha": "915c349939e1f57b759549cfd361113e25f80329",
  "branch": "oap/029-runtime-detection",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "028"
  ],
  "local_work": "Local main equals accepted remote main915c349; tracked clean before publication. Preserve .rclone-speed-test/, .research-test-scratch/, corpus/ and all histories/resources. New objective, no existing target branch or PR.",
  "prior_review": "PR30 merged normally at2026-11-10T00:40:16Z into915c349 after independent review and all four final-head CI SUCCESS. Merge tree equals actual CI checkout and reviewed report head. Normal B REMOTE and merge verification passed. All51 source identities match tested B candidate. No governance revision, MVP or deployment acceptance.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner directs functional runnable proxy, exact-original-span mandatory pinned Pandoc, sole existing foreground coding agent, no separate human evaluation dataset; continue authorized development."
    },
    {
      "kind": "A",
      "reference": "PLAN7.1-7.2, ARCH6-9/LR002-004: bounded CPU-selected original word/short-phrase targets before one isolated review; preserve source/protected boundaries and uncertainty."
    },
    {
      "kind": "E",
      "reference": "NEXT-runtime-producer-existing-evidence-reuse-probe.DRAFT.json: actual detector selects zero known-word100 with EXACT contexts1; existing all-token evidence exposes them at same14SQL for3tokens."
    },
    {
      "kind": "I",
      "reference": "NEXT-root-known-phrase-evidence-and-consumer-20261109.DRAFT.json: actual known alpha/beta selector0, all-token evidence19SQL; actual strict phrase consumer accepts preassigned alpha beta->omega beta with exact anchored evidence. Consumer proof only, no producer/Engine/HTTP claim."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

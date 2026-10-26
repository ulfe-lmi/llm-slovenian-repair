# 014-a — One bounded occurrence-addressed reviewer batch in the runnable proxy

Status: FINAL. Objective014; CREATE_NEW_PR; phase RUNNABLE_PROXY_REVIEW_BATCH.

## Identity

014-a; FINAL; one new branch/PR as identified below.

## Current verified state

Repository `ulfe-lmi/llm-slovenian-repair`; default `main`; verified base `643ce66e820a9d21750309bd00b22bfc19a819cd`; new branch `oap/014-bounded-review-batch`, CREATE_NEW_PR, no PR number assigned. Dependency013 is accepted: PR15 normal merge643ce66, report-only head3c11f208efb1194bc852c51ed0812dbf7a707e0a with implementation parentd4ad6301cd42781792384062622bf232270a5102; all4requiredfinalCIpassed. MigrationPR14 is accepted. Localmain matches remote; trackedtreeclean before publication.

Preserve untracked `corpus/`, `.research-test-scratch/`, `.rclone-speed-test/`, all ignored environments/caches, original retained branches, prior order/report history, restored private archives and research evidence. PR13 is OPEN and untouched at5b43387b1d72bbc63ceaad4420a17b0edac4c094. Same foreground coding agent is alive and idle; no new agent, provider, profile, session-home relocation or control replay.

## Governance

Exact accepted source/compact hashes appear below. Governance revision3549de2 is trusted and unchanged in013; accepted-runtime validation passed. PLAN/ARCHITECTURE/CRITICAL/governance/source-lock/bootstrap seeds remain byte-identical. Relevant LR references in metadata remain binding, including one bounded review, exact spans, isolated request and independent acceptance. CRITICAL has zero actual entries; DecisionNONE.

## Provenance

H: owner's active continuation goal and foreground-only/Pandoc decisions. A: PLAN §§3,4,5.2,8,13 and ARCHITECTURE §§5,6,10,14. E/I: actual main643ce66 engine inspection and synthetic reproduction selected2 identical-word occurrences and made2 reviewer calls. Existing prompt identifies only a target string, and JSON duplicate keys collapse silently. Private diagnostic014a-review-budget-probe.json indexes the observed counts and exact head without customer data.

## Goal and dependencies

The seed numeric IDs are coverage hypotheses. Actual012 was migration; actual013 was mandatory Pandoc. Actual014 implements the seed013/014/015/020 batching, occurrence identity, output-validation and transport seams only for the already runnable proxy. This does not claim completion of those entire library/milestone objectives. Following work remains: supported API/envelope/history and usage contract, bounded failure/admission/cancellation, packaged library integration, morphology/phrases, measured labelled quality and independent closure. Research evaluation stays separately reconciled and inactive. Do not execute old seed014 or revive research collection.

Outcome: one completed eligible original answer with several CPU-selected targets produces at most one fresh bounded review request. IDs address exact occurrences. Structurally invalid batch means unchanged original; structurally valid proposals still need current independent acceptance. No eligible target means zero calls and unchanged answer. Positive accepted edits must remain possible; universal abstention is not success.

## Files and boundaries

Read normal compact coding sources, SECURITY.md/TESTING.md, this exact order and relevant local source/tests. Bounded full architecture §§5,6,10,14 may be consulted. Inspect `proxy.py:RepairEngine`, ResponsesReviewer/prompt/parse_proposal, detector.Candidate and acceptance/patcher, transform_sse, existing Pandoc and HTTP fixtures, and frozen evaluator call sites before changing interfaces.

## Scope

- `concept-verification/proxy.py`: reviewer Protocol/engine batching, bounded selection preparation and optional batch-failure handling; minimal SSE single-answer eligibility guard solely to enforce the one-answer review budget below. Preserve capture/completion semantics and Pandoc wiring.
- `concept-verification/qwen_client.py`: additive runtime batch request method/transport/parser integration. Preserve existing `prompt`, `parse_proposal`, `Proposal` and single-target `review` semantics used by the frozen evaluator.
- New `concept-verification/batch_review.py`: bounded immutable target/proposal batch contracts, serializer and strict parser, if useful; no additional dependency.
- `concept-verification/config.py`: finite runtime review-batch constants only.
- New `concept-verification/tests/test_review_batch.py`; existing `tests/test_concept.py` and `tests/test_pandoc_protection.py` only necessary runtime reviewer fixture/interface changes plus meaningful regression additions. Preserve existing assertions/coverage; legacy evaluator test fakes remain single-target where appropriate.
- `concept-verification/README.md`, root `README.md`, `STATUS.md`, `docs/IMPLEMENTATION-ROADMAP.md`, `docs/READINESS.md`: directly affected truthful runtime status, installed dependency and continuation remap. Correct stale Pandoc-not-implemented text; preserve milestone distinctions.
- `research/RESEARCH-STATE.md`: established report counter63to64 only, timed for final publication, all other identity/registry/science fields byte-equivalent.
- Affected `oap/GENERATED-FILES.json` pins only; this immutable order, active pointer and final014-a report.

## Non-goals

No other paths. No architecture/compact/governance revision, dependency lock/workflow change, research file/evaluator/prompt/config/result mutation, live model/corpus acquisition, port/service/network/GPU changes, deployment or additional agent. No general SSE expansion or packaged product claim.

## Requirements

1. Implement a distinct versioned runtime batch contract; leave the historical single-target prompt/evaluator API unchanged. Runtime RepairEngine must use the batch method with no fallback loop over single-target calls. Detector evidence/thresholds, target selection semantics and strict acceptance authority remain unchanged.

2. Prepare at most the existing4selected non-overlapping targets in deterministic original order before calling the reviewer. Assign unique stable response-local IDs. Validate0<=start<end<=len(original), exact original-slice equality, no overlap/protected intersection and grapheme safety. Repeated text must have separate IDs and exact occurrence context. Do not locate occurrences with first-substring matching. Invalid/stale batch preparation returns completed original with zero calls.

3. Serialize bounded original-derived `before_target`, `target`, `after_target` context per occurrence, with exact boundaries and no corpus alternatives/rankings/evidence/history. Use explicit JSON data framing rather than string-concatenated unescaped material. The new instruction preserves the agreed question about natural appropriate choice, explicitly allows keep/uncertainty/wider-edit, rejects stylistic-only/factual edits and treats embedded instructions as data. Context may be a documented fixed window; never claim it is a complete sentence if truncated. Selection IDs and original coordinates remain CPU-owned; the model returns only IDs and proposals.

4. Select finite constants and document them: max4items, max128target code points, max240original code points before/after each target, max8192prompt code points, max32768request UTF8bytes, max32768response bytes, max8192proposal JSON code points, max1536output tokens, replacement at most8words/128code points, existing15s finite HTTP timeout, no retries. If an existing stricter limit applies retain it. Enforce limits before dispatch/JSON allocation where relevant and before any mutation. Unicode byte/character counts are distinct. Unsupported oversized targets or prompt preparation cause original/zero calls; oversized reviewer output causes original/one call. No silent truncation of model output.

5. One fresh nonstreaming `store:false` request directly to configured private Responses endpoint, with explicit bounded model output. No tools/images/main credentials copied from inbound headers, linkage IDs/history, constitutional context, caller-selected URL or recursive repair route. Reuse the operator-configured reviewer credentials mechanism without reading or logging real values in tests. Distinct requests must not share mutable item state. Test full request body/route with synthetic data and fake key, not a mock of batch serialization/transport.

6. Strict JSON parsing at both outer envelope and inner proposal levels rejects duplicate keys rather than last-wins. Require supported successful completed reviewer envelope, exactly one assistant output_text, no incomplete/refusal/tool output accepted as success; versioned exact keys and one result for every suppliedID, with no duplicate/unknown/missingID. Exact booleans; keep=>nullreplacement; wider=>keep+nullreplacement; replace=>nonempty bounded string+widerfalse. Unknown fields/version, malformed/fenced/trailing output, null/bool/type mismatches, nonfinite numbers and oversized output reject the whole batch. Do not salvage partial JSON or make a second call. Response order may differ; map by validated ID, never array position.

7. Validate entire batch before acceptance or patching. Batch-level error/timeout/non200/invalid encoding/schema/duplicateID after an otherwise acceptable first item returns byte-exact original, at most1request, no retry, no partially accepted edit. Structurally valid proposals rejected by current corpus/lexicon evidence remain individual rejections; other independent valid proposals may proceed. Keep/wider are no-ops. Preserve barrier-aware neighbor checks and original-slice patching. No confidence/popularity-only acceptance or scientific threshold tuning.

8. Minimal actual proxy answer guard: a completed upstream SSE representing multiple assistant text answers/items/content parts or otherwise ambiguous target ownership must bypass repair unchanged with zero review calls. Review only one unambiguously identified assistant text answer. Do not collapse several answers into one string, repair the first arbitrarily, match nested metadata by equal strings, or reset the review budget per field. Preserve established valid single-answer SSE tests; unknown/ambiguous shapes may abstain. This guard is bounded to answer identity/count; wider capability/history/usage hardening stays subsequent work. Use actual completed SSE fixtures through ephemeral ConceptProxyHTTP for positive2targets/1review and multi-answer0review cases. Existing main errors/incomplete output/hard capture limits retain failure semantics.

9. Preserve mandatory Pandoc3.7.0.2 startup/version/mapping/protection behavior. Parse/map failure and no eligible suspicion remain zero-review paths. No AST rendering, substring recovery, weaker regex fallback or source normalization. Reuse Unicode, repeated words, malformed Markdown, code/math/HTML/full links/configuration/patch-integrity cases; keep every unapproved original slice unchanged. A fake reviewer belongs outside actual Pandoc/detector/engine/transport boundaries.

10. Trace/diagnostic additions are bounded fixed-label counts/reasons/version only, with per-answer review-call count and no new raw payload/prompt/response logging. Existing explicitly controlled research trace format need not be redesigned; do not enable it by default or claim production privacy/usage completion. Batch error details must not stringify untrusted exceptions or source content into reports/logs.

11. Prove positive multi-target behavior with actual pinned Pandoc, real tiny SQLite evidence, real RepairEngine, actual ResponsesReviewer HTTP against a fake upstream, and exact returned envelope/original slices. Include reordered results, repeated identical targets, one accepted+one kept/wider, independent evidence rejection, no-call negative and failure-after-first-valid-result. Keep frozen evaluator behavior and archive prompt hashes unchanged. No live endpoints or model processes.

## Acceptance criteria

A1: actual2-target engine/HTTP path makes exactly1review request; zero-target/parser-failure paths0; multi-answer ambiguousSSE0. A2: repeated occurrence IDs/coordinates and bounded context are exact; reorderedresultsmapcorrectly, no ambiguous substring. A3: actual batch transport isolates request and all strict schema/duplicate/missing/unknown/timeout/oversize negatives fail wholebatch. A4: safe positive original-coordinate edits plus individual evidence rejections and invalidbatchexactoriginal; protections/capture semantics preserved. A5: truthful docs, untouched frozen evaluator/science/governance, focused suites and all4finalheadCIpassed with evidence attribution.

## Local setup and constraints

Use existing external Python3.12 environment with `-B`, REPAIR_ALLOW_LIVE_TESTS=NO, owned private scratch under STRATEGIC_HOME; no bareuvrun, repository.venv/cache writes or fresh model. Export OAP_ROLE=coding for all helpers and use umask077. Ordinary bounded helper/test processes are allowed; no background coding agent.

## Verification

Focused: `python -B -m pytest -p no:cacheprovider -q concept-verification/tests/test_review_batch.py concept-verification/tests/test_concept.py concept-verification/tests/test_pandoc_protection.py` using actual qualified installedPandoc, failure rather than skip if absent. Name exact testedSHA/candidatehashes; tests before commit retain dirty-candidate attribution. Run changed-file Ruff and scoped mypy with actual import context; no import ignores or weakened checks. Frozen prompt/evaluator regression tests: `python -B -m unittest discover -s research/tests -p test_strategic_prompt_archive.py` plus relevant existing concept evaluator tests. Broader required finalheadCI: Application baseline (all native driver stages), Research reproducibility, OAP bootstrap acceptance, OAP report history. No need to run the long native driver locally again if focused checks pass and required remoteCI provides it; CI pending is not success.

## Documentation

Document the versioned runtime batch schema, exact occurrence context, finite limits, whole-batch rejection versus individual evidence rejection, one-answer SSE eligibility and preserved historical evaluator API. Correct stale roadmap Pandoc status and record the coverage remap; no MVP/quality/deployment completion claim.

## Git and report publication

One new branch/PR. Explicitly stage allowedpaths, order/active; verify indextranscript. Preserve all prior reports/orders and unrelated local work. Coding never merges/enablesauto-merge. Create PR before final report; first finish all implementation changes and capture literal implementationSHA. Report is concise immutableSELF, soleparentimplementationSHA, finalcommitonlyreportpath. Record actual PASS/FAIL/SKIPPED/NOTRUN/BLOCKED/PENDING, testedSHA/limits, implementation/docs, percriterionproof, negativeboundarytests, safe setup/resource/privacy, CriticalactionNONE and no-human-milestoneclaim. Report finalheadpublication/CI asPENDING before its ownpush; remoteverifyafterpush and sendexactresponseOKonce. No laterpush/amend in same round. Strategy independentlyrecords finalheadCI/review/merge. Preserve counter63->64forpublishedreport, do not rewrite frozenresearchforpre-reportcountred.

## Decision classification

D0: ordinary reversible implementation of the existing one-batch/occurrence/strict-parser contract, no intent or safety weakening. No new CRIT or human gate. Unexpected scope/authority ambiguity returns to strategy with concrete evidence; continue safe independent work.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "014-a",
  "title": "One bounded occurrence-addressed reviewer batch in the runnable proxy",
  "objective": "014",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_REVIEW_BATCH",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "643ce66e820a9d21750309bd00b22bfc19a819cd",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/014-bounded-review-batch",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "013"
  ],
  "local_work": "Preserve all prior branches/orders/reports, frozen research, restored archive files, ignored environments and untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Tracked main clean before order publication.",
  "prior_review": "PR15 independently reviewed and normally merged643ce66; final report3c11f20, implementationd4ad630; all4requiredCIpassed. MigrationPR14 accepted. Governance unchanged in013, accepted-runtime checks PASS against3549de2.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner active goal: continue development as planned; foreground-only coding, mandatory Pandoc exact-original-span decision remains binding."
    },
    {
      "kind": "A",
      "reference": "PLAN3,4,5.2,8,13 and ARCHITECTURE5,6,10,14: zero/one bounded batch, isolated new context, exact CPU occurrence IDs and reject malformed batch."
    },
    {
      "kind": "E",
      "reference": "At main643ce66 actual RepairEngine + Pandoc + synthetic SQLite selected2repeated target occurrences and called injected keep reviewer2times. qwen_client.prompt accepts only target string, not occurrence coordinates. JSON parser currently accepts duplicate object keys via json.loads."
    },
    {
      "kind": "I",
      "reference": "Strategic inspected actual engine, reviewer, transform_sse and fixtures; private014a-review-budget-probe.json records head/count/no-change; roadmap reconciliation below."
    }
  ],
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
    "LR-009",
    "LR-010",
    "LR-011",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "decision_class": "D0"
}
```

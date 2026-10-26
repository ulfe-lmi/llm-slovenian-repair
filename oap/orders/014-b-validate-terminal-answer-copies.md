# 014-b — Validate every terminal answer copy before bounded review

Status: FINAL. Objective014, corrective roundb; AMEND_EXISTING_PR #16.

## Identity

Continue only branch `oap/014-bounded-review-batch` and PR16 https://github.com/ulfe-lmi/llm-slovenian-repair/pull/16. No new objective/branch/PR; same foreground agent.

## Current verified state

Repository `ulfe-lmi/llm-slovenian-repair`, default `main` at643ce66e820a9d21750309bd00b22bfc19a819cd. Existing PR16 OPEN/MERGEABLE, exact head/base for this correction6c4bf45060300932f721b31ea51a6da3d82c2984; sole implementationparentb5298e720e88c5b78bfc75af61ddebffcb7a8a9c. Report014-a remotelyverified, immutable, report-only path. All4requiredCI SUCCESS; independent exactheadfocused172PASS+5subtests. Semantic review FAILED on the concrete cases below, so no merge. Agent3341327/pane23 remains alive and idle after one exact responseOK; that reader is completed/closed. Do not replay014-a. This new corrective round gets its own externally consumed control and response wait.

Preserve all014-a/013/012 commits, priorreports/orders, restored archives/private inputs, ignored environments/caches and untracked `corpus/`, `.research-test-scratch/`, `.rclone-speed-test/`. PR13 stays OPEN/untouched at5b43387b1d72bbc63ceaad4420a17b0edac4c094.

## Governance

Trusted accepted governance3549de2a436f485a693730d0ee7d5f8c00aec0c0, source/compact identitiesbelow. No governance/source/PLAN/ARCHITECTURE/CRITICAL/bootstrap changes. CRITICAL haszeroactualentries. LR-001..014 remainbinding, particularly LR-006/007/010/011/013/014. Normal compactreadset plus SECURITY/TESTING and exactorder; bounded ARCHITECTURE §§6,12,13 may be consulted.

## Provenance

H: owner's continuing development goal and foreground-only/Pandoc decisions. A: exact014-a requirements7,8,9,11 and architectural ownership/patch/delivery invariants. E/I: final independent review at exact6c4bf45 reproduces3cases in private014a-final-terminal-integrity-probes.json; existing172greenfocusedtests and4greenCI do not cover those cases. Renderloops currently replace all output_text parts in a matching-ID terminalitem without proving cardinality/role/text agreement before repair.

## Goal and dependencies

Finish objective014's existing one-answer ownership contract. Establish the whole supported answer and all of its terminal representations before calling repair, and mutate only exact validated copies of that one answer. Preserve useful positive batching and all014-a protections. Dependency013 accepted;014-a publicationverified but objective014 not yet accepted for merge. No new milestone gate or product objective.

## Scope

- `concept-verification/proxy.py`: only transform_sse ownership preflight, bounded local helper/data structures if useful, and rendering of validated terminal paths. Preserve callable signature, maincapture behavior, mandatoryPandoc and batch/acceptance semantics.
- `concept-verification/tests/test_review_batch.py`, `tests/test_concept.py`, `tests/test_pandoc_protection.py`: focused terminalcopy ownership/consistency regressions and only necessary valid-fixture updates; retain every existing assertion/coverage.
- `concept-verification/README.md`, `STATUS.md`: directly affected ownership/fallback behavior and accurate corrective evidence; root `README.md` only if its current affected statement needs correction.
- `research/RESEARCH-STATE.md`: counter64to65 only for finalreport; no other science/identity/registry edits.
- Affected `oap/GENERATED-FILES.json` pins; thisorder, activepointer and final014-b report.

## Non-goals

No reviewerprompt/schema/transport/timeout change; no detector/acceptance/morphology/data/research/evaluation changes. No generalSSE capability expansion, gateway/API redesign, policy weakening, dependency/workflow change, live calls, model/GPU/service/port/network/credential change, deployment or agent spawn. Do not solve contradictory replicas by silently editing a subset, inventing IDs or disabling all repair.

## Files and boundaries

Inspect final014-a transform_sse and its explicit renderer, `_event`/capture semantics, existing terminalcopy tests/fullHTTP CompositionChainTests, original014-a report and thisexactorder. Review metadata-only failure receipt if helpful; no need to read private raw research text. Fakes belong outside actual transform/engine/ResponsesReviewer/Pandoc/SQLite boundaries.

## Requirements

1. Reproduce these exact6c4bf45 failure cases before the fix and preserve the observation: final completed response has one assistant message idm with one output_text T; streamdelta idm matches it, but (a) output_item.done itemidm contains two output_text parts T and differentT; (b) content_part.done itemidm/index0/0 contains differentT; (c) content_part.done output_text T has missing/null/nonstringitem_id. Currentbehaviorcallsrepair1andchangesbody. Requiredbehavior is raworiginalSSE byteidentical,0repair/reviewer calls. Add mismatched terminalrole/status/identity/index and conflicting done.text cases as the same ownership/consistency family.

2. Before calling repair, validate every answer-bearing terminal representation against the one final assistant answer. A content_part.done output_text must identify the same exact typed nonemptyitem_id and final output/content positions, contain exact originalanswertext, and have the expected partkind. A message-typed output_item.done must identify that same exact typedmessage.id, roleassistant, consistent completedstatus whenpresent, the expected content cardinality/kinds and one exact original output_text slice at the proved position. Refuse contradictory/extra answer parts, malformed/missingrequiredownership and any differentanswerID. Do not coerce IDs or use value-based recovery. Initial added events may be empty placeholders: validate their ownership and protect their content; do not confuse them with terminalcopies. Preserve recognized noneditable reasoning/nonanswer bookkeeping.

3. A supported final answer, its delta/done stream and every terminal copy must agree on ownership and original text before any reviewer side effect. Any copy that cannot be proved consistent makes the entire SSE ineligible: return raworiginal/zero calls, never keep one edited representation beside an incompatible original copy. Existing malformedJSON/mainerror/incomplete/hardcapture-limit semantics remain unchanged; do not broaden fallback around maincapture or hide main errors.

4. Collect bounded explicit references/paths to validated editable text fields during preflight and use only those when rendering. Do not iterate over all output_text nodes of a matching-ID object after repair, recurse into metadata, match substrings/identicalvalues, infer positions, repair several answers, or mutate unrelated protectedfields. One supported answer makes at most the existing single batched review request; no-copy/no-edit and optional-batch-failure paths preserve rawSSE bytes. Exact original-span/Pandoc/patching guarantees remain intact.

5. Prove a useful canonical positive through actual ephemeral ConceptProxyHTTP -> realRepairEngine/Pandoc/tinySQLite -> actualResponsesReviewer -> fake reviewerHTTP: at least2targets, one request, consistent replacement text in output_text.done/content_part.done/output_item.done/response.completed, unchanged unrelated metadata including a same-text output_text-shaped echo and untouched non-answer bookkeeping. Reordered batchresults stillmapbyID. The callback/directtransform layer additionally proves exact path ownership and0calls on contradictory copies. A valid canonical stream may contain protected reasoning plus the finalmessage at nonzerooutput_index; do not make the implementation pass by rejecting ordinary valid supported positives.

6. Exercise the new contradictory-copy negatives through that same actualHTTP chain, asserting status/unchangedrawbody and0reviewrequests, not a mock of the transformer. Include two-parts-terminal-item, conflictingterminaltext, absent/null/nonstring IDs, wrongrole/status, otherID, and wrongownershipindex. Add no-edit/invalidbatch raw-byte preservation with canonicalcopies. Existing172focusedtests remain meaningful and pass. No assertion weakening, threshold change or replacing a boundary with a fake to claim integration success.

7. Correct forward the evidence interpretation: immutable014-aA4 established nominalcopies only; it did not prove contradictory/unowned copies are rejected. State these findings and the corrected exactproof in014-b report and directly affected docs. Do not rewrite014-a report/order, fabricate human acceptance or claim currentlive compatibility/linguistic/MVP/deployment proof. No new CRIT debt for an ordinary bug.

## Acceptance criteria

A1: all newly named negativecopies bypass rawunchanged0repaircalls/0reviewHTTPrequests before any side effect. A2: canonical positive actualfullHTTPchain retains2target/1batchusefulrepairs, consistent knownterminalcopies, protectedsame-textmetadata/reasoning and exactunapprovedslices. A3: finalrenderer touches only prevalidated paths; no IDcoercion/value-basedmatching or unsupportedcopyrepair. A4: existingcapture/Pandoc/batch/evidencebehavior and allfocusedtests preservecoverage. A5: accurate corrective docs/report, unchangedoldhistory/science/governance, exactreportparent/path and all4required finalheadCIgreen.

## Verification

Use externalPython3.12 with-B and actual qualified installedPandoc3.7.0.2. Focused `python -B -m pytest -p no:cacheprovider -q concept-verification/tests/test_review_batch.py concept-verification/tests/test_concept.py concept-verification/tests/test_pandoc_protection.py`; missingbinaryfailsratherthanskips. Retain pre-fix failures with exacttestedSHA; after-fixcandidatecheckskeepdirtycandidateattribution/sourcehashes, not retrospectivecommitclaims. Namedfrozen regression `python -B -m unittest discover -s research/tests -p test_strategic_prompt_archive.py`. ChangedPython Ruff/scopedmypy with actualrepoimportcontext; no importignores or weakenedchecks. All4required remote finalheadchecks: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history. Longnativebaseline mayruninCI; no need duplicate localdriver iffocusedchecks pass. Pending is not success.

## Local setup and constraints

Only existingforegroundpane23/ownerlaunched3341327. Dispatcher consumes control once externally; no secondwait/agent/model/provider/relaunch. Nativeprivatefolders/files0700/0600; setumask077 in every fresh shell that writes privatescratch. Use existing externalinterpreter `$HOME/envs/llm-slovenian-repair/bin/python`, no bareuvrun or repo.venv/cache writes. REPAIR_ALLOW_LIVE_TESTS=NO; syntheticdata/fakekeys/ephemeralloopbackfixturesonly, no configuredliveendpointlaunch. OAP_ROLE=coding in allhelpers. Bounded test/helper subprocesses allowed, backgroundcodingagents forbidden. Original workingtreeandunrelatedresiduespreserved.

## Documentation

Document exact eligibility and copyconsistency rules, preflight-before-review, validatedrenderpaths, canonicalpositivesandnegativeabstentions. Qualify014-a's overstrongcopyclaim forward in014-b; do not claim beyond actualtestedboundary. Preserve currentprovisionalMVPestimate and independentrights/labels/live/ICA/deployment distinctions; no unrelated gates.

## Git and report publication

Samebranch/samePR16 AMEND_EXISTING_PR. Explicitstageallowlist/order/active and checkindextranscript. Preserveold014areport6c4bf45andallancestry. Coding nevermerges/enablesauto-merge. Finishnonreportcommits, updateexistingPRdescription, capture literalimplementationSHA. Write conciseimmutableSELFreport with exactorderhash, literalparent, percriterionchecks/testedSHA/limits, evidencecorrection, privacy/setup/negativeproof and CriticalactionNONE. Finalcommit only014-breportpath, soleparentimplementation; push, sharedremoteverify exacthead/bytes/shape, thenexactresponseOKonce. No subsequentpush/amend for thisround. Report ownpublication/finalCI asPENDING beforepush; strategyrecordsactualpostpublication results. Counter64->65only for newreport, no pre-reportred disguised as productfailure. No merge until independentreview/all4finalCIgreen.

## Decision classification

D0 ordinary reversible integritybug correction within existing014authority; no productintent change, sourceacquisition or realserviceboundarycrossing.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "014-b",
  "title": "Validate every terminal answer copy before bounded batch review",
  "objective": "014",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_REVIEW_BATCH_CORRECTION",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "6c4bf45060300932f721b31ea51a6da3d82c2984",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/014-bounded-review-batch",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 16,
  "dependencies": [
    "013"
  ],
  "local_work": "Preserve all014-a implementation/report/order commits and all private restoration, branches, ignored environments and untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Trackedbranchclean before publication.",
  "prior_review": "014-a report6c4bf45 independently remotely verified, all4finalCIgreen, independent172tests+5subtestsPASS. Semantic review failed3publishedheadcases: ambiguous terminal copies still reachrepair and are blindlyrewritten. SamePR16 correctiveb required; no merge.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner active goal continue development as planned; existing foreground-only coding and mandatory exact-span Pandoc decisions remain binding."
    },
    {
      "kind": "A",
      "reference": "014-a requirements7,8,9,11 and ARCHITECTURE6,7,12,13: unique original ownership, fail-closed unsupported shape and consistent supported terminal copies without rewriting unrelated fields."
    },
    {
      "kind": "E",
      "reference": "Exact published6c4bf45 actualtransform_sse probes: extra output_text in output_item.done, conflicting content_part.done text and missing content_part.done item_id each callrepair1and changebody; expectedunchanged0. Private014a-final-terminal-integrity-probes.json."
    },
    {
      "kind": "I",
      "reference": "Independent exacthead172PASS5subtests, remoteverifyreport and final4CIgreen were insufficient to cover contradictorycopies. Actualpreflight onlyvalidatesfinalanswer/id/index, renderloopsblindlyrewriteall output_text parts in same-ID terminalitems."
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

# Work order 035-c — Always remove defined API logprobs

Status: FINAL.

## Identity

Objective 035, round 035-c, AMEND_EXISTING_PR 37; branch oap/035-native-rtx3090-qualification; repository ulfe-lmi/llm-slovenian-repair; default main, accepted base 7dcd186fe394c1262bfe878ba5d6527b888fc317. Keep the same PR and branch.

## Provenance

H: The owner now requires ALWAYS removing API logprobs at defined probability locations, for every value and regardless of repair. No switches or recursive deletion of user data/metadata echoes. This supersedes nonempty-logprobs abstention and 035-b null-only compatibility. Other metadata, failure semantics, pinned Pandoc and exact spans remain protected. Existing 1M additional RTX requests, ten needed publication recoveries and no separate human dataset remain authoritative. A/E/I sources are pinned in metadata.

## Current verified state

Actual local/remote PR37 head 553280ae98cefdeb6c4ef868c9f0083502016223, implementation parent 7c8c26edc248406a92f1a30b097aa047c64c5cea; PR OPEN on the same branch, current default main/base 7dcd186fe394c1262bfe878ba5d6527b888fc317. 035-b report is PARTIAL, sole-report commit, exact15341B/hash089128e2..., normal REMOTE verification PASSED (Root97508 exit0), ONE responseOK received (34272 closed0). Root counter test PASSED:96total/95counted/block95; registry42/incidents2 unchanged. Tracked clean, three unrelated roots and key0600/ignored/untracked preserved. The nativeNULL finding and committed patch adb9b050667376d9925a7e04551ce500741f610e69da892b5187ee3ba7618480 are superseded historical baseline, not new-policy proof. Preserve issued history/private evidence. B final-head CI is pending/not required to finish before this concrete same-PR correction; C final-head fourchecks remain mandatory before merge. Existing foregroundCLI3341327/pane%23 is quiescent; same launched argv/profile/home/auth/chat. Prior normal timestamp failure stays recorded; owner10publicationrecoveries(1used) and1MRTX allowance remain valid.

## Governance

Trusted governance 3549de2a436f485a693730d0ee7d5f8c00aec0c0; all 16 identities, frozen registry/173 manifest/CRITICAL/full and compact sources remain unchanged. LR002/003/005/007/009/010/011/013/014 apply. D0, Decision NONE. Owner policy supersedes only the earlier logprobs gate/no-edit raw-body rule needed for removal. Independent evidence and answer protection stay unchanged.

## Goal and dependencies

Implement one mandatory policy: this proxy provides no token probabilities. Remove defined API logprobs independently of optional repair. Without an approved edit, answer text stays identical; metadata removal may change JSON/SSE data. Continue native qualification toward functional MVP. The verified 035-b checkpoint satisfies this dependency; no milestone acceptance is inferred.

## Scope

Allowed non-report paths:

- oap/orders/035-c-strip-defined-api-logprobs.md (exact issued bytes)
- oap/active
- concept-verification/proxy.py (normalization, JSON/SSE integration and necessary status-preserving delivery glue only)
- concept-verification/responses_contract.py (shared defined-location removal and logprobs eligibility change only)
- concept-verification/tests/test_responses_contract.py (policy and actual-HTTP regressions)
- concept-verification/tests/test_review_batch.py (directly affected expectations/helpers only)
- concept-verification/README.md (exact policy and verified behavior)
- oap/audit/results/035-native-rtx3090-qualification.json (current sanitized evidence/supersession)
- research/RESEARCH-STATE.md (only counter 95->96)

Sole report: oap/reports/035-c-strip-defined-api-logprobs.md. Other product/protection/acceptance/transport/dependency/workflow/source/manifest and prior artifacts are frozen. Owned private finite harnesses may live outside the repository.

## Non-goals

No configuration switch, request-capability expansion, generic key scrubber, annotation/citation stripping, weaker completion/ownership/acceptance/Pandoc guards, AST rendering, substring mapping, research/dataset/morphology/packaging gates, new service/model or deployment.

## Files and boundaries

Inspect transform_json/transform_sse/_event/_render_event and handler status/delivery paths; aligned_metadata_clean/validate_completed_envelope; current ContractHttpTests and terminal-copy tests; relevant capture/cancellation and exact-span contracts. Normal compact read set plus this order suffices.

Schema references fetched 2026-11-11: [response schema](https://developers.openai.com/api/reference/resources/responses/methods/create), [streaming schema](https://developers.openai.com/api/reference/resources/responses/streaming-events). Typed API locations:

- Response output[] message items -> content[] output_text parts -> direct logprobs.
- SSE response.output_text.delta/done -> direct logprobs.
- SSE response.content_part.added/done -> output_text part.logprobs.
- SSE response.output_item.added/done -> message item.content[] output_text parts.
- SSE response.created/in_progress/completed/incomplete/failed/queued -> nested response, same output rule.

No traversal into metadata echoes, tool arguments/results, refusal/reasoning data, strings, unknown event types or arbitrary same-named keys. Normalization of recognizable API containers does not grant repair eligibility or invent missing schema/status/ownership.

## Requirements

R1. Use only the existing foreground CLI/session/profile/model/home/auth under externally consumed control. Explicit OAP_ROLE=coding, actual umask077, qualified Python3.12.15-B/private TMP/cache and pinned Pandoc3.7.0.2. Preserve history/work, key0600/ignored/untracked and private0700/0600. No new/background agent, codexexec, configuration/auth or protected host changes.

R2. Delete defined logprobs by KEY PRESENCE, for null/empty/populated/unexpected JSON types alike; absence is harmless. No value/type/truthiness may block repair. Use one bounded schema-directed policy, no switch. Preserve annotations/citations and all other metadata. Never recursively scrub same-named keys or reinterpret unknown user data.

R3. Apply removal before eligibility/no-edit/bypass returns in JSON/SSE, covering every recognized copy. Clean, keep, rejected proposal, corpus/parser/mapping failure, analysis bypass, unsupported and well-formed incomplete/error-bearing responses still remove defined fields while preserving answer text and status. Captured non200 responses retain status/error/zero-review semantics; strip recognizable API locations without changing malformed error-body behavior. Strict malformed/duplicate/nonfinite/invalidUTF8 main failures remain failures. Original capture limits apply BEFORE removal. Preserve cancellation and owned cleanup; no widened fallback or swallowed control exceptions.

R4. Retain current completion/stateless/single-answer/terminal-ownership and annotations gates, isolated one-pass review, independent CPU acceptance and exact original codepoint patching. With no correction, preserve all answer/delta strings and segmentation; only probability-field removal may change wire data. With corrections, only approved spans and established consistent SSE copies change. Other fields/IDs/usage/citations/status and SSE order/framing/id/retry/comments/DONE semantics remain intact. No fields removed and no correction means existing byte-identical output. Keep text-edit flags/metrics distinct from metadata-only changes.

R5. Add meaningful actual-HTTP proxy->realEngine/Pandoc/tinySQLite/detector/reviewerHTTP/CPUacceptance/patcher tests; fakes only at outside upstream endpoints. Cover absent/null/empty/populated and unexpected types (false/zero/string/object), all defined locations, JSON/SSE zero-review and accepted-edit paths. Prove other fields and metadata/tool/user-data echoes unchanged, annotations/citations retain current abstention, and one SSE stream covers all copies. Include multiple message/part copies in an unrepairable response: deletion must reach every defined field. Unknown events carrying lookalike response/item/part data must remain untouched. Location matrices may supplement representative HTTP cases; avoid unnecessary fixture multiplication. Expected results must not call the production normalizer. Update only old logprobs-bypass expectations explicitly superseded by the owner; preserve other negative tests.

R6. Regress malformed JSON/SSE, duplicate/nonfinite/invalidUTF8, incomplete/error/unsupported/ambiguous ownership, mode mismatch, capture overflow even if deletion would shrink it, parser/mapping failures, disconnect/cancel/cleanup, protected code/math/HTML/links/config/quotes/Unicode/CRLF and unapproved slices. Include escaped lone surrogates in answer/metadata: metadata removal must not introduce an encoding failure, drop characters or replace them on a previously preserved response. Well-formed bypasses remove metadata; incomplete capture never becomes complete. Run focused contract/review-batch suites then the full concept suite with pinned Pandoc. Record actual source/hash/exit; old965 is not fresh new-code evidence.

R7. Retest real proxy.main on owned loopback port0, TRACE OFF, matching RTX3090 main/review models, owned synthetic inputs. Verify no defined probability fields in delivered JSON on zero-review and accepted-edit paths; prove identical text or only exact approved changes and other fields unchanged. Demonstrate useful native main->review->independent validation->final behavior or preserve the next precise gap. Fake transport is not native success. Labeled miniature corpus proves mechanics, not linguistic quality; existing authorized readonly index remains optional with evidence limits. Optional bounded native SSE may help, but do not invent another functional gate or a human dataset.

R8. Keep the same 1M-request ledger: reserve main/possible review separately, append durable outcomes, charge unknown delivery, preserve old ledger. Sequential finite reasoned trials, at most1review/1pass, no auto-retries; reviewer45s/child150s/parent180s, output1536 (up to4096 only for proved output-limit issue). Caller waits must allow bounded main+review. Diagnose pre-product failures before product mutation. Preserve separate actual/unknown counts and usage. Ten publication recoveries remain authorized (1used); no new approval question within either allowance.

R9. Document no token probabilities, unconditional/non-configurable removal, no-edit wire changes with identical answer text, exact approved corrections, untouched echoes/other fields. Explicitly supersede null-only/nonempty-abstention in current evidence; preserve issued history. Honest tested SHA/harness/source epochs and real timestamps; no coding MVP/deployment self-certification.

## Acceptance criteria

A1. Every defined field is removed for every value independently of repair; unrelated user data is intact, no switch.
A2. Actual JSON/SSE HTTP integration proves zero-review/edit/metadata integrity and existing failure/capture/cancel/protection contracts.
A3. Native evidence at an exact revision proves the useful path or precisely states its remaining gap, without fake/quality conflation.
A4. Exact scope/privacy/history/report publication and four final-head CI precede development merge; no deployment or human milestone acceptance.

## Verification

From concept-verification: qualifiedPython -B -m unittest tests.test_responses_contract tests.test_review_batch, then -m unittest discover -s tests -v with pinned Pandoc. Preserve relevant existing protection/patch/capture/cancel suites. Shared state/governance at trusted3549de2a, transcript035-c, report-history173manifest, both accepted-base whitespace checks, counter, unpublished preflight and normal REMOTE. Required final-head CI: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history. Pending/missing/cancelled blocks merge, not safe known-gap work.

## Local setup and constraints

Private handoff supplies exact interpreter/parser/key/index/scratch/ledger/endpoint/model/FIFO paths. Verify owner/type/no symlinks/private modes. Child-only live opt-in, no secret copy/stage/dump. Existing Qwen/GPU/services/ports/network and CLI home/auth remain unchanged. Finite owned CPU/Git/HTTP children allowed; clean exact owned resources, never pattern-kill.

## Documentation

README/current035 evidence only, plus counter95->96; registry42/incidents2 and frozen sources/history unchanged. Distinguish metadata-only changes, linguistic edits, local/native/quality/deployment evidence. No human dataset.

## Git and report publication

SamePR37/branch, forward commits. PUSH non-report work and verify remote implementation head BEFORE final private report composition. Record real UTC after actual PRview. Canonical035C report absent during preflight, exact checked copy, sole-pathSELF/literalparent; count-only scan every new blob/message/draft, push normal REMOTE, ONE responseOK then quiesce. Expected pre-report counter mismatch FAILED; final97total/96counted/block96 checked privately. No extra publication approval, merge/auto-merge/deploy.

## Decision classification

D0: explicit owner policy. Strongest counterargument is accidental user-data deletion or altered failure semantics. Mitigate by exact typed locations, no recursive traversal, unchanged answer/other metadata, actual HTTP negative tests and independent final-head review. No new CRIT or release gate.

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
    "LR-002",
    "LR-003",
    "LR-005",
    "LR-007",
    "LR-009",
    "LR-010",
    "LR-011",
    "LR-013",
    "LR-014"
  ],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "id": "035-c",
  "title": "Always remove defined API logprobs from proxy responses",
  "objective": "035",
  "status": "FINAL",
  "phase": "OWNER_DEFINED_API_LOGPROBS_POLICY_AND_NATIVE_QUALIFICATION",
  "base_sha": "7dcd186fe394c1262bfe878ba5d6527b888fc317",
  "branch": "oap/035-native-rtx3090-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 37,
  "dependencies": [
    "035"
  ],
  "local_work": "Actual local/remote PR37 report head553280ae98cefdeb6c4ef868c9f0083502016223, implementation parent7c8c26edc248406a92f1a30b097aa047c64c5cea, branch oap/035-native-rtx3090-qualification OPEN, defaultmain/base7dcd186fe394c1262bfe878ba5d6527b888fc317. Trackedclean,3unrelatedroots preserved, key0600/ignored/untracked; existingforegroundCLI3341327/pane%23 samehome/auth/chat. ExistingNULL-onlypatchADB iscommittedsupersededWIP; preserveit throughforwardcorrection.",
  "prior_review": "035BreportPARTIAL at553280ae98cefdeb6c4ef868c9f0083502016223, soleparent7c8c26edc248406a92f1a30b097aa047c64c5cea/solepath,15341B SHA256089128e2f602e533a1726b942008f3407ef39ffa65eeed1c5ee344e96bc8e041. NormalREMOTEverify97508RC0, oneexactresponse34272CLOSED0, RootfinalcounterPASS96total/95counted/block95. NewownerALWAYS-removalnotimplemented; Rootreviewrequires035CsamePR, notBmerge. Historicalproofepoch/setup qualifications in035b-root-final-remote-semantic-review-for-035c-20261111.json. Owner1MRTX+10pubrecoveries(1used)persist; no newpermission.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Actualowner2026-11-11 decision: ALWAYS remove APIlogprobs atdefinedprobabilitylocations independentofrepair/value, JSON/SSE, no configswitch, preserveothermetadata/error/capture/cancel/Pandoc/exactspans. Nohuman dataset;1MRTX+10publicationrecoveriesreconfirmed."
    },
    {
      "kind": "A",
      "reference": "PLAN5/11/13 andARCH13-16 capture/isolation/originalspans/metadata/resource/error contracts remain; current owner explicitly supersedes earlier015logprobs-abstention and035BNULL-only/no-editrawbyte policies only as needed for definedmetadata removal."
    },
    {
      "kind": "E",
      "reference": "Native035Battempt7 actualworker/clientobservedlogprobsNULL, contractrejectedbeforeCPU; predecisionNULL-onlyworkingpatchSHAadb9b050667376d9925a7e04551ce500741f610e69da892b5187ee3ba7618480 provenmechanicallybyRootactualHTTP6cases, now supersededdesiredbehavior."
    },
    {
      "kind": "I",
      "reference": "Root inspectedactualtransform_json, transform_sse andHandlerstatus200branch, including numerous no-edit/ineligibleearlyreturns andSSEterminalcopies. OfficialResponses schema identifies typednormalizationlocations; no genericrecursivekeydeletion is authorized."
    }
  ],
  "relevant_gates": [],
  "decision_class": "D0"
}
```

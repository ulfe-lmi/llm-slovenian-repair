# Work order 007-e — Recover forward from an immutable invalid report

Status: FINAL

```oap-metadata
{
  "id": "007-e",
  "title": "Recover forward from an immutable invalid report",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": [
    "001",
    "002",
    "003",
    "004",
    "005"
  ],
  "local_work": "Local and remote PR #8 head 88af5cefb76e5aaf727806ff589df93fa08f0861. Preserve dirty research/tests/test_strategic_campaign_replay.py unchanged and uncommitted during this protocol-only round; it is a strategic regression for subsequent archival correction.",
  "prior_review": "007-d is a remotely published, report-path-only immutable artifact, but strict validation fails REPORT_CHECK because checks[6].sha is abbreviated. It is NOT an accepted or verified report. Research/OAP-history CI pass; OAP-bootstrap and inherited Application-baseline CI fail. No merge.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner authorizes all forward-correction paths after the immutable 007-d report/transition deadlock was explained; this is forward-only protocol recovery and continuation of research archival work, not historical rewrite, scientific rerun or merge."
    },
    {
      "kind": "A",
      "reference": "Strategic communication section 7 requires correction after final report via a new suffix on the same PR, never amendment; S-PROTOCOL-01 and S-REVIEW-01 require truthful durable publication and strict independent acceptance."
    },
    {
      "kind": "E",
      "reference": "At 88af5cefb76e5aaf727806ff589df93fa08f0861 strict verify_report raises REPORT_CHECK; report check[6].sha=33e8d9a. Actual implementation parent=97eceffa4c1ca60f1b0cea0fef30a4dc54be18df. transition requires that invalid report to validate before permitting 007-e."
    },
    {
      "kind": "I",
      "reference": "Strategic reconciliation proves this is a protocol deadlock, not missing report bytes or permission to alter immutable history. Existing 006 history incidents remain distinct and exactly frozen."
    }
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
  "lr": [
    "LR-007",
    "LR-008",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "OAP report history",
    "Application baseline",
    "Research reproducibility"
  ],
  "decision_class": "D0",
  "prior_report_recovery": {
    "schema_version": 1,
    "classification": "INVALID_QUARANTINED",
    "prior_id": "007-d",
    "corrective_id": "007-e",
    "repository": "ulfe-lmi/llm-slovenian-repair",
    "pr": 8,
    "branch": "oap/007-concept-verification",
    "report_path": "oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md",
    "publication_commit": "88af5cefb76e5aaf727806ff589df93fa08f0861",
    "report_blob": "5bf351e69509f61860e123790d80f889ef2bfdf4",
    "report_sha256": "d19ac48b77f8d856ec79214de83590f0dcfc0cdf1c11b61c4ba421a962f864dd",
    "implementation_parent": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
    "order_path": "oap/orders/007-d-complete-research-publication-and-reproduction-coverage.md",
    "order_sha256": "5f5cf095cad7a0c30307b715d37781ba52da09aa6160f31bd0140a9bc774afec",
    "validation_error": "REPORT_CHECK",
    "reason": "checks[6].sha is abbreviated 33e8d9a; strict report acceptance remains invalid. Unique resolution 33e8d9a0e15dcb24749f79962087097e7b000123 is diagnostic only, not replacement report bytes.",
    "authority": "Explicit owner authorization of all forward-correction paths; strategic order selects only immediate same-objective same-PR corrective transition.",
    "evidence_scope": "Provenance and frozen publication identity only; not acceptance, successful checks, milestone clearance or merge authority."
  }
}
```

## Identity

Immediate corrective suffix after 007-d, SAME objective 007 branch and PR #8.
PROTOCOL RECOVERY ONLY. Coding implements this order and publishes one report;
strategy then reviews before issuing the separate remaining archival correction.

## Provenance

The owner explicitly authorized all forward-correction paths after the report
deadlock was explained. Existing communication law already requires a new suffix
after publication. This order makes that path executable without pretending an
invalid report was valid. No scientific outcome is changed or accepted.

## Current verified state

Main ee2d1b479719009ff1d07829478f241e3f395f7c; PR #8 OPEN/unmerged at
88af5cefb76e5aaf727806ff589df93fa08f0861. The report has sole parent
97eceffa4c1ca60f1b0cea0fef30a4dc54be18df and is its only changed path.
The exact report blob/hash and prior order hash are in metadata. Strict validation
returns REPORT_CHECK, not success. OAP report history and Research reproducibility
CI passed; OAP bootstrap acceptance and inherited Application baseline failed.
Main protection remains disabled; do not change it or merge.
Preserve the one dirty strategic research regression exactly.

## Governance

All governance identities in metadata remain unchanged accepted main identities.
CRITICAL has no actual entries and is READ ONLY. This is a D0 implementation of
explicit owner direction, not discretionary human judgment or human acceptance.
Protected full/compact laws, architecture, PLAN, manifests and seeds stay unchanged.
Operational helper documentation may clarify implementation without rewriting law.

## Goal and dependencies

Allow truthful forward correction of a structurally immutable, published but
schema-invalid report while strict report acceptance and historical immutability
remain enforceable. Prevent malformed drafts from becoming final publications.
This unblocks the still-unfinished research archive; it does not claim that archive
is complete. The existing 15 saved replay failures and variant gaps are deferred
to the subsequent same-PR archival order, not ignored.

## Scope

Allowed: oap/bin/oap_core.py, oap/bin/oap_cli.py, oap/bin/oap_runtime.py,
a small new shared helper/CLI under oap/bin/ if useful, focused oap/tests/,
a new oap/operations/forward-report-recovery.md guide, this exact order/active/new
report, and PR #8 description metadata. No unrelated workflow changes are needed.
Read related helper/test files as required. Existing oap/orders/** and
oap/reports/** are immutable, including 007-d. The current known 006-a/006-c
history exception identities and semantics must remain unchanged.

## Non-goals

No report amendment, restoration, rebase, history deletion, generic mutation
allowlist, acceptance weakening, merger, new objective, research implementation,
scientific evaluation, Qwen/model call, corpus acquisition, model/profile/service
change, source redistribution, production change or inherited baseline repair.

## Files and boundaries

Inspect the actual transition, validate_report, verify_report, check_transcript,
protocol_state, doctor, launch and strategic-gate entry points. Keep shared proofs
shared. Fakes belong at remote/model boundaries, not at the validator under test.
Read only this order and normal compact coding read set plus relevant helpers;
full strategic doctrine is not an additional coding read obligation.

## Requirements

1. Preserve every historical report/order/commit and the dirty strategic research
   test. Record 007-d as INVALID_QUARANTINED by the exact metadata identities above,
   never repaired in place or retroactively accepted. Its structural publication
   identity is usable; its report schema/check claims are not acceptance evidence.
2. Separate strict report validity from proof of immutable publication. Add a
   minimal explicit forward-recovery contract bound by the next immutable order.
   Support the prior_report_recovery metadata above without changing this order
   after publication. Prove actual report-only first publication, sole actual
   implementation parent, exact report and order bytes/blob/SHA, existing history
   guard, order/PR/branch identity, and the observed strict validation error.
   Metadata cannot authorize mutation or self-attest human acceptance.
3. Permit recovery only to the immediate next suffix on the SAME objective,
   branch and OPEN PR, with remotely verified publication head at transition time.
   Strict validation must actually fail as declared. Reject bogus errors, absent/
   stale/wrong hashes, altered report or order, wrong parent/branch/PR, suffix gaps,
   missing receipt/linkage, closed PR, and numeric advance. If an invalid artifact
   cannot satisfy immutable structural publication proof, fail closed and expose
   the exact boundary; do not add a historical-mutation exception.
4. Keep validate_report/verify_report strict: direct verification of 007-d must
   continue to fail REPORT_CHECK. For historical transcript checks, recognize ONLY
   a proved, exact, subsequent corrective-order linkage and expose the invalid
   report distinctly in output. Do not silently list it as validated acceptance.
   Current malformed reports still block readiness/merge. Later corrective evidence
   may address defects, but quarantine itself grants no completion or merge.
5. Reconcile publisher, check_transcript (index and revision), protocol_state/
   check_state, doctor, coding launch and strategic gate around the same proofs.
   A pushed invalid report means forward-correction required, never rerun its
   completed old coding round. Duplicate control for that old round must not
   invoke a model. The next unfinished corrective round may run normally.
   All failures remain visible; no broad catch-and-pass or skip-validation flag.
6. Add draft-report pre-publication validation at the real command boundary,
   checking schema, full literal check SHAs and ancestor relation, actual
   implementation HEAD, matching active/order and valid SELF/pre-push claims.
   It must work on an unpublished draft without falsely claiming remote publication.
   Use it BEFORE creating this round's report-only commit. Do not normalize an
   abbreviated SHA silently, alter published files or fabricate future CI success.
7. Add minimal real-Git positive/negative tests for the actual publication/
   transcript/state/launch paths: valid forward suffix succeeds; malformed current
   report remains invalid; missing linkage, wrong hashes/error/parent, same-ID
   rewrite, delete/re-add, suffix gap, wrong PR/branch and numeric advance fail.
   Prove an invalid old report cannot launch coding after duplicate FIFO control;
   prove a correct new round can. Existing 006 exact incidents remain frozen;
   any new touch still fails. Test draft short SHA rejection and correct full-SHA
   draft success. No fake replacement of the gate being claimed.
8. Verify the new e publication is strict-valid and transcript remains explicitly
   qualified about d. Run full OAP tests, focused new real-history/process tests,
   existing research tests (report the known unrelated dirty regression failure,
   do not fix or commit it here), governance/protected diff and git fsck.
   Record inherited application failure rather than fixing it. Update PR body
   with actual state, no acceptance/merge claim, using metadata only.
9. Keep all outputs/scratch/envs outside /tmp in the persistent owned native task
   directory. No dataset rows, raw scientific model responses/prompts, credentials
   or private endpoint configuration in public files or report.

## Acceptance criteria

The published 007-d bytes and all earlier report histories are unchanged.
Strict verification still rejects d. Exact authorized e recovery is executable,
but malformed/forged/mutating/numeric-advancing alternatives fail. Index/revision
transcripts show d as quarantined, and a valid new report can be strictly checked.
The real launcher cannot re-run d on duplicate signal. Draft preflight catches
the precise short-SHA defect before commit. No research/production science changed.
All new guards and existing OAP/history tests pass; any unrelated known failure
is accurately separated, not relabelled.

## Verification

Use focused unittest tests then python3 -m unittest discover -s oap/tests -v.
Run real-history tests in a full-history disposable native checkout rather than
a snapshot that skips them. Run python3 -m unittest discover -s research/tests -v
and identify the already-dirty retry-only replay regression as outside this order.
Run check_transcript.py in index and committed revision modes, check_report_history,
accepted-runtime check_governance with literal main SHA above, exact protected
source diff and git fsck. No live model service is required or authorized.
Record tested SHAs, commands and limitations. Current-head GitHub results are
strategy's post-publication observation, never predicted inside the report.

## Local setup and constraints

Use persistent native scratch:
 /home/ubuntu/.local/share/llm-slovenian-repair/research-runtime-20260911.YJemoq/007-d-scratch
or a uniquely named child. Set TMPDIR explicitly; do not put artifacts in /tmp.
The sync workspace can invalidate inherited cwd; start commands with a fresh
absolute cd to REPO_ROOT. Do not change the mount or role/profile configuration.
For costly tests, use a full-history clean native copy with byte-verification.
Do not copy ignored environments/cache repeatedly into fixtures; keep actual
tested code unchanged and record native-copy/source identities.

## Documentation

Write a concise operational guide explaining invalid publication vs strict
acceptance, exact recovery receipt/linkage, helper commands and bounded historical
evidence. Preserve this order's one-time bootstrap disclosure: before this fix,
strategy used an owner-authorized private exact-identity transition adapter around
the existing publish helper's governance, lock, immutable-order and active writes.
It did NOT change the report, patch repository helpers before ordering, fake
remote evidence or grant report acceptance. Permanent recovery must no longer
require that adapter.

## Git and report publication

SAME branch oap/007-concept-verification, SAME PR #8; no merge.
Commit this order and active during implementation. Do NOT commit the pre-existing
dirty research/tests/test_strategic_campaign_replay.py. Commit only ordered paths.
Capture full implementation HEAD after tests/implementation; preflight the report
draft. Final report is a NEW report-path-only commit matching this order filename.
Use SELF and publication_verified=false. Push normally, verify real remote report,
then exact response OK. If publication fails, preserve evidence; never edit a
published report. Coding stops after this one round; strategy owns further orders.

## Decision classification

D0: explicit owner-authorized forward-only protocol integrity correction.
Strongest concern: a recovery route could launder invalid reports into acceptance.
Mitigation: distinct quarantine evidence, unchanged strict validation and history
guard, exact Git/remote binding, immediate same-PR suffix only and negative tests.
No CRITICAL debt, acceptance, release or deployment authority is created.

## Deferred human adjudication

- Decision: NONE


# Work report 007-e — Recover forward from an immutable invalid report

```oap-report
{
  "id": "007-e",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md",
  "order_sha256": "454f91b1f98d3a0ddbafbc93c0b12be9c8517661db1f132b000cdaf0fc5b6875",
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
  "publication_commit": "SELF",
  "implementation_head": "17ee857e95c916b8733973e68cb4b9898efc50fe",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "88af5cefb76e5aaf727806ff589df93fa08f0861",
  "no_merge": true,
  "checks": [
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B -m unittest oap.tests.test_forward_recovery -v",
      "result": "PASSED",
      "details": "16 disposable full-history recovery tests passed, including initial transition, activation retry, protocol-state phases, draft preflight, transcript revision/index chronology, receipt identity, mutation, delete/re-add, and duplicate-control paths.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "120 OAP acceptance, process, report-history, split-layout, transcript, and forward-recovery tests passed in 664.745 seconds.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B -m unittest discover -s research/tests -v",
      "result": "FAILED",
      "details": "38 research tests ran; the pre-existing dirty retry-only regression failed with ValueError saved retry proposal missing for offset 5. No research file was changed by this round.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure and compact coding read-set checks passed; semantic and human authorization proof remain false.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "The report-history guard passed with the two known frozen 006 incidents and no new report mutation.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B oap/bin/check_transcript.py --repo-root . --revision 17ee857e95c916b8733973e68cb4b9898efc50fe --expected-id 007-e",
      "result": "PASSED",
      "details": "Committed revision transcript passed; 007-d is listed only as INVALID_QUARANTINED with REPORT_CHECK and 007-e is its immediate descendant order.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-e",
      "result": "PASSED",
      "details": "Index transcript passed the same quarantine classification and exact-order selection checks.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP python3 -B oap/bin/verify_report.py --repo-root . --id 007-d --commit 88af5cefb76e5aaf727806ff589df93fa08f0861",
      "result": "FAILED",
      "details": "Expected strict REPORT_CHECK because immutable 007-d records abbreviated check SHA 33e8d9a; its bytes and history remain unchanged.",
      "sha": "88af5cefb76e5aaf727806ff589df93fa08f0861",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP git diff --check 88af5cefb76e5aaf727806ff589df93fa08f0861 17ee857e95c916b8733973e68cb4b9898efc50fe -- . :(exclude)oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md",
      "result": "PASSED",
      "details": "Scoped implementation diff has no whitespace errors; the immutable 007-e order was excluded because its pre-existing trailing blank warning is preserved.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP git diff --check 88af5cefb76e5aaf727806ff589df93fa08f0861 17ee857e95c916b8733973e68cb4b9898efc50fe -- oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md",
      "result": "FAILED",
      "details": "Known pre-existing new blank line at EOF on the immutable published order; the order was not edited.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP git fsck --full --no-reflogs --no-progress",
      "result": "PASSED",
      "details": "Object check exited zero and reported only expected dangling scratch blobs/trees.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "env TMPDIR=ROUND_TMP git fsck --full --no-progress",
      "result": "FAILED",
      "details": "The full check reports pre-existing invalid reflog entries and dangling objects; no repository refs or reflogs were rewritten in this round.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    },
    {
      "command": "git push origin HEAD:refs/heads/oap/007-concept-verification; git ls-remote origin refs/heads/oap/007-concept-verification; gh api repos/ulfe-lmi/llm-slovenian-repair/pulls/8",
      "result": "PASSED",
      "details": "Non-report implementation commits are remotely present at 17ee857e95c916b8733973e68cb4b9898efc50fe; PR #8 is open, unmerged, and uses main as base. No report publication is claimed here.",
      "sha": "17ee857e95c916b8733973e68cb4b9898efc50fe",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-12T02:27:19+02:00",
  "report_written_at": "2026-09-12T02:27:19+02:00",
  "implementation": "Implemented the permanent forward-recovery path for an immutable published report whose strict schema is invalid. The normal initial publisher now uses a structural quarantine proof only for the exact declared prior report, then enforces immediate same-objective suffix, same open PR, branch, and exact old remote head. Active corrective orders use local structural proof across implementation descendants; a present corrective report is strictly checked separately. Recovery paths bind exact committed report/order names, blobs, bytes, SHA-256 values, sole parent, first publication, history, chronology, selected transcript revision/index, and the receipt classification, corrective ID, and reason. Draft preflight is unpublished-only and requires full literal check commits and ancestry. Strategic gate report verification is mandatory at the shared function boundary.",
  "documentation": "Added the forward-report-recovery operational guide with strict-versus-structural semantics, phase-specific helper commands, receipt linkage, draft preflight, transcript chronology, and bounded evidence notes.",
  "criteria": "All numbered 007-e protocol criteria are implemented and covered by real Git disposable histories or the actual shared entry points. Strict validation still rejects 007-d; valid 007-e recovery is structurally recognized without accepting the old report; malformed, forged, mutating, gap, identity, parent, path, remote-head, and duplicate-control alternatives fail closed.",
  "negative_paths": "Focused tests cover missing linkage; wrong classification, corrective ID, reason, hashes, declared error, path, parent, branch, PR, suffix, objective, and same-ID receipt; report mutation and delete/re-add; disconnected revision; malformed current report; exact old-head drift; draft short SHA and already-published rejection; and old duplicate control without a model call. The full OAP suite adds existing immutable-history, FIFO, process, governance, and transcript negatives.",
  "boundary_fidelity": "Only the 007-e implementation scope, exact order/active transition, generated metadata, operational guide, acceptance call-site arguments, and focused OAP tests changed. The published 007-d report and all prior reports/orders remain byte-identical. The pre-existing dirty research regression remains unstaged and unchanged. No model, dataset, corpus, service, GPU, gateway, production, baseline, merge, release, or deployment boundary was touched.",
  "setup": "Reconciled consumed SAME 007-e on branch oap/007-concept-verification and PR #8. All disposable fixtures and command outputs used persistent native TMPDIR /home/ubuntu/.local/share/llm-slovenian-repair/research-runtime-20260911.YJemoq/007-d-scratch/round-007-e-tmp. The first strategy interruption occurred after material-gap review and before any implementation/report commit, not from a product or test failure. A second safe-boundary interruption occurred after review of revised code; both were resumed truthfully in this same ID.",
  "privacy": "No dataset rows, private text, prompts, replacements, raw model responses, credentials, private endpoints, corpus bytes, or model weights were added to Git, logs, or this report. Tests use synthetic data, injected fake remote/model edges, and owned disposable histories.",
  "limits": "The required research suite has one known failure in the pre-existing dirty retry-only regression and was not repaired. Full fsck reports pre-existing invalid reflog entries; the no-reflog object check exits zero with dangling scratch objects. The immutable order has a preserved trailing blank warning. These limitations do not weaken strict report or recovery validation. No human acceptance, product correctness, scientific result, merge readiness, release, or deployment authority is claimed.",
  "human_gates": "D0/NONE. CRITICAL is empty. This report records implementation and evidence only; it does not append critical history, accept a report, merge PR #8, enable auto-merge, repair the inherited baseline, or authorize release/deployment.",
  "scope": "Finished only SAME 007-e. Implementation heads 02084dd and 17ee857 were pushed to existing PR #8; the literal final implementation head is 17ee857e95c916b8733973e68cb4b9898efc50fe. This draft was preflighted before the report-only commit. The final publication commit must contain only this report and use the implementation head as its sole parent.",
  "result_summary": "COMPLETE for the ordered protocol recovery implementation, with strict 007-d quarantine preserved and the known research regression, fsck reflog issue, and immutable-order formatting warning explicitly retained as limitations. PR #8 remains open and unmerged; no acceptance or release claim is made.",
  "interruption_record": "Strategy deliberately interrupted the prior process before implementation/report publication after identifying material gaps. After the revised code review, a second safe-boundary interruption occurred before tests/publication. No work was relabelled as a test failure, no new suffix was assigned, and this report is the same 007-e recovery round."
}
```

## Result

007-e completes the protocol-only forward recovery implementation. Its structural
proof keeps 007-d immutable and explicitly quarantined because strict report
validation still returns `REPORT_CHECK`. The corrective route is bound to the
exact next order, publication ancestry, report/order identities, existing PR,
and phase-specific remote checks.

## Evidence and limitations

The full OAP suite passed at the implementation head. The research suite was
run as required and retains one failure from the pre-existing dirty retry-only
regression; that file was not changed. Full fsck retains pre-existing reflog
errors, while the no-reflog object check exits zero with dangling scratch
objects. The immutable order’s trailing blank warning was observed and left
untouched.

## Deferred human adjudication

- Decision: NONE

# Work order 008-e — Quarantine the machine-invalid 008-d report, restore transcript coherence, and register the round

Status: FINAL

Finalized by strategic review of 008-d (final head
c0786f9898d3a97aefe9d063bcd43210c0d7d2f1, report-only commit over
implementation head 3baa4f3318f76ba5fc44260829f3f593832695bf, base
4b6a90ab13c0c9a02e533a2673a084e26f841a5c) per the explicit human
instruction of 2026-09-18 (finish the current corrective work correctly
without weakening, skipping, or redefining any check, without
manufacturing green status, milestone, deployment, or linguistic
acceptance, and keep the loop moving). Independently verified strategic
review found: (1) the 008-d implementation and bookkeeping accepted as
published; (2) the 008-d report MACHINE-INVALID - three of its fifteen
checks[] command strings carry angle-bracket placeholder tokens
(assembly artifact), so validate_report rejects the whole report with
REPORT_CHECK while every other recorded check, SHA, and identity field
is valid; (3) consequently the OAP bootstrap acceptance required check
is red at the 008-d final head, deterministically
(RECOVERY_LINKAGE_MISSING in committed-transcript coherence: the invalid
008-d report has no prior_report_recovery linkage, and reruns of the
identical commit cannot clear it); (4) the other three required checks
at the 008-d final head: Research reproducibility PASS, OAP report
history PASS, Application baseline green via a verbatim identical-commit
rerun of the zero-failure full-pytest TIMEOUT class (attempt 1 red at
the frozen 300 s cap with zero test failures; attempt 2 success on the
same commit - the current check state). The same defect class previously
invalidated the 007-n report (checks[5].command angle-bracket
placeholder), which was resolved by the 007-o order's forward-recovery
quarantine; the 007-d report was resolved identically by 007-e. This
round is therefore the bounded forward-recovery corrective suffix on the
same objective-008 branch and PR #9: it quarantines the 008-d report by
the canonical prior_report_recovery linkage (no report or order byte is
altered), re-verifies the 008-d evidence claims, registers the round in
the research ledger and machine block, corrects the now-stale suffix
reference in current status documentation (blind hidden acceptance and
the final objective-008 disposition are round 008-f, not 008-e), and
publishes a validator-valid 008-e report that additively records the
008-d final-head CI truth. The round makes NO gate, cap, driver,
workflow, or test change. A BLOCKED outcome is predeclared and permitted
for the Application baseline only, under the identical bounded
zero-failure-TIMEOUT observation policy as 008-d. No hidden-set
evaluation occurs in this round; that is 008-f. No linguistic-method
change of any kind occurs; the frozen 007-m system and the frozen 008-c
implementation remain byte-identical. No model call is made.

```oap-metadata
{
  "id": "008-e",
  "title": "Quarantine the machine-invalid 008-d report, restore transcript coherence, and register the round",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "c0786f9898d3a97aefe9d063bcd43210c0d7d2f1",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "dependencies": ["008"],
  "local_work": "Preserve byte-for-byte: every merged 000-007 seam on main, the entire research/ tree at the 008-d final head (including the frozen 008-a baseline under research/prose-boundary/: config/experiment-008a.json, fixtures/, results/increment1/, results/increment2/, REPORT.md, adapter/ source, identity/), the 008-c parser-first implementation (research/curated/prose_boundary.py, research/curated/protected.py, all research/prose-boundary/config/ files, the committed corpus under research/prose-boundary/corpus/, results/increment3/, results/baseline-timing/008d-decomposition.json), the 008-c focused test file research/tests/test_parser_first_protection.py byte-identical, ALL other test files byte-identical, scripts/verify_development_baseline.py byte-identical, all .github/workflows/ byte-identical, the committed 008-d order (oap/orders/008-d-application-baseline-restoration.md) and the committed 008-d report (oap/reports/008-d-application-baseline-restoration.md) byte-identical (the 008-d report is quarantined, never rewritten), every private experiment root (including the sealed 008c-hidden/ private root - manifest-hash access only, no hidden content reads in this round), and any unrelated local work (untracked .research-test-scratch/, any untracked root corpus/ residue, and any untracked .venv - never commit any of them).",
  "prior_review": "Strategy independent final-head review of 008-d (2026-09-18, private workorders/008-d-final-head-review-20260918.md): report-only commit c0786f9 (sole parent 3baa4f3, sole changed path oap/reports/008-d-application-baseline-restoration.md, 56,052 bytes, content sha256 6efbf90ee83e76997eb84985e3fe6f3498ba837a2998900094a0f4238c785a60, git blob 13effeaae9ec50ae9779d5ab0caa3c568a88362b); response OK frame received; root cause independently reproduced - exactly three of fifteen checks[] command strings carry angle-bracket spans (checks[5] temp-parent placeholder, checks[6] helper/TMPDIR placeholders, checks[8] source placeholder) and oap_core meaningful() (line 540) + validate_report (line 1158) reject the report with bare REPORT_CHECK, while every checks[] sha is a full 40-hex commit and every result token is valid; the identical latent class exists in the already-quarantined 007-n report checks[5]; all other publication invariants hold (agent isolated-verify-proof.json with only the angle-bracket clause relaxed = verified remote); CI at c0786f9: Research reproducibility PASS (35381405131), OAP report history PASS (35381405199), Application baseline run 35381405077 attempt 1 RED (zero-failure TIMEOUT class at the frozen 300 s cap) then attempt 2 SUCCESS (identical-commit green rerun = current check state), OAP bootstrap acceptance FAIL (deterministic RECOVERY_LINKAGE_MISSING; reruns cannot clear); bookkeeping independently verified (registry 28, machine block 28/47/2 consistent at the report head, RESEARCH-STATE note additive, STATUS.md suffix correction in place, hidden seal 4091/4091 with manifest sha256 8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18 unchanged); disposition: 008-d implementation accepted, 008-d report INVALID_QUARANTINED by this order's prior_report_recovery linkage, development merge of PR #9 at c0786f9 BLOCKED (one required check red, deterministic), corrective suffix 008-e consumes this identifier and the blind hidden acceptance plus final objective-008 disposition are renumbered to 008-f; PR #9 open/unmerged, auto-merge disabled, main still 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9.",
  "prior_report_recovery": {
    "schema_version": 1,
    "classification": "INVALID_QUARANTINED",
    "prior_id": "008-d",
    "corrective_id": "008-e",
    "repository": "ulfe-lmi/llm-slovenian-repair",
    "pr": 9,
    "branch": "oap/008-prose-boundary-qualification",
    "report_path": "oap/reports/008-d-application-baseline-restoration.md",
    "publication_commit": "c0786f9898d3a97aefe9d063bcd43210c0d7d2f1",
    "report_blob": "13effeaae9ec50ae9779d5ab0caa3c568a88362b",
    "report_sha256": "6efbf90ee83e76997eb84985e3fe6f3498ba837a2998900094a0f4238c785a60",
    "implementation_parent": "3baa4f3318f76ba5fc44260829f3f593832695bf",
    "order_path": "oap/orders/008-d-application-baseline-restoration.md",
    "order_sha256": "4e15638298f40b8871c2638371a2b5bfefa7d7df465d32eea6f1b907a9dfcbab",
    "validation_error": "REPORT_CHECK",
    "reason": "The 008-d report checks[5].command, checks[6].command, and checks[8].command record assembly-time placeholder tokens (angle-bracket-wrapped phrases where the literal temp parent path, the pinned helper environment value, the owned TMPDIR value, and the repository source value had to be recorded); validate_report applies the meaningful() predicate to every checks[] command string and that predicate rejects any string containing an angle-bracket span, so it rejects the whole report with REPORT_CHECK while every other recorded check, SHA, and identity field is valid. The defect is formal, not scientific: the 008-d implementation and bookkeeping were independently accepted by strategy on 2026-09-18 (private workorders/008-d-final-head-review-20260918.md), and the identical latent placeholder class in the earlier committed 007-n report (its checks[5].command temp-parent placeholder) is already quarantined under this exact mechanism by the 007-o order. The unique resolution is the forward-recovery quarantine by this exact next order on the same objective, branch, and PR; no byte of the 008-d report or order is altered, and the 008-d evidence claims are re-verified in this 008-e round.",
    "authority": "Owner instruction 2026-09-18 (current turn): finish the currently active corrective work correctly; resolve the current failure according to existing OAP recovery law without weakening any gate and without manufacturing green status; do not merge a red head; do not skip the report-only final state; the owner is not a terminal relay. OAP recovery law: a correction after the final report uses a new strategic corrective suffix on the same PR, never a mutated historical report. Precedents: the 007-d report was quarantined by the 007-e order; the 007-n report was quarantined by the 007-o order with this exact protocol block.",
    "evidence_scope": "Provenance and frozen publication identity only. Not acceptance of the 008-d report, not evidence that its checks passed, not milestone clearance, not merge authority."
  },
  "provenance": [
    {"kind": "H", "reference": "Human instruction 2026-09-18 (current turn): (1) finish the currently active corrective work correctly before any further scientific work; (2) ensure Application baseline, Research reproducibility, OAP bootstrap acceptance, and OAP report history are genuinely green at the reviewed final head, without weakening, skipping, or redefining any check; (3) correct materially stale current-status documentation when scope/governance permits, including any stale PR-status or round-suffix wording; (4) if a failure is unrelated inherited debt, classify it precisely and propose a separate bounded correction order - do not smuggle an unrelated fix into this round; (5) keep the Concentrated-OAP loop moving; the owner is not a terminal relay; D0/D1 are strategy's to resolve, only genuine D2 escalates. Continuing context of the 2026-09-17/18 research decisions: 008-a GO is supporting evidence only; LLM calls are authorized strictly for structural test-data generation (this round makes none); objective 009 remains separate and untouched; the frozen 007-m linguistic method is never tuned."},
    {"kind": "A", "reference": "S-REVIEW-01 (independent final-head review; post-publication checks recorded privately), S-RECOVER-01 (unverified publication enters explicit recovery; pushed report reviewed without coding replay), S-MERGE-01 (a failed required check blocks the development merge; a red head is never merged), S-ORDER-02/03 (exact order contract; corrective suffix preserves the objective branch and PR and is the exact next suffix), S-EVIDENCE-01 (truthful distinct recording of PASSED/FAILED/TIMEOUT/PENDING per head and SHA), S-DHA-02 (mitigation/superseding implementation does not close anything; no CRIT action in this round), the oap_core forward-recovery contract (prior_report_recovery schema v1: INVALID_QUARANTINED classification, REPORT_CHECK validation error, exact frozen publication identities, transcript sequence, remote head/base/duplicate-PR proof), the 007-e/007-d and 007-o/007-n quarantine precedents, the 004-d scoped generated-file pin precedent (oap/GENERATED-FILES.json STATUS.md entry), the 008-b/008-d ledger-registration pattern (registry kind audit entry + machine-block update), P-SELF-03 (a pre-push report never claims future push/CI success; publication_verified=false convention)."},
    {"kind": "E", "reference": "Strategy-verified CI facts at the 008-d final head c0786f9 (2026-09-18, GitHub): Research reproducibility PASS (run 35381405131, 30 s); OAP report history PASS (run 35381405199, 8 s); Application baseline run 35381405077 attempt 1 failure in the zero-failure full-pytest TIMEOUT-at-frozen-300s-cap class (the c0786f9 tree adds only order/report/bookkeeping files over the 008-c final head, whose four verbatim observations were 337.20 s, 335.98 s, 334.01 s with zero test failures, against the 2026-09-17 pool reference 134.92 s), attempt 2 = SUCCESS on the identical commit (current check state green; verbatim green-run session summary recorded in this round's report); OAP bootstrap acceptance FAIL (run 35381405199, stage 'Check committed transcript coherence', error RECOVERY_LINKAGE_MISSING, operation transcript) - deterministic until the prior_report_recovery linkage is committed. Local reproduction: verify_report --id 008-d returns REPORT_CHECK at c0786f9 (local and remote); strategy parse of the committed 008-d report fence locates exactly the three angle-bracket command spans; check_transcript --revision HEAD --expected-id 008-d fails with RECOVERY_LINKAGE_MISSING locally. Agent handoff records preserved privately (008d-handoff/: minimal-fix.txt, isolated-verify-proof.json, verify-local-failure.txt, verify-remote-failure.txt)."},
    {"kind": "I", "reference": "Strategy independent final-head reviews: workorders/008-d-final-head-review-20260918.md (this round's direct basis: root cause, quarantine decision, merge BLOCKED, 008-f renumbering), workorders/008-c-final-head-review-20260918.md (the D1 renumbering discipline and the pool-regime classification), and the committed 007-o order metadata (the prior_report_recovery template and the 007-n quarantine identity)."}
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
  "lr": ["LR-007", "LR-008", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Fifth round of objective 008, amending the objective-008 branch
`oap/008-prose-boundary-qualification` and PR #9. 008-a (frozen head
8dbb79a20f129d4c07c6b94827cacad74683ba6b) qualified `pulldown-cmark`
0.13.4 with outcome GO (supporting evidence only, per the 2026-09-17
human decision); 008-b (final head
49e4e70f1a8c304b4ad5ce27055a39e9e6e17288) restored the post-merge
research-state identities and registered 008-a in the ledger; 008-c
(final head 4b6a90ab13c0c9a02e533a2673a084e26f841a5c) implemented the
parser-first structural protection layer, the authorized generated
structural evaluation program, and the sealed hidden acceptance set;
008-d (final head c0786f9898d3a97aefe9d063bcd43210c0d7d2f1) observed
the frozen application-baseline stage, committed the data-free timing
decomposition, and registered the round - its implementation and
bookkeeping are accepted, but its report is machine-invalid (three
checks[] command strings carry angle-bracket placeholder tokens;
validate_report rejects with REPORT_CHECK). This round is the
forward-recovery corrective suffix mandated by the OAP recovery law:
it quarantines the 008-d report through the canonical
prior_report_recovery linkage (byte-immutable), re-verifies the 008-d
evidence claims, registers the round in the ledger and machine block,
corrects the stale round-suffix reference in current status
documentation (blind hidden acceptance and the final objective-008
disposition are round 008-f), and publishes a validator-valid report.
It is bounded D0 protocol correction plus ledger bookkeeping. It is
not a test change, not a gate change, not a production change, not a
linguistic experiment, and it makes no model call.

## Provenance

- H: Human instruction 2026-09-18 (metadata provenance H): finish the
  currently active corrective work correctly; all four required checks
  genuinely green at the reviewed final head; no weakening/skipping/
  redefining any check; no manufactured green status, milestone,
  deployment, or linguistic acceptance; correct materially stale
  current-status documentation; classify unrelated inherited debt
  precisely and propose a separate bounded correction order rather than
  smuggling a fix in; keep the loop moving; the owner is not a terminal
  relay.
- A: S-REVIEW-01, S-RECOVER-01, S-MERGE-01, S-ORDER-02/03,
  S-EVIDENCE-01, the oap_core forward-recovery contract
  (prior_report_recovery schema v1 and the check_transcript
  recovery-linkage rule), the 007-e/007-d and 007-o/007-n quarantine
  precedents, the 004-d scoped generated-file pin precedent, the
  008-b/008-d ledger-registration pattern, P-SELF-03.
- E: The strategy-verified CI facts at the 008-d final head c0786f9 and
  the local reproduction of the report defect (metadata provenance E):
  REPORT_CHECK at local and remote verify_report; exactly three
  angle-bracket command spans (checks[5], checks[6], checks[8]);
  RECOVERY_LINKAGE_MISSING deterministic at the transcript stage;
  Research PASS (35381405131); report history PASS (35381405199);
  Application baseline attempt 1 red (zero-failure TIMEOUT class) and
  attempt 2 green on the identical commit (run 35381405077); the 008-c
  head's four verbatim zero-failure observations (337.20/335.98/334.01 s
  plus the 09-17 pool reference 134.92 s); frozen surfaces byte-
  identical; hidden seal 4091/4091.
- I: Strategy independent final-head reviews 008-d, 008-c, 008-b
  (private workorders/), and the committed 007-o order (recovery
  template).

## Current verified state

Verified by strategy at publication (this session, from remote and
primary records):

- main remains `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9` (development-
  only merge of PR #8); objective 007 closed.
- PR #9 OPEN / UNMERGED, MERGEABLE, auto-merge disabled, head
  c0786f9898d3a97aefe9d063bcd43210c0d7d2f1 (the 008-d final head).
- CI at c0786f9 (re-verified this session): Research reproducibility
  PASS; OAP report history PASS; Application baseline green via the
  identical-commit rerun (attempt 1 red, zero-failure TIMEOUT class);
  OAP bootstrap acceptance FAIL (deterministic transcript-coherence
  RECOVERY_LINKAGE_MISSING - the only red, and the only one this round
  is designed to clear).
- Protocol state: `oap/active` = 008-d; consumed.json = 008-d; the
  008-d response OK frame was received by strategy; the coding wrapper
  is alive and blocked on the control FIFO.
- The 008-d report and order are byte-immutable from this round forward
  (quarantined publication; classified, never rewritten).
- Local worktree at c0786f9 plus untracked residue only
  (`.research-test-scratch/`, possibly an untracked root `corpus/`
  residue, possibly an untracked `.venv`; none is ever committed).

## Governance

S-REVIEW-01, S-RECOVER-01, S-MERGE-01, S-ORDER-01/02/03,
S-EVIDENCE-01, S-DECIDE-01 (D0: bounded, reversible, inside the risk
budget). D0 overall: forward-recovery quarantine linkage plus
ledger/state bookkeeping and one sentence of documentation correction,
under an explicitly predeclared BLOCKED policy for the stochastic
application-baseline pool regime. No D1 is created in this round (the
suffix renumbering to 008-f is the execution of the renumbering
discipline already recorded in the 008-c/008-d records). No CRIT
admission: the five conditions fail at condition 1 - the OAP recovery
law and the 2026-09-18 human instruction resolve the substantive issue,
and the residual choices are reversible engineering mechanics.

## Goal and dependencies

Restore the OAP bootstrap acceptance required check to green at this
round's final head by the lawful forward-recovery quarantine of the
machine-invalid 008-d report (this order's prior_report_recovery
linkage; no report or order byte altered), re-verify the 008-d evidence
claims, register the round in the research ledger and machine block,
correct the stale 008-e/008-f suffix reference in current status
documentation (blind hidden acceptance is 008-f), and publish a
validator-valid 008-e report that additively records the 008-d
final-head CI truth. The other three required checks must be genuinely
green at this round's final head: Research reproducibility and OAP
report history by ordinary correctness; Application baseline under the
bounded zero-failure-TIMEOUT observation policy of 008-d (a green
rerun of the identical commit is the current check state and is
disclosed verbatim, never manufactured). If the frozen full-pytest stage
still exceeds the 300 s cap at this round's final head after the bounded
observation budget, the round reports BLOCKED with the verbatim
observations and stops; strategy then adjudicates before 008-f (a
separate bounded correction order for the inherited timing debt, or a
pool-recovery wait - decided after this round's evidence, not inside
it). No hidden-set evaluation occurs; that is 008-f.

Dependencies (all satisfied and verified): 008-a (frozen candidate and
baseline), 008-b (ledger pattern), 008-c (frozen implementation, sealed
hidden set), 008-d (the quarantined publication whose evidence this
round re-verifies). No other dependencies.

## Scope

1. Reconcile current state exactly (requirement 1).
2. Forward-recovery quarantine (requirement 2): this order's
   prior_report_recovery block (already fixed in the metadata above) is
   the entire quarantine mechanism; the coding agent must NOT edit,
   move, or re-commit the 008-d order or report, and must re-verify
   byte-for-byte that both are unchanged after its own commits
   (git show base vs HEAD over both paths).
3. Ledger and state bookkeeping (requirement 3):
   (a) add exactly one 008-e registry entry to
       `research/registry/experiments.json` (kind `audit`, following the
       008-d entry pattern) with: experiment_id
       `008-e-report-republication-and-transcript-recovery`; question
       "The 008-d report is machine-invalid (REPORT_CHECK: three
       checks[] command strings carry angle-bracket placeholder tokens);
       how is it quarantined by forward recovery, how is transcript
       coherence restored, and how is the round registered without
       weakening, skipping, or redefining any gate and without altering
       any report or order byte?"; frozen_choices recording
       new_model_calls = 0, new_science = 0, gate_or_test_changes = 0,
       cap_or_driver_or_workflow_changes = 0, report_or_order_mutations
       = 0, hidden_set_evaluations = 0; metrics from the actual
       committed observations (the quarantine identity fields; the
       008-d final-head CI facts: Research PASS 35381405131, report
       history PASS 35381405199, Application baseline attempt 1 red in
       the zero-failure TIMEOUT class and attempt 2 green on the
       identical commit 35381405077, OAP bootstrap FAIL
       RECOVERY_LINKAGE_MISSING deterministic; this round's final-head
       CI facts verbatim); evidence_files citing the committed
       008-d order blob (sha256 4e15638298f40b8871c2638371a2b5bfefa7d7df465d32eea6f1b907a9dfcbab),
       the committed 008-d report blob (content sha256
       6efbf90ee83e76997eb84985e3fe6f3498ba837a2998900094a0f4238c785a60,
       git blob 13effeaae9ec50ae9779d5ab0caa3c568a88362b), the 008-e
       order (committed at activation), and the 008-e-final-head
       RESEARCH-STATE.md and experiments.json blobs; public_report
       `research/RESEARCH-STATE.md#16`; public_metrics the registry
       entry; public_configuration none; source_manifest none;
       pending_evidence `["008-f: blind hidden-acceptance evaluation of
       the frozen implementation (PASS/CONDITIONAL/FAIL), naturalistic
       label adjudication per the frozen annotation guide, end-to-end
       preservation on the hidden set"]`.
   (b) update the RESEARCH-STATE.md machine block: registry_entries
       28 -> 29, oap_reports_reviewed 47 -> 48; frozen_report_history_
       incidents UNCHANGED at 2 (it re-derives from
       oap/REPORT-HISTORY-INCIDENTS.json, which this quarantine does
       not extend - the quarantine is order-linkage-based, exactly as
       for 007-d and 007-n); every existing identity field unchanged
       EXCEPT the addition of one new identity key `quarantined_008d`
       carrying exactly: classification INVALID_QUARANTINED,
       validation_error REPORT_CHECK, publication_commit
       c0786f9898d3a97aefe9d063bcd43210c0d7d2f1, report_path
       oap/reports/008-d-application-baseline-restoration.md,
       report_blob 13effeaae9ec50ae9779d5ab0caa3c568a88362b,
       report_sha256 6efbf90ee83e76997eb84985e3fe6f3498ba837a2998900094a0f4238c785a60,
       order_path oap/orders/008-d-application-baseline-
       restoration.md, order_sha256 4e15638298f40b8871c2638371a2b5bfefa7d7df465d32eea6f1b907a9dfcbab,
       implementation_parent 3baa4f3318f76ba5fc44260829f3f593832695bf.
       Add one short additive note in the current-rounds narrative
       recording: the 008-d report is machine-invalid (REPORT_CHECK;
       three checks[] commands with angle-bracket placeholder tokens;
       same defect class as the quarantined 007-n report), classified
       INVALID_QUARANTINED by the 008-e order's forward-recovery
       linkage; transcript coherence is restored at this round's final
       head; the 008-d final-head CI truth (three checks green,
       Application baseline via identical-commit green rerun of the
       zero-failure TIMEOUT class, OAP bootstrap red deterministic
       until this linkage); and the renumbering: blind hidden
       acceptance and the final objective-008 disposition are round
       008-f (the 008-d note's 'round 008-e' label carries the
       pre-recovery numbering; the deferral itself is unchanged).
   (c) correct STATUS.md: the objective-008 paragraph's sentence
       "deferred to round 008-e, with round 008-d recorded as the
       bounded application-baseline timing corrective" must read that
       the blind hidden acceptance and final objective-008 disposition
       are deferred to round 008-f, with round 008-d recorded as the
       bounded application-baseline timing corrective whose machine-
       invalid report is classified INVALID_QUARANTINED by the 008-e
       order's forward-recovery linkage. No other semantic change to
       STATUS.md. In the same commit, update the scoped
       oap/GENERATED-FILES.json STATUS.md pin (class/sha256/bytes) per
       the 004-d mechanism and verify the OAP scoped-inventory/drift
       checks pass locally.
   (d) regenerate `research/tables/experiment-summary.csv` with
       `python3 -B -m research.tools.rebuild_tables` and verify with
       `--check`.
4. Freeze verification (requirement 4): git diff base..HEAD empty over
   the frozen surfaces: `research/curated/`, `src/`,
   `research/prose-boundary/config/`, `research/prose-boundary/corpus/`
   (manifests included), `research/prose-boundary/results/` (all of
   increment1, increment2, increment3, baseline-timing),
   `research/prose-boundary/REPORT.md`, `research/prose-boundary/
   REPORT-008C.md`, `research/prose-boundary/adapter/`,
   `research/prose-boundary/identity/`, `research/prose-boundary/
   fixtures/`, all test files (including the 008-c focused file and
   test_research_state_consistency.py),
   `scripts/verify_development_baseline.py`, `.github/workflows/`, and -
   in addition to 008-d - the two 008-d publications themselves:
   `oap/orders/008-d-application-baseline-restoration.md` and
   `oap/reports/008-d-application-baseline-restoration.md` byte-
   identical.
5. Hidden-seal re-verification, data-free (requirement 5): re-hash the
   private-root hidden content against the committed
   `research/prose-boundary/corpus/manifests/hidden-manifest.json`
   (expect 4091/4091 verified; manifest sha256 still
   8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18);
   no hidden file content is read or echoed anywhere (counts/hashes
   only). Any mismatch: STOP and report BLOCKED (seal contract).
6. Local verification (requirement 6): full research suite with the
   pinned helper present (at the bookkeeping-complete implementation
   head the 007-o consistency test fails locally ONLY on the designed
   count assertion - machine block oap_reports_reviewed 48 vs 47 report
   files in the tree before the report commit; verify exactly that
   single assertion), the OAP suite (including B10, scoped inventory/
   drift, report history), publication guard, whitespace check, and one
   full local Application-baseline driver run (per-stage durations
   recorded; local wall time is local evidence only, never a CI
   observation).
7. Implementation head, push, and CI (requirement 7): commit the
   bookkeeping, push; observe CI at the implementation head and record
   it verbatim. Expected red state (the 008-b/008-c/008-d designed
   precedent): the single designed pre-report count assertion failing
   in Research reproducibility and in the Application baseline
   full-pytest; on a slow pool the full-pytest stage may additionally
   record TIMEOUT at the 300 s cap with the session showing exactly
   that one designed failure. NO rerun is performed at the
   implementation head: a green is impossible by design before the
   report-only commit. Any additional genuine test failure beyond the
   single designed count assertion is a STOP/BLOCKED event with the
   failing test named (not pool variance).
8. Report-only final commit (requirement 8): one commit with the
   literal implementation head as sole parent and
   `oap/reports/008-e-report-republication-and-transcript-recovery.md`
   as the sole changed path; push; verify remote PR head, exact report
   bytes, parent, and changed-path invariant. BEFORE this push the
   report must pass the pre-push validity gate (requirement 9).
9. Pre-push report validity gate (requirement 9 - new, the 008-d
   lesson): with the report file written locally and the worktree at
   the bookkeeping-complete state, (a) scan the full draft report text
   for the meaningful() rejection patterns - any angle-bracket span
   matching the regex of oap_core meaningful() and any standalone
   VERIFY/TBD/TODO/UNRESOLVED token - in EVERY checks[] command string
   (and in no other field may an angle-bracket span appear where a
   literal value is recorded); any hit is fixed in the draft before
   commit; (b) run `python3 oap/bin/verify_report.py --id 008-e` in a
   temporary worktree containing the report-only commit (or equivalently
   with the report committed locally before push, per the round's
   git mechanics) and it MUST return result verified with no
   REPORT_CHECK; (c) run
   `python3 oap/bin/check_transcript.py --revision HEAD --expected-id
   008-e` in the same state and it MUST pass (the 008-d report now has
   its unique recovery linkage and the 008-e report is valid) - this
   local proof is the exact gate the red CI stage runs; (d) record all
   three command outputs verbatim in the report evidence and in the
   private review receipt. If (b) or (c) fails, the report is NOT
   pushed; the defect class is diagnosed and the draft corrected
   (in-round correction of the 008-e report itself is permitted before
   its report-only push; after the push the 008-d legal posture applies
   and a further suffix would be required).
10. Final-head CI (requirement 10): all four required checks green at
    the final head. OAP bootstrap acceptance is expected GREEN (the
    purpose of this round); if it is red for any reason, record the
    exact stage and error verbatim and report BLOCKED - no gate
    change. If the Application baseline full-pytest stage at the final
    head records TIMEOUT at the 300 s cap with ZERO test failures (the
    pool-variance failure class), apply the bounded rerun observation
    (up to 3 additional observations at the identical final head, each
    recorded verbatim with session summary and wall time); a green
    rerun of the identical commit is the current check state (GitHub
    required-check semantics track the latest run) and is disclosed
    verbatim in the report - an honest observation of a stochastic
    runner pool, never a manufactured or weakened check. If the stage
    is still red after the observation budget: publish the report with
    `Result: BLOCKED`, the verbatim observations, and the explicit
    predeclared stop - do not chase further reruns, do not change any
    gate; strategy adjudicates before 008-f (a separate bounded
    correction order for the inherited debt, or a pool-recovery wait).
    Any full-pytest failure showing a genuine test failure (a nonzero
    failure count other than the designed pre-report count assertion at
    the implementation head) is a DIFFERENT failure class: STOP,
    preserve evidence, report BLOCKED with the failing test named.
    After final-head CI settles, re-verify the remote PR head still
    equals the report-only commit (a changed head voids the review).

## Non-goals

- No change to the 300 s per-command cap, the baseline driver
  (`scripts/verify_development_baseline.py`), any workflow file, any
  oap/bin script, or any other gate definition.
- No change to any test file (no edits, no additions, no skips, no
  deletions); the full-pytest population is identical to the 008-d
  final head.
- No change to the 008-d order or report bytes (quarantined
  publication), to any earlier order or report, to `research/curated/`,
  `src/`, the 008-c implementation, the 008-a baseline, the committed
  corpus, configs, or the hidden manifest; no hidden-set evaluation or
  regeneration (008-f's scope).
- No 007-m linguistic change (detector, ranking, candidate semantics,
  validator prompt/parser, acceptance, reasoning settings); no
  linguistic benchmark artifact change.
- No model calls of any kind (the 008-c generation program is complete;
  its 414 disclosed attempts are closed); no new data acquisition.
- No objective-009 data of any kind; 009 remains reserved.
- No merge, no auto-merge, no force-push, no rewrite of any immutable
  order or report.
- No fix of the inherited application-suite performance debt in this
  round: it remains classified precisely by the 008-d committed
  decomposition, and any correction is a separate bounded order
  proposed after this round's evidence.
- No CRITICAL append or mitigation update.

## Files and boundaries

Inspect (read-only): `oap/orders/008-d-application-baseline-
restoration.md` and `oap/reports/008-d-application-baseline-
restoration.md` (quarantined immutable references);
`oap/orders/007-o-consolidate-research-state.md` (recovery template
reference); `oap/bin/oap_core.py` (meaningful(), validate_report,
check_transcript, forward-recovery contract - frozen, read-only);
`scripts/verify_development_baseline.py` (frozen driver contract);
`.github/workflows/*.yml` (frozen); `research/tests/*` (frozen);
`research/prose-boundary/corpus/manifests/hidden-manifest.json` (seal
reference); `research/RESEARCH-STATE.md`,
`research/registry/experiments.json`,
`research/tables/experiment-summary.csv`, `STATUS.md`,
`oap/GENERATED-FILES.json`, `oap/REPORT-HISTORY-INCIDENTS.json`
(bookkeeping targets / references); private
`workorders/008-d-final-head-review-20260918.md` (review basis);
`/home/ubuntu/.local/share/llm-slovenian-repair/008d-handoff/` (agent
root-cause handoff: minimal-fix.txt, isolated-verify-proof.json,
verify-local-failure.txt, verify-remote-failure.txt - private, never
committed); `workorders/consumed.json` and the FIFO state
(reconciliation).

Modify (only these): `oap/orders/008-e-report-republication-and-
transcript-recovery.md` (new, activation commit); `oap/active` (->
008-e); `research/registry/experiments.json` (append exactly one 008-e
entry); `research/RESEARCH-STATE.md` (machine block 28->29 and 47->48,
the new quarantined_008d identity key, plus the one additive note);
`STATUS.md` (the one sentence correction); `oap/GENERATED-FILES.json`
(the STATUS.md pin entry only);
`research/tables/experiment-summary.csv` (rebuild_tables output);
`oap/reports/008-e-report-republication-and-transcript-recovery.md`
(new, report-only commit).

## Requirements

1. Reconcile: `oap/active` = 008-e after activation; remote branch head
   == c0786f9898d3a97aefe9d063bcd43210c0d7d2f1 before any push; PR #9
   open/unmerged with auto-merge disabled; local worktree at c0786f9
   plus untracked residue only; verify the frozen surfaces of scope
   item 4 are byte-identical to base (git diff empty) BEFORE any
   commit; no other concurrent mutation.
2. Quarantine linkage: the order's prior_report_recovery block is the
   one carried by the published order (it is fixed in the metadata
   above; the agent publishes the order as-is and never rewrites it);
   after the agent's own commits, re-verify that the 008-d order and
   report blobs at HEAD equal their blobs at base (git rev-parse
   both paths at base and HEAD; identical).
3. Bookkeeping exactly per scope item 3 (a)-(d): one 008-e registry
   entry (byte-stable JSON, chronological position after the 008-d
   entry); machine block registry_entries 28 -> 29 and
   oap_reports_reviewed 47 -> 48, frozen_report_history_incidents
   unchanged at 2, the new quarantined_008d identity key exactly per
   scope item 3(b), every other identity field unchanged; the one
   additive RESEARCH-STATE note; the one STATUS.md sentence correction
   with the scoped pin updated in the same commit (OAP scoped-
   inventory/drift checks green locally); CSV is the byte-identical
   rebuild_tables output (--check passes).
4. Freeze verification after the bookkeeping commit and again before
   the report-only commit: git diff base..HEAD empty over every frozen
   surface in scope item 4, including the two 008-d publication files;
   the two frozen report-history incidents intact (report history
   check green locally).
5. Hidden-seal re-verification data-free per scope item 5
   (4091/4091; manifest sha256 unchanged; zero hidden content reads;
   any mismatch STOP/BLOCKED).
6. Local verification per scope item 6 (research suite with the
   designed single-assertion red state at the implementation head; OAP
   suite green including B10; publication guard PASS; whitespace PASS;
   one full local driver run with per-stage durations).
7. Implementation head, push, CI per scope item 7 (designed single
   assertion red in Research and full-pytest; no rerun at the
   implementation head; any other genuine failure STOP/BLOCKED).
8. Report-only commit per scope item 8 and the pre-push validity gate
   per scope item 9 (draft scan; verify_report --id 008-e = verified;
   check_transcript --revision HEAD --expected-id 008-e = pass; all
   outputs recorded verbatim). The report contains every mandatory
   field (Result; order identity/hash; PR mode/number/URL/state;
   branch/base and starting remote SHA; implementation head SHA;
   publication commit SELF; per-criterion evidence; each command/check
   with PASSED/FAILED/TIMEOUT/PENDING/NOT RUN and tested SHA - every
   sha a full 40-hex observed commit, every command string free of the
   meaningful() rejection patterns; negative-path evidence; setup/
   resource/privacy evidence; Critical action NONE; limitations; no-
   merge confirmation) and the documentation-section content;
   `publication_verified: false` before its own push per P-SELF-03.
   The report additively records: the 008-d root cause (three named
   checks[] commands, the meaningful() mechanism, the 007-n precedent);
   the quarantine (identity fields, byte-immutability proof); the
   008-d final-head CI truth (including the verbatim session summary
   of the green identical-commit rerun of run 35381405077, captured by
   the agent this round, and the deterministic OAP-bootstrap red with
   the exact error); the 008-f renumbering; and this round's final-
   head CI facts.
9. Final-head CI per scope item 10 (all four green at the final head,
   with the bounded verbatim rerun observation for the zero-failure
   TIMEOUT class; predeclared BLOCKED stop after the budget; any
   genuine test failure is a STOP/BLOCKED with the failing test named;
   OAP bootstrap acceptance expected green - the round's purpose - and
   any red is recorded verbatim and BLOCKED).
10. Send exact response OK after remote verification and stop. PR #9
    remains open and unmerged.

## Acceptance criteria

1. At the final head, either: all four required checks green (with
   every rerun observation disclosed verbatim) - the success state; or
   Result: BLOCKED with the verbatim observations and the predeclared
   stop - the permitted failure state. No third state is acceptable.
2. git diff base..final empty over every frozen surface of scope item 4
   (no test, gate, driver, workflow, implementation, corpus, config,
   manifest, 008-a baseline, or 008-d publication change).
3. Registry holds exactly 29 entries; the 008-e entry follows the
   008-d pattern (kind audit; evidence files' sha256/blobs matching
   committed bytes; pending_evidence naming 008-f); machine block
   registry_entries = 29, oap_reports_reviewed = 48,
   frozen_report_history_incidents = 2, quarantined_008d identity
   exactly per scope item 3(b), every other field unchanged; CSV
   byte-identical rebuild output; the 007-o consistency test green at
   the final head.
4. Report-only commit invariants verified remotely (parent = literal
   implementation head; sole changed path = the 008-e report; exact
   bytes); verify_report remote=verified at the final head (no
   REPORT_CHECK - the 008-d defect class must not recur).
5. check_transcript --revision HEAD --expected-id 008-e passes
   locally at the report-only state (pre-push) and the OAP bootstrap
   acceptance check is green at the final head.
6. STATUS.md carries exactly the one sentence correction (008-f
   suffix truth plus the quarantine clause); the scoped
   GENERATED-FILES.json STATUS.md pin updated in the same commit; OAP
   scoped-inventory/drift checks green.
7. Hidden seal re-verified data-free (4091/4091; manifest sha256
   8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18
   unchanged; zero content reads).
8. Zero model calls, zero hidden-set evaluations, zero linguistic
   changes, zero 009-data touches (the report records each as a
   negative-path evidence item).

## Verification

- Focused: the 007-o consistency test (machine-block re-derivation;
  green at the final head, exactly-one-assertion red at the
  implementation head), the OAP B10 inventory-link and scoped
  inventory/drift tests, check_report_history (locally and via CI),
  verify_report (local pre-push and remote at the final head),
  check_transcript (local pre-push and via the OAP bootstrap CI
  stage), the hidden-seal manifest re-hash (data-free), the
  rebuild_tables --check.
- Broader: full research suite with the pinned helper (280+ tests),
  the OAP suite, one full local Application-baseline driver run
  (per-stage durations), the full CI battery at the implementation
  head and the final head.

## Local setup and constraints

- CPU-only local verification plus the single local driver run; the
  pinned Rust helper and the frozen uv environment as in 008-c/008-d;
  the private research-runtime tree for the hidden-seal re-hash
  (hashes only, no content reads).
- No new dependencies, no environment changes, no service touches, no
  GPU, no network beyond the authorized GitHub API and the local
  GitHub runner semantics.
- Privacy: no private text, paths, or hidden content in the report or
  any committed artifact; the 008d-handoff files remain private.

## Documentation

- RESEARCH-STATE.md: the one additive note (scope item 3(b)) - the
  008-d report quarantine, the restored transcript coherence, the
  008-d final-head CI truth, the 008-f renumbering; the machine block
  update; the existing 008-c and 008-d records remain untouched.
- STATUS.md: the one sentence correction (scope item 3(c)); the
  objective-008 paragraph otherwise unchanged, preserving the
  structural-safety-not-linguistic-quality distinction and the
  no-acceptance/no-merge/no-release wording.
- The 008-e OAP report: the full evidence record (scope item 8/9).
- No other documentation change; no rewrite of any historical report
  or of EXPERIMENT-HISTORY.md.

## Git and report publication

- Activation commit: the order file plus `oap/active` -> 008-e
  (publish_order.py atomic publish; dry-run twice before the real
  publish; the accepted-ref is the current main
  7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9).
- Bookkeeping commit per scope item 3 (single commit).
- Report-only commit per scope item 8 (sole parent = literal
  implementation head; sole changed path = the 008-e report).
- Push semantics per the OAP communication profile; no force-push; no
  push after the report-only commit (C-REPORT-01); the exact response
  OK after remote verification.

## Decision classification

D0. Bounded, reversible protocol correction inside the risk budget:
a forward-recovery quarantine linkage mandated by the OAP recovery
law, ledger/state bookkeeping following the 008-b/008-d pattern, one
sentence of stale-reference correction, and an honest bounded
observation policy for the stochastic application-baseline pool
regime. No D1 is created (the 008-f renumbering executes the recorded
renumbering discipline). No CRIT admission (five conditions fail at
condition 1).

## Deferred human adjudication

- Decision: NONE

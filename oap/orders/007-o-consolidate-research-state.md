# Work order 007-o — Quarantine the machine-invalid 007-n report and consolidate the current research state

Status: FINAL

Finalized by strategic reconciliation of 2026-09-17: 007-n final-head review
(private `workorders/007-n-final-head-review-20260917.md`), root-cause proof of the
red OAP bootstrap acceptance check, and the owner's 2026-09-17 research-sequencing
decision. The 2026-09-17 prepublication review
(private `workorders/007-o-prepublication-review.md`) is the analysis baseline.

```oap-metadata
{
  "id": "007-o",
  "title": "Quarantine the machine-invalid 007-n report and consolidate the current research state",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": ["007"],
  "local_work": "Preserve every 003-007 product seam, all research/ projections and registries, all private experiment roots (007-i/j/m roots under the owner-selected research-runtime tree; preservation archive in the strategic workspace), the 007-m no-resample state, all prior orders/reports byte-for-byte (including the machine-invalid 007-n report, which is classified, never rewritten), and any unrelated local work.",
  "prior_review": "Strategic final-head review of 007-n (2026-09-17, private workorders/007-n-final-head-review-20260917.md): remotely verified report commit 735c9830db95cbb02fc80446b6d28f62a56f10c9 (sole parent b61f8e2e6b454a0969e5f2ac9009d4da87b8b215, report-only changed path), reviewed the implementation diff, reran the focused concept suite (19/19) and 25/25 consecutive iterations of the formerly flaky terminal-SSE test locally, and recorded final-head CI: Application baseline PASS, Research reproducibility PASS, OAP report history PASS, OAP bootstrap acceptance FAIL with RECOVERY_LINKAGE_MISSING because the 007-n report is machine-invalid (its checks[5].command carries an unfinalized placeholder token, so validate_report rejects the report with REPORT_CHECK and no later order carried the required prior_report_recovery linkage). The 007-n implementation is accepted; the 007-n report is byte-immutable and is classified INVALID_QUARANTINED by the prior_report_recovery block of this order; its evidence claims are re-verified by this round. The 2026-09-17 prepublication review independently reconstructed research truth (registry, configs, results projections, private root identities, OAP reports, PLAN/ARCHITECTURE, CI) and is the analysis baseline for this order.",
  "prior_report_recovery": {
    "schema_version": 1,
    "classification": "INVALID_QUARANTINED",
    "prior_id": "007-n",
    "corrective_id": "007-o",
    "repository": "ulfe-lmi/llm-slovenian-repair",
    "pr": 8,
    "branch": "oap/007-concept-verification",
    "report_path": "oap/reports/007-n-restore-deterministic-application-baseline.md",
    "publication_commit": "735c9830db95cbb02fc80446b6d28f62a56f10c9",
    "report_blob": "2b74413b54faf65de7659d3cf9957271d7721573",
    "report_sha256": "a0bf18f8b0e1218104f3fa4951be62758a3f4f5e88e7d776c4abe3d596b8372a",
    "implementation_parent": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215",
    "order_path": "oap/orders/007-n-restore-deterministic-application-baseline.md",
    "order_sha256": "0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82",
    "validation_error": "REPORT_CHECK",
    "reason": "The 007-n report checks[5].command records an unfinalized placeholder token (the angle-bracket-wrapped phrase owned native temp dir) where the literal native temp parent directory must have been recorded; validate_report therefore rejects the whole report with REPORT_CHECK while every other recorded check and identity field is valid. The defect is formal, not scientific: the 007-n implementation was independently accepted by strategy on 2026-09-17. The unique resolution is the forward-recovery quarantine by this exact next order on the same objective, branch and PR; no report byte is altered and the 007-n evidence claims are re-verified in this 007-o round.",
    "authority": "Owner instruction 2026-09-17: resolve the current OAP bootstrap acceptance failure according to existing OAP recovery law, without weakening any gate and without manufacturing green status. OAP communication profile section 7: a correction after the final report uses a new strategic corrective suffix on the same PR, not an amended historical report. Precedent: the 007-d report was quarantined by the 007-e order with the same protocol block.",
    "evidence_scope": "Provenance and frozen publication identity only. Not acceptance of the 007-n report, not evidence that its checks passed, not milestone clearance, not merge authority."
  },
  "provenance": [
    {"kind": "H", "reference": "Owner instruction 2026-09-17 (research-state consolidation): deliverable list, prohibitions, PR-disposition questions, and the directive to resolve the current OAP failure per existing recovery law without weakening gates. Owner instruction 2026-09-17 (research sequencing): protection research precedes linguistic confirmation - finish/reconcile 007 and PR #8; objective 008 researches, qualifies and, if justified, implements the prose/non-prose structural boundary (human-supplied Deep Research report 'Reliable Prose Segmentation in Mixed LLM Output' supplies the candidate space, pulldown-cmark 0.13.4 as leading candidate); freeze the resulting effective pipeline; objective 009 runs the fresh untouched human-labelled target-distribution linguistic confirmation. Objective-009 confirmation data must not be used during 008 and 007-m linguistic behaviour must not be tuned during 008."},
    {"kind": "A", "reference": "PLAN.md v1.0 sections 14-16 (linguistic evaluation requirements, D01-D07/M01-M07/S01-S05, MVP criteria); ARCHITECTURE.md v1.1 section 16 (evidence layers); S-ICA-01/02, S-ORDER-01/02/03, S-EVIDENCE-01, S-REVIEW-01, S-RECOVER-01; OAP communication profile sections 5-7 (finalized work-order contract, atomic publication, forward report recovery); oap_core.py forward-recovery protocol (precedent 007-d/007-e)."},
    {"kind": "E", "reference": "Verified 2026-09-17 at PR #8 head 735c9830db95cbb02fc80446b6d28f62a56f10c9: OAP bootstrap acceptance FAIL (check_transcript RECOVERY_LINKAGE_MISSING, job log of GitHub run 35171822181); root cause is the 007-n report checks[5].command placeholder making the report machine-invalid (REPORT_CHECK), independently reproduced by strategy; Application baseline, Research reproducibility and OAP report history PASS at the same head; no RESEARCH-STATE document exists; STATUS.md stops at 006-l and claims linguistic evaluation not run; PR #8 is 284 files, +66,792/-78 with stale Application-baseline wording."},
    {"kind": "I", "reference": "Strategic prepublication review 2026-09-17 (private workorders/007-o-prepublication-review.md: full experiment ledger, overfitting audit, PLAN matrix, deployment resolution, claims audit, next-experiment design) and strategic 007-n final-head review (private workorders/007-n-final-head-review-20260917.md); coding incident receipt logs/007-n-coding-incident-20260917.md (independent corroboration of the same root cause and identities)."}
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

Corrective/closure round 007-o amends objective 007 on branch
`oap/007-concept-verification` and PR #8 (AMEND_EXISTING_PR). It creates no new PR,
performs no scientific experiment, and makes two coordinated things true:

1. The transcript is coherent again because the machine-invalid 007-n report is
   classified INVALID_QUARANTINED through this order's canonical
   `prior_report_recovery` block (the protocol's designed path; precedent
   007-d/007-e). No gate is weakened and no report byte is rewritten.
2. Objective 007 reaches a reviewable closure point: one current authoritative
   document (`research/RESEARCH-STATE.md`) answers, for an independent reviewer,
   what was investigated, what ran, what is trustworthy, what failed or was
   superseded, what is the strongest frozen method, what is and is not
   demonstrated, what remains worth testing, and what must not be tuned further.

## Provenance

Owner-directed consolidation and sequencing decision (H), implementing PLAN
sections 14-16 and the architecture evidence-layer law (A), driven by observed
state (E): the 007-n report is machine-invalid and quarantined; no single current
research-state document exists; STATUS.md is stale; the PR #8 description carries
stale Application-baseline wording; the 007-m frozen report itself recommends
freezing the design and testing fresh evidence. The two private strategic
reviews (I) of 2026-09-17 are the verified analysis baselines; their
machine-checkable numbers must be re-derived by this round from primary records.

## Current verified state

Remote `main` = ee2d1b479719009ff1d07829478f241e3f395f7c, equal to the runtime
accepted reference. Branch `oap/007-concept-verification` and PR #8 head =
735c9830db95cbb02fc80446b6d28f62a56f10c9 ("Publish 007-n OAP report", sole parent
b61f8e2e6b454a0969e5f2ac9009d4da87b8b215, the 007-n implementation head). PR #8 is
OPEN, MERGEABLE, UNSTABLE solely through one red check; 284 files, +66,792/-78;
base main; auto-merge disabled. `oap/active` = 007-n; worktree clean. Final-head
CI at 735c983: Application baseline PASS, Research reproducibility PASS, OAP
report history PASS, OAP bootstrap acceptance FAIL - `check_transcript.py
--revision HEAD --expected-id 007-n` exits 2 with RECOVERY_LINKAGE_MISSING. Root
cause independently established by strategy: the 007-n report checks[5].command
records an unfinalized placeholder token where the literal native temp parent
directory must have been recorded, so validate_report rejects the report with
REPORT_CHECK and the transcript requires the prior_report_recovery linkage that
this order carries. The 007-n implementation is independently accepted (private
receipt: diff review, 19/19 focused tests, 25/25 stability iterations); the
007-n report is byte-immutable and is classified INVALID_QUARANTINED by this
order, with its evidence claims re-verified in this round. PLAN, ARCHITECTURE and
CRITICAL hashes match the governance block; the CRITICAL register is the empty
seed; no human adjudication gate is open. All facts were re-verified by strategy
on 2026-09-17 before finalization.

## Governance

S-AUTH-01/02, S-STATE-01, S-ORDER-01/02/03, S-EVIDENCE-01, S-REVIEW-01,
S-RECOVER-01, S-ICA-01/02 govern. LR-014 requires the document to keep code
correctness, model compatibility, linguistic benefit, and deployment/release
authority as separate evidence layers; LR-008 preserves EXACT/CENSORED/UNAVAILABLE
semantics in all restated numbers; LR-013 constrains everything published.
D0 documentation/evidence reconciliation; the quarantine follows the protocol's
defined forward-recovery path (no new judgment debt); no live-test, milestone,
merge, release, or deployment authority is granted by this order.

## Goal and dependencies

Restore transcript coherence by classifying the machine-invalid 007-n report as
INVALID_QUARANTINED through this order's forward-recovery linkage, and publish
`research/RESEARCH-STATE.md` as the single authoritative CURRENT research state
(snapshot, not history), make `research/README.md` point to it as START HERE,
correct the factually stale parts of `STATUS.md`, update the PR #8 description,
and add a focused consistency test binding the document's machine-readable
numbers to primary records. The document records the owner's 2026-09-17
sequencing decision: the 007-m linguistic method remains FROZEN; the
prose/non-prose structural boundary (new numeric objective 008, new PR after the
007 closure) is the next research uncertainty; fresh human-labelled linguistic
confirmation (objective 009) is reserved until the effective pipeline is frozen
after 008. Depends on objective 007; this round is the 007 closure.

## Scope

- Create `research/RESEARCH-STATE.md` (data-free, public-safe) containing, in
  this order: (1) scope and exact reviewed Git identities (main, branch head, PR,
  checked SHAs of registry/configs/results used, the quarantined 007-n report and
  its classification); (2) executive scientific conclusion; (3) current frozen
  candidate method with exact 007-m identity (config SHA-256
  0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, predeclared
  lexicographic ranking tuple, prompt SHA-256
  572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, validator
  protocol, 300 s/2 MB/no-resample limits, deployment class A100-FP8
  qwen3.8-27b); (4) full experiment ledger - every root in
  `research/registry/experiments.json` (24 entries) plus OAP rounds 007-a
  through 007-n and every corrective/recovery round that affects interpretation
  (007-b replacement, 007-b timeout300, 007-d quarantined report, 007-h
  publication recovery, 007-i aggregation recovery, 007-j same-id recovery,
  007-m failed roots ffdf13/090ea8/e6ca66 and zero-call final root ec2962, 007-n
  accepted implementation with quarantined report) - each with: question,
  variable changed, parent/baseline, population and denominator,
  deployment/runtime, evidence class (synthetic/benchmark/genuine target-model
  output/preservation), evidence role (tuning/same-sample/held-out/confirmatory),
  call accounting (new/reused/zero-call projection), completion state,
  operational failures and uncertain deliveries, primary metrics with exact
  denominators, preservation metrics, what the result supports, what it does NOT
  support, limitations, relationship to later rounds, decision-relevance now;
  (5) key metric progression tables - official scorer (M0-M3 per dataset, from
  `research/results/strategic-official-summary.json` with scorer-file SHAs) and
  custom token-coordinate alignment (baseline 604/193/911 -> 007-h 704/345/811
  -> 007-i 727/172/788 -> 007-j 822/154/693 -> 007-m HYBRID 799/114/716, with
  exact denominators 1,515/1,440/75 gold units and the precision/recall/F0.5
  values, plus the exact 007-m-vs-007-j deltas and preservation/call/latency
  deltas); (6) evidence hierarchy explicitly separating merged-main, unmerged
  application development, experimental research, historical/replay, live model,
  reference-based scoring, human semantic (ABSENT for the external campaign),
  operational, and milestone/ICA (ABSENT) and release/deployment (ABSENT)
  layers; (7) claims audit of PR #8 description, STATUS.md, research/README.md,
  research/EXPERIMENT-HISTORY.md, latest OAP reports, latest research reports
  (VERIFIED/PARTIALLY VERIFIED/UNVERIFIED/STALE/CONTRADICTED with exact
  corrections), including the 007-n report itself (machine-invalid,
  quarantined; its check claims re-verified by this round, not cited as
  accepted transcript evidence); (8) PLAN matrix - D01-D07, M01-M07, S01-S05
  and all eight section-16 criteria, each exactly IMPLEMENTED AND VERIFIED /
  PARTIAL / ABSENT / UNPROVEN with repository evidence, limitations,
  unmerged-PR-only flag, fresh-evidence-required flag, and remaining human or
  deployment gates (use the 2026-09-17 strategic classification, re-verified);
  (9) deployment-validity matrix - PLAN target (strongly quantized Qwen3.8-27B
  on RTX 3090) vs evaluated regime (A100-FP8 qwen3.8-27b), RTX-3090 endpoint
  offline at reconnaissance, Deployment B excluded by owner override, no
  attributable human target change found; record the mismatch as an open
  evidence gap with the two human-decision resolutions; (10) open research
  questions vs completed questions; (11) research-debt matrix (what is missing
  to decide experimental-MVP); (12) updated research sequencing per the
  owner's 2026-09-17 decision - the 007-m design is frozen for confirmation;
  the next research objective (008, new numeric objective and new PR after the
  007 closure) is the qualification of the prose/non-prose structural boundary
  (research question: does pulldown-cmark 0.13.4 provide sufficiently accurate,
  conservative and source-faithful structural segmentation of actual
  LLM-generated Markdown-like output to replace the Markdown-sensitive part of
  the current hand-written protection logic; candidate supplied by the
  human-commissioned Deep Research report 'Reliable Prose Segmentation in Mixed
  LLM Output'; falsification-first; no production integration; no model calls),
  design summary only, explicitly NOT executed in this round; (13) objective
  009 reserved - fresh untouched human-labelled target-distribution linguistic
  confirmation of the complete effective pipeline, to be designed after 008
  freezes the pipeline; 009 confirmation data must not be used during 008 and
  007-m linguistic behaviour must not be tuned during 008; (14) explicit
  boundary: no further tuning of the 007-m candidate rule, ranking, prompt,
  thresholds, validator, or retry policy on DASSLE or any already-inspected
  benchmark before fresh evidence; and (15) explicit merge/release/deployment
  limitations (PR #8 disposition, development-merge conditions, no milestone
  label, no ICA launched, no deployment).
- Update `research/README.md`: START HERE pointer naming RESEARCH-STATE.md as
  the current authoritative research state; state explicitly that
  EXPERIMENT-HISTORY.md is a 007-d-era archival snapshot (historical synthesis,
  superseded as current state, not to be read as moving status).
- Correct `STATUS.md`: replace the stale blanket "linguistic evaluation NOT
  RUN" with the layered truth (reference-based benchmark linguistic evaluation
  HAS run - full-campaign8 and 007-h/i/j/m on A100-FP8, same-sample
  exploratory; human-labelled target-distribution evaluation per PLAN section
  14.2 NOT RUN; product detection/review/acceptance/patching remain PLANNED as
  before); add a 007 progress note (007-a..007-n on PR #8, open/unmerged,
  research-state document published, 007-n report quarantined). Preserve the
  existing 001-006 history paragraphs verbatim.
- Update the PR #8 description body to the current round: 007-o closure,
  pointer to research/RESEARCH-STATE.md, truthful current Application-baseline
  status, open/unmerged, no acceptance claims.
- Add one focused consistency test (e.g.
  `research/tests/test_research_state_consistency.py`) that re-derives the
  machine-readable numbers from primary records (`research/registry/
  experiments.json`, `research/results/strategic-official-summary.json`,
  `research/results/*.json.gz` projections, `research/reports/*.md` frozen
  values, and the reviewed Git identities embedded in the document) and asserts
  equality against a small machine-readable block embedded in RESEARCH-STATE.md
  (a fenced JSON block keyed by stable metric IDs). CPU-only, offline, zero
  network/model calls.

## Non-goals

No new scientific model calls; no new data acquisition or downloads; no prompt,
threshold, ranking, candidate-rule, validator, or retry-policy change; no
change to any research semantic, configuration, result, report, registry entry,
or private root; no production integration or adapter work; no objective-008
work of any kind (no parser installation, no fixture creation, no wrapper, no
challenger comparison); no Qwen/vLLM/CUDA/GPU/service/network changes; no
release or deployment activity; no merge or auto-merge of PR #8; no rewriting,
mutation, or replacement of any prior order or report, including the
machine-invalid 007-n report (it is classified, never rewritten); no change to
`oap/REPORT-HISTORY-INCIDENTS.json` (a quarantine is not a history incident;
the manifest must remain exactly the two frozen incidents); no application-
baseline fix beyond reporting it (007-n owns the repair; if it is red at the
007-o head for a new reason, report truthfully and stop for a separate
strategic correction order); no CRITICAL append; no ICA launch.

## Files and boundaries

Read/inspect (verification against primary evidence): `research/registry/
experiments.json`, `research/registry/source-manifest.json`, `research/registry/
file-census.json(.gz)`, `research/registry/archive-catalog.json`, `research/
reports/*.md`, `research/configs/*.json`, `research/results/
strategic-official-summary.json`, `research/results/*.json.gz`, `research/
tables/experiment-summary.csv`, `research/README.md`, `research/
EXPERIMENT-HISTORY.md`, `oap/orders/*.md` and `oap/reports/*.md` (006/007
series), `PLAN.md` sections 14-16, `ARCHITECTURE.md` sections 16 and 2,
`STATUS.md`, `README.md`, `.github/workflows/*.yml`, `oap/bin/oap_core.py`
(forward-recovery semantics), and (identity verification ONLY, SHA-256 of root
manifests, no content copying, no publishing private paths or text) the private
007-i/j/m experiment roots. Write: `research/RESEARCH-STATE.md` (new),
`research/README.md`, `STATUS.md`, the new consistency test, the exact 007-o
order/active/report paths, and the PR #8 description via the normal publication
flow. No other file may change.

## Requirements

1. Reconcile exact active 007-o, remote main (must equal
   ee2d1b479719009ff1d07829478f241e3f395f7c), branch/PR #8 head (must equal
   735c9830db95cbb02fc80446b6d28f62a56f10c9 or a verified continuation), the
   007-n order/report bytes (sha256 and blob exactly as recorded in this
   order's prior_report_recovery block), and all local work before mutation.
   Reuse PR #8. If any identity conflicts, stop mutation and report.
2. The committed 007-o order must match the published order byte-for-byte
   (sha256 verified before commit); the transcript at the implementation head
   must classify 007-n as INVALID_QUARANTINED with the 007-d quarantine
   preserved.
3. Re-derive every number used in RESEARCH-STATE.md from the primary records
   named in Scope (registry, results projections, official summary, frozen
   research reports, OAP orders/reports, git identities). If a number in the
   strategic prepublication baseline does not match a primary record, stop and
   report the discrepancy; do not silently choose a value.
4. Produce RESEARCH-STATE.md with all fifteen Scope sections, data-free,
   public-safe, with exact denominators and the official-vs-custom scorer
   distinction; state explicitly that no human semantic labels exist for the
   external campaign and that non-reference edits are not labeled harmful;
   record the 007-n quarantine classification and root cause, and the updated
   008/009 sequencing with its two prohibitions (no 009 data in 008; no 007-m
   tuning in 008).
5. Produce the embedded machine-readable numbers block and the focused
   consistency test; the test must FAIL if any embedded number is altered
   (negative proof) and PASS at the implementation head (positive proof).
6. Update research/README.md (START HERE plus archival note for
   EXPERIMENT-HISTORY.md), STATUS.md (layered correction, 001-006 paragraphs
   preserved verbatim), and the PR #8 description.
7. Verify private-root identities (manifest SHA-256) only where the document
   cites root identities; no private content, paths, prompts, or response bytes
   in any public artifact.
8. Run the focused consistency test, the full research test suite,
   `research.tools.rebuild_tables --check`, and the publication guard over the
   updated tree (guard allowlist updated for RESEARCH-STATE.md and the new test
   only if required).
9. Run the real `scripts/verify_development_baseline.py` entry point; the
   Application baseline must be GREEN at the 007-o head (inherited from 007-n).
   The report records the command with the literal temp parent path actually
   used - placeholder tokens are forbidden. If it is red for a new reason, stop
   and report the exact failing stage truthfully; do not weaken, skip, or
   redefine the check, and do not publish a green claim.
10. Run the OAP suite, transcript, governance, report-history, whitespace, and
    Git integrity checks; all four required GitHub checks must be green at the
    pushed final head, with OAP bootstrap acceptance PASSING with 007-n
    quarantined.
11. Recovery-linkage negative proof: in a throwaway copy of the branch state,
    show that removing the prior_report_recovery block from the 007-o order
    makes check_transcript fail with RECOVERY_LINKAGE_MISSING, while the intact
    order passes with 007-n and 007-d both quarantined. Record both results in
    the report. This proves the linkage is load-bearing, not decorative.
12. Report hygiene: before pushing, the final 007-o report must pass
    `verify_report.py` (local mode) and `check_transcript.py --repo-root .
    --revision HEAD --expected-id 007-o` at the report commit; no command
    string may contain a placeholder token in angle brackets or the literal
    tokens VERIFY, TBD, TODO, or UNRESOLVED. This round must not produce a
    second quarantined report.
13. Publish one final report-only 007-o commit with the literal implementation
    head as sole parent and only the report path changed; verify remote head,
    report bytes, parent, and changed-path invariant; send response OK and stop.
    PR #8 remains open and unmerged.

## Acceptance criteria

1. RESEARCH-STATE.md exists on the branch, is referenced from
   research/README.md as START HERE, contains all fifteen sections, and every
   quoted number matches a primary record (consistency test green).
2. The consistency test demonstrably fails on an altered number (negative proof
   recorded in the report) and passes at the implementation head.
3. STATUS.md no longer states blanket "linguistic evaluation NOT RUN"; the
   layered distinction (reference-based benchmark evaluation done on A100-FP8
   same-sample; human-labelled target-distribution evaluation not run; product
   functionality planned) is present; 001-006 history untouched.
4. The PR #8 description states the 007-o closure round, points to
   RESEARCH-STATE.md, and carries a truthful Application-baseline status.
5. All four required checks green at the final head, including OAP bootstrap
   acceptance with 007-n classified INVALID_QUARANTINED and the 007-d
   quarantine preserved; report-only commit invariant verified remotely; PR #8
   open/unmerged; REPORT-HISTORY-INCIDENTS.json unchanged (exactly the two
   frozen incidents); no immutable order or report mutated.
6. Zero model calls, zero network calls beyond normal GitHub publication, zero
   private data in public artifacts (publication guard and privacy scan pass).
7. The 007-o report passes local verify_report before push and carries no
   placeholder tokens in any recorded command.
8. RESEARCH-STATE.md records the updated sequencing: 007-m frozen; 008
   structural-boundary qualification as the next objective (new PR); 009 fresh
   human-labelled linguistic confirmation reserved until the post-008 pipeline
   freeze; no 009 data in 008; no 007-m tuning in 008.

## Verification

Focused: `python3 -B -m unittest research.tests.test_research_state_consistency
-v` (and its negative-tamper run in a throwaway copy); `python3 -B -m unittest
discover -s research/tests -v`; `python3 -B -m research.tools.rebuild_tables
--check`; publication guard on the research tree. Recovery: `check_transcript.py
--repo-root . --revision HEAD --expected-id 007-o` at the implementation head
(007-n and 007-d quarantined); throwaway negative-linkage proof per Requirement
11. Broader: `python3.12 scripts/verify_development_baseline.py --temp-parent
<literal native temp path recorded in the report>` (must reach PASSED including
Application baseline); `python3 -B -m unittest discover -s oap/tests -v`;
`check_governance.py --mode accepted-runtime --accepted-ref
2832fa1e51bdf3641aabbd81feab8ddb64a876da`; `check_report_history.py --revision
HEAD --require-manifest`; `check_whitespace.py` against both accepted bases;
protected-source diff against the application accepted base; `git fsck --full
--no-reflogs`; `verify_report.py` (local) on the 007-o report before push.
Evidence boundary: local commands at the literal implementation head; final-head
GitHub checks awaited before the report; no live model, no private data.
Negative paths: tampered-number test failure; guard refusal of a planted
private-path canary; report-history refusal if any prior report byte changed
(must not occur); transcript refusal without the recovery block (Requirement 11).

## Local setup and constraints

CPU-only, offline; inherited persistent TMPDIR conventions; no system temporary
directory for research tools; no data acquisition; no GPU/model/service access;
no network beyond normal GitHub publication; private experiment roots read for
manifest-hash identity only; never print, persist, or copy private text,
prompts, responses, credentials, or private paths into public artifacts; keep
private absolute paths out of the public document.

## Documentation

RESEARCH-STATE.md must be readable by a competent independent reviewer with no
access to private roots: every claim cites a public record (path plus SHA where
material); the document states which evidence is unmerged-PR-only; it names the
human gates (target-deployment decision, human annotation, milestone judgment)
and the D2 boundaries (release, deployment, protected-resource changes)
explicitly; it contains no acceptance claim; it must not cite the quarantined
007-n report as accepted transcript evidence (its check claims may be stated as
re-verified by this round).

## Git and report publication

AMEND_EXISTING_PR #8 on `oap/007-concept-verification`. Commit non-report work
(including the exact 007-o order and active bytes) in one or more commits with
truthful messages; update the PR #8 description in the same non-report push;
wait for final-head CI; then one report-only commit (SELF convention) with the
literal implementation head as sole parent and only
`oap/reports/007-o-consolidate-research-state.md` changed; push; verify remote
PR head, exact report bytes, parent, and changed-path invariant; send exact
response OK; stop. No merge, no auto-merge, no subsequent push for this round.

## Decision classification

D0. Documentation/evidence reconciliation inside architecture and risk budget;
the quarantine follows the protocol's defined forward-recovery path (not a new
dilemma); no product mutation; no judgment debt.

## Deferred human adjudication
- Decision: NONE

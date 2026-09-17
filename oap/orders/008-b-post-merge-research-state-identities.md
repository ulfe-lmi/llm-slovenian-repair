# Work order 008-b — Post-merge research-state identities and 008-a ledger registration

Status: FINAL

Finalized by strategic reconciliation of 2026-09-17: independent final-head
review of 008-a at head 8dbb79a20f129d4c07c6b94827cacad74683ba6b (private
workorders/008-a-final-head-review-20260917.md), including independent
re-derivation of the 008-a scientific results and of the stale-consistency-
test mechanics from the committed test source. This round is a bounded
documentation/state corrective suffix of objective 008: it restores all four
required checks to green at its final head by the only viable non-weakening
means (additive post-merge identity update) and registers the 008-a research
round in the canonical experiment ledger. It contains no new scientific work.

```oap-metadata
{
  "id": "008-b",
  "title": "Post-merge research-state identities and 008-a ledger registration",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "8dbb79a20f129d4c07c6b94827cacad74683ba6b",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "dependencies": ["008"],
  "local_work": "Preserve every merged 000-007 seam byte-for-byte, the merged research/ tree (including research/prose-boundary/ from 008-a), all private experiment roots, the research test suite byte-for-byte, and any unrelated local work (including the untracked .research-test-scratch/ directory).",
  "prior_review": "Strategic final-head review of 008-a (2026-09-17, private workorders/008-a-final-head-review-20260917.md): report-only commit 8dbb79a (sole parent db9de49, changed path exactly oap/reports/008-a-qualify-prose-boundary-parser.md); verify_report (remote) result verified; transcript valid (active=latest=008-a); whole-round diff in-scope (26 files, research/prose-boundary/ + order + active + report) with zero immutable-report mutations, zero test changes, zero model calls; every cited 008-a record SHA re-verified; independent re-derivation: 1,288/1,288 coordinate invariants hold (0 violations), structural policy re-derived with strategy-authored ancestor tracking (0 missing prose bytes; 0 protected-region exposures under the documented D0 autolink rule; 183 autolink-destination bytes are protected only by that documented rule), selection/differential/challenger numbers re-checked against committed artifacts (8,919 -> 2,670 -> 100; 22 class-7 spans; NOT_TRIGGERED); CI at the final head observed red on exactly the two pre-predicted stale-snapshot assertions (Research reproducibility; Application baseline count stage) and green on OAP bootstrap acceptance + OAP report history. Two findings carried forward: (A) REPORT.md body number '4,910 input bytes' is the pre-rework total; the committed post-rework suite totals 4,907 bytes; (B) the config's literal candidate_rule does not encode the D0 autolink-destination rule. The 008-a report's 'D1 dilemma candidate' (requirement 9 vs. merged 007-o snapshot test) is reclassified D0 by strategy with the exact green path verified from the test source.",
  "provenance": [
    {"kind": "H", "reference": "Owner research decision 2026-09-17 (protection research precedes linguistic confirmation; keep the OAP loop moving; finish the 007 closure and reconcile current truth before new objectives) and standing instructions: do not weaken a gate, do not manufacture green status, do not silently skip corrective work, do not rewrite immutable reports, never use the owner as a relay for routine D0/D1 engineering choices."},
    {"kind": "A", "reference": "S-ORDER-01/02/03 (corrective suffixes preserve branch and PR), S-EVIDENCE-01 (distinct evidence states; truthful check recording), S-DECIDE-01 (D0 routine reversible choice), S-ICA-01 (map research state to actual evidence); the research-state-machine-v1 block contract and the frozen 007-o consistency test (research/tests/test_research_state_consistency.py, read-only); research/registry/experiments.json schema_version 3."},
    {"kind": "E", "reference": "Verified current state 2026-09-17 (this session, from remote and primary records): remote main = 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 (merge commit of PR #8; parents ee2d1b479719009ff1d07829478f241e3f395f7c and 4a029287f27e038d5c34c39b26ca836be7c6914b); PR #9 OPEN/UNMERGED/MERGEABLE, head 8dbb79a20f129d4c07c6b94827cacad74683ba6b, auto-merge disabled; final-head CI at 8dbb79a: Research reproducibility FAIL (test_main_is_ancestor_of_reviewed_head live origin/main 7d2cc9ee != block ee2d1b47; test_registry_and_report_counts 45-1=44 != 43), Application baseline FAIL (same count assertion in its .git-less workspace), OAP bootstrap acceptance PASS, OAP report history PASS; registry holds 24 entries without 008-a; the consistency test reads both main_sha and reviewed_branch_head_sha from the machine block (lines 122-138), so setting both to 7d2cc9ee... satisfies both assertions (self-ancestor exit 0 verified; live-ref equality holds while main is 7d2cc9ee...)."},
    {"kind": "I", "reference": "Strategy independent final-head review of 008-a (private workorders/008-a-final-head-review-20260917.md): identity chain, scientific re-derivation, findings A/B, test-mechanics analysis, and the D0 classification of the reported dilemma with the exact additive green path."}
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
  "lr": ["LR-001", "LR-003", "LR-007", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

Corrective suffix `008-b` of objective 008 on the existing branch
`oap/008-prose-boundary-qualification` and existing PR #9 (AMEND_EXISTING_PR),
based on the 008-a final head `8dbb79a20f129d4c07c6b94827cacad74683ba6b`.
The round is a bounded documentation/state correction with **no new
scientific content**: it updates the post-merge research-state identities so
the frozen 007-o consistency test is satisfied again at the final head, and it
registers the completed 008-a research round in the canonical experiment
ledger. No parser runs, no fixtures, no model calls, no application changes.

## Provenance

Owner-directed sequencing (H) on verified current state (E) with strategy's
independent 008-a final-head review and test-mechanics analysis (I), governed
by the OAP corrective-suffix and evidence-truth contracts (A). The stale-test
contradiction was reported by the 008-a coding round as a D1 dilemma candidate;
strategy investigated it and classified it D0 (single viable non-weakening
remedy; no human judgment debt).

## Current verified state

Verified by strategy 2026-09-17 (this session) from the remote and primary
records:

- Remote `main` = `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9` (merge commit
  "Merge pull request #8"; parents `ee2d1b479719009ff1d07829478f241e3f395f7c`
  and the reviewed 007-o head `4a029287f27e038d5c34c39b26ca836be7c6914b`).
  PR #8 MERGED; objective 007 closed.
- PR #9: OPEN, UNMERGED, MERGEABLE, auto-merge disabled; head
  `8dbb79a20f129d4c07c6b94827cacad74683ba6b` (008-a report-only commit, sole
  parent `db9de499a44d86fcaac39f5ef1a701ea01f1ad26`, changed path exactly
  `oap/reports/008-a-qualify-prose-boundary-parser.md`).
- `oap/active` = `008-a`; the 008-a report exists and is verified
  (verify_report remote: verified; check_transcript: valid, active=latest
  =008-a; report history valid with exactly the two frozen incidents).
- Final-head CI at `8dbb79a` (observed): Application baseline FAIL (2m38s);
  Research reproducibility FAIL (13s); OAP bootstrap acceptance PASS; OAP
  report history PASS. Both failures are exactly the stale 007-o snapshot
  assertions (demonstrated in the 008-a report pre-push and re-confirmed by
  strategy at the final head): `test_main_is_ancestor_of_reviewed_head`
  (live `refs/remotes/origin/main` = 7d2cc9ee != block `main_sha` ee2d1b47)
  and `test_registry_and_report_counts` (45 report files - 1 = 44 != block
  `oap_reports_reviewed` 43). No other failing test.
- Test mechanics (read from `research/tests/test_research_state_consistency.py`
  lines 122-138, read-only): `test_main_is_ancestor_of_reviewed_head` reads
  BOTH `main_sha` and `reviewed_branch_head_sha` from the machine block and
  asserts (i) `merge-base --is-ancestor main_sha reviewed_branch_head_sha`
  and (ii) `refs/remotes/origin/main == main_sha` (when the ref exists).
  Setting both fields to `7d2cc9ee...` satisfies both (self-ancestor
  verified exit 0; live-ref equality holds while main is 7d2cc9ee...).
  `test_registry_and_report_counts` asserts `registry_entries ==
  len(experiments.json entries)` and `oap_reports_reviewed == (report .md
  files - 1)` (the 007-o report file is excluded). At this round's final head
  there will be 46 report files, so the block must hold 45; the registry
  will hold 25 entries after 008-a registration.
- Registry (`research/registry/experiments.json`, schema_version 3): 24
  entries, 2-space indent, trailing newline; no 008-a entry; top-level scope
  string currently "all enumerated experiment and recovery roots plus stable
  child runs/phases and one non-benchmark diagnostic".
- `research/tables/experiment-summary.csv` is the deterministic projection of
  the registry via `python3 -B -m research.tools.rebuild_tables` and must be
  regenerated when the registry changes.
- Strategy 008-a review findings carried into this round's section 16:
  (A) REPORT.md "4,910 input bytes" is the pre-publication-rework fixture
  total; the committed post-rework suite totals 4,907 bytes (F30 73 -> 70
  bytes); (B) the D0 autolink-destination rule is not encoded in the
  config's literal `candidate_rule` text.

## Governance

S-ORDER-01/02/03, S-EVIDENCE-01, S-DECIDE-01, S-ICA-01 govern. D0: a routine,
reversible documentation/state correction after a development-only merge; the
corrective-suffix mechanism is the governing OAP path; all numeric
re-derivation assertions and all test logic remain byte-unchanged and fully
binding. No D2 boundary is crossed; no judgment debt is registered.

## Goal and dependencies

Restore all four required checks to green at this round's final head by the
only viable non-weakening means (additive post-merge identity update), and
make the canonical research ledger complete for objective 008 by registering
the 008-a round. Depends on 008-a (complete, verified, GO). This round adds no
experiment, no tuning, no parser execution, and no model call; it changes no
scientific result.

## Scope

Exactly the following; nothing else.

1. `research/RESEARCH-STATE.md` — machine-readable block
   (`research-state-machine-v1`): change EXACTLY these five fields, all other
   block bytes unchanged (including quarantined_007n, branch, pr_number,
   frozen_007m_* hashes, frozen_report_history_incidents, and every
   official_scorer/custom_alignment/campaign/007m section):
   - `identities.main_sha`:
     `ee2d1b479719009ff1d07829478f241e3f395f7c` ->
     `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`
   - `identities.reviewed_branch_head_sha`:
     `735c9830db95cbb02fc80446b6d28f62a56f10c9` ->
     `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`
   - `identities.reviewed_branch_head_parent_sha`:
     `b61f8e2e6b454a0969e5f2ac9009d4da87b8b215` ->
     `4a029287f27e038d5c34c39b26ca836be7c6914b`
   - `identities.registry_entries`: `24` -> `25`
   - `identities.oap_reports_reviewed`: `43` -> `45`
2. `research/RESEARCH-STATE.md` — insert a new top-level section
   `## 16. Post-merge acceptance update (objective 008, round 008-b)`
   immediately BEFORE `## Machine-readable state block (research-state-
   machine-v1)`. The 007 narrative (sections 1-15) must remain byte-identical
   except item 4 below. Section 16 must contain at least these statements:
   (a) PR #8 was development-only merged 2026-09-17 (merge commit
   `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`, second parent the reviewed
   007-o head `4a029287f27e038d5c34c39b26ca836be7c6914b`; strategy receipt
   `workorders/007-o-final-head-review-20260917.md`; workflows are
   pull_request-triggered, so the merge had no deployment side effect); the
   machine block now tracks the current accepted main.
   (b) The 007-o review point remains fully recorded in the 007 narrative,
   the unchanged quarantined 007-n identity, the committed 007-o order and
   report; this identity update is additive and records the accepted
   post-merge state; it is not a rewrite of the 007 narrative.
   (c) Rationale: the 007-o snapshot test's live-ref and report-count
   assertions are structurally unsatisfiable at any post-merge head
   (demonstrated at 008-a; disclosed in the 008-a report as a dilemma
   candidate; classified D0 by strategy; the only viable non-weakening
   remedy is this additive identity update as a corrective suffix); no test
   logic changed; every numeric re-derivation assertion remains binding.
   (d) 008-a outcome GO, with pointers (`research/prose-boundary/REPORT.md`;
   `oap/reports/008-a-qualify-prose-boundary-parser.md`) and facts: 50 frozen
   fixtures x 3 profiles, 1,288 parser events, 0 coordinate violations, 0
   protected-region exposures (under the documented D0 autolink rule), 0
   missing prose bytes, 100 deterministically selected preserved outputs
   (2,670 unique texts; 100 percent plain prose — recorded
   representativeness limitation), 22 class-7 differential spans (18 number,
   4 upper-identifier; 110 bytes), 0 safety-class false exposures,
   markdown-rs challenger NOT_TRIGGERED.
   (e) 008-a final-head CI was red on Research reproducibility and
   Application baseline solely through the stale snapshot assertions (as
   predicted in the 008-a report before push); this round restores all four
   required checks to green at its final head.
   (f) Correction: REPORT.md's "4,910 input bytes" is the
   pre-publication-rework fixture total; the committed post-rework suite
   totals 4,907 bytes (F30 reworded 73 -> 70 bytes); no semantic change.
   (g) Carried into 008-c: (i) the D0 autolink-destination rule (the config's
   literal `candidate_rule` does not encode it; the 183 autolink-destination
   bytes of F24/F48 are protected only by that documented D0 evaluator rule;
   008-c must implement it in the runtime and amend the committed config
   rule text); (ii) the D1 policy token-family matching note; (iii) the
   recorded neutral tradeoffs (strikethrough/superscript/subscript exposed;
   image alt text protected).
   (h) Sequencing: 008-c (parser-first protection architecture; next order on
   this branch/PR) freezes the effective pipeline; objective 009 remains
   reserved for the fresh human-labelled linguistic confirmation; the 007-m
   linguistic system stays frozen.
3. `research/RESEARCH-STATE.md` — exactly one heading-line replacement, line
   for line, with no other byte of the 4.2 section body changed:
      before: `### 4.2 Registry roots (all 24 entries of \`research/registry/experiments.json\`)`
      after:  `### 4.2 Registry roots (24 entries at the 007-o snapshot; 25 after the 008-b update)`
4. `research/registry/experiments.json` — append EXACTLY one new entry at
   the end of the `experiments` array (2-space indent, trailing newline
   preserved), with these exact field values (the coding round re-verifies
   that every cited `sha256` equals the committed file bytes at base head and
   that `size` equals the file size; do not alter any existing entry):

```json
{
  "experiment_id": "008-a-qualify-prose-boundary-parser",
  "logical_root": "research/prose-boundary (committed data-free research subtree; no private root)",
  "kind": "study",
  "variation": "falsification-first structural segmentation qualification of pulldown-cmark 0.13.4",
  "status": "COMPLETE",
  "question": "Does pulldown-cmark 0.13.4 provide sufficiently accurate, conservative and source-faithful structural segmentation of actual LLM-generated Markdown-like output to replace the Markdown-sensitive part of the current hand-written protection logic?",
  "frozen_choices": {
    "candidate": "pulldown-cmark 0.13.4 (MIT; registry checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e; upstream tag v0.13.4)",
    "fixtures_frozen_before_first_parser_run": true,
    "new_model_calls": 0,
    "dataset": "50 project-authored adversarial fixtures (38 required classes + 12 extras) + 100 deterministically selected preserved outputs (private; counts/hashes only in public artifacts)"
  },
  "metrics": {
    "model_calls": 0,
    "fixtures": 50,
    "parser_profiles": 3,
    "parser_events": 1288,
    "coordinate_violations": 0,
    "protected_region_exposures": 0,
    "prose_candidate_missing_bytes": 0,
    "representative_corpus_samples": 100,
    "corpus_unique_texts": 2670,
    "differential_disagreement_spans": 22,
    "differential_false_exposures": 0
  },
  "evidence_files": [
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/config/experiment-008a.json", "sha256": "c02a415a064d731672d98a4e0b0f6e829356323dbb00b409cc05fddd89db9300", "size": 11784},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/identity/candidate-identity.json", "sha256": "671d7cded433bbc0a3e1f60fcb4a2da7d89f2a79e254f6a5b57ac80eb38d9c0d", "size": 4634},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/fixtures/fixtures.json", "sha256": "ad2fcef95dc044e941bf346c64dc5e71d42b43a75e4334f88a0dcd012a26adc9", "size": 69220},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/results/increment1/summary.json", "sha256": "fa1ef6fbd229031c012d97e0ff3db80e0a173c63180164b865d18d2adb1ed021", "size": 135044},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/results/increment1/gate-decision.json", "sha256": "0afb138ec2e05822016f4debb74aeff43f49f4e83d7122ef70bfd0d14b52f554", "size": 1831},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/results/increment2/selection-receipt.json", "sha256": "cb27cb462cf9b33e42ce1e77db5ef5d9a33d0a3fc411aea39a08587ec8b1391b", "size": 9751},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/results/increment2/differential-summary.json", "sha256": "287319ffccaa357af88142f000c28fb373d45164b07231c86290f977a460c08c", "size": 44281},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/results/increment2/challenger-decision.json", "sha256": "8c056bc94cf514c6fe46277998deb3dd5d4208a80ac2727695ec5f818863c68f", "size": 1121},
    {"disposition": "data-free public projection", "logical_path": "research/prose-boundary/REPORT.md", "sha256": "7458ac7afdeb3726e2c4c40a10cad3fe0fe8a42a4aa04970a76ee21a0ed3e540", "size": 20256}
  ],
  "evidence_status": "public-data-free",
  "public_report": "research/prose-boundary/REPORT.md",
  "public_configuration": "research/prose-boundary/config/experiment-008a.json",
  "public_metrics": "research/prose-boundary/results/increment1/summary.json",
  "source_manifest": "none (no private source; committed data-free research subtree)",
  "child_runs": [],
  "conclusion": "GO: on 50 frozen fixtures x 3 profiles (1,288 parser events) all 8 hard invariants hold (exact source-range fidelity, no UTF-8 bisection, zero protected-region exposures under the documented D0 autolink rule, zero missing prose bytes, deterministic bounded recovery, stock-CLI cross-check). On 100 deterministically selected preserved outputs (2,670 unique texts; 100 percent plain prose - recorded representativeness limitation) the differential against the current regex protection is 22 disagreement spans, all class 7 (18 number, 4 upper-identifier; 110 bytes), zero safety-class false exposures; markdown-rs challenger NOT_TRIGGERED. Structural qualification only: not linguistic acceptance, not production integration; 008-c (parser-first protection architecture) follows on the same PR; objective 009 reserved.",
  "pending_evidence": [
    "008-c: parser-first protection architecture with 4-way rule classification and differential regression gates",
    "009: fresh human-labelled target-distribution linguistic confirmation of the frozen effective pipeline"
  ]
}
```

   and replace the top-level `scope` string exactly from
   `all enumerated experiment and recovery roots plus stable child
   runs/phases and one non-benchmark diagnostic` to `all enumerated
   experiment and recovery roots plus stable child runs/phases, non-benchmark
   diagnostics, and the 008-a parser-qualification study (committed data-free
   subtree)`.
5. `research/tables/experiment-summary.csv` — regenerate deterministically
   with `python3 -B -m research.tools.rebuild_tables` (adds exactly one 008-a
   row; every pre-existing row byte-identical); `rebuild_tables --check`
   green.
6. `oap/orders/008-b-post-merge-research-state-identities.md` (this exact
   order, written by the publication helper) and `oap/active` -> `008-b`.
7. `oap/reports/008-b-post-merge-research-state-identities.md` — the final
   report-only commit.

## Non-goals

No changes to `research/tests/` (byte-identical, including
`test_research_state_consistency.py`); no changes to `research/prose-
boundary/` or any other research path except the four named files; no
application source changes; no protected-source changes; no parser or
adapter execution (the 008-a binaries stay as committed records); no fixture,
config, or expectation changes; no Qwen/model calls; no data acquisition; no
objective-009 data touched; no linguistic tuning of the frozen 007-m system;
no prompt/threshold/ranking changes; no merge or auto-merge; no release or
deployment; no rewriting of any prior immutable order or report; no change to
`oap/REPORT-HISTORY-INCIDENTS.json`; no weakening, skipping, or redefinition
of any check (test logic byte-unchanged; every numeric re-derivation
assertion remains binding); no 007-narrative rewrite in RESEARCH-STATE.md
outside the scoped block fields, new section 16, and the single 4.2 heading
line.

## Files and boundaries

Read/inspect: `research/RESEARCH-STATE.md`;
`research/tests/test_research_state_consistency.py` (read-only, to confirm
the assertion mechanics before editing the block); `research/registry/
experiments.json`; `research/prose-boundary/` (identity/SHA verification
only); `oap/orders/008-a-*.md`; `oap/reports/008-a-*.md`; the four GitHub
workflow definitions. Write: exactly the seven scoped paths (the three
research files, this order, `oap/active`, the 008-b report).

## Requirements

1. Reconcile before mutation: exact active 008-b; remote branch head equals
   base_sha `8dbb79a20f129d4c07c6b94827cacad74683ba6b`; PR #9 open; remote
   main equals `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`; preserve all local
   work.
2. Apply the machine-block changes of scope item 1 exactly. Verify by
   re-parsing the block: exactly five fields differ from the base-head block;
   every other byte of the block identical.
3. Insert section 16 (scope item 2) with all eight required statements
   (a)-(h); the sections 1-15 body stays byte-identical except the 4.2
   heading line (scope item 3).
4. Append the 008-a registry entry (scope item 4) with the exact field
   values; verify every cited `sha256` and `size` against the committed
   files at base head; apply the exact scope-string replacement; the JSON
   must parse with 25 entries and 2-space indentation preserved.
5. Regenerate `research/tables/experiment-summary.csv` with the
   `rebuild_tables` tool; `python3 -B -m research.tools.rebuild_tables
   --check` must pass.
6. Local verification at the implementation head:
   `python3 -B -m unittest discover -s research/tests` must show
   `test_main_is_ancestor_of_reviewed_head` PASSED and
   `test_registry_and_report_counts` FAILED with exactly the expected
   pre-report count difference (45 report files - 1 = 44 != 45) — this is the
   designed pre-report state, to be recorded truthfully, not "fixed" by any
   test change; all other research tests pass.
7. Run the real `scripts/verify_development_baseline.py` entry point and the
   OAP hygiene suite at the implementation head (transcript expected id
   008-b, report history valid with exactly the two frozen incidents,
   whitespace checks against the accepted bases, protected-source diff exit
   0, `git fsck --full --no-reflogs`, publication guard on research/).
8. Wait for final-head CI; at the final head all four required checks must
   be green (Research reproducibility: the full suite including both
   formerly stale assertions; Application baseline: its full-pytest stage
   including the count assertion in the .git-less workspace). Record the
   per-head check states truthfully in the report (implementation head:
   Research reproducibility and Application baseline red on the expected
   count assertion only; final head: all green).
9. Publish one final report-only 008-b commit with the literal
   implementation head as sole parent and only the report path changed;
   verify remote head, report bytes, parent, and changed-path invariant via
   `verify_report` (remote); send response OK and stop. PR remains open and
   unmerged.
10. No model calls, no parser runs, no network use beyond normal GitHub
    publication.

## Acceptance criteria

1. RESEARCH-STATE.md diff is limited to the five machine-block field lines,
   the new section 16, and the single 4.2 heading line; section 16 contains
   all eight required statements (a)-(h) with exact identities.
2. Registry: exactly one entry added (008-a, exact field values), the exact
   scope-string replacement, valid JSON, all evidence SHAs/sizes verified
   against base-head bytes; 25 entries total.
3. experiment-summary.csv equals the deterministic rebuild_tables output
   (check green); all pre-existing rows byte-identical.
4. All four required checks green at the final head; per-head states recorded
   truthfully in the report; no check weakened, skipped, or redefined;
   `git diff 8dbb79a..final -- research/tests` empty.
5. Report-only commit invariants verified remotely; PR open/unmerged; no
   immutable prior order or report mutated; no protected source changed.
6. Zero Qwen/model calls; zero parser executions; 009 data untouched; no
   linguistic tuning.

## Verification

Focused: the research test suite at the implementation head (exact expected
failure set per requirement 6) and at the final head (all green); the
machine-block re-parse (exactly five fields changed); the registry entry
SHA/size verification against base-head bytes; `rebuild_tables --check`;
whitespace, protected-source diff, `git fsck --full --no-reflogs`, report
history, transcript (expected id 008-b), publication guard. Broader: real
`scripts/verify_development_baseline.py`; final-head GitHub checks. Negative
paths: (1) one deliberately altered non-scoped block field in a local scratch
copy must fail the consistency test (demonstrate locally on a scratch copy,
never in the working tree); (2) report-history refusal if any prior report
byte changed (must not occur); (3) the implementation-head count assertion
stays red until the report commit lands (recorded, not fixed). Evidence
boundary: local commands at the literal heads plus the read-only remote CI
state; no model, no parser, no private data in public artifacts.

## Local setup and constraints

CPU-only; no Rust toolchain use; no parser/adapter binaries executed; no
GPU/model/service access; no network beyond normal GitHub publication; no
private roots read; never print, persist, or copy private text, prompts,
responses, credentials, or private paths into public artifacts.

## Documentation

The 008-b report must state: the D0 classification of the 008-a-reported
dilemma candidate (with the one-line rationale: single viable non-weakening
remedy; corrective suffix; all numeric assertions and test logic unchanged);
the per-head CI truth (red at the implementation head on the expected count
assertion only; green at the final head); that this round changes no
scientific result and registers the 008-a GO evidence in the ledger; and
that PR #9 remains open for 008-c.

## Git and report publication

AMEND_EXISTING_PR on `oap/008-prose-boundary-qualification` (PR #9) from
`8dbb79a20f129d4c07c6b94827cacad74683ba6b`. Commit the exact 008-b order and
active bytes first; then the research-state update (scope items 1-5) in one
or more commits with truthful messages; wait for final-head CI; then one
report-only commit (SELF convention) with the literal implementation head as
sole parent and only `oap/reports/008-b-post-merge-research-state-
identities.md` changed; push; verify remote PR head, exact report bytes,
parent, and changed-path invariant; send exact response OK; stop. No merge,
no auto-merge, no subsequent push for this round.

## Decision classification

D0. Routine, reversible documentation/state correction after the
development-only merge of PR #8; the corrective-suffix mechanism is the
governing OAP path for the reported contradiction; every test assertion
remains binding. No D2 boundary is crossed.

## Deferred human adjudication
- Decision: NONE

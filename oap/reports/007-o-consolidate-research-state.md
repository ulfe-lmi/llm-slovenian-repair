# Work report 007-o — Quarantine the machine-invalid 007-n report and consolidate the research state

```oap-report
{
  "id": "007-o",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-o-consolidate-research-state.md",
  "order_sha256": "05509332f3935d89600da81e31f6bd374e39f748f8f11b87c455ddcf88ff5eb2",
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
  "implementation_head": "f20bc5538de25cbafa455c7f89b2900381fe1057",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "735c9830db95cbb02fc80446b6d28f62a56f10c9",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest research.tests.test_research_state_consistency -v",
      "result": "PASSED",
      "details": "10/10 at the implementation head on the real checkout: the embedded machine-readable block (research-state-machine-v1) re-derived from primary records matches; the three git-identity assertions (quarantined 007-n report bytes, remote-main ancestry, committed 007-o order metadata cross-check) run fully in a real checkout.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "negative tamper proof: throwaway copy of the f20bc55 branch state under /home/ubuntu/.local/share/llm-slovenian-repair/oap-007-o-scratch; changed exactly one embedded number in the copy's research/RESEARCH-STATE.md (007m_hybrid tp 799 -> 798) and ran python3 -B -m unittest research.tests.test_research_state_consistency in the copy; the intact copy passed the same test",
      "result": "PASSED",
      "details": "The tampered copy FAILED the consistency test as required (exit 1; the stages+gold and delta assertions caught the altered value), while the intact copy passed 10/10. The machine-readable block is binding, not decorative.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "recovery-linkage negative proof (Requirement 11): throwaway copy of the f20bc55 branch state; removed the prior_report_recovery block from the copy's committed 007-o order (single throwaway commit inside the copy, never pushed) and ran python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-o; the intact branch state passed the same command with both quarantines",
      "result": "PASSED",
      "details": "Copy with the block removed: check_transcript exited 2 with RECOVERY_LINKAGE_MISSING. Intact state: result valid with 007-n and 007-d both classified INVALID_QUARANTINED and report history valid (43 reports, exactly the two frozen historical incidents). The forward-recovery linkage is load-bearing.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "232/232 research tests at the implementation head (222 pre-existing plus the 10 new consistency tests).",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "PASSED",
      "details": "The deterministic numeric table matched the registry.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "The public research tree passed the privacy guard on 153 files (151 pre-existing plus RESEARCH-STATE.md and the new test): no raw text, targets, replacements, prompts, responses, credentials, endpoint values, profile paths, or private root paths. Negative canary: a planted private-path file in a throwaway copy made the guard fail (exit 1, 'absolute/private path' diagnostic); the canary was removed from the copy only.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /home/ubuntu/.local/share/llm-slovenian-repair/oap-007-o-temp --command-timeout 900",
      "result": "PASSED",
      "details": "The real baseline driver completed every stage PASSED with cleanup PASSED at the implementation head: uv lock --check, frozen dependency sync, focused contract tests, full pytest, Ruff, mypy, OAP unittest discovery, sdist and wheel build, built-wheel selection, fresh offline venv, offline runtime-only frozen sync, offline wheel installation, offline runtime import and metadata. Honest note: the first 007-o implementation commit (284d7d1) was red locally and in CI for two non-application causes - the ordered STATUS.md correction had not yet been paired with the same-commit generated-file pin refresh (SOURCE_GENERATION_DRIFT: STATUS.md in 22-23 OAP tests and in the bootstrap acceptance), and the new consistency test's git-identity assertions assumed a .git history that the driver's pytest workspace excludes. Commit f20bc55 fixed exactly those two artifacts (pin refresh in oap/GENERATED-FILES.json and oap/INSTALLATION.json; workspace-aware skip in the new test); no application code was changed, and this driver run at f20bc55 reached PASSED.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "129-test OAP suite: green in CI at the implementation head (OAP bootstrap acceptance, run 35206744322) and green in the baseline driver's OAP unittest discovery stage at the implementation head; the affected module (test_report_history_cache, 20 tests) passed 20/20 in an isolated local run with a warm git cache. One standalone local full-suite run recorded 128/129: a single test hit the hard 30-second git subprocess timeout of validate_acquisition_history during a cold-cache storage stall on this host (the identical git command measured 36.1 s cold and 0.26-0.31 s warm, with 0.06 s CPU, i.e. pure I/O wait); the test exercises resources/source-acquisitions, which this round does not touch. The defect is environmental latency, not a round change.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-o",
      "result": "PASSED",
      "details": "result valid at the implementation head: active=latest=007-o; quarantined_reports = 007-d (corrective 007-e) and 007-n (corrective 007-o), both INVALID_QUARANTINED, coexisting in one transcript; report history valid with 43 reports and exactly the two frozen historical incidents.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "details": "Governance structure valid in accepted-runtime mode; semantic and human authorization proofs remain false.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "Report history valid with exactly the two frozen historical incidents (RHI-0001, RHI-0002); the manifest (oap/REPORT-HISTORY-INCIDENTS.json, sha256 a3c874d58f0d62e5032347a4eb7fec5e0e5c020a78f23e69f72044161da4a92a) is unchanged; a quarantine is not a history incident.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da --revision HEAD and python3 oap/bin/check_whitespace.py --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base whitespace checks passed at the implementation head with exactly the three pre-existing frozen blank-at-EOF incident paths.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No protected source changed against the application accepted base at the implementation head.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Git object integrity passed at the implementation head; only pre-existing dangling scratch objects remain, no corruption.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/pulls/8 and gh api repos/ulfe-lmi/llm-slovenian-repair/actions/runs (per-run head_sha/conclusion for runs 35206744338, 35206744322, 35206744339)",
      "result": "PASSED",
      "details": "PR #8 observed OPEN and UNMERGED (merged_at null, auto-merge null) at head f20bc5538de25cbafa455c7f89b2900381fe1057. All four required checks green at that exact head: Application baseline success (run 35206744338), OAP bootstrap acceptance success (run 35206744322, with 007-n classified INVALID_QUARANTINED and the 007-d quarantine preserved), OAP report history success (same run), Research reproducibility success (run 35206744339). The PR #8 description was updated in this non-report window to the 007-o closure wording with the RESEARCH-STATE.md pointer and truthful Application-baseline status. No acceptance, merge, release, or deployment claim.",
      "sha": "f20bc5538de25cbafa455c7f89b2900381fe1057",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-17T10:54:45+02:00",
  "report_written_at": "2026-09-17T12:51:03+02:00",
  "implementation": "Closure round 007-o, two implementation commits on oap/007-concept-verification (284d7d1, f20bc55), no scientific experiment, no model calls. (1) Committed the exact 007-o order (sha256 05509332f3935d89600da81e31f6bd374e39f748f8f11b87c455ddcf88ff5eb2, re-verified on the committed blob) whose canonical prior_report_recovery block classifies the machine-invalid 007-n report INVALID_QUARANTINED (forward recovery; precedent 007-d/007-e; the 007-n implementation stays accepted, the report byte-immutable). (2) Published research/RESEARCH-STATE.md: the single authoritative current research state (15 sections plus the research-state-machine-v1 machine-readable block); every number was re-derived by this round from the primary records named in its section 1 (registry, strategic-official-summary, the 007-h/i/j/m results projections, the campaign projections, the committed frozen 007-m config, Git identities, private-root manifest SHAs). (3) research/README.md now names RESEARCH-STATE.md as START HERE and marks EXPERIMENT-HISTORY.md a 007-d-era archival snapshot superseded as current state. (4) STATUS.md: the stale blanket 'linguistic evaluation NOT RUN' sentence was replaced with the layered wording (reference-based benchmark linguistic evaluation HAS run on A100-FP8, same-sample exploratory; the PLAN 14.2 human-labelled target-distribution evaluation remains NOT RUN; product detection/review/acceptance/patching remain PLANNED; Qwen compatibility UNVERIFIED; ICA NOT RUN) and one 007 progress paragraph was appended; the 001-006 history paragraphs are preserved verbatim (round diff shows only the two intended hunks). (5) Added research/tests/test_research_state_consistency.py, which re-derives the embedded block from primary records and fails on any altered number (negative proof recorded). f20bc55 then paired the ordered STATUS.md correction with the same-commit generated-file pin refresh (oap/GENERATED-FILES.json sha256/bytes, oap/INSTALLATION.json sha256) - the exact same-commit pattern used by every prior round that edited STATUS.md - and made the new test's three git-identity assertions workspace-aware (they skip with a stated reason in the baseline driver's .git-less pytest workspace; all numeric assertions still run there). No application code, no research data, config, projection, registry entry, or private root was changed.",
  "documentation": "research/RESEARCH-STATE.md is now the single authoritative CURRENT research state and is referenced from research/README.md as START HERE. It records the full experiment ledger (24 registry roots plus OAP rounds 007-a..007-n and every corrective/recovery round), the exact metric progression with denominators, the evidence hierarchy (including ABSENT human-semantic and milestone/ICA layers), the claims audit (PR #8 description, STATUS.md, README, EXPERIMENT-HISTORY.md, latest reports, the quarantined 007-n report), the PLAN matrix (D01-D07, M01-M07, S01-S05, section-16 criteria, section-14.2 NOT MET, calibration goals NOT MEASURED at N=0), the deployment-validity matrix (RTX-3090 target unreachable at reconnaissance; A100-FP8 regime evaluated; open evidence gap with two human-decision resolutions), open vs completed questions, the research-debt matrix, the owner's 2026-09-17 sequencing (007-m FROZEN FOR CONFIRMATION; 008 structural-boundary qualification as a new numeric objective and new PR, design summary only, not executed; 009 fresh human-labelled confirmation reserved, with the two prohibitions), the explicit no-further-tuning boundary, and the merge/release/deployment limitations. The PR #8 description carries the 007-o closure round, the RESEARCH-STATE.md pointer, the truthful Application-baseline status, and the quarantine record.",
  "criteria": "Acceptance 1: RESEARCH-STATE.md exists on the branch, is the README START HERE, contains all fifteen sections, and every quoted number matches a primary record (consistency test 10/10 green at the implementation head). Acceptance 2: the consistency test demonstrably fails on an altered number (tampered copy: exit 1, 2 assertion failures) and passes on the intact branch state (10/10). Acceptance 3: STATUS.md states the layered distinction and preserves the 001-006 history verbatim (round diff shows exactly two hunks). Acceptance 4: the PR #8 description states the 007-o closure round, points to RESEARCH-STATE.md, and carries the truthful Application-baseline status. Acceptance 5: all four required checks green at the final (implementation) head, OAP bootstrap acceptance passing with 007-n classified INVALID_QUARANTINED and the 007-d quarantine preserved; report-only commit invariant verified remotely by verify_report; PR #8 open/unmerged; oap/REPORT-HISTORY-INCIDENTS.json unchanged (exactly the two frozen incidents); no immutable order or report mutated. Acceptance 6: zero model calls, zero network beyond normal GitHub publication, zero private data in public artifacts (publication guard 153 files plus the planted-canary negative). Acceptance 7: this report passes local verify_report before push and carries no placeholder tokens in any recorded command. Acceptance 8: RESEARCH-STATE.md records 007-m frozen, 008 structural-boundary qualification as the next objective (new PR), 009 reserved, and both sequencing prohibitions.",
  "negative_paths": "Three negative proofs recorded: (1) tamper - one embedded number changed in a throwaway copy (007m_hybrid tp 799 -> 798) makes the consistency test fail (exit 1) while the intact copy passes 10/10; (2) recovery linkage - removing the prior_report_recovery block from the copy's committed 007-o order makes check_transcript exit 2 with RECOVERY_LINKAGE_MISSING, while the intact state is valid with both 007-n and 007-d quarantined; (3) publication guard - a planted private-path canary in a throwaway copy fails the guard (exit 1, absolute/private path diagnostic). Additionally, the first implementation commit's red Application baseline and red OAP bootstrap acceptance were reproduced and root-caused (stale STATUS.md pin; .git-less workspace git assertions) and fixed in f20bc55, after which both checks passed locally and in CI. No assertion was weakened: the skip added to the new test applies only where the git history it asserts on does not exist, and every numeric re-derivation assertion still runs in that workspace.",
  "boundary_fidelity": "Only the exact 007-o write set changed: the 007-o order (byte-exact, committed blob sha256 05509332f3935d89600da81e31f6bd374e39f748f8f11b87c455ddcf88ff5eb2), oap/active (007-o), research/RESEARCH-STATE.md (new), research/README.md, STATUS.md, research/tests/test_research_state_consistency.py (new), and the two OAP generated-file pin metadata files for the ordered STATUS.md correction. No prior order or report was mutated (the machine-invalid 007-n report and the quarantined 007-d report remain byte-immutable; REPORT-HISTORY-INCIDENTS.json is unchanged, sha256 a3c874d58f0d62e5032347a4eb7fec5e0e5c020a78f23e69f72044161da4a92a). No model, GPU, vLLM/CUDA, service, network, profile, or protected-resource change; no merge, auto-merge, release, or deployment; PR #8 remains OPEN and UNMERGED. No application code was touched in the 284d7d1 -> f20bc55 correction; only OAP generated-file metadata and the new test changed.",
  "setup": "Reconciled before mutation: exact active 007-o; remote main ee2d1b479719009ff1d07829478f241e3f395f7c; branch/PR #8 head 735c9830db95cbb02fc80446b6d28f62a56f10c9 (report-only 007-n publication, sole parent b61f8e2e6b454a0969e5f2ac9009d4da87b8b215); the 007-n report blob 2b74413b54faf65de7659d3cf9957271d7721573 with sha256 a0bf18f8b0e1218104f3fa4951be62758a3f4f5e88e7d776c4abe3d596b8372a and the 007-n order sha256 0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82, exactly as recorded in the order's prior_report_recovery block; PR #8 OPEN/MERGEABLE/UNSTABLE with auto-merge disabled. PR #8 reused (AMEND_EXISTING_PR). The delivered order file matched the expected sha256 before commit and on the committed blob after commit. Persistent TMPDIR conventions and owned native temp parents under /home/ubuntu/.local/share/llm-slovenian-repair were used; no system temporary directory was used for research tools. The strategic prepublication review of 2026-09-17 served as the analysis baseline; every machine-checkable number in it was re-derived against the primary records by this round (no discrepancies found).",
  "privacy": "Data-free and public-safe: no dataset rows, gold strings, prompts, response bodies, credentials, or private native paths appear in any public artifact. Private experiment roots are cited by logical root name and manifest SHA-256 only. The RTX-3090 reconnaissance endpoint is described as an internal address recorded in the private reconnaissance record; no address literal is published. The literal temp parent path appears only in the recorded baseline command, as the order requires. Publication guard passed on 153 files; a planted private-path canary was refused in a throwaway copy. Zero model calls; the only network use was normal GitHub publication and CI observation.",
  "limits": "No new scientific model calls, no data acquisition, no prompt/threshold/ranking/candidate-rule/validator/retry change, no resampling, no production integration, no objective-008 work (no parser installation, fixture creation, wrapper, or challenger comparison), no Qwen/vLLM/CUDA/GPU/service/network changes, no release or deployment, no merge or auto-merge, no CRITICAL append, no ICA launch. The frozen 007-m identity (configuration sha256 0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26, prompt sha256 572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d, final root manifest sha256 3fb4aef33542e7fa3f357acb905b75f4d7e7551783f83a422b5d1ea6272c25f8, 300 s / 2,000,000-byte / no-resample limits) is unchanged and is re-asserted by the consistency test against the committed config.",
  "human_gates": "D0 / Decision: NONE. CRITICAL remains the empty seed with zero open gates. The named human gates are recorded in RESEARCH-STATE.md sections 8-15: the target-deployment decision (section 9, resolution (a) or (b)), human annotation for M01/009, and the milestone judgment. Closing this round grants no merge, milestone, release, or deployment authority; PR #8 remains OPEN and UNMERGED for strategic review, and development merge is explicitly the strategy/human's, conditioned on the four green checks at the final head plus independent strategic review.",
  "scope": "Finished only the exact active 007-o order: the forward-recovery quarantine of the machine-invalid 007-n report (committed order with the canonical block), the current authoritative research-state document, the README START HERE and archival note, the layered STATUS.md correction with verbatim 001-006 history, the PR #8 description update, the focused consistency test with its positive/negative proofs, the full verification battery, and this report-only publication. Objective 008 was not started in any form (design summary recorded in RESEARCH-STATE.md section 12 only); objective 009 remains reserved. No next suffix, no merge, no release, no deployment.",
  "result_summary": "COMPLETE for the 007-o closure round. The transcript is coherent again: the machine-invalid 007-n report is classified INVALID_QUARANTINED through this order's canonical prior_report_recovery block (the protocol's designed path), coexisting with the preserved 007-d quarantine, and OAP bootstrap acceptance passes with both quarantines in place. Objective 007 reaches a reviewable closure point: research/RESEARCH-STATE.md is the single authoritative current research state, machine-bound to the primary records by a consistency test that fails on any altered number. The Application baseline is GREEN at the implementation head (inherited from the accepted 007-n repair and re-verified through the real driver), all four required checks are green at f20bc55, and PR #8 remains open and unmerged. This is a documentation/evidence reconciliation (D0); it makes no acceptance, milestone, release, or deployment claim."
}
```


## Result

The 007-o closure round is COMPLETE. The machine-invalid 007-n report is
classified INVALID_QUARANTINED through this order's canonical
prior_report_recovery block, coexisting with the preserved 007-d quarantine,
and OAP bootstrap acceptance passes with both quarantines in place.
research/RESEARCH-STATE.md is now the single authoritative current research
state, machine-bound to the primary records by a consistency test that fails
on any altered number. All four required checks are green at the
implementation head, the Application baseline is GREEN (inherited from the
accepted 007-n repair and re-verified through the real driver), and PR #8
remains OPEN and UNMERGED. This round makes no acceptance, milestone,
release, or deployment claim.

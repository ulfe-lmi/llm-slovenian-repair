# Work report 007-b — Complete reviewer and Codex evaluation

```oap-report
{
  "id": "007-b",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-b-complete-reviewer-and-codex-evaluation.md",
  "order_sha256": "571a67d400f7937915acead6b00694141bf2f5a72fbf136a9a5d6a7dbbc7be1a",
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
  "implementation_head": "061100114c6ec6fc8acf8257006f8c0e0207c3e3",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "5efc25b523ae328d03339295037758c59665d67b",
  "no_merge": true,
  "checks": [
    {"command":"python3.12 -m unittest discover -s concept-verification/tests -v","result":"PASSED","details":"16 focused tests passed, covering reviewer/no-reviewer evaluation, malformed reviewer failure, acceptance harm/miss arithmetic, terminal-complete and incomplete SSE, both upstream path forms, non-200 forwarding, opt-in trace privacy, Codex command construction, and populated/empty review sheets.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"ruff check concept-verification","result":"PASSED","details":"Ruff 0.16.6 passed for the concept subtree.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"cd concept-verification && mypy --explicit-package-bases *.py eval/*.py","result":"PASSED","details":"Mypy 2.3.1 passed all 15 concept source modules in an owned locked /tmp environment.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/run_eval.py --phase heldout --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --frozen concept-verification/eval/frozen-experiment.json --reviewer-url REVIEWER_URL --reviewer-model qwen3.8-27b --reviewer-profile PRIVATE_PROFILE --results LOCAL_HELDOUT_FINAL","result":"FAILED","details":"The one allowed live reviewer sequence reached the ten selected candidates with one bounded sequential call each, then hit a post-evaluation detector-only aggregation-key exception before proposal/acceptance output was persisted. No second reviewer run was made.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/run_eval.py --phase heldout --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --frozen concept-verification/eval/frozen-experiment.json --results LOCAL_DETECTOR_ONLY","result":"PASSED","details":"After the live failure, a no-reviewer deterministic frozen detector record was produced without another model call: 145 eligible words, 7 known errors, 10 candidates, 1.00 recall, and 0.700 precision; reviewer/full fields remain NOT RUN.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/collect.py --cases 8 --codex-bin codex --codex-home PRIVATE_CODEX_HOME --profile qwen-neumann --provider-id qwen-LSI-A100 --proxy http://127.0.0.1:18024/v1 --trace-dir LOCAL_TRACE --work-root LOCAL_OWNED_WORK --results LOCAL_WORKLOAD_FINAL --timeout 120","result":"FAILED","details":"Exactly eight actual codex exec attempts were made once each; all exited 2 before contacting the proxy because the pre-fix builder passed unsupported --ask-for-approval. No traces, terminal events, or model outputs were produced. The builder is corrected in the implementation, but collection was not rerun.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD_FINAL --traces LOCAL_TRACE --output LOCAL_REVIEW_SHEET_FINAL","result":"BLOCKED","details":"No completed workload row had a joined trace, so no sheet was generated and no empty placeholder was accepted.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/score.py --controlled LOCAL_DETECTOR_ONLY/heldout.json --workload LOCAL_WORKLOAD_FINAL --traces LOCAL_TRACE --output concept-verification/eval/results/summary.json","result":"PASSED","details":"Computed aggregate is INCONCLUSIVE with detector-only metrics and zero completed workload traces; missing reviewer and human semantics remain explicit, not constants presented as quality.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"pytest -q --ignore=.venv","result":"PASSED","details":"340 existing tests passed in 311.99 seconds in an owned locked /tmp environment with project dependencies.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B -m unittest discover -s oap/tests -v","result":"PASSED","details":"104 OAP tests passed in 294.491 seconds.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"FAILED","details":"uv lock, frozen sync, focused contracts, full pytest, and Ruff passed; the earliest failure was the inherited application mypy check with 11 ZipInfo/stat_result type-shadow diagnostics in scripts/verify_source_artifact.py. No baseline path was changed.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-b","result":"PASSED","details":"Index transcript is valid at implementation head with active/latest 007-b and prior 007-a report preserved.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-b","result":"PASSED","details":"Committed transcript is valid at implementation head.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest","result":"PASSED","details":"Report history is valid with the two known frozen historical incidents only.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD","result":"PASSED","details":"Acquisition history is valid at cumulative count 14; no new archive GET was used in this round.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance structure is valid; semantic and human-authorization proofs remain false.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"protected diff against 5efc25b523ae328d03339295037758c59665d67b","result":"PASSED","details":"Protected product, script, test, governance-source, incident, resource, and frozen experiment input paths are byte-unchanged.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"source and built-wheel fresh-process lazy root imports","result":"PASSED","details":"Bare source and independently built-wheel imports load neither Pydantic nor HTTPX; wheel scan found no archive/database/private trace artifact.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"tracked/package/archive/credential-value scan","result":"PASSED","details":"No tracked archive/database/SSE/private trace artifact or credential value was found; controlled fixture evidence remained the only committed evaluation text.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"git diff --check 5efc25b523ae328d03339295037758c59665d67b...HEAD","result":"PASSED","details":"Implementation history has no whitespace errors.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs","result":"PASSED","details":"Repository object check passed; six preserved dangling historical blobs remain and were not cleaned.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"cache identities before/after and zero-GET validation","result":"PASSED","details":"Both owner-controlled archive identities match their fixed size/MD5/SHA-256; source-cache validation remained VERIFIED_REUSABLE with network_get_count 0 and no part file before and after.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false},
    {"command":"gh pr checks 8 --repo ulfe-lmi/llm-slovenian-repair","result":"FAILED","details":"At exact implementation head 0611001, OAP bootstrap acceptance and OAP report history PASS; inherited Application baseline FAILS. PR #8 is open, non-draft, and unmerged.","sha":"061100114c6ec6fc8acf8257006f8c0e0207c3e3","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-09T04:25:05+00:00",
  "report_written_at": "2026-09-09T04:26:00+00:00",
  "implementation": "Implemented the ordered concept-verification correction under concept-verification/**: real evaluator/reviewer plumbing with target evidence, strict acceptance and one apply_edits call per case; computed controlled ablations/metrics; terminal-complete buffered SSE capture; single /v1/responses normalization; non-200 forwarding; opt-in atomic privacy traces; actual Codex command construction; joined trace sheet validation; and computed scoring. The frozen inputs and protected product paths were unchanged. The live reviewer and workload boundaries remain PARTIAL because the one permitted runs were blocked as recorded.",
  "documentation": "README.md now contains exact reviewer-profile, proxy-trace, Codex-home/profile/provider, timeout, sheet, and score commands. concept-verification/REPORT.md records the computed detector evidence, live-attempt failures, six prior 007-a blocked cases as superseded only in interpretation, A-J answers, limitations, reuse, and INCONCLUSIVE status. Aggregate summary.json contains computed values and explicit missing states only.",
  "criteria": "PARTIAL: frozen detector evidence and all focused/protocol/governance checks pass; reviewer calls were attempted once per selected candidate but no proposal aggregate survived the bookkeeping defect; eight actual Codex attempts were bounded but blocked before proxy contact; no populated human sheet exists; no linguistic benefit, harm, natural-workload quality, merge, release, or deployment claim is made.",
  "negative_paths": "Focused tests cover malformed reviewer/error accounting, no-reviewer no-op, strict acceptance and harm/miss arithmetic, overlap/protection invariance, terminal-complete and incomplete SSE, comments/unknown blocks, /v1 normalization, non-200 status/content-type, trace-off/on privacy, fake Codex exit and command flags, and sheet refusal of empty or missing joined text. The first live failures were preserved as FAILED rather than retried or relabelled.",
  "boundary_fidelity": "Only concept-verification/**, the exact 007-b active/order paths, and PR #8 metadata were changed. The six frozen experiment identities, src/scripts/tests/uv.lock/PLAN/ARCHITECTURE/CRITICAL/resources, prior 007-a report, caches, service, GPU, network, gateway, ports, and deployment resources were not changed. PR #8 remains open and unmerged.",
  "setup": "The consumed durable marker, active pointer, branch, base, and existing PR #8 were reconciled as the same 007-b continuation. The exact frozen external index and owner-controlled archives were used read-only; temporary index, dependency environment, build artifacts, workload roots, traces, and failed-run diagnostics stayed outside Git. The stale assume-unchanged active-pointer index flag was cleared only to stage its delivered 007-b bytes.",
  "privacy": "No credential value, customer text, raw reviewer/Codex response, source row, token, reasoning, tool argument, or private trace was committed or placed in this OAP report. Tracing is opt-in and local; the blocked workload produced no traces. The committed controlled JSON contains only project-authored fixture-derived evidence and bounded metrics.",
  "limits": "The live reviewer sequence did not yield persisted proposals after its post-call aggregation exception, and the eight Codex cases exited before model/proxy execution due the pre-fix CLI option. The corrected collector command was not live-rerun because the order forbids a second final collection. The inherited application baseline remains red at 11 accepted-main verifier/mypy type-shadow diagnostics. Human benefit/harm, workload latency, tool-loop proof, semantic labels, production correctness, merge readiness, release, deployment, and milestone status remain unproven.",
  "human_gates": "D0/NONE and CRITICAL is empty. Human workload labels remain absent; no model self-review was treated as human review. Coding did not merge, enable auto-merge, adjudicate, select another suffix/objective, claim release/deployment authority, or append a critical entry.",
  "scope": "Finished only active order 007-b on the existing PR #8: one implementation commit 0611001, one bounded live reviewer attempt, one exactly-eight-case Codex attempt, computed detector-only fallback record, and this sole pending immutable SELF report. No 007-c or normal roadmap resumption is proposed. The final report commit changes only this exact report path, must have implementation 0611001 as its sole parent, and is followed by independent publication verification and exact OK.",
  "result_summary": "INCONCLUSIVE / PARTIAL. The one remaining discriminating action is strategic reconciliation of this truthful partial round; no further live experiment is authorized by coding."
}
```

## Result

007-b is a truthful partial correction. The detector and protocol boundaries are
implemented and verified, while the reviewer aggregate and real Codex workload
remain unavailable for the bounded reasons recorded above. The result is not a
production, merge, release, deployment, milestone, or natural-workload quality
claim.

## Deferred human adjudication

- Decision: NONE

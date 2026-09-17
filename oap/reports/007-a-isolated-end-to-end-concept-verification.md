# Work report 007-a — Isolated end-to-end concept verification

```oap-report
{
  "id": "007-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-a-isolated-end-to-end-concept-verification.md",
  "order_sha256": "e72a946ad5932195ff9140dc784242c177f9254068b638faebef9af1bc2c7441",
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
  "implementation_head": "2d793129582e6c660c46660b968b478fa2bbd1b2",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "no_merge": true,
  "checks": [
    {"command":"python3.12 -m unittest discover -s concept-verification/tests -v","result":"PASSED","details":"8 focused tests passed, including cache identity rejection, evidence states, protection, strict parser, exact patching, and fake SSE proxy round trip.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/perturb.py","result":"PASSED","details":"Deterministic dev count 16 and held-out count 32; JSONL identities recorded.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/corpus.py prepare --words-archive EXTERNAL_WORDS_ZIP --ngrams-archive EXTERNAL_NGRAMS_ZIP --output EXTERNAL_SQLITE","result":"PASSED","details":"Both external archive identities, selected members, headers, marker rows, fixed widths, CRLF, UTF-8, and bounded rows validated; derived SQLite remained external.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/run_eval.py --phase dev --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --results LOCAL_DEV","result":"PASSED","details":"Dev tuning evaluated two modes across four predeclared thresholds; 74 eligible words, 6 known errors, 7 candidates, recall 1.00, candidate precision 0.714.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/run_eval.py --freeze --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --output concept-verification/eval/frozen-experiment.json","result":"PASSED","details":"Frozen mode, threshold, prompt template hash, config, dataset, index, and decision thresholds were written before held-out execution.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/run_eval.py --phase heldout --config concept-verification/eval/config.json --index EXTERNAL_SQLITE --frozen concept-verification/eval/frozen-experiment.json --results LOCAL_HELDOUT","result":"PASSED","details":"Held-out identity checks passed; 145 eligible words, 7 known errors, 10 candidates, recall 1.00, candidate precision 0.700.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/collect.py --cases 8 --proxy http://127.0.0.1:18024/v1 --results LOCAL_WORKLOAD","result":"PASSED","details":"Eight bounded cases were attempted; two completed buffered SSE responses and six were explicitly blocked by endpoint/capture availability or upstream failure. Raw traces stayed local.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/score.py --controlled LOCAL_HELDOUT/heldout.json --workload LOCAL_WORKLOAD --output concept-verification/eval/results/summary.json","result":"PASSED","details":"Aggregate JSON is committed with decision INCONCLUSIVE and human status AWAITING_HUMAN_REVIEW; reviewer-dependent fields remain pending.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD --output LOCAL_REVIEW_SHEET","result":"PASSED","details":"Deterministic eight-row blinded sheet created with blank human labels.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"FAILED","details":"uv lock, frozen sync, focused contracts, full pytest, and Ruff passed; earliest failure was inherited script-inclusive mypy with 11 ZipInfo/stat_result type-shadow errors in scripts/verify_source_artifact.py. No weakening was made.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"UV_PROJECT_ENVIRONMENT=TEMP uv run --frozen --python 3.12 ruff check concept-verification","result":"PASSED","details":"All concept files pass Ruff 0.16.6.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"cd concept-verification && UV_PROJECT_ENVIRONMENT=TEMP uv run --frozen --python 3.12 mypy --explicit-package-bases *.py eval/*.py","result":"PASSED","details":"15 isolated concept source files pass mypy 2.3.1; the hyphenated directory is checked as a standalone experimental tree.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"pytest -q --ignore=.venv","result":"FAILED","details":"Direct system-interpreter collection failed for existing package tests because llm_slovenian_repair is not installed; the mandated disposable native baseline separately reached full pytest PASSED.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B -m unittest discover -s oap/tests -v","result":"PASSED","details":"104 OAP tests passed in 256.052 seconds.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-a","result":"PASSED","details":"Index transcript valid at implementation head with 007-a as sole unfinished current order.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-a","result":"PASSED","details":"Committed transcript valid at implementation head.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest","result":"PASSED","details":"Historical report-path guard valid; only the two frozen known incidents are surfaced.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD","result":"PASSED","details":"Cumulative acquisition history valid at 14; no new 007 archive fetch was used for index/evaluation.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance structure valid; semantic and human-authorization proofs remain false.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"git diff --exit-code bb8d9a0315081300ffaadc3ad392b169d51c8ad9 -- src scripts tests uv.lock PLAN.md ARCHITECTURE.md CRITICAL.md oap/REPORT-HISTORY-INCIDENTS.json resources","result":"PASSED","details":"Protected product, scripts, tests, governance source, incident, and resource paths are unchanged from preserved 006-m head.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"git diff --check bb8d9a0315081300ffaadc3ad392b169d51c8ad9...HEAD","result":"PASSED","details":"Implementation history has no whitespace errors.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs","result":"PASSED","details":"Repository object check passed; preserved dangling historical blobs were not cleaned.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"cache SHA-256/owner/link-count validation before and after evaluation","result":"PASSED","details":"Words remained 115865656 bytes, owner ubuntu, link count one, SHA-256 77ac4aa2; n-grams remained 22327366 bytes, owner ubuntu, link count one, SHA-256 782da9dd.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false},
    {"command":"gh pr checks 8 --repo ulfe-lmi/llm-slovenian-repair","result":"FAILED","details":"Observed at exact implementation head: OAP bootstrap acceptance PASS, OAP report history PASS, Application baseline FAIL at the inherited verifier/mypy contradiction.","sha":"2d793129582e6c660c46660b968b478fa2bbd1b2","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-09T03:12:40+00:00",
  "report_written_at": "2026-09-09T03:14:10+00:00",
  "implementation": "Implemented one isolated concept-verification vertical slice under concept-verification/. The verified loader, exact/censored/unavailable evidence, protected spans, deterministic detector, strict same-Qwen reviewer boundary, conservative acceptance, exact patcher, loopback buffered SSE proxy, frozen controlled evaluation, aggregate JSON, blank review sheet, and bounded workload collector are present. The implementation parent is 2d793129. The result is PARTIAL: controlled detector evidence and protocol proofs passed, but reviewer/full-pipeline evidence is incomplete and six of eight live workload cases were blocked.",
  "documentation": "README.md gives executable private-path commands and labels the subtree experimental/non-production. concept-verification/REPORT.md records design, protocol/model/source, ablations, metrics, harm, latency limits, A-J answers, reuse/shortcuts, and the INCONCLUSIVE decision. The aggregate JSON records config/dataset/index identities and pending human labels. No raw source rows, private responses, prompts, replacements, or credentials were documented.",
  "criteria": "PARTIAL: the proxy fake round trip and one owned disposable Codex tool-loop proof succeeded; a verified external index and frozen dev/held-out detector evidence ran with zero protected changes in focused tests; eight workload attempts were bounded with 2 complete and 6 blocked; reviewer-dependent accuracy, accepted/correct/harmful/missed edits and full recovery remain pending. Natural-workload quality is not GO.",
  "negative_paths": "Focused tests reject archive identity mismatch before member access, preserve EXACT/CENSORED/UNAVAILABLE semantics, reject malformed/contradictory reviewer JSON, protect code/URL/path/number/identifier slices, reject unsafe acceptance, preserve tool/non-text/ID/usage SSE fields, and refuse held-out frozen identity mismatches. The corrected live collector request shape and total upstream capture bound were the one permitted material corrective round; no further live cycling occurred.",
  "boundary_fidelity": "The implementation commit changes only concept-verification/**, exact oap/active 007-a, and the exact 007-a order. Protected src/scripts/tests/uv.lock/PLAN/ARCHITECTURE/CRITICAL/resources/OAP history paths are byte-unchanged from bb8d9a. No service, GPU, port, gateway, VPN, deployment, release, or closed PR #7 was changed. PR #8 remains open and unmerged.",
  "setup": "The wrapper-consumed durable marker identified 007-a with recovery false; the explicit new branch was reconciled from bb8d9a and no prior 007 branch/PR existed. The delivered active pointer had an index stat-cache anomaly; its exact 007-a bytes were restaged before the implementation commit. External caches stayed in the owner-selected strategic cache. Live profile credentials were read only in memory. Temporary SQLite, traces, review sheet, and disposable tool-loop directories stayed outside Git.",
  "privacy": "No credential values, customer data, raw model responses, source rows, prompts, replacements, or private traces entered Git, OAP reports, logs, or metric labels. The committed controlled cases are project-authored synthetic data. The two completed live traces and six blocked-case diagnostics remained local and were summarized only as bounded aggregate states.",
  "limits": "The inherited Application baseline remains red because accepted-main scripts/verify_source_artifact.py has 11 ZipInfo/stat_result mypy type-shadow errors; no production verifier or test was altered. Direct system pytest was not a valid installed-package environment, while the mandated disposable baseline full pytest passed. Reviewer-dependent ablations, complete live-workload latency/edit metrics, human labels, linguistic benefit, merge readiness, release, deployment, milestone, and production reuse remain unproven.",
  "human_gates": "D0/NONE. CRITICAL is empty. The real-workload sheet is AWAITING_HUMAN_REVIEW and no model self-review was treated as a human label. Coding did not merge, enable auto-merge, adjudicate, select follow-on scope, claim release/deployment authority, or append a critical entry.",
  "scope": "Finished only active order 007-a: one isolated implementation/evaluation round, one permitted corrective round for request shape and finite capture, one new PR #8, and this pending immutable report publication. No suffix or new objective was created. Final report publication changes only this exact report path; after publication verification, coding sends OK and exits with no later mutation."
}
```

## Result

007-a is a truthful partial concept-verification result. The isolated implementation
is usable for further human review, but the automatic evidence does not support a
GO/PROMISING or natural-workload quality claim. The aggregate decision is
`INCONCLUSIVE`; the only next discriminating action is attributable human review of
the blank blinded sheet.

## Deferred human adjudication

- Decision: NONE

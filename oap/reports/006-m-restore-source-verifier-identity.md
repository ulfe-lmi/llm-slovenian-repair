# Work report 006-m — Restore objective-005 verifier identity

```oap-report
{
  "id": "006-m",
  "result": "FAILED",
  "order_path": "oap/orders/006-m-restore-source-verifier-identity.md",
  "order_sha256": "30f0d50dcfc96d9014b4d2e9c207e88a26dc69b6f6f00ca2ec0abcd5aa0cac61",
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
  "implementation_head": "38a753df9fc870cd63bafb200c1ff65e9d66c730",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "53defa605970b6413f44f9e3d477f08247469c1c",
  "no_merge": true,
  "checks": [
    {"command":"pytest tests/contract/test_objective_005.py -q","result":"PASSED","details":"40 tests passed in the system interpreter.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"pytest tests/contract/test_objective_006.py -q","result":"FAILED","details":"System-interpreter collection failed because llm_slovenian_repair was not installed; the owned baseline reached full pytest before the later mypy stop.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"pytest tests/contract/test_objective_006_diagnostics.py -q","result":"PASSED","details":"24 tests passed in the system interpreter.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"pytest tests/contract/test_objective_006_smoke.py -q","result":"FAILED","details":"23 tests passed; isolated preflight failed with preflight-dependency-unavailable in the system interpreter.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"FAILED","details":"uv lock --check, frozen dependency sync, focused contract tests, full pytest, and Ruff passed in owned locked environments; the first failure was mypy. It reported 11 accepted-main type-shadow errors in scripts/verify_source_artifact.py at lines 618-636: ZipInfo was assigned to a stat_result-typed info variable, followed by stat_result attribute errors. The runner stopped before OAP unittest discovery, build, and offline wheel probes.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/source_cache.py validate --strategic-home OAP_STRATEGIC_HOME (first)","result":"PASSED","details":"VERIFIED_REUSABLE, generation 77ac4aa2, network_get_count 0, no part file; output contained only bounded metadata and counts.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/source_cache.py validate --strategic-home OAP_STRATEGIC_HOME (second)","result":"PASSED","details":"VERIFIED_REUSABLE, same generation, network_get_count 0, no part file.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 006-m","result":"PASSED","details":"Active/order transcript valid through 006-m with 006-m as the sole unfinished current order.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-m","result":"PASSED","details":"Committed transcript valid at the implementation head.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest","result":"PASSED","details":"All normal report paths are add-once; only frozen RHI-0001 and RHI-0002 are surfaced.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD","result":"PASSED","details":"Cumulative GET count remains 14 with no history rewrites.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance structure valid; semantic and human-authorization proofs remain false.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- scripts/verify_source_artifact.py resources/source-inventory-v1.json","result":"PASSED","details":"Restored verifier and source inventory are byte-identical to accepted main; restored verifier content SHA-256 is 90a806331e4b2ae45dc2b1c911d4e27cd0f5ed4da5c12f12e5ae056dd5bcf4e7.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"git diff --exit-code 53defa605970b6413f44f9e3d477f08247469c1c -- src tests uv.lock oap/REPORT-HISTORY-INCIDENTS.json resources/source-acquisitions oap/orders/006-a-unigram-lexicon-importer.md oap/reports/006-g-commit-and-run-verified-unigram-smoke.md","result":"PASSED","details":"Protected product, test, lock, incident, source-acquisition, prior-order and immutable 006-g paths are unchanged.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD","result":"PASSED","details":"Implementation history has no whitespace errors.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs","result":"PASSED","details":"Only preserved dangling blob bbca830666fc43fb89081d1c5a11cf1c5e37f606 was reported; no cleanup was performed.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"006-g immutable report byte comparison","result":"PASSED","details":"Accepted and current 006-g content SHA-256 both equal 0381e907dc4595c95a2809e498435002b471baca271fe75f151eb52fb60ff9d3.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"GitHub PR #7 metadata and body invariant","result":"PASSED","details":"PR #7 is open, non-draft and mergeable at 38a753df; body has real Markdown newlines, current 006-m wording, concept-first priority, cumulative fourteen GETs, and no-merge/release/deployment claims.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"GitHub Application baseline at 38a753df","result":"FAILED","details":"Exact implementation head check failed, consistent with the local accepted-main verifier type-shadow failure.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"GitHub OAP bootstrap acceptance at 38a753df","result":"PASSED","details":"Exact implementation head check passed.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"GitHub OAP report history at 38a753df","result":"PASSED","details":"Exact implementation head check passed.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"pytest tests/contract/test_objective_001.py -q; pytest tests/contract/test_objective_003.py -q; pytest tests/contract/test_objective_004.py -q; pytest tests/contract -q; pytest -q --ignore=.venv","result":"NOT RUN","details":"The owned baseline covered focused objective-001 and full pytest successfully before the first mypy failure; these standalone commands were not run after the mandated stop.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"ruff check src scripts tests; mypy src scripts tests; python3 -B -m unittest discover -s oap/tests -v","result":"NOT RUN","details":"Ruff passed inside the owned baseline; the explicit standalone sequence and OAP unittest discovery were not run after the first mypy failure.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"direct source import and independently built-wheel fresh-process probes","result":"NOT RUN","details":"The baseline stopped before build/offline wheel stages at the first mypy failure; no wheel was built for this round.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false},
    {"command":"archive/package scan","result":"NOT RUN","details":"No new archive or package artifact was produced or scanned after the first-failure stop; prior retained-cache/package evidence was not mutated.","sha":"38a753df9fc870cd63bafb200c1ff65e9d66c730","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-09T01:36:54+00:00",
  "report_written_at": "2026-09-09T01:37:17+00:00",
  "implementation": "Restored scripts/verify_source_artifact.py byte-for-byte from accepted main ee2d1b4, including the accepted local variable name info. Committed the restoration with the delivered 006-m order and active pointer at 38a753df. The earliest authoritative verification failure is mypy's accepted-main type shadow: archive.infolist() assigns ZipInfo to the earlier stat_result-typed info variable, producing 11 errors at lines 618-636. The order required stopping there; the rename was not reintroduced and no check or test was weakened.",
  "documentation": "Updated PR #7 body through GitHub metadata only to 006-m, recording exact restoration, inaccurate immutable 006-g attribution (21e053d9 introduced the rename, not b7bd642), bounded failure status, concept-first priority, cumulative fourteen GETs, retained verified cache, and no merge/release/deployment claim. Product documentation and all prior reports/orders/receipts remain unchanged.",
  "criteria": "FAILED: verifier and source inventory identity restoration passed, protected paths and immutable 006-g remained unchanged, cache reuse and OAP integrity checks passed, and two OAP remote checks were green. The required application baseline failed at the first mypy boundary, so the report cannot claim complete verification or a merge-ready green head.",
  "negative_paths": "Objective-005 artifact tests passed 40/40 and objective-006 diagnostics passed 24/24. The system objective-006 collection lacked the installed package and the system smoke run had one isolated dependency-unavailable failure; owned full pytest passed before the baseline stopped at mypy. No verifier rename-back, type suppression, test weakening, source/cache cleanup, or report-history mutation was performed.",
  "boundary_fidelity": "The restored verifier and source inventory match accepted main exactly. The retained external generation validated twice as VERIFIED_REUSABLE with zero network GETs and no part file; acquisition history remains cumulative fourteen. No archive was fetched, cache was consumed or changed, wheel was built, live service/model was contacted, or protected deployment resource was touched in this round.",
  "setup": "The consumed marker identified 006-m with recovery false; prior 006-l report 53defa6 was independently remote-verified before mutation. The delivered active/order handoff was reconciled, its Git stat-cache anomaly was corrected by restaging the exact bytes, and implementation commit 38a753df was pushed to the existing PR #7 branch. Owned temporary baseline paths were under /tmp and its cleanup passed.",
  "privacy": "Reports and command summaries contain only bounded identities, hashes, finite states, counts, logical paths and failure reasons. No source rows, raw archive values, private cache absolute path, customer text, prompts, model responses or credentials were emitted or retained.",
  "limits": "The exact restoration is not application-baseline green because accepted-main verifier identity conflicts with the current mypy type analysis. Remaining standalone tests, OAP unittest discovery, wheel/fresh-process probes, archive/package scan and any further code verification were stopped at that first failure. No product linguistic benefit, full-index correctness, live-Qwen quality, merge readiness, release, deployment or milestone claim is made.",
  "human_gates": "D0/NONE. CRITICAL is empty. The known accepted-main type-shadow contradiction is reported for strategic/owner disposition; coding did not invent a correction. Strategic review owns the failed PR head and any future decision; no merge or auto-merge was performed.",
  "scope": "Only the activated 006-m order/active transcript paths, scripts/verify_source_artifact.py, this new report, and PR #7 REST metadata were changed. The implementation commit has the restored verifier as its only product-file change; the report is the sole pending SELF publication. PR #7 remains open and unmerged. No next objective was selected."
}
```

## Result

006-m restores the accepted objective-005 verifier identity and publishes the
earliest mandated verification failure. Accepted-main bytes are preserved, but
the required baseline is not green because the restored `info` variable shadows
the later ZIP member type under mypy. The immutable 006-g report is unchanged;
its attribution of that rename to `b7bd642` is inaccurate, while its bounded
smoke/failure facts remain usable.

## Deferred human adjudication

None. The order’s deferred human adjudication is `Decision: NONE`.

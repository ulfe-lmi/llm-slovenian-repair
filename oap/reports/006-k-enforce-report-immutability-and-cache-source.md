# Work report 006-k — Enforce report immutability and cache source

```oap-report
{
  "id": "006-k",
  "result": "PARTIAL",
  "order_path": "oap/orders/006-k-enforce-report-immutability-and-cache-source.md",
  "order_sha256": "e88210594b87c004d4b8d8c1b0688617716bc01ea83acabd4f489585344893a2",
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
  "implementation_head": "fb057b3cf98c509ba84ffbbd8122995d62e7f2e9",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "2bc6007ec67ca3f58682cb3c14ac61a6545c0bb3",
  "no_merge": true,
  "checks": [
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"PASSED","details":"Final-head native baseline passed lock check, frozen sync, focused and full pytest, Ruff, mypy, OAP unittest discovery, builds, offline runtime closure, and cleanup.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"PYTHONPATH=oap/bin python3 -B -m unittest discover -s oap/tests -p test_report_history_cache.py -q","result":"PASSED","details":"Seven synthetic report-history/cache boundary tests passed, including hardlink-unavailable promotion fallback.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-k","result":"PASSED","details":"Committed transcript is coherent with 006-k active and 006-j as the latest completed report before this publication.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest","result":"PASSED","details":"All normal report paths are add-once; only exact RHI-0001 and RHI-0002 are explicit frozen historical violations.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"python3 oap/bin/acquisition_history.py --repo-root . --revision HEAD","result":"PASSED","details":"Legacy cumulative count 12 and current blocked-generation receipt count 1 are monotonic; no receipt rewrite or accidental refetch is present.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"python3 oap/bin/source_cache.py plan --strategic-home OAP_STRATEGIC_HOME","result":"PASSED","details":"Cache state is MISSING after exact failed-promotion-part cleanup; plan requires a fetch and performs zero network GETs.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"PYTHONPATH=src pytest -q --ignore=.venv","result":"FAILED","details":"Exploratory system-environment run reached 306 passed and four dependency-isolation failures; the authoritative final-head native baseline passed all equivalent stages.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"curl --disable --fail --proto =https --tlsv1.2 --max-filesize 115865656 --output fixed-part","result":"PASSED","details":"The one ordered direct GET produced the expected 115865656-byte archive identity; no retry was attempted.","sha":"00ce249e581ab2907ed5e8f8f7cfb52f6d9f4a20","publication_head_claim":false},
    {"command":"python3 oap/bin/source_cache.py promote --strategic-home OAP_STRATEGIC_HOME","result":"FAILED","details":"Canonical artifact verification passed, then hard-link promotion failed on the selected sync filesystem. The exact part was removed; fallback code was corrected and synthetic-tested, but re-fetch is forbidden in this round.","sha":"00ce249e581ab2907ed5e8f8f7cfb52f6d9f4a20","publication_head_claim":false},
    {"command":"python3 oap/bin/source_cache.py repair --strategic-home OAP_STRATEGIC_HOME","result":"PASSED","details":"Removed only the exact failed part after bounded root validation; no archive remains in the cache.","sha":"00ce249e581ab2907ed5e8f8f7cfb52f6d9f4a20","publication_head_claim":false},
    {"command":"git diff --check fb057b3cf98c509ba84ffbbd8122995d62e7f2e9..HEAD","result":"PASSED","details":"No post-implementation working-tree diff or whitespace error before report composition.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"git diff --exit-code fb057b3cf98c509ba84ffbbd8122995d62e7f2e9..HEAD -- src resources/source-inventory-v1.json scripts/verify_source_artifact.py uv.lock","result":"PASSED","details":"Product source, source inventory/verifier identities, and lock are unchanged after implementation.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs --no-progress","result":"PASSED","details":"Repository object integrity completed without diagnostics.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"GitHub Actions Application baseline at fb057b3","result":"PASSED","details":"Final-head required remote check completed successfully.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"GitHub Actions OAP bootstrap acceptance at fb057b3","result":"PASSED","details":"Final-head required remote check completed successfully.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"GitHub Actions OAP report history at fb057b3","result":"PASSED","details":"Final-head history-enforcing CI check completed successfully.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false},
    {"command":"Strategic gate dry validation","result":"BLOCKED","details":"Not run under coding authority; the helper requires OAP_ROLE=strategic. Remote required checks and the coding-side history evidence are recorded above.","sha":"fb057b3cf98c509ba84ffbbd8122995d62e7f2e9","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T23:51:38+00:00",
  "report_written_at": "2026-09-08T23:53:35+00:00",
  "implementation": "The implementation head adds hard-bound Git-history enforcement for report paths, strict RHI-0001/RHI-0002 identity validation, transcript/report integration, the named history CI job, explicit cache lifecycle/policy, acquisition-history validation, receipt 006-k, sync-filesystem promotion fallback, and synthetic negative tests. Three implementation commits (00ce249, 41583f6, fb057b3) are on the existing PR branch. src/**, numeric importer semantics, source inventory/verifier identities, protected governance, and neighboring resources were unchanged.",
  "documentation": "README.md, STATUS.md, docs/DATA-SOURCES.md, docs/DEVELOPMENT.md, and docs/OAP-RUNBOOK.md document frozen report incidents, history enforcement, cache lifecycle, exact twelve-plus-one GET accounting, retention limits, and the blocked promotion outcome. Generated projections were updated and verified. PR #7 metadata has readable newlines and a current 006-k summary.",
  "criteria": "PARTIAL: report immutability and exact frozen-incident enforcement pass; real temporary Git-history negatives pass; acquisition history passes; final native baseline and all three remote checks pass. The canonical cache generation was fetched and verified, but promotion failed at the sync filesystem hard-link boundary, the exact part was removed, and the order forbids a second GET. Cache establishment, two cache consumers, and 006-j cache consumption therefore remain incomplete.",
  "negative_paths": "Synthetic tests cover published-report modification, deletion/recreation, actual-parent/path-only violations, new corrective suffix success, unexpected cache files, missing cache, hardlink-unavailable promotion fallback, and exact incident identity enforcement. Receipt validation rejects rewrites, accidental refetch, malformed generation/count state, private data, and stale cache states. The blocked live cache path is preserved as FAILED rather than normalized to success.",
  "boundary_fidelity": "The one direct GET was bounded to the canonical source and expected size. Existing inventory verification passed before promotion. Promotion initially failed because the selected sync filesystem rejected hardlinks; the exact part was removed through the fixed-root repair path. The corrected atomic-rename fallback is covered by an offline synthetic fixture, but cannot be exercised against the discarded external bytes without a prohibited second GET. No live Qwen, service, GPU, gateway, network configuration, or deployment boundary was changed.",
  "setup": "The authoritative final-head Python 3.12 lock-derived baseline used an owned /tmp environment and passed cleanup. The external cache root remains present as an empty owner-approved objective directory with no final, part, metadata, archive, or source rows. No repository .venv, archive, wheel, or built source data was retained by this round.",
  "privacy": "Reports and receipts contain only bounded identities, digests, counts, states, finite failure reasons, and protocol facts. No source rows, raw values, private cache absolute path, credentials, prompts, responses, or customer text was emitted or retained. Redistribution remains false.",
  "limits": "Report guard scans full reachable Git history for every oap/reports Markdown path. The acquisition receipt binds legacy cumulative GETs 12 and current network_get_count 1/cumulative 13. Cache plan now reports MISSING with network_get_count 0. No retry, second GET, cache consumer, concept experiment, numeric parser change, full import, linguistic benefit, release, or deployment evidence is claimed.",
  "human_gates": "D0/NONE. CRITICAL is empty. Human-owned merge, semantic review, concept-verification interpretation, milestone, release, deployment, live-Qwen, redistribution, and future numeric scope remain gated and were not exercised.",
  "scope": "Only activated order 006-k, active state, report-history guard, cache/acquisition infrastructure and tests, receipt 006-k, current scoped docs/generated projections, PR metadata, and this report are in scope. PR #7 remains open and unmerged. The truthful result is PARTIAL because cache establishment was blocked after the one allowed GET; no later order was assigned or self-selected."
}
```

The round is published as PARTIAL: process-integrity enforcement is complete and
verified, while the external cache objective is blocked at promotion after the
single permitted acquisition. Strategic review owns the remaining disposition.

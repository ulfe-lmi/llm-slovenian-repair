# Work report 006-l — Complete cache promotion and history negatives

```oap-report
{
  "id": "006-l",
  "result": "COMPLETE",
  "order_path": "oap/orders/006-l-complete-cache-promotion-and-history-negatives.md",
  "order_sha256": "cb840a4b0b55b84dee1a44f10045e3156f04b5bcd1d1ef99e214667de4cd1220",
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
  "implementation_head": "03385088fd3aa77e940529234cf8592a67da7bcb",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "98f26097ebe5f848d700e9de308aada1eeae5cfa",
  "no_merge": true,
  "checks": [
    {"command":"PYTHONPATH=oap/bin python3 -B -m unittest discover -s oap/tests -p 'test_report_history_cache.py' -v","result":"PASSED","details":"Twenty focused history/cache/acquisition tests passed, including atomic-rename, post-verification cleanup, digest/metadata/type/owner/lifecycle negatives, implementation-head drift, same-path repair, manifest exception, frozen-incident third touch, monotonic receipt count, and accidental refetch rejection.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"PASSED","details":"Owned temporary Python 3.12/uv baseline passed lock check, frozen sync, focused/full pytest, Ruff, mypy, all OAP tests, sdist/wheel build, offline runtime closure, isolated imports, and cleanup.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 006-l","result":"PASSED","details":"Indexed active/order transcript is coherent through 006-l with no current report yet.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-l","result":"PASSED","details":"Committed transcript is coherent through 006-l and preserves 006-k as the latest completed report before this SELF publication.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest","result":"PASSED","details":"All normal report paths are add-once; only exact RHI-0001 and RHI-0002 are surfaced as frozen historical violations.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD","result":"PASSED","details":"Legacy twelve, immutable blocked 006-k one, and immutable 006-l one bind cumulative fourteen; prior receipt is untouched and no accidental refetch is present.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/source_cache.py plan --strategic-home OAP_STRATEGIC_HOME","result":"PASSED","details":"Retained canonical generation plans REUSE with zero network GETs.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/source_cache.py validate --strategic-home OAP_STRATEGIC_HOME","result":"PASSED","details":"Final is owner-controlled, regular, link-count one, canonical size/MD5/SHA-256, inventory-verified, and VERIFIED_REUSABLE.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"owned cache validation plus content-free 006-j diagnostic twice","result":"PASSED","details":"One owned dependency interpreter ran two sequential diagnostics against the retained final; both returned BLOCKED_NUMERIC_DIAGNOSTIC_IMPORT with 32 rows and 768 numeric cells, byte-identical safe results, and validation passed before and after each consumer.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance and protected source identities are valid; semantic and human-authorization proof remain false.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"git diff --exit-code 98f26097ebe5f848d700e9de308aada1eeae5cfa -- src resources/source-inventory-v1.json scripts/verify_source_artifact.py uv.lock oap/REPORT-HISTORY-INCIDENTS.json","result":"PASSED","details":"Product source, source inventory/verifier, dependency lock, and historical incident register are unchanged from the round start.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"git diff --check 98f26097ebe5f848d700e9de308aada1eeae5cfa...HEAD","result":"PASSED","details":"Implementation history has no whitespace errors.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs","result":"PASSED","details":"Only preserved pre-existing dangling blob bbca830666fc43fb89081d1c5a11cf1c5e37f606 was reported; no cleanup was performed.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"system-interpreter objective contract collection","result":"FAILED","details":"Initial direct system-environment collection lacked the installed package; the PYTHONPATH retry reached 216 passed but four expected dependency-isolation failures. The authoritative owned final baseline passed all equivalent stages.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"GitHub Actions Application baseline at 03385088","result":"PASSED","details":"Observed final-head required check passed at implementation head before report composition.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"GitHub Actions OAP bootstrap acceptance at 03385088","result":"PASSED","details":"Observed final-head required check passed at implementation head before report composition.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"GitHub Actions OAP report history at 03385088","result":"PASSED","details":"Observed final-head history-enforcing check passed at implementation head before report composition.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"GitHub PR #7 metadata and body invariant","result":"PASSED","details":"PR #7 is open, non-draft, mergeable, on the expected branch at 03385088; body has real newlines, current 006-l wording, and concept-first priority.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"GitHub main protection/ruleset observation","result":"PASSED","details":"Legacy branch protection endpoint returned not-found; active ruleset 22590837 was observed. No settings changed.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false},
    {"command":"Strategic gate","result":"BLOCKED","details":"Not run under coding authority; strategic review owns semantic merge adjudication. No merge, auto-merge, release, deployment, milestone, live-Qwen, or production action was taken.","sha":"03385088fd3aa77e940529234cf8592a67da7bcb","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-09T00:53:55+00:00",
  "report_written_at": "2026-09-09T00:55:23+00:00",
  "implementation": "The cache helper now performs one lock-protected same-directory os.replace of a verified part, flushes/fsyncs where supported, reopens and re-verifies the final, writes exclusive metadata, and requires a final VERIFIED_REUSABLE inspect. Expected rename, post-verification, and metadata failures clean only fixed cache artifacts; hardlink promotion and broad exception catches are absent. Acquisition history binds 006-k plus 006-l and rejects non-monotonic or accidental refetch receipts. Product src/**, importer/numeric semantics, source inventory/verifier identities, dependency lock, incident register, Qwen/GPU/services, and protected governance were unchanged.",
  "documentation": "README.md, STATUS.md, docs/DATA-SOURCES.md, docs/DEVELOPMENT.md, and docs/OAP-RUNBOOK.md describe the 006-k failed hardlink boundary, 006-l rename-only promotion, offline validation/reuse, retention/lifecycle gate, cumulative fourteen GET accounting, and concept-first handoff. Generated projections were refreshed and verified. Receipt 006-l is immutable and 006-k was not edited. PR #7 metadata was updated through REST only.",
  "criteria": "COMPLETE: atomic rename promotion and post-rename identity binding pass; two sequential content-free consumers and three validations reuse one canonical generation with zero further GETs; requested report-history/cache/acquisition negatives pass; cross-objective/protected checks, owned baseline, fsck, PR metadata, and all three final-head CI checks pass. This completes the cache/process correction only and does not certify product linguistic benefit or release readiness.",
  "negative_paths": "Focused tests pass corrupt size/MD5/SHA-256, stale/duplicate metadata, symlink, hardlink, nonregular, wrong-owner, wrong-root isolation, unexpected file, overwrite, rename/verification/metadata cleanup, invalid repair, lifecycle-gated cleanup, no os.link invocation, and os.replace boundary. Git-history tests pass implementation-head drift, same-path invalid repair, manifest exception rejection, exact frozen-incident recognition, third-touch rejection, and new-suffix success. Acquisition history rejects receipt rewrites, non-monotonic counts, and accidental refetch without exact invalid/missing deletion.",
  "boundary_fidelity": "The sole new archive GET was made only after MISSING/FETCH_REQUIRED planning, directly to the canonical fixed URL with the fixed size bound and no retry. The archive passed canonical inventory/ZIP verification, atomic rename, post-rename re-verification, exclusive metadata, and final inspection. The retained final was consumed twice by the existing content-free diagnostic and revalidated three times. No archive/part/cache file entered Git, the repository, a wheel, or package output; the external final remains owner-controlled until concept-experiment completion.",
  "setup": "Work resumed the consumed same ID on the existing PR #7 branch after reconciling active 006-l, its filename-digest immutable lock, consumed marker, local/remote head, and open PR. All temporary dependency environments and outputs were owned under /tmp and cleaned by the baseline; the external cache is retained only at its exact owner-selected strategic subtree. The preserved dangling blob was not removed.",
  "privacy": "Reports, receipt, logs, and command summaries contain only bounded identities, digests, finite states, counts, paths expressed as approved logical names, and failure reasons. No source rows, raw values, private cache absolute path, customer text, prompts, responses, credentials, or redistribution material was emitted or retained.",
  "limits": "The cache proof is one bounded archive acquisition, two sequential content-free diagnostic consumers, and three validations; the diagnostic remains blocked at the known numeric parser boundary and is not product or linguistic evidence. The system-interpreter exploratory failures were setup-only and are superseded by the passing owned baseline. No live test, Qwen run, full real import, numeric refinement, semantic acceptance, merge, release, deployment, or milestone claim is made.",
  "human_gates": "D0/NONE. CRITICAL is empty. Strategic review owns PR #7 semantic review and any development merge; concept-verification interpretation, product meaning, human annotation, milestone acceptance, release, deployment, live-Qwen, and redistribution remain human-gated.",
  "scope": "Only activated order 006-l, active/order/report transcript paths, cache/acquisition infrastructure and focused tests, 006-l receipt, current scoped documentation/generated projections, and PR #7 REST metadata were changed. PR #7 remains open and unmerged. This report is the sole SELF publication commit for implementation head 03385088; no later round was assigned or self-selected."
}
```

## Result

006-l completes the ordered cache promotion, reusable-generation, acquisition-history,
and report-history-negative correction on PR #7. Strategic review remains responsible
for semantic review and any development-only merge decision.

## Deferred human adjudication

None. The order’s deferred human adjudication is `Decision: NONE`.

# Work report 006-a — Unigram/lexicon importer

```oap-report
{
  "id": "006-a",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-a-unigram-lexicon-importer.md",
  "order_sha256": "31ee71c0affe2610a23e37c3b20f3eeea9b35b6b2576ef0619c6f6fd950365b3",
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
  "implementation_head": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "no_merge": true,
  "checks": [
    {
      "command": "python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --validate-only",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "24 passed",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "121 passed",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 pytest tests/contract -q",
      "result": "PASSED",
      "details": "145 passed",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 pytest -q",
      "result": "PASSED",
      "details": "229 passed in 124.63s",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-venv uv run --frozen --python 3.12 mypy src tests",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "84 tests",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "all 13 baseline stages passed; cleanup PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-a",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-a",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34221764849)",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34221764864)",
      "result": "PASSED",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification for PR #7",
      "result": "PASSED",
      "details": "remote head 4f3c3d66dbc8c48b6445e973e3ada61bafb131b5; PR open, merge state CLEAN",
      "sha": "4f3c3d66dbc8c48b6445e973e3ada61bafb131b5",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T13:41:11+02:00",
  "report_written_at": "2026-09-08T13:41:23+02:00",
  "implementation": "Added src/llm_slovenian_repair/unigram_importer.py with frozen extra-forbid provenance, limits, record, result, and summary types; strict all-fields-quoted 28-column parsing; incremental bounded stream reading; exact source-field retention; Decimal-backed lossless numeric views; NFC_CASEFOLD derived lookup; completeness-aware zero handling; stable morphology composite keys; deterministic input/output hashes; and finite non-content failure labels. Exported the seam lazily without changing import-time dependency/network behavior.",
  "documentation": "Updated README.md, STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md with the implemented parser boundary and explicit recovery limitation. Added a schema-only source-acquisition receipt with no row values or retained archive. Reconciled generated-document and installation inventory hashes and the installed-package export allowlist. Added project-authored synthetic fixture documentation and contract tests.",
  "criteria": {
    "1_source_fetch_verification_smoke_cleanup": "BLOCKED: durable recovery state records three prior GETs, violating the order's exact-one-fetch condition. The current context made no source request; no archive remains; current accepted offline verification of a temporary archive and real importer smoke are NOT RUN. Cleanup is PASSED for the recorded absent temporary tree. No real format-compatibility acceptance claim is made.",
    "2_synthetic_import": "PASSED: synthetic import is deterministic, retains exact and derived Unicode separately, preserves two analyses for one form, and accepts zero only with COMPLETE query metadata.",
    "3_negative_paths": "PASSED: focused tests cover malformed count variants and overflow, partial zero, invalid UTF-8/control/surrogate, malformed decimal, wrong header/columns/quoting, missing or non-CRLF newline, duplicate/conflicting key, and byte/line/field/row limits.",
    "4_provenance_summary": "PASSED: immutable summary binds source inventory revision/hash, acquisition hash, member/header contract, importer version, normalization, independent completeness states, limits, record count, and input/output hashes without upgrading samples to complete evidence.",
    "5_preservation_and_checks": "PASSED for offline implementation, package, governance, transcript, and required CI checks: no external row/archive is committed or packaged; PR #7 remains open and unmerged. Real-source criterion remains blocked as stated above."
  },
  "negative_paths": "The 24 focused tests exercise the actual parser entry point with synthetic bytes/text, including controls and surrogate input, strict quoted TSV structure, exact CRLF termination, resource ceilings, duplicate identity behavior, and immutable deterministic results. No fake replaces the parser boundary.",
  "boundary_fidelity": "Only active order 006-a, its matching order file, importer/package assertions, importer implementation, synthetic fixture/tests, schema-only recovery receipt, direct docs, generated/installation metadata, and this report path were changed. PLAN, architecture, CRITICAL, source inventory facts, dependencies, Qwen/GPU/services, gateway, network settings, neighboring repositories, release, deployment, and merge state were not changed. The recovery handoff remains untracked and is not part of the report publication.",
  "setup": "The invalid ignored repository .venv was preserved unchanged. Verification used the committed uv.lock, a fresh owned /tmp environment, bounded temporary test/build roots, and cleanup verified by the native baseline. No live model, customer data, credentials, source archive, or external row was used by this context.",
  "privacy": "No source rows, raw external text, prompts, model responses, customer text, credentials, secrets, or private strategic contents were logged, committed, or placed in the report. The receipt retains only source metadata, hashes, schema names, bounded counts, and recovery-status facts.",
  "limits": "The recovery handoff is not current independent source evidence. Three prior GETs make the exact-one-fetch acceptance unavailable for this round; no real importer output hash or sample count is claimed. The implementation is a parser seam only, not a detector, index, quality result, legal/redistribution decision, milestone acceptance, release, or deployment authorization. `publication_verified` is false until the separate report publication verification step.",
  "human_gates": "Decision class D0 and deferred adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains publication review and development-merge authority, while human intent, rights, release, and deployment authority remain unchanged.",
  "scope": "Executed only active order 006-a. Non-report work/order/active is committed and pushed as 4f3c3d66dbc8c48b6445e973e3ada61bafb131b5. This report is intended to be the sole final commit with that implementation head as its sole parent; publication verification and the exact OK response occur only after this report is pushed and independently verified."
}
```

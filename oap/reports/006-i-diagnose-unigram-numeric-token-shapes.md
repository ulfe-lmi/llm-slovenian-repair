# Work report 006-i — Diagnose unigram numeric token shapes

```oap-report
{
  "id": "006-i",
  "result": "COMPLETE",
  "order_path": "oap/orders/006-i-diagnose-unigram-numeric-token-shapes.md",
  "order_sha256": "563aba1859c67d29241e90ead34b63ed93f3a3eb166ba13908f51fd0cba2555d",
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
  "implementation_head": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
  "no_merge": true,
  "checks": [
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "40 focused objective-005 contract tests passed from the repository root with PYTHONPATH absent.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "51 focused objective-006 importer tests passed; importer semantics remain unchanged.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest tests/contract/test_objective_006_diagnostics.py -q",
      "result": "PASSED",
      "details": "21 numeric and structural diagnostic tests passed, including every closed category and priority overlap.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest tests/contract/test_objective_006_smoke.py -q",
      "result": "PASSED",
      "details": "22 smoke, CLI-mode, receipt, isolation, and one-importer-call tests passed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest tests/contract -q",
      "result": "PASSED",
      "details": "215 contract tests passed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m pytest -q --ignore=.venv",
      "result": "PASSED",
      "details": "299 tests passed in the full repository suite.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m ruff check src scripts tests",
      "result": "PASSED",
      "details": "Ruff checks passed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -m mypy src tests",
      "result": "PASSED",
      "details": "Mypy reported no issues in 12 source files.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "All 84 OAP governance and process-boundary tests passed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "Owned baseline passed lock check, frozen sync, focused/full tests, Ruff, mypy, OAP, builds, offline runtime closure, and cleanup.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -I -B scripts/smoke_unigram_prefix.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --preflight",
      "result": "PASSED",
      "details": "Exact isolated preflight passed before source access from an owned non-repository cwd with PYTHONPATH absent.",
      "sha": "d178230d54d5679d08fd3a40b7ba1698a324d650",
      "publication_head_claim": false
    },
    {
      "command": "curl --disable --silent --show-error --fail --connect-timeout 10 --max-time 900 --max-filesize 115865656 --output OWNED_006_I_SOURCE DIRECT_GIGAFIDA_ARTIFACT_URL",
      "result": "PASSED",
      "details": "Exactly one direct 006-i GET completed; cumulative objective-006 GET count reached eleven and no retry was attempted.",
      "sha": "d178230d54d5679d08fd3a40b7ba1698a324d650",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -I -B scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --artifact OWNED_006_I_SOURCE",
      "result": "PASSED",
      "details": "Canonical byte size, MD5, archive SHA-256, member count, and uncompressed-size verification passed before member access.",
      "sha": "d178230d54d5679d08fd3a40b7ba1698a324d650",
      "publication_head_claim": false
    },
    {
      "command": "LOCK_DERIVED_006_I_PYTHON -I -B scripts/smoke_unigram_prefix.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --diagnostic OWNED_006_I_SOURCE",
      "result": "PASSED",
      "details": "Verifier-first diagnostic completed one selected-member capture, structural success, 32-row numeric profiling, and exactly one current-importer attempt.",
      "sha": "d178230d54d5679d08fd3a40b7ba1698a324d650",
      "publication_head_claim": false
    },
    {
      "command": "exact 006-i source, environment, cache, and cwd cleanup",
      "result": "PASSED",
      "details": "All exact owned paths were removed and verified absent; no source content was retained.",
      "sha": "d178230d54d5679d08fd3a40b7ba1698a324d650",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-i",
      "result": "PASSED",
      "details": "Indexed transcript is coherent with 006-i as the latest unfinished order.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-i",
      "result": "PASSED",
      "details": "Committed transcript is coherent before report publication.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "git ls-files --stage oap/active",
      "result": "PASSED",
      "details": "Active pointer is mode 100644 and contains 006-i followed by one LF.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "details": "Implementation history has no whitespace errors.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "Protected product law, governance, strategic source, and bootstrap source paths are unchanged.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Repository object integrity completed without diagnostics.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at f14686c",
      "result": "PASSED",
      "details": "Remote required check completed successfully before report publication.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at f14686c",
      "result": "PASSED",
      "details": "Remote required check completed successfully before report publication.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 is open and non-draft at f14686c, based on main, unmerged, with both required checks successful.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/branches/main/protection",
      "result": "PASSED",
      "details": "Remote returned 404 Branch not protected; no repository setting was changed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/rulesets",
      "result": "PASSED",
      "details": "Remote returned an empty ruleset list; no repository setting was changed.",
      "sha": "f14686c8b30962a948ca4dd5acba7ebbe0a9d86a",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T21:19:10Z",
  "report_written_at": "2026-09-08T21:19:25Z",
  "implementation": "Commit a0ff780 added the fixed numeric category classifier, content-free parser-compatible profile, synthetic category/conservation tests, and mutually exclusive diagnostic CLI path. Commit d178230 activated 006-i and pushed the non-report implementation. Commit f14686c recorded the exact bounded 006-i receipt, current docs, generated projections, and receipt contract test. No importer semantics, source verifier, lock, protected governance, or product acceptance behavior changed.",
  "documentation": "STATUS.md, README.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md describe the 006-i bounded syntax diagnosis, its limits, one importer failure boundary, cumulative eleven GETs, cleanup, and non-redistribution status. Generated projections were updated and verified.",
  "criteria": "COMPLETE diagnostic round: fixed mutually exclusive enum and overlap priority; all 32 rows and 768 numeric cells profiled across 24 one-based numeric columns; 248/256 absolute-count cells and 4/512 published-decimal cells accepted by the current parser; first incompatibility row 1, column 5, absolute_count, OTHER_ASCII; one importer attempt returned allowlisted invalid-count at column 5; no importer conversion or normalization was performed.",
  "negative_paths": "Structural mismatch is rejected before numeric profiling; malformed category, UTF-8, row-count, CLI-mode, and no-content serialization paths are covered by synthetic tests. Default preflight and two-run smoke behavior remain covered and unchanged. The exploratory relative-test invocation from a non-repository cwd was not used as evidence; the repository-root authoritative rerun passed.",
  "boundary_fidelity": "Canonical inventory and archive verification preceded member access. Exactly one selected member was opened, the exact bounded envelope and 32-row structural aggregate passed, numeric fields were transient only, and the current importer was invoked exactly once with no second run, retry, or source re-fetch.",
  "setup": "One lock-derived owned Python 3.12.3 environment passed isolated preflight before the sole direct GET. The exact source, environment, cache, and cwd paths were removed and verified absent. Final owned verification environment was also removed and verified absent.",
  "privacy": "No source rows, numeric strings, digits, raw tokens, record objects, row hashes, prompts, responses, credentials, or private paths were emitted or retained. Receipt and report contain only fixed categories, aggregate counts, safe reason/column data, checksums, and bounded protocol facts.",
  "limits": "One 006-i GET, one selected-member access, 32 rows, 24 numeric columns, 768 numeric cells, one current-importer attempt, zero retry, zero second GET, zero second importer run, bounded 4 MiB envelope, and exact cleanup. Numeric categories are syntax evidence only and do not infer locale, grouping, decimal meaning, denominator, conversion, full import, linguistic benefit, rights, release, or deployment.",
  "human_gates": "D0/NONE. CRITICAL is empty; no human adjudication, live Qwen, milestone, release, deployment, merge, or redistribution authority was exercised or inferred.",
  "scope": "Only the activated 006-i implementation, tests, receipt, current docs, generated projections, active/order state, and report are in scope. PR #7 remains open and unmerged; no merge, auto-merge, release, deployment, GitHub setting, protected resource, neighboring repository, or future order was changed."
}
```

The diagnostic is complete as ordered: it separates the reached numeric syntax
hypotheses at the first importer boundary without selecting parser semantics or
claiming compatibility beyond the bounded observed prefix.

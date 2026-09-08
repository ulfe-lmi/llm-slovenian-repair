# Work report 006-j — Refine marker row and numeric units

```oap-report
{
  "id": "006-j",
  "result": "COMPLETE",
  "order_path": "oap/orders/006-j-refine-marker-row-and-numeric-units.md",
  "order_sha256": "bdee6314015235af4dab8884468274e8b3d9fc7a7ca043e8bb1d4c4edec7da0a",
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
  "implementation_head": "e81c5f1d7b87224d4e961a6453f1f78fd82ceef1",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "94f09a22dc202c29f61a87bfcc8cc68e7a076dcf",
  "no_merge": true,
  "checks": [
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest tests/contract/test_objective_005.py -q","result":"PASSED","details":"40 focused objective-005 contract tests passed.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest tests/contract/test_objective_006.py -q","result":"PASSED","details":"51 focused objective-006 importer tests passed; importer semantics remain unchanged.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest tests/contract/test_objective_006_diagnostics.py -q","result":"PASSED","details":"24 diagnostic tests passed, including marker and identity refinements.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest tests/contract/test_objective_006_smoke.py -q","result":"PASSED","details":"24 smoke, receipt, isolation, and counterfactual tests passed.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest tests/contract -q","result":"PASSED","details":"220 contract tests passed.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m pytest -q --ignore=.venv","result":"PASSED","details":"304 tests passed in the full repository suite.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m ruff check src scripts tests","result":"PASSED","details":"Ruff checks passed.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"LOCK_DERIVED_006_J_PYTHON -m mypy src tests","result":"PASSED","details":"Mypy reported no issues in 12 source files.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"python3 -B -m unittest discover -s oap/tests -v","result":"PASSED","details":"All 84 OAP governance and process-boundary tests passed.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300","result":"PASSED","details":"Native baseline passed frozen sync, focused/full tests, Ruff, mypy, OAP, builds, offline runtime closure, and cleanup.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-j","result":"PASSED","details":"Indexed transcript is coherent with 006-j as the latest unfinished order before report publication.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-j","result":"PASSED","details":"Committed transcript is coherent before report publication.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c","result":"PASSED","details":"Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"git ls-files --stage oap/active","result":"PASSED","details":"Active pointer is mode 100644 and contains 006-j followed by one LF.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"git diff --exit-code 94f09a22dc202c29f61a87bfcc8cc68e7a076dcf...HEAD -- src","result":"PASSED","details":"src is unchanged from the exact 006-j starting remote head.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD","result":"PASSED","details":"Implementation history has no whitespace errors.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"git diff --exit-code ee2d1b479719009ff1d07829478f241e3f395f7c -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap","result":"PASSED","details":"Protected product law, governance, strategic source, and bootstrap source paths are unchanged.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"git fsck --full --no-reflogs","result":"PASSED","details":"Repository object integrity completed without diagnostics after bounded orphan cleanup.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"GitHub Actions Application baseline at e81c5f1","result":"PASSED","details":"Remote required check completed successfully before report publication.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"GitHub Actions OAP bootstrap acceptance at e81c5f1","result":"PASSED","details":"Remote required check completed successfully before report publication.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false},
    {"command":"Independent remote branch/PR head verification before report publication","result":"PASSED","details":"PR #7 is open and non-draft at e81c5f1, based on main, unmerged, with both required checks successful.","sha":"e81c5f1d7b87224d4e961a6453f1f78fd82ceef1","publication_head_claim":false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T22:34:50+00:00",
  "report_written_at": "2026-09-08T22:35:00+00:00",
  "implementation": "Commit e8c88ca activated the exact 006-j order and active pointer. Commit 601cfa4 added fixed row-1 marker refinement, identity/equality/NFC-casefold profiling, family recurrence predicates, the in-memory row-one-omitted counterfactual importer path, and synthetic tests. Commit e81c5f1 recorded the one bounded 006-j acquisition, receipt, current docs, generated projections, and receipt contract test. No src importer semantics, verifier, source inventory, lock, protected governance, or product acceptance behavior changed.",
  "documentation": "README.md, STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md describe the content-free marker/identity evidence, the unresolved row-role/unit interpretation, the original invalid-count:5 boundary, the omitted-row invalid-decimal:6 boundary, cumulative twelve GETs, and exact cleanup. The receipt and generated projections were updated and verified.",
  "criteria": "COMPLETE diagnostic round: all 24 row-1 OTHER_ASCII numeric cells were refined as ASCII_MIXED_OTHER without emitting values; their 24 marker identities were distinct, nonrecurring in the same columns, and column-specific across absolute/share/relative families. The row-1 identity profile was MIXED/ASCII_LETTERS/MIXED/MIXED, ALL_DISTINCT, all NFC-casefold relations false, and matched zero rows 2–32, yielding only NUMERIC_MARKERS_COLUMN_SPECIFIC and IDENTITY_PROFILE_OUTLIER predicates. The original importer call returned invalid-count:5 at column 5; the preserved-preamble/header, row-1-omitted counterfactual made exactly one max_rows=31 call and returned invalid-decimal:6 at column 6.",
  "negative_paths": "Synthetic tests cover every marker and identity category, equality partitions, family mapping, recurrence/outlier relations, conservation, deterministic serialization, sentinel exclusion, structural-first failure, counterfactual envelope integrity, exact importer-call behavior, mode exclusion, and the prior preflight/full-smoke contracts. Safe importer exposure remains limited to allowlisted reason/column pairs; no raw source text, marker value, token, hash, length, or record object is emitted by the new diagnostic profile.",
  "boundary_fidelity": "One verifier-first direct GET reached the canonical archive, one selected member was accessed, the 14-line preamble/header and 32-row structure passed, all 768 numeric cells were profiled exactly once, the original diagnostic importer call ran once, and the row-one-omitted counterfactual importer call ran once with max_rows=31. No retry, second GET, broad search, retained source bytes, or production importer conversion occurred.",
  "setup": "An owned lock-derived Python 3.12.3 environment passed isolated preflight before the sole direct GET. The exact source, environment, cache, cwd, verifier output, diagnostic output, and final verification environment were removed and verified absent. Native baseline cleanup passed.",
  "privacy": "No source rows, numeric strings, marker values, identity strings, digits, raw tokens, record objects, prompts, responses, credentials, or private paths were emitted or retained. The receipt/report contain only fixed categories, aggregate counts, safe reason/column data, checksums, and bounded protocol facts.",
  "limits": "One 006-j GET (cumulative objective-006 GETs twelve), one selected-member access, 32 rows, 24 numeric columns, 768 numeric cells, one original importer attempt, one row-one-omitted importer attempt, zero retry, zero second GET, bounded 4 MiB envelope, and exact cleanup. Numeric and identity observations do not infer locale, grouping, units, row role, denominator completeness, conversion, full import, linguistic benefit, rights, release, or deployment authority.",
  "human_gates": "D0/NONE. CRITICAL is empty; no human adjudication, live Qwen, milestone, release, deployment, merge, or redistribution authority was exercised or inferred. Row-role and unit meanings remain unresolved pending strategic selection.",
  "scope": "Only the activated 006-j order/active state, diagnostic implementation and tests, 006-j receipt, current docs/generated projections, and this report are in scope. PR #7 remains open and unmerged; no merge, auto-merge, release, deployment, GitHub setting, protected resource, neighboring repository, or future order was changed."
}
```

The ordered diagnostic is complete at its intended boundary: the fixed content-free
marker and identity evidence exposes the next parser failure without selecting
production row-role, unit, skip, or normalization semantics.

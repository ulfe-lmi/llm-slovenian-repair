# Work report 006-c — Support observed terminal tab and complete smoke

```oap-report
{
  "id": "006-c",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-c-support-observed-terminal-tab-and-complete-smoke.md",
  "order_sha256": "dfe9decb1ea1d286079d8c635918caea2e49da423c92af9aec4036badf988ce9",
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
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949dd0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "publication_commit": "SELF",
  "implementation_head": "6e626fce9df874f569984bd0d810412f7685f0d8",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "4fc0f42d119ea22c914e0898b34a9a5e37cfa5c8",
  "no_merge": true,
  "checks": [
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "49 passed",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "121 passed",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 pytest tests/contract -q",
      "result": "PASSED",
      "details": "170 passed",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 pytest -q",
      "result": "PASSED",
      "details": "254 passed in 145.78s",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-c-venv uv run --frozen --python 3.12 mypy src tests",
      "result": "PASSED",
      "details": "Success: no issues found in 10 source files",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "84 tests",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "all 13 baseline stages passed; cleanup PASSED",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --validate-only",
      "result": "PASSED",
      "details": "four-entry inventory validated offline",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-c",
      "result": "PASSED",
      "details": "active 006-c; all historical orders/reports coherent",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-c",
      "result": "PASSED",
      "details": "committed transcript coherent at 6e626fc",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "accepted runtime structure valid; semantic and human authorization proof remain false",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "details": "no protected governance/bootstrap source changes",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "one 006-c curl --disable HTTPS GET, accepted verifier, bounded member shape sample, importer twice, and exact owned temporary-tree cleanup",
      "result": "BLOCKED",
      "details": "exactly one GET; verifier PASSED for size 115865656, MD5 b20a959f9c113aeb6504f0d753d36d10, archive SHA-256 77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a, five members, and total uncompressed size 1487654024; the bounded first-32-row structural sampler stopped on a non-content row-shape mismatch before importer execution, so importer runs, sample count, input hash, and output hash are null",
      "sha": "87a55086e84d6af9c19cfdf76c139f0be6545b09",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34232501475)",
      "result": "PASSED",
      "details": "remote head 6e626fc; completed in 1m36s",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34232501722)",
      "result": "PASSED",
      "details": "remote head 6e626fc; completed in 39s",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 open on 6e626fc, base main, no merge",
      "sha": "6e626fce9df874f569984bd0d810412f7685f0d8",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T13:33:55Z",
  "report_written_at": "2026-09-08T13:34:22Z",
  "implementation": "The importer now distinguishes the exact delimiter-free 28-field header from data records with one source-specific terminal tab before CRLF, consumes that tab without creating a semantic 29th field, and binds data_record_terminator=TAB_BEFORE_CRLF in provenance, summary, and result validation. Synthetic contract helpers and negative cases cover missing, repeated, spaced, extra-field, unquoted, and embedded-tab shapes while preserving existing identity, Unicode, zero, determinism, resource, and provenance checks.",
  "documentation": "Updated STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md with the header/row distinction, the bounded 006-c result, and preserved 006-a/006-b incidents. Added the 006-c source receipt with one verified GET, cumulative five objective GETs, the exact format contract, verifier facts, structural-sampler block, null importer evidence, cleanup, no-content, and no-redistribution facts; reconciled generated and installation metadata.",
  "criteria": "Criterion 1 is PASSED for the exact header/no-terminal-tab and data-row/one-terminal-tab contracts, strict wider/missing/malformed rejection, and unchanged importer semantics on synthetic data. Criterion 2 is BLOCKED: one verifier-first GET passed artifact integrity and the bounded sample read 32 rows, but the structural sampler stopped before importer execution on a non-content row-shape mismatch; no real import runs or hashes are claimed. Criterion 3 is PASSED for cumulative five, preservation of 006-a exact-one false and 006-b blocked terminator evidence, verifier ordering, cleanup, no retained bytes, and null unknowns. Criterion 4 is BLOCKED overall by the ordered real smoke, while all local product/OAP/native/protected checks and both required remote checks passed; PR #7 remains open and unmerged. This is a truthful BLOCKED round, not a claim of real compatibility, linguistic benefit, release, deployment, or milestone acceptance.",
  "negative_paths": "The preserved repository .venv was found invalid without being deleted; an owned disposable /tmp Python 3.12 environment was used instead. Focused tests reject header terminal tabs, missing/repeated/spaced row terminators, extra fields, unquoted fields, embedded tabs, malformed quoting, bad UTF-8/control/surrogate input, truncation, and resource violations. The real attempt reached the accepted verifier, then stopped at the first reached structural-sampler failure; no retry, second GET, parser weakening, importer run, or content logging occurred.",
  "boundary_fidelity": "Only active order 006-c, its order and report paths, the objective-006 importer/tests/fixture boundary, current status/data/development docs, the 006-c receipt, and generated metadata were changed. No PLAN, full architecture, CRITICAL, security/testing law, bootstrap source lock, protected governance, dependency, Qwen/GPU/service/gateway, neighboring repository, network setting, merge, release, deployment, or customer-data boundary was changed.",
  "setup": "The consumed marker was reconciled to 006-c on the existing oap/006-unigram-lexicon-importer branch and PR #7; the matching order was force-staged with exact active bytes 006-c\\n. The preserved invalid .venv was left untouched; verification used an owned disposable frozen project environment. The one source request used curl --disable, direct HTTPS without redirects or credentials, connect timeout 10s, total timeout 900s, and max-filesize 115865656, writing only to an owned .part path before verification; the archive and temporary tree were deleted after the blocked sample.",
  "privacy": "No source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content was logged, committed, or put in the report. The receipt/report retain only source identity, required URLs, finite schema/integrity metadata, aggregate counts/hashes where available, and non-content failure classification.",
  "limits": "The exact 28-field all-quoted parser is now bound to data_record_terminator=TAB_BEFORE_CRLF but remains fail-closed for all wider or malformed forms. Real smoke acceptance is BLOCKED by the bounded structural sampler; the receipt leaves importer runs, sample count, input hash, and output hash null. The 006-a three-GET incident and 006-b blocked terminator observation remain historical. This is a bounded parser seam, not an index, detector, linguistic result, legal/redistribution decision, milestone acceptance, release, deployment, or merge authorization. publication_verified remains false until the separate report-publication verification step.",
  "human_gates": "Decision class D0 and deferred adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, rights, release, deployment, and milestone authority remain unchanged.",
  "scope": "Executed only active order 006-c as a corrective suffix on the existing 006 objective branch/PR. The implementation and activation commits are 87a5508 and 6e626fc; prior 006-a and 006-b reports/receipts remain preserved. The single new GET was verified before member access, the structural smoke was bounded and stopped fail-closed, and the exact owned temporary tree was removed. All named local checks and both required remote checks passed except the ordered real compatibility smoke, which is recorded BLOCKED. No future CI result, report-publication verification, merge, release, or deployment claim is made."
}
```

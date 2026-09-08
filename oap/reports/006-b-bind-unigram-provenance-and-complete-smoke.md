# Work report 006-b — Bind unigram provenance and complete smoke

```oap-report
{
  "id": "006-b",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-b-bind-unigram-provenance-and-complete-smoke.md",
  "order_sha256": "ab77203e0680aa87a139ecbb71caf7b1ec2749756d3b9d72566f6d5ac68072fa",
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
  "implementation_head": "b8202c63b4fa609e35824705df53b4282d752b23",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "767062ac2b2c543c6bc6fdffae2a3fc3a39a786c",
  "no_merge": true,
  "checks": [
    {
      "command": "python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --source-id gigafida-2.0-words --artifact owned-006-b-part-path-redacted",
      "result": "PASSED",
      "details": "verified size 115865656, MD5 b20a959f9c113aeb6504f0d753d36d10, SHA-256 77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a, five ZIP members, total uncompressed size 1487654024",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "006-b exact HTTPS GET with curl --disable, no redirects, connect timeout 10s, total timeout 900s, max-filesize 115865656",
      "result": "PASSED",
      "details": "one GET to the accepted inventory artifact; owned .part staging only",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "40 passed",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py tests/contract/test_objective_005.py -q",
      "result": "PASSED",
      "details": "121 passed",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 pytest tests/contract -q",
      "result": "PASSED",
      "details": "161 passed",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 pytest -q",
      "result": "PASSED",
      "details": "245 passed in 129.93s",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 ruff check src scripts tests",
      "result": "PASSED",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "UV_PROJECT_ENVIRONMENT=/tmp/llm-slovenian-repair-006-b-venv uv run --frozen --python 3.12 mypy src tests",
      "result": "PASSED",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "84 tests",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "all 13 baseline stages passed; cleanup PASSED",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-b",
      "result": "PASSED",
      "details": "active 006-b; all historical orders/reports coherent",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-b",
      "result": "PASSED",
      "details": "committed transcript coherent at b8202c6",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "details": "no protected governance/bootstrap source changes",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "bounded real smoke using 14 preamble lines, exact header, and at most 32 rows, run twice",
      "result": "BLOCKED",
      "details": "first importer run stopped at line 16 with invalid-quoting before any record; non-content diagnostic found 28 parsed quoted fields followed by a trailing tab/empty 29th field; no second importer run, input hash, output hash, or real sample count is claimed",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "owned 006-b temporary-tree cleanup and absence check",
      "result": "PASSED",
      "details": "archive and temporary tree deleted; no matching 006-b tree remains",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34228298108)",
      "result": "PASSED",
      "details": "remote head b8202c6; completed in 1m6s",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34228298140)",
      "result": "PASSED",
      "details": "remote head b8202c6; completed in 48s",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 open on b8202c6, base main, no merge",
      "sha": "b8202c63b4fa609e35824705df53b4282d752b23",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T14:51:41+02:00",
  "report_written_at": "2026-09-08T14:52:04+02:00",
  "implementation": "The original product implementation head is 4f3c3d66dbc8c48b6445e973e3ada61bafb131b5. The preserved 006-a invalid report e16c3303aab40a914d7edf22520cbf2bf81f1095 and append-only reconciliation publication 767062ac2b2c543c6bc6fdffae2a3fc3a39a786c remain in ancestry. Implementation head b8202c63b4fa609e35824705df53b4282d752b23 binds explicit real versus project-synthetic provenance, reuses contracts.EvidenceCompleteness, rejects header-line rebinding and arbitrary real identity, removes duplicate parser aliases and root exports, validates summary constants and canonical output hashes during ordinary construction, cross-checks record numeric/text/key derivation, repairs the historical receipt field, and adds focused contract probes plus generated-document reconciliation.",
  "documentation": "Updated STATUS.md, docs/DATA-SOURCES.md, and docs/DEVELOPMENT.md with the single submodule entry point, exact provenance modes, contract limits, the historical 006-a handoff, and the blocked 006-b smoke. Added the 006-b finite receipt with verified archive metadata, one GET, cumulative four-GET context, verifier ordering, bounded failure boundary, and cleanup facts; retained 006-a PARTIAL_RECOVERY_HANDOFF unchanged except for renaming its misleading 40-hex field to base_revision_observed_locally. Updated objective-001 and baseline export expectations and reconciled generated/installation manifest hashes.",
  "criteria": "Criterion 1 is PASSED for the shared completeness type, exact real provenance binding, explicit project-synthetic identity, header-line 15 binding, one submodule entry point, root laziness, summary constant/output-hash validation, record numeric/text/key correspondence, and receipt schema probes. Criterion 2 is PASSED for deterministic project-authored synthetic import, ambiguity/Unicode/count/resource semantics, and the full offline product suite. Criterion 3 is BLOCKED after exactly one new 006-b GET: accepted verification passed for size 115865656, MD5 b20a959f9c113aeb6504f0d753d36d10, archive SHA-256 77ac4aa2e77016470a26ebf5b1bd265b9de240e8254d3511d51cb0fcb68a767a, five members, and total uncompressed size 1487654024, but the first data row has a trailing empty 29th field after 28 parsed fields. The schema was not weakened; the twice-run smoke therefore produced no real input/output hashes or sample count. Cleanup passed and no archive/temp tree or source data remains. Criterion 4 is PASSED for the truthful new receipt and preserved 006-a history: 006-b observed one GET, cumulative objective count is four, and 006-a exact-one remains false; no current real-import success or redistribution claim is made. Criterion 5 is PASSED for local product/OAP/native/protected checks and remote required checks at b8202c6; PR #7 remains open and unmerged. This is a truthful BLOCKED round, not a claim of real compatibility, linguistic benefit, release, deployment, or milestone acceptance.",
  "negative_paths": "Focused tests exercise the actual importer boundary for alias/root-export removal, shared enum identity, real provenance rebinding, header line 1, synthetic identity/hash placeholders, summary schema/importer/output-hash tampering, record numeric/text/key/key-derivation tampering, malformed counts/overflow/decimals, zero without complete query, invalid UTF-8/control/surrogate, quoting/header/field/newline errors, duplicate/conflicting records, limits, and immutable deterministic output. The real smoke's first setup invocation stopped before archive access because system Python lacked the package; the frozen-project retry reached the importer and stopped at the first incompatible row. No fake replaced the claimed parser boundary.",
  "boundary_fidelity": "Only active order 006-b, its immutable order file, the importer and root export expectations, focused tests, current status/data/development docs, source-acquisition receipts, generated/installation metadata, and this report path are in scope. No PLAN, ARCHITECTURE, CRITICAL, security/testing law, bootstrap source lock, protected governance, dependency, Qwen/GPU/service/gateway, neighboring repository, network setting, merge, release, deployment, or customer-data boundary was changed. The real archive was used only in the owned temporary tree after accepted verification and was deleted before commit.",
  "setup": "The consumed marker was reconciled to active 006-b on the existing oap/006-unigram-lexicon-importer branch and PR #7; no new PR was created. Verification used the committed uv.lock, a fresh owned /tmp project environment, the accepted standard-library artifact verifier, bounded member access, and native baseline cleanup. The single exact source request used curl --disable, HTTPS without redirects, connect timeout 10s, total timeout 900s, and max-filesize 115865656. No live model, GPU, service, credentials, customer data, or retained archive was used.",
  "privacy": "No source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content was logged, committed, or put in the report. The receipt and report retain only source identity, URLs required by the ordered receipt, finite schema/integrity metadata, counts, hashes, line number, and non-content failure classification.",
  "limits": "The exact 28-field all-quoted importer contract remains unchanged. Real smoke acceptance is BLOCKED by the observed trailing empty 29th field at line 16; no parser adaptation, retry, second GET, real input hash, output hash, or sample count is claimed. The 006-a three-GET incident remains historical and exact-one false. The implementation is a bounded parser seam, not an index, detector, linguistic result, legal/redistribution decision, milestone acceptance, release, deployment, or merge authorization. publication_verified remains false until the separate report publication verification step.",
  "human_gates": "Decision class D0 and deferred adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, rights, release, deployment, and milestone authority remain unchanged.",
  "scope": "Executed only active order 006-b as a corrective suffix on the existing 006 branch/PR. Original product implementation 4f3c3d66, 006-a invalid report e16c3303, 006-a reconciliation 767062ac, and 006-b implementation b8202c6 are explicitly distinguished and preserved. The single new GET was verified before member access, the real smoke was blocked without weakening schema, and the exact owned temporary tree was removed. All named local checks and both required remote checks passed at b8202c6 except the ordered real compatibility smoke, which is recorded BLOCKED. No future CI result, report publication verification, merge, release, or deployment claim is made."
}
```

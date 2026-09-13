# Work report 006-d — Diagnose real unigram row structure

```oap-report
{
  "id": "006-d",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-d-diagnose-real-unigram-row-structure.md",
  "order_sha256": "85507d269f7035bfdf0856a16e010530dc762db7d903dbc4472a267079b270e0",
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
  "implementation_head": "458481f4dc410132da9d754b75eac92691435160",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "898ccbc04ea1c8450f93ce3f1b7cc0869f97e9f9",
  "no_merge": true,
  "checks": [
    {
      "command": "uv run --frozen --python 3.12 pytest tests/contract/test_objective_006_diagnostics.py -q",
      "result": "BLOCKED",
      "details": "The exact workspace invocation was blocked by the pre-existing empty .venv; the same focused test passed 13 tests with PYTHONPATH=src, and the supported temporary baseline driver passed its focused stage.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src python3.12 -m pytest tests/contract/test_objective_006_diagnostics.py -q",
      "result": "PASSED",
      "details": "13 passed; content-free synthetic classifier cases and limits.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src python3.12 -m pytest tests/contract/test_objective_006.py -q",
      "result": "PASSED",
      "details": "49 passed; existing importer contract unchanged.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "All 13 baseline stages passed, including focused/full pytest, Ruff, mypy, OAP tests, builds, offline runtime checks, and cleanup.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src python3.12 -m pytest tests/contract -q",
      "result": "BLOCKED",
      "details": "180 passed and 3 environment-isolation tests failed because the workspace invocation lacked the installed package/dependency closure; the supported baseline driver passed the authoritative contract stage.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src python3.12 -m pytest -q",
      "result": "BLOCKED",
      "details": "264 passed and 3 environment-isolation tests failed for the same uninstalled workspace environment; the supported baseline driver passed full pytest.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "84 tests passed.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime structure valid; semantic and human-authorization proof remain false.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "details": "No protected governance, bootstrap source, dependency, or law changes.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "one 006-d curl --disable HTTPS GET, accepted verifier, bounded member-prefix handoff, classifier boundary, and exact owned temporary-tree cleanup",
      "result": "BLOCKED",
      "details": "Exactly one 006-d GET was spent and cumulative observed objective GETs reached six; verifier PASSED before member access, 14 preamble lines were skipped, but the handoff failed with requested-row-incomplete before 32 complete rows reached the classifier. Aggregate diagnosis is null, importer attempts are zero, no retry occurred, and cleanup/no-content/no-retained-source conditions are recorded in the receipt.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head",
      "result": "PASSED",
      "details": "Remote head 458481f4dc410132da9d754b75eac92691435160; run 34243927827 completed successfully.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head",
      "result": "PASSED",
      "details": "Remote head 458481f4dc410132da9d754b75eac92691435160; run 34243927970 completed successfully.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 is open on 458481f4dc410132da9d754b75eac92691435160, base main, with no merge.",
      "sha": "458481f4dc410132da9d754b75eac92691435160",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T15:20:52+00:00",
  "report_written_at": "2026-09-08T15:20:52+00:00",
  "implementation": "Commit 458481f4dc410132da9d754b75eac92691435160 adds only the standard-library content-free row-structure classifier, synthetic diagnostic tests, the 006-d receipt, direct status/data/development documentation, generated metadata, the active pointer, and the finalized order. The importer module, package exports, synthetic TSV, and prior 006-a/b/c receipts remain unchanged. The classifier's synthetic boundary is implemented and passes; the real diagnostic did not receive a complete 32-row input. Local recovery reconstructed this implementation additively after transient Git object loss; fsck was clean and the private recovery handoff remains untracked and unstaged.",
  "documentation": "STATUS.md, docs/DATA-SOURCES.md, docs/DEVELOPMENT.md, generated inventory metadata, and resources/source-acquisitions/gigafida-2.0-words-006-d.json record the bounded diagnostic contract and its blocked real-input outcome. They do not claim a source format correction, importer compatibility, or retained source data.",
  "criteria": "Criterion 1 PASSED for every named synthetic shape, bounded content-free output, unchanged importer/package behavior, and the focused diagnostic/importer suites. Criterion 2 BLOCKED: the one verifier-first fetch did not supply 32 complete rows to the classifier, so no aggregate or first-failure diagnosis exists. Criterion 3 PARTIAL/BLOCKED: the receipt records one 006-d GET, cumulative six, prior blocked history, verifier ordering, no importer run, null aggregates, no retained bytes, and cleanup, but it cannot establish a format contract. Criterion 4 BLOCKED overall by the real diagnostic boundary; local baseline/OAP checks and both required remote checks passed, and PR #7 remains open and unmerged. This is diagnosis status, not product compatibility, linguistic benefit, release readiness, or milestone completion.",
  "negative_paths": "No second source request, retry, parser mutation, importer run, source-content output, raw row/header logging, or source-byte retention occurred after the requested-row-incomplete boundary. Synthetic tests cover malformed/unclosed quoting, invalid UTF-8, newline variants, terminal delimiters, extra fields, embedded quoted tabs, limits, and forbidden content fields. The workspace-only uv invocation was blocked by the invalid ignored .venv; the supported temporary-parent baseline passed the corresponding installed checks.",
  "boundary_fidelity": "Only active order 006-d and its scoped classifier/tests/receipt/status-data-development/generated metadata were used. No importer behavior, protected governance/law, dependency, network/source settings, Qwen/GPU/service/gateway, neighboring repository, merge, release, deployment, or customer-data boundary was changed.",
  "setup": "The pre-existing ignored .venv was empty and invalid for uv; it was not treated as repository evidence. The supported temporary-parent baseline created owned disposable environments and passed with cleanup. The consumed one-fetch boundary was reconciled from the private recovery handoff; no FIFO wait or source refetch was performed. Implementation work was pushed normally to PR #7 before report composition.",
  "privacy": "No source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content is in the report. The committed receipt retains only the ordered source/integrity identities, bounded aggregate schema fields, failure classification, cleanup state, and rights/retention booleans required by the order.",
  "limits": "The real aggregate is null because the bounded member-prefix handoff stopped before 32 complete rows; no hypothesis was selected and no importer format correction was made. The receipt's blocked state is not an importer compatibility result. publication_verified is false because remote report publication is verified only after the SELF commit is pushed.",
  "human_gates": "Decision class D0 with Deferred human adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, rights, release, deployment, and milestone authority remain unchanged.",
  "scope": "Executed only active order 006-d on the existing objective-006 branch and PR #7. The implementation head is 458481f4dc410132da9d754b75eac92691435160, pushed before this report. The result is truthfully BLOCKED at the already-spent real diagnostic input boundary; this final publication commit must contain only this report and have the implementation head as its sole parent. No later mutation, merge, release, deployment, or future-CI claim is authorized by this report."
}
```

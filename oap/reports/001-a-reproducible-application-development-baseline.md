# Round report 001-a — Reproducible application development baseline

```oap-report
{
  "id": "001-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/001-a-reproducible-application-development-baseline.md",
  "order_sha256": "f8415df8ef6b3f6c99e5ac9bbf11531708781da04c86f085ee0049638bb809db",
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
  "implementation_head": "76711778ead2edbf4c039a62fd1beaa74fa2de8c",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 2,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/2",
  "pr_state": "open",
  "branch": "oap/001-reproducible-application-development-baseline",
  "base_sha": "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
  "starting_remote_sha": "82ea1e6f4173934fa47bb34ee6a6f78338d3603a",
  "no_merge": true,
  "checks": [
    {"command": "uv lock --check", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv sync --frozen --all-groups --all-extras --python 3.12", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv run --frozen pytest tests/contract/test_objective_001.py -q", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv run --frozen pytest -q", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv run --frozen ruff check src tests", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv run --frozen mypy src tests/contract", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "uv build --no-sources", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "offline wheel installation/import proof from outside the repository", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "python3 -B -m unittest discover -s oap/tests -v", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 82ea1e6f4173934fa47bb34ee6a6f78338d3603a", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "git diff --check 82ea1e6f4173934fa47bb34ee6a6f78338d3603a...HEAD", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "accepted-base protected-source diff", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "GitHub Application baseline check at implementation head", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "GitHub OAP bootstrap acceptance check at implementation head", "result": "PASSED", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "GitHub Application baseline check at final report head", "result": "PENDING", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false},
    {"command": "GitHub OAP bootstrap acceptance check at final report head", "result": "PENDING", "sha": "76711778ead2edbf4c039a62fd1beaa74fa2de8c", "publication_head_claim": false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T00:18:28Z",
  "report_written_at": "2026-09-08T00:18:28Z",
  "implementation": "Implemented the ordered Python 3.12 PEP 517 src-layout skeleton at implementation head 76711778ead2edbf4c039a62fd1beaa74fa2de8c. The package exposes inert version metadata only; runtime and development dependencies are separated, uv.lock is committed, and the morphology extra is empty.",
  "documentation": "Added docs/DEVELOPMENT.md and linked it from README.md. Documentation records supported Python/uv ranges, dependency separation, observed licenses, frozen commands, offline wheel proof, cleanup, and the continuing PLANNED/no-live-product boundary.",
  "criteria": "Local acceptance criteria 1-4 and 6-8 pass. The focused contract suite passed 4 tests; the full pytest suite passed 65 tests; bootstrap unittest discovery passed 61 tests; uv lock, frozen sync, Ruff, mypy, both builds, governance, whitespace, protected-source diff, and offline wheel import all passed. Both required PR checks passed at the implementation head. Final report-head checks are intentionally PENDING because they are post-publication observations.",
  "negative_paths": "Contract tests block socket connect and urllib opening before import, assert no file creation and no eager pydantic/httpx/model/analyzer imports, validate lock/source restrictions, inspect wheel metadata and payload, and exercise malformed/bootstrap governance paths through the existing 61-test suite. No live model, corpus, customer text, or production endpoint was used.",
  "boundary_fidelity": "Only order 001-a scope was changed. The accepted-base protected-source diff is empty; CRITICAL and governance identities are unchanged; the existing OAP bootstrap workflow is preserved; the application workflow uses the required pinned actions and read-only permissions. No GPU, Qwen, vLLM, CUDA, service, gateway, network, neighboring repository, or agent profile was mutated.",
  "setup": "The first shared-cache uv sync was stopped after filesystem/cache contention before it produced a test result. A separate owned temporary cache and project environment then completed frozen sync and all package proofs. Build, wheel, environment, and test-cache fixtures were cleaned through the recoverable trash mechanism after verification.",
  "privacy": "No credentials, auth files, customer/model text, prompts, replacements, raw responses, secrets, or private runtime paths were added to the repository, workflow, or report. Tests use synthetic data and owned disposable fixtures.",
  "limits": "This round proves packaging, import isolation, reproducibility, and governance baseline mechanics only. It does not prove repair behavior, serving/API compatibility, linguistic benefit, model quality, corpus rights, ICA, milestone acceptance, release, deployment, or production readiness.",
  "human_gates": "Decision class D0; deferred human adjudication is NONE; no critical action or gate was appended. PR #2 remains open, no merge or auto-merge was enabled, and release/deployment authority remains with the human owner and strategy review.",
  "scope": "Complete for the exact activated 001-a baseline scope. No next order was self-assigned, no merge was performed, and no post-report mutation is authorized for this round."
}
```

The final report-head CI observations are intentionally left for independent
post-publication verification; this report does not claim their future result.

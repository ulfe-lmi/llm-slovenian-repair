# OAP round 000-a report

```oap-report
{
  "id": "000-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/000-a-reconcile-bootstrap-repository-and-authority.md",
  "order_sha256": "4bddd781b78db243b95a9ad91e13f758a8815f904ba1f1122e3c455d1f897fbf",
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
  "implementation_head": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 1,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/1",
  "pr_state": "open",
  "branch": "oap/000-reconcile-bootstrap-repository-and-authority",
  "base_sha": "7ca26f1a6d9c110aa3c71a736d185028661d110d",
  "starting_remote_sha": "7ca26f1a6d9c110aa3c71a736d185028661d110d",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 7ca26f1a6d9c110aa3c71a736d185028661d110d",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 7ca26f1a6d9c110aa3c71a736d185028661d110d -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/commits/5e7e6c6a87d605d745aed2920e20dcf72ac0effd/check-runs",
      "result": "PASSED",
      "sha": "5e7e6c6a87d605d745aed2920e20dcf72ac0effd",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T00:54:28+02:00",
  "report_written_at": "2026-09-08T00:55:41+02:00",
  "implementation": "Implemented the scoped bootstrap adoption: isolated the live setup-shell fixture from all allowlisted runtime keys and ambient CODEX_HOME, asserted a zero shell result after the fake CLI exits nonzero, preserved configuration-conflict rejection, and added the full-history least-privilege bootstrap workflow. The synthetic fixture now excludes delivered live active/order protocol state so its intentionally inactive tests remain independent.",
  "documentation": "README.md, STATUS.md, and docs/OAP-RUNBOOK.md now state that the bootstrap baseline is owner-published and accepted for continued development, role operation is qualified, and the development loop has deliberately started. They direct readers to oap/active and check_state.py while retaining PLANNED product status, disabled live repair testing, and separate Qwen, linguistic, ICA, milestone, release, and deployment limitations. Generated inventories were updated for the changed generated surfaces.",
  "criteria": "The focused suite passed 16 tests in 34.011s and the complete suite passed 60 tests in 95.379s at the implementation head; tmux and the live-shell survival test executed. Accepted-runtime governance was valid against the literal base. The implementation-head hosted check named OAP bootstrap acceptance completed with success on the same SHA. The report-head check and final remote SELF verification are necessarily not observable before this report commit, so this report is PARTIAL.",
  "negative_paths": "The passing suites covered absent versus malformed active state, draft-order rejection, runtime configuration conflict rejection, duplicate-model-launch suppression, exact FIFO and PR/report boundaries, and the setup shell surviving the fake CLI exit. No negative path was weakened; no live model or product repair path was invoked.",
  "boundary_fidelity": "The change stays within bootstrap fixtures, documentation, generated inventory, protocol inputs, and the named CI workflow. The real runtime configuration-authority boundary remains unchanged. The workflow uses contents: read, a finite timeout, full history, the required immutable checkout action, Python 3.12/tmux presence checks, the literal accepted base, the complete suite, governance validation, and diff checking.",
  "setup": "Used the existing Python 3.12 standard-library unittest stack, local Git, native FIFOs, and tmux with owned disposable fixtures. No package, daemon, service, corpus, model, gateway, network, or GPU setup was used. The PR was created before report composition as PR #1 on the ordered branch.",
  "privacy": "Tests used synthetic data and fake CLI/GitHub edges. No credentials, authentication files, private runtime values, user/model text, raw responses, corpus data, or protected infrastructure were added to the repository, report, workflow, or PR.",
  "limits": "Evidence establishes bootstrap software mechanics only. It does not establish repair application functionality, Qwen compatibility, linguistic benefit, production readiness, ICA, branch protection, release, deployment, or human milestone acceptance. The report-head hosted result and post-publication remote verification remain pending observation after publication.",
  "human_gates": "Decision class D0; deferred human adjudication is NONE. No merge, auto-merge, repository-setting change, release, deployment, live repair test, or protected-resource mutation was performed. Product and deployment gates remain with the human/strategic process.",
  "scope": "No repair code, model/corpus artifact, credential, private path, product completion claim, GitHub setting mutation, merge, release, or deployment is present. The active pointer and 000-a order were committed byte-for-byte as delivered. Report publication is the sole remaining local mutation for this round."
}
```

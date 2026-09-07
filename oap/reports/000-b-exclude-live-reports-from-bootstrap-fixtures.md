# OAP round 000-b report

```oap-report
{
  "id": "000-b",
  "result": "COMPLETE",
  "order_path": "oap/orders/000-b-exclude-live-reports-from-bootstrap-fixtures.md",
  "order_sha256": "c70701b3f3de368081778d3480cb17551e2245b7f1fbf98a0f35a43db10c4251",
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
  "implementation_head": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 1,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/1",
  "pr_state": "open",
  "branch": "oap/000-reconcile-bootstrap-repository-and-authority",
  "base_sha": "7ca26f1a6d9c110aa3c71a736d185028661d110d",
  "starting_remote_sha": "7819dd0970019d966fd2756f5261efe3d9032c9b",
  "no_merge": true,
  "checks": [
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p 'test_acceptance.py' -v",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -p 'test_process_boundaries.py' -v",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 7ca26f1a6d9c110aa3c71a736d185028661d110d",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_state.py --repo-root . --repository ulfe-lmi/llm-slovenian-repair",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 7ca26f1a6d9c110aa3c71a736d185028661d110d...HEAD",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 7ca26f1a6d9c110aa3c71a736d185028661d110d -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "gh api repos/ulfe-lmi/llm-slovenian-repair/commits/d6f8ffc15a4c170ddcc44176a95e37abd1b9392d/check-runs",
      "result": "PASSED",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at the final 000-b report head",
      "result": "PENDING",
      "sha": "d6f8ffc15a4c170ddcc44176a95e37abd1b9392d",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T01:16:12+02:00",
  "report_written_at": "2026-09-08T01:16:30+02:00",
  "implementation": "Implemented the scoped bootstrap correction: synthetic repository copying now excludes Markdown reports symmetrically with live order history, while excluding only the root oap/active pointer and retaining scaffold placeholders. Added B36_live_protocol_history_is_not_copied to prove the source has live active/order/report artifacts, the copy is inactive and history-free, and report/order directories, .gitkeep placeholders, and report templates remain usable. The workflow now checks whitespace across the literal accepted-base-to-HEAD range. Updated only the generated and installation inventory values for the changed acceptance test.",
  "documentation": "No public product or status documentation was changed. The immutable 000-b order records the diagnosed final-head fixture leak, exact prior CI run/head, negative-path preservation, and evidence limits; the 000-a order/report remain unchanged.",
  "criteria": "At implementation head d6f8ffc15a4c170ddcc44176a95e37abd1b9392d, focused acceptance passed 38 tests, process boundaries passed 16 tests, and the complete bootstrap suite passed 61 tests with zero failures/errors. The real tmux and live-shell tests executed. Accepted-runtime governance passed against the literal base, protected-source diff was empty, the exact implementation-head OAP bootstrap acceptance check completed successfully, and the worktree/remote branch heads matched. The required check for the final report head is pending because that head does not exist until this report commit is published; strategic verification must observe it after publication.",
  "negative_paths": "The passing suites covered absent versus malformed active state, live-history exclusion, draft-order rejection, completed replay and ambiguous identifiers, configuration-authority conflict rejection, duplicate-model-launch suppression, SELF report parent/path/content rules, FIFO framing, competing locks, and the setup shell surviving a fake CLI's nonzero exit. No negative proof was weakened and no live model or product repair path was invoked.",
  "boundary_fidelity": "The implementation stays within oap/tests/test_acceptance.py, .github/workflows/oap-bootstrap.yml, the two required inventory rows, the delivered 000-b order, and oap/active. The filter excludes only oap/orders/*.md, oap/reports/*.md, and the root oap/active; it does not hide templates, source laws, other Markdown, or placeholders. The workflow retains the required job name, read-only permission, runner, timeout, full-history immutable checkout, Python/tmux checks, complete suite, governance check, and accepted-base range check.",
  "setup": "Used the existing Python 3.12 standard-library unittest stack, local Git, native FIFOs, and tmux with owned disposable fixtures. No package, daemon, service, corpus, model, gateway, network, or GPU setup was used. The existing PR #1 was adopted before report composition; no new PR was created.",
  "privacy": "Tests used synthetic data and fake CLI/GitHub edges. No credentials, authentication files, private runtime values, user/model text, raw responses, corpus data, or protected infrastructure were added to the repository, report, workflow, or PR.",
  "limits": "Evidence establishes bootstrap software mechanics and hosted implementation-head reproduction only. It does not establish repair application functionality, Qwen compatibility, linguistic benefit, production readiness, ICA, branch protection, release, deployment, or human milestone acceptance. The final report-head hosted check and remote SELF verification are pending observation after publication; the earlier failed run 34168409221 at 7819dd0 remains historical and was not rerun or relabelled.",
  "human_gates": "Decision class D0; deferred human adjudication is NONE. No merge, auto-merge, repository-setting change, release, deployment, live repair test, or protected-resource mutation was performed. Product and deployment gates remain with the human/strategic process.",
  "scope": "No repair code, model/corpus artifact, credential, private path, product completion claim, GitHub setting mutation, merge, release, or deployment is present. The 000-a order/report and historical commits were preserved. The implementation head is the sole parent planned for this report-only publication commit; after publication, remote report bytes/parent/only-path and final-head CI must be independently verified before response OK and exit."
}
```

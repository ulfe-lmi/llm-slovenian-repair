# Work report 007-d — Complete research publication and reproduction coverage

```oap-report
{
  "id": "007-d",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-d-complete-research-publication-and-reproduction-coverage.md",
  "order_sha256": "5f5cf095cad7a0c30307b715d37781ba52da09aa6160f31bd0140a9bc774afec",
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
  "implementation_head": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "427aca4b86be984499ac44c0eec5e041d6535db2",
  "no_merge": true,
  "checks": [
    {
      "command": "PYTHONPATH=. python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "37 research tests passed: copied historical Client/fake transport, detector/gate/case/patch/M3, saved campaign replay, nested English evidence, recorded first-call failure, exact prompts, parser fidelity, all none/low/high/xhigh mechanical variants, publication negatives, and zero-call replay.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.replay --scratch PERSISTENT_TMPDIR",
      "result": "PASSED",
      "details": "Synthetic replay exercised detector, English policy, gate, patch and retry boundaries with zero model/network calls.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.build_public_registry --existing-census PRESERVED_CENSUS",
      "result": "PASSED",
      "details": "21 records, 50 child runs/phases, 225757 census entries, 27 curated/redacted mappings, 211136 private-only entries, 14594 duplicate-linked entries, 10 numeric projections, zero curation calls.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "Working-tree research publication guard passed for 119 files after disposable bytecode caches were removed.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=. python3 -B -m research.tools.publication_guard --staged-tree MATERIALIZED_INDEX/research --private-root PREPARED_PRIVATE_SOURCE",
      "result": "PASSED",
      "details": "Materialized HEAD index tree passed staged-byte checks and a bounded prepared-source overlap scan (119 files). The full archive scan separately failed closed on the large historical campaign inventory; no public result was accepted from that failed pass.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src python3 -B -m pytest -q",
      "result": "FAILED",
      "details": "373 passed and 4 inherited failures: installed import isolation, lazy dependency availability, wheel dependency environment, and isolated unigram preflight dependency availability. No product, lock, service, or production file changed.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "All 104 OAP bootstrap, governance, FIFO, transcript, report-history, process-boundary, and recovery tests passed.",
      "sha": "33e8d9a",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/oap_cli.py transcript --index/--revision HEAD --expected-id 007-d",
      "result": "PASSED",
      "details": "Active and committed transcript resolve to 007-d; report history remains valid with only the two frozen historical incidents.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/oap_cli.py governance --mode candidate-review --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Candidate governance structure is valid; semantic and human-authorization proofs remain false.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 427aca4b86be984499ac44c0eec5e041d6535db2 97eceff; git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Implementation history has no whitespace errors; fsck passed with expected dangling scratch objects.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.replay --saved-record PRIVATE_CAMPAIGN_M2.json --index PRIVATE_VERIFIED_INDEX",
      "result": "BLOCKED",
      "details": "An exact preserved campaign M2 record failed closed because its saved record lacks the required detector maximum/uncapped marker. No default was inferred and no model/network call occurred.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "git ls-remote origin refs/heads/oap/007-concept-verification; gh api pulls/8",
      "result": "PASSED",
      "details": "Remote branch and PR #8 head are 97eceffa4c1ca60f1b0cea0fef30a4dc54be18df; PR is open, base is main, merged is false.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "ruff check research",
      "result": "MISSING",
      "details": "Ruff is not installed in the native environment; no Ruff result is claimed.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    },
    {
      "command": "mypy research",
      "result": "MISSING",
      "details": "Mypy is not installed in the native environment; no mypy result is claimed.",
      "sha": "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-11T21:55:22+02:00",
  "report_written_at": "2026-09-11T21:55:22+02:00",
  "implementation": "Copied and parameterized the owned historical executable closure: transport HTTP/capture/persistence, campaign storage/runner/checkpoint/scheduler, detector/gates/retry/case/patch methods, ten-run English-preserve driver, contextual JSON retry, later word-only retry and whitespace continuation, validator prompt/protocol, adapters, official scorer wrapper, aggregate metrics, and fixed-seed paired bootstrap. Defaults remain offline; live execution requires explicit endpoint, credential environment, caller-owned input/index/output resources, and bounded budget. The source manifest records function coverage and transformations.",
  "documentation": "research/README.md navigates all 21 records, child runs/phases, per-study data-free reports/configs, numeric evidence, archive census, source mappings, replay commands, and limitations. The low-unigram contextual JSON retry is distinct from the later word-only retry; inference fields explicitly record that source input was sent while filled records remain excluded from public Git.",
  "criteria": "PARTIAL but truthful: executable historical source coverage, data-free publication, synthetic/fake transport tests, saved campaign-shape replay, exact prompts/configs, catalog/census, and scoped protocol checks are complete. The preserved full-campaign record replay is blocked by a missing saved cap marker; the full archive overlap pass failed closed on a large inventory; official remote scoring remains access-blocked; and the inherited Application baseline has four failures.",
  "negative_paths": "Tests and guards reject duplicate keys, malformed proposals, combining-mark loss, protected/stale/overlapping edits, retry-only versus first-stage failures, missing English evidence, missing detector caps, recorded first-call failures, wrong reasoning variant, network defaults, credential/path/raw-field exposure, symlinks, overwrite races, staged-byte violations, and replay assumptions. No missing evidence was converted to zero or KEEP.",
  "boundary_fidelity": "Only research/**, the exact 007-d order/report paths, and the required active pointer changed in this round. Existing strategic/product sources, application code, locks, production configuration, services, GPU/CUDA/vLLM, gateway, profiles, ports, network, and private native experiment bytes were not changed. No live Qwen call, dataset acquisition, scientific rerun, tuning, merge, release, or deployment occurred.",
  "setup": "Startup recovery reconciled consumed 007-d on the same branch and PR #8. The assume-unchanged active pointer was explicitly reconciled to 007-d. All scratch, staged trees, fixtures, and scan inputs used the inherited persistent TMPDIR; no experiment artifact was created in /tmp.",
  "privacy": "No dataset sentences, gold/replacement strings, filled prompts, raw responses, reasoning, credentials, corpus/index bytes, or private host/profile values were committed or placed in this report. Public outputs contain only data-free numeric/status/hash projections, generic prompt templates, source coverage, and logical identities. The staged guard passed against 119 files with a bounded prepared-source overlap scan.",
  "limits": "The exact preserved campaign M2 replay failed closed at the missing cap/uncapped field, so no full-campaign replay success is claimed. The full archive overlap scanner failed closed on llm-slovenian-repair-campaign8.ewruv3.files.json; a bounded prepared-source scan passed, and the existing committed audit remains separate evidence. Ruff/mypy are missing. The application baseline has 373 passes and four inherited dependency/preflight failures. Remote/Scribendi scoring and Deployment B remain blocked/excluded. No linguistic benefit, human semantic labels, product correctness, merge readiness, release, or deployment authority is claimed.",
  "human_gates": "D0/NONE; CRITICAL is empty. Owner authorization covers archival/publication of owned code and data-free projections, not dataset rows, private responses, credentials, corpus/index/model bytes, or a new license. Coding did not append critical history, merge, enable auto-merge, repair the inherited baseline, select a new objective, or claim human acceptance.",
  "scope": "Finished only SAME007-d on existing PR #8: implementation commits 42d34fe, 33e8d9a, and 97eceff were pushed; the remote head was independently checked as 97eceff; this exact report is the sole remaining round mutation. The final commit must contain only this report, have 97eceff as its sole parent, be pushed once, independently verified, then followed by exact OK and exit.",
  "result_summary": "PARTIAL / archival and executable-source publication complete at the coding boundary, with explicit private replay, archive-scan, tool, remote-scoring, and inherited-baseline limitations. PR #8 remains open and unmerged; no product or linguistic acceptance is claimed."
}
```

## Result

007-d preserves runnable historical algorithms rather than contract labels: the owned HTTP client/capture path, campaign scheduler/checkpoints, variant prompts, detectors, gates, retry programs, scorers, bootstrap, and analysis are present under `research/curated/` with explicit resource injection. Public configs, reports, registry/census, and numeric projections are navigable and data-free.

The result is a truthful PARTIAL because one preserved final-campaign record lacks the cap metadata required for fail-closed replay, the broad private scan stops on a large inventory, and inherited/tool/access limitations remain.

## Deferred human adjudication

- Decision: NONE


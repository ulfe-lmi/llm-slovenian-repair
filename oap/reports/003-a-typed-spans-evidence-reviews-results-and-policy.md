# Work report 003-a — Typed spans, evidence, reviews, results and policy

```oap-report
{
  "id": "003-a",
  "result": "PARTIAL",
  "order_path": "oap/orders/003-a-typed-spans-evidence-reviews-results-and-policy.md",
  "order_sha256": "a68247a09f260a72a6f9554593e5196618bd59f8abc850e3657d9cdaa8be04e5",
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
  "implementation_head": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 4,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/4",
  "pr_state": "open",
  "branch": "oap/003-typed-spans-evidence-reviews-results-and-policy",
  "base_sha": "9f2d71533785e7505bdc1c2539040789d055d7de",
  "starting_remote_sha": "9f2d71533785e7505bdc1c2539040789d055d7de",
  "no_merge": true,
  "checks": [
    {
      "command": "pytest tests/contract/test_objective_003.py -q",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract -q",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "pytest -q",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "ruff check src tests/contract",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "ruff check .",
      "result": "FAILED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "mypy src tests",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 003-a",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 003-a",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 9f2d71533785e7505bdc1c2539040789d055d7de",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check 9f2d71533785e7505bdc1c2539040789d055d7de...HEAD",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "accepted-base protected-source diff",
      "result": "PASSED",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at final report head",
      "result": "PENDING",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at final report head",
      "result": "PENDING",
      "sha": "5ce260cd53fef5fb8cd447b3d9c258928ff69749",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T04:27:21+00:00",
  "report_written_at": "2026-09-08T04:28:09+00:00",
  "implementation": "Added strict frozen Pydantic v2 contracts for original-coordinate Unicode spans, bound selection batches, explicit evidence states and bounds, narrow reviewer proposals, original-coordinate edits, finite timings, result dispositions, and truthful result flags. Added PolicyConfig schema version 1 with detect_only default, bounded review/target/character/byte/code-point/queue limits, and immutable false settings for evidence-insufficient acceptance, production text storage, and experimental repair. The implementation head is 5ce260cd53fef5fb8cd447b3d9c258928ff69749.",
  "documentation": "Exported the stable contract and policy names from the package while retaining __version__ and py.typed. Updated README.md and STATUS.md to describe the implemented seam, Unicode offset convention, evidence states, finite defaults, and explicit non-capabilities. Updated only the required generated and installation inventory rows for the changed documentation.",
  "criteria": "Criteria 1-5, 7-10 are covered by the committed public models and synthetic tests. The focused suite passed 23 tests, contract suite passed 33 tests, full pytest passed 114 tests, OAP unittest discovery passed 81 tests, and the native baseline passed frozen sync, packaging, offline wheel installation/runtime import, Ruff, mypy, and cleanup. Transcript index/revision and accepted-runtime governance checks passed at the implementation head. The literal whole-repository ruff check was also run and failed on pre-existing OAP infrastructure findings outside this product order; the relevant scoped Ruff check and native baseline Ruff step passed, so this report is PARTIAL for that unresolved repository-wide diagnostic.",
  "negative_paths": "Synthetic validators reject stale, out-of-range, zero-length, duplicate, overlapping, and Unicode-slice-mismatched selections; inverted or denominator-exceeding evidence; fabricated exact zero; unavailable counts/cutoffs; inconsistent keep/replace/wider proposals; duplicate proposal IDs; NaN/infinite confidence or timings; identity/blank edits; inconsistent result flags, dispositions, coordinates, and edit slices; policy maxima, retry/concurrency, storage, experimental, nonfinite, and contradictory-bound violations.",
  "boundary_fidelity": "The contract boundary instantiates and validates real Pydantic models and keeps original text immutable within selection/result validation. No detector, tokenizer, corpus, morphology adapter, prompt serializer, JSON response parser, HTTP/model client, acceptance scorer, patch composer, pipeline, API, CLI, logging, live model, or production storage was implemented. No customer/model text, real corpus, Qwen, GPU, service, port, gateway, credential, network-setting, merge, release, or deployment action occurred.",
  "setup": "All temporary environments, caches, wheel artifacts, and offline installs were created under owned disposable /tmp paths. The committed lock was preserved and no dependency or ignored repository .venv was changed. The initial broad pytest run exposed generated README/STATUS inventory drift; the exact two inventory rows were reconciled, after which full pytest, OAP tests, and the native baseline passed.",
  "privacy": "Source, tests, and report contain only synthetic Unicode/count fixtures and finite policy labels. No customer text, prompts, replacements, raw reviewer responses, credentials, secrets, private responses, or private strategic contents were logged or committed.",
  "limits": "This is typed-contract and offline engineering evidence, not linguistic, model, live-Qwen, quality, ICA, milestone, release, deployment, or human-acceptance evidence. The repository-wide ruff failure is confined to pre-existing OAP files that this order does not own; it was not suppressed or repaired opportunistically. Final report-head CI checks and remote SELF verification are intentionally PENDING before publication.",
  "human_gates": "D0 with deferred human adjudication NONE. PR #4 is open and non-draft at implementation head 5ce260cd53fef5fb8cd447b3d9c258928ff69749; no merge or auto-merge was performed. Human owns any later review, merge, release, or deployment decision.",
  "scope": "Completed only the activated 003-a order on oap/003-typed-spans-evidence-reviews-results-and-policy from accepted base 9f2d71533785e7505bdc1c2539040789d055d7de. Published the exact order and active pointer, created sole PR #4, and prepared this report as the only remaining report commit. No later order, objective, strategic source, or private state was selected or changed."
}
```

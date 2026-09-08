# Work report 004-a — Source manifests and miniature synthetic corpus

```oap-report
{
  "id": "004-a",
  "result": "COMPLETE",
  "order_path": "oap/orders/004-a-source-manifests-and-miniature-synthetic-corpus.md",
  "order_sha256": "71131cfc2a17260768e9d6189a3a4ebb13f471660c7e39579c89b54e09ecbd06",
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
  "implementation_head": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
  "publication_verified": false,
  "pr_mode": "CREATE_NEW_PR",
  "pr": 5,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/5",
  "pr_state": "open",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "starting_remote_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "no_merge": true,
  "checks": [
    {
      "command": "pytest tests/contract/test_objective_004.py -q",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "pytest tests/contract -q",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "pytest -q",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "ruff check src scripts tests",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "mypy src tests",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-a",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-a",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "accepted-base protected-source diff",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline required CI at implementation head 2bc3cfb",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance required CI at implementation head 2bc3cfb",
      "result": "PASSED",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "Application baseline at final report head",
      "result": "PENDING",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    },
    {
      "command": "OAP bootstrap acceptance at final report head",
      "result": "PENDING",
      "sha": "2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T05:57:47+00:00",
  "report_written_at": "2026-09-08T05:57:47+00:00",
  "implementation": "Added frozen strict SourceManifest provenance contracts for source identity, release, acquisition reference, payload format/encoding, normalization/tagging, completeness/cutoff/threshold metadata, explicit denominator knowledge, rights/readiness, attribution, schema versions, and deterministic build parameters. Added frozen SyntheticCountRecord and bounded SyntheticCorpus models reusing EvidenceRecord, with exact word/bigram/trigram arity and synthetic source/scope enforcement. Added verify_manifest_payload and aliases for bounded UTF-8 JSON/JSONL loading, exact size/SHA-256 verification, duplicate-key/record rejection, safe repository-relative paths, symlink/type checks, and finite limits. Added four tiny project-authored records covering exact positive, justified exact zero, censored unknown-denominator, and unavailable evidence.",
  "documentation": "Exported the manifest, synthetic-record, verification, and failure-label APIs. Updated README.md, STATUS.md, and docs/DEVELOPMENT.md to describe the fixture and its limits. Reconciled the generated README/STATUS inventory and the scoped package export/wheel assertions. The test-only fixture is excluded from the installed runtime wheel.",
  "criteria": "All numbered 004-a acceptance criteria are covered by the implementation and focused negatives. The objective suite passed 19 tests, the contract suite passed 56 tests, full pytest passed 137 tests, Ruff and mypy passed, OAP unittest discovery passed 81 tests, and the locked native baseline passed all dependency, test, lint, type, build, offline-install, import, and cleanup stages. Both required remote CI checks passed at implementation head 2bc3cfb. The PR remains open and unmerged.",
  "negative_paths": "Coverage rejects blank or missing provenance, unknown fields, lowercase/invalid checksums, checksum and size drift, readiness contradictions, synthetic-rights mismatches, incomplete cutoff metadata, denominator-state contradictions, false synthetic labels, wrong token arity, non-synthetic evidence, traversal/absolute/dot paths, symlinks, non-files, oversized or malformed/invalid-UTF-8 manifests and payloads, malformed records, duplicate record IDs, duplicate JSON keys, unsupported formats, and blank JSONL lines. Failures expose only finite reason labels and bounded field metadata; payload contents are not echoed.",
  "boundary_fidelity": "The named boundary is the real public SourceManifest/SyntheticCountRecord model and explicit local verifier. Tests load the committed manifest and exact payload bytes through that boundary. No external corpus bytes, acquisition, query, importer, index, normalization transform, aggregation, detector, reviewer, patcher, pipeline, API, CLI, live model, Qwen, GPU, service, gateway, credential, network-setting, release, deployment, or merge action occurred.",
  "setup": "Verification used the committed uv.lock in owned native temporary environments under /tmp. The baseline created and cleaned fresh project and runtime-only environments, built sdist/wheel artifacts, performed frozen online-cache population followed by offline runtime installation, imported the installed package outside the repository, and completed cleanup. No repository .venv was used or changed and no dependency was added.",
  "privacy": "Source, tests, and report use only project-authored synthetic metadata, Slovenian-like tokens, counts, denominator states, and fixture paths. No customer text, prompts, replacements, raw reviewer responses, credentials, secrets, private responses, external corpus data, or private strategic contents were logged or committed.",
  "limits": "This is schema, checksum, bounded-file, and offline engineering evidence only. The fixture is not corpus or language-quality evidence. Real-source rights, access, release, format, acquisition, completeness, and linguistic benefit remain unverified; Qwen/live compatibility, production quality, ICA, milestone acceptance, release, and deployment remain unproven. Final report-head CI checks are intentionally PENDING until this SELF report is published and independently verified.",
  "human_gates": "Decision class D0 with deferred human adjudication NONE. PR #5 is open, non-draft, and unmerged at the verified implementation head; both required implementation-head CI checks passed. No merge or auto-merge was performed. Human retains review, merge, release, and deployment authority.",
  "scope": "Completed only active order 004-a on oap/004-source-manifests-and-miniature-synthetic-corpus from accepted main dac4789f52c9e82aec90d1cf92ce9f1194cc103a. Published the exact order and active pointer, implemented the listed manifest/fixture seam, added the listed regressions and documentation, created PR #5, and preserved accepted governance, CRITICAL, protected resources, and unrelated work. This report is intended to be the sole final round commit with implementation head 2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9 as its sole parent."
}
```

# Work report 007-i — Final canonical public-config correction

```oap-report
{
  "id": "007-i",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-i-validate-unique-one-letter-candidates-contextually.md",
  "order_sha256": "d5e554f4052984b6ad926cf95ca20cc58692371983915fe8e18c1768a11bf55f",
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
  "implementation_head": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "f7b45729d0a549b37d87e52932748ec03255b670",
  "no_merge": true,
  "checks": [
    {
      "command": "canonical config bytes, parsed-object equality, result configuration_sha256, and scientific identity comparison",
      "result": "PASSED",
      "details": "The existing parsed object is deeply equal before/after; canonical UTF-8 JSON bytes with ensure_ascii=false, sort_keys=true, indent=2 and one LF hash 8c04377331bf90f3c055d500df0b557845fbb0671e9be52dea9a2f478245c81f; compressed result claim matches; public result/report/private identity hashes and request-tree identity are unchanged.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "The public research tree passed with 138 files.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --staged-tree .",
      "result": "PASSED",
      "details": "The staged-byte public guard passed with 138 files and no private payload; the correction commit staged only the config path.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest research.tests.test_contextual_validator research.tests.test_research research.tests.test_one_substitution",
      "result": "PASSED",
      "details": "All 74 JSON/schema-sensitive and focused research tests passed.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 133 complete research tests passed; the expected synthetic worker traceback was contained by its test and the suite exited zero.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check HEAD^ HEAD; git diff-tree --no-commit-id --name-only -r HEAD",
      "result": "PASSED",
      "details": "The correction diff is whitespace-clean and changes exactly research/configs/007-i-contextual-validator.json.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "FAILED",
      "details": "The pre-existing numeric table is stale. It was not regenerated because this final correction forbids metric, registry, aggregation, and research-report changes; no scientific value was changed.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    },
    {
      "command": "git push origin oap/007-concept-verification; remote branch, PR #8, parent, and changed-path verification",
      "result": "PASSED",
      "details": "Correction head df427c3eb65d1d15ad3b4e4f13f36be18afa6721 is remote, has sole parent f7b45729d0a549b37d87e52932748ec03255b670, and PR #8 is OPEN/UNMERGED on the existing branch.",
      "sha": "df427c3eb65d1d15ad3b4e4f13f36be18afa6721",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-12T23:38:45+02:00",
  "report_written_at": "2026-09-12T23:40:00+02:00",
  "implementation": "Canonicalized exactly one public config file without changing its parsed object or any key/value. The correction head is df427c3eb65d1d15ad3b4e4f13f36be18afa6721. The prior scientific chain is retained truthfully: 007-h report head e916a2d9cafd171fbb71bfc70ac2c21222118f6e; 007-i live head e85600ffd91164440166ee33a20c3b84af50bfe6; aggregation head 752569d13d153ee6d16528f4b278a5a567e0b218; first public result publication head a95355020836af01c8a365e9b7bd0e43ceb2bedd; prior public metadata head f7b45729d0a549b37d87e52932748ec03255b670; final correction head df427c3eb65d1d15ad3b4e4f13f36be18afa6721. The aggregation incident identity remains 598b707790e303811faef0ccf15898686225947d19fce44352bde05f75984f39 with zero additional model/network calls and unchanged request-tree identity.",
  "documentation": "This immutable report records the final byte-level correction, exact artifact linkage, prior heads, the preserved aggregation incident, and the required verification results. No scientific or private evidence was regenerated or rewritten.",
  "criteria": "The actual config SHA-256 is 8c04377331bf90f3c055d500df0b557845fbb0671e9be52dea9a2f478245c81f and equals the compressed public result configuration_sha256. The public result SHA-256 remains e981e3802ad0fc0db2a32262ba4dfada160ee880d3a86538bd241e8a57241fb5; the public research report remains 317bfc9e9721819da73bcbc0365ec63c3f5aab7f884f96400709a6f0e0a59af2; private manifest/results identities remain 04f66e96d4feddaea520c1ccb27724dc5417b4f6535bbe85a5c6cac904395cb0 and 913572ae5d16ba29ab8afd6ea59a1dc3f03de90d40136891ea1637eba16f92f; candidate manifest identity remains 70544b1dec158f1e72cfaae8fb2547d9ba6ea22c3cd7934e0b7341bce8617854; request-tree identity remains 2,940 files, 4,651,774 bytes, digest d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945.",
  "negative_paths": "The parsed-object and result-link assertions reject key/value drift and hash mismatch. Public and staged guards reject private content and unsafe staged bytes. The 74 focused tests cover JSON schema, persistence, parser, projection, attribution, no-resampling and no-network boundaries; all 133 research tests pass. No aggregation, metric, model, or research network action was performed during this correction.",
  "boundary_fidelity": "Only research/configs/007-i-contextual-validator.json changed in the implementation commit; the final commit changes only this OAP report. No code, test, registry, result, research report, private evidence, metric, model, service, deployment, merge, release, or unrelated CI path changed.",
  "setup": "Reconciled the consumed SAME-ID 007-i state, active pointer, existing branch, remote branch, and open PR #8 before mutation. Pushed the single-file correction and independently checked its remote parent/path/head before composing this report. PR metadata required no separate body change because the branch head updated automatically.",
  "privacy": "No sentence, target, candidate, prompt fill, raw response, reasoning, credential, endpoint, profile path, private path, or private evidence body entered this report or Git. Only already-public aggregate/hash identities and incident counts are recorded.",
  "limits": "The exact correction is COMPLETE. The separately run numeric-table freshness check remains FAILED because the table is pre-existing stale state; regenerating it would violate the directive's no-metrics/no-registry/no-research-report boundary. This report makes no product, linguistic, release, deployment, or merge claim.",
  "human_gates": "D0 / NONE. CRITICAL remains empty. Coding did not merge PR #8, enable auto-merge, alter branch protection, release, deploy, or accept scientific/product results.",
  "scope": "Finished only the final same-ID canonical public-config correction. The implementation correction was committed and pushed first; this report is the immutable report-only commit whose sole parent is that exact correction head. After publication verification, send exact OK and stop.",
  "result_summary": "COMPLETE for the ordered final correction: the one public config is canonical, its parsed object and result linkage are unchanged and verified, required public/staged/focused/complete checks pass, the sole-file correction is remote, and the final report is ready for immutable publication verification."
}
```

## Result

The final 007-i public configuration correction is complete. Its canonical bytes
match the required SHA-256, the parsed object and scientific artifacts are
unchanged, and the existing open PR remains unmerged.

## Evidence and limitations

The required public/staged guards, focused tests, complete research suite, and
diff checks passed at the correction head. The numeric-table freshness check was
left unchanged because this round forbids metric, registry, aggregation, and
research-report mutations.

## Deferred human adjudication

- Decision: NONE

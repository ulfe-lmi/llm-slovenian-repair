# Work report 006-f — Support mixed terminal tab and prove import

```oap-report
{
  "id": "006-f",
  "result": "BLOCKED",
  "order_path": "oap/orders/006-f-support-mixed-terminal-tab-and-prove-import.md",
  "order_sha256": "af8c9b7a42d36df5153336e353480dfd657c93e651e8580d84485bb3c683c265",
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
  "implementation_head": "2a967fecaf650faa9c8459bf1b1913647384d274",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 7,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/7",
  "pr_state": "open",
  "branch": "oap/006-unigram-lexicon-importer",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "82231a627cceda9c8533a4f37b855aec13ed0873",
  "no_merge": true,
  "checks": [
    {
      "command": "PYTHONPATH=src /tmp/llm-slovenian-repair-006-f-env.wHXwyx/bin/python -m pytest tests/contract/test_objective_006.py tests/contract/test_objective_006_diagnostics.py -q",
      "result": "PASSED",
      "details": "68 focused importer and diagnostic tests passed, including both accepted row shapes, strict wider-shape negatives, deterministic hash binding, historical receipt distinctions, and content-free diagnostic contracts.",
      "sha": "3a536f2f9047c12156ea468ede5615005401ca2b",
      "publication_head_claim": false
    },
    {
      "command": "PYTHONPATH=src /tmp/llm-slovenian-repair-006-f-env.wHXwyx/bin/python -m pytest -q",
      "result": "PASSED",
      "details": "273 tests passed in 201.85s at the implementation worktree before the active-marker reconciliation commit; the tested tree is an ancestor of implementation_head.",
      "sha": "3a536f2f9047c12156ea468ede5615005401ca2b",
      "publication_head_claim": false
    },
    {
      "command": "/tmp/llm-slovenian-repair-006-f-env.wHXwyx/bin/ruff check src scripts tests",
      "result": "PASSED",
      "details": "All checks passed.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "/tmp/llm-slovenian-repair-006-f-env.wHXwyx/bin/mypy src tests",
      "result": "PASSED",
      "details": "Success: no issues found in 11 source files.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m unittest discover -s oap/tests -q",
      "result": "PASSED",
      "details": "All 84 OAP governance and process-boundary tests passed at the final implementation head.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300",
      "result": "PASSED",
      "details": "All 13 supported temporary-environment stages passed, including lock/sync, focused/full pytest, Ruff, mypy, OAP tests, builds, offline runtime checks, and cleanup.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 006-f",
      "result": "PASSED",
      "details": "Active 006-f is the latest order and all historical orders/reports are coherent in the index.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 006-f",
      "result": "PASSED",
      "details": "The committed implementation transcript is coherent at the final implementation head.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Accepted-runtime governance structure is valid; semantic and human-authorization proof remain false.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c...HEAD",
      "result": "PASSED",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "protected-tree diff exit check against accepted base",
      "result": "PASSED",
      "details": "No protected law, architecture, CRITICAL register, source lock, governance, or bootstrap source changed.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Repository object integrity check completed without diagnostics.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "one 006-f curl --disable direct HTTPS GET, accepted verifier, bounded selected-member smoke harness, and exact owned temporary-tree cleanup",
      "result": "BLOCKED",
      "details": "Exactly one 006-f GET completed and cumulative objective GET count reached eight. The accepted verifier passed with the canonical 115865656-byte archive, publisher MD5, archive SHA-256, five members, and total uncompressed size 1487654024. The smoke harness then failed with a syntax error before selected-member access; no structural rows, importer runs, input/output hashes, or real compatibility result are claimed. The owned source tree was deleted and no external bytes were retained; no retry was made.",
      "sha": "3a536f2f9047c12156ea468ede5615005401ca2b",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions Application baseline at implementation head (run 34256092815)",
      "result": "PASSED",
      "details": "Remote required check completed successfully at head 2a967fe.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Actions OAP bootstrap acceptance at implementation head (run 34256092818)",
      "result": "PASSED",
      "details": "Remote required check completed successfully at head 2a967fe.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    },
    {
      "command": "Independent remote branch/PR head verification before report publication",
      "result": "PASSED",
      "details": "PR #7 is open on 2a967fe, base main, with no merge; both required checks are successful.",
      "sha": "2a967fecaf650faa9c8459bf1b1913647384d274",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-08T17:17:54Z",
  "report_written_at": "2026-09-08T17:18:43Z",
  "implementation": "Commits 3a536f2f9047c12156ea468ede5615005401ca2b and 2a967fecaf650faa9c8459bf1b1913647384d274 implement the evidence-fixed parser correction. Data rows accept exactly the observed 28 quoted fields ending at CRLF or those fields plus one empty terminal tab, bound as OPTIONAL_SINGLE_EMPTY_TAB_BEFORE_CRLF; semantic records remain 28 fields and input hashes remain byte-sensitive. Synthetic tests cover the mixed stream, equal semantic/output hashes with differing input hashes, and strict wider-shape rejection. The required real smoke is BLOCKED before member access by the harness syntax failure, so no product commit guess or real-import result is claimed.",
  "documentation": "Current data-source and development docs supersede the 006-c mandatory-tab wording with the optional single empty terminal tab contract and explicitly record that 006-f's one verifier-first fetch passed but its smoke harness failed before member access. The new receipt records cumulative eight GETs, canonical verifier facts, prior 006-a–e distinctions, cleanup, non-retention, and null unobserved smoke fields. Historical orders, reports, and receipts were not rewritten.",
  "criteria": "Criterion 1 PASSED for the bounded offline importer contract: exactly the two evidenced terminator shapes pass, all wider/malformed/semantic extensions fail, semantic records stay at 28 fields, and the optional byte changes input hash but not canonical output hash. Criterion 2 BLOCKED: exactly one 006-f fetch passed accepted artifact verification, but the smoke harness failed before selected-member access, so the required 32-row structural aggregate and twice-run real importer evidence are null. Criterion 3 PASSED for truthful receipt structure, cumulative eight, preserved prior incidents, no content/retention, cleanup, and redistribution false. Criterion 4 BLOCKED overall by the ordered real smoke; final local tests, governance, transcript, fsck, and both required CI checks passed, and PR #7 remains open and unmerged. This is not a claim of full-source import, linguistic benefit, release, deployment, or milestone acceptance.",
  "negative_paths": "Focused tests exercise the actual importer for header terminal tabs, missing/repeated/spaced terminal tabs, quoted and unquoted extra fields, embedded tabs, malformed quoting, invalid UTF-8/control/surrogate input, truncation, strict newline, duplicate/conflicting records, count/decimal/zero semantics, provenance, limits, stable hashes, and historical receipt distinctions. The real action made no second GET, retry, member read, importer call, source-content output, per-row hash output, or external-byte retention.",
  "boundary_fidelity": "Only the active 006-f order, its receipt/report paths, the importer, objective-006 contract tests and fixture documentation, current data/development docs, and generated hash projections changed. The active pointer was explicitly reconciled from worktree 006-f to committed 006-f. Protected law, PLAN, full architecture, CRITICAL, dependencies, source inventory, Qwen/GPU/services/gateway, network settings, neighboring repositories, and merge/release/deployment boundaries were unchanged.",
  "setup": "The consumed handoff was reconciled to the same 006-f branch and existing PR #7; no second control wait, new suffix, or new PR was used. The repository .venv was not used or repaired. Locked dependencies ran in an owned disposable /tmp environment, which was removed; the source action used curl --disable, direct HTTPS without redirects or credentials, connect timeout 10 seconds, total timeout 900 seconds, max-filesize 115865656, and one owned .part path. Accepted verification preceded the attempted smoke, and the exact source tree was deleted after the harness failure.",
  "privacy": "The committed report and receipt contain no source row, header value, raw external text, prompt, model response, customer text, credential, secret, or private strategic content. They retain only canonical integrity identifiers and bounded aggregate/status facts required by the order.",
  "limits": "The importer retains finite input, line, field, row, and field-count bounds and the exact 28-field semantic model. The source action reached verifier success only; structural sample count, row aggregate, importer attempts, input hash, output hash, and real compatibility status remain unobserved and null. `publication_verified` is false because this pre-push report cannot claim its own future publication verification.",
  "human_gates": "Decision class D0 with Deferred human adjudication NONE. No CRITICAL append or human disposition was made. PR #7 is open and unmerged against main; strategy retains review and development-merge authority, while human intent, rights, release, deployment, and milestone authority remain unchanged.",
  "scope": "Executed only active order 006-f on the existing objective-006 branch and PR #7. Implementation head 2a967fecaf650faa9c8459bf1b1913647384d274 was pushed and remotely checked before report composition. This final publication commit must contain only this report and have the implementation head as its sole parent. After publication verification, no later mutation, merge, retry fetch, release, deployment, or future-CI claim is authorized by this report."
}
```

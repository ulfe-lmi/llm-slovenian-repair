# Work report 007-c — Preserve and publish the complete research trail

```oap-report
{
  "id": "007-c",
  "result": "PARTIAL",
  "order_path": "oap/orders/007-c-preserve-and-publish-the-complete-research-trail.md",
  "order_sha256": "388cf70b15624b248394d02c8ead89ab51dc317353dbeae999cc321209752740",
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
  "implementation_head": "1b017a76ddb33c6a1d3af28233d6331067f88a9b",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "51c0a0bb7a96fde72b7d58e503e816eb99f8e3ec",
  "no_merge": true,
  "checks": [
    {"command": "python3 -B -m unittest discover -s research/tests -v", "result": "PASSED", "details": "22 focused research tests passed, including actual detector/protection, English eligibility, strict proposal/retry schema, case/unigram gate/patch replay, staged publication export negatives, short overlap detection, duplicate-key rejection, evidence-derived status, numeric projection, and no-retry failure semantics.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.replay --scratch PERSISTENT_SCRATCH", "result": "PASSED", "details": "Synthetic replay executed the actual detector, English policy, gate, case restoration, and patch boundaries with two detector candidates, one review-eligible candidate, zero retry calls, zero network calls, and zero model calls.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.replay --private-case PRIVATE_VARIANT_ROOT/runs/01/cases/h01.json --index PRIVATE_PERSISTENT_INDEX", "result": "PASSED", "details": "One preserved ten-run case replayed against the explicit persistent native index. Detector, English evidence, saved proposal, case rule, unigram gate, exact patch, and saved output matched; zero model/network calls.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.replay --private-root STRATEGIC_HOME --manifest research/registry/file-census.json.gz --limit 100", "result": "PASSED", "details": "The compressed exact census was decoded and the first 100 private/duplicate identities matched their preserved native bytes; 225,632 additional entries remained explicitly unverified by this bounded receipt.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.build_public_registry --repo-root . --strategic-home STRATEGIC_HOME --existing-census PRESERVED_INTERRUPTED_CENSUS", "result": "PASSED", "details": "21 catalog records, 20 enumerated roots, 225,757 exact file-level entries, 25 curated/redacted mappings, 211,138 private-only entries, 14,594 duplicate-linked entries, nine compressed numeric projections, evidence-derived statuses, and zero curation calls.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.rebuild_tables --check", "result": "PASSED", "details": "The committed data-free experiment summary table rebuilt byte-identically from the registry.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m research.tools.publication_guard --root research --staged-tree MATERIALIZED_INDEX/research --private-root PREPARED_EVALUATION_SOURCE", "result": "PASSED", "details": "Exact intended Git tree 3c131a6ec21a6bbf35a59e1480986f4ce70651fc passed public schema/private-field/archive/path checks and the actual prepared-source short/16-token overlap scan. No dataset/private overlap was found.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "PYTHONPATH=src python3 -B -m pytest -q", "result": "FAILED", "details": "343 passed and 4 inherited failures after the source-layout rerun. Failures were installed import isolation, lazy dependency access, wheel dependency environment, and unigram preflight dependency availability; no research test failed and no product/lock/production file was changed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m pytest -q", "result": "FAILED", "details": "Initial native collection failed because the shell did not expose the installable source package; the source-layout rerun above is the discriminating result.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B -m unittest discover -s oap/tests -v", "result": "PASSED", "details": "All 104 OAP bootstrap, state, FIFO, transcript, history, governance, process-boundary, and recovery tests passed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B oap/bin/check_transcript.py --repo-root . --index --expected-id 007-c", "result": "PASSED", "details": "Active index is coherent with 007-c as latest order and 007-b as latest published report.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-c", "result": "PASSED", "details": "Implementation-head transcript is coherent before report publication.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest", "result": "PASSED", "details": "The two known historical report incidents remain frozen and no report was mutated.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c", "result": "PASSED", "details": "Accepted-runtime governance is structurally valid; semantic and human-authorization proofs remain false.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "python3 -B oap/bin/check_governance.py --repo-root . --mode candidate-review --allow-change research --allow-change .github/workflows/research.yml --allow-change oap/orders/007-c-preserve-and-publish-the-complete-research-trail.md --allow-change oap/active", "result": "PASSED", "details": "Candidate changed paths are within the exact ordered scope.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "git diff --check ee2d1b479719009ff1d07829478f241e3f395f7c HEAD", "result": "PASSED", "details": "Implementation history has no whitespace errors.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "protected-source diff against ee2d1b479719009ff1d07829478f241e3f395f7c", "result": "PASSED", "details": "Product, scripts, existing tests, locks, governance, and protected sources are byte-unchanged; only allowed research/order/active/workflow paths changed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "git fsck --full --no-reflogs", "result": "PASSED", "details": "Repository object check passed; expected dangling scratch blobs/trees were not cleaned.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "ruff check research", "result": "MISSING", "details": "Ruff is not installed in the native shell; offline uv resolution did not complete, so no Ruff result is claimed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "mypy research", "result": "MISSING", "details": "Mypy is not installed in the native shell; offline uv resolution did not complete, so no mypy result is claimed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false},
    {"command": "git ls-remote origin refs/heads/oap/007-concept-verification and gh pr checks 8", "result": "FAILED", "details": "Remote branch and PR head matched implementation 1b017a76ddb33c6a1d3af28233d6331067f88a9b; PR #8 is open/non-draft/unmerged. Research reproducibility, OAP bootstrap acceptance, and OAP report history passed. Inherited Application baseline failed.", "sha": "1b017a76ddb33c6a1d3af28233d6331067f88a9b", "publication_head_claim": false}
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-11T17:19:50+00:00",
  "report_written_at": "2026-09-11T17:21:00+00:00",
  "implementation": "Implemented the complete research-preservation projection within research/**: an evidence-derived catalog for all identified roots and nested stopped/recovery artifacts; exact private file census/dispositions; source-to-curated mappings; safe per-case numeric projections, retry ablations, category/type summaries and paired bootstrap records; and archive/retention metadata. The registry derives statuses and final-campaign totals from preserved records rather than order prose constants. The Levenshtein item is recorded as a single diagnostic, not a benchmark.",
  "documentation": "research/README.md is a navigable entry point with chronology, every experiment ID, variant distinctions, actual final-campaign totals, findings/limits, reproduction commands, retention policy, and public/private schema. Curated modules preserve the actual protected-span, corpus evidence, hyphen-view detector, English-preservation, contextual/retry, case-restoration, unigram-gate, patching, adapter, transport, official-score, and custom-metric seams with explicit resources. CI adds only the CPU-only Research reproducibility check.",
  "criteria": "PARTIAL but truthful: the public catalog has 21 records over 20 roots and a complete 225,757-entry exact census; all preserved public numeric projections are data-free and reproducible offline; actual replay boundaries and publication negatives pass. The inherited Application baseline remains failed, Ruff/mypy are unavailable, remote scoring remains pending/access-blocked, and private replay was bounded to a representative preserved case rather than a full campaign traversal.",
  "negative_paths": "Research tests and the preserved strategic regressions reject duplicate proposal keys, malformed schemas, protected/stale/overlapping edits, retry-only versus first-stage failures, hidden English-policy calls, forbidden JSON fields and credential canaries, archive/raw/binary artifacts, path traversal, internal/escaping symlinks, overwrite/export races, short private-text overlap, and stale worktree versus staged-byte scans. The guard validates actual intended staged bytes before publication.",
  "boundary_fidelity": "Only the exact 007-c order/active paths, research/**, and .github/workflows/research.yml changed. Existing concept-verification/**, src/**, scripts/**, tests/**, pyproject.toml, uv.lock, production/governance sources, earlier orders/reports, service/GPU/network/gateway/ports, and private native archives were not changed. No model, dataset acquisition, experiment rerun, production change, merge, release, or deployment occurred.",
  "setup": "The consumed durable marker was reconciled as same-ID 007-c recovery on branch oap/007-concept-verification and PR #8. The interrupted 111 MB census was preserved in the inherited persistent scratch and reclassified mechanically; no broad cleanup or reset was used. All new scratch/fixtures used the inherited persistent TMPDIR. Private replay used explicit persistent native roots and read-only index access.",
  "privacy": "No dataset sentences, translations, filled prompts, raw request/response bodies, reasoning, traces, credentials, corpus/index bytes, or private host/profile paths were committed or included in this report. Public numeric rows retain only data-free IDs, hashes, counts, timings, statuses, categories/types, and uncertainty metadata. The guard and actual prepared-source overlap scan passed against the intended staged tree.",
  "limits": "The full existing pytest suite has 343 passes and four inherited dependency/preflight failures. Ruff and mypy could not be run because native tools and offline cached resolution were unavailable. The final campaign's remote/Scribendi scoring is access-blocked; Deployment B is excluded. Complete private replay of every preserved final-campaign trace was not attempted because the stored payloads remain private and the bounded replay receipt covers one representative case. No human semantic labels, linguistic benefit, replication, product correctness, merge readiness, release, or deployment authority is claimed.",
  "human_gates": "D0/NONE; CRITICAL is empty. The owner-authorized archival/publication scope is followed, but no human semantic adjudication or product/milestone acceptance is inferred. Coding did not merge, enable auto-merge, repair the inherited baseline, select a new suffix/objective, or claim release/deployment authority.",
  "scope": "Finished only active 007-c on the existing PR #8: one pushed implementation commit 1b017a76ddb33c6a1d3af28233d6331067f88a9b, current PR metadata, and this sole pending immutable report. The implementation is pushed and independently observed at the exact remote head. This report is the only remaining round mutation; the final commit must change only this exact report path, have the implementation commit as its sole parent, be pushed once, independently verified, then followed by exact OK and exit.",
  "result_summary": "PARTIAL / research archival publication complete at the implementation boundary, with inherited application and unavailable-tool limitations explicit. PR #8 remains open and unmerged; no product or linguistic acceptance is claimed."
}
```

## Result

007-c publishes a coherent, data-free projection of the actual preserved
research trail. The source closure and offline replay exercise the scientific
boundaries that generated the records; the exact originals remain privately
retained. The result is a truthful archival PARTIAL because inherited baseline,
tool availability, remote scoring, and bounded private-replay limitations remain.

## Deferred human adjudication

- Decision: NONE

# 013-a — Mandatory Pandoc protection in the runnable proxy

Status: FINAL. Objective 013; CREATE_NEW_PR; phase RUNNABLE_PROXY_PROTECTION.

## Identity

013-a; mandatory Pandoc structural protection with exact original spans. FINAL; one new branch `oap/013-pandoc-original-span-protection`, CREATE_NEW_PR with no existing PR.

## Current verified state

Repository `ulfe-lmi/llm-slovenian-repair`, default branch `main`, accepted base and governance revision `3549de2a436f485a693730d0ee7d5f8c00aec0c0`. Migration PR #14 merged at that revision on 2026-10-26 after all four required final-head checks passed at ff99add3c5c92c0d6636e6274c49663085b7b11d. Both migration reports and original 011 ancestry remain preserved. Local main fast-forwarded cleanly; private governance refreshed with backups and reread. Existing foreground agent is idle; no new agent or control replay.

Preserve `corpus/`, `.research-test-scratch/`, `.rclone-speed-test/`, existing ignored environments including the separately backslash-named residue, all prior orders/reports, archive/private restoration and frozen science. PR #13 remains untouched. The recreated ignored .venv deviation is recorded, not claimed restored.

## Governance

Exact accepted source/compact identities are in metadata. PLAN, ARCHITECTURE, CRITICAL, governance, source lock and bootstrap seeds remain byte-identical. Relevant architecture excerpts §§6,7,12,14 may be read for this bounded task; normal compact coding read set otherwise applies. All LR-001 through LR-014 remain binding; relevant IDs are listed below. CRITICAL has no actual entries; no new judgment debt or milestone gate.

## Provenance

H: direct owner decision to use Pandoc as the runtime structural parser, exact-original-span constraints, foreground-only workflow and runnable-proxy scope. A: PLAN exact-span/protected-content intent and ARCHITECTURE §7 context boundaries. E/I: actual current proxy wiring and existing protection/patch tests; actual installed Pandoc 3.7.0.2 source-position probes recorded privately without customer data.

## Goal and dependencies

Replace the runnable proxy's structural protection path with mandatory installed Pandoc and validated original coordinates, while retaining conservative machine-content protection and original-slice patching. Dependency 012 is accepted. This is engineering work, not research evaluation or milestone closure.

## Scope

Exact allowed implementation paths:

- `concept-verification/protected.py`, new `concept-verification/pandoc_protection.py`, new `concept-verification/protection_residuals.py` only if needed to isolate existing pure residual policy.
- `concept-verification/proxy.py`, `concept-verification/repair.py`, `concept-verification/detector.py` only the ordered context-barrier helper, `concept-verification/config.py` only bounded parser configuration.
- `concept-verification/run_proxy.sh`, `concept-verification/README.md`, new `concept-verification/install_pandoc.sh`, new `concept-verification/pandoc-dependency.json`.
- `concept-verification/tests/test_concept.py`, new `concept-verification/tests/test_pandoc_protection.py`.
- `.github/workflows/application-baseline.yml` only pinned dependency installation for actual Pandoc integration tests; retain all current checks/guards/triggers/timeouts.
- `README.md`, `docs/DEVELOPMENT.md`, `STATUS.md` only directly affected setup/status.
- `research/RESEARCH-STATE.md` only established report counter 62 to 63 for final publication; no scientific or registry edits.
- Affected `oap/GENERATED-FILES.json` pins, this order, active pointer and final 013-a report.

No other paths or governance changes. Pure residual semantic rules may be reused as additional conservative protection, never structural-parser fallback. Frozen research behavior/artifacts remain unchanged.

## Files and boundaries

Inspect actual entry points: run_proxy.sh -> proxy.py:main -> RepairEngine.repair -> protected_intervals/detect/accept/apply_edits. The current proxy imports its own legacy regex protector; historical parser-first research uses pulldown-cmark. Ensure the selected runnable proxy depends on Pandoc and never discovers or invokes a historical pulldown helper. Inspect the existing concept tests and named research protection tests below before implementing; distinguish the full-link proxy policy from historical research label exposure.

## Non-goals

No research collection, labels, model call, scoring/prompt/model change, corpus acquisition, live service/port/network change, deployment, new milestone gate, parser substitution, AST rendering, frozen research rewrite or unrelated refactor. No new coding agent; only the existing foreground agent.

## Requirements

1. Inventory actual proxy call chain before implementation; eliminate regex-only runtime structural path and any pulldown runtime requirement for selected runnable proxy. Preserve frozen historical research separately.

2. Use explicit Pandoc3.7.0.2 installation/version contract unless evidence warrants exact reviewed version change; executable presence/version/capability startup check before accepting traffic.

3. Fix explicit CommonMark reader extension set supporting established code/math/HTML/link/metadata semantics; no silent dialect drift.

4. Prove sourcepos interpretation on actual installed binary; map lines/columns to exact original codepoint boundaries and preserve UTF8 original slices. NFD normalization, tabs, CRLF/bareCR, combining marks, emoji, missing/discontinuous sourcepos, repeated strings, escapes/entities and nested syntax are required probes.

5. No substring matching for position recovery and no AST-to-Markdown answer rendering. Only validated original-coordinate edits applied with unchanged unapproved slices.

6. If any region mapping is unprovable leave region protected; if global parsing/mapping integrity fails return original answer with zero review calls. Never expose uncertain regions.

7. Keep code/equations/HTML/link destinations/images/config/machine fragments protected with established residual semantic rules applied only after Pandoc grants structurally safe prose; residual recognizers are not an alternate structural parser.

8. Finite input/output/timeout limits; subprocess argv not shell; no untrusted filters or file/network reads; bounded non-content error diagnostics.

9. Reuse existing proxy/protection/patch tests; run actual Pandoc rather than mocks for mapping and positive integration. Place fake reviewer outside boundary. Verify missing/wrong-version/timeout/nonzero/malformedAST/map-failure negatives and byte-exact failclosed original.

10. If Pandoc cannot meet useful exact span safety, stop that dependent implementation and present minimal concrete failing case and smallest viable alternative before changing parser/protection contract.

11. Keep tests isolated from protected live endpoints; use synthetic documents and local fake reviewer/upstream at boundaries. Do not launch or replace a live proxy or change occupied ports.

12. Document parse/map failure must short-circuit RepairEngine.repair before Corpus/detect/reviewer, returning exact completed original. Test actual proxy/engine boundary with a reviewer that fails if called and a corpus open sentinel. Existing upstream capture errors remain errors; do not broaden exception handling around incomplete main responses.

13. Preserve the actual proxy's complete link/image protection (including labels), code, equations, HTML, configuration fragments, identifiers, paths and other established machine-sensitive regions. Historical research label-exposure expectations are a distinct policy and remain unchanged. Reuse the existing malformed Markdown, Unicode, code, math and exact-patch cases through actual Pandoc/proxy boundaries.

14. Preserve context barriers at both detector and acceptance. Current acceptance selects adjacent filtered tokens without checking intervening protected content; authorize only the smallest barrier-aware neighbor fix. Add candidate bounds/original-slice equality validation before acceptance to reject stale coordinates. Do not alter linguistic evidence thresholds or prompts.

15. Define useful positive coverage, including NFC Slovenian text with and without final LF, emoji prefixes, lists/emphasis and prose around protected content. Conservative abstention outside a documented proven input subset is permitted. Universal abstention is not implementation success.

16. Reject edits splitting grapheme-sensitive sequences; NFC alone does not exclude combining marks, variation selectors or ZWJ sequences. Add focused preservation cases and conservatively protect unproved targets; no new linguistic/NER programme.

## Concrete mapping evidence to resolve

- Actual Pandoc 3.7.0.2 with commonmark_x+sourcepos-smart normalizes decomposed e + combining acute: later columns shift relative to original. Never normalize the answer silently; prove an explicit map or conservatively abstain.
- Tabs, CRLF/bare CR, NUL replacement, entities/escapes and duplicate words need explicit coordinate validation. Unicode LS/PS/NEL/formfeed do not follow Python splitlines conventions in the observed parser; wrong repeated-word matches must fail closed.
- User attributes can duplicate data-pos. Generated position provenance must be established; never collapse duplicate attributes and trust the last value.
- Ordinary no-final-LF paragraphs can have virtual container endpoints: Beseda has paragraph 1:1-2:1 but exact leaf 1:1-1:7; a one-line list can have an outer endpoint at3:1. Do not blindly clamp coordinates to EOF or reject all useful no-final-LF prose. Container traversal/context and editable leaf mapping may be distinct; any virtual endpoint handling must be explicit and tested.
- Inline HTML can contain inner Str nodes between RawInline tags. Structural leaf presence alone does not authorize editing the machine-sensitive fragment.

Prefer deny-by-default prose grants from supported structures with validated original-indexed slices, then protect the complement and apply conservative residual rules. Original whitespace/glue may be granted only within a proven shared prose context, never across protected nodes or structural barriers. This is design guidance, not proof: actual installed-binary tests must establish safety.

## Dependency contract

Observed local binary: /usr/bin/pandoc3.7.0.2 (Debian3.7.0.2+ds-1). Official Linux amd64 3.7.0.2 release archive is33,678,610 bytes, SHA2568f8f67fdd540b6519326b0ac49d5c55c5d5d15e43920e80a086e02c8aff83268, from https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-linux-amd64.tar.gz (release https://github.com/jgm/pandoc/releases/tag/3.7.0.2). This is a locally computed HTTPS download checksum, not an upstream signature attestation. Pin installation/version explicitly; no runtime download. Local Debian and official static builds are not assumed behavior-identical merely from version strings: actual mapping/protection tests run on the selected local binary and CI distribution. Startup checks version and required reader capability before accepting traffic.

## Acceptance criteria

A1: actual runnable proxy requires qualified Pandoc at startup, with explicit installed dependency and no historical discovery/fallback.
A2: actual Pandoc positive cases prove useful exact original spans; trap cases prove unchanged unprovable regions or whole-document abstention.
A3: malformed Markdown, Unicode, code/math/HTML/links/configuration and every unapproved slice remain protected; no artificial adjacency at detector or acceptance.
A4: actual RepairEngine parse/map failure returns only safely completed original, before corpus access/detection/reviewer; missing/wrong-version/startup errors and runtime timeout/nonzero/malformed AST cases are explicit. Upstream incomplete/error semantics remain unchanged.
A5: original-slice patching rejects stale, overlapping, out-of-bounds and protected edits; no Markdown regeneration.
A6: focused actual-Pandoc/proxy tests and applicable broader required final-head CI pass, with exact tested revisions and limitations. Historic skipped pulldown tests are not Pandoc evidence.

## Verification

Use the existing external Python 3.12 environment, not bare `uv run` or repository .venv. Run `python -B -m pytest -p no:cacheprovider concept-verification/tests/test_concept.py concept-verification/tests/test_pandoc_protection.py` with the qualified actual Pandoc binary. Missing dependency must fail, not skip these integration tests. Reuse tiny SQLite and HTTP fixtures; reviewer/upstream fakes stay outside parser/mapper/RepairEngine. Test actual startup before HTTP bind and ephemeral HTTP requests through ConceptProxy; never start the configured live endpoint.

Run existing `research/tests/test_parser_first_protection.py`, `test_raw_document_fragment_protection.py`, `test_008h_dialect_edge_protection.py`, `test_008i_composition_and_class_boundary.py` unchanged through unittest discovery (`python -B -m unittest discover -s research/tests -p '<exact filename>'`). Report missing historical optional-helper skips honestly; those are not Pandoc proof. Reuse relevant malformed Markdown, Unicode/code/math and original-patch fixtures in actual Pandoc tests.

Run Ruff on changed Python and applicable existing type checks; `python -B -m unittest discover -s research/tests -p test_research_state_consistency.py` verifies report bookkeeping (62 before report, 63 after). Validate generated pins, protected-source/scientific diffs, `git diff --check`, transcript/report publication and accepted-runtime governance. Required final-head CI: Application baseline, Research reproducibility, OAP bootstrap acceptance, OAP report history. CI supplies full baseline/OAP coverage; do not repeat the approximately 54-minute native baseline solely to relabel a tested SHA. Stage all authorized implementation changes explicitly; candidate tests retain dirty-candidate limitations.

## Local setup and constraints

Only the existing foreground coding agent implements; OAP_ROLE=coding explicitly for helpers. No subagent/background model/codex exec/new pane/provider change. If the agent dies, only the exact owner launch `codex --yolo --profile early-beta` in the coding directory is permitted. Control is consumed externally once; do not wait for it inside the model. Preserve launched CODEX_HOME/auth.

Use owned temporary directories, external Python 3.12, PYTHONDONTWRITEBYTECODE=1, REPAIR_ALLOW_LIVE_TESTS=NO and bounded test processes. Existing /usr/bin/pandoc may be qualified read-only; official pinned archive installation is permitted only to an owned project/test or CI prefix, without sudo/system replacement. No runtime downloads, historical research directory search or regex fallback. No live Qwen/GPU/service/network/VPN/firewall/credential changes. No real customer data or content-bearing logs/reports. Synthetic fixtures only; do not bind occupied port18024. Preserve all ignored/unrelated local work.

## Documentation

Document the exact reader profile, original-coordinate mapping/provenance checks, supported subset and conservative abstentions, dependency pin/installation/startup and bounded failure behavior. Preserve source text; distinguish actual proxy integration from frozen research. Do not claim linguistic/MVP/deployment acceptance.

## Git and report publication



Document reader profile, supported coordinate conventions, abstention limitations, dependency installation/startup behavior and tested boundaries. Preserve protected source/governance bytes unless exact later authorization requires otherwise. No invented human acceptance or new judgment debt.

Normal implementation commits on one new branch/PR; coding never merges or enables auto-merge. Stage all authorized paths explicitly. Concise report with literal implementation SHA and SELF, report-only sole-parent publication, actual remote verification and one response OK. Candidate tests retain actual starting SHA plus dirty-candidate limitation; final report-head CI is post-publication strategic evidence. Required pending/cancelled checks block merge, not permission to claim a pass.

## Decision classification

D0 engineering within the direct owner parser decision. If useful exact-original-span safety cannot be established, preserve concrete minimal failing case and recommend the smallest viable alternative before any parser substitution or weakening of protection. Do not cross deployment or protected-service boundaries.

## Deferred human adjudication

- Decision: NONE

## Metadata

```oap-metadata
{
  "id": "013-a",
  "title": "Mandatory Pandoc structural protection with exact original spans",
  "objective": "013",
  "status": "FINAL",
  "phase": "RUNNABLE_PROXY_PROTECTION",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "governance_ref": "3549de2a436f485a693730d0ee7d5f8c00aec0c0",
  "branch": "oap/013-pandoc-original-span-protection",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "012"
  ],
  "local_work": "Preserve all prior branches/orders/reports, frozen research, restored archive files, ignored environments and untracked corpus/, .research-test-scratch/, .rclone-speed-test/. Tracked main clean before order publication.",
  "prior_review": "012-a and 012-b independently reviewed; PR14 normal merge 3549de2 from ff08d6e and reviewed ff99add; all four required final-head CI passed. Accepted governance refreshed with backups and reread; no deployment or scientific acceptance.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner decision: mandatory installed/versioned Pandoc runtime structural parser, exact original spans, no rendering or ambiguous substring mapping; fail closed; foreground-only coding; runnable proxy scope."
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE sections6,7,12,14; exact original spans, protected content/context boundaries, independent acceptance and bounded capture/error semantics."
    },
    {
      "kind": "E",
      "reference": "Inspected concept-verification proxy/protected/repair/detector and existing tests at accepted main; actual Pandoc3.7.0.2 probes show NFD shifts, virtual container endpoints, duplicate sourcepos attributes and Unicode line traps."
    },
    {
      "kind": "I",
      "reference": "Strategic call-chain/protection inspection and private pandoc-source-position-probes.json, pandoc-additional-structural-probes.json, pandoc-unicode-line-probes.json, pandoc-eof-position-probes.json."
    }
  ],
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "313d77900f9bbf1c974e76ea3f546083b117eeaac5f5fc2e964e77b3c19b9ccc",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "d10f9a0d673bd84f91a27f4f24b8505bf966e3eb5825bdfbd9404e1385b6681e",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "db624bb41b34d8263bc5745083d86e7db5bb8907816cd8725871e7225eb6ce9d",
    "oap/governance/DISTILLATION-MAP.md": "eeaf84b26e39c1cadd5d375d8d40f21b62bcf607a18472cd426d13656d5d3e62",
    "oap/governance/WORKSPACE-LAYOUT.json": "90f8b69f4054dffb4d93313da54841ccfddafdca511b86604765d51b63631d16",
    "oap/prompts/coding-round.md": "c682b1bbe016429bf4712a4174ae5ca4ec8b78ab36ebbc2c9b3ce625d83d3ffd",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "ba91f90ef1a8692472661900f1f91faacafa1a47954222c0e75e2f9d9752f6ae",
    "oap/strategic-instructions/AGENTS.md": "c08be7ea6f50ff218948e06ca942d40ce370b041f3580035a4f8ae8ef37c8221",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "83c87a5277ca798609422927e47caa2babab2cf555824813cbbe7f4ac2531ea5",
    "oap/strategic-instructions/strategic_model_init_material.md": "ac972d8e5fcd58b263df11d044aafed9fb1017d2173157d829fbc2953a1ba3b6"
  },
  "lr": [
    "LR-001",
    "LR-002",
    "LR-003",
    "LR-006",
    "LR-007",
    "LR-011",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "Application baseline",
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history"
  ],
  "decision_class": "D0"
}
```

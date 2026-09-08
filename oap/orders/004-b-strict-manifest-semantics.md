# Work order 004-b — Strict manifest semantics

Status: FINAL

```oap-metadata
{
  "id": "004-b",
  "title": "Strict manifest semantics",
  "objective": "004",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 5,
  "dependencies": ["003"],
  "local_work": "Clean objective branch at remote 004-a report head f38f9618c0820eb68b462e43242ea0cd22efe945; preserve 004-a and all prior commits/reports plus ignored environments and private strategic state.",
  "prior_review": "004-a remote SELF and both final-head checks verify, but direct final-head probes accept a rights alias, non-UTF-8 encoding and mismatched media type, while the censored [0,4] fixture says counts above 4 are censored.",
  "provenance": [
    {"kind": "A", "reference": "ARCHITECTURE.md §§8.1–8.2, LR-008/LR-013/LR-014 and 004-a requirements 1–9"},
    {"kind": "E", "reference": "2026-09-08 probes at f38f961: rights_status=synthetic normalizes to PROJECT_AUTHORED_SYNTHETIC; encoding=ISO-8859-2 and media_format=text/csv validate although loader decodes UTF-8 JSONL; fixture cutoff says above 4 censored while bounds are 0..4."}
  ],
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
  "lr": ["LR-008", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

004-b is the first corrective round on objective-004 branch and PR #5. Preserve
`2bc3cfb`/`f38f961` and all earlier history. Do not amend, create a second PR or
advance the objective number.

## Provenance

- A: a strict versioned manifest is an exact contract, not a fuzzy ingestion API.
  Declared encoding/media/record format must describe the bytes actually parsed.
- A: CENSORED bounds preserve the omitted low-frequency side; an upper bound 4
  cannot be described as censoring values above 4.
- E: the direct probes in metadata reproduce these defects at the public model.
  Review also found broad `except Exception` conversion around Pydantic validation
  and numerous unneeded public/field aliases before any consumer exists.

## Current verified state

Accepted main remains `dac4789f52c9e82aec90d1cf92ce9f1194cc103a`. PR #5 is the
sole open PR at remote report head `f38f9618c0820eb68b462e43242ea0cd22efe945`
with implementation parent `2bc3cfbcb0b2c2c2042b612317e6c499ee2f3dd9`. Remote SELF,
exact `004-a\n` active, transcript/governance and both final-head checks verify.
CRITICAL remains empty; no external corpus/model/live/release/deployment action.

004-a added a bounded local verifier and four project-authored synthetic records.
Its evidence is valid for the behaviors actually tested, but it is not accepted for
merge until the demonstrated strictness/metadata defects are corrected.

## Governance

Preserve accepted sources and history. Rights labels are inert provenance data and
never authenticate permission. Exact strict parsing reduces ambiguity without adding
rights. D0/NONE; no legal decision or real-source use occurs.

## Goal and dependencies

Make the 004 manifest/fixture seam exact: one canonical field/value vocabulary,
declared format identical to actual parser behavior, directionally correct censoring,
truthful no-importer status, scoped synthetic-use readiness and narrow exception
translation. Continue on PR #5.

## Scope

1. Tighten `source_manifest.py` manifest fields/enums/validators and exception types.
2. Correct the synthetic manifest/payload metadata and derived size/SHA-256.
3. Add direct regressions for all probes and public-schema reduction.
4. Update direct exports/docs/inventory assertions only as necessary.
5. Publish exact 004-b order/active/report on PR #5.

## Non-goals

No external source fact/right/access, acquisition, importer, index, lookup, corpus
arithmetic or downstream repair behavior. No generalized content-type framework or
backward-compatibility aliases: there is no accepted consumer to preserve. No broad
OAP refactor, dependency, live test, model/GPU/service/network/GitHub setting, merge,
release or deployment.

## Files and boundaries

Expected changes: `source_manifest.py`, its public exports, objective-004 tests, the
two synthetic fixture files, and direct docs/inventory/package assertions. Protocol
paths are 004-b order/active/report. Existing 003 semantics remain unchanged.

Exercise the real public model and verifier. Tests must demonstrate rejection rather
than inspect implementation text. Recalculate checksum/size only after final payload
bytes are fixed.

## Requirements

1. Remove rights-value normalization. Accept only the four exact serialized
   `RightsStatus` values; reject `synthetic`, `permitted`, `unknown`, `restricted`,
   case/space/hyphen variants, booleans and other types.
2. Because no backward-compatible consumer exists, remove manifest input field aliases
   and redundant public class/function aliases introduced by 004-a. Publish one
   documented canonical field name and one canonical public name per concept. Unknown
   alternate keys must fail under `extra=forbid`. Retain aliases only if an existing
   003 contract already requires them; do not modify 003 here.
3. Bind schema version 1 to actual supported bytes: encoding is exactly `UTF-8`;
   record format is exactly `jsonl` or `json`; media format is an exact documented
   value paired each supported record format. Reject mismatched/unsupported declarations
   in the model or before any payload parse. Do not silently case-fold declarations.
4. Add an explicit nonempty authorized-use scope. `use_ready=true` is meaningful only
   within that declared scope. The checked fixture scope is exactly local synthetic
   tests, not corpus, linguistic, runtime, production or redistribution authority.
   Synthetic fixture license/terms must reference the repository `LICENSE` explicitly;
   attribution states project-authored synthetic content and no external corpus.
5. Do not claim an importer exists. Rename/represent importer version truthfully and
   set the fixture to an exact `NOT_APPLICABLE_SYNTHETIC_FIXTURE` value (or null with
   equally strict validation). Preserve record/manifest schema version 1 and explicit
   deterministic fixture parameters.
6. Correct censored evidence text to state that an omitted synthetic query is bounded
   from 0 through 4 because values at/below the synthetic cutoff are not retained.
   Update manifest cutoff/threshold wording consistently. Preserve CENSORED state,
   `[0,4]`, `query_complete=false` and UNKNOWN denominator; never imply real thresholds.
7. Narrow broad `except Exception` blocks around manifest/record validation to the
   actual Pydantic/JSON/type/value exceptions. Let unexpected programming/resource
   failures remain distinguishable; preserve finite public errors for expected bad
   input without payload echo.
8. Keep existing safe path, bounded read, duplicate key/ID, size/checksum, UTF-8 and
   synthetic record tests green. Add exact negative probes for requirements 1–7,
   including wrong encoding, media/record mismatch, alternate keys, importer claim,
   missing use scope and the corrected fixture text/checksum.
9. Preserve no import-time I/O/network and no fixture in runtime wheel. Docs continue
   to label all records synthetic and every real-source fact/rights/access unverified.
10. Run fresh implementation-head checks. Force-stage exact `004-b\n`; preserve
    004-a report, and publish only the matching report as the final commit.

## Acceptance criteria

1. All three direct invalid-manifest probes now reject and canonical checked-in
   manifest/payload still verify and round-trip.
2. Censored fixture metadata is directionally consistent with `[0,4]`; exact payload
   size/SHA match the corrected committed bytes.
3. Canonical public/field names are documented and redundant 004 aliases are absent;
   expected invalid inputs map to finite errors without broad exception masking.
4. Rights/use/license/importer metadata makes only local synthetic-test claims. No
   external-source or language-quality claim appears in code, fixture, docs or report.
5. Focused/broad tests, `ruff check src scripts tests`, mypy, full OAP suite, native
   locked/offline baseline, transcript/governance/protected checks and both required
   final-head CI checks pass at exact SHAs.
6. PR #5 remains sole open/unmerged PR during coding and remote SELF verifies. No
   later/live/private/release/deployment action occurs.

## Verification

Use a fresh owned native temporary environment and run/report:

```text
pytest tests/contract/test_objective_004.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-b
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-b
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a
git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD
git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After report publication strategy verifies remote SELF, active bytes and final-head
CI. Evidence remains synthetic schema/file-integrity only.

## Local setup and constraints

Use frozen lock and owned `/tmp` environments; no repository `.venv`. Synthetic tiny
fixtures only. No external URLs are followed or data acquired. No customer/model text,
credentials, prompts or review output. All protected/live/release boundaries remain.

## Documentation

Document the canonical schema/value vocabulary, local-test use scope, repository
license reference, no-importer status, corrected censoring direction and limitations.

## Git and report publication

Stay on `oap/004-source-manifests-and-miniature-synthetic-corpus`, amend only PR #5,
and preserve `2bc3cfb`/`f38f961`. Commit/push all non-report work, exact order and
force-staged active; run CI and record the literal implementation SHA. Then create
only `oap/reports/004-b-strict-manifest-semantics.md` as a SELF report-only commit
with implementation sole parent. Push, remotely verify, send exact `OK`, and exit.

## Decision classification

D0. Exact schema cleanup, honest synthetic metadata and narrow exception handling are
deterministic reversible development corrections with no external rights decision.

## Deferred human adjudication
- Decision: NONE

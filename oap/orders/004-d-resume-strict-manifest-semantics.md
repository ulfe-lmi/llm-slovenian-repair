# Work order 004-d — Resume strict manifest semantics

Status: FINAL

```oap-metadata
{
  "id": "004-d",
  "title": "Resume strict manifest semantics",
  "objective": "004",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "dac4789f52c9e82aec90d1cf92ce9f1194cc103a",
  "branch": "oap/004-source-manifests-and-miniature-synthetic-corpus",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 5,
  "dependencies": ["001", "002", "003"],
  "local_work": "Clean objective branch at remote 004-c report head 536a1b2cc94b0c65762a36329eea967dc5cab10e; preserve all 004-a/b/c and earlier transcript commits plus ignored environments/private strategic state.",
  "prior_review": "004-c restored the merged objective-001 root-import invariant with verified source and built-wheel evidence. 004-b remains truthfully BLOCKED; its independently demonstrated 004-a manifest defects now resume under this next suffix before PR #5 can be reviewed for merge.",
  "provenance": [
    {"kind": "A", "reference": "PLAN.md §§6.2–6.3, ARCHITECTURE.md §§8.1–8.2, LR-008/LR-013/LR-014 and immutable 004-b strict-manifest requirements"},
    {"kind": "E", "reference": "Direct 004-a probes: rights alias synthetic is accepted, ISO-8859-2 and text/csv declarations are accepted although verifier decodes UTF-8 JSONL, and [0,4] censored evidence is described as counts above 4 censored"},
    {"kind": "C", "reference": "004-b BLOCKED report 8f236e0 and completed cross-objective remediation 004-c report 536a1b2 permit safe resumption without rewriting history"}
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

004-d resumes the product work deliberately blocked in 004-b after 004-c closed the
higher-priority root-import contradiction. Continue on existing PR #5. Preserve all
historical orders/reports; do not call 004-b complete or rewrite its disposition.

## Provenance

- A: manifests must be exact metadata contracts; declared encoding/media/format must
  match the parser, rights values must not normalize into stronger claims, and
  censored bounds must describe the omitted low-frequency side correctly.
- E: final 004-a probes reproduced all three false acceptances/metadata contradiction.
  Review also found unneeded aliases, broad validation catches and a synthetic
  `importer` value despite no importer implementation.
- C: 004-c source/no-dependency-wheel/dependency-installed-wheel proofs pass; root
  lazy imports must remain invariant while source-manifest exports are narrowed.

## Current verified state

Accepted main remains `dac4789f52c9e82aec90d1cf92ce9f1194cc103a`. PR #5 is
the sole open PR at remote 004-c report head
`536a1b2cc94b0c65762a36329eea967dc5cab10e`, implementation parent
`18382e4b07ced4793c88372e841a473338d52b4f`. Remote SELF, transcript, governance,
active `004-c\n`, Application baseline and a same-SHA rerun of OAP bootstrap verify.
The first final-head OAP attempt failed only in unrelated fixture teardown and remains
recorded. Independent native baseline passed all stages/cleanup.

Branch protection is disabled and rulesets empty; do not change settings. CRITICAL is
empty. No external corpus/right/access, live model, release or deployment is authorized.

## Governance

Apply LR-008/LR-013/LR-014 and preserve the restored 001 import boundary. Schema labels
are untrusted records, not authorization. Exact synthetic fixture rights are limited
to project-authored local test use. D0/NONE.

## Goal and dependencies

Complete objective 004 by making the existing manifest/fixture/checker strict and
internally truthful while keeping all root exports lazy. Do not add new corpus
capability or real-source facts.

## Scope

1. Tighten `source_manifest.py` canonical fields/enums/format and exception handling.
2. Correct synthetic manifest/payload wording, no-importer/use/license metadata, size
   and checksum.
3. Add focused regressions and update lazy root exports/tests for removed 004 aliases.
4. Update only direct docs/inventory/package assertions.
5. Publish exact 004-d order/active/report on PR #5.

## Non-goals

No external source acquisition/right decision, importer, index, lookup, arithmetic,
detector/reviewer/patcher/pipeline/API, dependency, governance, live/model/GPU/service/
network/GitHub setting, merge, release or deployment. Do not modify 003 contracts or
weaken 004-c import isolation.

## Files and boundaries

Expected changes are `source_manifest.py`, root lazy export mapping/typing/`__all__`,
objective-001 export lists only as needed, objective-004 tests and two fixtures, direct
README/STATUS/DEVELOPMENT and exact inventories. Protocol paths are 004-d order/active/
report. Exercise the real public Pydantic model and bounded verifier.

## Requirements

1. Remove rights normalization. Accept only exact serialized RightsStatus values and
   reject shorthand/case/space/hyphen variants, booleans and unknown types.
2. Remove 004-a manifest field aliases and redundant 004 public class/function aliases;
   there is no accepted consumer requiring compatibility. Keep one canonical field and
   one public name per concept. Alternate keys fail under `extra=forbid`. Update lazy
   root map, `TYPE_CHECKING`, `__all__`, driver/test export lists consistently without
   causing eager imports.
3. Schema v1 supports exact `UTF-8` encoding and exact `jsonl`/`json` record formats
   with one documented matching media type per format. Reject non-UTF-8, case variants,
   unsupported or mismatched media/record declarations before payload parsing.
4. Add a nonempty authorized-use scope; `use_ready=true` applies only within it. The
   checked fixture scope is local synthetic tests only. License/terms explicitly
   reference repository `LICENSE`; attribution says project-authored synthetic and no
   external corpus. Unknown/restricted rights remain fail-closed.
5. Do not claim an importer exists. Use one canonical importer-version field and set
   the fixture to exact `NOT_APPLICABLE_SYNTHETIC_FIXTURE` (or a validated null with
   equivalent meaning). Retain manifest/record schema v1 and deterministic parameters.
6. Correct censored evidence to say values at/below synthetic cutoff 4 are represented
   only by `[0,4]`; align manifest wording, retain CENSORED/query-incomplete/unknown
   denominator, and make no real-corpus threshold claim. Recompute exact payload size
   and SHA after final bytes.
7. Replace broad `except Exception` around manifest/record validation with actual
   Pydantic/JSON/type/value exceptions. Preserve finite safe labels for expected bad
   input while unexpected programming/resource failures remain distinguishable.
8. Keep all bounded path/symlink/type/size/checksum/UTF-8/duplicate-key/record tests.
   Add direct negatives for requirements 1–7 and exact corrected fixture bytes.
9. Re-run 004-c source and exact no-dependency/dependency-installed wheel proofs after
   export changes. Bare root import must still add zero Pydantic/HTTPX modules.
10. Preserve dependencies/governance/history. Force-stage exact `004-d\n`, run complete
    checks, and publish the matching report as the sole final commit.

## Acceptance criteria

1. The three demonstrated invalid manifest inputs reject; canonical checked-in
   manifest/payload verify and round-trip with corrected censoring and exact hash/size.
2. Only canonical fields/values/public names remain. Rights/use/license/importer
   metadata claims local synthetic tests only and no external permission/capability.
3. Expected invalid inputs map to finite errors without broad exception masking;
   filesystem containment and bounded-read negatives remain green.
4. Restored root import isolation passes source and exact built-wheel probes before
   and after lazy symbol access; expanded package files remain correctly tested.
5. Focused/broad pytest, scoped Ruff, mypy, OAP suite, native locked/offline baseline,
   transcript/governance/protected checks and both fresh final-head CI checks pass.
6. PR #5 remains sole open/unmerged PR during coding; remote SELF verifies. No real
   corpus/live/ICA/milestone/release/deployment evidence is claimed.

## Verification

Use fresh owned native environments and run/report:

```text
pytest tests/contract/test_objective_001.py -q
pytest tests/contract/test_objective_004.py -q
pytest tests/contract -q
pytest -q
ruff check src scripts tests
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 004-d
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 004-d
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref dac4789f52c9e82aec90d1cf92ce9f1194cc103a
git diff --check dac4789f52c9e82aec90d1cf92ce9f1194cc103a...HEAD
git diff --exit-code dac4789f52c9e82aec90d1cf92ce9f1194cc103a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

After publication strategy independently verifies remote SELF, root/wheel behavior,
final-head CI and strongest merge objection. Evidence is synthetic schema/integrity
only, not real corpus or linguistic proof.

## Local setup and constraints

Frozen lock and owned native `/tmp` environments only; no repository `.venv`. Tiny
project-authored fixtures, no external URL/data access. No secrets/customer/model text,
Qwen/GPU/service/network change. Live/release/deployment gates remain closed.

## Documentation

Document exact canonical schema/public names, local synthetic-test use scope,
repository license reference, no-importer status, corrected censoring and all limits.
Preserve the root lazy-import promise and historical 004-b BLOCKED fact.

## Git and report publication

Stay on `oap/004-source-manifests-and-miniature-synthetic-corpus`, amend only PR #5,
preserve all prior heads through `536a1b2`, and commit/push non-report work/order/active
before recording implementation SHA. Create only
`oap/reports/004-d-resume-strict-manifest-semantics.md` as SELF report-only commit,
push, remotely verify, send exact `OK`, and exit. Do not merge.

## Decision classification

D0. This resumes deterministic strictness corrections after the higher-priority
regression was closed. No external right, intent change or protected action occurs.

## Deferred human adjudication
- Decision: NONE

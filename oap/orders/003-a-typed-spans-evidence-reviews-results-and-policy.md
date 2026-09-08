# Work order 003-a — Typed spans, evidence, reviews, results and policy

Status: FINAL

```oap-metadata
{
  "id": "003-a",
  "title": "Typed spans, evidence, reviews, results and policy",
  "objective": "003",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "9f2d71533785e7505bdc1c2539040789d055d7de",
  "branch": "oap/003-typed-spans-evidence-reviews-results-and-policy",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": [
    "001",
    "002"
  ],
  "local_work": "Clean main at remote accepted merge 9f2d71533785e7505bdc1c2539040789d055d7de; preserve ignored local environments, private strategic files and all prior transcript history.",
  "prior_review": "Objective 002 completed through corrective 002-b and PR #3 merged as 9f2d71533785e7505bdc1c2539040789d055d7de after exact-head strategic review; no open PR remains.",
  "provenance": [
    {
      "kind": "H",
      "reference": "PLAN.md §§5.2, 6.2, 8.4–8.5, 9.3, 13.1; D01"
    },
    {
      "kind": "A",
      "reference": "ARCHITECTURE.md §§6, 8.1, 10.3, 11, 14.1 and compact A-SPAN-01, A-EVIDENCE-01, A-SCHEMA-01, A-ACCEPT-01, A-LIMIT-01"
    },
    {
      "kind": "E",
      "reference": "Accepted main has only the reproducible package baseline under src, no contracts.py or policy.py, Pydantic 2.13.5 is locked, both required PR checks exist, and CRITICAL contains zero entries."
    }
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
  "lr": [
    "LR-003",
    "LR-006",
    "LR-008",
    "LR-010"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "Application baseline"
  ],
  "decision_class": "D0"
}
```

## Identity

003-a is the first round of numeric objective 003 and creates one new branch/PR
from accepted main `9f2d71533785e7505bdc1c2539040789d055d7de`. If interrupted after PR
creation, recover that exact branch/PR and ID; do not create a replacement PR.

## Provenance

- H: PLAN fixes Unicode code-point original offsets, exact slice equality,
  EXACT/CENSORED/UNAVAILABLE evidence meaning, the keep/replace/wider-edit
  relationships, finite modes, and bounded engineering defaults.
- A: Architecture requires typed spans/evidence/results, immutable-original
  semantics, non-authoritative confidence, finite review/call/resource limits,
  fail-closed unknown states and explicit evidence incompleteness.
- E: Merged main contains only `__version__` and `py.typed` in the package. There
  is no product contract or policy implementation to preserve. Pydantic is already
  a locked runtime dependency; no dependency or source acquisition is required.

## Current verified state

Remote and local default `main` are clean and equal at merge commit
`9f2d71533785e7505bdc1c2539040789d055d7de`. Objective 002's complete transcript
through 002-b is merged; the committed active blob remains exact `002-b\n` and
both required checks passed on its reviewed head. GitHub has no open PR.

Accepted governance validates at this exact main. PLAN SHA-256 is
`d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0`,
ARCHITECTURE SHA-256 is
`a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7`,
and CRITICAL SHA-256 is
`a9ea5fa5db2affabf0f85710f41e37e73b108c0236a58b7efb9c17cb36a07e9e`
with zero entries. Live repair tests remain disabled. No model, corpus, service,
GPU, port, credential, release or deployment fact is inferred.

## Governance

Preserve accepted PLAN, architecture, CRITICAL, role law, compact sources,
governance and historical order/report bytes. LR-003 fixes CPU-owned original
code-point targets; LR-006 preserves exact/censored/unavailable evidence and
unknown denominators; LR-008 limits review output to untrusted local proposals;
LR-010 requires fail-closed validation and exact approved-span composition.

The exact Python names and internal model factorization below are reversible D0
engineering choices. They must not weaken the behavioral invariants. Proposed
PLAN defaults remain versioned engineering defaults, not measured performance or
human acceptance claims. Deferred human adjudication is NONE.

## Goal and dependencies

Create the first side-effect-free public contract seam in
`llm_slovenian_repair.contracts` and bounded policy seam in
`llm_slovenian_repair.policy`. They must represent original-coordinate selected
spans, evidence uncertainty, narrow review proposals, original-coordinate edits,
repair results and operating limits without performing detection, review,
acceptance or patching.

Dependencies 001 and 002 supply the locked Python/Pydantic baseline and current
transcript/CI guards. This objective becomes a typed dependency for later corpus,
span mapping, reviewer, acceptance and pipeline objectives.

## Scope

1. Add strict Pydantic v2 contract models and finite string enums in
   `src/llm_slovenian_repair/contracts.py`.
2. Add a versioned immutable bounded configuration model in
   `src/llm_slovenian_repair/policy.py`.
3. Add focused contract tests using only clearly synthetic Unicode text and
   numeric evidence.
4. Update only direct package exports/type marker expectations and concise status/
   contract documentation needed to make the public seam discoverable.
5. Publish exact 003-a order, active pointer and report on one new PR.

## Non-goals

No tokenizer, Markdown/protected-span detector, corpus manifest/importer/index,
suspicion heuristic, prompt serializer, response JSON parser, HTTP/model client,
acceptance scoring, patch composition, pipeline, API, CLI or persistent logging.
Do not access or fabricate real language data, reviewer results, thresholds,
quality labels or throughput. Do not enable experimental repair or live tests.

Do not change dependencies, accepted governance, existing CI names, Qwen weights/
quantization/launch settings, CUDA/GPU, services, ports, gateway, network/VPN,
credentials, neighboring repositories, GitHub settings, release or deployment.

## Files and boundaries

Expected product paths are `src/llm_slovenian_repair/contracts.py`,
`src/llm_slovenian_repair/policy.py`, `src/llm_slovenian_repair/__init__.py`, and
`tests/contract/test_objective_003.py`. Existing objective-001 contract assertions
may change only where they currently require an empty package payload or the old
public export list. Direct README/status documentation and exact generated-file
inventory rows may change if required by existing repository checks.

Contract validation is the named boundary. Tests must instantiate/deserialize the
real models and exercise their real validators. Synthetic strings and counts are
inputs, not substitutes for the model boundary. Use no fake model/corpus/network.

## Requirements

1. Use immutable/frozen Pydantic v2 models with forbidden extra fields and strict
   field types. Public enums serialize to these exact finite values:
   `EXACT`, `CENSORED`, `UNAVAILABLE`; `detect_only`, `shadow`, `strict`,
   `experimental`; and a finite result/disposition vocabulary chosen and documented
   for original, shadow-original, degraded-original and patched outcomes. Unknown
   enum values and coercion-prone invalid types fail validation.
2. Define a selected-span contract with nonempty CPU-assigned `span_id`, inclusive
   `start`, exclusive `end`, exact nonempty `original`, containing sentence and
   bounded neighboring-context fields, plus evidence references. A response-local
   selection/batch contract binds spans to the immutable `original_text` and rejects
   zero-length, out-of-bounds, stale-slice, duplicate-ID and overlapping targets.
   Python Unicode code-point indexing is authoritative. It must preserve and test
   combining marks, emoji, repeated substrings and CRLF without normalization or
   detokenization. Protected-material exclusion remains a later seam and is not
   falsely claimed here.
3. Define an evidence contract containing nonempty source/version, normalization,
   annotation convention, measurement scope and unit plus completeness/cutoff
   metadata. Counts/bounds and a context denominator are nonnegative integers when
   known. Enforce: EXACT has one equal lower/upper value; EXACT zero requires an
   explicit query-complete assertion; CENSORED carries justified noncontradictory
   bounds/cutoff without turning absence into zero; UNAVAILABLE carries no invented
   count/bound/cutoff; an unknown denominator has no numeric value. Reject lower
   greater than upper and any known numerator bound exceeding its compatible known
   denominator. Do not compute probabilities, ratios or cross-scope comparisons.
4. Define the narrow review-proposal contract with `span_id`, `keep`, nullable
   `replacement`, `needs_wider_edit`, and optional finite confidence in `[0,1]`.
   Enforce exactly: keep requires null replacement; replace requires a nonblank
   replacement and `needs_wider_edit=false`; wider edit requires keep and null
   replacement. Confidence remains explicitly self-reported/non-authoritative.
   A batch/container rejects duplicate review IDs; matching unknown/missing IDs and
   raw JSON/output-size handling remain objective 014.
5. Define original-coordinate edit and overall repair-result contracts. An edit
   retains span ID, original start/end/slice, replacement and an explicit finite
   acceptance class; it cannot claim an empty/identity replacement. A result retains
   original/final text, a truthful changed flag, selected-span/review/edit metadata,
   review-call count limited to 0 or 1, finite nonnegative stage timings and a finite
   disposition/reason. Enforce at least: unchanged means byte-for-byte equal Python
   strings and no edits; changed means unequal strings and at least one edit; edit
   IDs/coordinates are unique/nonoverlapping and still match the original slice.
   Do not implement or claim composed patch correctness in this objective.
6. Define policy schema version 1 with `detect_only` default and these maximum
   defaults: one review request, one generative pass, zero automatic retries, one
   concurrent review, eight targets, six target words and eight replacement words.
   Select and document conservative finite positive character/byte/code-point limits
   for target, replacement, safe capture, analysis, per-target context, total prompt,
   review output, queue depth/wait and total review duration. Reject zero/negative,
   nonfinite, internally contradictory or architecture-exceeding values. Automatic
   evidence-insufficient acceptance and persistent production text storage are
   immutable false in schema version 1. These are configurable engineering bounds,
   not measured optimums.
7. Imports and validation perform no network, filesystem write, environment lookup,
   corpus/model loading, logging or service discovery. Do not include customer/model
   text in exception messages beyond Pydantic's ordinary local validation context;
   tests and docs use synthetic examples only.
8. Export the intended stable contract/policy names explicitly, retain
   `__version__`, and keep `py.typed`. Update package-payload assertions and concise
   documentation to state exactly what is implemented and what remains absent.
   Do not expose a working repair API or imply demonstrator completion.
9. Preserve the dependency lock. Add no package. Keep all existing objective-001
   baseline proofs green, including import isolation, wheel metadata/payload,
   offline installation and runtime metadata.
10. Force-stage `oap/active` as exact `003-a\n`. Prove index and implementation
    transcript modes before the report, and preserve all prior order/report/SELF
    history. Report publication is the sole final commit.

## Acceptance criteria

1. Representative valid strict models round-trip deterministically without side
   effects, and the documented public imports work from both source and built wheel.
2. Real validators accept exact Unicode slices for repeated text, combining marks,
   emoji and CRLF and reject zero-length, stale, out-of-range, duplicate-ID and
   overlapping selections.
3. A table-driven evidence matrix accepts valid EXACT/CENSORED/UNAVAILABLE and
   known/unknown denominator states and rejects negative, inverted, fabricated-zero,
   contradictory completeness and denominator-overrun states.
4. Keep, replace and wider-edit proposals accept only their exact consistent field
   combinations. Unknown fields/types/modes, NaN/infinite confidence or timings,
   duplicate review IDs, blank/identity replacements and inconsistent result flags/
   edits fail closed.
5. Default policy is detect-only and equals every selected finite v1 bound; attempts
   to exceed architectural maxima, enable retries/concurrency/evidence-insufficient
   acceptance/storage, or supply nonpositive/nonfinite bounds are rejected.
6. Focused and complete product tests, Ruff, mypy, full OAP suite, locked/offline
   native baseline, transcript guards, governance/protected-source checks and both
   required final-head CI checks pass at their exact reported SHAs.
7. PR #4 or the actually created sole objective PR remains open/unmerged during
   coding; remote SELF verification passes. No live/model/corpus/private/release/
   deployment action or evidence claim occurs.

## Verification

Run focused and broad product checks in a fresh owned native temporary environment
created from the frozen lock; record the exact resolved environment commands/paths:

```text
pytest tests/contract/test_objective_003.py -q
pytest tests/contract -q
pytest -q
ruff check .
mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 003-a
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 003-a
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 9f2d71533785e7505bdc1c2539040789d055d7de
git diff --check 9f2d71533785e7505bdc1c2539040789d055d7de...HEAD
git diff --exit-code 9f2d71533785e7505bdc1c2539040789d055d7de -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

The native driver remains the installed/offline boundary and must pass after new
package files are included in the wheel. After report publication, strategy verifies
the remote SELF commit, exact active bytes, actual diff and both required checks on
the literal final report head. Unit/schema evidence is not linguistic, model, live,
ICA, milestone, release or deployment evidence.

## Local setup and constraints

Use the committed lock and an owned native temporary project environment/cache;
do not mutate or depend on an ignored repository `.venv`. Ordinary registry access
already exercised by the baseline is allowed only for frozen setup/CI; add no new
dependency or unbounded download. Clean owned temporary paths.

Keep tests deterministic, CPU-only and finite. Use synthetic text/count fixtures.
No Qwen/corpus/GPU/service/gateway/port/network-setting/credential/GitHub-setting
mutation. No raw customer/model text, prompt/review output or secret in Git, OAP
reports or logs. Live repair testing remains separately disabled.

## Documentation

Document the public model/policy names, Unicode offset convention, evidence state
meaning, selected finite v1 defaults and explicit non-capabilities. State that
confidence is self-reported and that strict acceptance, parsing, patching, live
compatibility and quality remain unimplemented/unproven. Keep licensing status as
already selected in the repository; acquire or redistribute no data.

## Git and report publication

Create only `oap/003-typed-spans-evidence-reviews-results-and-policy` from exact
accepted main and one new PR. Reconcile remote identity immediately before creation;
if PR numbering is not 4, report the actual verified identity without rewriting the
order. Never merge or enable auto-merge.

Commit/push all non-report work, exact immutable order and force-staged active before
the report. Run implementation-head checks and CI, record the literal implementation
SHA, then create only
`oap/reports/003-a-typed-spans-evidence-reviews-results-and-policy.md`. Its SELF
commit has the implementation head as sole parent and changes only that report.
Push, verify remote head/bytes/parent/path and active blobs, send exact `OK`, and
exit without later mutation. Report-head checks remain PENDING inside the report.

## Decision classification

D0. This order pins reversible internal type shapes and conservative engineering
limits within explicit PLAN/architecture bounds. It introduces no independent
acceptance threshold, external right, protected-host change, public exposure or
other consequential unresolved alternative. Future evidence can revise defaults
through an ordinary versioned architecture-consistent order.

## Deferred human adjudication
- Decision: NONE

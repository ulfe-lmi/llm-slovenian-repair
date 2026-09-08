# Work order 005-b — Bind source evidence and bounded fetch recipe

Status: FINAL

```oap-metadata
{
  "id": "005-b",
  "title": "Bind source evidence and bounded fetch recipe",
  "objective": "005",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4",
  "branch": "oap/005-real-source-inventory-and-permitted-acquisition-recipe",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 6,
  "dependencies": ["004"],
  "local_work": "Clean objective branch at remote 005-a report head 33fd75a7c93d82d87f8d5ee997754954251549ee; preserve ignored environments/caches and private strategic state.",
  "prior_review": "005-a remote SELF and final CI verify, but independent semantic review rejected future/rounded observation timestamps, an uncapped fetch template, unbound canonical source IDs and report claims not covered by tests.",
  "provenance": [
    {"kind": "E", "reference": "At 2026-09-08T09:54:09Z the committed snapshot_at was future 2026-09-08T23:59:59Z and all observed_at fields were rounded to 00:00:00Z rather than the recorded 09:13:23Z observation."},
    {"kind": "I", "reference": "Direct mutations of release, item path, artifact path, byte size, MD5, license name/URI, publisher whitespace and future issue date all passed validate_inventory; docs contained no --max-filesize."},
    {"kind": "A", "reference": "S-STATE-01/S-EVIDENCE-01, ARCHITECTURE §8.2 and 005-a requirements 1–2/7–8 require truthful dated evidence, exact identity/checksum binding and tests that match report claims."}
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
  "lr": ["LR-008", "LR-012", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["OAP bootstrap acceptance", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

005-b is a corrective suffix on existing objective branch and PR #6. Preserve 005-a
order, implementation, COMPLETE report, tests and final CI as immutable historical
evidence; correct forward without amending or claiming that its green checks proved the
rejected semantics.

## Provenance

- E: Report-head CI and broad suites are green, but the snapshot timestamp postdates
  the actual observation and the fetch template lacks its claimed exact maximum.
- I: Nine materially invalid rebindings passed the closed four-source validator. The
  test file contains no malformed-license/checksum cases and only one ZIP-limit case,
  despite the 005-a report claiming those paths.
- A: Durable source identity and rights evidence must fail closed; reports must name
  only executed proof. These are ordinary reversible D0 defects, not judgment debt.

## Current verified state

Accepted main remains `c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4`. PR #6 is the sole
open PR at remote 005-a SELF head `33fd75a7c93d82d87f8d5ee997754954251549ee`,
implementation parent `f5928582fab1d3051bc9f726d7ede3d8cc6b85af`. Remote report,
transcript, governance and exact `005-a\n` active bytes verify. Both final checks pass.

No real source byte was acquired. Objective-004 fixture/root imports remain correct;
CRITICAL is empty. Branch protection/rulesets remain disabled; no setting change.

## Governance

Apply compact coding law, LR-008/LR-012/LR-014 and existing security/testing contracts.
Preserve PLAN, architecture, CRITICAL, role law, source lock, compact sources and all
005-a history. Treat inventory/URLs/archives as untrusted data and keep real network/
download/extraction disabled. D0/NONE.

## Goal and dependencies

Make the 005 inventory a truthful exact evidence snapshot rather than a permissive
shape check, and make the documented future fetch actually enforce its declared size
boundary. Align regression coverage and the new report with demonstrated behavior.

## Scope

1. Correct inventory timestamps and bind fixed version-1 source facts.
2. Tighten standard-library validation for canonical identity and temporal/string rules.
3. Correct the manual `.part` fetch/check/pin recipe with exact max-size enforcement.
4. Add the missing canonical, license/checksum and ZIP-limit negative proofs; clean the
   intentional duplicate-fixture warning if possible without weakening it.
5. Publish exact 005-b order/active/report on PR #6.

## Non-goals

No new source, changed source selection, artifact/body download, HEAD/range request,
query, extraction, importer/index, dependency, package API, data sample, rights/license
adjudication, GitHub setting, live test, model/GPU/service, merge, release or deployment.
Do not rewrite 005-a report claims or hide its semantic rejection.

## Files and boundaries

Expected paths are the existing inventory, verifier, objective-005 tests and DATA-
SOURCES/direct docs, exact generated inventories if required, plus 005-b protocol files.
No product package source is expected. Keep the CLI offline and standard-library-only.

## Requirements

1. Replace `snapshot_at` and every entry `observed_at` with exact UTC
   `2026-09-08T09:13:23Z`, the durable observation instant. Validate issued date is not
   after observed date, observed is not after snapshot, and for this closed snapshot
   the entry observations equal its snapshot. Do not consult wall-clock time in CI.
2. Reject empty or whitespace-only strings and leading/trailing whitespace in all
   identity, publisher, license, status, scope and filename fields. Preserve UTF-8 and
   control rejection. Add direct blank-publisher and future-issue negatives.
3. Version 1 has exactly four closed IDs. Bind each ID to its exact kind, source name,
   release, issued date, item URL/handle, ordered publisher list, access label, exact
   license name/URI, artifact URL/name/media/byte size/MD5/container/member format or
   query-only null artifact, downstream objective, selection/acquisition/bulk/
   redistribution states, readiness/fallback, completeness/absence/denominator and
   exact cutoff semantics. A source revision requires an explicit new inventory
   revision/code review; it cannot silently rebind an existing ID.
4. At minimum regress all nine demonstrated invalid changes: release, item path,
   artifact path, byte size, MD5, license name, license URI, blank publisher and future
   issue date. Also reject a malformed checksum length/case/algorithm and query entry
   given a CC license/artifact/readiness. Assert the committed canonical table exactly.
5. Preserve generic local ZIP verification while keeping the production CLI bound to
   the canonical committed inventory. If miniature tests need injectable expected
   metadata, isolate that seam below the canonical loader/ID lookup so callers cannot
   bypass canonical validation. Do not add a CLI flag that disables identity checks.
6. Add deterministic focused cases for each enforced ZIP limit: member count, one
   member's uncompressed size, total uncompressed size and compression ratio. Add a
   directory/non-regular member case. Retain size/MD5, unsafe name, duplicate,
   encrypted, symlink and no-extraction paths. Suppress only the known warning emitted
   while constructing the deliberate duplicate fixture; do not suppress verifier errors
   or broad warning classes.
7. The docs fetch template must write to an owned `*.part` path and include curl
   `--max-filesize` set from the exact selected inventory byte size, HTTPS-only initial/
   redirect protocols, connect and total timeout, fail-on-HTTP, and no credentials.
   It must explicitly verify exact size plus MD5/SHA-256 through the offline tool before
   any separately authorized final rename/use. Do not run the template. A single static
   512 MiB program cap does not substitute for the selected artifact's exact cap.
8. Correct new tests/report to say exactly what ran. The immutable 005-a overclaim stays
   visible; 005-b must explicitly state that invalid license/checksum and all four ZIP-
   limit proofs were added here. Preserve publisher-MD5-versus-project-SHA distinction,
   CC obligations, provider-agreement block and all acquisition/import/release NOT RUN.
9. Preserve full objective-001 root source/wheel laziness, objective-003 evidence,
   objective-004 exact fixture bytes/hash and all 005-a positive behavior. No dependency,
   wheel/sdist source inventory or external data bytes may be added.
10. Run focused/broad product tests, scoped Ruff/mypy, full OAP, native baseline,
    transcript/governance/protected checks and both required CI checks. Force-stage
    exact `005-b\n`; matching report is the sole final commit.

## Acceptance criteria

1. Committed timestamps equal `2026-09-08T09:13:23Z`; all nine demonstrated mutation
   probes and malformed/contradictory variants reject with finite errors.
2. The exact canonical four-entry inventory passes, while no existing fixed ID can be
   rebound to another release/path/license/size/checksum under schema version 1.
3. Each of four ZIP limits and directory/non-regular handling has a real synthetic ZIP
   boundary test; all prior verifier positives/negatives remain green without extraction.
4. Docs visibly contain `--max-filesize`, a selected exact byte value mechanism and a
   `.part` target before verification. No real network/data action occurred.
5. All prior product/OAP/native evidence and final-head CI pass; PR #6 stays open and
   unmerged during coding. The final report truthfully distinguishes 005-a history.

## Verification

Run/report:

```text
python3.12 scripts/verify_source_artifact.py --inventory resources/source-inventory-v1.json --validate-only
uv run --frozen --python 3.12 pytest tests/contract/test_objective_005.py -q
uv run --frozen --python 3.12 pytest tests/contract/test_objective_001.py tests/contract/test_objective_003.py tests/contract/test_objective_004.py -q
uv run --frozen --python 3.12 pytest tests/contract -q
uv run --frozen --python 3.12 pytest -q
uv run --frozen --python 3.12 ruff check src scripts tests
uv run --frozen --python 3.12 mypy src tests
python3 -B -m unittest discover -s oap/tests -v
python3.12 scripts/verify_development_baseline.py --temp-parent /tmp --command-timeout 300
python3 oap/bin/check_transcript.py --repo-root . --index --expected-id 005-b
python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 005-b
python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4
git diff --check c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4...HEAD
git diff --exit-code c19f13dcb0baa2f3d74292857b7c8f88ff64ccc4 -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap
```

Also rerun the nine independent mutation probes and inspect the docs command text. No
online source check is required or permitted in coding. Evidence remains metadata and
offline verifier evidence, not acquisition, linguistic, legal, live or release proof.

## Local setup and constraints

Use committed lock and owned `/tmp` environments/fixtures; preserve ignored repository
`.venv` and caches. No real URL is contacted. No credential, external bytes, customer/
model text or private strategic contents in Git/logs. Do not touch protected model/GPU/
service/network/gateway/neighbor/GitHub settings. Live/release/deploy gates stay closed.

## Documentation

Correct the recipe and describe exact observation instant/version binding. Keep code
Apache versus external CC/provider terms distinct. State that future acquisition must
create a new evidence record with computed SHA-256 and separate rights/release review.

## Git and report publication

Remain on PR #6 and the existing branch. Commit/push non-report correction, wait for
implementation-head checks, record literal SHA, then publish only
`oap/reports/005-b-bind-source-evidence-and-bounded-fetch-recipe.md` as SELF with that
implementation parent. Push, remotely verify, send exact `OK`, exit. Do not merge.

## Decision classification

D0. These are bounded truthful-evidence, validation and test corrections within the
existing design. No legal/source acquisition decision or other D1/D2 boundary is made.

## Deferred human adjudication
- Decision: NONE

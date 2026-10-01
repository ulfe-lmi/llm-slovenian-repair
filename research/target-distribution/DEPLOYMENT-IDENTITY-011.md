# DEPLOYMENT-IDENTITY-011 — Data-free E2(b) designation record and bounded
# freshness re-probe record (objective 011, round 2)

Status: round 011-b record (objective 011, round 2). Data-free: this
document carries no endpoint values, no credentials, no private paths,
and no raw text. The full attempt-level receipt (timestamps, statuses,
wall times, response-size fields, request metadata) is kept in the
round private directory (`011b-identity` under the round private
research runtime root; file `reprobe-receipt.json`) and is never
committed.

## 1. E2(b) designation (recorded verbatim)

The owner's verbatim decision (2026-09-30, owner strategic thread):

> (b) Designate A100-FP8 as the confirmation target

This selects alternative E2(b) of the committed decision package
(`research/target-distribution/DEPLOYMENT-IDENTITY-009.md`, section 4)
and lifts the PROTOCOL-009 element (a) hard gate for the A100-FP8
regime only, subject to the bounded freshness re-probe of section 3 of
this record before the first sample is opened. The attributable
decision is recorded privately (private receipt
`workorders/e2b-decision-receipt-20261001.md`, referenced by name only,
never reproduced).

## 2. Product-intent-change impact statement

Recorded as a PRODUCT-INTENT CHANGE per DEPLOYMENT-IDENTITY-009
section 4(b): the A100-FP8 regime (the 007 lineage deployment) becomes
the confirmation TARGET by designation, and no additional replication
is required (the frozen method was developed and frozen on this
regime). Impact: evidence transferability NONE to the RTX-3090 target
(the study then confirms the A100-FP8 regime, not the PLAN deployment —
the deployment-validity gap in RESEARCH-STATE section 9 is closed by
re-designation, not by transfer); the delivered "target-distribution"
label refers to the designated regime, and any future RTX-3090
deployment remains unconfirmed by this study; rights: no new access
needed (the authorized out-of-band identity already covers the
regime); the A100-FP8 designation does not authorize, and is not
evidence for, any other deployment.

## 3. Bounded freshness re-probe (order 011-b scope item 2b)

Bounded read-only metadata re-probe executed in this round, BEFORE any
sample was opened: exactly 2 HTTP attempts total, no retries, zero
chat/generation/responses calls, zero other endpoints, zero writes,
zero server mutation, zero contact with the RTX-3090 host, zero
contact with Deployment B. The authorized profile (endpoint and
bearer) was read only from the round private credentials receipt
(`011b-identity/target-credentials-20261001.json`, 0600; value never
committed, never logged, never echoed).

The 009-a pinned identity is referenced by hash only: committed record
`research/target-distribution/DEPLOYMENT-IDENTITY-009.md`
(sha256 `b6734b35390f13c9170722fbf68ffee06d7d5f73da3a5e1a077980e3452994e4`,
FROZEN), whose section 1 pins the reference identity (serving
framework version 0.28.0; model identifier qwen3.8-27b; exposed model
root suffix Qwen3.8-27B-FP8; max model length 262144; OpenAI-compatible
Responses wire API, non-streaming) with the private attempt-level
receipt under `009a-identity` in the round private research runtime
root.

Attempt summary (2 of 2 authorized attempts used; full receipt
private):

| # | Endpoint class | Requested path | Auth | HTTP status | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | serving-version metadata GET | `/v1/version` | none | 401 | unauthenticated; consistent with, not proof of, the deployment's `/v1` authentication gate observed in the 009-a record |
| 2 | models metadata GET | `/v1/v1/models` | authorized bearer (value never recorded) | 404 | route not found (doubled path prefix) |

Observation window: 2026-09-30T22:58:26.577Z to
2026-09-30T22:58:26.923Z UTC. Response bodies of the two non-200
responses were not captured on the error path (status codes, timing,
and request metadata only; the private receipt records this).

EXACT FINDING (data-free): no identity field was observed on either
attempt. Both attempts returned non-200 status within the 2-attempt
budget, which is the transport-failure branch of the order's verdict
rule (scope item 2c). Path-construction finding: the round private
credentials receipt records `endpoint_base_url` WITH an embedded `/v1`
API path prefix, whereas the private 009-a C2 receipt records the
server root as the base; the two private records' scheme/host/port
are EQUAL (boolean-verified; values never committed, never echoed).
This round's probe appended the 009-a metadata paths (`/version`,
`/v1/models`) to the prefixed base, producing the non-canonical
metadata routes `/v1/version` (attempt 1) and `/v1/v1/models`
(attempt 2); the 009-a precedent probed the canonical server-root
routes `/version` and `/v1/models`. The 401 on attempt 1 is
consistent with the deployment's `/v1` authentication gate recorded as
an access-control observation in the 009-a record (unauthenticated
`/v1` routes return 401; authorized profile returns 200); the 404 on
attempt 2 indicates a non-existent route (doubled prefix). Per the
owner's credentials usage constraint (at most 2 metadata GETs total,
exactly 2 attempts, no retries), no further probe was performed this
round; the 2-attempt budget is consumed. Drift of the designated
regime is NEITHER ESTABLISHED NOR EXCLUDED by this round: the
regime-unchanged verdict is not established.

## 4. Verdict

Result: BLOCKED (probe failure), per order 011-b scope item 2c: a
transport failure occurred within the 2-attempt budget, so the round
STOPS at this finding with the exact mismatch named in section 3. NO
intake, NO manifest, NO collection, NO split, NO sample opened; an
intervening round is required before any collection. The intervening
round must re-execute the ordered 2-GET probe against the canonical
server-root metadata routes (`/version` unauthenticated; `/v1/models`
with the authorized bearer) under the same exactly-2-attempt budget,
and record its own private receipt.

## 5. Reaffirmed boundaries

- RTX-3090: MUST-NOT-BE-STARTED / MUST-NOT-BE-RECONFIGURED; zero
  probes, zero calls (this round and ever, absent an attributable
  owner decision).
- Deployment B: EXCLUDED_BY_HUMAN_OVERRIDE; zero probes, zero calls,
  ever. This exclusion is absolute and unaffected by E2(b).
- REPAIR_ALLOW_LIVE_TESTS remains NO (product live tests unchanged;
  this round's bounded re-probe is separately authorized by the owner
  E2(b) decision plus PROTOCOL-009 and is metadata-only).
- No second large GPU model; no server mutation; no endpoint value,
  credential, or private path in any committed artifact or log.
## 6. Bounded canonical-route identity re-verification (order 011-c,
## intervening pinning round)

This section is the additive 011-c record (D0 execution of the ordered
bounded verification pre-specified by section 4 of this record under
the owner's standing E2(b) authorization; the E2(b) designation of
section 1 stands untouched). Sections 1-5 are byte-preserved by this
round. The full attempt-level receipt (timestamps, statuses, observed
fields, response sizes, wall times, request metadata) is kept in the
round private directory (`011c-identity` under the round private
research runtime root; file `reprobe-receipt.json`) and is never
committed.

Bounded read-only metadata re-probe executed in this round, BEFORE any
other mutation beyond the ordered record: exactly 2 HTTP attempts
total, no retries, zero chat/generation/responses calls, zero other
endpoints, zero writes, zero server mutation, zero contact with the
RTX-3090 host, zero contact with Deployment B. The authorized profile
(both bases and the bearer) was read ONLY from the strategy-corrected
private credentials receipt (`011b-identity/
target-credentials-20261001.json`, 0600; values never committed, never
logged, never echoed); the route construction followed that receipt's
`metadata_probe_routes` field verbatim (dual bases: the server-root
base for the `/version` route; the `/v1`-prefixed API base for the
`/v1/models` route; bearer unchanged per its correction record).

Attempt summary (2 of 2 authorized attempts used; full receipt
private):

| # | Endpoint class | Requested path | Auth | HTTP status | Note |
| --- | --- | --- | --- | --- | --- |
| 1 | serving-version metadata GET | `/version` | none | 200 | observed serving framework version `0.28.0` (20 response bytes) |
| 2 | models metadata GET | `/v1/models` | authorized bearer (value never recorded) | 200 | one model row: identifier `qwen3.8-27b`, owned_by `vllm`, max model length `262144`, exposed model root suffix `Qwen3.8-27B-FP8` (505 response bytes) |

Observation window: 2026-10-01T00:58:35.948Z to
2026-10-01T00:58:36.253Z UTC.

Field-by-field match against the 009-a pinned identity
(DEPLOYMENT-IDENTITY-009 section 1, referenced by hash in section 3):
serving framework version 0.28.0 MATCH; model identifier qwen3.8-27b
MATCH; exposed model root suffix Qwen3.8-27B-FP8 MATCH; max model
length 262144 MATCH. The wire protocol class remains OpenAI-compatible
HTTP serving (vLLM; Responses wire API; non-streaming) per the
observed identity fields and the frozen 007 profiles. The observed
authentication behavior (unauthenticated `/version` 200; `/v1/models`
200 with the authorized bearer) is consistent with the 009-a
attempt-level record.

EXACT FINDING (data-free): all observed identity fields match the
009-a pin. The 011-b non-canonical-route finding (401 on `/v1/
version`; 404 on `/v1/v1/models`; no identity field observed) is
thereby explained as a route-construction artifact: the 011-b probe
appended the 009-a metadata paths to the `/v1`-prefixed API base,
whereas the canonical 009-a routes use the server-root base for
`/version` and the API base for `/v1/models` (the two private
records' scheme/host/port are equal, boolean-verified; values never
committed, never echoed). This round probed the canonical routes and
observed the pinned identity in full.

VERDICT (order 011-c scope item 3): REGIME-UNCHANGED, ESTABLISHED -
both attempts returned 200 and every observed identity field matches
the 009-a pin. The pinned identity is re-verified as of this round;
the PROTOCOL-009 element (a) hard gate is satisfied for collection.

CONSEQUENCE: the collection round (011-d) may proceed on this
verified identity, subject to its own intake gate. The single named
human input (the `011b-intake` corpus per the 011-b order item 3b)
remains outstanding (escalated to the owner exactly once,
independently of this round); this round performed NO intake, NO
manifest, NO selection, NO split, NO generation call, and NO sample
opened.

REAFFIRMED BOUNDARIES: RTX-3090 MUST-NOT-BE-STARTED /
MUST-NOT-BE-RECONFIGURED - zero probes, zero calls (this round and
ever, absent an attributable owner decision); Deployment B
EXCLUDED_BY_HUMAN_OVERRIDE - zero probes, zero calls, ever, absolute
and unaffected by E2(b); REPAIR_ALLOW_LIVE_TESTS remains NO (this
round's bounded re-probe is separately authorized by the owner E2(b)
decision plus PROTOCOL-009 and is metadata-only); no second large GPU
model; no server mutation; no endpoint value, credential, or private
path in any committed artifact or log.

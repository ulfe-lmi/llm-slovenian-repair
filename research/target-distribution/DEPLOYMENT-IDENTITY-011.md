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

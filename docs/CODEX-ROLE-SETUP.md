# Codex role setup and qualification

How the OAP role sessions (strategic and coding) are set up and qualified in
this repository. Setup needs no model or authentication and never starts an
operational round.

## Layout authority

The owner-selected layout keeps both role CODEX_HOME directories under
STRATEGIC_HOME and only the actual FIFOs in OAP_FIFO_HOME. The versioned
[`oap/governance/WORKSPACE-LAYOUT.json`](../oap/governance/WORKSPACE-LAYOUT.json)
is the authority for exact roots and storage semantics; the
[workspace placement](WORKSPACE-PLACEMENT.md) document is the historical
2026-09-07 sync-mount record.

## Foreground dispatch (012-a selection)

- The owner launches the coding session; adoption verifies the already-running
  pane and conveys the handoff without starting any model.
- Owner-launched session homes remain exactly as launched: adoption never
  relocates a CODEX_HOME, copies authentication, or re-authenticates, and
  historical private role homes are preserved.
- No background coding launch (tmux panes or `codex exec`) is permitted under
  this selection.

Two paths must not be mixed:

- **Fresh helper-managed setup** (procedure below) creates a role home and
  launch configuration only when the owner has not already launched that
  role.
- **Adoption of the owner-launched foreground session** uses the exact
  `foreground_launch` argv stored in the
  [layout](../oap/governance/WORKSPACE-LAYOUT.json): it starts zero models,
  reconfigures no home or authentication, and follows the
  [OAP runbook foreground-dispatch procedure](OAP-RUNBOOK.md). The exact
  relaunch rule stays only-if-dead.

## Setup procedure (fresh helper-managed setup)

1. Use the setup launcher, then deliberately configure/login each role with
   its own CODEX_HOME (each role `config.toml` starts as valid comment-only
   TOML).
2. `runtime.env` is the sole launch authority for helper-managed role
   launch: choose exactly one MODEL or PROFILE per role; a profile must
   exist in that role home. It does not replace the owner-selected
   foreground argv above.
3. Select permissions and qualify the CLI version before enabling operation.

Do not configure another provider, copy global state, or silently fall back
models. No credentials, `auth.json` or history are copied from the
generator. An already-adopted pane is never re-logged-in or
reconfigured by this procedure.

## Inspection evidence

Local inspection during generation: codex-cli 0.153.4; tmux 3.4.
`codex --help` and `codex exec --help` expose `--model`, `--profile`, `--cd`,
`--dangerously-bypass-approvals-and-sandbox`; exec also exposes `--ephemeral`.
Installed `--profile` semantics are a named `CODEX_HOME/<name>.config.toml`
layer. No model IDs, reasoning enums, context capacities or tokenizer counts
are inferred; optional unsupported/unset overrides are omitted.

Tiny prompts explicitly state role and route; the env label alone is not
assumed visible to the model. Generation-era observation (historical, inactive
under the current foreground selection): coding exec was fresh and
ephemeral after one wrapper-consumed control signal. Strategy
interactive context starts in the
private home and reconstructs logical continuity on replacement. Actual
instruction discovery/token/context qualification is separately recorded in
receipts; fake argv capture proves only configured behavior. An owner-chosen
future CLI/version must be requalified.

Installed `codex debug prompt-input --help` describes a prompt renderer; run it
only in an isolated synthetic home when qualifying discovery, without model
requests. No operational audit/strategic/coding session is launched for
bootstrap acceptance.

## Version policy

Owner version policy update: `OAP_CLI_QUALIFIED_VERSION="ANY"` means an upgrade
does not fail solely because `codex --version` changed. Operational launch
still requires the configured executable to exist, exit successfully and
return a nonempty version. Model/profile TOML parsing, accepted governance,
authentication, remote and activation gates remain enforced. `ANY` is a
compatibility policy, not evidence that an untested future CLI preserves every
behavior.

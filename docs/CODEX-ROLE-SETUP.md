# Codex role setup and qualification

The owner-selected layout keeps both role CODEX_HOME directories under
STRATEGIC_HOME and only actual FIFOs in OAP_FIFO_HOME. See
[workspace placement](WORKSPACE-PLACEMENT.md) for exact roots and sync-permission
semantics. Setup still needs no model/auth and never starts an operational round.

Local inspection during generation: codex-cli 0.153.4; tmux 3.4. `codex --help`
and `codex exec --help` expose --model, --profile, --cd,
--dangerously-bypass-approvals-and-sandbox; exec also exposes --ephemeral.
Installed --profile semantics are a named CODEX_HOME/<name>.config.toml layer.
No model IDs, reasoning enums, context capacities or tokenizer counts are inferred.
Optional unsupported/unset overrides are omitted. Role config.toml starts as valid
comment-only TOML. No credentials, auth.json or history copied from generator.

Setup shells need neither models nor auth. Use setup launcher, then deliberately
configure/login each role with its own CODEX_HOME. runtime.env is sole launch
authority: choose exactly one MODEL or PROFILE per role; profile must exist in
that role home. Select permissions and qualify version before enabling operation.
Do not configure another provider, copy global state or silently fallback models.

Tiny prompts explicitly state role and route; env label alone is not assumed
visible to the model. Coding exec is fresh and ephemeral after one wrapper-consumed
control signal. Strategy interactive context starts in private home and reconstructs
logical continuity on replacement. Actual instruction discovery/token/context
qualification is separately recorded in receipt; fake argv capture proves only
configured behavior. An owner-chosen future CLI/version must be requalified.

Installed `codex debug prompt-input --help` describes a prompt renderer; run only
in an isolated synthetic home when qualifying discovery, without model requests.
No operational audit/strategic/coding session is launched for bootstrap acceptance.

Owner version policy update: `OAP_CLI_QUALIFIED_VERSION="ANY"` means an upgrade
does not fail solely because `codex --version` changed. Operational launch still
requires the configured executable to exist, exit successfully and return a
nonempty version. Model/profile TOML parsing, accepted governance, authentication,
remote and activation gates remain enforced. `ANY` is a compatibility policy,
not evidence that an untested future CLI preserves every behavior.

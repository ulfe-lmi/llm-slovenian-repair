# Operational security

SEC-05. Owner layout update 2026-09-07: only the selected sync strategic subtree
in oap/governance/WORKSPACE-LAYOUT.json is excepted from POSIX 0700/0600 assertions.
Its access and synchronization follow the owner-selected storage. Ownership,
regular-file/type and symlink guards remain. Native OAP_FIFO_HOME and its real
FIFOs retain strict 0700/0600. This exception does not spread to other paths or
authorize a model, credential copying, live tests or deployment.

SEC-01. Work only inside the active order and owned disposable fixtures. Keep
Qwen weights/quantization/vLLM/CUDA/shared GPU, services/ports/network/VPN/firewall,
gateway, neighboring repositories and other agent profiles unchanged unless
explicit human authority covers the exact boundary. Full access is not authority.

SEC-02. No secrets/auth files/session histories/customer text/prompts/replacements/
private model responses in Git, OAP reports, logs or metric labels. Use synthetic
fixtures/fake keys. Real evaluation needs permission and private storage. Resolve
data/package rights; do not invent a code license or infer bulk download rights.

SEC-03. Parse configuration as allowlisted data, never eval/source it. Reject
unsafe symlinks, wrong ownership/types and private permissions. Use command arrays,
scoped manifests, locks and atomic writes. Preserve dirty/unrelated work. Do not
install daemons, startup hooks or perform deployment through setup helpers.

SEC-04. D2 actions and applicable DHA gates remain human-controlled. See the
relevant active order for exact boundary scope. Rationale for strategic review is
in [decision policy](docs/DECISION-POLICY.md); this link is optional background,
not a transitive mandatory full-source coding read.

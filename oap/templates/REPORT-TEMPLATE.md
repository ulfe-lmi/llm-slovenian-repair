# Inert final report template

PR must exist before composition. Commit only report with literal implementation sole parent. SELF is not a fabricated commit SHA; future push/CI cannot be observed here. Remote verification later goes in private receipt.

```oap-report
{
  "id": "VERIFY ID",
  "result": "VERIFY COMPLETE/PARTIAL/BLOCKED/FAILED",
  "order_path": "VERIFY exact order path",
  "order_sha256": "VERIFY digest",
  "governance": {},
  "publication_commit": "SELF",
  "implementation_head": "VERIFY literal SHA",
  "publication_verified": false,
  "pr_mode": "VERIFY mode",
  "pr": null,
  "pr_url": "VERIFY actual PR URL",
  "pr_state": "open",
  "branch": "VERIFY branch",
  "base_sha": "VERIFY base",
  "starting_remote_sha": "VERIFY observed start",
  "no_merge": true,
  "checks": [
    {
      "command": "VERIFY actual command",
      "result": "NOT RUN",
      "sha": "VERIFY tested SHA",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "VERIFY timestamp",
  "report_written_at": "VERIFY timestamp",
  "implementation": "VERIFY actual observations and limitations",
  "documentation": "VERIFY actual observations and limitations",
  "criteria": "VERIFY actual observations and limitations",
  "negative_paths": "VERIFY actual observations and limitations",
  "boundary_fidelity": "VERIFY actual observations and limitations",
  "setup": "VERIFY actual observations and limitations",
  "privacy": "VERIFY actual observations and limitations",
  "limits": "VERIFY actual observations and limitations",
  "human_gates": "VERIFY actual observations and limitations",
  "scope": "VERIFY actual observations and limitations"
}
```

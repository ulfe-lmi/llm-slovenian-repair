# Installation guide (compatibility pointer)

This page is a compatibility pointer, not a current procedure. It was added by
[PR39](https://github.com/ulfe-lmi/slaif-llm-response-language-repair/pull/39) as the detailed
lab installation record for the runnable proxy; its verified details —
statistics licence and exact downloads, checksum-guarded fetch, runtime index
build and verification, mandatory Pandoc, configuration, foreground launch,
remote SSH tunnel and the owned synthetic smoke request — are preserved in
the root [INSTALL.md](../INSTALL.md), which is now the **canonical and complete
installation procedure**. Where the two differ, INSTALL.md governs; this page
deliberately no longer keeps a second copy of the commands.

Nothing here is a record of a deployment that occurred. The instructions
prepare a foreground, loopback-only proxy instance; they do not install a public
service or change the model server, GPU, firewall or gateway.

Functional software and native Qwen compatibility are demonstrated in the
[036-a readiness audit](../oap/audit/results/036-current-functional-proxy-readiness-audit.md)
and its [report](../oap/reports/036-a-current-functional-proxy-readiness-audit.md).
Linguistic benefit is unmeasured; no separate human evaluation dataset exists
or is required (owner decision). Live qualification evidence:
[LIVE-TEST-ENVIRONMENT.md](LIVE-TEST-ENVIRONMENT.md).

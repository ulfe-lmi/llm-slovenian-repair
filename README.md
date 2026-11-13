<div align="center">
  <a href="https://www.slaif.si">
    <img src="docs/assets/slaif-logo.svg" width="300" alt="SLAIF">
  </a>
</div>

# SLAIF Slovenian Repair

<div align="center">

**A loopback-only proxy that completes a Slovenian answer, conservatively checks
bounded original spans on the CPU, and returns only evidence-backed exact-text
corrections.**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

[**Quickstart** — first request in the shortest supported path](QUICKSTART.md) ·
[**Install** — full lab setup](INSTALL.md)

</div>

SLAIF Slovenian Repair sits in front of an existing Responses API model. It waits
for a **complete** answer, selects a few suspicious words or short phrases at exact
original coordinates, optionally asks the same model in a fresh, isolated request
whether each is natural and appropriate in context, and applies a replacement only
when independent CPU evidence supports it. Everything outside the approved spans is
returned unchanged.

This is an experimental local lab proxy that you install and run yourself on
loopback; it is not a hosted service, and it makes no claim about the linguistic
quality of the underlying model.

## How it works

```mermaid
flowchart TD
    client["Client — Responses API"]
    proxy["SLAIF proxy<br/>loopback-only"]
    admit["Admission + request contract"]
    main["Main upstream Qwen<br/>complete answer captured"]
    gate["Eligibility + Pandoc protection<br/>exact original spans"]
    cpu["CPU detection<br/>bounded exact-coordinate targets"]
    review["Isolated reviewer batch<br/>fresh request, strict JSON"]
    accept["Strict lexical acceptance"]
    out["Final response<br/>only approved spans changed"]

    client --> proxy --> admit --> main --> gate --> cpu
    cpu -->|eligible targets| review --> accept
    cpu -->|no eligible target| out
    review -->|decline or fail| out
    accept -->|validated edit| out
    accept -->|no accepted edit| out
```

One proxy process owns each request end to end. Main generation and the optional
review for one answer are sequential, and the CPU side never loads a second large
model.

## Supported behavior and limits

- **Transport** — `POST /v1/responses`, stateless text input, `store: false`; the
  documented delayed-SSE profile is also supported. The listener is loopback-only
  (`127.0.0.1:18024`); a client on another host uses an SSH tunnel.
- **No token probabilities** — defined Responses API `logprobs` metadata is always
  removed, even when no correction is made.
- **Exact, conservative edits** — only approved original-coordinate spans change;
  protected material, formatting and every other code point are preserved.
- **Fail-closed** — a missing or incompatible index, or a technical failure
  of the optional repair after safe completion, returns the completed original;
  a malformed or truncated main transport is an honest protocol error; and a
  valid explicitly-incomplete envelope passes through without repair, keeping
  its status and text while defined `logprobs` are still removed. Nothing is
  masked or truncated.
- **Mandatory pinned Pandoc 3.7.0.2** for structural original-span protection.
- **External statistics** — real unigram/bigram/trigram counts (CC BY-SA 4.0) are
  not bundled in the repository; the installation fetches them into an external
  read-only index location (INSTALL.md), and the code's Apache-2.0 licence does
  not relicense them.
- **No separate human evaluation dataset**; linguistic benefit is unmeasured.

## Documentation

| Topic | Document |
| --- | --- |
| Architecture and the current runtime | [ARCHITECTURE.md](ARCHITECTURE.md) |
| First request (quickstart) | [QUICKSTART.md](QUICKSTART.md) |
| Full lab installation | [INSTALL.md](INSTALL.md) |
| Security model | [SECURITY.md](SECURITY.md) |
| Testing and verification strategy | [TESTING.md](TESTING.md) |
| Topic index and navigation | [docs/README.md](docs/README.md) |
| Development history and evidence | [docs/HISTORY.md](docs/HISTORY.md) |
| Product agreement (protected) | [PLAN.md](PLAN.md) |

## License and attribution

The code is released under the [Apache License 2.0](LICENSE). The linguistic
statistics it queries are a separate [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
publication, not bundled in the repository (the installation fetches it into an
external index location; see INSTALL.md) and not relicensed by the code. SLAIF
artwork is reused from the SLAIF project.

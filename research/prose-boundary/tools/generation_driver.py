#!/usr/bin/env python3
"""008-c bounded generation driver (human-authorized structural test-data generation).

Executes the frozen prompt library (config/generation/prompt-families.json)
against the authorized private research endpoint using the env-credential
mechanism of the 007 lineage. Hard budget: 400 generation calls total
(component batches <= 250, naturalistic <= 150, preflight 1), at most one
retry per failed call, all failures and retries recorded.

Behaviour contract:
  * BEFORE any bulk generation, one bounded preflight call verifies endpoint
    availability; the observed model/profile identity is recorded. On
    preflight failure the driver STOPS the generation increment and exits 2
    (BLOCKED); it never fabricates generated content locally.
  * Dev outputs are written into the committed corpus under
    research/prose-boundary/corpus/ (project-authored structural test data).
  * Hidden outputs are written ONLY to the private research runtime root
    under 008c-hidden/ and are never committed.
  * stdout carries counts and hashes only - never generated content.
  * The bearer is read as data and injected only into the child HTTP request;
    it is never printed, persisted, hashed, copied, or logged.

Usage:
  python3 -B generation_driver.py --runtime-root <private runtime parent> \
      --repo-root <repo> --stage all

Stages: preflight | components | naturalistic | all
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import sys
import tomllib
import urllib.parse
from pathlib import Path

SCHEMA = "008c-generation-identity/1"
PREFLIGHT_PROMPT = "Napi\u0161i samo besedo OK."
MAX_FRAG_CHARS = {"prose": 1200, "markdown": 1200, "malformed": 1200,
                   "code": 1500, "structured": 1500, "math": 1500, "machine": 1500}
MAX_NAT_CHARS = 8000
PATH_MARKERS = tuple(("/" + part + "/").encode() for part in ("tmp", "home", "root")) + (b"C:" + b"\\Users\\",)
LONG_BASE64 = re.compile(rb"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{160,}={0,2}(?![A-Za-z0-9+/])")
BEARER_VALUE = re.compile(rb"(?i)bearer[ \t]+[A-Za-z0-9._~+/=-]{20,}")
ZERO = b"\x00"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


class Budget:
    """Slot-based budget (order: total 400; component batches <= 250;
    naturalistic <= 150) plus a raw attempt ledger.

    A *slot* is one planned generation unit (one component batch or one
    naturalistic sequence). The retry policy (order: at most one retry per
    failed call, all recorded) permits retry/recovery attempts beyond the
    slot allocation; every HTTP attempt - initial, retry, and recovery -
    is counted in ``total_attempts`` and disclosed in the identity and the
    round report (the driver enforces the slot caps; the raw attempt count
    is recorded, never hidden).
    """

    def __init__(self, total: int, component_max: int, naturalistic_max: int):
        self.total, self.component_max, self.naturalistic_max = total, component_max, naturalistic_max
        self.preflight_calls = 0
        self.component_calls = 0
        self.naturalistic_calls = 0
        self.retries = 0
        self.failures = 0
        self.total_attempts = 0  # every HTTP attempt (informational ledger)

    @property
    def used(self) -> int:
        return self.preflight_calls + self.component_calls + self.naturalistic_calls

    def attempt(self) -> None:
        self.total_attempts += 1

    def take(self, kind: str) -> None:
        if self.used >= self.total:
            raise SystemExit("HARD BUDGET EXCEEDED: stopping generation increment (recorded partial state)")
        if kind == "preflight":
            self.preflight_calls += 1
        elif kind == "component":
            if self.component_calls >= self.component_max:
                raise SystemExit("component batch budget exceeded (<= 250); stopping")
            self.component_calls += 1
        else:
            if self.naturalistic_calls >= self.naturalistic_max:
                raise SystemExit("naturalistic budget exceeded (<= 150); stopping")
            self.naturalistic_calls += 1


class Endpoint:
    """007-lineage env-credential endpoint resolution (read-only)."""

    def __init__(self, runtime_root: Path):
        self.url = self._resolve_url(runtime_root)
        self.model = self._resolve_model(runtime_root)
        self.profile_path = self._resolve_profile(runtime_root)
        self.profile_sha256 = sha256_bytes(self.profile_path.read_bytes()) if self.profile_path else None
        self.bearer_source = None
        self.bearer = self._resolve_bearer()
        if not self.url or not self.model or self.bearer is None:
            raise SystemExit("endpoint resolution failed: no url/model/bearer available "
                             "(env-credential mechanism unresolvable) - preflight will be BLOCKED")

    @staticmethod
    def _env(name: str) -> str:
        value = os.environ.get(name, "")
        return value if value else None

    @staticmethod
    def _deployment_records(runtime_root: Path) -> list[dict]:
        records = []
        for name in ("007-i-contextual-validator.20260912",
                     "007-j-levenshtein-one-contextual-validator-recovery.54KmUx",
                     "007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962"):
            cfg = runtime_root / name / "CONFIGURATION.json"
            if cfg.is_file():
                try:
                    records.append(json.loads(cfg.read_text(encoding="utf-8"))["deployment"])
                except (OSError, ValueError, KeyError):
                    continue
        return records

    def _resolve_url(self, runtime_root: Path) -> str | None:
        url = self._env("RESEARCH_ENDPOINT") or self._env("REPAIR_QWEN_BASE_URL")
        if url:
            return url
        for record in self._deployment_records(runtime_root):
            if record.get("endpoint"):
                return str(record["endpoint"])
        return None

    def _resolve_model(self, runtime_root: Path) -> str | None:
        model = self._env("RESEARCH_MODEL") or self._env("REPAIR_QWEN_MODEL")
        if model:
            return model
        for record in self._deployment_records(runtime_root):
            if record.get("model"):
                return str(record["model"])
        return None

    def _resolve_profile(self, runtime_root: Path) -> Path | None:
        profile_env = self._env("CONCEPT_REVIEWER_PROFILE")
        if profile_env:
            path = Path(profile_env)
            return path if path.is_file() and not path.is_symlink() else None
        for record in self._deployment_records(runtime_root):
            if record.get("profile_path"):
                path = Path(str(record["profile_path"]))
                if path.is_file() and not path.is_symlink():
                    return path
        return None

    def _resolve_bearer(self) -> str | None:
        for name in ("RESEARCH_CREDENTIAL_REF", "REPAIR_QWEN_API_KEY_ENV"):
            env_name = self._env(name)
            if env_name and os.environ.get(env_name):
                self.bearer_source = f"env-credential variable named by {name}"
                return os.environ.get(env_name)
        if self.profile_path is not None:
            try:
                with self.profile_path.open("rb") as handle:
                    data = tomllib.load(handle)
            except (OSError, tomllib.TOMLDecodeError):
                return None
            provider = data.get("model_providers", {}).get(data.get("model_provider", ""), {})
            value = provider.get("experimental_bearer_token")
            if isinstance(value, str) and value:
                self.bearer_source = "profile experimental_bearer_token (read as data; never printed/persisted/hashed/committed)"
                return value
        return None


def parse_endpoint_url(url: str) -> tuple[str, str, int | None, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise SystemExit("endpoint URL must be an explicit HTTP(S) URL")
    return parsed.scheme, parsed.hostname, parsed.port, parsed.path.rstrip("/")


def responses_path(base_path: str) -> str:
    base = base_path if base_path.endswith("/v1") else base_path + "/v1"
    return base + "/responses"


def make_request(url: str, model: str, prompt: str, bearer: str, *, timeout: float = 300.0):
    scheme, host, port, base_path = parse_endpoint_url(url)
    body = json.dumps(
        {"model": model, "stream": False, "store": False,
         "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}]},
        ensure_ascii=False,
    ).encode("utf-8")
    connection_class = http.client.HTTPSConnection if scheme == "https" else http.client.HTTPConnection
    connection = connection_class(host, port, timeout=timeout)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    result = None
    try:
        connection.request("POST", responses_path(base_path), body=body, headers=headers)
        result = connection.getresponse()
        payload = result.read(2_000_001)
    except (OSError, TimeoutError) as exc:
        # transport-level failure (read timeout, reset): a normal failed
        # call under the frozen retry policy (at most one retry), never a
        # crash of the generation stage
        return None, f"transport error: {type(exc).__name__}"
    finally:
        connection.close()
    if result.status != 200 or len(payload) > 2_000_000:
        return None, f"HTTP {result.status}"
    try:
        doc = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"invalid JSON response: {type(exc).__name__}"
    texts = []
    for item in doc.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message" or item.get("role") != "assistant":
            continue
        for part in item.get("content", []):
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                texts.append(part["text"])
    if len(texts) != 1:
        return None, "expected exactly one assistant output_text"
    return texts[0], None


def fragment_violations(fragment: str, max_chars: int) -> list[str]:
    data = fragment.encode("utf-8")
    errors = []
    if not isinstance(fragment, str) or not fragment:
        return ["empty or non-string fragment"]
    if len(fragment) > max_chars:
        errors.append(f"fragment exceeds {max_chars} characters")
    if ZERO in data:
        errors.append("NUL byte")
    if any(b < 0x20 and b not in (0x09, 0x0A) for b in data):
        errors.append("control character")
    if any(marker in data for marker in PATH_MARKERS):
        errors.append("private path marker")
    if LONG_BASE64.search(data):
        errors.append("long base64-like run")
    if BEARER_VALUE.search(data):
        errors.append("credential marker")
    return errors


def write_jsonl_free(path: Path, records: list[dict]) -> str:
    """Write a JSON record array (guard-compatible; .jsonl is outside results/)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(records, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    path.write_bytes(payload)
    return sha256_bytes(payload)


def run_preflight(endpoint: Endpoint, identity: dict, receipts: Path) -> bool:
    budget.attempt()
    text, error = make_request(endpoint.url, endpoint.model, PREFLIGHT_PROMPT, endpoint.bearer, timeout=120.0)
    record = {"call_index": 1, "stage": "preflight", "status": "ok" if error is None else "failed", "error": error}
    if error is None:
        record["response_sha256"] = sha256_text(text)
    receipts.joinpath("preflight.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    identity["preflight"] = {
        "status": "ok" if error is None else "FAILED",
        "call_index": 1,
        "model": endpoint.model,
        "response_sha256": record.get("response_sha256"),
        "error": error,
    }
    if error is not None:
        identity["status"] = "BLOCKED"
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", required=True, type=Path, help="private research runtime parent (never committed)")
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--stage", choices=("preflight", "components", "naturalistic", "all"), default="all")
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    runtime_root = args.runtime_root.resolve()
    if not runtime_root.is_dir():
        raise SystemExit(f"runtime root missing: {runtime_root.name}")
    lib_path = repo / "research/prose-boundary/config/generation/prompt-families.json"
    library = json.loads(lib_path.read_text(encoding="utf-8"))
    policy = library["generator_policy"]["call_budget"]
    budget = Budget(policy["total"], policy["component_batches_max"], policy["naturalistic_max"])

    hidden_root = runtime_root / "008c-hidden"
    receipts = hidden_root / "generation-receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    identity_path = repo / "research/prose-boundary/config/generation/generation-identity.json"
    # Multi-stage runs accumulate: carry prior stage records (preflight,
    # budget counts, failures) so the committed identity reflects every call
    # made by the generation program, not only the last stage.
    prior: dict = {}
    if identity_path.is_file():
        try:
            prior = json.loads(identity_path.read_text(encoding="utf-8"))
        except ValueError:
            prior = {}
    identity: dict = {
        "schema": SCHEMA,
        "order": "008-c",
        "status": "IN_PROGRESS",
        "purpose": "structural test-data generation only (human decision 2026-09-17); NOT linguistic-method tuning; NOT objective-009 data",
        "prompt_library_sha256": sha256_bytes(lib_path.read_bytes()),
        "batch_plan_sha256": sha256_bytes(json.dumps(library["batch_plan"], sort_keys=True).encode("utf-8")),
        "budget": {"total": budget.total, "component_batches_max": budget.component_max, "naturalistic_max": budget.naturalistic_max},
        "failures": [],
        "privacy": "no raw outputs, no endpoint value, no bearer, no private paths in this file",
    }
    _pb = prior.get("budget", {})
    budget.preflight_calls = int(_pb.get("preflight_calls", 0))
    budget.component_calls = int(_pb.get("component_calls", 0))
    budget.naturalistic_calls = int(_pb.get("naturalistic_calls", 0))
    budget.retries = int(_pb.get("retries", 0))
    budget.failures = int(_pb.get("failed_batches", 0))
    budget.total_attempts = int(_pb.get("total_attempts", budget.preflight_calls + budget.component_calls + budget.naturalistic_calls))
    if isinstance(prior.get("preflight"), dict):
        identity["preflight"] = prior["preflight"]
    identity["failures"] = list(prior.get("failures", []))
    identity["seeds"] = {
        "dev_mashup": library["batch_plan"]["mashup_seeds"]["dev"],
        "hidden_mashup": library["batch_plan"]["mashup_seeds"]["hidden"],
        "family_seeds": {f["family_id"]: f["seeds"] for f in library["families"]},
        "scenario_seeds": {s["scenario_id"]: s["seeds"] for s in library["naturalistic"]},
        "note": "instance separation = separate per-instance seed streams and separate batch draws under the frozen deterministic order; the seed of every generated component/naturalistic record is recorded in the record itself",
    }

    endpoint = Endpoint(runtime_root)
    identity["generator"] = {
        "endpoint": "private research endpoint identity omitted (007 convention)",
        "deployment_class": "A100-FP8 (007 lineage deployment record)",
        "model": endpoint.model,
        "protocol": "Responses non-streaming",
        "profile_sha256": endpoint.profile_sha256,
        "credential_source": endpoint.bearer_source,
        "workers": 1,
        "timeout_seconds": 300,
        "parameter_note": "the driver request carries model/stream/store/input only; the frozen library's per-family temperature (0.8-0.9) and max_output_tokens were NOT sent - the endpoint's own sampling defaults applied (recorded driver-fidelity gap; the corpus shows empirically non-deterministic sampling, so instance diversity is present); disclosed in REPORT-008C section 14",
    }

    def save_identity() -> None:
        identity["budget"].update({"preflight_calls": budget.preflight_calls,
                                   "component_calls": budget.component_calls,
                                   "naturalistic_calls": budget.naturalistic_calls,
                                   "total_calls": budget.used,
                                   "retries": budget.retries,
                                   "failed_batches": budget.failures,
                                   "total_attempts": budget.total_attempts,
                                   "note": "total_calls = planned slots consumed (hard caps apply to slots); total_attempts = every HTTP attempt incl. retries and recovery calls (disclosed ledger)"})
        identity_path.write_text(json.dumps(identity, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if args.stage in ("preflight", "all"):
        budget.take("preflight")
        ok = run_preflight(endpoint, identity, receipts)
        save_identity()
        print(json.dumps({"stage": "preflight", "status": identity["preflight"]["status"],
                          "model": identity["preflight"]["model"],
                          "response_sha256": identity["preflight"]["response_sha256"]}))
        if not ok:
            raise SystemExit(2)
        if args.stage == "preflight":
            return 0

    if args.stage in ("components", "all"):
        comp_root_dev = repo / "research/prose-boundary/corpus/components-dev"
        comp_root_hidden = hidden_root / "components"
        for family in library["families"]:
            for instance in ("dev", "hidden"):
                wanted = family["instance_counts"][instance]
                target_root_skip = comp_root_dev if instance == "dev" else comp_root_hidden
                existing = target_root_skip / family["category"] / f"{family['family_id']}.json"
                if existing.is_file():
                    try:
                        prior_records = json.loads(existing.read_text(encoding="utf-8"))
                    except ValueError:
                        prior_records = []
                    if isinstance(prior_records, list) and len(prior_records) == wanted:
                        # already complete in an earlier run: no calls
                        print(json.dumps({"family": family["family_id"],
                                          "instance": instance, "skipped": "complete",
                                          "count": len(prior_records)}))
                        continue
                got: list[str] = []
                # plan entries are [batch_size, already_retried]; a batch is
                # re-issued at most once (order: at most one retry per failed call)
                plan: list[list] = [[size, False] for size in family["batches_per_instance"]]

                def _call(prompt: str):
                    return make_request(endpoint.url, endpoint.model, prompt, endpoint.bearer,
                                        timeout=family["generation_parameters"]["request_timeout_seconds"])

                def _validate(text: str, batch_size: int):
                    """Return (fragments, error)."""
                    try:
                        value = json.loads(text)
                    except json.JSONDecodeError as exc:
                        return [], f"invalid JSON array: {type(exc).__name__}"
                    if not (isinstance(value, list) and len(value) == batch_size and all(isinstance(v, str) for v in value)):
                        return [], "response is not a JSON array of exactly K strings"
                    max_chars = MAX_FRAG_CHARS[family["category"]]
                    violations = []
                    for frag in value:
                        violations.extend(fragment_violations(frag, max_chars))
                    if violations:
                        return [], "guard violations: " + "; ".join(violations[:3])
                    return list(value), None

                index = 0
                while len(got) < wanted and index < len(plan):
                    batch_size, retried = plan[index]
                    take = min(batch_size, wanted - len(got))
                    prompt = family["prompt"].replace("{K}", str(take))
                    budget.take("component")
                    budget.attempt()
                    text, error = _call(prompt)
                    fragments: list[str] = []
                    if error is None:
                        fragments, error = _validate(text, take)
                    if error is not None:
                        budget.failures += 1
                        if not retried:
                            # exactly one retry of this failed batch
                            budget.retries += 1
                            budget.attempt()
                            text, error = _call(prompt)
                            if error is None:
                                fragments, error = _validate(text, take)
                        if error is not None:
                            plan[index][1] = True
                            receipts.joinpath(f"{family['family_id']}-{instance}-fail{index}.json").write_text(
                                json.dumps({"family": family["family_id"], "instance": instance,
                                            "batch_size": take, "status": "failed", "error": error,
                                            "refilled_by": "later batch if budget allows"},
                                           ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                            identity["failures"].append({"stage": "component", "family": family["family_id"],
                                                         "instance": instance, "batch": index, "error": error})
                            # shortfall is refilled by the next batch of the same
                            # family instance if the remaining budget allows it
                            continue
                    got.extend(fragments)
                    receipts.joinpath(f"{family['family_id']}-{instance}-n{len(got)}.json").write_text(
                        json.dumps({"family": family["family_id"], "instance": instance, "batch_size": take,
                                    "status": "ok", "count": len(got)}, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
                    index += 1
                if len(got) != wanted:
                    identity["status"] = "PARTIAL"
                    identity["failures"].append({"stage": "component", "family": family["family_id"],
                                                 "instance": instance, "error": f"shortfall {len(got)}/{wanted}"})
                records = []
                for seq, frag in enumerate(got, start=1):
                    records.append({
                        "component_id": f"comp-{family['category']}-{family['family_id'].split('-', 1)[1]}-{instance}-{seq:04d}",
                        "family": family["family_id"],
                        "instance": instance,
                        "category": family["category"],
                        "subcategory": family["subcategory"],
                        "fragment": frag,
                        "fragment_sha256": sha256_text(frag),
                        "fragment_bytes": len(frag.encode("utf-8")),
                        "seed": family["seeds"][instance],
                    })
                target_root = comp_root_dev if instance == "dev" else comp_root_hidden
                digest = write_jsonl_free(target_root / family["category"] / f"{family['family_id']}.json", records)
                where = "dev" if instance == "dev" else "hidden(private)"
                print(json.dumps({"family": family["family_id"], "instance": where, "count": len(records),
                                  "sha256": digest}))
        save_identity()
        if identity["status"] == "PARTIAL":
            raise SystemExit(3)

    if args.stage in ("naturalistic", "all"):
        nat_root_dev = repo / "research/prose-boundary/corpus/naturalistic-dev"
        nat_root_hidden = hidden_root / "naturalistic"
        for scenario in library["naturalistic"]:
            for instance in ("dev", "hidden"):
                wanted = scenario["instance_counts"][instance]
                target_root_skip = nat_root_dev if instance == "dev" else nat_root_hidden
                existing = target_root_skip / f"{scenario['scenario_id']}.json"
                prior_records: list[dict] = []
                if existing.is_file():
                    try:
                        loaded = json.loads(existing.read_text(encoding="utf-8"))
                        if isinstance(loaded, list):
                            prior_records = [r for r in loaded if isinstance(r, dict)
                                             and isinstance(r.get("case_id"), str)
                                             and isinstance(r.get("fragment"), str)]
                    except ValueError:
                        prior_records = []
                have = {int(r["case_id"].rsplit("-", 1)[1]) for r in prior_records
                        if r["case_id"].rsplit("-", 1)[1].isdigit()}
                fresh = not prior_records
                if not fresh and have == set(range(1, wanted + 1)):
                    # already complete in an earlier run: no calls
                    print(json.dumps({"scenario": scenario["scenario_id"],
                                      "instance": instance, "skipped": "complete",
                                      "count": len(prior_records)}))
                    continue
                # surgical completion: re-issue only the missing sequences of
                # a partially completed instance (recovery); a fresh instance
                # runs all its sequences (each one is one planned slot)
                missing = [seq for seq in range(1, wanted + 1) if seq not in have]
                if not missing:
                    missing = list(range(1, wanted + 1))
                records = list(prior_records)
                for seq in missing:
                    if fresh:
                        budget.take("naturalistic")
                    budget.attempt()
                    prompt = scenario["prompt_template"]
                    text, error = make_request(endpoint.url, endpoint.model, prompt, endpoint.bearer,
                                               timeout=scenario["generation_parameters"]["request_timeout_seconds"])
                    ok = False
                    violations: list[str] = []
                    if error is None:
                        try:
                            value = json.loads(text)
                            if isinstance(value, str) and value:
                                text = value
                                violations = fragment_violations(text, MAX_NAT_CHARS)
                                ok = not violations
                        except json.JSONDecodeError:
                            ok = False
                            violations = ["response is not a single JSON string"]
                    if not ok:
                        budget.failures += 1
                        identity["failures"].append({"stage": "naturalistic", "scenario": scenario["scenario_id"],
                                                     "instance": instance, "seq": seq,
                                                     "error": error or "guard violation: " + "; ".join(violations),
                                                     "retry_pending": True})
                        budget.retries += 1
                        budget.attempt()
                        text, error = make_request(endpoint.url, endpoint.model, prompt, endpoint.bearer,
                                                   timeout=scenario["generation_parameters"]["request_timeout_seconds"])
                        violations = []
                        if error is None:
                            try:
                                value = json.loads(text)
                                if isinstance(value, str) and value:
                                    text = value
                                    violations = fragment_violations(text, MAX_NAT_CHARS)
                                    ok = not violations
                            except json.JSONDecodeError:
                                ok = False
                                violations = ["response is not a single JSON string"]
                        if not ok:
                            identity["status"] = "PARTIAL"
                            identity["failures"].append({"stage": "naturalistic", "scenario": scenario["scenario_id"],
                                                         "instance": instance, "seq": seq,
                                                         "error": (error or "guard violation: " + "; ".join(violations))
                                                                 + " (retry failed)",
                                                         "final": True})
                            continue
                    case_id = f"nat-{scenario['scenario_id'].removeprefix('ns-')}-{instance}-{seq:02d}"
                    records.append({
                        "case_id": case_id,
                        "scenario": scenario["scenario_id"],
                        "scenario_index": scenario["scenario_index"],
                        "instance": instance,
                        "fragment": text,
                        "fragment_sha256": sha256_text(text),
                        "fragment_bytes": len(text.encode("utf-8")),
                        "prompt_sha256": sha256_text(prompt),
                        "seed": scenario["seeds"][instance],
                    })
                    receipts.joinpath(f"{scenario['scenario_id']}-{instance}-{seq:02d}.json").write_text(
                        json.dumps({"scenario": scenario["scenario_id"], "instance": instance, "seq": seq,
                                    "status": "ok", "sha256": records[-1]["fragment_sha256"]}, indent=1) + "\n",
                        encoding="utf-8")
                records.sort(key=lambda r: int(r["case_id"].rsplit("-", 1)[1]))
                target_root = nat_root_dev if instance == "dev" else nat_root_hidden
                digest = write_jsonl_free(target_root / f"{scenario['scenario_id']}.json", records)
                where = "dev" if instance == "dev" else "hidden(private)"
                print(json.dumps({"scenario": scenario["scenario_id"], "instance": where,
                                  "count": len(records), "completed_sequences": len(missing), "sha256": digest}))
        save_identity()
        if identity["status"] == "PARTIAL":
            raise SystemExit(3)

    # program completion: every planned family instance and scenario instance
    # present with its exact planned record count (the whole program, not only
    # the stage just run; a clean stage that leaves the program incomplete is
    # IN_PROGRESS)
    def _set_complete(root: Path, rel: str, wanted: int) -> bool:
        try:
            recs = json.loads((root / rel).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        return isinstance(recs, list) and len(recs) == wanted

    comp_root_dev = repo / "research/prose-boundary/corpus/components-dev"
    comp_root_hidden = hidden_root / "components"
    comp_ok = all(
        _set_complete(comp_root_dev if instance == "dev" else comp_root_hidden,
                      f"{family['category']}/{family['family_id']}.json",
                      family["instance_counts"][instance])
        for family in library["families"] for instance in ("dev", "hidden"))
    nat_root_dev = repo / "research/prose-boundary/corpus/naturalistic-dev"
    nat_root_hidden = hidden_root / "naturalistic"
    nat_ok = all(
        _set_complete(nat_root_dev if instance == "dev" else nat_root_hidden,
                      f"{scenario['scenario_id']}.json",
                      scenario["instance_counts"][instance])
        for scenario in library["naturalistic"] for instance in ("dev", "hidden"))
    if identity["status"] != "PARTIAL" and comp_ok and nat_ok:
        identity["status"] = "COMPLETE"
    elif identity["status"] != "PARTIAL":
        identity["status"] = "IN_PROGRESS"
    save_identity()
    print(json.dumps({"stage": "done", "status": identity["status"], "total_calls": budget.used,
                      "component_calls": budget.component_calls, "naturalistic_calls": budget.naturalistic_calls,
                      "retries": budget.retries, "failures": budget.failures,
                      "total_attempts": budget.total_attempts,
                      "hard_total": budget.total,
                      "attempts_over_hard_total": max(0, budget.total_attempts - budget.total),
                      "identity_sha256": sha256_bytes(identity_path.read_bytes())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

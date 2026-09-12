"""Disposable full-history tests for immutable invalid-report recovery."""
import base64
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
from oap_core import (OAPError, check_transcript, digest, git, prove_forward_report_recovery,
                      protocol_state, read, strategic_gate, validate_order,
                      validate_report_draft, verify_report)
from oap_runtime import launch


REPO = Path(__file__).resolve().parents[2]
HISTORY_SOURCE_ENV = "OAP_FORWARD_RECOVERY_HISTORY_SOURCE"
ORDER = REPO / "oap/orders/007-e-recover-forward-from-an-immutable-invalid-report.md"
E_NAME = ORDER.name
E_ORDER_PATH = "oap/orders/" + E_NAME
E_REPORT_PATH = "oap/reports/" + E_NAME
PRIOR_ID = "007-d"
PUBLICATION = "88af5cefb76e5aaf727806ff589df93fa08f0861"
IMPLEMENTATION = "97eceffa4c1ca60f1b0cea0fef30a4dc54be18df"
REPOSITORY = "ulfe-lmi/llm-slovenian-repair"

def select_scratch(environ):
    """Choose an explicit safe scratch root or the runner-owned GHA fallback."""
    for name in ("TMPDIR", "RUNNER_TEMP"):
        value = environ.get(name)
        if not value:
            continue
        candidate = Path(value).expanduser().absolute()
        if candidate == Path("/tmp") or Path("/tmp") in candidate.parents:
            continue
        return candidate
    raise ValueError("a persistent TMPDIR or runner-owned RUNNER_TEMP is required; /tmp is rejected")


def history_source(environ=None):
    """Resolve a caller-provided Git worktree, or this checkout by default."""
    environ = os.environ if environ is None else environ
    configured = environ.get(HISTORY_SOURCE_ENV)
    candidate = Path(configured).expanduser() if configured else REPO
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ValueError("forward-recovery history source is unavailable") from exc
    if not resolved.is_dir() or resolved.is_symlink():
        raise ValueError("forward-recovery history source must be a real directory")
    result = subprocess.run(
        ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        raise ValueError("forward-recovery history source must be a Git worktree")
    try:
        top_level = Path(result.stdout.strip()).resolve(strict=True)
    except OSError as exc:
        raise ValueError("forward-recovery Git worktree is unavailable") from exc
    if top_level != resolved:
        raise ValueError("forward-recovery history source is not the Git worktree root")
    return resolved


PERSISTENT_TMPDIR = select_scratch(os.environ)


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def replace_metadata(data, tag, change):
    marker = ("```" + tag + "\n").encode()
    start = data.index(marker) + len(marker)
    end = data.index(b"```", start)
    value = json.loads(data[start:end])
    change(value)
    return data[:start] + json_bytes(value) + data[end:]


class RecoveryRemote:
    repository = REPOSITORY

    def __init__(self, head=PUBLICATION):
        self.calls = []
        self.prs = {
            8: {
                "number": 8,
                "state": "open",
                "merged": False,
                "draft": False,
                "created_at": "2026-09-06T09:00:00Z",
                "head": {"sha": head, "ref": "oap/007-concept-verification"},
                "base": {"ref": "main", "repo": {"full_name": REPOSITORY}},
            }
        }
        self.responses = {}

    def pr(self, number):
        self.calls.append(("pr", number))
        if number not in self.prs:
            raise OAPError("REMOTE_UNVERIFIED")
        return copy.deepcopy(self.prs[number])

    def branch_prs(self, branch):
        self.calls.append(("branch_prs", branch))
        return [copy.deepcopy(self.prs[8])] if branch == self.prs[8]["head"]["ref"] else []

    def api(self, path):
        self.calls.append(("api", path))
        if path not in self.responses:
            raise OAPError("REMOTE_UNVERIFIED")
        return copy.deepcopy(self.responses[path])


class ForwardRecoveryTests(unittest.TestCase):
    def test_scratch_selection_requires_an_owned_non_tmp_root(self):
        self.assertEqual(select_scratch({"TMPDIR": "/persistent/work"}), Path("/persistent/work"))
        self.assertEqual(select_scratch({"RUNNER_TEMP": "/runner/_temp"}), Path("/runner/_temp"))
        self.assertEqual(select_scratch({"TMPDIR": "/tmp", "RUNNER_TEMP": "/runner/_temp"}), Path("/runner/_temp"))
        with self.assertRaises(ValueError):
            select_scratch({})
        with self.assertRaises(ValueError):
            select_scratch({"TMPDIR": "/tmp"})

    def test_history_source_defaults_to_this_self_contained_worktree(self):
        if (REPO / ".git").exists():
            self.assertEqual(history_source({}), REPO.resolve())
        else:
            with self.assertRaises(ValueError):
                history_source({})

    def test_history_source_accepts_only_an_explicit_real_git_worktree(self):
        self.assertEqual(history_source({HISTORY_SOURCE_ENV: str(self.repo)}), self.repo.resolve())
        nongit = self.root / "not-a-git-worktree"
        nongit.mkdir()
        with self.assertRaises(ValueError):
            history_source({HISTORY_SOURCE_ENV: str(nongit)})

    def setUp(self):
        PERSISTENT_TMPDIR.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="oap-forward-recovery-", dir=PERSISTENT_TMPDIR)
        self.root = Path(self.temp.name)
        self.repo = self.root / "full-history-repo"
        source = history_source()
        env = os.environ.copy()
        env["TMPDIR"] = str(PERSISTENT_TMPDIR)
        result = subprocess.run(
            ["git", "clone", "--shared", str(source), str(self.repo)],
            capture_output=True, text=True, env=env, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        git(self.repo, "checkout", "--detach", PUBLICATION)
        git(self.repo, "config", "user.name", "Synthetic recovery fixture")
        git(self.repo, "config", "user.email", "synthetic@example.invalid")
        self.remote = RecoveryRemote()

    def tearDown(self):
        self.temp.cleanup()

    def error(self, code, function, *args, **kwargs):
        with self.assertRaises(OAPError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def order_data(self):
        return read(ORDER)

    def install_order(self, *, active="007-e"):
        path = self.repo / "oap/orders" / E_NAME
        path.write_bytes(self.order_data())
        (self.repo / "oap/active").write_text(active + "\n")
        return path

    def commit_paths(self, paths, message):
        git(self.repo, "add", "-f", "--", *paths)
        git(self.repo, "-c", "commit.gpgsign=false", "commit", "-m", message)
        return git(self.repo, "rev-parse", "HEAD").decode().strip()

    def new_order(self, data=None, path=E_ORDER_PATH, ident="007-e"):
        data = self.order_data() if data is None else data
        return validate_order(data, self.repo, ident, Path(path).name)

    def make_e_report(self, implementation_head):
        prior = read(self.repo / "oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md")

        def change(value):
            value.update(
                id="007-e",
                order_path=E_ORDER_PATH,
                order_sha256=digest(self.order_data()),
                implementation_head=implementation_head,
                publication_commit="SELF",
                publication_verified=False,
                pr_mode="AMEND_EXISTING_PR",
                pr=8,
                pr_url=f"https://github.com/{REPOSITORY}/pull/8",
                pr_state="open",
                branch="oap/007-concept-verification",
                base_sha="ee2d1b479719009ff1d07829478f241e3f395f7c",
                starting_remote_sha=PUBLICATION,
                no_merge=True,
                critical_action="NONE",
            )
            value["checks"] = [dict(check, sha=implementation_head) for check in value["checks"]]
            value["pr_observed_at"] = "2026-09-12T09:00:00+00:00"
            value["report_written_at"] = "2026-09-12T09:01:00+00:00"

        return replace_metadata(prior, "oap-report", change)

    def publish_e_report(self):
        self.install_order()
        implementation = self.commit_paths(
            [E_ORDER_PATH, "oap/active"], "Synthetic 007-e implementation history"
        )
        draft = self.root / "unpublished-007-e-draft.md"
        draft.write_bytes(self.make_e_report(implementation))
        self.assertEqual(validate_report_draft(self.repo, draft, "007-e")["implementation_head"], implementation)
        report = self.repo / "oap/reports" / E_NAME
        report.write_bytes(draft.read_bytes())
        publication = self.commit_paths([E_REPORT_PATH], "Synthetic 007-e report publication")
        self.remote.prs[8]["head"]["sha"] = publication
        self.remote.responses["commits/" + publication] = {
            "parents": [{"sha": implementation}], "files": [{"filename": E_REPORT_PATH}],
        }
        self.remote.responses["contents/" + E_REPORT_PATH + "?ref=" + publication] = {
            "encoding": "base64", "content": base64.b64encode(report.read_bytes()).decode(),
        }
        return implementation, publication, draft, report

    def test_initial_publisher_transition_uses_forward_recovery(self):
        data = self.order_data()
        self.install_order(active=PRIOR_ID)
        transition_order = self.new_order(data)
        from oap_core import transition
        transition(self.repo, transition_order, self.remote,
                   new_order_data=data, new_order_path=E_ORDER_PATH)
        self.assertIn(("pr", 8), self.remote.calls)

    def test_initial_publisher_keeps_exact_old_head_enforcement(self):
        self.install_order(active=PRIOR_ID)
        self.remote.prs[8]["head"]["sha"] = IMPLEMENTATION
        from oap_core import transition
        self.error(
            "RECOVERY_REMOTE_HEAD", transition, self.repo, self.new_order(), self.remote,
            new_order_data=self.order_data(), new_order_path=E_ORDER_PATH,
        )

    def test_same_id_activation_retry_reproves_forward_recovery(self):
        self.install_order(active="007-e")
        from oap_core import transition
        transition(self.repo, self.new_order(), self.remote)
        self.assertFalse((self.repo / "oap/reports" / E_NAME).exists())

    def test_exact_prior_report_is_quarantined_but_not_accepted(self):
        self.error("REPORT_CHECK", verify_report, self.repo, PRIOR_ID, commit=PUBLICATION)
        self.install_order()
        result = prove_forward_report_recovery(
            self.repo, "007-e", order_data=self.order_data(), order_path=E_ORDER_PATH
        )
        self.assertEqual(result["classification"], "INVALID_QUARANTINED")
        self.assertEqual(result["validation_error"], "REPORT_CHECK")

    def test_real_history_negative_contracts(self):
        cases = [
            ("missing linkage", lambda value: value.pop("prior_report_recovery"), "RECOVERY_LINKAGE_MISSING", E_ORDER_PATH, "007-e"),
            ("wrong classification", lambda value: value["prior_report_recovery"].update(classification="VALIDATED"), "RECOVERY_CLASSIFICATION", E_ORDER_PATH, "007-e"),
            ("wrong corrective id", lambda value: value["prior_report_recovery"].update(corrective_id="007-f"), "RECOVERY_CORRECTIVE_ID", E_ORDER_PATH, "007-e"),
            ("missing reason", lambda value: value["prior_report_recovery"].update(reason=""), "RECOVERY_REASON", E_ORDER_PATH, "007-e"),
            ("wrong report hash", lambda value: value["prior_report_recovery"].update(report_sha256="0" * 64), "RECOVERY_REPORT_BYTES", E_ORDER_PATH, "007-e"),
            ("wrong order hash", lambda value: value["prior_report_recovery"].update(order_sha256="0" * 64), "RECOVERY_ORDER_BYTES", E_ORDER_PATH, "007-e"),
            ("wrong declared error", lambda value: value["prior_report_recovery"].update(validation_error="OK"), "RECOVERY_VALIDATION_ERROR", E_ORDER_PATH, "007-e"),
            ("arbitrary path", lambda value: value["prior_report_recovery"].update(report_path="oap/reports/007-d-alternate.md", order_path="oap/orders/007-d-alternate.md"), "RECOVERY_REPORT_PATH", E_ORDER_PATH, "007-e"),
            ("wrong parent", lambda value: value["prior_report_recovery"].update(implementation_parent="0" * 40), "RECOVERY_REPORT_PARENT", E_ORDER_PATH, "007-e"),
            ("branch mismatch", lambda value: value["prior_report_recovery"].update(branch="other-branch"), "RECOVERY_BRANCH", E_ORDER_PATH, "007-e"),
            ("PR mismatch", lambda value: value["prior_report_recovery"].update(pr=9), "RECOVERY_PR", E_ORDER_PATH, "007-e"),
            ("suffix gap", lambda value: (value.update(id="007-f"), value["prior_report_recovery"].update(corrective_id="007-f")), "RECOVERY_SUFFIX_SEQUENCE", "oap/orders/007-f-recover-forward-from-an-immutable-invalid-report.md", "007-f"),
            ("numeric advance", lambda value: (value.update(id="008-a", objective="008", pr_mode="CREATE_NEW_PR", pr=None), value["prior_report_recovery"].update(corrective_id="008-a")), "RECOVERY_NUMERIC_ADVANCE", "oap/orders/008-a-recover-forward-from-an-immutable-invalid-report.md", "008-a"),
            ("same-ID rewrite", lambda value: value.update(id="007-d", prior_report_recovery={**value["prior_report_recovery"], "corrective_id": "007-d"}), "RECOVERY_SAME_ID", "oap/orders/007-d-recover-forward-from-an-immutable-invalid-report.md", "007-d"),
        ]
        for name, change, code, path, ident in cases:
            with self.subTest(name=name):
                data = replace_metadata(self.order_data(), "oap-metadata", change)
                self.error(code, prove_forward_report_recovery, self.repo, ident,
                           order_data=data, order_path=path)

    def test_mutation_history_is_rejected(self):
        report_path = self.repo / "oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md"
        report_path.write_bytes(report_path.read_bytes() + b"mutation\n")
        self.commit_paths(["oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md"], "Synthetic report mutation")
        self.error("REPORT_HISTORY_MUTATION", prove_forward_report_recovery, self.repo, "007-e",
                   order_data=self.order_data(), order_path=E_ORDER_PATH)

    def test_delete_readd_history_is_rejected(self):
        report_path = self.repo / "oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md"
        original = report_path.read_bytes()
        report_path.unlink()
        self.commit_paths(["oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md"], "Synthetic report deletion")
        report_path.write_bytes(original)
        self.commit_paths(["oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md"], "Synthetic report re-addition")
        self.error("REPORT_HISTORY_MUTATION", prove_forward_report_recovery, self.repo, "007-e",
                   order_data=self.order_data(), order_path=E_ORDER_PATH)

    def test_draft_preflight_requires_unpublished_full_sha_ancestor(self):
        self.install_order()
        implementation = self.commit_paths([E_ORDER_PATH, "oap/active"], "Synthetic draft implementation")
        draft = self.root / "draft.md"
        valid = self.make_e_report(implementation)
        short = replace_metadata(valid, "oap-report", lambda value: value["checks"].__setitem__(0, dict(value["checks"][0], sha="33e8d9a")))
        draft.write_bytes(short)
        self.error("REPORT_CHECK", validate_report_draft, self.repo, draft, "007-e")
        draft.write_bytes(valid)
        self.assertEqual(validate_report_draft(self.repo, draft, "007-e")["result"], "valid unpublished report draft")
        (self.repo / "oap/reports" / E_NAME).write_bytes(valid)
        self.error("DRAFT_REPORT_ALREADY_PUBLISHED", validate_report_draft, self.repo, draft, "007-e")

    def test_transcript_index_and_revision_quarantine_only_after_valid_successor(self):
        self.install_order()
        self.commit_paths([E_ORDER_PATH, "oap/active"], "Synthetic corrective order")
        revision = git(self.repo, "rev-parse", "HEAD").decode().strip()
        result = check_transcript(self.repo, revision=revision, expected_id="007-e")
        self.assertNotIn("007-e", result["reports"])
        self.assertEqual(result["quarantined_reports"][0]["id"], PRIOR_ID)

        self.temp.cleanup()
        self.setUp()
        self.install_order()
        git(self.repo, "add", "-f", "--", E_ORDER_PATH, "oap/active")
        result = check_transcript(self.repo, index=True, expected_id="007-e")
        self.assertEqual(result["quarantined_reports"][0]["classification"], "INVALID_QUARANTINED")

    def test_disconnected_transcript_revision_cannot_launder_recovery(self):
        self.install_order()
        order_blob = git(self.repo, "hash-object", "-w", "--", E_ORDER_PATH).decode().strip()
        active_blob = git(self.repo, "hash-object", "-w", "--", "oap/active").decode().strip()
        git(self.repo, "read-tree", "HEAD")
        git(self.repo, "update-index", "--add", "--cacheinfo", "100644," + order_blob + "," + E_ORDER_PATH)
        git(self.repo, "update-index", "--add", "--cacheinfo", "100644," + active_blob + ",oap/active")
        tree = git(self.repo, "write-tree").decode().strip()
        forged_process = subprocess.run(
            ["git", "-C", str(self.repo), "-c", "gc.auto=0", "commit-tree", tree, "-p", IMPLEMENTATION],
            input=b"forged disconnected transcript\n", capture_output=True,
            env={**os.environ, "TMPDIR": str(PERSISTENT_TMPDIR)}, timeout=30,
        )
        self.assertEqual(forged_process.returncode, 0, forged_process.stderr.decode())
        forged = forged_process.stdout.decode().strip()
        self.error("RECOVERY_TRANSCRIPT_ANCESTRY", check_transcript, self.repo,
                   revision=forged, expected_id="007-e")

    def test_malformed_current_report_without_successor_blocks(self):
        self.error("RECOVERY_LINKAGE_MISSING", check_transcript, self.repo,
                   revision=PUBLICATION, expected_id=PRIOR_ID)

    def test_protocol_state_uses_local_recovery_after_implementation(self):
        strategy = self.root / "strategy"
        (strategy / "workorders").mkdir(parents=True)
        self.install_order()
        implementation = self.commit_paths(
            [E_ORDER_PATH, "oap/active"], "Synthetic corrective implementation"
        )
        self.remote.prs[8]["head"] = {
            "sha": implementation, "ref": "oap/007-concept-verification"
        }
        (strategy / "workorders/consumed.json").write_bytes(
            json_bytes({"id": "007-e", "phase": "consumed"})
        )
        before = list(self.remote.calls)
        state = protocol_state(self.repo, strategy=strategy, remote=self.remote)
        self.assertEqual(state["state"], "RECOVERY_REQUIRED")
        self.assertEqual(before, self.remote.calls)

    def test_protocol_state_valid_corrective_report_is_review_ready(self):
        _, publication, _, _ = self.publish_e_report()
        state = protocol_state(self.repo, remote=self.remote)
        self.assertEqual(state["state"], "REVIEW_READY")
        self.assertEqual(state["prior_report_recovery"]["classification"], "INVALID_QUARANTINED")
        self.assertEqual(self.remote.prs[8]["head"]["sha"], publication)

    def test_protocol_state_malformed_current_corrective_report_blocks(self):
        _, _, _, report = self.publish_e_report()
        malformed = replace_metadata(
            report.read_bytes(), "oap-report",
            lambda value: value["checks"].__setitem__(0, dict(value["checks"][0], sha="33e8d9a")),
        )
        report.write_bytes(malformed)
        self.error("REPORT_CHECK", protocol_state, self.repo, remote=self.remote)

    def test_duplicate_control_suppresses_invalid_old_round_and_invokes_new_round(self):
        strategy = self.root / "strategy"
        (strategy / "workorders").mkdir(parents=True)
        config = {"OAP_REPO_ROOT": str(self.repo), "OAP_STRATEGIC_HOME": str(strategy),
                  "OAP_FIFO_HOME": str(strategy), "OAP_GITHUB_REPOSITORY": REPOSITORY}
        context = {"argv": ["synthetic-model"], "cwd": str(self.repo), "env": {}, "role": "coding"}
        with patch.dict(os.environ, {"OAP_ROLE": "coding"}), \
                patch("oap_runtime.role_context", return_value=context), \
                patch("oap_runtime.GitHub", return_value=self.remote), \
                patch("oap_runtime.fifo") as consume, patch("oap_runtime.run_model") as model:
            self.error("REPORT_CHECK", launch, config, "coding", once=True)
            consume.assert_called_once()
            model.assert_not_called()

            self.install_order()
            model.return_value = subprocess.CompletedProcess(["synthetic-model"], 0)
            self.error("REPORT_OR_ORDER_MISSING", launch, config, "coding", once=True)
            self.assertEqual(model.call_count, 1)

    def test_strategic_gate_requires_shared_report_verification(self):
        with patch.dict(os.environ, {"OAP_ROLE": "strategic"}):
            self.error("REPORT_REPOSITORY_REQUIRED", strategic_gate, self.remote, 8, PUBLICATION,
                       ["OAP report history"], merge_effect="development-only")
            implementation, publication, _, _ = self.publish_e_report()
            self.remote.responses[f"commits/{publication}/check-runs?per_page=100"] = {
                "total_count": 1,
                "check_runs": [{"name": "OAP report history", "head_sha": publication,
                                 "status": "completed", "conclusion": "success"}],
            }
            result = strategic_gate(self.remote, 8, publication, ["OAP report history"],
                                    merge_effect="development-only", repo=self.repo,
                                    report_id="007-e")
            self.assertTrue(result["report_verified"])
            self.assertEqual(implementation, git(self.repo, "rev-parse", "HEAD^").decode().strip())


if __name__ == "__main__":
    unittest.main()

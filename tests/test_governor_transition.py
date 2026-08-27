from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import validate_governor_transition as TRANSITION  # noqa: E402


def run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def git_bytes(root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def evaluator(version: str) -> dict[str, str]:
    return {
        "archive_name": f"se_harness-{version}-py3-none-any.whl",
        "archive_sha256": "a" * 64,
        "payload_manifest": "se-harness-installed-payload-v1",
        "payload_sha256": "b" * 64,
        "version": version,
    }


def config(version: str) -> bytes:
    return (
        "[harness]\n"
        "schema_version = 2\n"
        f'tool_version = "{version}"\n'
        'project_name = "fixture"\n'
        'artifact_root = "docs/engineering"\n'
    ).encode("utf-8")


def lock(version: str, *, schema: int, identity: dict[str, str] | None) -> bytes:
    value: dict[str, object] = {
        "files": {},
        "hash_algorithm": "sha256",
        "hash_mode": "utf8-text-lf-v1",
        "schema": schema,
        "tool_version": version,
    }
    if identity is not None:
        value["evaluator"] = identity
    return json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def write(root: Path, relative: str, raw: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


class RepositoryFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        run_git(root, "init")
        run_git(root, "config", "user.email", "fixture@example.invalid")
        run_git(root, "config", "user.name", "Fixture")

    def commit(self, message: str) -> str:
        run_git(self.root, "add", "--all")
        run_git(self.root, "commit", "-m", message)
        return run_git(self.root, "rev-parse", "HEAD")

    def base(self, version: str = "7.4.0", *, distribution_schema: int = 2) -> str:
        write(self.root, ".engineering-harness.toml", config(version))
        write(self.root, ".engineering-harness.lock", lock(version, schema=3, identity=evaluator(version)))
        released = evaluator("7.5.0")
        release = f'''+++
id = "RLS-TST-001"
type = "release_record"
title = "Released target fixture"
status = "released"
owners = ["release-owner"]
created = "2026-08-23"
updated = "2026-08-23"
version = "7.5.0"
commit = "{'1' * 40}"
git_object_format = "sha1"
released_at = "2026-08-23T00:00:00Z"
authorized_by = "release-owner"
tag = "v7.5.0"

[distribution]
schema = {distribution_schema}
kind = "python-wheel-sdist"
wheel = "{released['archive_name']}"
wheel_sha256 = "{released['archive_sha256']}"
sdist = "se_harness-7.5.0.tar.gz"
sdist_sha256 = "{'2' * 64}"

[relations]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-08-23T00:00:00Z"
decided_by = "release-owner"
+++

# Released target fixture
'''.encode("utf-8")
        write(self.root, "docs/engineering/sample/releases/RLS-TST-001.md", release)
        return self.commit("base")

    def target(
        self,
        base: str,
        version: str = "7.5.0",
        *,
        work_order: str | None = None,
        archive: str = "lock",
        evidence_name: str = "evaluator-upgrade.json",
    ) -> str:
        """Write the target root and the retained transaction document of the simple upgrade.

        `archive="null"` records no archive pair in the lock (an index install,
        REQ-REB-028); `work_order` is the optional id the transaction may name.
        """

        identity: dict[str, object] = dict(evaluator(version))
        if archive == "null":
            identity["archive_name"] = None
            identity["archive_sha256"] = None
        write(self.root, ".engineering-harness.toml", config(version))
        write(self.root, ".engineering-harness.lock", lock(version, schema=3, identity=identity))
        base_lock = git_bytes(self.root, "show", f"{base}:.engineering-harness.lock")
        prior_sha = hashlib.sha256(TRANSITION._canonical_lf(base_lock, "base lock")).hexdigest()
        evidence = {
            "authority": "read-only fixture",
            "authorization_path": None,
            "authorized_by": None,
            "plan": [],
            "postconditions": {
                "external_action_performed": False,
                "lock_matches_target": True,
                "no_op_replay": True,
                "product_release_performed": False,
            },
            "prior": {
                "evaluator": evaluator("7.4.0"),
                "lock_match": None,
                "lock_sha256": prior_sha,
                "tool_version": "7.4.0",
            },
            "schema": "se-harness-evaluator-upgrade-evidence-v1",
            "scope": "standard-root-only",
            "target": identity,
            "transaction": {
                "atomic": True,
                "outcome": "applied",
                "rollback": "fixture",
            },
            "work_order": work_order,
        }
        write(
            self.root,
            f"docs/engineering/sample/evidence/{evidence_name}",
            canonical_json(evidence),
        )
        return self.commit("target")


class GovernorTransitionTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], RepositoryFixture]:
        temporary = tempfile.TemporaryDirectory()
        return temporary, RepositoryFixture(Path(temporary.name))

    def test_changed_version_selects_exact_approved_transition(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            head = fixture.target(base)
            plan = TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")
        self.assertTrue(plan["transition_required"])
        self.assertEqual(base, plan["base"]["commit"])
        self.assertEqual(head, plan["target"]["commit"])
        self.assertEqual("7.5.0", plan["target"]["version"])
        self.assertEqual("docs/engineering/sample/evidence/evaluator-upgrade.json", plan["transition"]["evidence_path"])
        self.assertIsNone(plan["transition"]["work_order"])
        self.assertEqual("lock", plan["transition"]["archive_source"])
        self.assertEqual("RLS-TST-001", plan["transition"]["trusted_release"]["id"])

    def test_index_installed_target_takes_its_wheel_from_the_trusted_release(self) -> None:
        """SPEC-REB-012: a null archive pair is an index install; the released record
        binding the version supplies the wheel the assessment installs."""
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base, archive="null")
            plan = TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")
        self.assertTrue(plan["transition_required"])
        self.assertEqual("trusted-release", plan["transition"]["archive_source"])
        released = evaluator("7.5.0")
        self.assertEqual(released["archive_name"], plan["target"]["evaluator"]["archive_name"])
        self.assertEqual(released["archive_sha256"], plan["target"]["evaluator"]["archive_sha256"])
        self.assertEqual(released["payload_sha256"], plan["target"]["evaluator"]["payload_sha256"])

    def test_schema_one_release_record_is_still_a_trusted_release(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base(distribution_schema=1)
            fixture.target(base)
            plan = TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")
        self.assertTrue(plan["transition_required"])

    def test_recorded_archive_must_equal_the_trusted_release(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            lock_path = fixture.root / ".engineering-harness.lock"
            value = json.loads(lock_path.read_text(encoding="utf-8"))
            value["evaluator"]["archive_sha256"] = "d" * 64
            write(fixture.root, ".engineering-harness.lock", canonical_json(value))
            evidence = fixture.root / "docs/engineering/sample/evidence/evaluator-upgrade.json"
            document = json.loads(evidence.read_text(encoding="utf-8"))
            document["target"]["archive_sha256"] = "d" * 64
            evidence.write_bytes(canonical_json(document))
            fixture.commit("foreign archive")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "differs from the trusted base"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_same_version_and_lock_are_not_a_transition(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            write(fixture.root, "notes.txt", b"ordinary change\n")
            fixture.commit("ordinary")
            plan = TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")
            result = TRANSITION.assess(
                str(fixture.root), base, "refs/remotes/origin/main", None, None, None
            )
        self.assertFalse(plan["transition_required"])
        self.assertEqual("not_applicable", result["assessment"])
        self.assertEqual({}, result["commands"])

    def test_same_version_lock_drift_fails_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            changed = json.loads((fixture.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
            changed["files"] = {"unexpected": {"mode": "managed", "sha256": "c" * 64}}
            write(fixture.root, ".engineering-harness.lock", canonical_json(changed))
            fixture.commit("drift")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "same-version"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_wrong_prior_lock_fails_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            path = fixture.root / "docs/engineering/sample/evidence/evaluator-upgrade.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["prior"]["lock_sha256"] = "0" + value["prior"]["lock_sha256"][1:]
            path.write_bytes(canonical_json(value))
            fixture.commit("wrong prior")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "exactly one"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_target_archive_requires_one_released_record_in_the_trusted_base(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            write(fixture.root, ".engineering-harness.toml", config("7.4.0"))
            write(
                fixture.root,
                ".engineering-harness.lock",
                lock("7.4.0", schema=3, identity=evaluator("7.4.0")),
            )
            base = fixture.commit("base without target release")
            fixture.target(base)
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "trusted base"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_declared_crlf_materialization_binds_the_exact_base_blob(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            base_raw = git_bytes(fixture.root, "show", f"{base}:.engineering-harness.lock")
            canonical = TRANSITION._canonical_lf(base_raw, "base lock")
            crlf = canonical.decode("utf-8").replace("\n", "\r\n").encode("utf-8")
            crlf_sha = hashlib.sha256(crlf).hexdigest()
            lf_sha = hashlib.sha256(canonical).hexdigest()
            self.assertNotEqual(lf_sha, crlf_sha)
            evidence = fixture.root / "docs/engineering/sample/evidence/evaluator-upgrade.json"
            value = json.loads(evidence.read_text(encoding="utf-8"))
            value["prior"]["lock_sha256"] = crlf_sha
            evidence.write_bytes(canonical_json(value))
            fixture.commit("crlf-bound transition")
            plan = TRANSITION.build_plan(
                str(fixture.root), base, "refs/remotes/origin/main"
            )
        self.assertTrue(plan["transition_required"])
        self.assertEqual("docs/engineering/sample/evidence/evaluator-upgrade.json", plan["transition"]["evidence_path"])

    def test_multiple_matching_evidence_documents_fail_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            source = fixture.root / "docs/engineering/sample/evidence/evaluator-upgrade.json"
            write(
                fixture.root,
                "docs/engineering/other/evidence/second-upgrade.json",
                source.read_bytes(),
            )
            fixture.commit("duplicate")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "exactly one"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_noncanonical_evidence_fails_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            path = fixture.root / "docs/engineering/sample/evidence/evaluator-upgrade.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
            fixture.commit("noncanonical evidence")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "canonical JSON"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_branch_creation_uses_one_default_branch_merge_base(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            run_git(fixture.root, "update-ref", "refs/remotes/origin/main", base)
            plan = TRANSITION.build_plan(
                str(fixture.root), "0" * 40, "refs/remotes/origin/main"
            )
        self.assertEqual("merge-base", plan["base_source"])
        self.assertEqual(base, plan["base"]["commit"])

    def test_abbreviated_or_nonancestor_base_fails_closed(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "full lowercase"):
                TRANSITION.build_plan(str(fixture.root), base[:12], "refs/remotes/origin/main")

    def test_dirty_worktree_fails_before_planning(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            write(fixture.root, "dirty.txt", b"dirty\n")
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "must be clean"):
                TRANSITION.build_plan(str(fixture.root), base, "refs/remotes/origin/main")

    def test_canonical_hash_is_independent_of_lf_or_crlf_materialization(self) -> None:
        lf = b"first\nsecond\n"
        crlf = b"first\r\nsecond\r\n"
        self.assertEqual(
            hashlib.sha256(TRANSITION._canonical_lf(lf, "lf")).hexdigest(),
            hashlib.sha256(TRANSITION._canonical_lf(crlf, "crlf")).hexdigest(),
        )

    def test_changed_version_assessment_requires_external_exact_evaluator(self) -> None:
        temporary, fixture = self.fixture()
        with temporary:
            base = fixture.base()
            fixture.target(base)
            with self.assertRaisesRegex(TRANSITION.GovernorTransitionError, "requires exact"):
                TRANSITION.assess(
                    str(fixture.root), base, "refs/remotes/origin/main", None, None, None
                )

    @unittest.skipIf(os.name == "nt", "POSIX virtual environments use symlinked Python launchers")
    def test_posix_python_symlink_preserves_the_virtual_environment_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / "checkout"
            checkout.mkdir()
            environment = root / "target-evaluator"
            launchers = environment / "bin"
            launchers.mkdir(parents=True)
            system_python = root / "system" / "python"
            system_python.parent.mkdir()
            system_python.write_bytes(b"python")
            python = launchers / "python"
            python.symlink_to(system_python)
            entry_point = launchers / "harnessctl"
            entry_point.write_bytes(b"harnessctl")

            actual_python, actual_entry_point, actual_root = (
                TRANSITION._evaluator_installation(
                    str(python), str(entry_point), checkout.resolve()
                )
            )
            resolved_python = actual_python.resolve()

            self.assertEqual(python, actual_python)
            self.assertEqual(entry_point, actual_entry_point)
            self.assertEqual(environment, actual_root)
            self.assertEqual(system_python, resolved_python)

    @unittest.skipIf(os.name == "nt", "POSIX virtual environments use symlinked Python launchers")
    def test_python_symlink_resolving_into_the_checkout_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / "checkout"
            checkout.mkdir()
            checkout_python = checkout / "python"
            checkout_python.write_bytes(b"python")
            launchers = root / "target-evaluator" / "bin"
            launchers.mkdir(parents=True)
            python = launchers / "python"
            python.symlink_to(checkout_python)
            entry_point = launchers / "harnessctl"
            entry_point.write_bytes(b"harnessctl")

            with self.assertRaisesRegex(
                TRANSITION.GovernorTransitionError, "outside the checkout"
            ):
                TRANSITION._evaluator_installation(
                    str(python), str(entry_point), checkout.resolve()
                )

    def test_entry_point_outside_the_launcher_directory_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkout = root / "checkout"
            checkout.mkdir()
            launchers = root / "target-evaluator" / (
                "Scripts" if os.name == "nt" else "bin"
            )
            launchers.mkdir(parents=True)
            python = launchers / ("python.exe" if os.name == "nt" else "python")
            python.write_bytes(b"python")
            entry_point = root / "other" / (
                "harnessctl.exe" if os.name == "nt" else "harnessctl"
            )
            entry_point.parent.mkdir()
            entry_point.write_bytes(b"harnessctl")

            with self.assertRaisesRegex(
                TRANSITION.GovernorTransitionError,
                "outside the evaluator installation",
            ):
                TRANSITION._evaluator_installation(
                    str(python), str(entry_point), checkout.resolve()
                )


if __name__ == "__main__":
    unittest.main()

"""Independent OWN01–OWN14 acceptance for the approved seven-file migration.

The expected catalog and retained bytes are fixed fixtures, not planner output.
Source runs explicitly mock only installed-evaluator authority. The identical
suite also runs from an isolated installed candidate, without those mocks.
Set SE_HARNESS_OWNERSHIP_EVIDENCE to an explicit directory outside this checkout
to retain observations; ordinary test discovery creates no repository evidence.
"""
from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock
import uuid

from se_harness import __version__
from se_harness import installer
from se_harness import skill_ownership as ownership
from se_harness.evaluator_identity import InstalledEvaluatorIdentity, installed_evaluator_identity
from se_harness.integrity import IntegrityError
from se_harness.preflight import inspect_installation


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "skill_ownership"
EXPECTED = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
CATALOG = tuple(EXPECTED["repository_catalog"])
RETAINED = tuple(sorted(EXPECTED["retained_files"]))
LOCK = ".engineering-harness.lock"
PENDING = ".engineering-harness.skill-ownership.pending.json"
PACKAGE = os.environ.get("SE_HARNESS_OWNERSHIP_PACKAGE") == "1"
INERT_WHEEL = b"inert independent acceptance archive; never imported or extracted\n"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def canonical_text(raw: bytes) -> bytes:
    return raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def snapshot(root: Path) -> dict[str, dict]:
    """Record ordinary bytes and directories without following hostile links."""
    observed = {}
    if not root.exists():
        return observed
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in sorted(directory.iterdir()):
            name = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
                observed[name] = {"kind": "link", "target": os.readlink(path)}
            elif stat.S_ISDIR(info.st_mode):
                observed[name] = {"kind": "directory"}
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                raw = path.read_bytes()
                observed[name] = {"kind": "file", "bytes": len(raw), "sha256": sha(raw)}
            else:
                observed[name] = {"kind": "special", "mode": info.st_mode}
    return observed


def trusted_source_authority(root: Path, **_kwargs) -> SimpleNamespace:
    """Use the repository's shared authority fixture, never a package guard patch."""
    spec = importlib.util.spec_from_file_location("ownership_mutation_test_support", ROOT / "tests" / "mutation_guard_support.py")
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    _kwargs.setdefault("operation", "skill-ownership-apply")
    return support.trusted_mutation_authority(root, **_kwargs)


class OwnershipReadBoundaryTests(unittest.TestCase):
    """Exercise bounded reads and input races without a migration fixture."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="ownership-read-")
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "input.bin"
        self.path.write_bytes(b"a" * 70000)

    def reader(self, *, after_first=None, short_read=None, observations=None):
        original = os.fdopen

        class Reader:
            def __init__(self, *args, **kwargs):
                self.handle = original(*args, **kwargs)
                self.called = False

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return self.handle.__exit__(*args)

            def fileno(self):
                return self.handle.fileno()

            def read(self, size):
                raw = self.handle.read(min(size, short_read) if short_read else size)
                if observations is not None:
                    observations.append((size, len(raw)))
                if not self.called:
                    self.called = True
                    if after_first is not None:
                        after_first()
                return raw

        return mock.patch.object(ownership.os, "fdopen", Reader)

    def test_exact_bytes_at_chunk_and_size_boundaries(self) -> None:
        for size in (0, 1, 65535, 65536, 65537, 131073, ownership.MAX_FILE):
            with self.subTest(size=size):
                expected = (b"0123456789abcdef" * ((size + 15) // 16))[:size]
                self.path.write_bytes(expected)
                self.assertEqual(expected, ownership._read(self.path, limit=size))

    def test_short_reads_preserve_complete_bytes(self) -> None:
        expected = self.path.read_bytes()
        with self.reader(short_read=997):
            self.assertEqual(expected, ownership._read(self.path))

    def test_existing_oversize_refuses_before_open(self) -> None:
        with mock.patch.object(ownership.os, "open") as opened:
            with self.assertRaisesRegex(ownership.OwnershipError, "exceeds size bound"):
                ownership._read(self.path, limit=69999)
            opened.assert_not_called()

    def test_growth_during_read_refuses(self) -> None:
        def grow():
            with self.path.open("ab") as stream:
                stream.write(b"x" * 40000)

        with self.reader(after_first=grow), self.assertRaisesRegex(ownership.OwnershipError, "changed during read"):
            ownership._read(self.path, limit=80000)
        self.assertEqual(110000, self.path.stat().st_size)

    def test_growth_is_bounded_even_with_stale_metadata(self) -> None:
        before = self.path.stat()
        observations = []

        def grow():
            with self.path.open("ab") as stream:
                stream.write(b"x" * 40000)

        with (self.reader(after_first=grow, observations=observations),
              mock.patch.object(ownership, "_ordinary", return_value=before),
              mock.patch.object(ownership.os, "fstat", return_value=before)):
            with self.assertRaisesRegex(ownership.OwnershipError, "changed during read"):
                ownership._read(self.path, limit=80000)
        self.assertEqual(110000, self.path.stat().st_size)
        self.assertEqual(80001, sum(returned for _, returned in observations))
        self.assertLessEqual(max(requested for requested, _ in observations), 65536)

    def test_truncation_during_read_refuses(self) -> None:
        def shrink():
            with self.path.open("r+b") as stream:
                stream.truncate(10)

        with self.reader(after_first=shrink), self.assertRaisesRegex(ownership.OwnershipError, "changed during read"):
            ownership._read(self.path)
        self.assertEqual(10, self.path.stat().st_size)

    def test_changed_timestamp_during_read_refuses(self) -> None:
        before = self.path.stat()

        def touch():
            os.utime(self.path, ns=(before.st_atime_ns, before.st_mtime_ns + 10000000000))

        with self.reader(after_first=touch), self.assertRaisesRegex(ownership.OwnershipError, "changed during read"):
            ownership._read(self.path)
        self.assertNotEqual(before.st_mtime_ns, self.path.stat().st_mtime_ns)

    def test_opened_identity_mismatch_refuses(self) -> None:
        before = self.path.stat()
        changed = SimpleNamespace(st_dev=before.st_dev, st_ino=before.st_ino + 1, st_nlink=1)
        with mock.patch.object(ownership.os, "fstat", return_value=changed):
            with self.assertRaisesRegex(ownership.OwnershipError, "changed while opening"):
                ownership._read(self.path)

    def test_final_path_identity_mismatch_refuses(self) -> None:
        before = self.path.stat()
        changed = SimpleNamespace(st_dev=before.st_dev, st_ino=before.st_ino + 1)
        with mock.patch.object(ownership, "_ordinary", side_effect=[before, changed]):
            with self.assertRaisesRegex(ownership.OwnershipError, "changed during read"):
                ownership._read(self.path)

    def test_hard_link_refuses(self) -> None:
        os.link(self.path, self.path.with_name("alias.bin"))
        with self.assertRaisesRegex(ownership.OwnershipError, "singly linked file required"):
            ownership._read(self.path)

    def test_read_error_refuses(self) -> None:
        def fail():
            raise OSError("injected read error")

        with self.reader(after_first=fail), self.assertRaisesRegex(ownership.OwnershipError, "cannot read input"):
            ownership._read(self.path)


_legacy_reader_spec = importlib.util.spec_from_file_location("ownership_legacy_reader", FIXTURES / "legacy_reader.py")
_legacy_reader = importlib.util.module_from_spec(_legacy_reader_spec)
_legacy_reader_spec.loader.exec_module(_legacy_reader)


class SkillOwnershipAcceptanceTests(_legacy_reader.LegacyReaderCases, unittest.TestCase):
    _legacy_source_root = ROOT
    _legacy_snapshot = staticmethod(snapshot)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ownership-acceptance-")
        self.base = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.events = []
        self.metadata = {"test": self.id(), "platform": platform.platform(),
                         "python": sys.version, "executable": sys.executable,
                         "argv": sys.argv, "mode": "installed-package" if PACKAGE else "source-authority-double",
                         "candidate_commit": os.environ.get("SE_HARNESS_OWNERSHIP_COMMIT"),
                         "case_outcome": "running"}
        if PACKAGE:
            self.identity = installed_evaluator_identity()
            selected = os.environ.get("SE_HARNESS_OWNERSHIP_WHEEL")
            self.assertTrue(selected, "installed package acceptance requires its explicitly selected wheel")
            wheel = Path(selected)
            self.assertTrue(wheel.is_absolute())
            self.wheel_bytes = wheel.read_bytes()
            self.assertEqual(self.identity.archive_sha256, sha(self.wheel_bytes))
            self.assertFalse(Path(importlib.import_module("se_harness").__file__).resolve().is_relative_to(ROOT))
        else:
            self.wheel_bytes = INERT_WHEEL
            self.identity = InstalledEvaluatorIdentity(
                __version__, "se-harness-installed-payload-v1", "a" * 64,
                f"se_harness-{__version__.replace('-', '_')}-py3-none-any.whl", sha(INERT_WHEEL),
            )
            self.stack.enter_context(mock.patch("se_harness.mutation_guard.require_mutation_authority",
                                                side_effect=trusted_source_authority))
            for module in (installer, ownership, importlib.import_module("se_harness.evaluator_identity")):
                if hasattr(module, "installed_evaluator_identity"):
                    self.stack.enter_context(mock.patch.object(module, "installed_evaluator_identity",
                                                                return_value=self.identity))
        self.metadata["evaluator"] = self.identity.to_lock()
        self.root = self.base / "repository"
        changes, old = installer.plan_install(self.root, project_name="ownership-acceptance", mode="init")
        installer.apply_changes(self.root, changes, old, allow_updates=False)
        self.catalog_bytes = {name: (self.root / name).read_bytes() for name in CATALOG}
        self.original_lock = (self.root / LOCK).read_bytes()
        self.plugins = {}
        self.binding_path = self.base / "binding.json"
        self.binding = self.make_binding(("codex", "claude"))
        self.write_binding()

    def tearDown(self) -> None:
        output = os.environ.get("SE_HARNESS_OWNERSHIP_EVIDENCE")
        if not output:
            return
        destination = Path(output)
        if not destination.is_absolute() or destination.resolve().is_relative_to(ROOT.resolve()):
            raise AssertionError("evidence destination must be explicitly outside the source checkout")
        destination.mkdir(parents=True, exist_ok=True)
        result = getattr(self._outcome, "result", None)
        failed = bool(result and any(case is self or getattr(case, "test_case", None) is self
                                     for case, _ in list(result.errors) + list(result.failures)))
        skipped = [{"test": case.id(), "reason": reason}
                   for case, reason in getattr(result, "skipped", ())
                   if case is self or getattr(case, "test_case", None) is self]
        self.metadata["case_outcome"] = ("failed" if failed else
                                         "partial" if skipped and self.events else
                                         "unavailable" if skipped else "passed")
        if skipped:
            self.metadata["skipped_subcases"] = skipped
            self.metadata["unavailable_reason"] = skipped[0]["reason"]
        self.metadata["events"] = self.events
        self.metadata["final_snapshot"] = snapshot(self.base)
        pending = self.root / PENDING
        if pending.is_file():
            self.metadata["retained_recovery_bytes_base64"] = base64.b64encode(pending.read_bytes()).decode()
        name = self._testMethodName + "-" + uuid.uuid4().hex[:8] + ".json"
        (destination / name).write_bytes(canonical(self.metadata))

    def make_binding(self, hosts: tuple[str, ...], *, external_name="external") -> dict:
        binding = {"schema": "se-harness-skill-ownership-binding-v1", "hosts": {}}
        for host in hosts:
            root = self.base / external_name / host / "verity-plane"
            root.mkdir(parents=True, exist_ok=True)
            self.plugins[host] = root
            payload = {}
            for name in RETAINED:
                raw = canonical_text((FIXTURES / "payload" / name).read_bytes())
                self.assertEqual(EXPECTED["retained_files"][name]["sha256"], sha(raw))
                payload[name] = (raw, "shared")
            payload[f".{host}-plugin/plugin.json"] = (canonical({"name": "verity-plane", "version": "1.0.0"}), host)
            payload["scripts/never-execute.py"] = (
                b"from pathlib import Path\nPath(__file__).with_name('EXECUTED').write_text('unsafe')\n", "shared")
            payload["skills/harness-operator-brief/agents/openai.yaml"] = (
                b"policy:\n  allow_implicit_invocation: false\n", "shared")
            payload["packages/" + self.identity.archive_name] = (self.wheel_bytes, "evaluator")
            inventory = {
                "schema": "se-harness-plugin-assembly-v1", "host": host, "plugin": "verity-plane",
                "source": {"revision": "1" * 40, "plan": "fixture/plan.json", "plan_sha256": "2" * 64},
                "evaluator": {"version": self.identity.version, "archive": self.identity.archive_name,
                              "archive_sha256": self.identity.archive_sha256,
                              "payload_sha256": self.identity.payload_sha256,
                              "release_revision": "3" * 40,
                              "release_record": "docs/engineering/fixture/release-records/RLS-TST-001.md",
                              "release_record_sha256": "4" * 64},
                "files": {},
            }
            for name, (raw, origin) in payload.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                inventory["files"][name] = {"sha256": sha(raw), "bytes": len(raw), "mode": 0o644, "origin": origin}
            inventory_raw = canonical(inventory)
            (root / "assembly-inventory.json").write_bytes(inventory_raw)
            binding["hosts"][host] = {"root": str(root), "expected": {
                "plugin": "verity-plane", "version": "1.0.0", "inventory_sha256": sha(inventory_raw),
                "retained_files": {name: EXPECTED["retained_files"][name]["sha256"] for name in RETAINED},
            }}
        return binding

    def write_binding(self) -> None:
        self.binding_path.write_bytes(canonical(self.binding))

    def change_inventory(self, host: str, update) -> None:
        path = self.plugins[host] / "assembly-inventory.json"
        value = json.loads(path.read_bytes())
        update(value)
        raw = canonical(value)
        path.write_bytes(raw)
        self.binding["hosts"][host]["expected"]["inventory_sha256"] = sha(raw)
        self.write_binding()

    def call(self, provider="plugin", *, apply=False, digest=None, root=None, binding=True) -> dict:
        selected = root or self.root
        args = {"provider": provider, "binding_input": self.binding_path if provider == "plugin" and binding else None}
        if apply:
            args["expected_plan_sha256"] = digest
        before = snapshot(self.base)
        event = {"operation": "apply_skill_ownership" if apply else "plan_skill_ownership",
                 "arguments": {"target": str(selected), **{k: str(v) if isinstance(v, Path) else v for k, v in args.items()}},
                 "before": before, "lock_before_base64": base64.b64encode((selected / LOCK).read_bytes()).decode()}
        try:
            result = (ownership.apply_skill_ownership if apply else ownership.plan_skill_ownership)(selected, **args)
            event["result"] = result
            event["exit_status"] = 0 if result.get("passed") else 1
            return result
        except (IntegrityError, installer.HarnessError) as exc:
            event["result"] = {"passed": False, "exception": type(exc).__name__, "message": str(exc)}
            event["exit_status"] = 1
            return event["result"]
        finally:
            event["after"] = snapshot(self.base)
            event["changed_destinations"] = sorted(k for k in set(before) | set(event["after"])
                                                     if before.get(k) != event["after"].get(k))
            event["lock_after_base64"] = base64.b64encode((selected / LOCK).read_bytes()).decode()
            self.events.append(event)

    def migrate(self) -> dict:
        plan = self.call()
        self.assertTrue(plan["passed"], plan)
        result = self.call(apply=True, digest=plan["plan_sha256"])
        self.assertTrue(result["passed"], result)
        return result

    def refuse_unchanged(self, **kwargs) -> dict:
        before = snapshot(self.base)
        result = self.call(**kwargs)
        self.assertFalse(result["passed"], result)
        self.assertEqual(before, snapshot(self.base))
        return result

    def test_own01_exact_catalog_and_each_selected_host(self) -> None:
        for hosts in (("codex",), ("claude",), ("codex", "claude")):
            with self.subTest(hosts=hosts):
                self.binding["hosts"] = {host: {"root": str(self.plugins[host]), "expected": {
                    "plugin": "verity-plane", "version": "1.0.0",
                    "inventory_sha256": sha((self.plugins[host] / "assembly-inventory.json").read_bytes()),
                    "retained_files": {p: EXPECTED["retained_files"][p]["sha256"] for p in RETAINED},
                }} for host in hosts}
                self.write_binding()
                before = snapshot(self.root)
                external = snapshot(self.base / "external")
                plan = self.call()
                self.assertTrue(plan["passed"], plan)
                self.assertEqual(before, snapshot(self.root))
                removed = sorted(item["path"] for item in plan["changes"] if item["action"] == "remove")
                self.assertEqual(list(CATALOG), removed)
                result = self.call(apply=True, digest=plan["plan_sha256"])
                self.assertTrue(result["passed"], result)
                lock = json.loads((self.root / LOCK).read_bytes())
                self.assertEqual(4, lock["schema"])
                self.assertEqual({p: sha(canonical_text(raw)) for p, raw in self.catalog_bytes.items()},
                                 lock["skill_ownership"]["catalog"])
                self.assertEqual(set(hosts), set(lock["skill_ownership"]["hosts"]))
                self.assertEqual(self.identity.to_lock(), lock["evaluator"])
                for name in CATALOG:
                    self.assertFalse((self.root / name).exists())
                    self.assertNotIn(name, lock["files"])
                for name, value in before.items():
                    if value["kind"] == "file" and name not in CATALOG and name != LOCK:
                        self.assertEqual(value, snapshot(self.root)[name])
                self.assertEqual(external, snapshot(self.base / "external"))
                self.assertEqual("unobserved", result["availability"])
                self.assertEqual("unobserved", result["native_discovery"])
                restoration = self.call("repository")
                self.assertTrue(restoration["passed"], restoration)
                self.assertTrue(self.call("repository", apply=True, digest=restoration["plan_sha256"])["passed"])

    def test_own01_cli_plan_apply_stale_refusal_and_restore_json(self) -> None:
        spec = importlib.util.spec_from_file_location("ownership_cli_test_support", ROOT / "tests" / "cli_support.py")
        support = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(support)
        def invoke(provider="plugin", *extra):
            args = ["skill-ownership", str(self.root), "--provider", provider, "--json"]
            if provider == "plugin":
                args += ["--binding-input", str(self.binding_path)]
            args += list(extra)
            before = snapshot(self.base)
            code, stdout, stderr = support.invoke(*args)
            result = json.loads(stdout)
            self.events.append({"operation": "cli", "arguments": args, "exit_status": code,
                                "stdout": stdout, "stderr": stderr,
                                "result": result, "before": before, "after": snapshot(self.base)})
            return code, result
        before = snapshot(self.root)
        code, plan = invoke()
        self.assertEqual(0, code, plan)
        self.assertEqual(before, snapshot(self.root))
        self.assertEqual(list(CATALOG), sorted(item["path"] for item in plan["changes"] if item["action"] == "remove"))
        code, result = invoke("plugin", "--apply", "--expected-plan-sha256", "0" * 64)
        self.assertNotEqual(0, code)
        self.assertFalse(result["passed"])
        self.assertEqual(before, snapshot(self.root))
        code, applied = invoke("plugin", "--apply", "--expected-plan-sha256", plan["plan_sha256"])
        self.assertEqual(0, code, applied)
        self.assertTrue(applied["passed"])
        for name in CATALOG:
            self.assertFalse((self.root / name).exists())
        code, plan = invoke("repository")
        self.assertEqual(0, code, plan)
        code, restored = invoke("repository", "--apply", "--expected-plan-sha256", plan["plan_sha256"])
        self.assertEqual(0, code, restored)
        for name, raw in self.catalog_bytes.items():
            self.assertEqual(raw, (self.root / name).read_bytes())

    def test_own02_preserves_owner_content_and_directories(self) -> None:
        entries = {
            ".agents/skills/owner-skill/SKILL.md": b"owner skill\n",
            ".agents/skills/harness-orient/owner-note.txt": b"owner note beside managed core\n",
            ".claude/owner.txt": b"owner provider content\n",
        }
        for name, raw in entries.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        empty = self.root / ".agents/skills/harness-orient/owner-empty"
        empty.mkdir()
        agents = self.root / "AGENTS.md"
        agents.write_bytes(b"Owner preamble\n" + agents.read_bytes() + b"Owner suffix\n")
        fragment = agents.read_bytes()
        self.migrate()
        for name, raw in entries.items():
            self.assertEqual(raw, (self.root / name).read_bytes())
        self.assertTrue(empty.is_dir())
        self.assertEqual(fragment, agents.read_bytes())

    def test_own03_modified_missing_and_unowned_catalog_refuse(self) -> None:
        path = self.root / CATALOG[0]
        original = path.read_bytes()
        for effect in ("modified", "missing", "unowned"):
            with self.subTest(effect=effect):
                if effect == "modified":
                    path.write_bytes(original + b"local customization\n")
                elif effect == "missing":
                    path.unlink()
                else:
                    lock = json.loads(self.original_lock)
                    del lock["files"][CATALOG[0]]
                    (self.root / LOCK).write_bytes(canonical(lock))
                self.refuse_unchanged()
                path.write_bytes(original)
                (self.root / LOCK).write_bytes(self.original_lock)

    def test_own03_hard_link_refusal(self) -> None:
        sources = (self.root / CATALOG[0], self.root / LOCK, self.binding_path,
                   self.plugins["codex"] / "assembly-inventory.json",
                   self.plugins["codex"] / ".codex-plugin/plugin.json", self.plugins["codex"] / RETAINED[0])
        for index, selected in enumerate(sources):
            with self.subTest(selected=str(selected.relative_to(self.base))):
                linked = self.base / f"owner-linked-copy-{index}"
                try:
                    os.link(selected, linked)
                except OSError as exc:
                    self.skipTest(f"hard-link mechanism unavailable: {exc}")
                try:
                    self.assertGreater(selected.stat().st_nlink, 1)
                    self.refuse_unchanged()
                finally:
                    linked.unlink()

    def test_own03_symbolic_link_refusal(self) -> None:
        sources = (self.root / CATALOG[0], self.root / LOCK, self.binding_path,
                   self.plugins["codex"] / "assembly-inventory.json",
                   self.plugins["codex"] / ".codex-plugin/plugin.json", self.plugins["codex"] / RETAINED[0])
        for index, selected in enumerate(sources):
            with self.subTest(selected=str(selected.relative_to(self.base))):
                original = selected.read_bytes()
                destination = self.base / f"outside-owned-file-{index}"
                destination.write_bytes(original)
                selected.unlink()
                try:
                    selected.symlink_to(destination)
                except OSError as exc:
                    selected.write_bytes(original)
                    self.skipTest(f"symbolic-link mechanism unavailable: {exc}")
                try:
                    self.refuse_unchanged()
                finally:
                    selected.unlink()
                    selected.write_bytes(original)

    def test_own03_repository_case_spelling_collision_refuses(self) -> None:
        selected = self.root / CATALOG[0]
        changed = selected.with_name(selected.name.swapcase())
        selected.rename(changed)
        self.refuse_unchanged()

    def test_own03_explicit_hosts_roots_and_closed_expected_fields(self) -> None:
        original = copy.deepcopy(self.binding)
        for variant in ("empty-hosts", "unknown-host", "relative-root", "missing-root", "extra-expected"):
            with self.subTest(variant=variant):
                self.binding = copy.deepcopy(original)
                if variant == "empty-hosts":
                    self.binding["hosts"] = {}
                elif variant == "unknown-host":
                    self.binding["hosts"]["unqualified-host"] = self.binding["hosts"].pop("codex")
                elif variant == "relative-root":
                    self.binding["hosts"]["codex"]["root"] = "relative-plugin"
                elif variant == "missing-root":
                    del self.binding["hosts"]["codex"]["root"]
                else:
                    self.binding["hosts"]["codex"]["expected"]["native_activation"] = True
                self.write_binding()
                self.refuse_unchanged()

    @unittest.skipUnless(os.name == "nt", "Windows junction fixture unavailable on this platform")
    def test_own03_windows_reparse_junction_refusal(self) -> None:
        for index, selected in enumerate((self.root / ".agents/skills/harness-orient", self.plugins["codex"], self.root)):
            with self.subTest(selected=str(selected.relative_to(self.base))):
                destination = self.base / f"junction-owner-source-{index}"
                selected.rename(destination)
                command = ["cmd", "/d", "/c", "mklink", "/J", str(selected), str(destination)]
                run = subprocess.run(command, capture_output=True, text=True, timeout=30)
                if run.returncode:
                    destination.rename(selected)
                    self.skipTest("junction creation unavailable: " + run.stderr)
                try:
                    self.assertTrue(selected.lstat().st_file_attributes & 1024)
                    self.refuse_unchanged()
                finally:
                    if selected.lstat().st_file_attributes & 1024:
                        selected.rmdir()
                    destination.rename(selected)

    def test_own03_closed_binding_duplicate_keys_and_control_limit(self) -> None:
        original = self.binding_path.read_bytes()
        invalid = [b'{"schema":"se-harness-skill-ownership-binding-v1","hosts":{},"hosts":{}}',
                   canonical({**self.binding, "schema": "unknown"}),
                   canonical({**self.binding, "extra": True}), b" " * (1048576 + 1)]
        for raw in invalid:
            with self.subTest(size=len(raw), prefix=raw[:40]):
                self.binding_path.write_bytes(raw)
                self.refuse_unchanged()
        self.binding_path.write_bytes(original)

    def test_own03_assembly_unknown_schema_and_duplicate_keys_refuse(self) -> None:
        path = self.plugins["codex"] / "assembly-inventory.json"
        original = path.read_bytes()
        unknown = json.loads(original)
        unknown["schema"] = "unknown-assembly"
        for raw in (canonical(unknown), original.replace(b'"host":', b'"host":"codex","host":', 1)):
            with self.subTest(input_sha256=sha(raw)):
                path.write_bytes(raw)
                self.binding["hosts"]["codex"]["expected"]["inventory_sha256"] = sha(raw)
                self.write_binding()
                self.refuse_unchanged()

    def test_own03_wrong_typed_assembly_values_are_bounded_refusals(self) -> None:
        path = self.plugins["codex"] / "assembly-inventory.json"
        original = path.read_bytes()
        for field, invalid in (("origin", []), ("mode", []), ("bytes", True), ("sha256", [])):
            with self.subTest(field=field, invalid=invalid):
                path.write_bytes(original)
                self.change_inventory("codex", lambda value: value["files"][RETAINED[0]].update({field: invalid}))
                self.refuse_unchanged()

    def test_own03_unsafe_inventory_paths_and_case_collisions(self) -> None:
        inventory_path = self.plugins["codex"] / "assembly-inventory.json"
        original = inventory_path.read_bytes()
        for name in ("../escape", "/absolute", "C:/escape", "skills\\escape", "skills/CON.txt", "skills/name.",
                     "skills/HARNESS-ORIENT/SKILL.md"):
            with self.subTest(path=name):
                inventory_path.write_bytes(original)
                self.change_inventory("codex", lambda value: value["files"].update({name: {
                    "sha256": "a" * 64, "bytes": 1, "mode": 0o644, "origin": "shared"}}))
                self.refuse_unchanged()

    def test_own03_external_hard_link_and_unlisted_file_refuse(self) -> None:
        selected = self.plugins["codex"] / RETAINED[0]
        extra = self.base / "external-hardlink"
        try:
            os.link(selected, extra)
        except OSError as exc:
            self.skipTest(f"external hard-link mechanism unavailable: {exc}")
        self.refuse_unchanged()
        extra.unlink()
        extra = self.plugins["codex"] / "unlisted.txt"
        extra.write_bytes(b"unlisted payload\n")
        self.refuse_unchanged()

    def test_own03_inventory_count_and_declared_size_limits(self) -> None:
        path = self.plugins["codex"] / "assembly-inventory.json"
        original = path.read_bytes()
        cases = ("count", "file-size")
        for case in cases:
            with self.subTest(limit=case):
                path.write_bytes(original)
                def update(value):
                    if case == "count":
                        value["files"].update({f"assets/{i}.txt": {"sha256": "a" * 64, "bytes": 1,
                                                                   "mode": 0o644, "origin": "shared"}
                                               for i in range(2001)})
                    elif case == "file-size":
                        value["files"][RETAINED[0]]["bytes"] = 16777217
                self.change_inventory("codex", update)
                result = self.refuse_unchanged()
                self.assertIn("bound", json.dumps(result), result)

    def test_own03_actual_aggregate_payload_limit(self) -> None:
        raw = b"x" * 16777216
        entries = {}
        for index in range(9):
            name = f"assets/payload-{index}.txt"
            path = self.plugins["codex"] / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            entries[name] = {"sha256": sha(raw), "bytes": len(raw), "mode": 0o644, "origin": "shared"}
        self.change_inventory("codex", lambda value: value["files"].update(entries))
        result = self.refuse_unchanged()
        self.assertIn("aggregate", json.dumps(result), result)

    def test_own03_actual_external_file_size_limit(self) -> None:
        selected = self.plugins["codex"] / RETAINED[0]
        with selected.open("wb") as stream:
            stream.truncate(16777217)
        result = self.refuse_unchanged()
        self.assertIn("size bound", json.dumps(result), result)

    def test_own04_stale_equal_size_file_lock_binding_and_inventory(self) -> None:
        for changed in ("selected", "lock", "binding", "inventory", "plugin-file", "root", "hosts"):
            with self.subTest(changed=changed):
                before = {path: path.read_bytes() for path in (
                    self.root / CATALOG[0], self.root / LOCK, self.binding_path,
                    self.plugins["codex"] / "assembly-inventory.json", self.plugins["codex"] / RETAINED[0])}
                plan = self.call()
                self.assertTrue(plan["passed"], plan)
                if changed == "selected":
                    path = self.root / CATALOG[0]
                    raw = path.read_bytes()
                    path.write_bytes((b"X" if raw[:1] != b"X" else b"Y") + raw[1:])
                elif changed == "lock":
                    (self.root / LOCK).write_bytes(self.original_lock + b" ")
                elif changed == "binding":
                    self.binding_path.write_bytes(self.binding_path.read_bytes() + b" ")
                elif changed == "inventory":
                    path = self.plugins["codex"] / "assembly-inventory.json"
                    path.write_bytes(path.read_bytes() + b" ")
                elif changed == "plugin-file":
                    path = self.plugins["codex"] / RETAINED[0]
                    path.write_bytes(path.read_bytes() + b" ")
                else:
                    value = copy.deepcopy(self.binding)
                    if changed == "root":
                        other = self.base / "same-package-different-root"
                        shutil.copytree(self.plugins["codex"], other)
                        value["hosts"]["codex"]["root"] = str(other)
                    else:
                        del value["hosts"]["claude"]
                    self.binding_path.write_bytes(canonical(value))
                self.refuse_unchanged(apply=True, digest=plan["plan_sha256"])
                for path, raw in before.items():
                    path.write_bytes(raw)

    def test_own05_replay_doctor_and_direct_installer_preserve_binding(self) -> None:
        self.migrate()
        before = snapshot(self.root)
        original_lock = (self.root / LOCK).read_bytes()
        for _ in range(2):
            result = self.migrate()
            self.assertEqual("unchanged", result["outcome"])
            self.assertEqual(before, snapshot(self.root))
            self.assertEqual(original_lock, (self.root / LOCK).read_bytes())
        checks = inspect_installation(self.root)
        self.events.append({"operation": "inspect_installation", "checks": [vars(item) for item in checks]})
        self.assertTrue(all(item.passed for item in checks), checks)
        for mode in ("init", "upgrade"):
            changes, old = installer.plan_install(self.root, project_name=None, mode=mode)
            self.assertTrue(all(item.path not in CATALOG for item in changes))
            installer.apply_changes(self.root, changes, old, allow_updates=mode == "upgrade")
            self.assertEqual(original_lock, (self.root / LOCK).read_bytes())
            self.assertEqual(before, snapshot(self.root))

    def test_own05_handcrafted_direct_installer_path_aliases_cannot_recreate_retired_core(self) -> None:
        self.migrate()
        selected = CATALOG[0]
        directory, filename = selected.rsplit("/", 1)
        aliases = (selected, directory + "/./" + filename, selected.replace("/", "\\"),
                   selected.upper(), selected + ".", selected + ":stream",
                   ".claude/skills/harness-operator-brief/SKILL.md",
                   ".CLAUDE/SKILLS/HARNESS-OPERATOR-BRIEF/SKILL.MD")
        for alias in aliases:
            with self.subTest(path=alias):
                changes, old = installer.plan_install(self.root, project_name=None, mode="init")
                changes.append(installer.Change(alias, "add", "managed", self.catalog_bytes[selected], None))
                before = snapshot(self.root)
                error = None
                try:
                    installer.apply_changes(self.root, changes, old, allow_updates=False)
                except (installer.HarnessError, IntegrityError) as exc:
                    error = str(exc)
                self.events.append({"operation": "handcrafted-direct-installer-input", "path": alias,
                                    "error": error, "before": before, "after": snapshot(self.root)})
                self.assertIsNotNone(error, "unreviewed direct API input recreated a retired core")
                self.assertEqual(before, snapshot(self.root))

    @unittest.skipUnless(os.name == "nt", "Windows junction alias fixture unavailable on this platform")
    def test_own05_direct_installer_junction_alias_cannot_recreate_retired_core(self) -> None:
        self.migrate()
        selected = CATALOG[0]
        parent, filename = selected.rsplit("/", 1)
        alias = self.root / "owner-junction-alias"
        target = self.root / parent
        target.mkdir(parents=True, exist_ok=True)
        run = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(alias), str(target)],
                             capture_output=True, text=True, timeout=30)
        if run.returncode:
            self.skipTest("junction creation unavailable: " + run.stderr)
        try:
            self.assertTrue(alias.lstat().st_file_attributes & 1024)
            changes, old = installer.plan_install(self.root, project_name=None, mode="init")
            relative = alias.relative_to(self.root).as_posix() + "/" + filename
            changes.append(installer.Change(relative, "add", "managed", self.catalog_bytes[selected], None))
            before = snapshot(self.root)
            error = None
            try:
                installer.apply_changes(self.root, changes, old, allow_updates=False)
            except (installer.HarnessError, IntegrityError) as exc:
                error = str(exc)
            self.events.append({"operation": "direct-installer-junction-alias", "path": relative,
                                "error": error, "before": before, "after": snapshot(self.root)})
            self.assertIsNotNone(error)
            self.assertEqual(before, snapshot(self.root))
        finally:
            if alias.lstat().st_file_attributes & 1024:
                alias.rmdir()

    def test_own06_invalid_ownership_format_upgrade_is_atomic(self) -> None:
        self.migrate()
        lock = json.loads((self.root / LOCK).read_bytes())
        lock["skill_ownership"]["schema"] = "unknown-future-ownership"
        (self.root / LOCK).write_bytes(canonical(lock))
        before = snapshot(self.root)
        with self.assertRaises((installer.HarnessError, ownership.OwnershipError, ValueError)):
            changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade")
            installer.apply_changes(self.root, changes, old, allow_updates=True)
        self.assertEqual(before, snapshot(self.root))

    def test_own06_synthetic_compatible_prior_version_upgrades_preserving_binding(self) -> None:
        self.migrate()
        lock = json.loads((self.root / LOCK).read_bytes())
        prior_archive = b"independent synthetic prior evaluator archive; not a release\n"
        prior = {"version": "0.18.0.dev0", "payload_manifest": "se-harness-installed-payload-v1",
                 "payload_sha256": "b" * 64, "archive_name": "se_harness-0.18.0.dev0-py3-none-any.whl",
                 "archive_sha256": sha(prior_archive)}
        target_identity, target_archive = self.identity, self.wheel_bytes
        try:
            self.identity = InstalledEvaluatorIdentity(**prior)
            self.wheel_bytes = prior_archive
            prior_input = self.make_binding(("codex", "claude"), external_name="synthetic-prior-external")
        finally:
            self.identity, self.wheel_bytes = target_identity, target_archive
        binding = {"schema": "se-harness-skill-ownership-v1", "provider": "plugin",
                   "catalog": {name: sha(canonical_text(raw)) for name, raw in self.catalog_bytes.items()},
                   "hosts": {host: value["expected"] for host, value in prior_input["hosts"].items()}}
        binding["binding_sha256"] = sha(canonical(binding))
        lock["skill_ownership"] = binding
        config = self.root / ".engineering-harness.toml"
        raw = config.read_bytes().replace(self.identity.version.encode(), prior["version"].encode())
        self.assertNotEqual(config.read_bytes(), raw)
        config.write_bytes(raw)
        lock["tool_version"] = prior["version"]
        lock["evaluator"] = prior
        lock["files"][".engineering-harness.toml"]["sha256"] = sha(canonical_text(raw))
        (self.root / LOCK).write_bytes(canonical(lock))
        before = snapshot(self.root)
        changes, old = installer.plan_install(self.root, project_name=None, mode="upgrade")
        self.assertTrue(all(item.path not in CATALOG for item in changes))
        with contextlib.ExitStack() as stack:
            if not PACKAGE:
                def source_upgrade_authority(root, **kwargs):
                    self.assertTrue(kwargs.get("allow_upgrade_transition"))
                    authority = trusted_source_authority(root)
                    authority.target_identity = self.identity
                    authority.transition = True
                    return authority
                stack.enter_context(mock.patch("se_harness.mutation_guard.require_mutation_authority",
                                                side_effect=source_upgrade_authority))
            installed = installer.apply_changes(self.root, changes, old, allow_updates=True)
        self.events.append({"operation": "synthetic-prior-version-compatible-upgrade", "prior_identity": prior,
                            "prior_identity_kind": "independent-synthetic-fixture-not-a-release",
                            "prior_external_assembly_input": prior_input,
                            "prior_external_snapshot": snapshot(self.base / "synthetic-prior-external"),
                            "target_identity": self.identity.to_lock(), "before": before,
                            "after": snapshot(self.root), "observed_lock": installed})
        self.assertEqual(binding, installed["skill_ownership"])
        self.assertEqual(self.identity.to_lock(), installed["evaluator"])
        self.assertEqual(self.identity.version, installed["tool_version"])
        for name in CATALOG:
            self.assertFalse((self.root / name).exists())
        self.assertTrue(all(item.passed for item in inspect_installation(self.root)))

    def test_own07_unsupported_old_lock_refuses_before_writes(self) -> None:
        for schema in (1, 2, 5):
            with self.subTest(schema=schema):
                value = json.loads(self.original_lock)
                value["schema"] = schema
                (self.root / LOCK).write_bytes(canonical(value))
                self.refuse_unchanged()

    def _candidate_report_command(self, arguments):
        before = snapshot(self.base)
        if PACKAGE:
            argv = [sys.executable, "-I", "-B", "-m", "se_harness", *map(str, arguments)]
            process = subprocess.run(argv, cwd=self.base, capture_output=True, text=True, timeout=120)
            code, stdout, stderr = process.returncode, process.stdout, process.stderr
        else:
            spec = importlib.util.spec_from_file_location("ownership_report_cli_support", ROOT / "tests/cli_support.py")
            support = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(support)
            argv = list(map(str, arguments))
            code, stdout, stderr = support.invoke(*argv)
        after = snapshot(self.base)
        self.events.append({"operation": "candidate-report-output", "arguments": argv,
                            "exit_status": code, "stdout": stdout, "stderr": stderr,
                            "before": before, "after": after})
        self.assertEqual(before, after)
        return code, stdout, stderr

    def test_own07_candidate_qualification_output_preserves_retired_skill(self) -> None:
        (self.root / ".agents/skills/harness-orient/owner-note.txt").write_bytes(b"Keep this owner directory.\n")
        self.migrate()
        target = self.root / ".agents/skills/harness-orient/SKILL.md"
        lock = self.root / LOCK
        original = lock.read_bytes()
        try:
            for schema in (4, 99):
                with self.subTest(schema=schema):
                    if schema == 99:
                        invalid = json.loads(original)
                        invalid["schema"] = 99
                        lock.write_bytes(canonical(invalid))
                    self.assertFalse(target.exists())
                    code, stdout, stderr = self._candidate_report_command(
                        ["qualify", "released-root", self.root, "--output", target, "--json"])
                    self.assertEqual(1, code, stderr)
                    self.assertEqual("RQ002", json.loads(stdout)["checks"][0]["id"])
                    self.assertFalse(target.exists())
        finally:
            lock.write_bytes(original)

    def test_own07_candidate_dashboard_output_preserves_installed_workflow(self) -> None:
        self.migrate()
        for destination in (".github", ".github/workflows", ".agents/skills/harness-orient"):
            with self.subTest(output=destination):
                code, stdout, stderr = self._candidate_report_command(
                    ["dashboard", self.root, "--output", destination, "--json"])
                self.assertEqual(2, code, stdout + stderr)
                self.assertIn("protected", stderr)

    def test_own07_released_017_cli_format_and_command_refusals(self) -> None:
        legacy = os.environ.get("SE_HARNESS_OWNERSHIP_LEGACY_PYTHON")
        if not legacy:
            self.skipTest("actual released 0.17.0 interpreter not supplied; old-reader observation unavailable")
        version_command = [legacy, "-I", "-B", "-m", "se_harness", "--version"]
        version = subprocess.run(version_command, cwd=self.base, capture_output=True, text=True, timeout=60)
        self.events.append({"operation": "released-0.17-version", "arguments": version_command,
                            "exit_status": version.returncode, "stdout": version.stdout, "stderr": version.stderr})
        self.assertEqual(0, version.returncode)
        self.assertRegex(version.stdout.strip(), r"(?:^|\s)0\.17\.0$")
        self.migrate()
        for args in (("doctor",), ("init",), ("upgrade", "--apply"),
                     ("skill-ownership", "--provider", "repository", "--apply")):
            with self.subTest(command=args):
                before = snapshot(self.root)
                command = [legacy, "-I", "-B", "-m", "se_harness", args[0], str(self.root), *args[1:]]
                run = subprocess.run(command, cwd=self.base, capture_output=True, text=True, timeout=60)
                self.events.append({"operation": "released-0.17-reader", "arguments": command,
                                    "exit_status": run.returncode, "stdout": run.stdout, "stderr": run.stderr,
                                    "before": before, "after": snapshot(self.root)})
                self.assertNotEqual(0, run.returncode)
                self.assertEqual(before, snapshot(self.root))
                diagnostic = (run.stdout + run.stderr).lower()
                if args[0] == "skill-ownership":
                    self.assertIn("invalid choice: 'skill-ownership'", diagnostic)
                else:
                    self.assertIn("unsupported lock schema", diagnostic)
                    self.assertNotIn("unrecognized arguments", diagnostic)

    def test_own08_reintroduced_copy_and_deleted_or_tampered_binding_fail_integrity(self) -> None:
        self.migrate()
        lock_raw = (self.root / LOCK).read_bytes()
        for effect in ("reintroduced", "deleted-record", "catalog-digest", "inventory-digest",
                       "inventory-valid-digest", "retained-valid-digest"):
            with self.subTest(effect=effect):
                lock = json.loads(lock_raw)
                if effect == "reintroduced":
                    destination = self.root / CATALOG[0]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(self.catalog_bytes[CATALOG[0]])
                elif effect == "deleted-record":
                    del lock["skill_ownership"]
                elif effect == "catalog-digest":
                    lock["skill_ownership"]["catalog"][CATALOG[0]] = "0" * 64
                elif effect == "inventory-digest":
                    lock["skill_ownership"]["hosts"]["codex"]["inventory_sha256"] = "invalid"
                elif effect == "inventory-valid-digest":
                    lock["skill_ownership"]["hosts"]["codex"]["inventory_sha256"] = "0" * 64
                else:
                    lock["skill_ownership"]["hosts"]["codex"]["retained_files"][RETAINED[0]] = "0" * 64
                (self.root / LOCK).write_bytes(canonical(lock))
                checks = inspect_installation(self.root)
                self.assertFalse(all(item.passed for item in checks), checks)
                self.refuse_unchanged(provider="repository")
                if effect == "reintroduced":
                    destination.unlink()
                (self.root / LOCK).write_bytes(lock_raw)

    def test_own08_current_lock_evaluator_evidence_matches_schema4_identity(self) -> None:
        from se_harness.engine.validation_core import Artifact
        from se_harness.engine.validation_evidence import _validate_evaluator_evidence_binding
        self.migrate()
        relative = "docs/engineering/acceptance/evidence/evaluator.json"
        destination = self.root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        selected = json.loads(trusted_source_authority(self.root).evidence_bytes)
        for mismatch in (False, True):
            with self.subTest(mismatch=mismatch):
                value = copy.deepcopy(selected)
                if mismatch:
                    value["evaluator"]["payload_sha256"] = "f" * 64
                raw = canonical(value)
                destination.write_bytes(raw)
                artifact = Artifact(self.root / "docs/engineering/acceptance/verification-records/VREC-TST-001.md",
                                    {"id": "VREC-TST-001", "type": "verification_record", "status": "ready",
                                     "evaluator_evidence_path": relative, "evaluator_evidence_sha256": sha(raw)}, "")
                errors = []
                _validate_evaluator_evidence_binding(artifact, errors, self.root, required=True,
                                                     require_archive=True, match_current_lock=True)
                self.events.append({"operation": "current-lock-evaluator-evidence", "mismatch": mismatch,
                                    "input_sha256": sha(raw), "errors": [vars(item) for item in errors]})
                if mismatch:
                    self.assertTrue(errors)
                    self.assertTrue(any("differs" in item.message for item in errors), errors)
                else:
                    self.assertEqual([], errors)

    def test_own11_restore_exact_distribution_and_refuse_owner_conflicts(self) -> None:
        self.migrate()
        path = self.root / CATALOG[0]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"intervening owner content\n")
        self.refuse_unchanged(provider="repository")
        path.unlink()
        plan = self.call("repository")
        self.assertTrue(plan["passed"], plan)
        result = self.call("repository", apply=True, digest=plan["plan_sha256"])
        self.assertTrue(result["passed"], result)
        lock = json.loads((self.root / LOCK).read_bytes())
        self.assertEqual(3, lock["schema"])
        self.assertNotIn("skill_ownership", lock)
        for name, raw in self.catalog_bytes.items():
            self.assertEqual(raw, (self.root / name).read_bytes())

    def test_own09_exception_at_each_write_and_durable_boundary_rolls_back(self) -> None:
        schedule = [(stage, path) for path in (*CATALOG, LOCK)
                    for stage in ("before-write", "after-write", "journal-updated")]
        schedule += [(stage, None) for stage in ("journal-prepared", "stages-prepared", "before-postcondition",
                                                "after-postcondition", "before-journal-cleanup")]
        for provider in ("plugin", "repository"):
            if provider == "repository":
                self.migrate()
                self.prune_empty_fixture_catalog_directories()
            for stage, path in schedule + self.preparation_fault_schedule(provider):
                with self.subTest(provider=provider, stage=stage, path=path):
                    plan = self.call(provider)
                    self.assertTrue(plan["passed"], plan)
                    before = snapshot(self.root)
                    triggered = []
                    def fail_once(actual_stage, actual_path=None):
                        if (actual_stage, actual_path) == (stage, path) and not triggered:
                            triggered.append(True)
                            raise OSError("independent injected write-boundary failure")
                    with mock.patch.object(ownership, "_fault_hook", side_effect=fail_once):
                        result = self.call(provider, apply=True, digest=plan["plan_sha256"])
                    self.assertTrue(triggered, f"fault boundary not exercised: {stage} {path}")
                    self.assertFalse(result["passed"], result)
                    self.assertEqual("rolled-back", result["outcome"], result)
                    self.assertEqual(before, snapshot(self.root))
                    self.events[-1]["fault_schedule"] = {"stage": stage, "path": path, "triggered": True}

    @staticmethod
    def preparation_fault_schedule(provider: str) -> list[tuple[str, str]]:
        label = "before_stage" if provider == "plugin" else "after_stage"
        schedule = [("stage-journal-updated", path + ":" + label) for path in CATALOG]
        schedule += [("stage-journal-updated", LOCK + ":" + label) for label in ("before_stage", "after_stage")]
        if provider == "repository":
            parents = {parent.as_posix() for name in CATALOG for parent in Path(name).parents if parent.as_posix() != "."}
            schedule += [("directory-journal-updated", name) for name in sorted(parents)]
        return schedule

    def prune_empty_fixture_catalog_directories(self) -> None:
        directories = {self.root / parent for name in CATALOG for parent in Path(name).parents
                       if parent.as_posix() != "."}
        for directory in sorted(directories, key=lambda value: len(value.parts), reverse=True):
            self.assertTrue(directory.resolve().is_relative_to(self.root.resolve()))
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()

    def worker(self, plan: dict, *, stage=None, path=None, provider="plugin", binding_path=None):
        marker = self.base / ("worker-marker-" + uuid.uuid4().hex + ".json")
        release = self.base / ("worker-release-" + uuid.uuid4().hex)
        command = [sys.executable, "-I", "-B", str(FIXTURES / "transaction_worker.py"),
                   "--test-module", str(Path(__file__).resolve()), "--target", str(self.root),
                   "--provider", provider, "--digest", plan["plan_sha256"],
                   "--identity", json.dumps(vars(self.identity)), "--pause-seconds", "40"]
        if not PACKAGE:
            command += ["--source-root", str(ROOT)]
        if provider == "plugin":
            command += ["--binding", str(binding_path or self.binding_path)]
        if stage:
            command += ["--fault-stage", stage, "--marker", str(marker), "--release", str(release)]
        if path is not None:
            command += ["--fault-path", path]
        process = subprocess.Popen(command, cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        def cleanup():
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=10)
        self.addCleanup(cleanup)
        return process, marker, release, command

    def wait_marker(self, process, marker: Path) -> None:
        deadline = time.monotonic() + 30
        while not marker.is_file() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.02)
        if not marker.is_file():
            if process.poll() is None:
                process.kill()
            stdout, stderr = process.communicate(timeout=10)
            self.fail(f"durable crash boundary not reached: status={process.returncode}; {stdout}; {stderr}")
        # Its atomic publication is the handshake. Read the payload only after
        # the child closes its handles; Windows may defer sharing after rename.

    def crash_at(self, stage: str, path=None, *, provider="plugin") -> None:
        plan = self.call(provider)
        self.assertTrue(plan["passed"], plan)
        before = snapshot(self.root)
        process, marker, release, command = self.worker(plan, stage=stage, path=path, provider=provider)
        self.wait_marker(process, marker)
        process.kill()
        stdout, stderr = process.communicate(timeout=10)
        reached = json.loads(marker.read_bytes())
        self.assertNotEqual(0, process.returncode)
        self.assertTrue((self.root / PENDING).is_file(), "a killed durable transaction must retain recovery metadata")
        self.events.append({"operation": "killed-independent-process", "arguments": command,
                            "fault_schedule": reached, "exit_status": process.returncode,
                            "stdout": stdout, "stderr": stderr, "before": before,
                            "after": snapshot(self.root),
                            "recovery_bytes_base64": base64.b64encode((self.root / PENDING).read_bytes()).decode()})

    def recover(self, provider="plugin") -> dict:
        plan = self.call(provider)
        self.assertTrue(plan["passed"], plan)
        self.assertNotEqual("none", plan["recovery"]["status"])
        result = self.call(provider, apply=True, digest=plan["plan_sha256"])
        self.assertTrue(result["passed"], result)
        self.assertFalse((self.root / PENDING).exists())
        return result

    def test_own10_killed_process_recovers_each_durable_boundary(self) -> None:
        schedule = [("journal-prepared", None), ("stages-prepared", None)]
        schedule += [(stage, path) for path in (*CATALOG, LOCK) for stage in ("after-write", "journal-updated")]
        schedule += [("after-postcondition", None), ("before-journal-cleanup", None)]
        for provider in ("plugin", "repository"):
            if provider == "repository":
                self.migrate()
                self.prune_empty_fixture_catalog_directories()
            for stage, path in schedule + self.preparation_fault_schedule(provider):
                with self.subTest(provider=provider, stage=stage, path=path):
                    before = snapshot(self.root)
                    self.crash_at(stage, path, provider=provider)
                    checks = inspect_installation(self.root)
                    self.assertFalse(all(item.passed for item in checks), checks)
                    self.recover(provider)
                    self.assertEqual(before, snapshot(self.root))

    def test_own10_durable_commit_and_partial_cleanup_finalize_applied_state(self) -> None:
        for stage in ("committed", "stage-cleaned"):
            for provider in ("plugin", "repository"):
                with self.subTest(provider=provider, stage=stage):
                    self.crash_at(stage, provider=provider)
                    result = self.recover(provider)
                    self.assertEqual("applied", result["outcome"])
                    self.assertEqual("finalized", result["recovery"]["status"])
                    lock = json.loads((self.root / LOCK).read_bytes())
                    self.assertEqual(4 if provider == "plugin" else 3, lock["schema"])
                    for name, raw in self.catalog_bytes.items():
                        if provider == "plugin":
                            self.assertFalse((self.root / name).exists())
                        else:
                            self.assertEqual(raw, (self.root / name).read_bytes())
                    self.assertTrue(all(item.passed for item in inspect_installation(self.root)))

    def test_own10_intervening_owner_edits_and_new_files_are_preserved(self) -> None:
        for effect in ("new-destination", "tracked-edit", "unrelated-new-file"):
            with self.subTest(effect=effect):
                self.crash_at("after-write", CATALOG[0])
                name = CATALOG[0] if effect == "new-destination" else CATALOG[-1] if effect == "tracked-edit" else ".agents/skills/harness-orient/owner-new.txt"
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                raw = b"intervening owner bytes must remain untouched\n"
                path.write_bytes(raw)
                before = snapshot(self.root)
                result = self.call()
                if result["passed"]:
                    result = self.call(apply=True, digest=result["plan_sha256"])
                self.assertFalse(result["passed"], result)
                self.assertEqual(raw, path.read_bytes())
                self.assertEqual(before, snapshot(self.root))
                self.assertTrue((self.root / PENDING).is_file())
                # Remove only the test's known intervention, then finish safe
                # recovery to exercise the next independent variant.
                if effect == "tracked-edit":
                    path.write_bytes(self.catalog_bytes[name])
                else:
                    path.unlink()
                self.recover()

    def test_own10_recovery_write_failure_retains_diagnostics_and_can_retry(self) -> None:
        for stage in ("recovery-before-write", "recovery-after-write"):
            with self.subTest(stage=stage):
                before = snapshot(self.root)
                self.crash_at("after-write", CATALOG[0])
                plan = self.call()
                self.assertTrue(plan["passed"], plan)
                triggered = []
                def failure(actual_stage, path=None):
                    if actual_stage == stage and not triggered:
                        triggered.append(path)
                        raise OSError("independent recovery-write failure")
                with mock.patch.object(ownership, "_fault_hook", side_effect=failure):
                    result = self.call(apply=True, digest=plan["plan_sha256"])
                self.assertTrue(triggered)
                self.assertFalse(result["passed"], result)
                self.assertEqual("required", result["recovery"]["status"])
                self.assertTrue((self.root / PENDING).is_file())
                self.recover()
                self.assertEqual(before, snapshot(self.root))

    def test_own10_byte_identical_owner_replacement_is_not_recovery_authority(self) -> None:
        self.crash_at("after-write", CATALOG[0])
        selected = self.root / CATALOG[-1]
        original = selected.read_bytes()
        held = self.base / "held-original-owned-inode"
        original_inode = selected.stat().st_ino
        selected.rename(held)
        selected.write_bytes(original)
        self.assertNotEqual(original_inode, selected.stat().st_ino)
        before = snapshot(self.root)
        result = self.call()
        if result["passed"]:
            result = self.call(apply=True, digest=result["plan_sha256"])
        self.assertFalse(result["passed"], result)
        self.assertEqual(before, snapshot(self.root))
        self.assertEqual(original, selected.read_bytes())
        self.assertTrue((self.root / PENDING).is_file())
        selected.unlink()
        held.rename(selected)
        self.recover()

    def test_own10_rehashed_journal_cannot_delete_preexisting_owner_empty_directory(self) -> None:
        self.migrate()
        self.prune_empty_fixture_catalog_directories()
        owner = self.root / ".agents"
        owner.mkdir()
        owner_inode = owner.stat().st_ino
        self.crash_at("journal-prepared", provider="repository")
        journal = self.root / PENDING
        original = journal.read_bytes()
        value = json.loads(original)
        self.assertNotIn(".agents", value["payload"]["created_directories"])
        value["payload"]["created_directories"].append(".agents")
        value["sha256"] = sha(canonical(value["payload"]))
        journal.write_bytes(canonical(value))
        before = snapshot(self.root)
        result = self.call("repository")
        if result["passed"]:
            result = self.call("repository", apply=True, digest=result["plan_sha256"])
        self.assertFalse(result["passed"], result)
        self.assertTrue(owner.is_dir())
        self.assertEqual(owner_inode, owner.stat().st_ino)
        self.assertEqual(before, snapshot(self.root))
        self.assertTrue(journal.is_file())
        journal.write_bytes(original)
        self.recover("repository")

    def test_own10_tampered_truncated_and_escaping_recovery_never_write(self) -> None:
        self.crash_at("after-write", CATALOG[0])
        journal = self.root / PENDING
        original = journal.read_bytes()
        outside = self.base / "escape-owner.txt"
        outside.write_bytes(b"outside owner bytes\n")
        mutations = [original[: max(1, len(original) // 2)],
                     canonical({"schema": "se-harness-skill-ownership-recovery-v1", "path": "../escape-owner.txt"}),
                     original.replace(CATALOG[0].encode(), b"../escape-owner.txt"),
                     original.replace(b'"schema":', b'"schema":"unknown","schema":', 1)]
        # The envelope digest is not authentication. Exercise malicious records
        # with a correctly recomputed digest, using an independent JSON encoder.
        for variant in ("corrupt-snapshot", "escaped-entry", "escaped-directory", "incomplete-entries"):
            value = json.loads(original)
            payload = value["payload"]
            if variant == "corrupt-snapshot":
                payload["entries"][CATALOG[0]]["before"] = base64.b64encode(b"forged replacement\n").decode()
            elif variant == "escaped-entry":
                payload["entries"]["../escape-owner.txt"] = payload["entries"].pop(CATALOG[0])
            elif variant == "escaped-directory":
                payload["created_directories"] = ["../outside"]
            else:
                del payload["entries"][CATALOG[0]]
            value["sha256"] = sha(canonical(payload))
            mutations.append(canonical(value))
        for raw in mutations:
            with self.subTest(tampered_sha256=sha(raw)):
                journal.write_bytes(raw)
                before = snapshot(self.base)
                result = self.call()
                if result["passed"]:
                    result = self.call(apply=True, digest=result["plan_sha256"])
                self.assertFalse(result["passed"], result)
                self.assertEqual(before, snapshot(self.base))
                self.assertEqual(raw, journal.read_bytes())
                self.assertEqual(b"outside owner bytes\n", outside.read_bytes())
        journal.write_bytes(original)
        self.recover()

    def test_own13_independent_processes_refuse_contention_and_stale_plan(self) -> None:
        first = self.call()
        self.assertTrue(first["passed"], first)
        other = copy.deepcopy(self.binding)
        del other["hosts"]["claude"]
        other_path = self.base / "other-binding.json"
        other_path.write_bytes(canonical(other))
        second = ownership.plan_skill_ownership(self.root, provider="plugin", binding_input=other_path)
        self.assertTrue(second["passed"], second)
        child, marker, release, command = self.worker(first, stage="journal-prepared")
        self.wait_marker(child, marker)
        contender, _, _, contender_command = self.worker(second, binding_path=other_path)
        stdout, stderr = contender.communicate(timeout=30)
        self.events.append({"operation": "contending-independent-process", "arguments": contender_command,
                            "exit_status": contender.returncode, "stdout": stdout, "stderr": stderr})
        self.assertNotEqual(0, contender.returncode)
        self.assertFalse(json.loads(stdout)["passed"])
        release.write_bytes(b"continue\n")
        stdout, stderr = child.communicate(timeout=30)
        self.events.append({"operation": "exclusive-independent-process", "arguments": command,
                            "exit_status": child.returncode, "stdout": stdout, "stderr": stderr})
        self.assertEqual(0, child.returncode, stdout + stderr)
        before = snapshot(self.root)
        contender, _, _, _ = self.worker(second, binding_path=other_path)
        stdout, stderr = contender.communicate(timeout=30)
        self.assertNotEqual(0, contender.returncode)
        self.assertFalse(json.loads(stdout)["passed"])
        self.assertEqual(before, snapshot(self.root))
        self.assertEqual({"codex", "claude"}, set(json.loads((self.root / LOCK).read_bytes())["skill_ownership"]["hosts"]))

    def test_own12_clone_without_plugin_is_integral_and_availability_unobserved(self) -> None:
        self.migrate()
        clone = self.base / "different-location" / "clone"
        shutil.copytree(self.root, clone)
        for root in self.plugins.values():
            root.rename(root.with_name("unavailable-package"))
        checks = inspect_installation(clone)
        self.assertTrue(all(item.passed for item in checks), checks)
        self.assertEqual((self.root / LOCK).read_bytes(), (clone / LOCK).read_bytes())
        portable = (clone / LOCK).read_text(encoding="utf-8")
        self.assertNotIn(str(self.base), portable)
        result = self.call("repository", root=clone)
        self.assertTrue(result["passed"], result)
        self.assertEqual("unobserved", result["availability"])
        self.assertEqual("unobserved", result["native_discovery"])

    def test_own14_independent_expected_identity_mismatches_refuse(self) -> None:
        original = copy.deepcopy(self.binding)
        for field in ("plugin", "version", "inventory_sha256", "retained_files"):
            with self.subTest(field=field):
                self.binding = copy.deepcopy(original)
                expected = self.binding["hosts"]["codex"]["expected"]
                if field == "retained_files":
                    expected[field][RETAINED[0]] = "f" * 64
                else:
                    expected[field] = "f" * 64 if field == "inventory_sha256" else "unexpected"
                self.write_binding()
                self.refuse_unchanged()

    def test_own14_missing_payload_core_and_evaluator_identity_refuse(self) -> None:
        inventory_path = self.plugins["codex"] / "assembly-inventory.json"
        original_inventory = inventory_path.read_bytes()
        for effect in ("wheel-missing", "core-missing", "evaluator-version", "evaluator-payload", "evaluator-archive"):
            with self.subTest(effect=effect):
                inventory_path.write_bytes(original_inventory)
                missing = None
                if effect.endswith("missing"):
                    name = "packages/" + self.identity.archive_name if effect == "wheel-missing" else RETAINED[0]
                    missing = self.plugins["codex"] / name
                    raw = missing.read_bytes()
                    missing.unlink()
                    self.change_inventory("codex", lambda value: value["files"].pop(name))
                else:
                    field = {"evaluator-version": "version", "evaluator-payload": "payload_sha256",
                             "evaluator-archive": "archive_sha256"}[effect]
                    self.change_inventory("codex", lambda value: value["evaluator"].update({field: "0.0.1" if field == "version" else "f" * 64}))
                self.refuse_unchanged()
                if missing is not None:
                    missing.write_bytes(raw)

    def test_own14_rehashed_modified_retained_contract_or_helper_remains_incompatible(self) -> None:
        for name in ("skills/harness-operator-brief/skill-contract.json", "skills/harness-orient/scripts/orient.py"):
            with self.subTest(path=name):
                path = self.plugins["codex"] / name
                original = path.read_bytes()
                if name.endswith(".json"):
                    value = json.loads(original)
                    value["activation"]["implicit"] = True
                    changed = canonical(value)
                else:
                    changed = original + b"\n# unreviewed changed helper identity\n"
                path.write_bytes(changed)
                self.binding["hosts"]["codex"]["expected"]["retained_files"][name] = sha(changed)
                self.change_inventory("codex", lambda value: value["files"][name].update({"sha256": sha(changed), "bytes": len(changed)}))
                result = self.refuse_unchanged()
                self.assertIn("incompatible", json.dumps(result), result)
                path.write_bytes(original)
                self.binding["hosts"]["codex"]["expected"]["retained_files"][name] = sha(original)
                self.change_inventory("codex", lambda value: value["files"][name].update({"sha256": sha(original), "bytes": len(original)}))


SMOKE_TESTS = {
    "test_own07_candidate_qualification_output_preserves_retired_skill",
    "test_own07_candidate_dashboard_output_preserves_installed_workflow",
    "test_own01_cli_plan_apply_stale_refusal_and_restore_json",
    "test_own01_exact_catalog_and_each_selected_host",
    "test_own05_replay_doctor_and_direct_installer_preserve_binding",
    "test_own07_unsupported_old_lock_refuses_before_writes",
    "test_own07_released_017_cli_format_and_command_refusals",
    "test_own07_released_017_protected_authoring_interfaces",
    "test_own07_released_017_ordinary_transitions_and_decisions",
    "test_own07_released_017_default_reports_preserve_protected_bytes",
    "test_own07_released_017_delegated_start",
    "test_own07_released_017_delegated_completion",
    "test_own07_released_017_retained_check_output_preserves_protected_bytes",
    "test_own07_released_017_qualification_output_cannot_recreate_retired_core",
    "test_own07_released_017_dashboard_output_cannot_replace_installed_workflow",
    "test_own11_restore_exact_distribution_and_refuse_owner_conflicts",
    "test_own12_clone_without_plugin_is_integral_and_availability_unobserved",
}


def acceptance_suite(smoke: bool = False) -> unittest.TestSuite:
    names = unittest.defaultTestLoader.getTestCaseNames(SkillOwnershipAcceptanceTests)
    suite = unittest.TestSuite(SkillOwnershipAcceptanceTests(name) for name in names if not smoke or name in SMOKE_TESTS)
    if not smoke:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(OwnershipReadBoundaryTests))
    return suite


if __name__ == "__main__":
    unittest.main()

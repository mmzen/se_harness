"""Run the setup reference's actual command blocks in disposable host fixtures.

This is verification tooling, not shipped plugin code or an alternative setup
implementation. Expected identities are fixed from published release evidence.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback

IDENTITIES = {
    "0.16.0": {
        "archive": "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
        "payload": "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
    },
    "0.17.0": {
        "archive": "305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced",
        "payload": "dd48b16b69d90a04412f458c756876ec22a687c99282075e69d0f58316c43405",
    },
}
REFERENCE = Path(__file__).resolve().parents[3] / "plugins/verity-plane/common/skills/setup/references/environment.md"


def snippets(path=REFERENCE):
    return dict(re.findall(r"<!-- snippet:([a-z]+) -->\n```[^\n]+\n(.*?)\n```", path.read_text(encoding="utf8"), re.S))


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


def ps_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def bash_quote(value):
    return "'" + str(value).replace("'", "'\"'\"'") + "'"


class Acceptance:
    def __init__(self, python, wheel, version, scratch, evidence, network):
        self.python, self.wheel, self.version = Path(os.path.abspath(python)), Path(os.path.abspath(wheel)), version
        self.expected = IDENTITIES[version]
        self.scratch, self.evidence = Path(os.path.abspath(scratch)), Path(os.path.abspath(evidence))
        self.scratch.mkdir(parents=True, exist_ok=False)
        self.evidence.mkdir(parents=True, exist_ok=False)
        self.blocks = snippets()
        shutil.copy2(REFERENCE, self.evidence / 'executed-reference.md')
        shutil.copy2(__file__, self.evidence / 'executed-runner.py')
        self.repo = self.scratch / "target repository"
        self.data = self.scratch / "persistent plugin data"
        self.repo.mkdir()
        self.data.mkdir()
        (self.repo / "owner.txt").write_text("Preserve this target repository.\n", encoding="utf8")
        self.env = self.data / "released evaluator"
        self.repo_before = snapshot(self.repo)
        self.shell = shutil.which("pwsh") or shutil.which("powershell") if os.name == "nt" else shutil.which("bash")
        if not self.shell:
            raise RuntimeError("A native PowerShell or Bash host is required")
        if not self.python.is_absolute() or not self.python.is_file():
            raise RuntimeError("Supply an existing absolute host Python")
        if hashlib.sha256(self.wheel.read_bytes()).hexdigest() != self.expected["archive"]:
            raise RuntimeError("Published wheel disagrees with fixed independent SHA-256")
        self.platform = {"system": platform.system(), "release": platform.release(),
                         "version": platform.version(), "python": self.command([str(self.python), "-I", "-c", "import sys; print(sys.version)"])["stdout"].strip(),
                         "evaluator": version, "network_constraint": network,
                         "host_shell": Path(self.shell).name,
                         "live_native_plugin_activation": False}
        if sys.platform.startswith('linux') and 'namespace' in network:
            devices = Path('/proc/net/dev').read_text()
            routes = Path('/proc/net/route').read_text()
            assert all(line.split(':')[0].strip() == 'lo' for line in devices.splitlines() if ':' in line)
            assert len(routes.splitlines()) == 1, 'network namespace has routes'
            self.platform['network_observation'] = {'devices': devices, 'routes': routes, 'external_interfaces': False}
        self.counter = 0
        self.commands = []
        self.results = []

    def sanitize(self, value):
        text = json.dumps(value, ensure_ascii=False)
        for path, replacement in ((self.scratch, "<fixture-root>"), (self.evidence, "<evidence-root>"),
                                  (self.python.parent, "<provided-python-root>"), (self.wheel.parent, "<wheel-root>"),
                                  (REFERENCE.parents[5], "<source-root>")):
            for form in {str(path), path.as_posix()}:
                text = text.replace(json.dumps(form)[1:-1], replacement)
        return json.loads(text)

    def save(self, name, value):
        (self.evidence / name).write_text(json.dumps(self.sanitize(value), indent=2, ensure_ascii=False) + "\n", encoding="utf8")

    def command(self, argv, *, env=None, cwd=None, timeout=120):
        started = time.monotonic()
        run = subprocess.run(argv, env=env, cwd=cwd, capture_output=True, timeout=timeout)
        result = {"argv": argv, "exit_status": run.returncode,
                  "duration_seconds": round(time.monotonic() - started, 4),
                  "stdout": run.stdout.decode("utf8", "replace"),
                  "stderr": run.stderr.decode("utf8", "replace")}
        if hasattr(self, "commands"):
            self.commands.append(result)
        return result

    def values(self, **overrides):
        self.counter += 1
        value = {"SetupPython": str(self.python), "Repo": str(self.repo), "Data": str(self.data),
                 "EnvDir": str(self.env), "Wheel": str(self.wheel), "Version": self.version,
                 "Payload": self.expected["payload"], "Archive": self.expected["archive"],
                 "IdentityFile": str(self.data / ("identity-%03d.json" % self.counter)),
                 "PrerequisiteCheck": self.blocks["prerequisites"], "InputCheck": self.blocks["inputs"],
                 "EntryCheck": self.blocks["entry"], "AcceptIdentity": self.blocks["accept"]}
        value.update({key: str(item) for key, item in overrides.items()})
        return value

    def setup(self, *, inherited=None, **overrides):
        values = self.values(**overrides)
        dialect = "powershell" if os.name == "nt" else "bash"
        quote = ps_quote if os.name == "nt" else bash_quote
        prefix = "$" if os.name == "nt" else ""
        source = "\n".join(prefix + key + "=" + quote(value) for key, value in values.items())
        source += "\n" + self.blocks[dialect] + "\n"
        script = self.scratch / ("invocation-%03d" % self.counter + (".ps1" if os.name == "nt" else ".sh"))
        script.write_text(source, encoding="utf8")
        argv = [self.shell, "-NoProfile", "-NonInteractive", "-File", str(script)] if os.name == "nt" else [self.shell, str(script)]
        process_env = os.environ.copy()
        process_env.update(inherited or {})
        original_path = os.environ.get("PATH")
        before = snapshot(self.repo)
        result = self.command(argv, env=process_env, cwd=self.repo)
        assert os.environ.get("PATH") == original_path, "parent PATH was changed"
        assert snapshot(self.repo) == before, "documented setup changed the target repository"
        result["document_snippet"] = dialect
        result["document_sha256"] = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
        result["selected_inputs"] = {key: value for key, value in values.items() if key not in
                                    ("PrerequisiteCheck", "InputCheck", "EntryCheck", "AcceptIdentity")}
        identity_path = Path(values["IdentityFile"])
        if identity_path.exists():
            try:
                result["identity"] = json.loads(identity_path.read_text(encoding="utf-8-sig"))
            except ValueError:
                result["identity"] = None
        result["repository_unchanged"] = True
        result["parent_path_unchanged"] = True
        return result

    def fragment(self, name, args=(), prefix=""):
        return self.command([str(self.python), "-I", "-S", "-c", prefix + self.blocks[name], *map(str, args)], cwd=self.repo)

    def site(self):
        if os.name == "nt":
            return self.env / "Lib/site-packages"
        return next((self.env / "lib").glob("python*/site-packages"))

    def installed(self, name):
        return self.site() / ("se_harness-" + self.version + ".dist-info") / name

    @contextlib.contextmanager
    def changed(self, path, content):
        old = path.read_bytes() if path.exists() else None
        if content is None:
            path.unlink()
        else:
            path.write_bytes(content)
        try:
            yield
        finally:
            if old is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(old)

    def run_case(self, case, description, method):
        self.commands = []
        started = time.monotonic()
        try:
            facts = method()
            result = {"case": case, "description": description, "passed": True, "observations": facts}
        except Exception as error:
            result = {"case": case, "description": description, "passed": False,
                      "failure": str(error), "traceback": traceback.format_exc()}
        result.update(platform=self.platform, expected=self.expected,
                      duration_seconds=round(time.monotonic() - started, 4), commands=self.commands)
        self.save(case.lower() + ".json", result)
        self.results.append({key: result[key] for key in ("case", "description", "passed")})
        print(case, "PASS" if result["passed"] else "FAIL", flush=True)

    def env01(self):
        result = self.setup()
        assert result["exit_status"] == 0, result["stderr"]
        assert result["identity"]["passed"] is True
        assert result["identity"]["evaluator_archive_sha256"] == self.expected["archive"]
        assert result["identity"]["evaluator_payload_sha256"] == self.expected["payload"]
        assert snapshot(self.repo) == self.repo_before
        (self.evidence / "env01-diff.txt").write_text("Target repository snapshot: unchanged.\nParent process PATH: unchanged.\n", encoding="utf8")
        return {"environment_ready": True, "setup_seconds": result["duration_seconds"], "identity": result["identity"],
                "repository_initialized": False, "manual_activation": False}

    def env02(self):
        missing = self.data / "missing-python-env"
        result = self.setup(SetupPython=self.data / "no-python", EnvDir=missing)
        assert result["exit_status"] != 0 and not missing.exists()
        observations = [{"variant": "missing Python executable", "blocked": True, "fixture": "real absent path"}]
        for name, prefix in [
            ("Python below 3.11", "import sys; sys.version_info=(3,10,0)\n"),
            ("missing venv", "import sys; sys.modules['venv']=None\n"),
            ("missing ensurepip", "import sys; sys.modules['ensurepip']=None\n"),
        ]:
            before = snapshot(self.data)
            result = self.fragment("prerequisites", prefix=prefix)
            assert result["exit_status"] != 0
            assert snapshot(self.data) == before
            observations.append({"variant": name, "blocked": True, "fixture": "isolated prerequisite-failure injection; no old/broken interpreter installed"})
        return observations

    def env03(self):
        partial = self.data / "interrupted environment"
        result = self.command([str(self.python), "-I", "-m", "venv", "--without-pip", str(partial)])
        assert result["exit_status"] == 0
        before = snapshot(partial)
        result = self.setup(EnvDir=partial)
        assert result["exit_status"] != 0
        assert snapshot(partial) == before
        return {"interruption_point": "environment created; pip/evaluator installation has not run", "ready": False,
                "retained_partial_files": sorted(before), "repair_attempted": False}

    def env04(self):
        before = {str(p.relative_to(self.env)): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                  for p in self.env.rglob("*") if p.is_file() and not p.is_symlink()}
        result = self.setup()
        after = {str(p.relative_to(self.env)): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                 for p in self.env.rglob("*") if p.is_file() and not p.is_symlink()}
        assert result["exit_status"] == 0, result["stderr"]
        assert before == after, "reuse changed installed files or timestamps"
        return {"same_environment_reused": True, "files_and_mtimes_unchanged": True,
                "identity_rechecked": result["identity"]["passed"], "reuse_seconds": result["duration_seconds"]}

    def env05(self):
        path = self.site() / "se_harness/__init__.py"
        content = path.read_bytes().replace(self.version.encode(), b"0.0.0-fixture")
        assert content != path.read_bytes()
        with self.changed(path, content):
            result = self.setup()
            assert result["exit_status"] != 0
            codes = [item["code"] for item in result["identity"]["diagnostics"]]
            assert "RID002" in codes
        return {"ready": False, "version_fixture": "changed installed runtime version; original restored", "diagnostic_codes": codes}

    def env06(self):
        path = self.site() / "se_harness/cli.py"
        with self.changed(path, path.read_bytes() + b"\n# altered fixture payload\n"):
            result = self.setup()
            assert result["exit_status"] != 0
            assert result["identity"]["evaluator_payload_sha256"] != self.expected["payload"]
        return {"ready": False, "fixed_expected_payload": self.expected["payload"], "observed": result["identity"]}

    def env07(self):
        path = self.installed("direct_url.json")
        value = json.loads(path.read_bytes())
        value["archive_info"] = {"hash": "sha256=" + "a" * 64, "hashes": {"sha256": "a" * 64}}
        with self.changed(path, json.dumps(value).encode()):
            result = self.setup()
            assert result["exit_status"] != 0
            assert result["identity"]["evaluator_archive_sha256"] == "a" * 64
        return {"ready": False, "observed_archive": result["identity"]["evaluator_archive_sha256"]}

    def env08(self):
        with self.changed(self.installed("direct_url.json"), None):
            result = self.setup()
            assert result["exit_status"] != 0
            assert result["identity"]["passed"] is True, "generic identity premise changed; inspect the released contract"
            assert result["identity"]["evaluator_archive_sha256"] is None
            assert result["identity"]["evaluator_wheel_sha256"] == self.expected["archive"]
        return {"generic_identity_passed": True, "plugin_ready": False, "expected_flag_was_supplied": True,
                "observed_archive": None}

    def env09(self):
        bad = self.scratch / "changed package"
        bad.mkdir()
        wheel = bad / self.wheel.name
        wheel.write_bytes(self.wheel.read_bytes() + b"changed after trust selection")
        target = self.data / "refused wheel environment"
        result = self.setup(Wheel=wheel, EnvDir=target)
        assert result["exit_status"] != 0 and not target.exists()
        return {"install_attempted": False, "ready": False, "expected_archive_unchanged": self.expected["archive"]}

    def env10(self):
        shadow = self.repo / "se_harness.py"
        foreign = self.scratch / "unrelated global bin"
        foreign.mkdir()
        (foreign / ("harnessctl.exe" if os.name == "nt" else "harnessctl")).write_text("Never execute this fixture.\n", encoding="utf8")
        marker = self.repo / "shadow-was-imported"
        payload = ("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('unsafe')\nraise RuntimeError('shadow imported')\n").encode()
        with self.changed(shadow, payload):
            result = self.setup(inherited={"PYTHONPATH": str(self.repo), "PATH": str(foreign) + os.pathsep + os.environ.get("PATH", "")})
            assert result["exit_status"] == 0, result["stderr"]
            identity = result["identity"]
            assert identity["isolated_python"] and not identity["pythonpath_present"]
            assert not marker.exists()
            assert str(self.env) in identity["entry_point_origin"]
        return {"isolated_python": True, "pythonpath_cleared": True, "shadow_imported": False,
                "entry_point": identity["entry_point_origin"], "controlled_path_first": str(self.env / ("Scripts" if os.name == "nt" else "bin"))}

    def env11(self):
        entry = self.env / ("Scripts/harnessctl.exe" if os.name == "nt" else "bin/harnessctl")
        with self.changed(entry, None):
            missing = self.setup()
            assert missing["exit_status"] != 0 and "identity" not in missing
        python = self.env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        wrong = self.fragment("entry", [self.env, python, self.python])
        assert wrong["exit_status"] != 0
        controlled = os.environ.copy()
        controlled.pop("PYTHONPATH", None)
        controlled["PATH"] = str(python.parent) + os.pathsep + controlled.get("PATH", "")
        argv = [str(python), "-I", "-m", "se_harness", "identity", "--role", "released-evaluator",
                "--expected-version", self.version, "--expected-root", str(self.data), "--checkout-root", str(self.repo),
                "--evaluator-payload-sha256", self.expected["payload"], "--evaluator-wheel-sha256", self.expected["archive"],
                "--entry-point", str(entry), "--require-entry-point", "--require-isolated-python", "--json"]
        root = self.command(argv, env=controlled, cwd=self.repo)
        assert root["exit_status"] != 0
        root_identity = json.loads(root["stdout"])
        assert any(item["code"] == "RID004" for item in root_identity["diagnostics"])
        # Inject a plain .pth search path and move the installed package aside.
        # The foreign module is an unchanged copy of the released package.
        source = self.site() / "se_harness"
        foreign = self.data / "foreign released package"
        foreign.mkdir()
        shutil.copytree(source, foreign / "se_harness")
        held = self.site() / "held_se_harness"
        source.rename(held)
        pth = self.site() / "foreign-fixture.pth"
        try:
            pth.write_text(str(foreign) + "\n", encoding="utf8")
            unsafe = self.setup()
            assert unsafe["exit_status"] != 0
            codes = [item["code"] for item in unsafe["identity"]["diagnostics"]]
            assert "RID003" in codes
        finally:
            pth.unlink(missing_ok=True)
            held.rename(source)
        return {"missing_entry_point_refused_before_identity": True, "wrong_entry_point_refused": True,
                "wrong_root_diagnostics": root_identity["diagnostics"], "foreign_import_diagnostics": codes}

    def env12(self):
        # Execute host-native discovery, then the documented prerequisite block.
        if os.name == "nt":
            argv = [self.shell, "-NoProfile", "-NonInteractive", "-Command",
                    "Get-Command -CommandType Application -Name " + ps_quote(str(self.python)) + " | Select-Object -ExpandProperty Source"]
        else:
            argv = [self.shell, "-c", "type -a -- " + bash_quote(str(self.python))]
        discovered = self.command(argv)
        assert discovered["exit_status"] == 0
        prerequisites = self.fragment("prerequisites")
        assert prerequisites["exit_status"] == 0
        # Check an installed root's identity lock, and a mismatched lock refusal.
        lock = self.repo / ".engineering-harness.lock"
        evaluator = {"version": self.version, "payload_sha256": self.expected["payload"],
                     "archive_sha256": self.expected["archive"], "archive_name": self.wheel.name}
        with self.changed(lock, json.dumps({"schema": 3, "evaluator": evaluator}).encode()):
            matched = self.setup()
            assert matched["exit_status"] == 0, matched["stderr"]
            before = snapshot(self.env)
            changed = {**evaluator, "version": "0.0.0"}
            lock.write_text(json.dumps({"schema": 3, "evaluator": changed}), encoding="utf8")
            mismatch = self.setup()
            assert mismatch["exit_status"] != 0 and snapshot(self.env) == before
        assert snapshot(self.repo) == self.repo_before
        return {"native_discovery_precedes_python_probe": True, "host": self.platform["system"],
                "other_shell": "execute this runner on that platform; not claimed from text inspection",
                "matching_lock_accepted": True, "wrong_lock_refused_without_upgrade": True,
                "new_plugin_executables": [], "target_snapshot_unchanged": True}

    def run(self):
        self.save("inputs.json", {"platform": self.platform, "expected": self.expected,
                  "wheel_sha256_observed_before_run": hashlib.sha256(self.wheel.read_bytes()).hexdigest(),
                  "reference_sha256": hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
                  "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "expectation_source": "Published 0.16.0/0.17.0 release identities retained in the approved PLG probe/assembly evidence; never candidate output."})
        cases = [
            ("ENV01", "Offline setup with spaces and no manual activation", self.env01),
            ("ENV02", "Missing or unsupported Python prerequisites", self.env02),
            ("ENV03", "Interrupted installation remains unavailable", self.env03),
            ("ENV04", "Reuse without reinstalling; identity rechecked", self.env04),
            ("ENV05", "Installed runtime version mismatch", self.env05),
            ("ENV06", "Modified installed payload", self.env06),
            ("ENV07", "Wrong observed archive digest", self.env07),
            ("ENV08", "Missing archive despite supplied expected hash", self.env08),
            ("ENV09", "Bundled wheel changed after trust selection", self.env09),
            ("ENV10", "Repository/PYTHONPATH/global-command shadowing", self.env10),
            ("ENV11", "Unsafe import origin, expected root and entry points", self.env11),
            ("ENV12", "Native discovery, command order and repository lock", self.env12),
        ]
        for case, description, method in cases:
            self.run_case(case, description, method)
        self.save("summary.json", {"platform": self.platform, "cases": self.results,
                  "passed": all(item["passed"] for item in self.results),
                  "limitations": ["Missing/broken prerequisite classes use isolated failure injection where noted.",
                                  "No native plugin installation or activation is exercised.",
                                  "Only the reported OS/interpreter/evaluator combination is exercised."]})
        return all(item["passed"] for item in self.results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--version", choices=IDENTITIES, required=True)
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--network-constraint", required=True, help="Observed execution boundary, not a claim invented by this runner")
    args = parser.parse_args()
    accepted = Acceptance(args.python, args.wheel, args.version, args.scratch, args.evidence, args.network_constraint).run()
    raise SystemExit(0 if accepted else 1)


if __name__ == "__main__":
    main()

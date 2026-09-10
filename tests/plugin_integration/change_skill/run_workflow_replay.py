"""Replay fixed observed commands with a verified external 0.16.0 evaluator.

This is portable command regression, not a new agent-behavior experiment. The
manifest fixes every lifecycle call. No authority selection is implemented.
All initialization, edits and Git writes occur only in a newly reserved sandbox.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import time
import tomllib


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(repo):
    return {p.relative_to(repo).as_posix(): digest(p) for p in sorted(repo.rglob("*"))
            if p.is_file() and ".git" not in p.parts}


def metadata(path):
    return tomllib.loads(path.read_text().split("+++", 2)[1])


def validate_inputs(fixtures):
    manifest = json.loads((fixtures / "manifest.json").read_text())
    for rel, expected in manifest["assets"].items():
        target = (fixtures / rel).resolve()
        if not target.is_relative_to(fixtures.resolve()) or digest(target) != expected:
            raise ValueError("Fixture input mismatch: " + rel)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).parent / "fixtures/observed")
    parser.add_argument("--sandbox", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--wheel", type=Path, required=True)
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Use the external evaluator's Python with -I")
    args.fixtures, args.sandbox, args.source, args.wheel = (
        path.resolve() for path in (args.fixtures, args.sandbox, args.source, args.wheel))
    manifest = validate_inputs(args.fixtures)  # Reject mismatch before any target writes.
    if digest(args.wheel) != manifest["archive_sha256"]:
        raise ValueError("Supplied released wheel input mismatch")
    if args.sandbox == args.source or args.source.is_relative_to(args.sandbox) or args.sandbox.is_relative_to(args.source):
        raise ValueError("Use a new disposable directory separate from the source")
    args.sandbox.mkdir(parents=True, exist_ok=False)
    evidence = args.sandbox / "behavior-evidence"
    evidence.mkdir()
    helpers = args.sandbox
    for path in (args.fixtures / "helpers").iterdir():
        shutil.copyfile(path, helpers / path.name)
    python = str(Path(sys.executable).absolute())  # Preserve POSIX venv symlink.
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PATH"] = str(Path(python).parent) + os.pathsep + env.get("PATH", "")
    commands, observations = [], []
    summary = {"classification": manifest["classification"], "platform": platform.platform(),
               "python": sys.version, "evaluator_python": python,
               "runner_sha256": digest(Path(__file__)), "fixture_manifest_sha256": digest(args.fixtures / "manifest.json"),
               "fresh_native_host_behavior": False, "decision_prompt_count": None,
               "limitations": ["No model is invoked: prompt counts and authority-refusal behavior remain the original Windows observations.",
                               "CHG07 live CI and delegated lifecycle are outside this replay.",
                               "Receipt loss is an after-exit injection; recovery actions are fixed replay inputs.",
                               "Governance context is delivered by the actual shared handler, without native host activation."],
               "observations": observations}

    def call(label, argv, repo=None, expected=0, phase="replay", stdin=None):
        before = snapshot(repo) if repo else {}
        start = time.time()
        result = subprocess.run(argv, cwd=args.sandbox, env=env, input=stdin,
                                capture_output=True, timeout=60)
        after = snapshot(repo) if repo else {}
        row = {"label": label, "phase": phase, "argv": argv, "cwd": str(args.sandbox),
               "started_unix": start, "duration_seconds": time.time() - start,
               "exit_code": result.returncode, "expected_exit": expected,
               "stdout": result.stdout.decode("utf8", "replace"), "stderr": result.stderr.decode("utf8", "replace"),
               "before": before, "after": after,
               "changed_paths": [p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]}
        if stdin is not None:
            row["stdin"] = stdin.decode("utf8")
        (evidence / (label + ".json")).write_text(json.dumps(row, indent=2) + "\n", encoding="utf8", newline="\n")
        commands.append({"label": label, "phase": phase, "argv": argv, "exit_code": result.returncode})
        print(json.dumps({"label": label, "exit_code": result.returncode, "changed_paths": row["changed_paths"]}), flush=True)
        if result.returncode != expected:
            raise AssertionError(label + ": unexpected process exit; see retained record")
        return row

    def evaluator(label, argv, repo=None, expected=0, phase="setup"):
        return call(label, [python, "-I", "-B", "-m", "se_harness", *argv], repo, expected, phase)

    def replay(name, repo, output_label=None):
        record = manifest["records"][name]
        replacements = {"{python}": python, "{repo}": str(repo), "{fixtures}": str(args.fixtures), "{helpers}": str(helpers)}
        argv = []
        for arg in record["argv"]:
            for token, replacement in replacements.items():
                arg = arg.replace(token, replacement)
            argv.append(arg)
        row = call(output_label or name, argv, repo, record["expected_exit"])
        if row["changed_paths"] != record["expected_changed_paths"]:
            raise AssertionError(name + ": changed-path mismatch against observed trace")
        if record["expected_state"] is not None:
            if json.loads(row["stdout"]).get("state") != record["expected_state"]:
                raise AssertionError(name + ": state mismatch against observed trace")
        if "lost-receipt" in name:
            observations.append({"case": name, "injection": "Receipt omitted after process exit; raw result retained independently.",
                                 "actual_changed_paths": row["changed_paths"]})
        return row

    def setup_repo(name, corrected=True, git=False):
        repo = args.sandbox / name
        evaluator(name + "-init", ["init", str(repo), "--project-name", "Change Acceptance Fixture", "--json"], repo)
        for path in (args.fixtures / "raw").rglob("*"):
            if path.is_file():
                rel = path.relative_to(args.fixtures / "raw").as_posix()
                if corrected:
                    rel = rel.replace("docs/engineering/acceptance/", "docs/engineering/demo-change/")
                target = repo / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                content = path.read_bytes()
                if corrected and path.name == "WO-ACC-001.md":
                    content = content.replace(b"docs/engineering/acceptance/", b"docs/engineering/demo-change/")
                target.write_bytes(content)
        if corrected:
            decision = json.loads((args.fixtures / "fixture-repair.json").read_text())["decision"]
            assert digest(repo / "docs/engineering/demo-change/work-orders/WO-ACC-001.md") == decision["reviewed_sha256"]
        if git:
            for index, argv in enumerate((["init", "-b", "main"], ["add", "--all"],
                                         ["-c", "user.name=Fixture Owner", "-c", "user.email=fixture@example.invalid", "commit", "-m", "Fixed disposable baseline"],
                                         ["update-ref", "refs/remotes/origin/main", "HEAD"])):
                call(name + "-git-" + str(index), ["git", "-C", str(repo), "-c", "core.autocrlf=false", *argv], repo, phase="setup")
        (evidence / (name + "-baseline.json")).write_text(json.dumps(snapshot(repo), indent=2) + "\n")
        return repo

    try:
        corrupt = args.sandbox / "corrupt-fixtures"
        shutil.copytree(args.fixtures, corrupt)
        corrupt_path = corrupt / "raw/src/feature.py"
        corrupt_path.write_bytes(corrupt_path.read_bytes() + b"# injected fixture corruption\n")
        rejected_target = args.sandbox / "mismatched-input-must-not-create"
        rejection = call("fixture-input-mismatch", [python, "-I", "-B", str(Path(__file__).resolve()),
                         "--fixtures", str(corrupt), "--sandbox", str(rejected_target), "--source", str(args.source),
                         "--wheel", str(args.wheel)], expected=1, phase="test-infrastructure")
        assert "Fixture input mismatch: raw/src/feature.py" in rejection["stderr"] and not rejected_target.exists()
        observations.append({"case": "Fixture input corruption", "classification": "Runner input-integrity regression, not candidate failure",
                             "rejected_before_target_creation": True, "passed": True})
        evaluator("identity", ["identity", "--role", "released-evaluator", "--expected-version", "0.16.0", "--expected-root", str(Path(python).parent.parent),
                               "--evaluator-payload-sha256", manifest["payload_sha256"], "--evaluator-wheel-sha256", manifest["archive_sha256"],
                               "--checkout-root", str(args.source), "--require-isolated-python", "--json"])
        for command in ("init", "create-artifact", "scaffold-domain", "transition", "check", "preflight", "evidence"):
            evaluator(command + "-help", [command, "--help"])

        definition = setup_repo("definition", corrected=False)
        for name in manifest["groups"]["definition_approval_original"]:
            replay(name, definition)
        intent = metadata(definition / "docs/engineering/acceptance/intent/INT-ACC-001.md")
        assert intent["status"] == "approved" and len(intent["lifecycle_events"]) == 1
        observations.append({"case": "CHG03", "state": "approved", "applied_transitions": 1, "passed": True})

        work = setup_repo("work", git=True)
        for name in manifest["groups"]["work_order_corrected_fixture"]:
            replay(name, work)
            if name == "chg06-passing-preflight":
                fixed = snapshot(work)
                observations.append({"case": "CHG06", "classification": "Empty mutation sequence from original observation, replayed as snapshots only",
                                     "before": fixed, "after": snapshot(work), "unchanged": fixed == snapshot(work), "transition_calls": 0})
            if name == "chg04-start-after":
                replay("chg05-proposed-scope", work)
        wo = metadata(work / "docs/engineering/demo-change/work-orders/WO-ACC-001.md")
        assert wo["status"] == "in_progress" and len(wo["lifecycle_events"]) == 2
        assert (work / "src/feature.py").read_text() == "def message():\n    return 'The feature is ready to use.'\n"
        assert digest(work / "src/outside.py") == digest(args.fixtures / "raw/src/outside.py")
        commit_result = call("chg04-commit-count", ["git", "-C", str(work), "rev-list", "--count", "origin/main..HEAD"], work)
        assert commit_result["stdout"].strip() == "2"
        observations.append({"case": "CHG04/CHG05/CHG09", "state": "in_progress", "local_feature_commits": 2,
                             "outside_file_unchanged": True, "approval_apply_calls": 1, "start_apply_calls": 1, "passed": True})

        for name in manifest["groups"]["package_after_work_order_group"]:
            replay(name, work)
        states = {aid: metadata(work / "docs/engineering/package-demo" / folder / (aid + ".md"))["status"]
                  for aid, folder in (("SPEC-PKG-001", "specifications"), ("WO-PKG-001", "work-orders"), ("DEC-PKG-001", "decisions"))}
        assert states == {"SPEC-PKG-001": "draft", "WO-PKG-001": "draft", "DEC-PKG-001": "open"}
        observations.append({"case": "CHG01/CHG08-create", "states": states, "spec_create_calls": 1, "passed": True})

        negative = setup_repo("negative")
        changed = negative / "docs/engineering/demo-change/intent/INT-ACC-001.md"
        before_injection = digest(changed)
        shutil.copyfile(args.fixtures / "changed-intent.md", changed)
        fixed = snapshot(negative)
        observations.append({"case": "CHG02", "classification": "Reconstructed fixed operands and empty mutation sequence; no fresh agent evaluated them",
                             "fixture_injection_before_sha256": before_injection, "fixture_injection_after_sha256": digest(changed),
                             "before": fixed, "after": snapshot(negative), "transition_calls": 0, "unchanged": fixed == snapshot(negative)})

        recovery = setup_repo("receipt-recovery")
        for name in manifest["groups"]["transition_receipt_recovery"]:
            replay(name, recovery)
        intent = metadata(recovery / "docs/engineering/demo-change/intent/INT-ACC-001.md")
        assert intent["status"] == "approved" and len(intent["lifecycle_events"]) == 1
        observations.append({"case": "CHG08-transition", "applied_transitions": 1, "state": "approved", "passed": True})

        readiness = setup_repo("readiness")
        replay("chg10-repeat-state-before", readiness)
        before = snapshot(readiness)
        observations.append({"case": "CHG10-unready", "classification": "Original selected checkpoint-free observation sequence; absent/stale/incomplete behavior was tested on Windows",
                             "before": before, "after": snapshot(readiness), "mutation_calls": 0, "unchanged": before == snapshot(readiness)})
        reference = args.source / "plugins/verity-plane/common/skills/setup/references/environment.md"
        blocks = dict(re.findall(r"<!-- snippet:([a-z]+) -->\n```[^\n]+\n(.*?)\n```", reference.read_text(), re.S))
        data = args.sandbox / "plugin-data"
        data.mkdir()
        values = {"SetupPython": python, "Repo": str(readiness), "Data": str(data), "EnvDir": str(data / "evaluator-016"),
                  "Wheel": str(args.wheel), "Version": "0.16.0", "Payload": manifest["payload_sha256"], "Archive": manifest["archive_sha256"],
                  "IdentityFile": str(data / "identity.json"), "PrerequisiteCheck": blocks["prerequisites"], "InputCheck": blocks["inputs"],
                  "EntryCheck": blocks["entry"], "AcceptIdentity": blocks["accept"]}
        script = args.sandbox / "readiness-setup.sh"
        script.write_text("\n".join(k + "=" + shlex.quote(v) for k, v in values.items()) + "\n" + blocks["bash"] + "\n", encoding="utf8", newline="\n")
        row = call("chg10-linux-setup", ["bash", str(script)], readiness, phase="setup-recovery")
        assert row["before"] == row["after"]
        context_script = args.source / "plugins/verity-plane/common/scripts/session-context.py"
        event = json.dumps({"hook_event_name": "SessionStart", "source": "resume", "cwd": str(readiness)}).encode("utf8")
        context = call("chg10-linux-context", [str(data / "evaluator-016/bin/python"), "-I", "-B", str(context_script), "--repo", str(readiness),
                       "--environment", str(data / "evaluator-016"), "--version", "0.16.0", "--payload-sha256", manifest["payload_sha256"],
                       "--archive-sha256", manifest["archive_sha256"], "--host", "codex", "--context-limit", "32768", "--read-limit", "32768"], readiness, stdin=event)
        assert "END VERIFIED GOVERNANCE" in context["stdout"] and "complete context delivered" in context["stdout"]
        assert context["before"] == context["after"]
        for name in ("chg10-repeat-preview", "chg10-repeat-apply", "chg10-repeat-state-after"):
            replay(name, readiness)
        assert metadata(readiness / "docs/engineering/demo-change/work-orders/WO-ACC-001.md")["status"] == "approved"
        observations.append({"case": "CHG10-recovery", "setup_reference_sha256": digest(reference), "context_handler_sha256": digest(context_script),
                             "complete_context_delivered": True, "state": "approved", "approval_apply_calls": 1, "passed": True})
        summary["passed"] = True
    except Exception as error:
        summary["passed"] = False
        summary["failure"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        summary["commands"] = commands
        (args.sandbox / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8", newline="\n")
        print(json.dumps({"passed": summary.get("passed"), "command_count": len(commands), "summary": str(args.sandbox / "summary.json")}))


if __name__ == "__main__":
    main()

"""Retained WO-ECP-007 demonstration; run against a separately installed wheel."""

import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=False)
    executable = str(Path(args.python).resolve())
    report = {
        "candidate": args.candidate,
        "wheel_sha256": hashlib.sha256(Path(args.wheel).read_bytes()).hexdigest(),
        "platform": platform.platform(),
        "python": executable,
        "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commands": [],
        "scenarios": [],
        "passed": False,
    }

    def run(label, command, expected=0):
        start = time.monotonic()
        result = subprocess.run(command, cwd=workspace, capture_output=True, timeout=90)
        elapsed = round(time.monotonic() - start, 4)
        entry = {
            "label": label, "argv": command, "cwd": str(workspace),
            "exit_code": result.returncode, "expected_exit": expected,
            "seconds": elapsed,
            "stdout": result.stdout.decode("utf-8", errors="replace"),
            "stderr": result.stderr.decode("utf-8", errors="replace"),
        }
        report["commands"].append(entry)
        if result.returncode != expected:
            raise AssertionError(f"{label}: expected exit {expected}, got {result.returncode}")
        return entry

    def cli(label, *arguments, expected=0):
        return run(label, [executable, "-I", "-B", "-m", "se_harness", *arguments, "--json"], expected)

    try:
        run("runtime", [executable, "-I", "-B", "-c",
            "import sys,se_harness,importlib.metadata,json; print(json.dumps({'python':sys.version,'package':se_harness.__file__,'version':importlib.metadata.version('se-harness')}))"])
        run("git-version", ["git", "--version"])
        for mode in ("explicit-git", "owner-rule"):
            consumer = workspace / mode
            consumer.mkdir()
            owner_bytes = b"# Owner instructions\nKeep this content unchanged.\n"
            (consumer / "AGENTS.md").write_bytes(owner_bytes)
            initialized = cli(mode + "/init", "init", str(consumer), "--project-name", "Consumer")
            files = sorted(p.relative_to(consumer).as_posix() for p in consumer.rglob("*") if p.is_file())
            assert files == [".engineering-harness.lock", ".engineering-harness.toml", "AGENTS.md"], files
            assert initialized["seconds"] < 60

            def git(*arguments):
                return run(mode + "/git-" + arguments[0], ["git", "-C", str(consumer), *arguments])

            git("init", "--quiet")
            git("config", "user.name", "Consumer qualification")
            git("config", "user.email", "consumer@example.invalid")
            git("config", "core.autocrlf", "false")
            git("add", ".")
            git("commit", "--quiet", "-m", "Minimal installation")
            missing = cli(mode + "/missing-attributes", "doctor", str(consumer), expected=1)
            failed = [c["name"] for c in json.loads(missing["stdout"])["checks"] if not c["passed"]]
            assert "hash-bound-attribute-effective" in failed, failed
            assert not (consumer / "docs").exists()

            if mode == "explicit-git":
                cli(mode + "/preview", "upgrade", str(consumer), "--integration", "git")
                cli(mode + "/apply", "upgrade", str(consumer), "--integration", "git", "--apply")
            else:
                (consumer / ".gitattributes").write_bytes(b"docs/engineering/**/evidence/*.json text eol=lf\n")
            git("add", ".")
            git("commit", "--quiet", "-m", "Select evidence attributes")
            ready = cli(mode + "/ready", "doctor", str(consumer))
            assert all(c["passed"] for c in json.loads(ready["stdout"])["checks"])
            assert ready["seconds"] < 60
            assert not (consumer / "docs").exists()
            assert (consumer / "AGENTS.md").read_bytes() == owner_bytes
            with (consumer / ".gitattributes").open("ab") as stream:
                stream.write(b"docs/engineering/**/evidence/*.json -text\n")
            damaged = cli(mode + "/damaged-attributes", "doctor", str(consumer), expected=1)
            failed = [c["name"] for c in json.loads(damaged["stdout"])["checks"] if not c["passed"]]
            assert "hash-bound-attribute-effective" in failed, failed
            report["scenarios"].append({
                "mode": mode, "passed": True, "initial_files": files,
                "init_seconds": initialized["seconds"], "doctor_seconds": ready["seconds"],
                "no_evidence_directory_created": True, "owner_bytes_preserved": True,
                "missing_and_damaged_attributes_rejected": True,
            })
        report["passed"] = True
    except Exception as error:
        report["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({key: report[key] for key in ("candidate", "wheel_sha256", "platform", "scenarios", "passed")}))


if __name__ == "__main__":
    main()

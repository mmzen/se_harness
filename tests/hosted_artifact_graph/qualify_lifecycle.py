"""Released-command feasibility first; this does not qualify the hosted service."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
import tomllib
from pathlib import Path

from lifecycle_fixture import DOMAIN, REL, VER, WORK, write


class ReferenceRun:
    def __init__(self, python, output):
        self.python, self.output = python.resolve(), output.resolve()
        self.output.mkdir(parents=True, exist_ok=False)
        self.root = self.output / "test-copy"
        self.entries = []

    def run(self, label, argv, *, cwd=None, expected=0):
        env = {k: v for k, v in os.environ.items() if not k.startswith(("PYTHON", "GIT_"))}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        started = time.monotonic()
        process = subprocess.run(list(map(str, argv)), cwd=cwd or self.output, env=env,
                                 capture_output=True, timeout=180)
        out, err = process.stdout.decode("utf-8", "replace"), process.stderr.decode("utf-8", "replace")
        entry = {"label": label, "argv": list(map(str, argv)), "cwd": str(cwd or self.output),
                 "exit": process.returncode, "seconds": round(time.monotonic() - started, 3), "stdout": out, "stderr": err}
        self.entries.append(entry)
        (self.output / f"{len(self.entries):03}-{label}.json").write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"step": label, "exit": process.returncode, "seconds": entry["seconds"]}), flush=True)
        if process.returncode != expected:
            raise RuntimeError(f"{label}: expected {expected}, got {process.returncode}; inspect retained result")
        try:
            return json.loads(out)
        except ValueError:
            return out.strip()

    def cli(self, label, command, *args, expected=0):
        return self.run(label, [self.python, "-I", "-m", "se_harness", command, self.root, *args, "--json"], expected=expected)

    def git(self, label, *args):
        return self.run(label, ["git", "-c", "core.hooksPath=/dev/null", "-c", "core.autocrlf=false",
            "-c", "commit.gpgsign=false", "-c", "user.name=Rehearsal Test", "-c", "user.email=rehearsal@example.invalid", *args], cwd=self.root)

    def commit(self, label):
        self.git(label + "-stage", "add", "--all")
        self.git(label + "-commit", "commit", "-m", label)
        return self.git(label + "-head", "rev-parse", "HEAD")

    def transition(self, label, ids, state, actor="test-owner"):
        args = []
        for ident in ids:
            args += ["--set", f"{ident}={state}", "--decision", f"{ident}={actor}",
                     "--reason", f"{ident}=Synthetic rehearsal only; no real human decision or external authority."]
        self.cli(label + "-preview", "transition", *args)
        return self.cli(label, "transition", *args, "--apply")

    def execute(self):
        self.cli("init", "init", "--project-name", "Disposable lifecycle rehearsal", "--integration", "git")
        identity = json.loads((self.root / ".engineering-harness.lock").read_text())["evaluator"]
        if (identity.get("version") != "0.22.1"
                or identity.get("archive_sha256") != "cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053"
                or identity.get("payload_sha256") != "0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff"):
            raise RuntimeError("The reference must use the approved released 0.22.1 evaluator")
        self.git("git-init", "init", "--quiet", "--template=", "-b", "main")
        (self.root / "REHEARSAL.txt").write_text("Synthetic test copy. No real human authority.\n", encoding="utf-8")
        (self.root / "src").mkdir()
        (self.root / "src/greeting.py").write_text("def greeting():\n    return 'Not implemented'\n", encoding="utf-8")
        write(self.root)
        self.cli("validate-drafts", "validate")
        base = self.commit("draft-fixture")
        self.transition("approve-definitions", ["INT-P3-001", "CAP-P3-001", "REQ-P3-001", "SPEC-P3-001", VER, REL], "approved")
        self.transition("approve-work", [WORK], "approved")
        self.cli("start-preflight", "preflight", "--work-order", WORK, "--phase", "start")
        self.transition("start-work", [WORK], "in_progress", "test-executor")
        risk_args = ["--domain", "lifecycle-pilot", "--id", "RISK-P3-001", "--title", "Incorrect test greeting",
                     "--description", "A test implementation could return a different greeting.",
                     "--action", "Run the independent exact-string assertion.", "--owner", "test-owner",
                     "--raised-by", "test-executor", "--threatens", WORK,
                     "--with-decision", "--decision-id", "DEC-P3-001", "--recommend", "mitigate"]
        self.cli("risk-preview", "raise-risk", *risk_args, "--dry-run")
        self.cli("risk-create", "raise-risk", *risk_args)
        decide_args = ["--artifact", "DEC-P3-001", "--option", "mitigate", "--mitigated-by", WORK,
                       "--decision", "test-owner", "--reason", "Synthetic risk treatment; no real risk acceptance."]
        self.cli("decision-preview", "decide", *decide_args)
        self.cli("decision-apply", "decide", *decide_args, "--apply")
        self.cli("context", "check", "--artifact", WORK)
        self.cli("scope", "check", "--artifact", WORK, "--checkpoint", "scope", "--from-git", base)
        (self.root / "src/greeting.py").write_text("def greeting():\n    return 'Hello rehearsal'\n", encoding="utf-8")
        self.run("greeting-assertion", [self.python, "-I", "-c",
            "import runpy,sys; assert runpy.run_path(sys.argv[1])['greeting']() == 'Hello rehearsal'; print('exact greeting passed')",
            self.root / "src/greeting.py"])
        evidence = f"{DOMAIN}/evidence/{WORK}/assertion.json"
        (self.root / evidence).parent.mkdir(parents=True, exist_ok=True)
        (self.root / evidence).write_text(json.dumps(self.entries[-1], indent=2) + "\n", encoding="utf-8")
        self.cli("review-preflight", "preflight", "--work-order", WORK, "--phase", "review")
        # The released handoff procedure first creates its exact evidence header.
        self.cli("handoff-evidence", "evidence", "--artifact", WORK, "--checkpoint", "handoff")
        self.cli("handoff", "check", "--artifact", WORK, "--checkpoint", "handoff", "--from-git", base)
        self.transition("complete-work", [WORK], "implemented", "test-executor")
        candidate = self.commit("implemented-test-candidate")
        self.cli("capture", "capture-verification", "--id", "VREC-P3-001", "--work-order", WORK,
            "--verification", VER, "--evidence", evidence, "--owner", "quality-owner", "--domain", "lifecycle-pilot")
        self.transition("verify-test", ["VREC-P3-001"], "verified", "quality-owner")
        self.commit("test-verification-decision")
        self.cli("prepare-release", "prepare-release", "--id", "RLS-P3-001", "--release-contract", REL,
            "--verification-record", "VREC-P3-001", "--work-order", WORK, "--version", "0.0.1",
            "--owner", "release-owner", "--tag", "rehearsal-0.0.1", "--domain", "lifecycle-pilot")
        self.transition("release-test", ["RLS-P3-001"], "released", "release-owner")
        self.commit("test-release-decision")
        self.cli("final-validation", "validate")
        self.cli("final-record", "check", "--artifact", "RLS-P3-001")
        self.git("git-bundle", "bundle", "create", str(self.output / "test-history.bundle"), "--all")
        replay = self.output / "independent-replay"
        self.run("replay-clone", ["git", "-c", "core.autocrlf=false", "-c", "core.hooksPath=/dev/null",
            "clone", "--quiet", "--template=", self.output / "test-history.bundle", replay])
        tracked = self.git("export-paths", "ls-files").splitlines()
        for name in tracked:
            if (self.root / name).read_bytes() != (replay / name).read_bytes():
                raise RuntimeError("Export replay bytes differ: " + name)
        self.run("replay-validation", [self.python, "-I", "-m", "se_harness", "validate", replay, "--json"])
        self.run("replay-release-check", [self.python, "-I", "-m", "se_harness", "check", replay,
            "--artifact", "RLS-P3-001", "--json"])
        result = {"schema": "hag-phase3-released-feasibility/v1", "test_only": True,
                  "base": base, "candidate": candidate, "hosted_scenarios_executed": 0,
                  "outcome": "passed", "steps": len(self.entries), "evaluator": identity,
                  "replayed_exact_files": len(tracked), "artifacts": []}
        for path in sorted((self.root / DOMAIN).rglob("*.md")):
            if path.read_bytes().startswith(b"+++"):
                record = tomllib.loads(path.read_text(encoding="utf-8").split("+++", 2)[1])
                result["artifacts"].append({"path": path.relative_to(self.root).as_posix(), "id": record["id"],
                    "status": record["status"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        (self.output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluator-python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(ReferenceRun(args.evaluator_python, args.output).execute(), indent=2))

"""CHG07 supplement: probe the released guard with real GitHub check results.

This observes the existing guard, not model behavior or applied transitions.
Local clones isolate base/ref variants. No configuration or CI result is faked.
Run with the verified external evaluator's Python and -I from outside a checkout.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tomllib

from se_harness.gate_source import authorize_delegated_right, DelegationError

WO = "docs/engineering/plugin-integration/work-orders/WO-PLG-010.md"
LIVE = "9bc323a7bd5bd259b1ba2098b719314091734a20"
DEFINITION = "f20943ba509537d4896b48c39a8e58ba7643309b"
BEFORE_DEFINITION = "403a2c10f449032dc67ae70d4a9e37286d07d754"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--sandbox", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("run with the verified external evaluator and -I")
    args.source = args.source.resolve()
    args.sandbox = args.sandbox.resolve()
    args.evidence = args.evidence.resolve()
    args.sandbox.mkdir(parents=True, exist_ok=False)
    args.evidence.mkdir(parents=True, exist_ok=False)
    commands, observations = [], []
    source_git_dir = None

    def git(repo, *argv):
        command = ["git", "-c", "safe.directory=" + repo.as_posix(), "-c", "core.longpaths=true",
                   "-c", "core.autocrlf=false"]
        if source_git_dir:
            command.extend(["-c", "safe.directory=" + source_git_dir])
        command.extend(["-C", str(repo), *argv])
        env = os.environ.copy()
        if source_git_dir:
            # Git's local transport drops command-line configuration. Give only
            # this child process an isolated config for these exact source paths.
            config = args.sandbox / "fixture.gitconfig"
            config.write_text("[safe]\n\tdirectory = " + args.source.as_posix() +
                              "\n\tdirectory = " + source_git_dir + "\n",
                              encoding="utf8", newline="\n")
            env["GIT_CONFIG_GLOBAL"] = str(config)
        run = subprocess.run(command, capture_output=True, cwd=args.sandbox, env=env)
        commands.append({"argv": command, "exit_status": run.returncode,
                         "stdout": run.stdout.decode("utf8", "replace"),
                         "stderr": run.stderr.decode("utf8", "replace")})
        if run.returncode:
            raise RuntimeError(commands[-1])
        return run.stdout.decode("utf8").strip()

    def clone(name, head, base):
        repo = args.sandbox / name
        git(args.source, "clone", "--shared", "--no-checkout", args.source.as_posix(), repo.as_posix())
        git(repo, "checkout", "--detach", head)
        git(repo, "update-ref", "refs/remotes/origin/main", base)
        # Configurable subprocess environment is process-local, never written to the clone.
        os.environ.update(GIT_CONFIG_COUNT="2", GIT_CONFIG_KEY_0="safe.directory",
                          GIT_CONFIG_VALUE_0=str(repo), GIT_CONFIG_KEY_1="core.longpaths",
                          GIT_CONFIG_VALUE_1="true")
        return repo

    def probe(repo, case, right, expected_code=None):
        path = repo / WO
        before = path.read_bytes()
        status_before = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
        row = {"case": case, "right": right, "head": git(repo, "rev-parse", "HEAD"),
               "base": git(repo, "rev-parse", "origin/main"), "expected_code": expected_code}
        match = re.match(r"\A\+\+\+\r?\n(.*?)\r?\n\+\+\+(?:\r?\n|\Z)", before.decode("utf8"), re.S)
        if not match:
            raise ValueError("fixture has no line-delimited TOML metadata")
        try:
            row["gate"] = asdict(authorize_delegated_right(repo,
                work_order_metadata=tomllib.loads(match.group(1)),
                work_order_path=path, right=right))
            row["passed"] = expected_code is None and row["gate"]["conclusion"] == "success"
        except DelegationError as error:
            row["error"] = {"code": error.code, "message": str(error)}
            row["passed"] = error.code == expected_code
        row["work_order_unchanged"] = before == path.read_bytes()
        row["git_status_unchanged"] = status_before == git(repo, "status", "--porcelain=v1", "--untracked-files=all")
        row["passed"] = row["passed"] and row["work_order_unchanged"] and row["git_status_unchanged"]
        observations.append(row)
        print(json.dumps(row), flush=True)

    try:
        source_git_dir = Path(git(args.source, "rev-parse", "--absolute-git-dir")).as_posix()
        live = clone("published", LIVE, LIVE)
        for right in ("DR-WO-START", "DR-WO-COMPLETE", "DR-VREC-PREPARE"):
            probe(live, "published-exact-check", right)
        for right in ("DR-WO-APPROVE", "DR-VREC-DECIDE", "DR-RLS-DECIDE", "DR-EXTERNAL-ACTION"):
            probe(live, "right-not-delegated", right, "WEX-ECP-022")
        branch = clone("branch-only", DEFINITION, BEFORE_DEFINITION)
        probe(branch, "class-missing-at-base", "DR-WO-START", "WEX-ECP-022")
        stale = clone("new-unpublished-head", LIVE, LIVE)
        # A new local commit has no GitHub check; the published parent's pass must not carry over.
        marker = stale / "plugins/verity-plane/common/skills/change/fixture-head.txt"
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("Disposable CHG07 fixture, never pushed.\n", encoding="utf8", newline="\n")
        git(stale, "add", "--", marker.relative_to(stale).as_posix())
        git(stale, "-c", "user.name=CHG07 fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-m", "Disposable unpublished candidate for stale-check refusal")
        probe(stale, "parent-pass-is-not-current-pass", "DR-WO-START", "WEX-ECP-040")
    finally:
        metadata = {"classification": "Released guard integration, not a skill-behavior test or lifecycle application",
                    "python": sys.version, "platform": platform.platform(),
                    "evaluator_python": sys.executable, "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "observations": observations}
        (args.evidence / "chg07-guard.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf8", newline="\n")
        (args.evidence / "commands.json").write_text(json.dumps(commands, indent=2) + "\n", encoding="utf8", newline="\n")
    return 0 if len(observations) == 9 and all(row["passed"] for row in observations) else 1


if __name__ == "__main__":
    raise SystemExit(main())

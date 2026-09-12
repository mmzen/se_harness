"""Prepare only WO-PLG-005's disposable accepted-profile fixture and package."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

HERE = Path(__file__).absolute().parent
ROOT = HERE.parents[2]
WORK = ROOT.parent
PYTHON = WORK / "se-harness-plugin-eval-016/Scripts/python.exe"
CODEX = Path("C:/Users/mathi/AppData/Local/OpenAI/Codex/bin/8e5b6932251c2c1c/codex.exe")
PROFILE = WORK / "plugin-probe-sandboxes/codex/run-001 with spaces/profile"
SCHEMAS = PROFILE.parent / "schemas"
SANDBOX = WORK / "codex-adapter-sandboxes/accepted 001 with spaces"
PROBE = ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/readiness-fixture-inputs/synthetic-inputs"
sys.path.insert(0, str(ROOT / "tests/plugin_integration/codex_probe"))
from probe import isolated_environment


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n")


def run(argv, folder, *, cwd=ROOT, env=None):
    folder.mkdir(parents=True, exist_ok=False)
    result = subprocess.run([str(item) for item in argv], cwd=cwd, env=env, capture_output=True, timeout=120)
    write(folder / "command.json", {"argv": [str(item) for item in argv], "exit_status": result.returncode})
    (folder / "stdout.txt").write_bytes(result.stdout)
    (folder / "stderr.txt").write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError("command failed; inspect " + str(folder))
    return result


def host_environment():
    return isolated_environment(PROFILE)


def host_argv(*args):
    # Native /hooks review explicitly disabled the old probe hooks. The initial
    # process-local plugin-disable override did not disable them; retained
    # preparation evidence preserves that attempt. Verify loaded state per run.
    return [str(CODEX), *args]


def binding(repo, environment=PYTHON.parent.parent, capture=True):
    decision_path = ROOT / "docs/engineering/plugin-integration/decisions/DEC-PLG-001.md"
    metadata = tomllib.loads(decision_path.read_text(encoding="utf8").split("+++", 2)[1])
    return {"schema": "verity-codex-binding-v1", "repo": str(repo), "environment": str(environment),
            "artifact": "WO-PROBE-001", "capture": capture,
            "profile": {"host": "0.153.4", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"},
            "decision": {"id": metadata["id"], "status": metadata["status"],
                         "option": metadata.get("disposition", {}).get("option")}}


def prepare(evidence):
    SANDBOX.mkdir(parents=True, exist_ok=False)
    repo = SANDBOX / "repo with spaces"
    run([PYTHON, "-I", "-B", "-m", "se_harness", "init", repo, "--project-name", "codex-adapter-fixture", "--json"], evidence / "init", cwd=SANDBOX)
    for source in PROBE.rglob("*.md.txt"):
        destination = repo / source.relative_to(PROBE).as_posix().removesuffix(".txt")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    wo = repo / "docs/engineering/readiness-probe/work-orders/WO-PROBE-001.md"
    wo.write_text(wo.read_text().replace('status = "approved"', 'status = "in_progress"', 1)
                  .replace('paths = ["governed-target.txt"]', 'paths = ["governed-target.txt", "café quoted \' target.txt"]'), encoding="utf8")
    for name in ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt"):
        (repo / name).write_text("initial fixture target\n", encoding="utf8")
    run([PYTHON, "-I", "-B", "-m", "se_harness", "evidence", repo, "--artifact", "WO-PROBE-001", "--checkpoint", "pre-action", "--json"], evidence / "pre-action", cwd=SANDBOX)
    observed = run([CODEX, "--version"], evidence / "host-version", cwd=SANDBOX, env=host_environment())
    if observed.stdout.decode().strip() != "codex-cli 0.153.4":
        raise RuntimeError("selected actual host is not the DEC-PLG-001 profile")
    write(evidence / "identity.json", {"host_executable": str(CODEX), "host_sha256": sha(CODEX),
          "expected_host_version": "codex-cli 0.153.4", "python": str(PYTHON), "python_sha256": sha(PYTHON),
          "profile": str(PROFILE), "profile_origin": "Existing authenticated disposable WO-PLG-003 file store; no credentials copied",
          "sandbox": str(SANDBOX), "fixture_sources": {p.relative_to(PROBE).as_posix(): sha(p) for p in PROBE.rglob("*.md.txt")}})
    write(evidence / "fixture-source-hashes.json", {p.relative_to(repo).as_posix(): sha(p) for p in repo.rglob("*") if p.is_file()})
    return repo


def assemble(revision, evidence):
    wheel = WORK / "plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl"
    output = SANDBOX / ("package " + revision[:12])
    argv = [PYTHON, "-I", "-B", ROOT / "scripts/build_plugin_archives.py", "build", "--revision", revision,
            "--plan", "tests/plugin_integration/codex_adapter/assembly-plan.json", "--release-revision", revision,
            "--release-record", "docs/engineering/release-0-16-0/releases/RLS-SEH-025.md",
            "--expected-wheel-sha256", "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
            "--wheel", wheel, "--evaluator-python", PYTHON, "--output-directory", output]
    run(argv, evidence / "build")
    argv[4] = "check"
    run(argv, evidence / "check")
    marketplace = SANDBOX / "marketplace with spaces"
    target = marketplace / "plugins/verity-plane"
    shutil.copytree(output / "codex/verity-plane", target)
    write(marketplace / ".agents/plugins/marketplace.json", {
        "name": "verity-plane-codex-fixture", "interface": {"displayName": "Codex adapter disposable acceptance"},
        "plugins": [{"name": "verity-plane", "source": {"source": "local", "path": "./plugins/verity-plane"},
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": "Productivity"}]})
    write(evidence / "package.json", {"asset_revision": revision, "archive_sha256": sha(output / "verity-plane-codex.zip"),
          "package_root": str(target), "payload": {p.relative_to(target).as_posix(): sha(p) for p in target.rglob("*") if p.is_file()},
          "companion": "The Claude output is an explicitly inert assembly fixture; no native Claude support claim."})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "assemble", "install"))
    parser.add_argument("--revision")
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    if args.action == "prepare":
        print(prepare(args.evidence))
    elif args.action == "assemble":
        assemble(args.revision, args.evidence)
    else:
        marketplace = SANDBOX / "marketplace with spaces"
        run(host_argv("plugin", "marketplace", "add", str(marketplace)), args.evidence / "marketplace-add", env=host_environment())
        run(host_argv("plugin", "add", "verity-plane@verity-plane-codex-fixture", "--json"), args.evidence / "plugin-add", env=host_environment())
        run(host_argv("plugin", "list", "--json"), args.evidence / "plugin-list", env=host_environment())

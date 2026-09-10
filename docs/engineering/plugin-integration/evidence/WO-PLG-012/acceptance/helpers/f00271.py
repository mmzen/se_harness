"""Build a fresh platform-native fixture through the real released evaluator."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_runner import environment, sha, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--product-root", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    here = Path(__file__).resolve().parent
    fixtures = here / "fixtures"
    for rel, expected in json.loads((fixtures / "input-sha256.json").read_text()).items():
        if sha(fixtures / rel) != expected:
            raise ValueError("Frozen fixture input mismatch: " + rel)
    output.mkdir(parents=True, exist_ok=False)
    repository = output / "repository"
    home = output / "isolated-home"
    home.mkdir()
    credential = home / "synthetic-credentials.txt"
    credential.write_text("synthetic-canary-not-a-real-secret\n")
    git = shutil.which("git")
    if git is None:
        raise ValueError("Fixture requires local Git")
    import se_harness
    settings = {"python": str(Path(sys.executable).absolute()), "environment": sys.prefix, "git": str(Path(git).absolute()),
                "target": str(repository), "home": str(home), "synthetic_credential": str(credential),
                "engine": str(Path(se_harness.__file__).resolve().parent / "engine"), "platform": platform.platform(), "python_version": sys.version,
                "read_roots": [sys.prefix, sys.base_prefix, str(output)], "helpers": {}, "product_sha256": {}}
    for name, script in (("harness-orient", "orient.py"), ("harness-operator-brief", "check_brief.py")):
        source = args.product_root.resolve() / name
        core = output / "frozen-plugin" / name
        shutil.copytree(source, core)
        relative = "scripts/" + script
        managed = fixtures / "governing-source/.agents/skills" / name
        for rel in (relative, "skill-contract.json"):
            if sha(source / rel) != sha(managed / rel):
                raise ValueError("Packaged helper/contract changed: " + name + "/" + rel)
        settings["helpers"]["orient" if name == "harness-orient" else "brief"] = str(core / relative)
        for file in core.rglob("*"):
            if file.is_file():
                settings["product_sha256"][str(file)] = sha(file)
    env = environment(settings)
    source_copy = output / "setup-executed-source"
    shutil.copytree(here, source_copy, ignore=shutil.ignore_patterns("__pycache__"))
    (output / "setup-source-sha256.json").write_text(json.dumps(snapshot(source_copy), indent=2) + "\n")
    trace = output / "setup-trace"
    trace.mkdir()

    def run(label, argv):
        before, started = snapshot(repository), time.time()
        stdout = stderr = b""
        status = None
        error = None
        try:
            result = subprocess.run(argv, cwd=output, env=env, capture_output=True, timeout=90)
            stdout, stderr, status = result.stdout, result.stderr, result.returncode
        except (OSError, subprocess.TimeoutExpired) as exc:
            error = {"type": type(exc).__name__, "message": str(exc)}
            stdout, stderr = getattr(exc, "stdout", None) or b"", getattr(exc, "stderr", None) or b""
        row = {"argv": argv, "cwd": str(output), "exit_code": status, "stdout": stdout.decode("utf8", "replace"), "stderr": stderr.decode("utf8", "replace"),
               "execution_error": error, "before": before, "after": snapshot(repository), "started_unix": started}
        (trace / (label + ".json")).write_text(json.dumps(row, indent=2) + "\n")
        print(json.dumps({"setup": label, "exit_code": status}), flush=True)
        if status != 0:
            raise ValueError("Fixture setup failed; retained " + label)
    evaluator = [settings["python"], "-I", "-B", "-m", "se_harness"]
    run("identity", [*evaluator, "identity", "--role", "released-evaluator", "--expected-version", "0.16.0", "--expected-root", sys.prefix,
                     "--evaluator-payload-sha256", "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
                     "--evaluator-wheel-sha256", "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae", "--require-isolated-python"])
    run("init", [*evaluator, "init", str(repository), "--project-name", "Retained helper fixture", "--json"])
    before_assets = snapshot(repository)
    for path in (fixtures / "raw-assets").rglob("*"):
        if path.is_file():
            dest = repository / path.relative_to(fixtures / "raw-assets")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    (repository / "readonly-sentinel.txt").write_text("tracked target bytes\n")
    (repository / "target").mkdir(exist_ok=True)
    (repository / "target/ignored-sentinel.txt").write_text("ignored bytes still measured\n")
    (trace / "raw-assets.json").write_text(json.dumps({"classification": "Explicit synthetic authored fixture setup", "before": before_assets, "after": snapshot(repository)}, indent=2) + "\n")
    run("git-init", [git, "-C", str(repository), "init", "-b", "main"])
    run("git-add", [git, "-C", str(repository), "add", "--all"])
    run("git-commit", [git, "-C", str(repository), "-c", "user.name=Retained Fixture", "-c", "user.email=retained@example.invalid", "commit", "-m", "Fixed read-only retained-helper fixture"])
    run("git-base", [git, "-C", str(repository), "update-ref", "refs/remotes/origin/main", "HEAD"])
    run("doctor", [*evaluator, "doctor", str(repository)])
    run("validate", [*evaluator, "validate", str(repository), "--json"])
    (output / "settings.json").write_text(json.dumps(settings, indent=2) + "\n", encoding="utf8")
    (output / "setup-final-snapshot.json").write_text(json.dumps(snapshot(repository), indent=2) + "\n")
    print(json.dumps({"prepared": True, "settings": str(output / "settings.json")}))


if __name__ == "__main__":
    main()

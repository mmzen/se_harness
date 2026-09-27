"""Transient Windows demo preparation; not part of se_harness or a release."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

WORKSPACE = Path(__file__).resolve().parents[2]
SOURCE = WORKSPACE / "work/se_harness"
PACKAGE = WORKSPACE / "work/ci19-package.json"
SHARED_WHEEL = Path(__file__).resolve().parent / "inputs/se_harness-0.19.0-py3-none-any.whl"
SOURCE_COMMIT = "2b45556ee23aff46e2cb131ac08992dc59131709"
WHEEL_HASH = "3b45680ee7f76509e09a933a4d061ff522d29c25b236201985861376221f5b3f"
HOSTS = {
    "codex": Path(r"C:\Users\mathi\AppData\Local\OpenAI\Codex\bin\13995fba801849b0\codex.exe"),
    "claude": Path(r"C:\Users\mathi\.local\bin\claude.exe"),
}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child_env(base, host):
    profile = base / "profiles" / host
    env = {k: os.environ[k] for k in (
        "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "NUMBER_OF_PROCESSORS",
        "PROCESSOR_ARCHITECTURE", "TERM", "COLORTERM"
    ) if k in os.environ}
    env.update({
        "HOME": str(profile), "USERPROFILE": str(profile),
        "CODEX_HOME": str(profile / "codex"),
        "CLAUDE_CONFIG_DIR": str(profile / "claude"),
        "APPDATA": str(profile / "AppData/Roaming"),
        "LOCALAPPDATA": str(profile / "AppData/Local"),
        "TEMP": str(profile / "tmp"), "TMP": str(profile / "tmp"),
        "PATH": os.pathsep.join([
            str(Path(sys.executable).resolve().parent),
            str(Path(os.environ["SYSTEMROOT"]) / "System32"),
            r"C:\Program Files\Git\cmd",
        ]),
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    })
    return env


def prepare():
    if os.name != "nt" or sys.version_info < (3, 11):
        raise RuntimeError("Use Windows and Python 3.11 or later.")
    identity = subprocess.check_output(
        ["whoami.exe", "/user", "/fo", "csv", "/nh"], text=True
    ).strip()
    principal, sid = next(csv.reader([identity]))
    if "codexsandbox" in principal.casefold():
        raise RuntimeError(
            "Run preparation from your normal PowerShell session. "
            "A demo created by the Codex sandbox account is not accessible "
            "from your Windows account."
        )
    git = ["git", "-c", f"safe.directory={SOURCE.as_posix()}", "-C", str(SOURCE)]
    def git_output(*args):
        return subprocess.check_output([*git, *args], text=True).strip()
    if git_output("rev-parse", "HEAD") != SOURCE_COMMIT:
        raise RuntimeError("Source HEAD changed; review and update the demo input pin first.")
    if git_output("status", "--porcelain"):
        raise RuntimeError("Source has local changes; review them before preparing this pinned demo.")
    package = json.loads(PACKAGE.read_text(encoding="utf-8-sig"))
    # The original wheel lives in sandbox-owned Temp storage. Only use the
    # digest-checked copy staged beside this launcher for the human operator.
    wheel = SHARED_WHEEL.resolve(strict=True)
    if sha(wheel) != WHEEL_HASH or package["promotable"] is not False:
        raise RuntimeError("Candidate wheel identity or non-promotable designation differs.")
    if git_output("diff", "--name-only", package["package_source_commit"], "HEAD", "--",
                  "se_harness", "templates/repository/standard", "pyproject.toml",
                  "MANIFEST.in", "README.md", "LICENSE"):
        raise RuntimeError("Candidate wheel inputs changed; prepare a matching candidate wheel first.")
    for executable in HOSTS.values():
        if not executable.is_file():
            raise RuntimeError(f"Host executable moved: {executable}")

    base = Path(tempfile.mkdtemp(prefix="iar-instruction-demo-"))
    evidence = base / "evidence"
    evidence.mkdir()
    commands = []
    manifest = {
        "status": "preparing", "demo": str(base),
        "prepared_by": {"principal": principal, "sid": sid},
        "source": str(SOURCE), "source_commit": SOURCE_COMMIT,
        "wheel_source_commit": package["package_source_commit"],
        "wheel_sha256": WHEEL_HASH, "promotable": False,
        "host_executables": {k: str(v) for k, v in HOSTS.items()},
        "native_delivery": "not_assessed",
    }
    write_json(base / "demo.json", manifest)
    print(f"Creating {base}", flush=True)

    def run(label, argv, cwd=base):
        result = subprocess.run([str(a) for a in argv], cwd=cwd, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=180)
        (evidence / f"{label}.stdout").write_text(result.stdout, encoding="utf-8")
        (evidence / f"{label}.stderr").write_text(result.stderr, encoding="utf-8")
        commands.append({"label": label, "argv": [str(a) for a in argv],
                         "exit_code": result.returncode})
        write_json(evidence / "commands.json", commands)
        print(f"{label}: exit {result.returncode}", flush=True)
        if result.returncode:
            raise RuntimeError(f"{label} failed; read {evidence / (label + '.stderr')} and .stdout")
        return result.stdout

    inputs = base / "inputs"
    inputs.mkdir()
    selected_wheel = inputs / wheel.name
    shutil.copy2(wheel, selected_wheel)
    if sha(selected_wheel) != WHEEL_HASH:
        raise RuntimeError("Copied wheel digest differs.")
    run("venv", [sys.executable, "-m", "venv", base / "evaluator"])
    evaluator = base / "evaluator/Scripts/python.exe"
    run("install-wheel", [evaluator, "-I", "-m", "pip", "install",
        "--disable-pip-version-check", "--no-index", "--no-deps", selected_wheel])
    checker = [evaluator, "-I", "-m", "se_harness"]
    manifest["evaluator_version"] = run("evaluator-version", [*checker, "--version"]).strip()
    if "0.19.0" not in manifest["evaluator_version"]:
        raise RuntimeError("Expected candidate evaluator 0.19.0.")
    market = base / "marketplace"
    run("assemble-plugins", [sys.executable, "-B", SOURCE / "scripts/build_plugin_archives.py",
        "develop", "--repository", SOURCE, "--wheel", selected_wheel,
        "--output-directory", market / "packages"])
    for relative in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        destination = market / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / "release/plugin-marketplace" / relative, destination)

    roots = {}
    for host in HOSTS:
        project = base / "repositories" / host
        project.mkdir(parents=True)
        run(f"{host}-git-init", ["git", "init", project])
        owner_text = "# Demo repository\n\nThis repository contains no application code.\n"
        for name in ("AGENTS.md", "CLAUDE.md"):
            (project / name).write_text(owner_text, encoding="utf-8")
        project_name = f"Instruction delivery demo - {host}"
        run(f"{host}-init-preview", [*checker, "init", project, "--project-name", project_name, "--dry-run", "--json"])
        run(f"{host}-init", [*checker, "init", project, "--project-name", project_name, "--json"])
        plugin = market / "packages" / host / "verity-plane"
        ownership = [*checker, "skill-ownership", project, "--provider", "plugin", "--plugin-root", plugin]
        run(f"{host}-ownership-preview", [*ownership, "--json"])
        run(f"{host}-ownership-apply", [*ownership, "--apply", "--json"])
        run(f"{host}-doctor", [*checker, "doctor", project, "--json"])
        for name in ("AGENTS.md", "CLAUDE.md"):
            if (project / name).read_text(encoding="utf-8") != owner_text:
                raise RuntimeError(f"Owner file changed: {project / name}")
        root = project / "ENGINEERING_HARNESS.md"
        digest = hashlib.sha256(root.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        lock = json.loads((project / ".engineering-harness.lock").read_text(encoding="utf-8"))
        if lock["files"]["ENGINEERING_HARNESS.md"]["sha256"] != digest:
            raise RuntimeError(f"Root digest differs from lock: {root}")
        roots[host] = {"repository": str(project), "root_path": str(root),
                       "root_sha256": digest, "plugin": str(plugin)}
        env = child_env(base, host)
        for key in ("CODEX_HOME", "CLAUDE_CONFIG_DIR", "APPDATA", "LOCALAPPDATA", "TEMP"):
            Path(env[key]).mkdir(parents=True, exist_ok=True)
        Path(env["CODEX_HOME"], "config.toml").write_text(
            'cli_auth_credentials_store = "file"\ncheck_for_update_on_startup = false\n', encoding="utf-8")
    manifest.update(status="prepared", evaluator_python=str(evaluator), roots=roots)
    write_json(base / "demo.json", manifest)
    write_json(Path(__file__).with_name("prepared-demo.json"), manifest)
    print(json.dumps(manifest, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "codex", "claude"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
        return 0
    manifest_path = Path(__file__).with_name("prepared-demo.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["status"] != "prepared":
        raise RuntimeError("Prepare the demo first.")
    try:
        base = Path(manifest["demo"]).resolve(strict=True)
        # Fail here, with a recovery instruction, if this is a run created
        # by another Windows account or an expired temporary directory.
        (base / "demo.json").read_text(encoding="utf-8")
    except (PermissionError, FileNotFoundError) as error:
        raise RuntimeError(
            "The selected demo is inaccessible or no longer exists. "
            "Run this launcher with 'prepare' from your normal PowerShell "
            "session, then reload prepared-demo.json and $demoBase."
        ) from error
    argv = args.arguments
    if argv[:1] == ["--"]:
        argv = argv[1:]
    print(f"Profile: {base / 'profiles' / args.action}", flush=True)
    print(f"Repository: {manifest['roots'][args.action]['repository']}", flush=True)
    return subprocess.call([manifest["host_executables"][args.action], *argv],
        cwd=manifest["roots"][args.action]["repository"], env=child_env(base, args.action))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        raise SystemExit(1)

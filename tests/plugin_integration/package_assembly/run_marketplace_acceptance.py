"""Validate native marketplace installs and setup in disposable host profiles."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--marketplace", type=Path, required=True, help="accepted local distribution for content comparison")
parser.add_argument("--output", type=Path, required=True, help="new disposable directory outside the repository")
parser.add_argument("--codex", type=Path, required=True)
parser.add_argument("--claude", type=Path, required=True)
parser.add_argument("--expected-wheel-sha256", required=True)
parser.add_argument("--source", help="optional public Git marketplace source")
parser.add_argument("--ref", help="Git ref for the optional public source")
parser.add_argument("--install-only", action="store_true")
args = parser.parse_args()
market = args.marketplace.resolve(strict=True)
out = args.output.absolute()
repo = Path(__file__).resolve().parents[3]
if out.resolve().is_relative_to(repo) or out.resolve().is_relative_to(market):
    parser.error("choose a disposable output outside the source and marketplace")
if args.ref and not args.source:
    parser.error("--ref requires --source")
install_only = args.install_only
source = args.source or str(market)
out.mkdir(parents=True, exist_ok=False)
hosts = {"codex": args.codex.resolve(strict=True), "claude": args.claude.resolve(strict=True)}
commands = []
observations = []
expected_skills = {"setup", "change", "evidence", "harness-orient", "harness-operator-brief"}
for host, executable in hosts.items():
    profile = out / host / "profile"
    project = out / host / "project"
    project.mkdir(parents=True)
    env = {key: os.environ[key] for key in ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE") if key in os.environ}
    env.update(HOME=str(profile), USERPROFILE=str(profile), CODEX_HOME=str(profile / "codex"),
               CLAUDE_CONFIG_DIR=str(profile / "claude"), APPDATA=str(profile / "AppData/Roaming"),
               LOCALAPPDATA=str(profile / "AppData/Local"), TEMP=str(profile / "tmp"), TMP=str(profile / "tmp"),
               PATH=os.pathsep.join([str(Path(sys.executable).parent), os.path.join(os.environ["SYSTEMROOT"], "System32"), r"C:\Program Files\Git\cmd"]),
               NO_COLOR="1", CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
    for key in ("CODEX_HOME", "CLAUDE_CONFIG_DIR", "APPDATA", "LOCALAPPDATA", "TEMP"):
        Path(env[key]).mkdir(parents=True, exist_ok=True)
    (profile / "codex/config.toml").write_text('cli_auth_credentials_store = "file"\ncheck_for_update_on_startup = false\n', encoding="utf-8")

    def run(label, argv, expect=0):
        label = host + "-" + label
        argv = [str(arg) for arg in argv]
        result = subprocess.run(argv, cwd=project, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150)
        (out / (label + ".stdout")).write_text(result.stdout, encoding="utf-8")
        (out / (label + ".stderr")).write_text(result.stderr, encoding="utf-8")
        commands.append({"label": label, "argv": argv, "exit_code": result.returncode, "expect": expect})
        (out / "commands.json").write_text(json.dumps(commands, indent=2) + "\n", encoding="utf-8")
        print(label, result.returncode, flush=True)
        if expect == "missing-harness":
            assert result.returncode != 0 and not (project / ".engineering-harness.toml").exists(), result.stdout + result.stderr
            # Setup prints pip progress and its Python path before doctor JSON.
            _progress, marker, report = result.stdout.partition("\n{")
            assert marker, result.stdout + result.stderr
            doctor = json.loads("{" + report)
            assert any(c.get("name") == "ENGINEERING_HARNESS.md" and not c.get("passed") for c in doctor["checks"]), doctor
        else:
            assert result.returncode == expect, result.stdout + result.stderr
        return result.stdout

    version = run("version", [executable, "--version"]).strip()
    if host == "codex":
        run("marketplace-add", [executable, "plugin", "marketplace", "add", source, *(["--ref", args.ref] if args.ref else []), "--json"])
        installed = json.loads(run("install", [executable, "plugin", "add", "verity-plane@se-harness", "--json"]))
        plugin = Path(installed["installedPath"])
        discovered = run("native-discovery", [executable, "debug", "prompt-input", "Use verity-plane:setup to connect this disposable project."])
        assert "verity-plane:setup" in discovered
    else:
        run("marketplace-validate", [executable, "plugin", "validate", market])
        ref_separator = "#" if "://" in source or source.startswith("git@") else "@"
        claude_source = source + (ref_separator + args.ref if args.ref else "")
        run("marketplace-add", [executable, "plugin", "marketplace", "add", claude_source])
        run("install", [executable, "plugin", "install", "verity-plane@se-harness"])
        run("installed-list", [executable, "plugin", "list", "--json"])
        discovered = run("native-discovery", [executable, "plugin", "details", "verity-plane@se-harness"])
        manifests = list((profile / "claude/plugins/cache").rglob(".claude-plugin/plugin.json"))
        matches = [p.parent.parent for p in manifests if json.loads(p.read_text(encoding="utf-8"))["name"] == "verity-plane"]
        assert len(matches) == 1, matches
        plugin = matches[0]
    expected_plugin = market / "packages" / host / "verity-plane"
    compared = 0
    for expected_file in expected_plugin.rglob("*"):
        if expected_file.is_file():
            relative = expected_file.relative_to(expected_plugin)
            assert (plugin / relative).read_bytes() == expected_file.read_bytes(), (host, str(relative))
            compared += 1
    assert compared > 0
    actual_skills = {p.parent.name for p in (plugin / "skills").glob("*/SKILL.md")}
    assert actual_skills == expected_skills, actual_skills
    # Codex intentionally omits the briefing skill from implicit discovery.
    # Its packaged openai.yaml declares allow_implicit_invocation: false.
    for skill in expected_skills - ({"harness-operator-brief"} if host == "codex" else set()):
        assert skill in discovered, (host, skill)
    wheel = plugin / "packages/se_harness-0.18.0-py3-none-any.whl"
    assert hashlib.sha256(wheel.read_bytes()).hexdigest() == args.expected_wheel_sha256
    if install_only:
        observations.append({"host": host, "version": version, "route": "persistent native marketplace installation",
            "skills": sorted(actual_skills), "result": "passed", "installed_path": str(plugin), "compared_files": compared})
        continue
    data = profile / "plugin-data"
    python = data / "verity-plane/evaluator/Scripts/python.exe"
    run("setup-empty-project", [sys.executable, "-I", plugin / "scripts/setup.py", "--target", project,
        "--data-root", data, "--wheel", wheel], expect="missing-harness")
    checker = [python, "-I", "-m", "se_harness"]
    checker_version = run("checker-version", [*checker, "--version"]).strip()
    assert "0.18.0" in checker_version
    run("init-preview", [*checker, "init", project, "--project-name", "Marketplace acceptance", "--dry-run", "--json"])
    assert not (project / ".engineering-harness.toml").exists()
    run("init", [*checker, "init", project, "--project-name", "Marketplace acceptance", "--json"])
    run("provider-preview", [*checker, "skill-ownership", project, "--provider", "plugin", "--plugin-root", plugin, "--json"])
    run("provider", [*checker, "skill-ownership", project, "--provider", "plugin", "--plugin-root", plugin, "--apply", "--json"])
    run("doctor", [*checker, "doctor", project, "--json"])
    run("setup-repeat", [sys.executable, "-I", plugin / "scripts/setup.py", "--target", project,
        "--data-root", data, "--wheel", wheel])
    assert json.loads((project / ".engineering-harness.lock").read_text(encoding="utf-8"))["skill_ownership"] == {"provider": "plugin"}
    observations.append({"host": host, "version": version, "checker": checker_version, "route": "persistent native marketplace installation",
                         "skills": sorted(actual_skills), "result": "passed", "installed_path": str(plugin), "compared_files": compared})
    (out / "progress.json").write_text(json.dumps(observations, indent=2) + "\n", encoding="utf-8")
summary = {"result": "passed", "platform": sys.platform, "python": sys.version.split()[0], "hosts": observations,
           "install_only": install_only, "source": source, "ref": args.ref,
           "commands": len(commands), "limits": "Fresh Windows profiles; no model calls, official portal validation, or changes to real host settings. Public Git use is recorded by source/ref."}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))

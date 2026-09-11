"""Freeze specified observed records and raw inputs; never select new actions."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--observed", type=Path, required=True)
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--record", action="append", required=True)
    ap.add_argument("--asset", action="append", default=[])
    ap.add_argument("--secondary-repo", action="append", default=[])
    ns = ap.parse_args()
    observed, bundle = ns.observed.resolve(), ns.bundle.resolve()
    bundle.mkdir(parents=True, exist_ok=False)
    assets = {}

    def copy(source, rel, expected=None):
        if expected and sha(source) != expected:
            raise ValueError("Observed fixture asset mismatch: " + rel)
        target = bundle / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assets[rel] = sha(target)

    raw = json.loads((observed / "raw-assets-manifest.json").read_text())
    for rel, expected in raw.items():
        copy(observed / "raw-assets" / rel, "raw-assets/" + rel, expected)
    for name in ("oracle.md", "raw-scenarios.json", "raw-assets-manifest.json", "fixture_edit.py", "inspect_fixture.py"):
        copy(observed / name, name)
    for name in ns.asset:
        copy(observed / name, name)
    if "external-input-hashes.json" in ns.asset:
        for rel, expected in json.loads((observed / "external-input-hashes.json").read_text()).items():
            if sha(observed / rel) != expected:
                raise ValueError("Fixed external input hash mismatch: " + rel)

    def portable(arg, first=False):
        clean = arg.replace("\\", "/")
        if first and clean.endswith("/python.exe"):
            return "{python}"
        if clean == "C:/Users/mathi/Documents/Codex/2026-09-04/hel/work/se-harness-plugin-eval-016":
            return "{environment}"
        if clean.endswith("/se-harness-plugin-evidence-skill/plugins/verity-plane/common/scripts/session-context.py"):
            if "session-context.py" not in assets:
                copy(Path(arg), "session-context.py")
            return "{bundle}/session-context.py"
        if clean.startswith(observed.as_posix() + "/"):
            rest = clean[len(observed.as_posix()) + 1:]
            for repo_name in ns.secondary_repo:
                if rest == repo_name or rest.startswith(repo_name + "/"):
                    return "{output}/" + rest
            for repo_name in ("capture-repository", "lost-repository", "uncertain-repository", "dirty-repository", "handoff-repository", "release-repository", "unauthorized-repository", "unauthorized-release-repository", "no-context-repository", "corrected-repository", "partial-uncertain-repository"):
                if rest == repo_name or rest.startswith(repo_name + "/"):
                    return "{repo}" + rest[len(repo_name):]
            if rest.startswith("external-control-") or rest.startswith("external-cases/"):
                return "{external}/" + rest
            if rest == "trace":
                return "{trace}"
            return "{bundle}/" + rest
        return arg

    def input_values(value):
        if isinstance(value, str):
            return portable(value)
        if isinstance(value, dict):
            return {k: input_values(v) for k, v in value.items()}
        if isinstance(value, list):
            return [input_values(v) for v in value]
        return value
    records = []
    for label in ns.record:
        source = observed / "trace" / (label + ".json")
        value = json.loads(source.read_text())
        argv = [portable(arg, i == 0) for i, arg in enumerate(value["argv"])]
        stdin = value.get("stdin")
        if stdin:
            stdin = json.dumps(input_values(json.loads(stdin)))
        try:
            result = json.loads(value["stdout"])
        except ValueError:
            result = {}
        records.append({"label": label, "argv": argv, "expected_exit": value["exit_code"],
                        "expected_changed_paths": [p for p in value["changed_paths"] if not p.startswith(".git/")],
                        "expected_state": result.get("state"), "stdin": stdin,
                        "original_receipt_suppressed_after_exit": value.get("receipt_suppressed_after_exit", False),
                        "original_record": str(source), "original_sha256": sha(source)})
    manifest = {"classification": "Explicit command replay inputs from the independent Windows observer; no new model behavior or authority decisions",
                "assets": assets, "records": records}
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8", newline="\n")
    (bundle / ".gitattributes").write_text("* -text\n", encoding="utf8", newline="\n")
    print(json.dumps({"bundle": str(bundle), "records": len(records), "manifest_sha256": sha(bundle / "manifest.json")}))


if __name__ == "__main__":
    main()

"""Replay the observed intercepted project-tool calls and empty observation spans.

All effects belong to JSON simulation directories. No network tool exists in
this runner. The independent fixture's project_action.py supplies its existing
controls; this runner neither implements nor selects authority decisions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--replay-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    bundle, replay_root, output = (p.resolve() for p in (args.bundle, args.replay_root, args.output))
    manifest = json.loads((bundle / "manifest.json").read_text())
    for rel, expected in manifest["assets"].items():
        path = (bundle / rel).resolve()
        if not path.is_relative_to(bundle) or sha(path) != expected:
            raise ValueError("External fixture input mismatch: " + rel)
    output.mkdir(parents=True, exist_ok=False)
    original = json.loads((bundle / "candidate-inputs.json").read_text())
    native = json.loads((replay_root / "candidate-inputs-linux.json").read_text())
    identity_map = {original["candidate"]: native["candidate"], next(iter(original["evidence"].values())): next(iter(native["evidence"].values()))}

    def retarget(value):
        if isinstance(value, str):
            return identity_map.get(value, value)
        if isinstance(value, list):
            return [retarget(v) for v in value]
        if isinstance(value, dict):
            return {k: retarget(v) for k, v in value.items()}
        return value

    def fixture(folder):
        folder.mkdir(parents=True, exist_ok=False)
        for path in (bundle / "external-input-base").iterdir():
            if path.suffix == ".json":
                (folder / path.name).write_text(json.dumps(retarget(json.loads(path.read_text())), indent=2) + "\n", encoding="utf8", newline="\n")
            else:
                (folder / path.name).write_bytes(path.read_bytes())

    external = output / "fixtures"
    fixture(external / "external-control-calibration")
    fixture(external / "external-control-gate-failure")
    (external / "external-control-gate-failure/gates.json").write_text(json.dumps(retarget(json.loads((bundle / "external-control-gate-failure/gates.json").read_text())), indent=2) + "\n")
    cases = retarget(json.loads((bundle / "external-case-inputs.json").read_text()))
    for name, value in cases.items():
        target = external / "external-cases" / name
        fixture(target)
        (target / "gates.json").write_text(json.dumps(retarget(json.loads((bundle / "external-cases" / name / "gates.json").read_text())), indent=2) + "\n")
        (target / "request-and-decision.json").write_text(json.dumps(value, indent=2) + "\n")
    (output / "fixture-bindings.json").write_text(json.dumps({"classification": "Explicit native Linux C/evidence substitution in fixed synthetic requests and independent control data", "identity_map": identity_map, "cases": cases}, indent=2) + "\n")
    repo = replay_root / "release-repository"
    python = str(Path(sys.executable).absolute())
    bindings = {"{python}": python, "{repo}": str(repo), "{bundle}": str(bundle), "{external}": str(external)}
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PATH"] = str(Path(python).parent) + os.pathsep + env.get("PATH", "")
    env["GIT_CONFIG_NOSYSTEM"], env["GIT_CONFIG_GLOBAL"], env["GIT_OPTIONAL_LOCKS"] = "1", os.devnull, "0"
    summary = {"classification": "Command replay and fixed empty observation spans, not fresh model compliance or live external enforcement",
               "platform": platform.platform(), "python": sys.version, "runner_sha256": sha(Path(__file__)),
               "bundle_sha256": sha(bundle / "manifest.json"), "native_model_calls": 0, "decision_prompt_count": None,
               "commands": [], "negative_observations": []}
    traces = output / "trace"
    traces.mkdir()
    try:
        # These are already-selected empty sequences from the original observer,
        # not refusals newly chosen by code. Retain original paired record hashes.
        for original_before in sorted((bundle / "behavior").glob("*-before.json")):
            before_source = json.loads(original_before.read_text())
            name = before_source["case"]
            if name == "evd09-positive":
                continue
            original_after = original_before.with_name(name + "-after.json")
            after_source = json.loads(original_after.read_text())
            source_name = before_source["root"].replace("\\", "/").rsplit("/", 1)[-1]
            native_target = external / "external-cases" / name if name in cases else replay_root / source_name
            if not native_target.is_dir():
                raise ValueError("Native negative fixture missing: " + str(native_target))
            before, local_before = snapshot(native_target), snapshot(repo)
            after, local_after = snapshot(native_target), snapshot(repo)
            row = {"case": name, "classification": "Configured empty replay span only; the original Windows agent made the authority/readiness choice",
                   "before": before, "after": after, "local_before": local_before, "local_after": local_after,
                   "unchanged": before == after and local_before == local_after, "replayed_commands": [],
                   "original_before_sha256": sha(original_before), "original_after_sha256": sha(original_after),
                   "original_model_observation": after_source.get("model_observation"),
                   "original_approval_prompts": after_source.get("approval_prompts")}
            (output / (name + "-empty-replay.json")).write_text(json.dumps(row, indent=2) + "\n")
            summary["negative_observations"].append({"case": name, "unchanged": row["unchanged"]})

        for record in manifest["records"]:
            argv = []
            for arg in record["argv"]:
                for token, value in bindings.items():
                    arg = arg.replace(token, value)
                argv.append(identity_map.get(arg, arg))
            target = Path(argv[argv.index("--control-dir") + 1]) if "--control-dir" in argv else repo
            before, local_before, started = snapshot(target), snapshot(repo), time.time()
            invocation_before = len((target / "invocations.jsonl").read_text().splitlines()) if (target / "invocations.jsonl").exists() else None
            effects_before = len((target / "effects.jsonl").read_text().splitlines()) if (target / "effects.jsonl").exists() else None
            result = subprocess.run(argv, cwd=output, env=env, capture_output=True, timeout=60)
            after, local_after = snapshot(target), snapshot(repo)
            changed = [p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]
            row = {"label": record["label"], "argv": argv, "cwd": str(output), "exit_code": result.returncode,
                   "stdout": result.stdout.decode("utf8", "replace"), "stderr": result.stderr.decode("utf8", "replace"),
                   "before": before, "after": after, "local_before": local_before, "local_after": local_after,
                   "changed_paths": changed, "started_unix": started, "duration_seconds": time.time() - started,
                   "original_record_sha256": record["original_sha256"]}
            if invocation_before is not None:
                row["dispatch_delta"] = len((target / "invocations.jsonl").read_text().splitlines()) - invocation_before
                row["simulated_effect_delta"] = len((target / "effects.jsonl").read_text().splitlines()) - effects_before
            (traces / (record["label"] + ".json")).write_text(json.dumps(row, indent=2) + "\n", encoding="utf8", newline="\n")
            summary["commands"].append({k: row[k] for k in ("label", "argv", "exit_code", "changed_paths")})
            if result.returncode != record["expected_exit"] or changed != record["expected_changed_paths"] or local_before != local_after:
                raise AssertionError(record["label"] + ": replay effects differ from fixed observation")
            if record["expected_state"] is not None and json.loads(row["stdout"]).get("state") != record["expected_state"]:
                raise AssertionError("Integration gate state projection differs")
            if invocation_before is not None and (row["dispatch_delta"] != 1 or row["simulated_effect_delta"] != int("effects.jsonl" in record["expected_changed_paths"])):
                raise AssertionError("Actual intercepted invocation/effect counts differ")
            print(json.dumps({"label": record["label"], "exit_code": result.returncode, "changed_paths": changed}), flush=True)
        summary["passed"] = True
    except Exception as error:
        summary["passed"] = False
        summary["failure"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8", newline="\n")
        print(json.dumps({"passed": summary.get("passed"), "output": str(output)}))


if __name__ == "__main__":
    main()

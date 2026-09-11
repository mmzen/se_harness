"""Replay eight fixed observer calls; never select activation or render content."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_runner import sha, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    bundle = here / "fixtures/observer-final"
    manifest = json.loads((bundle / "manifest.json").read_text())
    for rel, digest in manifest["assets"].items():
        assert sha(bundle / rel) == digest, "Frozen observer input mismatch: " + rel
    settings = json.loads(args.settings.read_text())
    accepted = json.loads((bundle / "accepted-final-corrected-manifest-identity.json").read_text())
    for name, helper in settings["helpers"].items():
        core = Path(helper).parents[1]
        for path in core.rglob("*"):
            if path.is_file():
                key = core.name + "/" + path.relative_to(core).as_posix()
                assert sha(path) == accepted["raw_sha256"][key], "Final native core differs from observer fixed input"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(bundle, output / "frozen-observer-inputs")
    shutil.copyfile(__file__, output / "executed-replay_observer_cases.py")
    shutil.copyfile(args.settings, output / "settings.json")
    target = Path(settings["target"])
    baseline = snapshot(target)
    summary = {"classification": manifest["classification"], "manifest_sha256": sha(bundle / "manifest.json"),
               "original_model_receipt": "Retained separately; no Linux model receipt or activation decision fabricated", "cases": [], "passed": False}
    try:
        for case in manifest["cases"]:
            folder = output / case["label"]
            flags = [item.replace("{bundle}", str(bundle)) for item in case["flags"]]
            argv = [settings["python"], "-I", "-B", str(here / "boundary_runner.py"), "--settings", str(args.settings.resolve()), "--output", str(folder), *flags]
            try:
                result = subprocess.run(argv, capture_output=True, timeout=300)
            except (OSError, subprocess.TimeoutExpired) as exc:
                (output / (case["label"] + "-driver.json")).write_text(json.dumps({"argv": argv, "exit_code": None,
                    "execution_error": {"type": type(exc).__name__, "message": str(exc)},
                    "stdout": (getattr(exc, "stdout", None) or b"").decode("utf8", "replace"),
                    "stderr": (getattr(exc, "stderr", None) or b"").decode("utf8", "replace")}, indent=2) + "\n")
                raise
            (output / (case["label"] + "-driver.json")).write_text(json.dumps({"argv": argv, "exit_code": result.returncode,
                "stdout": result.stdout.decode("utf8", "replace"), "stderr": result.stderr.decode("utf8", "replace")}, indent=2) + "\n")
            observation = json.loads((folder / "observations.json").read_text())
            assert result.returncode == 0 and observation["passed"] and snapshot(target) == baseline
            row = {"case": case["label"], "passed": True, "actual_exit": observation["exit_code"], "original_record_sha256": case["original_record_sha256"],
                   "native_observations_sha256": sha(folder / "observations.json"), "native_stdout_sha256": sha(folder / "stdout.txt")}
            if case["label"] == "C05-final-04-helper":
                value = json.loads((folder / "stdout.txt").read_text())
                fixed = json.loads((bundle / "C05-unicode-request.json").read_text())
                assert value["source_sha256"] == fixed["source_sha256"] and value["protected_binding_count"] == 4
                row["source_sha256"] = value["source_sha256"]
                row["protected_binding_count"] = value["protected_binding_count"]
            summary["cases"].append(row)
            print(json.dumps(row), flush=True)
        summary["after_C07_fixed_empty_sequence"] = {"classification": "Original observer selected no checker or state query; empty replay span is not fresh model refusal", "replayed_commands": [], "before": snapshot(target), "after": snapshot(target)}
        summary["passed"] = True
    except BaseException as exc:
        summary["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main()

"""Replay one fixed observed batch in a new or verified existing Linux fixture.

The bundle supplies explicit argv and effects from actual Windows observations.
This recorder does not select authority or lifecycle transitions. It permits
incremental batches while the independent observer completes later cases.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import tomllib


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(repo):
    return {p.relative_to(repo).as_posix(): sha(p) for p in sorted(repo.rglob("*")) if p.is_file()}


def load_inputs(bundle):
    value = json.loads((bundle / "manifest.json").read_text())
    for rel, expected in value["assets"].items():
        path = (bundle / rel).resolve()
        if not path.is_relative_to(bundle) or sha(path) != expected:
            raise ValueError("Fixture input mismatch: " + rel)
    return value


def stable_output_path(path):
    # The observed dashboard generator names generated files by their contents.
    # Linux candidate/evidence bytes have different native hashes; preserve each
    # directory, extension and count while comparing these derived output names.
    if path.startswith("target/harness-dashboard/"):
        return re.sub(r"(?<=/)[0-9a-f]{64}(?=\.)", "{content-sha256}", path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--continue-existing", action="store_true")
    ap.add_argument("--batch", required=True)
    ap.add_argument("--repository", default="capture-repository")
    ap.add_argument("--clone-fixture", choices=("clean-candidate-input", "capture-repository"))
    ns = ap.parse_args()
    if not sys.flags.isolated:
        ap.error("Use the verified external evaluator Python with -I")
    bundle, output = ns.bundle.resolve(), ns.output.resolve()
    manifest = load_inputs(bundle)  # Reject corruption before any target creation.
    if output.is_relative_to(bundle) or bundle.is_relative_to(output):
        raise ValueError("Use a separate disposable output directory")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", ns.repository):
        raise ValueError("Use one simple disposable repository name")
    repo = output / ns.repository
    checkpoint = output / ("checkpoint.json" if ns.repository == "capture-repository" else "checkpoint-" + ns.repository + ".json")
    if ns.continue_existing:
        saved = json.loads(checkpoint.read_text())
        if saved["snapshot"] != snapshot(repo):
            raise ValueError("Prior disposable fixture changed outside recorded replay")
    elif ns.clone_fixture:
        origin = output / ns.clone_fixture
        if not output.is_dir() or not origin.is_dir() or origin == repo:
            raise ValueError("Select an existing native fixture source and a new target")
        before_copy = snapshot(origin)
        shutil.copytree(origin, repo)
        if snapshot(repo) != before_copy or snapshot(origin) != before_copy:
            raise ValueError("Native fixture copy changed input bytes")
        (output / (ns.batch + "-fixture-copy.json")).write_text(json.dumps({
            "classification": "Native Linux fixture reconstruction matching the observed Windows fixture copy; no model-directed action",
            "source": str(origin), "target": str(repo), "snapshot": before_copy}, indent=2) + "\n", encoding="utf8", newline="\n")
    else:
        output.mkdir(parents=True, exist_ok=False)
    traces = output / "trace"
    traces.mkdir(exist_ok=True)
    batch_file = output / (ns.batch + ".json")
    if batch_file.exists():
        raise FileExistsError(batch_file)
    python = str(Path(sys.executable).absolute())
    bindings = {"{python}": python, "{environment}": str(Path(python).parent.parent),
                "{repo}": str(repo), "{bundle}": str(bundle), "{trace}": str(traces)}
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PATH"] = str(Path(python).parent) + os.pathsep + env.get("PATH", "")
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_OPTIONAL_LOCKS"] = "0"
    summary = {"classification": manifest["classification"], "platform": platform.platform(), "python": sys.version,
               "evaluator_python": python, "runner_sha256": sha(Path(__file__)), "bundle_sha256": sha(bundle / "manifest.json"),
               "batch": ns.batch, "bindings": bindings, "commands": [], "fresh_model_behavior": False,
               "decision_prompt_count": None, "receipt_note": "Suppression belongs to the original Windows model observation; this runner replays actual commands and fixed readback choices."}
    try:
        for record in manifest["records"]:
            label = record["label"]
            path = traces / (label + ".json")
            if path.exists():
                raise FileExistsError(path)
            argv = []
            for arg in record["argv"]:
                for token, value in bindings.items():
                    arg = arg.replace(token, value)
                argv.append(arg)
            stdin = record["stdin"]
            if stdin:
                for token, value in bindings.items():
                    stdin = stdin.replace(token, value)
            if label == "evd07-capture":
                # A transparent new-platform fixture binding, fixed before the
                # selected replayed call. It grants no authority outside tests.
                original = json.loads((bundle / "candidate-inputs.json").read_text())
                observed = json.loads(json.loads((traces / "evd07-candidate-readback.json").read_text())["stdout"])
                candidate = observed["head"]
                if not re.fullmatch(r"[0-9a-f]{40}", candidate) or observed["status"]:
                    raise ValueError("Native candidate fixture must already be clean and committed")
                declaration = {**original, "candidate": candidate,
                               "evidence": {p: sha(repo / p) for p in original["evidence"]},
                               "original_windows_candidate": original["candidate"],
                               "original_windows_evidence": original["evidence"],
                               "classification": "Explicit synthetic fixture input binding to native Linux identities before replay; not an authority engine"}
                (output / "candidate-inputs-linux.json").write_text(json.dumps(declaration, indent=2) + "\n", encoding="utf8", newline="\n")
                baseline = output / "clean-candidate-input"
                shutil.copytree(repo, baseline)
                if snapshot(baseline) != snapshot(repo):
                    raise ValueError("Native clean candidate copy differs")
            if label == "evd02-rls-prepare":
                original = json.loads((bundle / "release-inputs.json").read_text())
                vrec = tomllib.loads((repo / "docs/engineering/evidence-demo/verification-records/VREC-EVD-001.md").read_text().split("+++", 2)[1])
                fixed = json.loads((output / "candidate-inputs-linux.json").read_text())
                if vrec["commit"] != fixed["candidate"] or vrec["status"] != "verified":
                    raise ValueError("Preverified native release fixture input does not match its fixed candidate")
                release_declaration = {**original, "candidate": fixed["candidate"],
                                       "input_sha256": {p: sha(repo / p) for p in original["input_sha256"]},
                                       "original_windows_candidate": original["candidate"],
                                       "original_windows_input_sha256": original["input_sha256"],
                                       "classification": "Explicit synthetic release fixture binding before replay; preexisting assurance is setup only"}
                (output / "release-inputs-linux.json").write_text(json.dumps(release_declaration, indent=2) + "\n", encoding="utf8", newline="\n")
            before, started = snapshot(repo), time.time()
            result = subprocess.run(argv, cwd=output, env=env, capture_output=True,
                                    input=stdin.encode("utf8") if stdin else None, timeout=60)
            after = snapshot(repo)
            changed = [p for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]
            row = {"label": label, "argv": argv, "stdin": stdin, "cwd": str(output), "exit_code": result.returncode,
                   "stdout": result.stdout.decode("utf8", "replace"), "stderr": result.stderr.decode("utf8", "replace"),
                   "before": before, "after": after, "changed_paths": changed, "started_unix": started,
                   "duration_seconds": time.time() - started, "original_record_sha256": record["original_sha256"]}
            path.write_text(json.dumps(row, indent=2) + "\n", encoding="utf8", newline="\n")
            summary["commands"].append({"label": label, "argv": argv, "exit_code": result.returncode})
            print(json.dumps({"label": label, "exit_code": result.returncode, "non_git_changes": [p for p in changed if not p.startswith(".git/")]}), flush=True)
            if result.returncode != record["expected_exit"]:
                raise AssertionError(label + ": unexpected process exit; retained actual outputs")
            actual_paths = sorted(stable_output_path(p) for p in changed if not p.startswith(".git/"))
            expected_paths = sorted(stable_output_path(p) for p in record["expected_changed_paths"])
            if actual_paths != expected_paths:
                raise AssertionError(label + ": unexpected non-Git mutation paths")
            if record["expected_state"] is not None and json.loads(row["stdout"]).get("state") != record["expected_state"]:
                raise AssertionError(label + ": unexpected lifecycle state projection")
            if label == "setup-15-context" and ("END VERIFIED GOVERNANCE" not in row["stdout"] or "complete context delivered" not in row["stdout"]):
                raise AssertionError("Actual context handler did not deliver complete verified governance")
            if label == "evd07-capture":
                data = tomllib.loads((repo / "docs/engineering/evidence-demo/verification-records/VREC-EVD-001.md").read_text().split("+++", 2)[1])
                if data["status"] != "ready" or data["commit"] != declaration["candidate"]:
                    raise AssertionError("Native VREC does not bind the fixed native candidate as ready")
            if label == "evd07-governance-readback":
                observed = json.loads(row["stdout"])
                prepared = observed["records"][0]["metadata"]
                fixed = json.loads((output / "candidate-inputs-linux.json").read_text())
                if prepared["commit"] != fixed["candidate"] or observed["head"] == fixed["candidate"] or prepared["status"] != "ready":
                    raise AssertionError("Governance commit must differ from the VREC's unchanged native candidate")
                (output / "governance-inputs-linux.json").write_text(json.dumps({"candidate": fixed["candidate"], "governance": observed["head"], "state": prepared["status"]}, indent=2) + "\n", encoding="utf8", newline="\n")
            if label == "evd02-rls-prepare":
                prepared = tomllib.loads((repo / "docs/engineering/evidence-demo/releases/RLS-EVD-001.md").read_text().split("+++", 2)[1])
                if prepared["status"] != "ready" or prepared["commit"] != release_declaration["candidate"]:
                    raise AssertionError("Ready release preparation changed its fixed native candidate")
        summary["passed"] = True
        checkpoint.write_text(json.dumps({"batch": ns.batch, "snapshot": snapshot(repo)}, indent=2) + "\n", encoding="utf8", newline="\n")
    except Exception as error:
        summary["passed"] = False
        summary["failure"] = {"type": type(error).__name__, "message": str(error)}
        raise
    finally:
        batch_file.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8", newline="\n")
        print(json.dumps({"passed": summary.get("passed"), "batch": str(batch_file)}))


if __name__ == "__main__":
    main()

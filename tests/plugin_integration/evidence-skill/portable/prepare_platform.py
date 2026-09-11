"""Record the provided Linux evaluator's identity and help, before trace replay.

This preparation performs no repository or lifecycle writes. It never reads the
candidate evidence skill and cannot choose an authority or lifecycle action.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

VERSION = "0.16.0"
PAYLOAD = "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c"
ARCHIVE = "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Use the independently supplied evaluator Python with -I")
    source, output = args.source.resolve(), args.output.resolve()
    if output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError("Keep disposable outputs separate from the source")
    output.mkdir(parents=True, exist_ok=False)
    python = str(Path(sys.executable).absolute())
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["PATH"] = str(Path(python).parent) + os.pathsep + env.get("PATH", "")
    records = []
    expected = {}
    for aid, folder in (("SPEC-PLG-011", "specifications"), ("VER-PLG-011", "verification")):
        path = source / "docs/engineering/plugin-integration" / folder / (aid + ".md")
        expected[aid] = sha(path)
        (output / path.name).write_bytes(path.read_bytes())
    commands = [("identity", ["identity", "--role", "released-evaluator", "--expected-version", VERSION,
                              "--expected-root", str(Path(python).parent.parent), "--evaluator-payload-sha256", PAYLOAD,
                              "--evaluator-wheel-sha256", ARCHIVE, "--checkout-root", str(source),
                              "--require-isolated-python", "--json"])]
    commands.extend((name + "-help", [name, "--help"]) for name in
                    ("init", "check", "evidence", "capture-verification", "prepare-release", "preflight", "transition"))
    for label, arguments in commands:
        argv = [python, "-I", "-B", "-m", "se_harness", *arguments]
        result = subprocess.run(argv, cwd=output, env=env, capture_output=True, timeout=60)
        row = {"label": label, "phase": "read-only platform preparation", "argv": argv, "cwd": str(output),
               "exit_code": result.returncode, "stdout": result.stdout.decode("utf8", "replace"),
               "stderr": result.stderr.decode("utf8", "replace")}
        records.append(row)
        (output / (label + ".json")).write_text(json.dumps(row, indent=2) + "\n", encoding="utf8", newline="\n")
        print(json.dumps({"label": label, "exit_code": result.returncode}), flush=True)
        if result.returncode:
            raise RuntimeError("Platform preparation failed; retained " + label)
    summary = {"classification": "Read-only platform preparation; no behavioral or lifecycle acceptance result",
               "platform": platform.platform(), "python": sys.version, "evaluator_python": python,
               "version": VERSION, "payload_sha256": PAYLOAD, "archive_sha256": ARCHIVE,
               "governing_artifact_hashes": expected, "runner_sha256": sha(Path(__file__)),
               "identity_and_help_passed": True, "candidate_skill_read": False, "commands": records}
    (output / "preparation.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf8", newline="\n")


if __name__ == "__main__":
    main()

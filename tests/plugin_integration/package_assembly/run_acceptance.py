"""Retain VER-PLG-001 C01-C08 observations using a separately selected real wheel.

Outputs are disposable fixtures. This does not create a verification record or
make an assurance decision. Pass the same input arguments as the assembly CLI,
plus --evidence-directory (new) and --scratch-directory (new).
"""
from copy import deepcopy
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from repository_tools import plugin_distribution as pkg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-directory", required=True, type=Path)
    parser.add_argument("--scratch-directory", required=True, type=Path)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--release-revision", required=True)
    parser.add_argument("--release-record", required=True)
    parser.add_argument("--expected-wheel-sha256", required=True)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--evaluator-python", required=True, type=Path)
    args = parser.parse_args()
    args.evidence_directory.mkdir(parents=True, exist_ok=False)
    args.scratch_directory.mkdir(parents=True, exist_ok=False)
    inputs = {key: getattr(args, key) for key in ("repository", "revision", "plan", "release_revision",
              "release_record", "expected_wheel_sha256", "wheel", "evaluator_python")}
    logs = []
    outcomes = []
    observations = []
    case_dir = None

    def capture(command, **kwargs):
        start = time.perf_counter()
        run = subprocess.run([str(v) for v in command], capture_output=True, **kwargs)
        logs.append({"argv": [str(v) for v in command], "exit_status": run.returncode,
                     "duration_seconds": round(time.perf_counter() - start, 3),
                     "stdout": run.stdout.decode("utf8", errors="replace"),
                     "stderr": run.stderr.decode("utf8", errors="replace")})
        return run

    def note(label, expected, observed):
        observations.append({"check": label, "expected": expected, "observed": observed})
        if expected != observed:
            raise AssertionError(f"{label}: expected {expected!r}, observed {observed!r}")

    def listing(path):
        return {p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(path.rglob("*")) if p.is_file()}

    def save(name, value):
        (case_dir / name).write_bytes(pkg.json_bytes(value))

    def invoke(action, output, ok=True, **changes):
        selected = {**inputs, **changes}
        command = [sys.executable, "-B", ROOT / "scripts/build_plugin_archives.py", action]
        for key, value in selected.items():
            command += ["--" + key.replace("_", "-"), value]
        run = capture(command + ["--output-directory", output])
        note(f"{action} accepted exit", ok, run.returncode == 0)
        data = json.loads(run.stdout if ok else run.stderr)
        note(f"{action} accepted flag", ok, data["accepted"])
        if not ok:
            observations.append({"rejection": data["error"], "output_listing": listing(output)})
        return data

    def git(repo, *command, **kwargs):
        run = capture(["git", "-c", "core.autocrlf=false", "-c", "core.longpaths=true", "-C", repo, *command], **kwargs)
        if run.returncode:
            raise RuntimeError("fixture Git operation failed; see stderr.txt")
        return run.stdout.decode().strip()

    variants = args.scratch_directory / "variants"
    # A disposable shared clone gives variants immutable commits without editing
    # the implementation checkout or checking out its large repository tree.
    setup = capture(["git", "clone", "--shared", "--no-checkout", "--quiet", args.repository, variants])
    if setup.returncode:
        raise RuntimeError("cannot create disposable fixture clone")
    git(variants, "config", "user.name", "Assembly acceptance fixture")
    git(variants, "config", "user.email", "fixture@example.invalid")
    setup_logs = list(logs)
    original_plan = json.loads(git(variants, "show", f"{args.revision}:{args.plan}"))

    def variant(plan, extra=None):
        git(variants, "read-tree", args.revision)
        blobs = {args.plan: pkg.json_bytes(plan), **(extra or {})}
        for path, raw in blobs.items():
            oid = git(variants, "hash-object", "-w", "--stdin", input=raw)
            git(variants, "update-index", "--add", "--cacheinfo", f"100644,{oid},{path}")
        tree = git(variants, "write-tree")
        revision = git(variants, "commit-tree", tree, "-p", args.revision, "-m", "Disposable negative assembly fixture")
        observations.append({"fixture_revision": revision, "plan": plan,
                             "extra_sources": {path: pkg.digest(raw) for path, raw in (extra or {}).items()}})
        return {"repository": variants, "revision": revision}

    first = args.scratch_directory / "valid"
    plugin = original_plan["name"]
    shared = next(path for path in original_plan["shared"] if path.startswith("scripts/"))

    def c01():
        # Separate invocation of the existing canonical function; do not take
        # the builder's inventory as the expected digest.
        code = ("from pathlib import Path; import sys; from se_harness.evaluator_identity import wheel_payload_sha256; "
                "print(wheel_payload_sha256(Path(sys.argv[1]), sys.argv[2]))")
        version = args.wheel.name.split("-")[1]
        raw_hash = hashlib.sha256(args.wheel.read_bytes()).hexdigest()
        note("independent archive SHA-256", args.expected_wheel_sha256, raw_hash)
        run = capture([args.evaluator_python, "-I", "-c", code, args.wheel, version], cwd=args.scratch_directory)
        note("independent canonical hash exit", 0, run.returncode)
        expected_payload = run.stdout.decode().strip()
        result = invoke("build", first)
        repeat = invoke("build", args.scratch_directory / "repeat")
        note("repeat archive digests", result["archives"], repeat["archives"])
        for host in pkg.HOSTS:
            folder = first / host / plugin
            inventory = json.loads((folder / pkg.INVENTORY).read_bytes())
            save(f"{host}-inventory.json", inventory)
            note(f"{host} exact wheel bytes", True, (folder / "packages" / args.wheel.name).read_bytes() == args.wheel.read_bytes())
            note(f"{host} payload hash", expected_payload, inventory["evaluator"]["payload_sha256"])
            note(f"{host} source revision", args.revision, inventory["source"]["revision"])
            for path, source in original_plan["shared"].items():
                source_raw = capture(["git", "-C", args.repository, "show", f"{args.revision}:{source}"]).stdout
                note(f"{host} source bytes: {path}", pkg.digest(source_raw), pkg.digest((folder / path).read_bytes()))
            note(f"{host} file listing", sorted(inventory["files"]), sorted(set(listing(folder)) - {pkg.INVENTORY}))
        save("independent-calculations.json", {"archive_sha256": raw_hash, "payload_sha256": expected_payload})

    def c02():
        wheel = args.scratch_directory / "bad-wheel" / args.wheel.name
        wheel.parent.mkdir()
        invoke("build", args.scratch_directory / "missing", ok=False, wheel=wheel)
        raw = bytearray(args.wheel.read_bytes())
        raw[len(raw) // 2] ^= 1
        wheel.write_bytes(raw)
        invoke("build", args.scratch_directory / "corrupt", ok=False, wheel=wheel)

    def c03():
        for index, (destination, raw) in enumerate([
            ("runtime/python.exe", b"MZfixture"), ("packages/candidate.whl", b"PK\x03\x04fixture"),
            ("assets/dependency.whl", b"PK\x03\x04dependency"), ("bin/run.py", b"# forbidden root")]):
            plan = deepcopy(original_plan)
            plan["shared"][destination] = "forbidden.txt"
            invoke("build", args.scratch_directory / f"forbidden-{index}", ok=False,
                   **variant(plan, {"forbidden.txt": raw}))

    def c04():
        plan = deepcopy(original_plan)
        plan["shared"][shared] = "missing-shared.py"
        invoke("build", args.scratch_directory / "missing-shared", ok=False, **variant(plan))
        target = first / "claude" / plugin / shared
        original = target.read_bytes()
        target.write_bytes(original + b"\n# divergent host\n")
        save("divergent-digests.json", {"expected": pkg.digest(original), "observed": pkg.digest(target.read_bytes())})
        invoke("check", first, ok=False)
        target.write_bytes(original)

    def c05():
        for host, own in pkg.HOSTS.items():
            paths = listing(first / host / plugin)
            save(f"{host}-listing.json", paths)
            note(f"{host} own manifest", True, own in paths)
            foreign = pkg.HOSTS["claude" if host == "codex" else "codex"]
            note(f"{host} foreign manifest absent", False, foreign in paths)
        plan = deepcopy(original_plan)
        plan["hosts"]["codex"][shared] = original_plan["shared"][shared]
        invoke("build", args.scratch_directory / "conflict", ok=False, **variant(plan))

    def c06():
        outside = args.scratch_directory / "outside"
        outside.mkdir()
        (outside / "sentinel.txt").write_bytes(b"unchanged sentinel")
        before = listing(outside)
        plan = deepcopy(original_plan)
        plan["shared"]["../../../outside/sentinel.txt"] = original_plan["shared"][shared]
        invoke("build", args.scratch_directory / "escaped", ok=False, **variant(plan))
        note("outside listing and bytes", before, listing(outside))
        save("sentinel-before-after.json", {"before": before, "after": listing(outside)})

    def c07():
        target = first / "codex" / plugin / pkg.INVENTORY
        original = target.read_bytes()
        changed = json.loads(original)
        del changed["files"][shared]
        target.write_bytes(pkg.json_bytes(changed))
        save("before-inventory.json", json.loads(original))
        save("omitted-inventory.json", changed)
        save("independent-listing.json", listing(target.parent))
        result = invoke("check", first, ok=False)
        note("rejection identifies omitted entry", True, shared in result["error"])
        target.write_bytes(original)

    def c08():
        assembly_inputs = {**inputs, "plan_path": inputs["plan"]}
        del assembly_inputs["plan"]
        assembly = pkg.prepare(**assembly_inputs)
        output = args.scratch_directory / "interrupted"
        write = pkg._write
        count = 0

        def interrupt(path, raw):
            nonlocal count
            if count == 1:
                raise OSError("injected interruption after first copied file")
            write(path, raw)
            count += 1

        try:
            with patch.object(pkg, "_write", interrupt):
                pkg.build(assembly, output)
        except OSError:
            (case_dir / "interruption-trace.txt").write_text(traceback.format_exc(), encoding="utf8")
        note("files copied before interruption", 1, count)
        before = listing(output)
        save("partial-listing.json", before)
        invoke("check", output, ok=False)
        invoke("build", output, ok=False)
        note("same-directory retry preserves partial bytes", before, listing(output))
        invoke("build", args.scratch_directory / "retry")
        invoke("check", args.scratch_directory / "retry")
        save("final-listing.json", listing(args.scratch_directory / "retry"))

    for number, case in enumerate([c01, c02, c03, c04, c05, c06, c07, c08], 1):
        case_dir = args.evidence_directory / f"C{number:02}"
        case_dir.mkdir()
        logs = list(setup_logs) if number == 1 else []
        observations = []
        conclusion = "pass"
        try:
            case()
        except Exception:
            conclusion = "fail"
            (case_dir / "failure-trace.txt").write_text(traceback.format_exc(), encoding="utf8")
        save("actions.txt", {"runner_argv": sys.argv, "case": case.__name__, "commands": logs})
        for field in ("stdout", "stderr"):
            (case_dir / f"{field}.txt").write_text("\n".join(log[field] for log in logs), encoding="utf8")
        save("observations.json", {"conclusion": conclusion, "checks": observations,
             "source_revision": args.revision, "platform": platform.platform(), "python": sys.version,
             "source_evidence_paths": ["actions.txt", "stdout.txt", "stderr.txt"],
             "exit_statuses": [log["exit_status"] for log in logs]})
        outcomes.append({"case": case_dir.name, "conclusion": conclusion})
    summary = {"outcomes": outcomes, "platform": platform.platform(), "python": sys.version,
               "unavailable_platforms": [name for name in ["Windows", "Linux", "Darwin"] if name != platform.system()],
               "claim": "Assembly fixture observations only; no formal assurance, native host support or publication."}
    (args.evidence_directory / "case-summary.json").write_bytes(pkg.json_bytes(summary))
    print(json.dumps(summary, indent=2))
    return 0 if all(row["conclusion"] == "pass" for row in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())

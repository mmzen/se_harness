"""Audit fixed helper evidence and retain it with short flat filenames."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from boundary_runner import sha, snapshot


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windows", type=Path, required=True)
    parser.add_argument("--windows-failed", type=Path, required=True)
    parser.add_argument("--linux", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    roots = {"windows": args.windows.resolve(), "windows-setup-failed": args.windows_failed.resolve(), "linux": args.linux.resolve()}
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {"passed": False, "classification": "Actual fixed helper and calibrated boundary tests; independent model instruction observations are separate", "platforms": {}}
    selected_helpers = ["C01-selected", "C02-preflight", "C03-version", "C03-root", "C03-payload", "C06-valid", "C06-wrong-digest", "C06-reversed-spans", "C06-altered-output"]
    for platform_name in ("windows", "linux"):
        root = roots[platform_name]
        settings = load(root / "final-inputs/settings.json")
        assert snapshot(root / "repository") == load(root / "setup-final-snapshot.json"), "Native target changed after setup"
        selected = []
        for name in selected_helpers:
            group = "matrix-final" if platform_name == "linux" else "brief-final" if name.startswith("C06") else "matrix1"
            folder = root / group / name
            row = load(folder / "observations.json")
            assert row["passed"] and row["before"] == row["after"] and not row["denied_events"]
            source_map = load(folder / "executed-source/source-map.json")
            for file, declaration in source_map.items():
                assert sha(folder / "executed-source" / file) == declaration["sha256"]
            result = load(folder / "stdout.txt")
            item = {"case": name, "group": group, "expected_exit": row["expected_exit"], "observed_exit": row["exit_code"],
                    "expected_code": row["expected_code"], "observed_codes": row["observed_codes"], "changed_paths": [], "denied_events": [],
                    "observation_sha256": sha(folder / "observations.json"), "source_hashes": row["source_sha256"]}
            if name.startswith(("C01", "C02", "C03")):
                receipt = result["execution_receipt"]
                item["operations"] = receipt["execution"]["operations"]
                assert receipt["effects"]["changed_paths"] == receipt["execution"]["worker_results"] == []
                if name.startswith(("C01", "C02")):
                    assert "engine" in row["boundary_entries"] and "evaluator" in row["boundary_entries"]
            selected.append(item)
        calibrations = []
        for group in (("matrix1", "brief-final") if platform_name == "windows" else ("matrix-final",)):
            assert load(root / group / "summary.json")["passed"]
            for category in ("write", "network", "credential", "spawn", "lifecycle"):
                folder = root / group / ("C08-calibrate-" + category)
                row = load(folder / "observations.json")
                assert row["passed"] and row["before"] == row["after"]
                assert len(row["denied_events"]) == 1 and row["denied_events"][0]["category"] == category
                calibrations.append({"group": group, "category": category, "denied": True, "observations_sha256": sha(folder / "observations.json")})
        report["platforms"][platform_name] = {"platform": settings["platform"], "python_version": settings["python_version"], "evaluator_version": "0.16.0", "helper_cases": selected, "calibrations": calibrations, "target_matches_initial_snapshot": True}
    report["passed"] = True
    report["scope"] = {"covered": ["C01", "C02", "C03", "C06", "C08 helper boundary"], "separate_independent_observer": ["C04", "C05", "C07", "C08 instruction surfaces"],
                       "fresh_model_decisions_in_helper_runner": False, "production_sandbox_claim": False, "native_host_qualification": False}
    report["preserved_defects"] = ["Pre-run altered-output fixture initially changed unprotected prose; corrected protected identifier before any helper test", "Windows setup identity omitted checkout boundary", "Windows audit argv was a string rather than list", "Fixed selected-check allowlist included an unsupported0.16 result-schema option", "Linux audit cwd was PathLike and needed explicit serialization"]
    report["final_brief_skill_sha256"] = "3e39fc61f7dfb41ca2b54d2c78f03ef2a7f3391402492dcd3ccef39a50a4af51"
    report["orientation_skill_sha256"] = "7f084f0c5f92856c7112daaad9b9013b55c00880a6094da7c2163ecd20c18abf"
    report["limits"] = ["CPython-visible audited operations only; no malicious native-extension containment", "Git internals are bounded by exact read-only argv and isolated configuration plus independent full target hashes", "Lifecycle canary stops at the boundary before evaluator module dispatch", "No real credential, network, lifecycle decision, release or external action exercised"]
    (output / "audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    mappings = []
    blobs = {}
    excluded = {"repository", "wrong-payload-repository", "isolated-home", "__pycache__", ".git"}
    for group, root in roots.items():
        for source in sorted(root.rglob("*")):
            if not source.is_file() or excluded.intersection(source.relative_to(root).parts):
                continue
            digest = sha(source)
            if digest not in blobs:
                suffix = source.suffix if source.suffix in {".json", ".jsonl", ".txt", ".md", ".py"} else ".txt"
                name = "f" + str(len(blobs) + 1).zfill(5) + suffix
                shutil.copyfile(source, output / name)
                assert sha(output / name) == digest
                blobs[digest] = name
            mappings.append({"group": group, "source": str(source), "relative": source.relative_to(root).as_posix(), "retained": blobs[digest], "sha256": digest, "bytes": source.stat().st_size})
    here = Path(__file__).resolve().parent
    for source in (here / "README.md", here / "fixtures/oracle.md", Path(__file__).resolve()):
        digest = sha(source)
        name = "f" + str(len(blobs) + 1).zfill(5) + source.suffix
        if digest not in blobs:
            shutil.copyfile(source, output / name)
            blobs[digest] = name
        mappings.append({"group": "final-source", "source": str(source), "relative": source.relative_to(here).as_posix(), "retained": blobs[digest], "sha256": digest, "bytes": source.stat().st_size})
    (output / "source-path-map.json").write_text(json.dumps({"classification": "Flat byte-preserving evidence retention; nested source paths are metadata only", "files": mappings}, indent=2) + "\n", encoding="utf8")
    text = """# WO-PLG-012 actual helper acceptance

All final selected C01/C02/C03/C06 helper fixtures passed on Windows and Linux,
using unchanged packaged helpers/contracts and real external released0.16.0.
The audit covers nine selected helper cases per OS, with ten Windows and five
Linux calibrated denied-effect probes supporting the executed worker versions.
C04/C05/C07 model activation/rendering/refusal observations are separate.

Orientation completed with actual version, identity, doctor, validation,
inspection and selected projection operations. Only the requested C02 run added
preflight. Wrong version stopped after version (AEXORI013); wrong root/payload
stopped after failed actual identity, before later operations. All receipts stayed
inline, with empty changed_paths and worker_results. Independent snapshots include
all target, ignored and Git files and remain identical before/after every case.

Brief helper calibration preserved three fixed source spans. Wrong source hash,
reversed spans and altered protected bytes returned TCM006, TCM007 and TCM010.
This helper validation does not claim independent briefing activation or rendering.

C08's real denied write/socket/synthetic-credential/spawn canaries and forbidden
evaluator entry all failed at the calibrated test boundary before effects. Real
allowed evaluator/engine/Git logs are nonempty; helper-case denied logs are empty.
The unchanged evaluator scripts execute through the propagated CPython wrapper,
with actual stdout/status and identity. No evaluator output was mocked.

This is a CPython test boundary, not a production sandbox or universal external
enforcement. Native extensions and fixed Git internals are outside audit coverage;
Git's exact read-only vectors, isolated config and complete hashes bound that
surface. No live network, real credentials, lifecycle action, assurance/release
decision, or native host-hook activation was exercised. The lifecycle canary
demonstrates pre-dispatch rejection, not applied lifecycle legality.

The first Windows matrix used intermediate brief SKILL6bb140; final3e39fc
brief-only cases and calibration were repeated. Orientation/core/helpers were
unchanged, so its passing evidence was retained. Linux's final matrix uses the
final core throughout. Source/runner bytes are preserved before every invocation,
including original failures, and must not be relabeled as later source versions.

Original setup/boundary defects remain preserved: missing checkout identity
argument, Windows string-form audit argv, unsupported expected check flag, and
Linux PathLike logger serialization. The pre-run protected-output fixture error
and correction are also retained. None modified product helper or evaluator code.

`audit.json` maps final cases to their original groups and expected/observed facts.
`source-path-map.json` maps original evidence/source paths to short flat retained
files with exact SHA256. Duplicate identical byte streams share a retained file.
Disposable repositories, Git directories and runtime environments are excluded;
their complete original before/after hashes remain inside observations. Keep this
folder flat when copying it into acceptance to avoid long Windows checkout paths.
"""
    (output / "REPORT.md").write_text(text, encoding="utf8")
    inventory = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(output.iterdir()) if p.is_file()}
    (output / "inventory.json").write_text(json.dumps({"payload_files": len(inventory), "mapped_source_files": len(mappings), "files": inventory}, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"passed": True, "output": str(output), "payload_files": len(inventory), "mapped_source_files": len(mappings), "inventory_sha256": sha(output / "inventory.json")}))


if __name__ == "__main__":
    main()

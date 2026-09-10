"""Audit retained fixed command replay, without executing candidate actions."""
import argparse
import hashlib
import json
from pathlib import Path
import tomllib


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def artifact(repo, category, ident):
    path = repo / "docs/engineering/evidence-demo" / category / (ident + ".md")
    return tomllib.loads(path.read_text().split("+++", 2)[1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--external", type=Path, required=True)
    args = parser.parse_args()
    output, external = args.output.resolve(), args.external.resolve()
    here = Path(__file__).resolve().parent
    provenance = here / "fixtures/provenance"
    for rel, expected in read(provenance / "sha256.json").items():
        assert sha(provenance / rel) == expected, "Independent provenance changed: " + rel
    groups = read(provenance / "trace-groups.json")["groups"]
    original_labels = [label for group in groups.values() for label in group]
    batches = ("setup-original", "capture", "governance", "lost", "uncertain", "dirty", "handoff", "release", "unauthorized", "unauthorized-release", "no-context", "corrected", "partial")
    records, batch_hashes = {}, {}
    for name in batches:
        batch = read(output / (name + ".json"))
        assert batch["passed"] is True, name
        batch_hashes[name] = sha(output / (name + ".json"))
        for command in batch["commands"]:
            label = command["label"]
            assert label not in records, "Duplicate replay label"
            records[label] = read(output / "trace" / (label + ".json"))
    external_summary = read(external / "summary.json")
    assert external_summary["passed"] is True
    for command in external_summary["commands"]:
        label = command["label"]
        assert label not in records
        records[label] = read(external / "trace" / (label + ".json"))
    assert sorted(records) == sorted(original_labels) and len(records) == 82
    assert all(row["unchanged"] for row in external_summary["negative_observations"])
    assert len(external_summary["negative_observations"]) == 17
    for bundle in (here / "fixtures").iterdir():
        if not (bundle / "manifest.json").exists():
            continue
        manifest = read(bundle / "manifest.json")
        for rel, digest in manifest["assets"].items():
            assert sha(bundle / rel) == digest, "Frozen input changed: " + str(bundle / rel)
        for expected in manifest["records"]:
            actual = records[expected["label"]]
            assert actual["original_record_sha256"] == expected["original_sha256"]
            assert actual["exit_code"] == expected["expected_exit"]
    fixed = read(output / "candidate-inputs-linux.json")
    governance = read(output / "governance-inputs-linux.json")
    assert governance["candidate"] == fixed["candidate"] != governance["governance"]
    clean = output / "clean-candidate-input"
    for name in ("capture-repository", "lost-repository", "uncertain-repository", "corrected-repository", "partial-uncertain-repository"):
        repo = output / name
        record = artifact(repo, "verification-records", "VREC-EVD-001")
        assert record["status"] == "ready" and record["commit"] == fixed["candidate"]
        for rel in ("docs/engineering/evidence-demo/work-orders/WO-EVD-001.md", "src/feature.py", ".engineering-harness.lock"):
            assert sha(repo / rel) == sha(clean / rel), name + ": fixture input changed"
    release = output / "release-repository"
    assert artifact(release, "verification-records", "VREC-EVD-001")["status"] == "verified"
    rls = artifact(release, "releases", "RLS-EVD-001")
    assert rls["status"] == "ready" and rls["commit"] == fixed["candidate"]
    partial = output / "partial-uncertain-repository"
    assert not (partial / "docs/engineering/evidence-demo/evidence/VREC-EVD-001-evaluator.json").exists()
    captures = ("evd07-capture", "evd03-lost-capture", "evd03-uncertain-capture", "corrected-capture")
    footprint = {}
    for label in captures:
        paths = records[label]["changed_paths"]
        exported = [p for p in paths if p.startswith("target/harness-dashboard/")]
        assert len(exported) == 14
        footprint[label] = exported
    project_rows = [row for row in records.values() if "dispatch_delta" in row]
    assert len(project_rows) == 8
    assert sum(row["dispatch_delta"] for row in project_rows) == 8
    assert sum(row["simulated_effect_delta"] for row in project_rows) == 3
    assert records["evd09-project-tool"]["dispatch_delta"] == records["evd09-project-tool"]["simulated_effect_delta"] == 1
    integrity = read(output / "input-integrity/result.json")
    assert integrity["passed"] is True and integrity["target_created"] is False
    result = {
        "passed": True, "classification": "Fixed Linux command replay only; independent Windows model observations are separate",
        "record_count": len(records), "batch_hashes": batch_hashes, "external_summary_sha256": sha(external / "summary.json"),
        "candidate_C": fixed["candidate"], "governance_G": governance["governance"],
        "evidence_sha256": fixed["evidence"], "ready_capture_vrec": True, "ready_release_record": True,
        "preverified_release_input": "Synthetic fixture setup, not an exercised assurance decision",
        "negative_empty_replay_spans": 17, "fresh_model_behavior": False, "native_model_approval_prompt_count": None,
        "recorded_nonzero_exits": {label: row["exit_code"] for label, row in records.items() if row["exit_code"]},
        "external_fixed_tool_invocations": 8, "external_simulated_effects": 3, "external_behavioral_positive_replayed_effects": 1,
        "original_capture_oracle": "Failed record/evaluator-only footprint expectation retained in independent provenance; not overridden by command-replay matching",
        "capture_dashboard_outputs": footprint, "injected_partial_vrec_without_sidecar": True,
        "input_integrity_rejected_before_target_creation": True,
        "limits": ["No fresh Linux model authority selection", "No native host activation or live CI", "External effects are local JSON simulation only", "No in-flight crash or atomicity qualification"],
    }
    (output / "audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf8", newline="\n")
    print(json.dumps({"passed": True, "records": len(records), "audit": str(output / "audit.json")}))


if __name__ == "__main__":
    main()

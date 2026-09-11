"""Assess retained native receipts against independently retained source bytes."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(value):
    return hashlib.sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    prepared = Path(__file__).parent / "prepared-inputs"
    # The shared contract emits UTF-8 with LF. Reconstruct those bytes even
    # when a Windows Git checkout materializes retained text with CRLF.
    gate = (prepared / "expected-gate.txt").read_text(encoding="utf8").encode("utf8")
    router = (prepared / "expected-router.md").read_text(encoding="utf8").encode("utf8")
    body = b"AGENTS.md managed gate:\n" + gate + b"\n\nENGINEERING_HARNESS.md:\n" + router
    marker = b"END VERIFIED GOVERNANCE " + sha(body).encode() + b"; complete context delivered.\n"
    transcript = json.loads((args.run / "transcript.json").read_text(encoding="utf8"))
    observation = json.loads((args.run / "observations.json").read_text(encoding="utf8"))
    selection = json.loads((prepared / "selection.json").read_text(encoding="utf8"))["binding"]
    expected_argv = [str(Path(selection["environment"]) / "Scripts/python.exe"), "-I", "-B",
        str(Path(observation["loaded_payload"]["root"]) / "scripts/session-context.py"),
        "--repo", selection["repo"], "--environment", selection["environment"],
        "--version", "0.16.0", "--payload-sha256", "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
        "--archive-sha256", "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
        "--host", "codex", "--context-limit", "16000", "--read-limit", "0"]
    dispatch = [json.loads(line) for line in (args.run / "dispatch.jsonl").read_text(encoding="utf8").splitlines()]
    prepared_contexts = [json.loads(row["stdout"])["hookSpecificOutput"]["additionalContext"]
                         for row in dispatch if row.get("status") == "handler-output-returned"]
    receipts = []
    for index, row in enumerate(transcript):
        message = row.get("message", {})
        if "received_monotonic" not in row or message.get("method") != "hook/completed":
            continue
        run = message["params"]["run"]
        if run["eventName"] != "sessionStart":
            continue
        contexts = [entry["text"] for entry in run["entries"] if entry["kind"] == "context"]
        for context_index, context in enumerate(contexts):
            raw = context.encode("utf8")
            path = f"host-context-{len(receipts) + 1:02}.txt"
            (args.run / path).write_bytes(raw)
            receipts.append({"transcript_index": index, "context_index": context_index,
                "source_path": run["sourcePath"], "status": run["status"],
                "received_monotonic": row["received_monotonic"], "duration_ms": run["durationMs"],
                "context_path": path, "context_sha256": sha(raw), "context_bytes": len(raw),
                "exact_body_present": body in raw, "matching_end_marker": raw.endswith(marker),
                "exact_dispatch_context": context in prepared_contexts})
    result = {"scope": "Retained native SessionStart context receipts; no new host invocation or authority decision.",
        "body_sha256": sha(body), "gate_sha256": sha(gate), "router_sha256": sha(router),
        "gate_bytes": len(gate), "router_bytes": len(router), "body_bytes": len(body),
        "receipts": receipts, "dispatch_count": len(dispatch), "expected_argv": expected_argv,
        "observed_argv": [row.get("argv") for row in dispatch],
        "exact_argv": bool(dispatch) and all(row.get("argv") == expected_argv for row in dispatch),
        "cleanup": observation["cleanup"], "targets_unchanged": observation["before"] == observation["after"],
        "observer_stopped": observation.get("observer_stopped"),
        "unexpected_server_requests": [row for row in transcript if "received_monotonic" in row
            and "id" in row.get("message", {}) and "method" in row.get("message", {})]}
    result["complete_native_context_observed"] = bool(receipts) and all(
        row["status"] == "completed" and row["exact_body_present"] and row["matching_end_marker"]
        and row["exact_dispatch_context"] for row in receipts)
    (args.run / "context-assessment.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

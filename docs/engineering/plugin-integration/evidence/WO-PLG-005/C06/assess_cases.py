"""Recompute native argument and unsupported-tool observations; no host calls."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def hooks(trace):
    return [(i, row["message"]["params"]) for i, row in enumerate(trace)
            if "received_monotonic" in row and row["message"].get("method") == "hook/completed"
            and row["message"]["params"]["run"]["eventName"] == "preToolUse"]


def save(folder, result):
    result["sources"] = {name: sha((folder / name).read_bytes())
                         for name in ("actions.txt", "observations.json", "transcript.json", "dispatch.jsonl")}
    (folder / "native-assessment.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n")
    print(json.dumps({"case": folder.name, "conclusion": result["conclusion"]}))


def main():
    folder = ROOT / "unicode-edit-01"
    observed, trace = read(folder / "observations.json"), read(folder / "transcript.json")
    planned = observed["plan"]
    expected = "café quoted ' target.txt"
    before = "initial fixture target\r\n".encode()
    after = b"WO-PLG-005 Unicode and quoted path edit\n"
    receipts = hooks(trace)
    proof = read(folder / "approval-prepared.json")
    messages = [(i, row["message"]) for i, row in enumerate(trace)]
    completions = [(i, msg["params"]) for i, msg in messages if msg.get("method") == "item/completed"
                   and msg["params"].get("item", {}).get("type") == "fileChange"]
    changes = proof["changes"]
    target_exact = (len(changes) == 1 and Path(changes[0]["path"]).name == expected
                    and changes[0]["kind"] == {"move_path": None, "type": "update"})
    ordered = (len(receipts) == len(completions) == 1
               and receipts[0][0] < completions[0][0]
               and receipts[0][1]["run"]["status"] == "completed"
               and completions[0][1]["item"]["status"] == "completed"
               and receipts[0][1]["run"]["id"].endswith(":" + completions[0][1]["item"]["id"]))
    dispatch = [json.loads(line) for line in (folder / "dispatch.jsonl").read_text(encoding="utf8").splitlines() if line.strip()]
    tool_rows = [row for row in dispatch if "check-tool-action.py" in row.get("argv", [""])[3]]
    checks = [check for row in tool_rows for line in row["stderr"].splitlines()
              for check in (json.loads(line).get("checks", []) if line.strip() else []) if "--changed-path" in check.get("argv", [])]
    mapped = len(checks) == 1 and checks[0]["argv"][checks[0]["argv"].index("--changed-path") + 1] == expected
    passed = (observed.get("observation_complete") is True and observed.get("acceptance_sent") is True
              and planned == {"schema": "verity-one-edit-v1", "target": expected,
                              "before_utf8": before.decode(), "after_utf8": after.decode()}
              and proof["before_sha256"] == sha(before) and proof["after_sha256"] == sha(after)
              and observed["target_actual_sha256"] == sha(after) and observed["changed_sentinels"] == [expected]
              and observed["cleanup"].get("active_processes") == 0 and target_exact and ordered and mapped)
    save(folder, {"conclusion": "pass" if passed else "fail", "exact_unicode_and_quote_target": target_exact,
                  "mapped_changed_path_exact": mapped, "hook_before_completed_effect": ordered,
                  "exact_planned_after_sha256": sha(after), "actual_after_sha256": observed["target_actual_sha256"],
                  "qualification": "Observed supported path mapping only; no general tool coverage claim."})

    folder = ROOT / "unsupported-noop-01"
    observed, trace = read(folder / "observations.json"), read(folder / "transcript.json")
    receipts = hooks(trace)
    request = observed.get("stop_detail", {})
    warnings = [entry["text"] for _, params in receipts for entry in params["run"].get("entries", [])
                if entry.get("kind") == "warning"]
    expected_warning = "UNENFORCED COVERAGE GAP: this tool has no Verity Plane evaluator mapping. No successful governance check is claimed. Ordinary host permissions and already-authorized setup remain available."
    actual_request = request.get("params", {})
    correlated = (len(receipts) == 1 and request.get("method") == "item/commandExecution/requestApproval"
                  and receipts[0][1]["run"]["id"].endswith(":" + actual_request.get("itemId", ""))
                  and receipts[0][1]["threadId"] == actual_request.get("threadId")
                  and receipts[0][1]["turnId"] == actual_request.get("turnId"))
    sent_approvals = [row for row in trace if "sent_monotonic" in row and "result" in row["message"]]
    completed_commands = [row for row in trace if row["message"].get("method") == "item/completed"
                          and row["message"]["params"].get("item", {}).get("type") == "commandExecution"]
    dispatch = [json.loads(line) for line in (folder / "dispatch.jsonl").read_text(encoding="utf8").splitlines() if line.strip()]
    no_tool_dispatch = all("session-context.py" in row.get("argv", [""])[3] for row in dispatch)
    passed = (correlated and warnings == [expected_warning] and no_tool_dispatch
              and not sent_approvals and not completed_commands
              and observed["before"] == observed["after"] and observed["cleanup"].get("active_processes") == 0)
    save(folder, {"conclusion": "pass" if passed else "fail", "coverage_warning": warnings,
                  "correlated_native_tool_attempt": correlated, "no_evaluator_tool_success_claim": no_tool_dispatch,
                  "command_approval_answered": bool(sent_approvals), "command_completed": bool(completed_commands),
                  "targets_unchanged": observed["before"] == observed["after"],
                  "limits": "The unsupported command reached the native hook and emitted its coverage gap. The observer stopped at ordinary command approval without answering it. This proves coverage reporting, not successful command execution or enforcement. The earlier update_plan attempt had no available tool and is not counted."})


if __name__ == "__main__":
    main()

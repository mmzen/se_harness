"""Package already observed inputs/argv. Does not run or choose lifecycle actions."""
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
    ns = ap.parse_args()
    source = ns.observed.resolve()
    dest = Path(__file__).resolve().parent / "observed"
    dest.mkdir(exist_ok=False)
    fixed = json.loads((source / "fixed-inputs.json").read_text())
    groups = json.loads((source / "trace-groups.json").read_text())
    assets = {}

    def copy(src, rel, expected=None):
        if expected and sha(src) != expected:
            raise ValueError("Independent fixture input mismatch: " + str(src))
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        assets[rel] = sha(target)

    for rel, digest in fixed["raw_artifact_sha256"].items():
        copy(source / "raw-repository" / rel, "raw/" + rel, digest)
    for path in (source / "raw-repository/src").iterdir():
        copy(path, "raw/src/" + path.name)
    package = json.loads((source / "package-inputs/request.json").read_text())
    for name, digest in package["raw_paths"].items():
        copy(source / "package-inputs" / name, "package-inputs/" + name, digest)
    for name in ("oracle.md", "fixed-inputs.json", "trace-groups.json"):
        copy(source / name, name)
    for name in ("fixture-repair", "chg02-raw-operands", "chg06-observation", "chg04-request", "chg10-repeat-inputs"):
        copy(source / "behavior-evidence" / (name + ".json"), name + ".json")
    for name in ("edit_feature.py", "retain_feature_evidence.py"):
        copy(source / name, "helpers/" + name)
    copy(source / "behavior2-repository/docs/engineering/demo-change/intent/INT-ACC-001.md",
         "changed-intent.md", json.loads((source / "behavior-evidence/chg02-raw-operands.json").read_text())["fixture_injection"]["after_sha256"])

    selected = {k: v for k, v in groups.items() if isinstance(v, list) and k != "notes"}
    selected["negative_outside_scope"] = ["chg05-proposed-scope"]
    # The explicit lost-receipt group was recorded after the first group index.
    selected["transition_receipt_recovery"] = ["chg08-transition-preview", "chg08-transition-apply-lost-receipt", "chg08-transition-recovery-readback"]
    records = {}
    for name in sorted({name for rows in selected.values() for name in rows}):
        path = source / "behavior-evidence" / (name + ".json")
        record = json.loads(path.read_text())
        argv = []
        for i, arg in enumerate(record["argv"]):
            normalized = arg.replace("\\", "/")
            if i == 0 and normalized.endswith("/python.exe"):
                arg = "{python}"
            else:
                for repo in ("behavior-repository", "behavior2-repository", "behavior3-repository", "readiness-repository", "transition-repository"):
                    prefix = source.as_posix() + "/" + repo
                    if normalized == prefix or normalized.startswith(prefix + "/"):
                        arg = "{repo}" + normalized[len(prefix):]
                        break
                else:
                    for folder, token in (("package-inputs", "{fixtures}/package-inputs"),):
                        prefix = source.as_posix() + "/" + folder
                        if normalized.startswith(prefix + "/"):
                            arg = token + normalized[len(prefix):]
                    for helper in ("edit_feature.py", "retain_feature_evidence.py"):
                        if normalized == source.as_posix() + "/" + helper:
                            arg = "{helpers}/" + helper
            argv.append(arg)
        try:
            result = json.loads(record["stdout"])
        except ValueError:
            result = {}
        records[name] = {"argv": argv, "expected_exit": record["exit_code"],
                         "expected_changed_paths": record.get("changed_paths", []),
                         "expected_state": result.get("state"), "observed_record_sha256": sha(path),
                         "observed_record": str(path)}
    manifest = {"classification": "Fixed command replay of independently observed Windows actions; not fresh model behavior or a policy engine",
                "evaluator_version": "0.16.0", "payload_sha256": "51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c",
                "archive_sha256": "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae",
                "assets": assets, "groups": selected, "records": records}
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf8", newline="\n")
    print(json.dumps({"assets": len(assets), "recorded_commands": len(records), "manifest_sha256": sha(dest / "manifest.json")}))


if __name__ == "__main__":
    main()

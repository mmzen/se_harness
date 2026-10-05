"""Independent oracle, run by the exact released evaluator, not the service.

Copies the mounted original source directly. Neither the service materializer
nor its read handler supplies this oracle's inputs or expected file set.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from se_harness.evaluator_identity import installed_evaluator_identity
from se_harness.engine.validation_core import load_artifacts
from se_harness.installer import apply_changes, plan_install
from se_harness.workflow_change_set import formal_snapshot_digest


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def independent_digest(root, paths):
    value = hashlib.sha256()
    for name in sorted(paths):
        raw = (root / name).read_bytes()
        try:
            raw = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        except UnicodeDecodeError:
            pass
        path = name.encode("utf-8")
        value.update(len(path).to_bytes(8, "big")); value.update(path)
        value.update(len(raw).to_bytes(8, "big")); value.update(raw)
    return value.hexdigest()


def main(args):
    args.output.mkdir(parents=True, exist_ok=False)
    identity = installed_evaluator_identity().to_lock()
    assert identity["version"] == "0.22.1"
    assert identity["archive_sha256"] == "cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053"
    assert identity["payload_sha256"] == "0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff"
    fixture = json.loads(args.fixture.read_text())["reference_context"]
    manifest = json.loads(args.manifest.read_text())
    with tempfile.TemporaryDirectory(prefix="independent-hag-oracle-") as scratch:
        root = Path(scratch) / "project"
        shutil.copytree(args.source, root)
        for entry in manifest["artifacts"]:
            raw = (root / entry["path"]).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == entry["raw_sha256"]
            assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == entry["blob_oid"]
        changes, lock = plan_install(root, project_name="hosted-artifact-poc", mode="upgrade")
        apply_changes(root, changes, lock, allow_updates=True)
        cmd = [sys.executable, "-I", "-m", "se_harness", "check", str(root), "--artifact", "WO-RLS-038", "--json"]
        child = subprocess.run(cmd, cwd=scratch, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        result = json.loads(child.stdout)
        save(args.output / "released-oracle.json", {"command": cmd, "exit": child.returncode,
             "stdout": child.stdout.decode(), "stderr": child.stderr.decode(), "identity": identity})
        assert child.returncode == 0
        assert set(result["scope"]["governing"]) == set(fixture["governing_ids"])
        assert set(result["scope"]["declared_paths"]) == set(fixture["declared_scope"])
        if args.hosted_result:
            hosted = json.loads(json.loads(args.hosted_result.read_text())["stdout"])
            assert hosted["evaluator_output"] == result
        artifacts, errors = load_artifacts(root / "docs/engineering", root)
        assert not errors
        catalog = {a.artifact_id: a for a in artifacts}
        paths = {catalog[a].path.relative_to(root).as_posix() for a in [fixture["work_order_id"], *fixture["governing_ids"]]}
        paths.update(p for p in fixture["declared_scope"] if not p.startswith("docs/engineering/") and (root / p).is_file())
        digest = independent_digest(root, paths)
        actual = formal_snapshot_digest(root, artifacts, ["WO-RLS-038"])
        assert digest == actual
        observations = {"identity": identity, "files": sorted(paths), "independent_digest": digest, "released_digest": actual,
                        "original_git_artifacts": len(manifest["artifacts"])}
        code = root / "README.md"; original = code.read_bytes()
        code.write_bytes(original + b"\nHistorical binding qualification change.\n")
        changed = formal_snapshot_digest(root, artifacts, ["WO-RLS-038"])
        assert changed != digest and changed == independent_digest(root, paths)
        observations["changed_scoped_code_digest"] = changed
        code.write_bytes(original)
        chosen = catalog["REQ-IAR-030"]
        previous = chosen.path; moved = previous.with_name("REQ-IAR-030-moved.md")
        previous.rename(moved)
        moved_artifacts, errors = load_artifacts(root / "docs/engineering", root)
        assert not errors
        moved_digest = formal_snapshot_digest(root, moved_artifacts, ["WO-RLS-038"])
        assert moved_digest != digest
        observations["moved_original_path_digest"] = moved_digest
        moved.rename(previous)
        raw = previous.read_bytes(); previous.write_bytes(raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        crlf_digest = formal_snapshot_digest(root, artifacts, ["WO-RLS-038"])
        assert crlf_digest == digest
        observations["crlf_legacy_digest"] = crlf_digest
        observations["raw_lf_sha256"] = hashlib.sha256(raw).hexdigest()
        observations["raw_crlf_sha256"] = hashlib.sha256(previous.read_bytes()).hexdigest()
        assert observations["raw_lf_sha256"] != observations["raw_crlf_sha256"]
        save(args.output / "historical-bindings.json", observations)
    print(json.dumps({"independent_oracle": "passed", "original_artifacts": len(manifest["artifacts"]), "legacy_digest": digest}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "manifest", "fixture", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--hosted-result", type=Path)
    main(parser.parse_args())

"""Reuse the retained graph fixture against the exact wheel's viewer bytes."""

import argparse
import ast
import hashlib
import json
import platform
import re
import shutil
import subprocess
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.source).resolve()
    wheel = Path(args.wheel).resolve()
    member = "se_harness/engine/harness_explorer/index.template.html"
    with zipfile.ZipFile(wheel) as archive:
        content = archive.read(member)
        inventory = [{"path": entry.filename, "size": entry.file_size,
                      "sha256": hashlib.sha256(archive.read(entry)).hexdigest()}
                     for entry in archive.infolist() if not entry.is_dir()]
    assert content == (root / member).read_bytes(), "wheel viewer differs from exact source"
    html = content.decode("utf-8")
    marker = '"./Lineage%20View.dc.html": new Blob(['
    view, _ = json.JSONDecoder().raw_decode(html[html.index(marker) + len(marker):])
    script = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', view, re.S).group(1)
    fixture_path = root / "tests/test_dashboard_webui.py"
    tree = ast.parse(fixture_path.read_text(encoding="utf-8"))
    method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
                  and n.name == "test_lineage_prefers_verified_records_independently_of_id")
    assignment = next(n for n in method.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "runner" for t in n.targets))
    runner = ast.literal_eval(assignment.value)
    node = shutil.which("node")
    assert node, "Node is required; an absent runtime is not a pass"
    command = [node, "-e", runner]
    result = subprocess.run(command, input=json.dumps(script), text=True,
                            encoding="utf-8", capture_output=True, timeout=30)
    outcomes = json.loads(result.stdout) if result.returncode == 0 else []
    passed = result.returncode == 0 and len(outcomes) == 4 and all(
        o["selected"] == (o["id"] if o["status"] == "verified" else "VREC-AAA-001") for o in outcomes)
    report = {
        "candidate": args.candidate, "platform": platform.platform(),
        "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
        "viewer_sha256": hashlib.sha256(content).hexdigest(),
        "fixture_path": str(fixture_path),
        "fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        "argv": command, "input_script_sha256": hashlib.sha256(script.encode()).hexdigest(),
        "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        "outcomes": outcomes, "passed": passed, "wheel_inventory": inventory,
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: report[key] for key in ("candidate", "wheel_sha256", "viewer_sha256", "outcomes", "passed")}))
    assert passed, "packaged viewer failed the definition-derived outcomes"


if __name__ == "__main__":
    main()

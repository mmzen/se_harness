"""Index the retained pre-login observations; never turn missing cases into passes."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import digest, write

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--evidence", type=Path, required=True)
args = parser.parse_args()
root = args.evidence.resolve()
cases = {
    "C01": ("Discovery, startup, resume and compaction invoke the guard or retain the precise unavailable step.",
            "Plugin installation and skill discovery succeeded. Hooks are registered but untrusted. No handler delivery observed.",
            ["host-attempts/plugin-add.json", "host-attempts/prompt-input.json"], "live host; no model completion"),
    "C02": ("Real setup identifies missing, old or unusable supplied Python without installing Python or claiming readiness.",
            "Missing-runtime guidance was observed only in direct inline calibration. Live setup awaits authentication; old/unusable Python not assessed.",
            ["calibration-inline-corrected/missing-runtime.json"], "direct calibration only"),
    "C03": ("Two fresh host sessions deliver interpreter identity and source bytes from the prepared evaluator.",
            "Exact 0.16.0 wheel installs offline; direct identity/doctor checks pass and source bytes are emitted. No two trusted host runs yet.",
            ["calibration-inline-corrected/install-wheel.json", "calibration-inline-corrected/prepared-runtime.json"], "direct calibration only"),
    "C04": ("Resume and completed compaction deliver fresh changed source bytes, or a precise unavailable route is retained.",
            "Empty-thread start succeeded; immediate resume found no rollout; compact request accepted without observed completion. Real restoration remains untested.",
            [], "live app-server endpoint observations only"),
    "C05": ("Observe separately denied/untrusted and trusted hook activation, including actual permission interaction.",
            "Both hooks reported trustStatus=untrusted. No deliberate denial or grant interaction has occurred.",
            [], "live hooks/list observation only"),
    "C06": ("Observe paths with spaces, update/reload, persistent plugin data and interpreter removal through the host.",
            "Live installation uses paths with spaces. Removed-runtime behavior and data paths calibrated directly, not through Codex. Update/reload pending.",
            ["host-attempts/plugin-add.json", "calibration-inline-corrected/removed-runtime.json"], "live install plus separately labeled calibration"),
    "C07": ("Real agent shell tools complete authorized setup and repair; retain the unready governed-write result and normal permissions.",
            "No model turn completed: unblocked network retry returned 401 missing authentication. No agent tool setup/repair or governed-write attempt occurred.",
            ["host-attempts/exec-startup-network-retry.json"], "live unauthenticated host attempt"),
}
transcript = json.loads((root / "app-server/transcript.json").read_text())
for case, (expected, observed, paths, layer) in cases.items():
    directory = root / case
    if directory.exists():
        raise SystemExit(f"Preserve previous case index: {directory}")
    records = [json.loads((root / p).read_text()) for p in paths]
    extra = []
    if case in ("C04", "C05"):
        ids = (4, 5, 6) if case == "C04" else (2,)
        extra = [x for x in transcript if x["message"].get("id") in ids]
        paths.append("app-server/transcript.json")
    write(directory / "actions.txt", json.dumps({"layer": layer,
        "argv": [r.get("argv") for r in records], "app_server_messages": extra,
        "source_evidence": paths}, indent=2)+"\n")
    write(directory / "stdout.txt", "\n".join(r.get("stdout", "") for r in records)
          +(json.dumps(extra, indent=2) if extra else ""))
    write(directory / "stderr.txt", "\n".join(r.get("stderr", "") for r in records))
    write(directory / "observations.json", json.dumps({
        "case": case, "expected": expected, "observed": observed,
        "conclusion": "unavailable", "case_passed": False, "evidence_layer": layer,
        "exit_statuses": [r.get("exit_status") for r in records],
        "source_evidence": {p: digest(root / p) for p in paths},
        "remaining": "See report.md; operator login and hook trust are not complete."
    }, indent=2)+"\n")
write(root / "fixture-source-digests.json", json.dumps({
    p.name: digest(p) for p in Path(__file__).parent.iterdir() if p.suffix in (".py", ".ps1", ".md")
}, indent=2)+"\n")
print("Indexed C01-C07 as incomplete/unavailable; no case counted as passed.")

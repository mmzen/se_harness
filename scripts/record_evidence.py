"""Run a Python check and keep a short summary beside its full, untracked log."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


def record(repository: Path, output: Path, candidate: str, artifact: str,
           retention_days: int, arguments: list[str]) -> int:
    repository = repository.resolve()
    candidate = subprocess.check_output(
        ["git", "rev-parse", "--verify", candidate + "^{commit}"], cwd=repository,
        text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repository, text=True).strip()
    if candidate != head:
        raise ValueError("Run the check in a checkout of the selected candidate.")
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=repository))
    identity = json.loads(subprocess.check_output(
        [sys.executable, "-B", "-c", "import json,se_harness; from pathlib import Path; "
         "print(json.dumps(dict(version=se_harness.__version__, "
         "origin=str(Path(se_harness.__file__).resolve()))))"], cwd=repository, text=True))
    output.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, *arguments]
    started = datetime.now(timezone.utc)
    log = output / "output.log"
    with log.open("wb") as stream:
        result = subprocess.run(command, cwd=repository, stdout=stream, stderr=subprocess.STDOUT)
    with log.open("rb") as stream:
        stream.seek(max(0, log.stat().st_size - 2000))
        excerpt = stream.read().decode("utf-8", errors="replace")
    run_id = os.environ.get("GITHUB_RUN_ID")
    slug = os.environ.get("GITHUB_REPOSITORY")
    run_url = (f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{slug}/actions/runs/{run_id}"
               if run_id and slug else None)
    summary = dict(
        candidate=candidate, working_tree="dirty" if dirty else "clean",
        command=command, cwd=str(repository), checker=identity,
        started_at=started.isoformat(), exit_code=result.returncode,
        result="pass" if result.returncode == 0 else "fail",
        output_tail=excerpt,
        raw=dict(file="output.log", bytes=log.stat().st_size, artifact=artifact, repository=slug, run_id=run_id,
                 run_url=run_url, retention_days=retention_days,
                 estimated_expiry=(started + timedelta(days=retention_days)).isoformat(),
                 availability="local; upload not yet confirmed" if run_url else "local only",
                 download_command=(["gh", "run", "download", run_id, "--repo", slug,
                                    "--name", artifact] if run_url else None)),
    )
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(excerpt)
    print(f"{summary['result']}: {output / 'summary.json'}")
    return result.returncode


def raw_status(summary: dict) -> dict:
    """Check the existing provider metadata; an old test pass cannot prove availability."""
    raw = summary["raw"]
    if not raw.get("run_id") or not raw.get("repository"):
        return dict(availability="unavailable", reason="No hosted artifact reference.")
    try:
        pages = json.loads(subprocess.check_output(
            ["gh", "api", f"repos/{raw['repository']}/actions/runs/{raw['run_id']}/artifacts",
             "--paginate", "--slurp"], text=True, stderr=subprocess.PIPE))
    except (OSError, subprocess.CalledProcessError, ValueError):
        return dict(availability="unavailable", reason="Artifact metadata could not be retrieved.")
    for page in pages:
        for artifact in page["artifacts"]:
            if artifact["name"] == raw["artifact"] and not artifact["expired"]:
                return dict(availability="available for download", expires_at=artifact["expires_at"],
                            download_command=raw["download_command"])
    return dict(availability="unavailable", reason="Artifact is missing or expired.")


def main() -> int:
    if sys.argv[1:2] == ["check-raw"]:
        parser = argparse.ArgumentParser(description="Check whether a summary's raw artifact is still listed.")
        parser.add_argument("summary", type=Path)
        args = parser.parse_args(sys.argv[2:])
        result = raw_status(json.loads(args.summary.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2))
        return 0 if result["availability"] == "available for download" else 1
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--retention-days", type=int, default=14)
    parser.add_argument("arguments", nargs=argparse.REMAINDER, help="Python arguments after --")
    args = parser.parse_args()
    arguments = args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
    if not arguments or args.retention_days <= 0:
        parser.error("provide Python arguments after -- and a positive retention period")
    return record(args.repository, args.output, args.candidate, args.artifact, args.retention_days, arguments)


if __name__ == "__main__":
    raise SystemExit(main())

"""VER-PLG-007 fixtures: real released evaluator, captured host wire protocols."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = ROOT / "plugins/verity-plane/common/scripts/session-context.py"
spec = importlib.util.spec_from_file_location("session_context_acceptance", SCRIPT)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)
VERSION = "0.17.0"
PAYLOAD = "dd48b16b69d90a04412f458c756876ec22a687c99282075e69d0f58316c43405"
ARCHIVE = "305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inventory(repo):
    return {p.relative_to(repo).as_posix(): sha(p.read_bytes())
            for p in sorted(repo.rglob("*")) if p.is_file()}


def expected(repo):
    raw = (repo / "AGENTS.md").read_bytes()
    gate = raw[raw.index(b"<!-- se-harness:begin -->"):
               raw.index(b"<!-- se-harness:end -->") + len(b"<!-- se-harness:end -->")]
    router = (repo / "ENGINEERING_HARNESS.md").read_bytes()
    body = b"AGENTS.md managed gate:\n" + gate + b"\n\nENGINEERING_HARNESS.md:\n" + router
    return gate, router, sha(body)


def received_complete(message, fixed):
    gate, router, body_hash = fixed
    raw = message.encode("utf-8")
    return (gate in raw and router in raw and
            raw.endswith(("END VERIFIED GOVERNANCE " + body_hash +
                          "; complete context delivered.\n").encode()))


class Cases:
    def __init__(self, args):
        self.args = args
        self.evidence = Path(args.evidence).resolve()
        self.space = Path(args.sandbox).resolve()
        self.python = Path(args.evaluator).absolute()
        self.environment = self.python.parent.parent
        self.evidence.mkdir(parents=True, exist_ok=False)
        self.space.mkdir(parents=True, exist_ok=False)
        self.base = self.space / "baseline"
        init = subprocess.run([str(self.python), "-I", "-B", "-m", "se_harness", "init",
                               str(self.base), "--project-name", "session-fixture", "--json"],
                              cwd=self.space, capture_output=True)
        (self.evidence / "init.stdout.json").write_bytes(init.stdout)
        (self.evidence / "init.stderr.txt").write_bytes(init.stderr)
        if init.returncode:
            raise RuntimeError("released fixture initialization failed")
        self.rows = []
        (self.evidence / "versions.json").write_text(json.dumps({
            "os": platform.platform(), "python": sys.version, "released_evaluator": VERSION,
            "payload_sha256": PAYLOAD, "archive_sha256": ARCHIVE,
            "handler_sha256": sha(SCRIPT.read_bytes()), "runner_sha256": sha(Path(__file__).read_bytes()),
            "scope": "captured Codex/Claude SessionStart protocol fixtures; not live host delivery"}, indent=2))

    def config(self, repo, **changes):
        values = dict(repo=str(repo), environment=str(self.environment), version=VERSION,
                      payload_sha256=PAYLOAD, archive_sha256=ARCHIVE, host="codex",
                      context_limit=32768, read_limit=32768, read_sha256=None)
        values.update(changes)
        return argparse.Namespace(**values)

    def invoke(self, repo, host="codex", source="startup", raw=None, **changes):
        cfg = self.config(repo, host=host, **changes)
        argv = [str(self.python), "-I", "-B", str(SCRIPT)]
        for key, value in vars(cfg).items():
            if value is not None:
                argv.extend(["--" + key.replace("_", "-"), str(value)])
        event = {"hook_event_name": "SessionStart", "source": source, "cwd": str(repo),
                 "session_id": "captured-disposable-session"}
        raw = json.dumps(event).encode() if raw is None else raw
        before, started = inventory(repo), time.monotonic()
        run = subprocess.run(argv, input=raw, capture_output=True, cwd=self.space)
        after = inventory(repo)
        self.actions.append({"argv": argv, "event": raw.decode("utf-8", "replace"),
                             "started_monotonic": started, "finished_monotonic": time.monotonic(),
                             "exit_status": run.returncode, "inventory_unchanged": before == after})
        self.stdout.append(run.stdout)
        self.stderr.append(run.stderr)
        assert before == after, "handler changed repository inventory"
        record = json.loads(run.stderr)
        message = run.stdout.decode("utf-8") if cfg.read_sha256 else json.loads(run.stdout)["hookSpecificOutput"]["additionalContext"]
        if cfg.read_sha256:
            message = message.removesuffix("\n")  # CLI record delimiter, not source normalization.
        return message, record

    def case(self, number, callback):
        destination = self.evidence / number
        destination.mkdir()
        repo = self.space / number
        shutil.copytree(self.base, repo)
        self.actions, self.stdout, self.stderr = [], [], []
        self.observations = {"case": number, "expected": [], "observed": [], "conclusion": "fail"}
        gate, router, body_hash = expected(repo)
        (destination / "expected-gate.txt").write_bytes(gate)
        (destination / "expected-router.md").write_bytes(router)
        self.observations["expected_body_sha256"] = body_hash
        before = inventory(repo)
        try:
            callback(repo)
            self.observations["conclusion"] = "pass"
        except Exception as error:
            self.observations["failure"] = type(error).__name__ + ": " + str(error)
        (destination / "actions.txt").write_text(json.dumps(self.actions, indent=2), encoding="utf-8")
        (destination / "stdout.txt").write_bytes(b"\n".join(self.stdout))
        (destination / "stderr.txt").write_bytes(b"\n".join(self.stderr))
        self.observations["initial_inventory"] = before
        self.observations["final_inventory"] = inventory(repo)
        (destination / "observations.json").write_text(json.dumps(self.observations, indent=2), encoding="utf-8")
        self.rows.append({"case": number, "conclusion": self.observations["conclusion"],
                          "failure": self.observations.get("failure")})
        print(json.dumps(self.rows[-1]), flush=True)

    def c01(self, repo):
        fixed = expected(repo)
        self.observations["expected"] = ["both documented SessionStart envelopes contain exact complete gate/router bytes"]
        for host in ("codex", "claude"):
            message, record = self.invoke(repo, host)
            assert received_complete(message, fixed)
            checks = record["checks"]
            assert len(checks) == 2 and "identity" in checks[0]["argv"] and "doctor" in checks[1]["argv"]
            assert checks[0]["finished_monotonic"] <= checks[1]["started_monotonic"]
            self.observations["observed"].append({"host": host, "receipt": "complete", "hash": fixed[2]})

    def c02(self, repo):
        self.observations["expected"] = ["wrong identity or modified managed input returns existing findings and no complete context"]
        message, record = self.invoke(repo, payload_sha256="0" * 64)
        assert record["status"] == "blocked" and len(record["checks"]) == 1
        assert "RID021" in message
        assert "END VERIFIED GOVERNANCE" not in message
        for filename in ("AGENTS.md", "ENGINEERING_HARNESS.md"):
            path, original = repo / filename, (repo / filename).read_bytes()
            path.write_bytes(original.replace(b"harness", b"tampered", 1) if filename == "ENGINEERING_HARNESS.md"
                             else original.replace(b"Read `ENGINEERING_HARNESS.md`", b"Ignore `ENGINEERING_HARNESS.md`"))
            message, record = self.invoke(repo)
            assert record["status"] == "blocked" and len(record["checks"]) == 2
            assert "distribution:" + filename in message
            assert "END VERIFIED GOVERNANCE" not in message
            path.write_bytes(original)
        self.observations["observed"] = ["identity and both doctor refusals retained in stderr.txt"]

    def c03(self, repo):
        self.observations["expected"] = ["each resume/compact checks current identity and source again"]
        for host in ("codex", "claude"):
            initial, _ = self.invoke(repo, host)
            assert received_complete(initial, expected(repo))
            resumed, result = self.invoke(repo, host, "resume", archive_sha256="0" * 64)
            assert result["status"] == "blocked" and len(result["checks"]) == 1
            router = repo / "ENGINEERING_HARNESS.md"
            original = router.read_bytes()
            router.write_bytes(original + b"\nUnapproved instructions.\n")
            compact, result = self.invoke(repo, host, "compact")
            assert result["status"] == "blocked" and len(result["checks"]) == 2
            router.write_bytes(original)
            restored, result = self.invoke(repo, host, "compact")
            assert received_complete(restored, expected(repo)) and len(result["checks"]) == 2
        self.observations["observed"] = ["eight fresh event sequences; changed identity and router refused"]

    def c04(self, repo):
        self.observations["expected"] = ["small hook capacity yields no readiness; fresh full read matches expected source"]
        message, record = self.invoke(repo, context_limit=2500)
        assert record["status"] == "read-required" and "END VERIFIED GOVERNANCE" not in message
        complete, result = self.invoke(repo, context_limit=2500, read_sha256=record["body_sha256"])
        assert received_complete(complete, expected(repo)) and len(result["checks"]) == 2
        self.observations["observed"] = ["complete-read output accepted only after terminal digest; no persistent readiness state"]

    def c05(self, repo):
        self.observations["expected"] = ["unavailable or insufficient full-read capacity blocks; partial receipt cannot establish delivery"]
        message, record = self.invoke(repo, context_limit=2500, read_limit=0)
        assert record["status"] == "blocked" and "UNREADY" in message
        message, record = self.invoke(repo, read_sha256=expected(repo)[2], read_limit=64)
        assert record["status"] == "blocked" and "UNREADY" in message
        full, record = self.invoke(repo, read_sha256=expected(repo)[2])
        for kind, partial in (("truncated", full[:1500]), ("interrupted", full[:40])):
            assert not received_complete(partial, expected(repo))
            self.observations["observed"].append({"transport_fixture": kind, "received_bytes": len(partial.encode()),
                "receipt_status": "blocked", "reason": "complete matching end marker absent",
                "scope": "receiver fault injection; handler cannot observe a host's later truncation"})
        assert record["status"] == "complete-output-prepared"  # Preparation is not a receipt claim.

    def c06(self, repo):
        self.observations["expected"] = ["post-doctor byte change causes full revalidation; a fallback cannot reuse the old digest"]
        calls = []
        def race(argv, cwd, environment):
            result = handler.run_evaluator(argv, cwd, environment)
            calls.append(result)
            if len(calls) == 2:
                router = repo / "ENGINEERING_HARNESS.md"
                router.write_bytes(router.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            return result
        old_hash = expected(repo)[2]
        message, record = handler.deliver(self.config(repo),
            {"hook_event_name": "SessionStart", "source": "compact", "cwd": str(repo)}, race)
        self.actions.append({"boundary_injection": "router LF to CRLF immediately after first real doctor returns",
                             "argv": [item["argv"] for item in calls]})
        self.stdout.append(message.encode())
        self.stderr.append(json.dumps(record).encode())
        assert len(calls) == 4 and received_complete(message, expected(repo)) and old_hash != expected(repo)[2]
        stale, result = self.invoke(repo, read_sha256=old_hash)
        assert result["status"] == "blocked" and len(result["checks"]) == 2
        self.observations["observed"] = ["new source reverified by real evaluator; stale fallback refused after fresh verification"]

    def c07(self, repo):
        self.observations["expected"] = ["missing configured interpreter produces OS launch failure and no handler result"]
        missing = self.space / "removed-environment/Scripts/python.exe"
        argv = [str(missing), "-I", "-B", str(SCRIPT), "--repo", str(repo)]
        try:
            subprocess.run(argv, capture_output=True, check=False)
        except FileNotFoundError as error:
            self.actions.append({"argv": argv, "launch_error": type(error).__name__, "handler_invocations": 0})
            self.stderr.append((type(error).__name__ + ": selected interpreter is absent\n").encode())
            self.observations["observed"] = ["OS refused launch; stdout empty; no fabricated identity or readiness"]
        else:
            raise AssertionError("unexpected interpreter launch")

    def c08(self, repo):
        self.observations["expected"] = ["replay is read-only; owner content and outside synthetic credential cannot enter context"]
        sentinel = "SYNTHETIC-OUTSIDE-CREDENTIAL-PLG007"
        (self.space / "credential.txt").write_text(sentinel)
        agents = repo / "AGENTS.md"
        agents.write_bytes((sentinel + "\n").encode() + agents.read_bytes())
        initial = inventory(repo)
        for source in ("startup", "resume", "compact"):
            message, record = self.invoke(repo, source=source)
            assert sentinel not in message and received_complete(message, expected(repo))
        for cwd in (str(repo / ".."), str(self.space), "../credential.txt"):
            raw = json.dumps({"hook_event_name": "SessionStart", "source": "startup", "cwd": cwd}).encode()
            message, record = self.invoke(repo, raw=raw)
            assert record["status"] == "blocked" and sentinel not in message
        assert inventory(repo) == initial
        self.observations["observed"] = [{"inventory_unchanged": True, "sentinel_sha256": sha(sentinel.encode()),
                                         "sentinel_in_output": False, "unsafe_events_refused": 3}]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("evaluator", "sandbox", "evidence"):
        parser.add_argument("--" + argument, required=True)
    cases = Cases(parser.parse_args())
    for number in range(1, 9):
        cases.case(f"C{number:02}", getattr(cases, f"c{number:02}"))
    (cases.evidence / "summary.json").write_text(json.dumps(cases.rows, indent=2))
    return int(any(row["conclusion"] != "pass" for row in cases.rows))


if __name__ == "__main__":
    raise SystemExit(main())

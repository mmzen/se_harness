"""Retain actual private-sandbox recovery observations without changing source.

The operator supplies the same HAG_* environment as the original Compose run.
The original volumes and the restored copy are preserved for inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import secrets
import shutil
import time
import zipfile
from pathlib import Path

RUNTIME = "python@sha256:88310c082760d93ac7c74d579e95e53a4ab6ea52dd8901abc61a103daf488ac4"
OBSERVE = r'''
import hashlib,json
from pathlib import Path
from hosted_artifact_graph.service import Service
from hosted_artifact_graph.canonical import canonical_json
s=Service(json.loads(Path('/run/config/config.json').read_text()),json.loads(Path('/run/secrets/sandbox_credentials').read_text()))
try:
 version=s.store.ready()
 with s.store.transaction() as tx:
  nodes=sorted(hashlib.sha256(canonical_json(dict(r['p']))).hexdigest() for r in tx.run('MATCH (n) RETURN properties(n) AS p'))
  edges=sorted(hashlib.sha256(canonical_json(dict(r))).hexdigest() for r in tx.run('MATCH (a)-[e]->(b) RETURN coalesce(a.revision_id,a.baseline_id,a.context_id,a.artifact_id,a.project_id) AS a,type(e) AS t,properties(e) AS p,coalesce(b.revision_id,b.baseline_id,b.context_id,b.artifact_id,b.project_id) AS b'))
  baselines=sorted(r['id'] for r in tx.run('MATCH (b:Baseline) RETURN b.baseline_id AS id'))
  receipts=sorted([r['key'],hashlib.sha256(r['result'].encode()).hexdigest()] for r in tx.run('MATCH (o:Operation) RETURN o.operation_key AS key,o.result_json AS result'))
 with s.store.driver.session() as session:
  storage=session.run('SHOW STORAGE INFO').data()
 print(json.dumps({'project_version':version,'nodes':len(nodes),'edges':len(edges),'logical_store_sha256':hashlib.sha256(canonical_json([nodes,edges])).hexdigest(),'baselines':baselines,'receipts':receipts,'storage':storage}))
finally:s.store.driver.close()
'''


def prepare(args):
    """Build the exact source combination; this does not claim qualification."""
    root, output = args.repository.resolve(), args.output.resolve()
    if output == root or output.is_relative_to(root):
        raise ValueError("Choose a new output directory outside the repository")
    output.mkdir(parents=True, exist_ok=False)
    commands = []

    def run(label, command, *, cwd=output):
        child = subprocess.run(list(map(str, command)), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=900)
        record = {"command": list(map(str, command)), "cwd": str(cwd), "exit": child.returncode,
                  "stdout": child.stdout.decode(errors="replace"), "stderr": child.stderr.decode(errors="replace")}
        (output / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        commands.append(label + ".json")
        if child.returncode:
            raise RuntimeError(label + " failed; inspect retained output")
        return child.stdout

    commit = run("source-commit", ["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    if run("source-status", ["git", "status", "--porcelain"], cwd=root).strip():
        raise ValueError("Commit the reviewed implementation before building its combination")
    replay = json.loads(args.client_replay.read_text(encoding="utf-8"))
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    client = {"version": "0.22.2", "wheel_sha256": digest(args.client_wheel)}
    if replay["candidate"]["commit"] != commit or replay["manifest"]["wheel_sha256"] != client["wheel_sha256"]:
        raise ValueError("Client replay does not bind this clean commit and wheel")
    if len(replay["builds"]) != 2 or any(b["wheel_sha256"] != client["wheel_sha256"] for b in replay["builds"]):
        raise ValueError("Both pinned builds must reproduce the supplied wheel")
    evaluator = {"version": "0.22.1", "archive_sha256": "cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053",
                 "payload_sha256": "0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff"}
    if digest(args.evaluator_wheel) != evaluator["archive_sha256"]:
        raise ValueError("Supplied evaluator is not the selected immutable public wheel")
    source = output / "candidate-source"
    for row in subprocess.check_output(["git", "ls-tree", "-rz", commit, "--", "server", "plugins/verity-plane"], cwd=root).split(b"\0"):
        if not row:
            continue
        header, relative = row.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError("Only regular candidate source files are supported")
        target = source / relative.decode("utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(["git", "cat-file", "blob", oid], cwd=root))
    plugin_dir = output / "plugin"
    run("plugin-assembly", [sys.executable, "-B", "-c",
        "import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from repository_tools.plugin_distribution import develop;print(json.dumps(develop(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]))))",
        root, source, args.evaluator_wheel, plugin_dir])
    canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    plugins = {}
    for host in ("codex", "claude"):
        archive_path = plugin_dir / f"verity-plane-{host}.zip"
        with zipfile.ZipFile(archive_path) as archive:
            inventory = [{"path": name, "sha256": hashlib.sha256(archive.read(name)).hexdigest()} for name in sorted(archive.namelist())]
            manifest_name = ".codex-plugin" if host == "codex" else ".claude-plugin"
            version = json.loads(archive.read(f"verity-plane/{manifest_name}/plugin.json"))["version"]
            if version != "0.2.7":
                raise ValueError("Select the distinct unpublished plugin candidate")
            if hashlib.sha256(archive.read("verity-plane/packages/" + args.evaluator_wheel.name)).hexdigest() != evaluator["archive_sha256"]:
                raise ValueError("Plugin changed the governing evaluator")
        (output / f"plugin-{host}-inventory.json").write_bytes(canonical(inventory))
        plugins[host] = {"version": version, "archive_sha256": digest(archive_path), "inventory_sha256": hashlib.sha256(canonical(inventory)).hexdigest()}
    context = source / "server"
    (context / "vendor").mkdir()
    shutil.copy2(args.evaluator_wheel, context / "vendor" / args.evaluator_wheel.name)
    run("server-build", ["docker", "buildx", "build", "--load", "--provenance=false", "--build-arg", "SOURCE_COMMIT=" + commit,
         "--metadata-file", output / "image-metadata.json", "--tag", args.image, context])
    observed = json.loads(run("image-package", ["docker", "run", "--rm", "--entrypoint", "python", args.image, "-c",
        "import json,hashlib,platform;from pathlib import Path;from importlib.metadata import version;w,=Path('/opt/service-wheel').glob('*.whl');print(json.dumps({'version':version('se-harness-hosted-sandbox'),'wheel_sha256':hashlib.sha256(w.read_bytes()).hexdigest(),'python':platform.python_version()}))"]))
    image = json.loads((output / "image-metadata.json").read_text())
    config = json.loads((context / "config.example.json").read_text())
    config["client"] = client
    config.pop("components")
    deployment_digest = hashlib.sha256(canonical({"configuration": config, "compose_sha256": digest(context / "compose.yaml")})).hexdigest()
    payload = {"schema": "se-harness-hosted-combination/v1", "source": {"repository": "https://github.com/mmzen/se_harness.git", "candidate_commit": commit},
               "client": client, "plugins": plugins, "server": {"version": observed["version"], "wheel_sha256": observed["wheel_sha256"],
               "image_manifest": image["containerimage.digest"], "dependency_lock_sha256": digest(context / "requirements.lock"),
               "system_packages_sha256": digest(context / "system-packages.lock.json")}, "evaluator": evaluator,
               "runtime": {"python": observed["python"], "platform": "linux/amd64", "image": RUNTIME},
               "database": {"version": "3.13.1", "image": "memgraph/memgraph@sha256:4710bee1ab5b47599876e30f17ae1679d0bbb2262d84dc06641521fecb7c89ce"},
               "schema_revision": 1, "protocols": config["protocols"], "deployment_sha256": deployment_digest,
               "required_secret_keys": ["principals[].token"]}
    combination_id = "sha256:" + hashlib.sha256(b"se-harness-hosted-combination/v1\n" + canonical(payload)).hexdigest()
    config["components"] = payload
    directory = output / "configuration"; directory.mkdir()
    (directory / "config.json").write_bytes(canonical(config))
    credentials = {"principals": [{"id": name, "role": role, "projects": [config["project_id"]], "token": secrets.token_urlsafe(32)}
        for name, role in (("operator", "operator"), ("author-one", "sandbox-author"), ("author-two", "sandbox-author"), ("reader", "sandbox-reader"))]}
    secret = output / "credentials.json"
    secret.write_bytes(canonical(credentials)); secret.chmod(0o600)
    result = {"combination_id": combination_id, "payload": payload, "state": "built; qualification pending", "commands": commands}
    (output / "combination.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"combination_id": combination_id, "candidate": commit, "state": result["state"], "output": str(output)}))


def recover(args):
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    sequence = 0
    env = dict(os.environ)
    original = args.project
    restored = original + "-restore"
    commands = []

    def run(label, command, *, environment=env, allowed=(0,)):
        nonlocal sequence
        sequence += 1
        start = time.monotonic()
        result = subprocess.run(list(map(str, command)), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=environment, timeout=300)
        value = {"command": list(map(str, command)), "exit": result.returncode,
                 "seconds": round(time.monotonic() - start, 3), "stdout": result.stdout.decode(errors="replace"),
                 "stderr": result.stderr.decode(errors="replace")}
        filename = f"{sequence:03}-{label}.json"
        (output / filename).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        commands.append(filename)
        print(json.dumps({"step": label, "exit": result.returncode, "seconds": value["seconds"]}), flush=True)
        if result.returncode not in allowed:
            raise RuntimeError(label + " failed; inspect " + filename)
        return value

    def compose(project, *argv):
        return ["docker", "compose", "-p", project, "-f", args.compose, *argv]

    def observe(label, project, environment=env):
        # The image is already built. Wait only for startup, never migrate/reinitialize.
        for attempt in range(30):
            value = run(label + "-" + str(attempt), compose(project, "exec", "-T", "service", "python", "-c", OBSERVE),
                        environment=environment, allowed=(0, 1))
            if value["exit"] == 0:
                return json.loads(value["stdout"])
            if not any(term in value["stderr"] for term in ("not running", "Connection refused", "ServiceUnavailable", "DatabaseUnavailable", "Failed to establish")):
                raise RuntimeError("Observation failed beyond startup availability; inspect the retained result")
            time.sleep(1)
        raise RuntimeError("Readiness did not recover")

    def same(before, after):
        keys = ("project_version", "logical_store_sha256", "baselines", "receipts", "nodes", "edges")
        assert all(before[k] == after[k] for k in keys), "Recovery changed acknowledged identities"

    before = observe("cutoff", original)
    started = time.monotonic()
    run("stop-original", compose(original, "stop", "service", "graph"))
    run("restart-original", compose(original, "up", "-d", "graph", "service"))
    restarted = observe("restarted", original)
    restart_seconds = round(time.monotonic() - started, 3)
    same(before, restarted)
    run("quiesce-for-backup", compose(original, "stop", "service", "graph"))
    graph_volume = original + "_graph_data"
    run("copy-consistent-backup", ["docker", "run", "--rm", "--mount", f"type=volume,src={graph_volume},dst=/data,readonly",
        "--mount", f"type=bind,src={output},dst=/backup", "--entrypoint", "tar", RUNTIME, "-cf", "/backup/graph-data.tar", "-C", "/data", "."])
    archive = output / "graph-data.tar"
    with archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    run("resume-original", compose(original, "up", "-d", "graph", "service"))
    # Refuse reuse so this test cannot overwrite an earlier restored database.
    inspect = run("restore-volume-must-be-new", ["docker", "volume", "inspect", restored + "_graph_data"], allowed=(0, 1))
    if inspect["exit"] == 0:
        raise ValueError("Restore volume already exists; choose a new qualification project")
    started = time.monotonic()
    run("create-restore-volume", ["docker", "volume", "create", restored + "_graph_data"])
    run("restore-backup", ["docker", "run", "--rm", "--mount", f"type=volume,src={restored}_graph_data,dst=/data",
        "--mount", f"type=bind,src={output},dst=/backup,readonly", "--entrypoint", "tar", RUNTIME, "-xf", "/backup/graph-data.tar", "-C", "/data"])
    restored_env = dict(env, HAG_HTTP_PORT=str(args.restore_port))
    run("start-restored", compose(restored, "up", "-d", "graph", "service"), environment=restored_env)
    after = observe("restored", restored, restored_env)
    restore_seconds = round(time.monotonic() - started, 3)
    same(before, after)
    resumed = observe("original-preserved", original)
    same(before, resumed)
    result = {"state": "restart_and_consistent_restore_passed", "cutoff": before,
              "restarted": restarted, "restored": after, "original_preserved": resumed,
              "restart_seconds": restart_seconds, "restore_seconds": restore_seconds,
              "backup": {"path": str(archive), "bytes": archive.stat().st_size, "sha256": digest},
              "original_project": original, "restored_project": restored, "commands": commands,
              "limits": "Observed quiesced backup and process restart only; no power-loss, HA or production RPO/RTO claim."}
    (output / "recovery.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"state": result["state"], "backup_sha256": digest, "restore_seconds": restore_seconds}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    build = commands.add_parser("prepare", help="build an exact unpublished combination; no qualification claim")
    for name in ("repository", "output", "client-wheel", "client-replay", "evaluator-wheel"):
        build.add_argument("--" + name, type=Path, required=True)
    build.add_argument("--image", required=True)
    restore = commands.add_parser("recover", help="restart and restore the private initialized sandbox")
    restore.add_argument("--compose", type=Path, required=True)
    restore.add_argument("--project", required=True)
    restore.add_argument("--output", type=Path, required=True)
    restore.add_argument("--restore-port", type=int, default=18081)
    args = parser.parse_args()
    prepare(args) if args.action == "prepare" else recover(args)

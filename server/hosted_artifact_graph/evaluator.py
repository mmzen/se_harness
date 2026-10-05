"""Disposable materialization and bounded calls into the pinned release."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import threading
from contextlib import contextmanager
from pathlib import Path

from .canonical import canonical_json
from .protocol import EVALUATOR, Refusal, contained_file, require

BRIDGE = Path(__file__).with_name("evaluator_bridge.py")
OUTPUT_LIMIT = 32 * 1024 * 1024


class Evaluator:
    def __init__(self, config):
        self.python = Path(config["evaluator_python"])
        self.source = Path(config["source_directory"])
        self.manifest = json.loads(Path(config["source_manifest"]).read_text(encoding="utf-8"))
        self.support = json.loads(Path(config["source_inventory"]).read_text(encoding="utf-8"))
        self.wheel = Path(config["evaluator_wheel"])
        self.semaphore = threading.BoundedSemaphore(2)

    def invoke(self, args, *, cwd=None):
        # A fixed executable/argv, isolated imports, no shell or inherited Python path.
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
        with tempfile.TemporaryDirectory(prefix="harness-evaluator-") as scratch:
            with open(Path(scratch) / "out", "wb") as out, open(Path(scratch) / "err", "wb") as err:
                with self.semaphore:
                    process = subprocess.Popen([str(self.python), "-I", "-B", *map(str, args)],
                                               cwd=cwd or scratch, stdout=out, stderr=err, env=env)
                    try:
                        process.wait(timeout=120)
                    except subprocess.TimeoutExpired as exc:
                        process.kill()
                        process.wait()
                        raise Refusal(429, "RESOURCE_LIMIT", "Released evaluator exceeded 120 seconds.") from exc
                require(out.tell() <= OUTPUT_LIMIT and err.tell() <= OUTPUT_LIMIT, 429,
                        "RESOURCE_LIMIT", "Released evaluator output exceeds its bound.")
            raw = (Path(scratch) / "out").read_bytes()
            try:
                result = json.loads(raw)
            except (ValueError, UnicodeError) as exc:
                raise Refusal(422, "BINDING_UNAVAILABLE", "Released evaluator did not return a JSON result.") from exc
            return process.returncode, result

    def bridge(self, action, root=None):
        code, result = self.invoke([BRIDGE, action, *([root] if root is not None else [])])
        require(code == 0, 422, "BINDING_UNAVAILABLE", "Released adapter failed.", evaluator_output=result)
        return result

    def identity(self):
        require(self.python.is_absolute() and self.python.is_file(), 409, "UNSUPPORTED_TUPLE", "Missing isolated evaluator.")
        require(hashlib.sha256(self.wheel.read_bytes()).hexdigest() == EVALUATOR["archive_sha256"],
                409, "UNSUPPORTED_TUPLE", "Selected evaluator archive differs.")
        actual = self.bridge("identity")
        require(all(actual.get(k) == v for k, v in EVALUATOR.items()), 409,
                "UNSUPPORTED_TUPLE", "Installed evaluator version, archive or payload differs.")
        return actual

    def verify_source(self):
        require(self.support["source"] == self.manifest["source"], 409, "SOURCE_MISMATCH", "Source inventories disagree.")
        for item in self.support["files"]:
            raw = contained_file(self.source, item["path"]).read_bytes()
            require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                    422, "BINDING_UNAVAILABLE", "Pinned source binding differs: " + item["path"])

    @contextmanager
    def project(self, revisions=None):
        self.identity()
        with tempfile.TemporaryDirectory(prefix="harness-projection-") as scratch:
            root = Path(scratch) / "project"
            root.mkdir()
            # Copy only operator-manifested regular files. Never execute source inputs.
            for item in self.support["files"]:
                source = contained_file(self.source, item["path"])
                target = root / item["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                raw = source.read_bytes()
                require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                        422, "BINDING_UNAVAILABLE", "Pinned source binding differs: " + item["path"])
                target.write_bytes(raw)
            if revisions is not None:
                for entry in self.manifest["artifacts"]:
                    (root / entry["path"]).unlink()
                paths = set()
                for revision in revisions.values():
                    envelope = revision["envelope"]
                    path = envelope["original_path"]
                    require(path is not None and path not in paths, 422, "INCOMPLETE_SELECTION", "Missing or duplicate projection path.")
                    paths.add(path)
                    # Revision paths originate in the verified import or released authoring tool.
                    require(not Path(path).is_absolute() and ".." not in Path(path).parts and "\\" not in path
                            and ":" not in path, 422, "PROTECTED_FIELD", "Invalid projection path.")
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(base64.b64decode(revision["document_base64"], validate=True))
            self.bridge("select", root)
            yield root

    def catalog(self, root):
        result = self.bridge("catalog", root)
        require(not result["errors"], 422, "INVALID_DRAFT", "Released parser rejected content.", evaluator_output=result)
        items = result["artifacts"]
        require(len({a["id"].casefold() for a in items}) == len(items), 422,
                "INVALID_DRAFT", "Duplicate artifact IDs.")
        return {a["id"]: a for a in items}

    def cli(self, root, command, *args):
        return self.invoke(["-m", "se_harness", command, root, *args, "--json"])[1]

    def check(self, revisions, artifact_id):
        with self.project(revisions) as root:
            return self.cli(root, "check", "--artifact", artifact_id)

"""Read-only acceptance check for the approved plugin stack integration.

The approved digest is an independent input, never calculated as approval here.
This checks committed objects only; it neither grants assurance nor runs CI.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib


DOMAIN = "docs/engineering/plugin-integration/"
OID = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class Refusal(ValueError):
    """An input or preservation obligation was not satisfied."""


def require(condition, message):
    if not condition:
        raise Refusal(message)


def oid(value):
    require(isinstance(value, str) and OID.fullmatch(value), "Expected a full immutable SHA-1 object ID")
    return value


def path(value, *, scope=False):
    require(isinstance(value, str) and bool(value), "Empty or non-string repository path")
    stripped = value[:-1] if scope and value.endswith("/") else value
    require(
        bool(stripped) and "\\" not in stripped and ":" not in stripped
        and all(ord(c) >= 32 and ord(c) != 127 for c in stripped)
        and all(p not in ("", ".", "..", ".git") for p in stripped.split("/")),
        f"Unsafe repository path: {value!r}",
    )
    return value


def covered(name, scopes):
    return any(name.startswith(s) if s.endswith("/") else name == s for s in scopes)


def scopes(value):
    require(isinstance(value, list) and bool(value), "Scopes must be a nonempty list")
    result = [path(v, scope=True) for v in value]
    require(len(set(result)) == len(result), "Duplicate scope")
    return result


def entry(value):
    require(isinstance(value, dict) and set(value) == {"mode", "blob"}, "Invalid planned tree entry")
    require(value["mode"] in ("100644", "100755", "120000"), "Invalid imported blob mode")
    return value["mode"], oid(value["blob"])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def metadata(data):
    lines = data.decode("utf-8").splitlines()
    require(bool(lines) and lines[0] == "+++", "Missing artifact metadata")
    try:
        end = lines.index("+++", 1)
    except ValueError as exc:
        raise Refusal("Unterminated artifact metadata") from exc
    return tomllib.loads("\n".join(lines[1:end]))


class Git:
    def __init__(self, repository):
        self.repository = Path(repository).resolve(strict=True)
        # Do not accept ambient alternate repositories, replacement objects or
        # index locations. These reads do not refresh the index or contact a host.
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1")
        self.prefix = ["git", "--no-replace-objects", "-c", f"safe.directory={self.repository.as_posix()}",
                       "-c", "core.longpaths=true", "-c", "core.autocrlf=false",
                       "-c", "core.fsmonitor=false", "-C", str(self.repository)]
        self.trees = {}
        top = Path(self.run("rev-parse", "--show-toplevel").decode().strip()).resolve()
        require(top == self.repository, "Repository must name the worktree root")
        require(self.run("rev-parse", "--show-object-format").strip() == b"sha1", "Expected SHA-1 repository")

    def run(self, *args, input=None, accepted=(0,)):
        result = subprocess.run(self.prefix + list(args), input=input, env=self.env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        require(result.returncode in accepted,
                f"Git read failed ({args[0]}): {result.stderr.decode('utf-8', 'replace')[:500].strip()}")
        return result.stdout

    def kind(self, object_id, expected):
        require(self.run("cat-file", "-t", oid(object_id)).strip().decode() == expected,
                f"Expected {expected} object: {object_id}")

    def ancestor(self, ancestor, candidate):
        self.kind(ancestor, "commit")
        # merge-base exits one for an existing object that is not an ancestor.
        result = subprocess.run(self.prefix + ["merge-base", "--is-ancestor", ancestor, candidate],
                                env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        require(result.returncode == 0, f"Missing required ancestry: {ancestor} -> {candidate}")

    def tree(self, object_id):
        oid(object_id)
        if object_id not in self.trees:
            found = {}
            for item in self.run("ls-tree", "-r", "-z", "--full-tree", object_id).split(b"\0"):
                if not item:
                    continue
                header, name = item.split(b"\t", 1)
                mode, kind, blob = header.decode("ascii").split()
                name = path(name.decode("utf-8"))
                require(name not in found and kind in ("blob", "commit"), "Invalid tree entry")
                found[name] = (mode, oid(blob))
            self.trees[object_id] = found
        return self.trees[object_id]

    def blobs(self, object_ids):
        ids = list(dict.fromkeys(oid(x) for x in object_ids))
        if not ids:
            return {}
        raw = self.run("cat-file", "--batch", input=("\n".join(ids) + "\n").encode("ascii"))
        result, pos = {}, 0
        for expected in ids:
            end = raw.find(b"\n", pos)
            require(end >= 0, "Incomplete object response")
            fields = raw[pos:end].split()
            require(len(fields) == 3 and fields[0].decode() == expected and fields[1] == b"blob",
                    f"Missing evidence or imported blob: {expected}")
            size = int(fields[2])
            data = raw[end + 1:end + 1 + size]
            require(len(data) == size and raw[end + 1 + size:end + 2 + size] == b"\n", "Truncated blob")
            require(hashlib.sha1(b"blob " + str(size).encode() + b"\0" + data).hexdigest() == expected,
                    f"Corrupt Git blob: {expected}")
            result[expected] = data
            pos = end + size + 2
        require(pos == len(raw), "Unexpected object response")
        return result


def archive_entries(tree):
    directories = set()
    for name in tree:
        parts = name.split("/")
        directories.update("/".join(parts[:n]) for n in range(1, len(parts)))
    return len(tree) + len(directories)


def tree_oid(entries):
    """Hash Git's tree encoding without writing or requiring preview objects."""
    root = {}
    for name, leaf in entries.items():
        node = root
        parts = name.split("/")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            require(isinstance(node, dict), f"File/directory collision: {name}")
        require(parts[-1] not in node, f"File/directory collision: {name}")
        node[parts[-1]] = leaf

    def encode(node):
        contents = []
        # Git compares directory names as if they end in '/'. Plain name
        # sorting is wrong when a neighboring filename contains punctuation.
        for name, value in sorted(node.items(), key=lambda item:
                                  item[0].encode("utf-8") + (b"/" if isinstance(item[1], dict) else b"")):
            mode, object_id = ("40000", encode(value)) if isinstance(value, dict) else value
            contents.append(mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + bytes.fromhex(object_id))
        raw = b"".join(contents)
        return hashlib.sha1(b"tree " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

    return encode(root)


def compare(actual, expected, label, exceptions=()):
    differences = sorted(name for name in actual.keys() | expected.keys()
                         if actual.get(name) != expected.get(name) and not covered(name, exceptions))
    require(not differences, f"{label}: {len(differences)} mismatched paths: {differences[:12]}")


def verify(repository, candidate, plan_path, approved_plan_sha256):
    require(isinstance(approved_plan_sha256, str) and SHA256.fullmatch(approved_plan_sha256),
            "Expected independently approved SHA-256 digest")
    plan_file = Path(plan_path).resolve(strict=True)
    require(plan_file.stat().st_size <= 16 * 1024 * 1024, "Plan exceeds 16 MiB")
    plan_bytes = plan_file.read_bytes()
    require(digest(plan_bytes) == approved_plan_sha256, "Plan does not match independently approved digest")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    plan = json.loads(plan_bytes, object_pairs_hook=unique_keys)
    require(isinstance(plan, dict) and plan.get("schema") == "plugin-stack-integration-plan-v1", "Unsupported plan schema")
    candidate, base = oid(candidate), oid(plan["base_main"])
    heads = plan["source_heads"]
    require(isinstance(heads, dict) and bool(heads), "Missing source heads")
    source_ids = [oid(h) for h in heads.values()]
    imported_scope = scopes(plan["source_import_scope"])
    integration_scope = scopes(plan["integration_only_scope"])
    require(not any(covered(a.rstrip("/"), integration_scope) or covered(b.rstrip("/"), imported_scope)
                    for a in imported_scope for b in integration_scope), "Import and integration scopes overlap")
    changes, records = plan["changes"], plan["verified_records_and_preserved_history"]
    require(isinstance(changes, list) and bool(changes), "Missing planned imports")
    require(isinstance(records, list) and bool(records), "Missing preserved records")
    require(type(plan["source_changed_paths"]) is int and plan["source_changed_paths"] == len(changes), "Incorrect import count")
    limit = plan["archive_entry_limit"]
    require(type(limit) is int and 0 < limit <= 10000, "Invalid archive limit")

    git = Git(repository)
    git.kind(candidate, "commit")
    git.ancestor(base, candidate)
    for head in source_ids:
        git.ancestor(head, candidate)
    assembly = plan["assembly"]
    require(assembly["left"] in source_ids and assembly["right"] in source_ids
            and assembly["conflicts"] is False, "Invalid assembly inputs")
    oid(assembly["expected_tree"])
    baseline = git.tree(base)
    expected = baseline.copy()
    source_trees = [git.tree(head) for head in source_ids]
    imported = {}
    change_counts = Counter()
    for change in changes:
        name = path(change["path"])
        require(name not in imported and covered(name, imported_scope), f"Invalid or duplicate import: {name}")
        original = None if change["base"] is None else entry(change["base"])
        target = entry(change["expected"])
        require(original == baseline.get(name) and target != original, f"Incorrect baseline entry: {name}")
        require(change["change"] == ("A" if original is None else "M"), f"Incorrect change type: {name}")
        require(any(t.get(name) == target for t in source_trees), f"Import absent from pinned sources: {name}")
        owners = change["source_work_orders"]
        require(isinstance(owners, list) and bool(owners) and len(set(owners)) == len(owners)
                and all(isinstance(w, str) and re.fullmatch(r"WO-PLG-\d{3}", w) for w in owners),
                f"Missing or invalid import owners: {name}")
        imported[name] = target
        expected[name] = target
        change_counts[change["change"]] += 1
    require(dict(change_counts) == plan["source_change_counts"], "Incorrect change census")
    require(tree_oid(expected) == assembly["expected_tree"], "Pinned assembly differs from baseline plus imports")
    require(archive_entries(expected) == plan["source_archive_entries"], "Incorrect source archive census")
    actual = git.tree(candidate)
    compare(actual, expected, "Candidate differs from frozen import/baseline", integration_scope)
    count = archive_entries(actual)
    require(count <= limit, f"Archive entry limit exceeded: {count} > {limit}")
    # Also compare the committed plan when the explicit input is in this worktree.
    if plan_file.is_relative_to(git.repository):
        plan_name = plan_file.relative_to(git.repository).as_posix()
        require(plan_name in actual, "Approved plan is not in the candidate")
        require(digest(git.blobs([actual[plan_name][1]])[actual[plan_name][1]]) == approved_plan_sha256,
                "Candidate plan differs from independently approved digest")

    # Read bytes, not only tree IDs: missing/corrupt imported objects fail closed.
    imported_bytes = git.blobs(value[1] for value in imported.values())
    work_orders = sorted({w for c in changes for w in c["source_work_orders"]})
    wo_scopes = {}
    for work_order in work_orders:
        name = DOMAIN + "work-orders/" + work_order + ".md"
        require(name in imported, f"Source work order is not a frozen import: {work_order}")
        data = metadata(imported_bytes[imported[name][1]])
        require(data.get("id") == work_order and data.get("type") == "work_order"
                and data.get("status") == "implemented", f"Source work order is not implemented: {work_order}")
        wo_scopes[work_order] = scopes(data["execution_scope"]["paths"])
    for change in changes:
        require(all(covered(change["path"], wo_scopes[w]) for w in change["source_work_orders"]),
                f"Import lacks its declared original work-order scope: {change['path']}")

    report_records, seen_records = [], set()
    for record in records:
        record_id = record["id"]
        require(isinstance(record_id, str) and re.fullmatch(r"VREC-PLG-\d{3}", record_id)
                and record_id not in seen_records, "Invalid or duplicate preserved record")
        seen_records.add(record_id)
        name = DOMAIN + "verification-records/" + record_id + ".md"
        require(name in imported and imported[name][1] == oid(record["record_blob"]), f"Incorrect record blob: {record_id}")
        raw = imported_bytes[record["record_blob"]]
        require(digest(raw) == record["record_sha256"], f"Incorrect record digest: {record_id}")
        data = metadata(raw)
        bound = oid(record["candidate"])
        require(data.get("id") == record_id and data.get("type") == "verification_record"
                and data.get("status") == record["status"] and record["status"] in ("ready", "verified")
                and data.get("commit") == bound and data.get("worktree_state") == "clean"
                and data.get("git_object_format") == "sha1"
                and data["relations"]["verifies_work_order"] == record["verifies_work_order"],
                f"Incorrect preserved record binding: {record_id}")
        require(all(w in wo_scopes for w in record["verifies_work_order"]), f"Uncovered record work order: {record_id}")
        git.ancestor(bound, candidate)
        sidecar = path(data["evaluator_evidence_path"])
        require(sidecar in imported, f"Sidecar is not a frozen import: {record_id}")
        require(digest(imported_bytes[imported[sidecar][1]]) == record["evaluator_sha256"]
                == data["evaluator_evidence_sha256"], f"Incorrect evaluator sidecar: {record_id}")
        evidence = data["evidence_paths"]
        require(isinstance(evidence, list) and bool(evidence) and len(set(evidence)) == len(evidence)
                and type(record["selected_evidence_files"]) is int
                and len(evidence) == record["selected_evidence_files"], f"Incorrect evidence selection: {record_id}")
        historical = git.tree(bound)
        for evidence_path in evidence:
            path(evidence_path)
            require(evidence_path in historical and historical[evidence_path][0] in ("100644", "100755"),
                    f"Selected evidence absent from bound candidate: {record_id}: {evidence_path}")
        evidence_bytes = git.blobs(historical[p][1] for p in evidence)
        inventory = [{"path": p, "mode": historical[p][0], "blob": historical[p][1],
                      "sha256": digest(evidence_bytes[historical[p][1]])} for p in sorted(evidence)]
        report_records.append({"id": record_id, "status": data["status"], "candidate": bound,
                               "record_sha256": digest(raw), "selected_evidence_files": len(evidence),
                               "evidence_inventory_sha256": digest(json.dumps(inventory, sort_keys=True).encode()),
                               "current_evidence_entries_differ_from_bound_commit":
                                   sum(actual.get(p) != historical[p] for p in evidence)})

    return {"schema": "plugin-stack-integration-check-v1", "passed": True,
            "candidate": candidate, "base_main": base, "approved_plan_sha256": approved_plan_sha256,
            "source_heads": heads, "imported_paths": len(imported), "source_change_counts": dict(change_counts),
            "archive_entries_including_directories": count, "archive_entry_limit": limit,
            "source_work_orders": work_orders, "preserved_records": report_records,
            "boundary": "Committed-object preservation only. No lifecycle decision, CI result or merge authority."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--candidate", required=True, help="Full immutable commit ID")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--approved-plan-sha256", required=True, help="Digest supplied from the independent approval")
    args = parser.parse_args(argv)
    try:
        result = verify(args.repository, args.candidate, args.plan, args.approved_plan_sha256)
    except (Refusal, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result = {"schema": "plugin-stack-integration-check-v1", "passed": False,
                  "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())

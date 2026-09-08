"""The generator's bundle seam (SPEC-ECP-024 ECP-ENG-018): from a snapshot to the resources, the manifest, the rendered index and the transactional write.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from se_harness.engine.dashboard_snapshot import GenerationError, is_within, text_list, text_value


BUNDLE_SCHEMA = "harness-dashboard-bundle-v2"

BOOTSTRAP_SCHEMA = "harness-dashboard-bootstrap-v2"

SUMMARY_RESOURCE_SCHEMA = "harness-dashboard-summary-v2"

TOPOLOGY_RESOURCE_SCHEMA = "harness-dashboard-topology-v2"

READINESS_RESOURCE_SCHEMA = "harness-dashboard-readiness-v2"

ARTIFACT_RESOURCE_SCHEMA = "harness-dashboard-artifact-v2"

MAX_SUMMARY_BYTES = 262_144

TOPOLOGY_ACCEPTANCE_BYTES = 2_097_152


def serialize_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def serialize_compact_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def _resource_descriptor(
    *,
    role: str,
    schema: str,
    path_prefix: str,
    content: str,
    artifact_id: str | None = None,
) -> dict[str, Any]:
    payload = content.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    descriptor: dict[str, Any] = {
        "role": role,
        "schema": schema,
        "path": f"{path_prefix}/{digest}.json" if schema != "utf8-markdown-v1" else f"content/{digest}.txt",
        "bytes": len(payload),
        "sha256": digest,
    }
    if artifact_id is not None:
        descriptor["artifact_id"] = artifact_id
    return descriptor


def _public_descriptor(descriptor: dict[str, Any]) -> dict[str, Any]:
    return dict(descriptor)


def topology_target_exceeded(topology_bytes: int) -> bool:
    """Return whether a compact topology exceeds the repository target."""
    return topology_bytes > TOPOLOGY_ACCEPTANCE_BYTES


def _hours_between(start: Any, end: Any) -> float | None:
    """Elapsed hours between two RFC 3339 timestamps, or None."""
    try:
        first = datetime.fromisoformat(str(start).replace("Z", "+00:00"))
        last = datetime.fromisoformat(str(end).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if first.tzinfo is None or last.tzinfo is None:
        return None
    return (last - first).total_seconds() / 3600


def build_explorer_metrics(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Governance indicators derived once from the canonical projection.

    Every figure is a restatement of recorded lifecycle events and declared
    relations; none is an assurance score, and none infers a decision.
    """
    artifacts = [item for item in snapshot.get("artifacts", []) if isinstance(item, dict) and isinstance(item.get("id"), str)]
    relations = [item for item in snapshot.get("relations", []) if isinstance(item, dict)]
    decided: Counter[str] = Counter()
    event_count = 0
    unattributed = 0
    delegated_transitions = 0
    delegated_records = 0
    delegated_artifacts: set[str] = set()
    lead_times: list[dict[str, Any]] = []
    for artifact in artifacts:
        events = [event for event in artifact.get("lifecycle_events") or [] if isinstance(event, dict)]
        for event in events:
            event_count += 1
            actor = text_value(event.get("decided_by"))
            if actor:
                decided[actor] += 1
            else:
                unattributed += 1
            if "delegated" in actor:
                delegated_transitions += 1
                delegated_artifacts.add(artifact["id"])
        if "delegated" in text_value(artifact.get("prepared_by")):
            delegated_records += 1
            delegated_artifacts.add(artifact["id"])
        if artifact.get("type") == "work_order":
            approved = next((event for event in events if event.get("to") == "approved"), None)
            implemented = next((event for event in events if event.get("to") == "implemented"), None)
            if approved and implemented:
                hours = _hours_between(approved.get("decided_at"), implemented.get("decided_at"))
                if hours is not None and hours > 0:
                    lead_times.append({"id": artifact["id"], "hours": round(hours, 2)})
    lead_times.sort(key=lambda item: (item["hours"], item["id"]))
    # SPEC-DCM-001 rule 13: decision counts and raise-to-dispose times. A decision
    # is raised when created (a date, read at midnight UTC) and disposed at the
    # time its disposition records.
    decisions = [item for item in artifacts if item.get("type") == "decision"]
    decisions_open = sum(1 for item in decisions if item.get("status") in {"open", "deferred"})
    decisions_decided = sum(1 for item in decisions if item.get("status") == "decided")
    dispose_times: list[dict[str, Any]] = []
    for item in decisions:
        disposition = item.get("disposition")
        if not isinstance(disposition, dict) or item.get("status") not in {"decided", "deferred", "withdrawn"}:
            continue
        raised = text_value(item.get("created"))
        if len(raised) == 10:
            raised = f"{raised}T00:00:00Z"
        hours = _hours_between(raised, disposition.get("decided_at"))
        if hours is not None and hours >= 0:
            dispose_times.append({"id": item["id"], "hours": round(hours, 2)})
    dispose_times.sort(key=lambda item: (item["hours"], item["id"]))
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relation in relations:
        outgoing[str(relation.get("source"))].append(relation)
        incoming[str(relation.get("target"))].append(relation)
    released = [item for item in artifacts if item.get("type") == "release_record" and item.get("status") == "released"]
    released_work = sorted(
        {
            str(relation.get("target"))
            for record in released
            for relation in outgoing[record["id"]]
            if relation.get("relation") == "releases_work" and isinstance(relation.get("target"), str)
        }
    )
    verified_work = [
        work_order
        for work_order in released_work
        if any(relation.get("relation") == "verifies_work_order" for relation in incoming[work_order])
    ]
    latest = max(released, key=lambda item: (text_value(item.get("released_at")), item["id"]), default=None)
    latest_release: dict[str, Any] | None = None
    release_arc: dict[str, Any] | None = None
    if latest is not None:
        verification_record = next(
            (relation["target"] for relation in outgoing[latest["id"]] if relation.get("relation") == "includes_verification" and isinstance(relation.get("target"), str)),
            None,
        )
        latest_release = {
            "id": latest["id"],
            "version": latest.get("version"),
            "released_at": latest.get("released_at"),
            "commit": latest.get("commit"),
            "verification_record": verification_record,
        }
        contract_id = next(
            (relation["target"] for relation in outgoing[latest["id"]] if relation.get("relation") == "satisfies" and isinstance(relation.get("target"), str)),
            None,
        )
        contract = next((item for item in artifacts if item.get("id") == contract_id), None)
        if contract is not None:
            approved = next(
                (event for event in contract.get("lifecycle_events") or [] if isinstance(event, dict) and event.get("to") == "approved"),
                None,
            )
            if approved is not None:
                hours = _hours_between(approved.get("decided_at"), latest.get("released_at"))
                release_arc = {
                    "contract_id": contract_id,
                    "contract_approved_at": approved.get("decided_at"),
                    "released_at": latest.get("released_at"),
                    "hours": round(hours, 2) if hours is not None else None,
                }
    return {
        "lifecycle_events": event_count,
        "unattributed_events": unattributed,
        "decided_by": dict(sorted(decided.items())),
        "delegated_transitions": delegated_transitions,
        "delegated_records": delegated_records,
        "delegated_artifacts": sorted(delegated_artifacts),
        "lead_times": lead_times,
        "decisions_open": decisions_open,
        "decisions_decided": decisions_decided,
        "decision_dispose_times": dispose_times,
        "released_work_orders": len(released_work),
        "released_work_orders_verified": len(verified_work),
        "latest_release": latest_release,
        "release_arc": release_arc,
    }


def build_dashboard_bundle(
    snapshot: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], dict[str, Any]]:
    """Partition one canonical projection into deterministic progressive resources."""

    source_repository = snapshot.get("repository")
    if not isinstance(source_repository, dict):
        raise GenerationError("dashboard snapshot has no repository descriptor")
    repository = dict(source_repository)
    source_revision = repository.get("revision")
    revision = source_revision if isinstance(source_revision, str) and source_revision else "unavailable"
    repository["revision"] = revision

    evidence_documents = [
        document
        for document in snapshot.get("evidence_documents", [])
        if isinstance(document, dict)
    ]
    evidence_by_artifact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    resource_files: dict[str, str] = {}
    resource_descriptors: list[dict[str, Any]] = []

    for document in evidence_documents:
        public_document = {
            key: value
            for key, value in document.items()
            if key != "markdown"
        }
        for association in text_list(document.get("associations")):
            evidence_by_artifact[association].append(public_document)
        if document.get("state") != "included":
            continue
        markdown = document.get("markdown")
        if not isinstance(markdown, str):
            raise GenerationError("included evidence document has no Markdown")
        descriptor = _resource_descriptor(
            role="evidence",
            schema="utf8-markdown-v1",
            path_prefix="content",
            content=markdown,
        )
        if descriptor["path"] != document.get("raw_path"):
            raise GenerationError("evidence content path differs from its digest")
        previous = resource_files.get(descriptor["path"])
        if previous is not None and previous != markdown:
            raise GenerationError("evidence content collides on one digest path")
        resource_files[descriptor["path"]] = markdown
        if not any(item["path"] == descriptor["path"] for item in resource_descriptors):
            resource_descriptors.append(descriptor)

    compact_artifacts: list[dict[str, Any]] = []
    for artifact in snapshot.get("artifacts", []):
        if not isinstance(artifact, dict):
            raise GenerationError("dashboard artifact projection must be an object")
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not artifact_id:
            raise GenerationError("dashboard artifact projection has no ID")
        detail = {
            "schema": ARTIFACT_RESOURCE_SCHEMA,
            "repository_revision": revision,
            "artifact": artifact,
            "evidence_documents": sorted(
                evidence_by_artifact.get(artifact_id, []),
                key=lambda item: str(item.get("path") or ""),
            ),
        }
        detail_text = serialize_compact_json(detail)
        detail_descriptor = _resource_descriptor(
            role="artifact",
            schema=ARTIFACT_RESOURCE_SCHEMA,
            path_prefix="data/artifacts",
            content=detail_text,
            artifact_id=artifact_id,
        )
        resource_files[detail_descriptor["path"]] = detail_text
        resource_descriptors.append(detail_descriptor)
        compact_artifact = {
            **{
                key: artifact.get(key)
                for key in ("id", "type", "title", "status", "owners", "authority", "path")
            },
            "detail": _public_descriptor(detail_descriptor),
        }
        if "assurance_classification" in artifact:
            compact_artifact["assurance_classification"] = artifact[
                "assurance_classification"
            ]
        if artifact.get("type") == "release_record":
            for key in ("version", "released_at", "distribution"):
                if artifact.get(key) is not None:
                    compact_artifact[key] = artifact[key]
        if artifact.get("type") == "capability" and artifact.get("ability") is not None:
            # SPEC-TCM-005 TCM-RFC-006: the lineage board shows the ability under the title.
            compact_artifact["ability"] = artifact["ability"]
        if artifact.get("type") == "decision":
            # SPEC-DCM-001 rule 13: the in-flight tile shows age and deciding role.
            for key in ("created", "kind", "deciding_roles"):
                if artifact.get(key) is not None:
                    compact_artifact[key] = artifact[key]
        compact_artifacts.append(compact_artifact)

    summary = {
        "schema": SUMMARY_RESOURCE_SCHEMA,
        "finding_rules_version": snapshot.get("finding_rules_version"),
        "quality_gates_version": snapshot.get("quality_gates_version"),
        "repository": repository,
        "counts": {
            "artifacts": len(snapshot.get("artifacts", [])),
            "artifact_types": len(
                {
                    item.get("type")
                    for item in snapshot.get("artifacts", [])
                    if isinstance(item, dict) and item.get("type")
                }
            ),
            "relations": len(snapshot.get("relations", [])),
            "declared_relations": sum(
                1
                for item in snapshot.get("relations", [])
                if isinstance(item, dict) and item.get("authority") == "declared"
            ),
            "unresolved_relations": sum(
                1
                for item in snapshot.get("relations", [])
                if isinstance(item, dict) and item.get("target_exists") is False
            ),
            "coverage_active": sum(
                1 for item in snapshot.get("coverage", []) if item.get("active")
            ),
            "coverage_specified": sum(
                1
                for item in snapshot.get("coverage", [])
                if item.get("active") and item.get("specified")
            ),
            "coverage_verified": sum(
                1
                for item in snapshot.get("coverage", [])
                if item.get("active") and item.get("verified")
            ),
            "finding_blocking": sum(
                1
                for item in snapshot.get("findings", [])
                if item.get("severity") in {"error", "blocking"}
            ),
            "finding_error": sum(
                1
                for item in snapshot.get("findings", [])
                if item.get("severity") == "error"
            ),
            "finding_warning": sum(
                1
                for item in snapshot.get("findings", [])
                if item.get("severity") == "warning"
            ),
            "finding_info": sum(
                1
                for item in snapshot.get("findings", [])
                if item.get("severity") == "info"
            ),
        },
        "lifecycle_counts": dict(
            sorted(
                Counter(
                    str(item.get("status") or "unknown")
                    for item in snapshot.get("artifacts", [])
                    if isinstance(item, dict)
                ).items()
            )
        ),
        "queue_counts": {
            "draft": sum(
                1
                for item in snapshot.get("artifacts", [])
                if isinstance(item, dict) and item.get("status") == "draft"
            ),
            "ready": sum(
                1
                for item in snapshot.get("artifacts", [])
                if isinstance(item, dict) and item.get("status") == "ready"
            ),
            "unresolved_relations": sum(
                1
                for item in snapshot.get("relations", [])
                if isinstance(item, dict) and item.get("target_exists") is False
            ),
        },
        "metrics": build_explorer_metrics(snapshot),
    }
    topology = {
        "schema": TOPOLOGY_RESOURCE_SCHEMA,
        "repository_revision": revision,
        "artifacts": compact_artifacts,
        "relations": snapshot.get("relations", []),
        "coverage": snapshot.get("coverage", []),
    }
    readiness = {
        "schema": READINESS_RESOURCE_SCHEMA,
        "repository_revision": revision,
        "readiness": snapshot.get("readiness", []),
        "revision_provenance": snapshot.get("revision_provenance", []),
        "diagnostics": snapshot.get("diagnostics", []),
        "findings": snapshot.get("findings", []),
        "revision_policy": snapshot.get("revision_policy", {}),
        "experiments": snapshot.get("experiments", []),
        "evidence": snapshot.get("evidence", []),
    }

    entrypoints: dict[str, dict[str, Any]] = {}
    for role, schema, prefix, value in (
        ("summary", SUMMARY_RESOURCE_SCHEMA, "data/summary", summary),
        ("topology", TOPOLOGY_RESOURCE_SCHEMA, "data/topology", topology),
        ("readiness", READINESS_RESOURCE_SCHEMA, "data/readiness", readiness),
    ):
        text = serialize_compact_json(value)
        descriptor = _resource_descriptor(
            role=role,
            schema=schema,
            path_prefix=prefix,
            content=text,
        )
        resource_files[descriptor["path"]] = text
        resource_descriptors.append(descriptor)
        entrypoints[role] = _public_descriptor(descriptor)

    if entrypoints["summary"]["bytes"] > MAX_SUMMARY_BYTES:
        raise GenerationError(
            f"dashboard summary exceeds {MAX_SUMMARY_BYTES} UTF-8 bytes"
        )

    manifest = {
        "schema": BUNDLE_SCHEMA,
        "repository": repository,
        "entrypoints": entrypoints,
        "resources": sorted(resource_descriptors, key=lambda item: item["path"]),
    }
    manifest_text = serialize_json(manifest)
    manifest_payload = manifest_text.encode("utf-8")
    manifest_descriptor = {
        "path": "dashboard-manifest.json",
        "bytes": len(manifest_payload),
        "sha256": hashlib.sha256(manifest_payload).hexdigest(),
    }
    bootstrap = {
        "schema": BOOTSTRAP_SCHEMA,
        "bundle_schema": BUNDLE_SCHEMA,
        "repository_revision": revision,
        "manifest": manifest_descriptor,
    }
    role_bytes = Counter()
    role_counts = Counter()
    for descriptor in resource_descriptors:
        role = str(descriptor["role"])
        role_counts[role] += 1
        role_bytes[role] += int(descriptor["bytes"])
    largest = max(resource_descriptors, key=lambda item: int(item["bytes"]), default=None)
    observations = {
        "role_bytes": dict(sorted(role_bytes.items())),
        "role_counts": dict(sorted(role_counts.items())),
        "resource_count": len(resource_descriptors),
        "resource_bytes": sum(int(item["bytes"]) for item in resource_descriptors),
        "largest_resource": _public_descriptor(largest) if largest is not None else None,
        "topology_target_exceeded": topology_target_exceeded(entrypoints["topology"]["bytes"]),
    }
    return bootstrap, manifest, resource_files, observations


def _safe_embedded_json(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    replacements = {
        "&": "\\u0026",
        "<": "\\u003c",
        ">": "\\u003e",
        "\u2028": "\\u2028",
        "\u2029": "\\u2029",
    }
    for source, replacement in replacements.items():
        payload = payload.replace(source, replacement)
    return payload


def render_dashboard(bootstrap: dict[str, Any]) -> str:
    template_path = Path(__file__).resolve().parent / "harness_explorer" / "index.template.html"
    try:
        template = template_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise GenerationError("owned dashboard template is unavailable or unreadable") from exc
    marker = "__HARNESS_BOOTSTRAP_JSON__"
    if template.count(marker) != 1:
        raise GenerationError("owned dashboard template must contain exactly one bootstrap marker")
    return template.replace(marker, _safe_embedded_json(bootstrap))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_remove_tree(path: Path, parent: Path) -> None:
    resolved_path = path.resolve()
    resolved_parent = parent.resolve()
    if resolved_path == resolved_parent or not is_within(resolved_path, resolved_parent):
        raise GenerationError("refusing to remove a path outside the intended output parent")
    if path.exists():
        shutil.rmtree(path)


def _strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise GenerationError(f"{label} contains duplicate JSON key: {key}")
            value[key] = item
        return value

    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=reject_duplicates,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise GenerationError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise GenerationError(f"{label} must be a JSON object")
    return value


def verify_serialized_bundle(files: dict[str, bytes]) -> None:
    required_roots = {"dashboard-manifest.json", "generation-summary.json", "index.html"}
    if not required_roots <= set(files):
        raise GenerationError("generated dashboard is missing a required root file")
    manifest_bytes = files["dashboard-manifest.json"]
    manifest = _strict_json_bytes(manifest_bytes, "dashboard manifest")
    repository = manifest.get("repository")
    if (
        manifest.get("schema") != BUNDLE_SCHEMA
        or not isinstance(repository, dict)
        or not isinstance(repository.get("revision"), str)
        or not isinstance(manifest.get("resources"), list)
    ):
        raise GenerationError("dashboard manifest schema or repository is invalid")
    contracts = {
        "summary": (SUMMARY_RESOURCE_SCHEMA, "data/summary/"),
        "topology": (TOPOLOGY_RESOURCE_SCHEMA, "data/topology/"),
        "readiness": (READINESS_RESOURCE_SCHEMA, "data/readiness/"),
        "artifact": (ARTIFACT_RESOURCE_SCHEMA, "data/artifacts/"),
        "evidence": ("utf8-markdown-v1", "content/"),
    }
    declared: dict[str, dict[str, Any]] = {}
    for descriptor in manifest["resources"]:
        if not isinstance(descriptor, dict):
            raise GenerationError("dashboard manifest resource must be an object")
        path = descriptor.get("path")
        role = descriptor.get("role")
        schema = descriptor.get("schema")
        size = descriptor.get("bytes")
        digest = descriptor.get("sha256")
        contract = contracts.get(role)
        if (
            not isinstance(path, str)
            or not re.fullmatch(
                r"(?:data/(?:summary|topology|readiness|artifacts)/[0-9a-f]{64}\.json|content/[0-9a-f]{64}\.txt)",
                path,
            )
            or contract is None
            or schema != contract[0]
            or not path.startswith(contract[1])
            or not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or PurePosixPath(path).stem != digest
            or path in declared
        ):
            raise GenerationError("dashboard manifest resource descriptor is invalid")
        declared[path] = descriptor
    if set(files) != required_roots | set(declared):
        raise GenerationError("generated dashboard recursive set differs from its manifest")
    for path, descriptor in declared.items():
        payload = files[path]
        if len(payload) != descriptor["bytes"] or hashlib.sha256(payload).hexdigest() != descriptor["sha256"]:
            raise GenerationError(f"generated dashboard resource differs from its descriptor: {path}")
        if descriptor["schema"] == "utf8-markdown-v1":
            try:
                payload.decode("utf-8")
            except UnicodeError as exc:
                raise GenerationError(f"generated evidence resource is not UTF-8: {path}") from exc
            continue
        value = _strict_json_bytes(payload, path)
        if value.get("schema") != descriptor["schema"]:
            raise GenerationError(f"generated dashboard resource schema differs: {path}")
        if descriptor["role"] == "artifact":
            artifact = value.get("artifact")
            if not isinstance(artifact, dict) or artifact.get("id") != descriptor.get("artifact_id"):
                raise GenerationError(f"generated artifact resource identity differs: {path}")
    entrypoints = manifest.get("entrypoints")
    if not isinstance(entrypoints, dict):
        raise GenerationError("dashboard manifest entrypoints are invalid")
    for role in ("summary", "topology", "readiness"):
        descriptor = entrypoints.get(role)
        if not isinstance(descriptor, dict) or descriptor.get("role") != role or declared.get(descriptor.get("path")) != descriptor:
            raise GenerationError(f"dashboard manifest {role} entrypoint is invalid")
    try:
        html_text = files["index.html"].decode("utf-8")
    except UnicodeError as exc:
        raise GenerationError("dashboard index is not UTF-8") from exc
    matches = re.findall(
        r'<script id="harness-dashboard-bootstrap" type="application/json">(.*?)</script>',
        html_text,
        flags=re.DOTALL,
    )
    if len(matches) != 1:
        raise GenerationError("dashboard index has no unique bootstrap")
    bootstrap = _strict_json_bytes(matches[0].encode("utf-8"), "dashboard bootstrap")
    expected_manifest = {
        "path": "dashboard-manifest.json",
        "bytes": len(manifest_bytes),
        "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    }
    if (
        bootstrap.get("schema") != BOOTSTRAP_SCHEMA
        or bootstrap.get("bundle_schema") != BUNDLE_SCHEMA
        or bootstrap.get("repository_revision") != repository["revision"]
        or bootstrap.get("manifest") != expected_manifest
    ):
        raise GenerationError("dashboard bootstrap differs from its manifest")


def write_output_transactionally(output_root: Path, files: dict[str, str]) -> None:
    output_parent = output_root.parent.resolve()
    output_parent.mkdir(parents=True, exist_ok=True)
    if output_root.exists() and output_root.is_symlink():
        raise GenerationError("output root became a symbolic link")
    if output_root.exists() and not output_root.is_dir():
        raise GenerationError("output root became a non-directory path")

    temporary = Path(tempfile.mkdtemp(prefix=f".{output_root.name}.next-", dir=output_parent))
    backup: Path | None = None
    promoted = False
    try:
        normalized_names: dict[str, str] = {}
        for name, content in sorted(files.items()):
            relative = PurePosixPath(name)
            if (
                not relative.parts
                or relative.is_absolute()
                or ".." in relative.parts
                or any(not part or ":" in part for part in relative.parts)
            ):
                raise GenerationError(f"unsafe generated output path: {name}")
            collision_key = relative.as_posix().casefold()
            previous = normalized_names.get(collision_key)
            if previous is not None and previous != relative.as_posix():
                raise GenerationError(f"generated output path collision: {name}")
            normalized_names[collision_key] = relative.as_posix()
            destination = temporary.joinpath(*relative.parts)
            if not is_within(destination.resolve(), temporary.resolve()):
                raise GenerationError(f"generated output path escapes transaction: {name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8", newline="\n")
        expected = {PurePosixPath(name).as_posix() for name in files}
        actual = {
            path.relative_to(temporary).as_posix()
            for path in temporary.rglob("*")
            if path.is_file()
        }
        if actual != expected:
            raise GenerationError("temporary output is incomplete")
        if "dashboard-manifest.json" in files:
            verify_serialized_bundle(
                {
                    path.relative_to(temporary).as_posix(): path.read_bytes()
                    for path in temporary.rglob("*")
                    if path.is_file()
                }
            )

        if output_root.exists():
            backup = Path(tempfile.mkdtemp(prefix=f".{output_root.name}.previous-", dir=output_parent))
            backup.rmdir()
            output_root.replace(backup)
        temporary.replace(output_root)
        promoted = True
        if backup is not None:
            _safe_remove_tree(backup, output_parent)
    except Exception:
        if not promoted and backup is not None and backup.exists() and not output_root.exists():
            backup.replace(output_root)
        raise
    finally:
        if temporary.exists():
            _safe_remove_tree(temporary, output_parent)
        if promoted and backup is not None and backup.exists():
            _safe_remove_tree(backup, output_parent)

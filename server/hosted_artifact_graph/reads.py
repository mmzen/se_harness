"""HTTP and MCP share these explicit-view domain reads."""
from __future__ import annotations

import json
from .canonical import canonical_json
from .cypher import compile_query, public_rows
from .protocol import EVALUATOR, READ, Refusal, contained_file, require


def binding(revisions, artifact_id):
    require(artifact_id in revisions, 404, "UNKNOWN_IDENTITY", "Artifact is absent from the selected view: " + artifact_id)
    return {"artifact_id": artifact_id, "revision_id": revisions[artifact_id]["revision_id"]}


def edges(revisions):
    resolved, unresolved = [], []
    for artifact_id, revision in sorted(revisions.items()):
        for kind, targets in sorted(revision["envelope"]["declared_relations"].items()):
            for target in targets:
                if target in revisions:
                    resolved.append({"source": binding(revisions, artifact_id), "kind": kind, "target": binding(revisions, target)})
                else:
                    unresolved.append({"source_artifact_id": artifact_id, "kind": kind, "target_artifact_id": target})
    return resolved, unresolved


def edge_order(edge):
    return edge["source"]["artifact_id"], edge["kind"], edge["target"]["artifact_id"]


def incomplete(response, reason):
    strategies = {"unresolved_references": ("create_a_new_complete_view", "Resolve the named references in a new explicit view."),
                  "binding_unavailable": ("restore_exact_binding_and_repeat_at_same_view", "Restore the missing pinned input, then repeat at this exact view.")}
    strategy, instruction = strategies.get(reason, ("repeat_at_same_view_with_narrower_selection",
        "Repeat at this exact view with a narrower artifact selection or a larger budget within the fixed limits. This partial response is not a governing context."))
    response["complete"] = False
    response["continuation"] = {"reason": reason, "strategy": strategy, "instructions": instruction}


def constrain(response, budget):
    remaining = budget["rows"]
    # Each returned binding/edge/path/unresolved item consumes the shared allowance.
    for group in (response.get("data"), response):
        if not isinstance(group, dict):
            continue
        names = ("governing_artifacts", "declared_scope", "dependencies", "relevant_decisions", "changes",
                 "added_relations", "removed_relations", "artifacts", "relations", "rows", "unresolved_references")
        for name in names:
            values = group.get(name)
            if isinstance(values, list):
                if len(values) > remaining:
                    group[name] = values[:remaining]
                    incomplete(response, "row_limit")
                remaining = max(0, remaining - len(group[name]))
    # Never truncate evaluator JSON or canonical revision bytes to satisfy a byte budget.
    require(len(canonical_json(response)) <= budget["bytes"], 429,
            "RESOURCE_LIMIT", "Complete response envelope exceeds the selected byte budget; use a narrower selection or a larger allowed budget.")
    return response


def read(service, principal, request):
    require(isinstance(request, dict), 400, "MALFORMED", "Expected a read request.")
    service.access(principal, request.get("project_id"))
    service.wire.validate(request, "read-v1.json")
    service.evaluator.identity()
    operation, view, budget = request["operation"], request["view"], request["budget"]
    with service.store.transaction(timeout=5 if operation == "cypher" else 120) as tx:
        if operation == "compare":
            snapshot = service.store.view(tx, view["left"])
            other = service.store.view(tx, view["right"])
        else:
            snapshot = service.store.view(tx, view)
        revisions = snapshot["revisions"]
        snapshot["snapshot"] = service.store.selected_snapshot(tx, snapshot)
        response = {"schema": READ, "project_id": service.project_id, "observed_project_version": snapshot["version"],
                    "evaluator": EVALUATOR, "provenance": [], "unresolved_references": [], "complete": True,
                    "continuation": None, "operation": operation, "view": view, "data": None, "evaluator_output": None}
        if service.config.get("test_copy") is True:
            response.update(schema="se-harness-graph-read/v2", test_copy=True,
                            authority="rehearsal-only; Git remains authoritative")
        if operation == "cypher":
            query = compile_query(request["query"], request["parameters"], snapshot, budget, service.project_id)
            rows = public_rows(list(tx.run(query.cypher, **query.parameters)), query)
            response["data"] = {"columns": query.columns, "rows": rows[:query.limit]}
            if len(rows) > query.limit:
                incomplete(response, "row_limit")
        # The explicit transaction always rolls back, including exploratory queries.
    selected_ids = set(revisions)
    relation_values, unresolved = edges(revisions)
    if operation == "revision":
        selected_ids = {request["artifact_id"]}
        selected = binding(revisions, request["artifact_id"])
        require(selected["revision_id"] == request["revision_id"], 404,
                "UNKNOWN_IDENTITY", "Revision is not selected by this view.")
        response["data"] = revisions[request["artifact_id"]]
    elif operation in ("work-context", "check"):
        artifact_id = request.get("work_order_id", request.get("artifact_id"))
        selected = binding(revisions, artifact_id)
        with service.projection(snapshot, allow_missing=True) as root:
            output = service.evaluator.cli(root, "check", "--artifact", artifact_id)
            catalog = service.evaluator.catalog(root)
            response["evaluator_output"] = output
            if operation == "check":
                response["data"] = {"artifact": selected}
                selected_ids = {artifact_id} | set(output.get("scope", {}).get("governing", [])) | set(output.get("scope", {}).get("dependencies", []))
            else:
                require("scope" in output, 422, "BINDING_UNAVAILABLE", "Evaluator did not return the selected work scope.", evaluator_output=output)
                scope = output["scope"]
                selected_ids = {artifact_id} | set(scope["governing"]) | set(scope["dependencies"])
                decisions = sorted(a["id"] for a in catalog.values() if a["type"] == "decision" and
                    artifact_id in set(a["relations"].get("concerns", [])) | set(a["relations"].get("blocks", [])))
                response["data"] = {"work_order": selected,
                    "governing_artifacts": [binding(revisions, a) for a in sorted(scope["governing"])],
                    "declared_scope": sorted(scope["declared_paths"]),
                    "dependencies": [binding(revisions, a) for a in sorted(scope["dependencies"])],
                    "relevant_decisions": [binding(revisions, a) for a in decisions]}
                selected_ids.update(decisions)
            bindings = set()
            source_paths = {item["path"] for item in service.evaluator.support["files"]}
            for a in selected_ids:
                if a not in catalog:
                    continue
                metadata = catalog[a]["metadata"]
                bindings.update(metadata.get("evidence_paths", []))
                if metadata.get("evaluator_evidence_path"):
                    bindings.add(metadata["evaluator_evidence_path"])
                for scoped in metadata.get("execution_scope", {}).get("paths", []):
                    if scoped.endswith("/"):
                        bindings.update(item["path"] for item in service.evaluator.support["files"] if item["path"].startswith(scoped))
                    elif scoped in source_paths:
                        bindings.add(scoped)
            missing = []
            for path in sorted(bindings):
                try:
                    contained_file(root, path)
                except Refusal:
                    missing.append(path)
            if missing:
                incomplete(response, "binding_unavailable")
                response["continuation"]["instructions"] += " Missing inputs: " + ", ".join(missing)
    elif operation == "compare":
        right = other["revisions"]
        right_edges, right_missing = edges(right)
        left_values = {canonical_json(e): e for e in relation_values}
        right_values = {canonical_json(e): e for e in right_edges}
        changes = []
        for a in sorted(set(revisions) | set(right)):
            before, after = revisions.get(a, {}).get("revision_id"), right.get(a, {}).get("revision_id")
            if before != after:
                changes.append({"artifact_id": a, "before": before, "after": after})
        response["data"] = {"changes": changes,
            "added_relations": sorted((right_values[k] for k in right_values.keys() - left_values.keys()), key=edge_order),
            "removed_relations": sorted((left_values[k] for k in left_values.keys() - right_values.keys()), key=edge_order)}
        unresolved += right_missing
    elif operation in ("impact", "lineage"):
        artifact_id = request["artifact_id"]
        selected = binding(revisions, artifact_id)
        found, frontier, traversed = {artifact_id}, {artifact_id}, {}
        lineage_kinds = {"assures", "conforms_to", "verifies_work_order", "includes_verification", "releases_work", "verification", "satisfies"}
        eligible = relation_values if operation == "impact" else [e for e in relation_values if e["kind"] in lineage_kinds]
        for depth in range(budget["depth"] + 1):
            next_ids = set()
            for edge in eligible:
                source, target = edge["source"]["artifact_id"], edge["target"]["artifact_id"]
                hit = target in frontier or (operation == "lineage" and source in frontier)
                if not hit:
                    continue
                endpoints = {source, target} - found
                if depth == budget["depth"]:
                    if endpoints:
                        incomplete(response, "depth_limit")
                    continue
                traversed[canonical_json(edge)] = edge
                next_ids.update(endpoints)
            found.update(next_ids)
            frontier = next_ids
            if not frontier:
                break
        selected_ids = found
        response["data"] = {"root": selected, "artifacts": [binding(revisions, a) for a in sorted(found - {artifact_id})],
                            "relations": sorted(traversed.values(), key=edge_order)}
    response["unresolved_references"] = [u for u in unresolved if u["source_artifact_id"] in selected_ids]
    if response["unresolved_references"]:
        incomplete(response, "unresolved_references")
    sources = {canonical_json(r["envelope"]["provenance"]["source"]) for a, r in revisions.items()
               if a in selected_ids and r["envelope"]["provenance"]["kind"] == "git"}
    if operation == "compare":
        sources.update(canonical_json(r["envelope"]["provenance"]["source"]) for r in other["revisions"].values()
                       if r["envelope"]["provenance"]["kind"] == "git")
    response["provenance"] = [json.loads(s) for s in sorted(sources)]
    if service.config.get("test_copy") is True:
        service.wire.validate(response, "read-result-v2.json")
    return constrain(response, budget)

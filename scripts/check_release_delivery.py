#!/usr/bin/env python3
"""Assess retained delivery evidence without publishing or changing formal state."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit


PLAN_SCHEMA = "se-harness-delivery-plan/v1"
COMPLETE_PLAN_SCHEMA = "se-harness-delivery-plan/v2"
COMPLETE_ACTIONS = {"release-integration", "version-tag", "github-release", "pypi",
                    "maintenance-line", "marketplace", "documentation", "pages", "latest", "last", "receipts"}
OBSERVATIONS_SCHEMA = "se-harness-delivery-observations/v1"
RESULT_SCHEMA = "se-harness-delivery-result/v1"
SURFACES = ("evaluator", "marketplace", "documentation", "demonstration", "release_markers")
REQUIRED_EVIDENCE = {
    "evaluator": {"publisher", "public_install"},
    "marketplace": {"assembly", "qualification", "public_ref"},
    "documentation": {"claims_review", "links"},
    "demonstration": {"deployment"},
    "release_markers": {"authorization", "readback"},
}
IDENTITY_FIELDS = {
    "evaluator": {"record", "version", "wheel_sha256"},
    "marketplace": {"plugin_version", "source_commit", "evaluator_version", "wheel_sha256", "public_revision"},
    "documentation": {"commit"},
    "demonstration": {"governance_commit"},
    "release_markers": {"latest", "last"},
}
LIMITATION = ("Assesses supplied, retained observations only. Does not independently run host tests, "
              "authenticate human reviews, or establish live public state. Grants no lifecycle or external authority.")
MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_EVIDENCE_BYTES = 64 * 1024 * 1024


class InvalidInput(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidInput(message)


def object_value(value, location):
    require(isinstance(value, dict), f"{location}: expected an object")
    return value


def text_value(value, location):
    require(isinstance(value, str) and bool(value.strip()) and
            all(ord(char) >= 32 for char in value), f"{location}: expected non-empty text without controls")
    return value


def timestamp(value, location):
    text_value(value, location)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise InvalidInput(f"{location}: expected ISO 8601 timestamp") from error
    require(parsed.tzinfo is not None, f"{location}: timestamp needs a timezone")
    return value


def digest_value(value, location):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value), f"{location}: expected lowercase SHA-256")
    return value


def unique_strings(value, location):
    require(isinstance(value, list) and bool(value), f"{location}: expected a non-empty array")
    for item in value:
        text_value(item, location)
    require(len(set(value)) == len(value), f"{location}: duplicate values")
    return set(value)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise InvalidInput(f"invalid JSON constant: {value}")


def read_json(path, schema):
    with path.open("rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    require(len(raw) <= MAX_JSON_BYTES, f"{path}: JSON exceeds 2 MiB")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates, parse_constant=invalid_constant)
    object_value(value, str(path))
    accepted = {PLAN_SCHEMA, COMPLETE_PLAN_SCHEMA} if schema == PLAN_SCHEMA else {schema}
    require(value.get("schema") in accepted, f"{path}: unsupported schema; expected {schema}")
    return value, hashlib.sha256(raw).hexdigest()


def surface_map(value, location, complete=False):
    require(isinstance(value, list), f"{location}: expected an array")
    result = {}
    for entry in value:
        object_value(entry, location)
        name = text_value(entry.get("id"), location + ".id")
        require(name in SURFACES, f"{location}: unknown surface {name}")
        require(name not in result, f"{location}: duplicate surface {name}")
        result[name] = entry
    if complete:
        require(set(result) == set(SURFACES), f"{location}: missing surfaces {sorted(set(SURFACES) - set(result))}")
    return result


def validate_plan(plan):
    require(plan.get("schema") in {PLAN_SCHEMA, COMPLETE_PLAN_SCHEMA}, "unsupported delivery plan schema")
    release = object_value(plan.get("release"), "release")
    for field in ("contract", "record", "version"):
        text_value(release.get(field), "release." + field)
    digest_value(release.get("wheel_sha256"), "release.wheel_sha256")
    review = object_value(plan.get("review"), "review")
    for field in ("by", "reference"):
        text_value(review.get(field), "review." + field)
    surfaces = surface_map(plan.get("surfaces"), "plan.surfaces", complete=True)
    for name, surface in surfaces.items():
        for field in ("owner", "destination", "work_reference", "next_action"):
            text_value(surface.get(field), name + "." + field)
        disposition = surface.get("disposition")
        require(disposition in ("update", "unchanged", "deferred"), f"{name}: invalid disposition")
        expected = object_value(surface.get("expected"), name + ".expected")
        fields = set(IDENTITY_FIELDS[name])
        if name == "marketplace":
            destination = urlsplit(surface["destination"])
            require(destination.scheme == "https" and destination.hostname and destination.path not in {"", "/"}
                    and destination.fragment and not destination.query and not destination.username
                    and not destination.password, "marketplace.destination: expected HTTPS repository URL with #branch")
            hosts = unique_strings(surface.get("hosts"), "marketplace.hosts")
            require(hosts <= {"codex", "claude-code"}, "marketplace.hosts: unsupported host")
            fields.update(host + "_content_sha256" for host in hosts)
        require(fields <= expected.keys(), f"{name}: missing expected identity fields {sorted(fields - expected.keys())}")
        for key, value in expected.items():
            text_value(key, name + ".expected key")
            if value is not None:
                text_value(value, name + ".expected." + key)
                if key.endswith("sha256"):
                    digest_value(value, name + ".expected." + key)
                derived = (plan.get("schema") == COMPLETE_PLAN_SCHEMA and name == "demonstration"
                           and key == "governance_commit" and value == "release-governance")
                if not derived and (key.endswith("commit") or key == "public_revision" or (name == "release_markers" and key == "last")):
                    require(re.fullmatch(r"[0-9a-f]{40}", value), name + ".expected." + key + ": expected full commit ID")
        minimum = REQUIRED_EVIDENCE[name] if disposition == "update" else {"readback", "compatibility"} if disposition == "unchanged" else {"deferral"}
        required = unique_strings(surface.get("required_observations"), name + ".required_observations")
        require(minimum <= required, f"{name}: missing required observations {sorted(minimum - required)}")
        if disposition in {"unchanged", "deferred"}:
            field = "compatibility" if disposition == "unchanged" else "deferral"
            detail = object_value(surface.get(field), name + "." + field)
            for key in (("reason", "review_reference") if field == "compatibility" else
                        ("reason", "decision_reference", "follow_up", "revisit")):
                text_value(detail.get(key), name + "." + field + "." + key)
    for surface, keys in (("evaluator", {"record": "record", "version": "version", "wheel_sha256": "wheel_sha256"}),
                          ("marketplace", {"evaluator_version": "version", "wheel_sha256": "wheel_sha256"})):
        # A deliberately unchanged older plugin may bundle an older compatible evaluator.
        if surfaces[surface]["disposition"] == "update":
            for field, release_field in keys.items():
                require(surfaces[surface]["expected"][field] == release[release_field],
                        f"{surface}.expected.{field}: disagrees with selected release")
    if plan["schema"] == COMPLETE_PLAN_SCHEMA:
        validate_complete_release(plan, surfaces)
    else:
        require("complete_release" not in plan, "legacy plan cannot declare complete-release authority")
    return surfaces


def repository_path(value, location):
    text_value(value, location)
    require(not any(c in value for c in ("\\", ":", "\x00")) and
            not any(p in {"", ".", ".."} for p in value.split("/")), location + ": unsafe repository path")
    return value


def commit_value(value, location):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value), location + ": expected full commit ID")
    return value


def validate_complete_release(plan, surfaces):
    """Validate a reviewed envelope, not the identity or authority of its author."""
    value = object_value(plan.get("complete_release"), "complete_release")
    require(set(value) == {"repository", "candidate_commit", "actions", "marketplace", "markers",
                           "integration", "readiness", "observations", "evidence_root", "documentation"}, "complete_release: unexpected field set")
    require(value["repository"] == "mmzen/se_harness", "complete_release: unsupported repository")
    commit_value(value["candidate_commit"], "candidate_commit")
    require(unique_strings(value["actions"], "actions") == COMPLETE_ACTIONS, "complete_release: incomplete or extra action")
    require(all(s["disposition"] == "update" for s in surfaces.values()), "complete release requires all five updated surfaces")
    require(all(v is not None for s in surfaces.values() for v in s["expected"].values()), "complete release has unresolved identities")
    require(set(surfaces["marketplace"]["hosts"]) == {"codex", "claude-code"}, "complete release needs both hosts")
    expected_destinations = {
        "evaluator": "https://pypi.org/project/se-harness/" + plan["release"]["version"] + "/",
        "marketplace": "https://github.com/mmzen/se_harness.git#plugin-marketplace",
        "documentation": "https://github.com/mmzen/se_harness/tree/main",
        "demonstration": "https://mmzen.github.io/se_harness/",
        "release_markers": "https://github.com/mmzen/se_harness",
    }
    for name, destination in expected_destinations.items():
        require(surfaces[name]["destination"] == destination, name + ": unapproved destination")
    docs = object_value(value["documentation"], "documentation")
    require(bool(docs), "documentation: exact reviewed files are required")
    for path, digest in docs.items():
        repository_path(path, "documentation path")
        require(path == "README.md" or path.startswith("docs/"), "documentation: unsupported path")
        digest_value(digest, "documentation file digest")
    market = object_value(value["marketplace"], "complete_release.marketplace")
    require(set(market) == {"parent", "commit", "tree", "identity_sha256"}, "marketplace: unexpected field set")
    for key in ("parent", "commit", "tree"):
        commit_value(market[key], "marketplace." + key)
    digest_value(market["identity_sha256"], "marketplace.identity_sha256")
    require(market["parent"] != market["commit"], "marketplace must be a new child commit")
    require(surfaces["marketplace"]["expected"]["public_revision"] == market["commit"], "marketplace revision differs")
    require(surfaces["marketplace"]["expected"]["source_commit"] == value["candidate_commit"], "marketplace source differs")
    markers = object_value(value["markers"], "markers")
    require(set(markers) == {"previous_latest", "previous_last"}, "markers: unexpected field set")
    if markers["previous_last"] is not None:
        commit_value(markers["previous_last"], "markers.previous_last")
    if markers["previous_latest"] is not None:
        require(isinstance(markers["previous_latest"], str) and re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", markers["previous_latest"]), "invalid previous_latest")
    require(surfaces["release_markers"]["expected"] == {"latest": "v" + plan["release"]["version"], "last": value["candidate_commit"]}, "marker targets differ")
    integration = object_value(value["integration"], "integration")
    require(set(integration) == {"decision_paths", "receipt_paths"}, "integration: unexpected field set")
    for key in ("decision_paths", "receipt_paths"):
        paths = unique_strings(integration[key], "integration." + key)
        for path in paths:
            repository_path(path, "integration path")
            require(path.startswith("docs/engineering/"), "integration limited to formal decision and evidence paths")
            if key == "receipt_paths":
                require("/evidence/" in path and path.endswith(".json"), "receipt must be a named evidence JSON file")
    readiness = object_value(value["readiness"], "readiness")
    require(set(readiness) == {"path", "sha256"}, "readiness: unexpected field set")
    repository_path(readiness["path"], "readiness.path")
    digest_value(readiness["sha256"], "readiness.sha256")
    for key in ("observations", "evidence_root"):
        repository_path(value[key], key)
        require(value[key].startswith("docs/engineering/") and "/evidence/" in value[key], key + ": must be retained evidence")


def issue(code, location, message, **details):
    return {"code": code, "location": location, "message": message, **details}


def compare(expected, observed, location):
    findings = []
    for field, value in expected.items():
        if value is None:
            findings.append(issue("pending", location + "." + field, "Expected identity is not yet selected"))
        elif observed.get(field) != value:
            findings.append(issue("mismatch", location + "." + field, "Identity differs", expected=value, observed=observed.get(field)))
    return findings


def check_evidence(entries, root, location):
    if entries is None or entries == []:
        return [issue("missing", location, "Retained evidence is required")]
    require(isinstance(entries, list), f"{location}: expected an evidence array")
    findings = []
    for entry in entries:
        object_value(entry, location)
        name = text_value(entry.get("path"), location + ".path")
        expected = digest_value(entry.get("sha256"), location + ".sha256")
        parts = name.split("/")
        require(not any(part in {"", ".", ".."} for part in parts) and
                not any(char in name for char in ("\\", ":")) and not PurePosixPath(name).is_absolute(),
                f"{location}: evidence path must stay inside the evidence root: {name}")
        try:
            path = (root / name).resolve()
            require(path.is_relative_to(root), f"{location}: evidence escapes root: {name}")
            require(path.is_file() or not path.exists(), f"{location}: evidence is not a regular file: {name}")
            with path.open("rb") as stream:
                digest = hashlib.sha256()
                total = 0
                while block := stream.read(1024 * 1024):
                    total += len(block)
                    require(total <= MAX_EVIDENCE_BYTES, f"{location}: evidence exceeds 64 MiB: {name}")
                    digest.update(block)
            if digest.hexdigest() != expected:
                findings.append(issue("mismatch", location, "Evidence digest differs", path=name,
                                      expected=expected, observed=digest.hexdigest()))
        except OSError as error:
            findings.append(issue("missing", location, "Evidence unavailable", path=name, detail=str(error)))
    return findings


def check_routes(surface, observed, root):
    routes = observed.get("routes", [])
    require(isinstance(routes, list), "marketplace.routes: expected an array")
    seen = {}
    findings = []
    for route in routes:
        object_value(route, "route")
        host, kind = route.get("host"), route.get("kind")
        require(host in surface["hosts"] and kind in ("fresh", "update"), "route: unsupported host or kind")
        require((host, kind) not in seen, f"route: duplicate {host}/{kind}")
        seen[host, kind] = route
        name = f"marketplace.routes.{host}.{kind}"
        timestamp(route.get("observed_at"), name + ".observed_at")
        text_value(route.get("host_version"), name + ".host_version")
        if kind == "update":
            for key in ("starting_version", "starting_source"):
                text_value(route.get(key), name + "." + key)
        expected = surface["expected"]
        findings += compare({"source": surface["destination"], "revision": expected["public_revision"],
                             "plugin_version": expected["plugin_version"],
                             "content_sha256": expected[host + "_content_sha256"],
                             "evaluator_version": expected["evaluator_version"], "wheel_sha256": expected["wheel_sha256"]}, route, name)
        require(route.get("status") in ("pass", "failed", "pending"), name + ": invalid status")
        if route["status"] != "pass":
            findings.append(issue(route["status"], name, "Public route has not passed"))
        findings += check_evidence(route.get("evidence"), root, name)
    for host in surface["hosts"]:
        for kind in ("fresh", "update"):
            if (host, kind) not in seen:
                findings.append(issue("missing", f"marketplace.routes.{host}.{kind}", "Public installation observation missing"))
    return findings


def assess(plan_path, observations_path, evidence_root, *, governance_commit=None, before_markers=False):
    result = {"schema": RESULT_SCHEMA, "status": "incomplete", "input_status": "valid",
              "authority": "derived operational evidence; no lifecycle transition",
              "limitation": LIMITATION, "formal_release": None, "evaluator_publication": "unobserved",
              "observed_at": None, "surfaces": [], "findings": []}
    try:
        plan, plan_digest = read_json(plan_path, PLAN_SCHEMA)
        surfaces = validate_plan(plan)
        if plan["schema"] == COMPLETE_PLAN_SCHEMA:
            commit_value(governance_commit, "resolved release governance commit")
            if surfaces["demonstration"]["expected"]["governance_commit"] == "release-governance":
                surfaces["demonstration"]["expected"]["governance_commit"] = governance_commit
        else:
            require(not before_markers, "legacy report cannot authorize marker continuation")
        observations, _ = read_json(observations_path, OBSERVATIONS_SCHEMA)
        result["plan_sha256"] = plan_digest
        result["observed_at"] = timestamp(observations.get("observed_at"), "observed_at")
        digest_value(observations.get("plan_sha256"), "observations.plan_sha256")
        if observations["plan_sha256"] != plan_digest:
            result["findings"].append(issue("mismatch", "plan_sha256", "Observations bind another plan",
                                            expected=plan_digest, observed=observations["plan_sha256"]))
        root = evidence_root.resolve(strict=True)
        require(root.is_dir(), "evidence root must be a directory")
        release = object_value(observations.get("release"), "observations.release")
        for field in ("record", "status", "source"):
            text_value(release.get(field), "observations.release." + field)
        timestamp(release.get("observed_at"), "observations.release.observed_at")
        result["formal_release"] = release
        result["findings"] += compare({"record": plan["release"]["record"], "status": "released"}, release, "release")
        result["findings"] += check_evidence(release.get("evidence"), root, "release.evidence")
        observed_surfaces = surface_map(observations.get("surfaces"), "observations.surfaces")
        for name in SURFACES:
            surface = surfaces[name]
            observed = observed_surfaces.get(name)
            findings = []
            if observed is None:
                findings.append(issue("missing", name, "Surface not observed"))
            else:
                require(observed.get("status") in ("pass", "failed", "pending"), name + ": invalid observed status")
                timestamp(observed.get("observed_at"), name + ".observed_at")
                text_value(observed.get("source"), name + ".source")
                if observed["status"] != "pass":
                    findings.append(issue(observed["status"], name, "Surface has not passed"))
                findings += compare({"source": surface["destination"]}, observed, name)
                identity = object_value(observed.get("identity"), name + ".identity")
                findings += compare(surface["expected"], identity, name + ".identity")
                evidence = object_value(observed.get("evidence"), name + ".evidence")
                for required in surface["required_observations"]:
                    findings += check_evidence(evidence.get(required), root, name + ".evidence." + required)
                if name == "marketplace" and surface["disposition"] == "update":
                    findings += check_routes(surface, observed, root)
            if surface["disposition"] == "deferred":
                findings.append(issue("deferred", name, "Deferral remains outstanding", **surface["deferral"]))
            status = ("satisfied" if not findings else "deferred" if surface["disposition"] == "deferred" else
                      "failed" if any(f["code"] in {"failed", "mismatch"} for f in findings) else "pending")
            row = {"id": name, "disposition": surface["disposition"], "status": status,
                   "owner": surface["owner"], "next_action": surface["next_action"],
                   "expected": surface["expected"], "observation": observed, "findings": findings}
            result["surfaces"].append(row)
            if name == "evaluator":
                result["evaluator_publication"] = status
        assessed = [row for row in result["surfaces"] if not (before_markers and row["id"] == "release_markers")]
        if before_markers and not result["findings"] and all(row["status"] == "satisfied" for row in assessed):
            result["status"] = "ready_for_markers"
        elif not result["findings"] and all(row["status"] == "satisfied" for row in result["surfaces"]):
            result["status"] = "complete"
        return result, 0 if result["status"] in {"complete", "ready_for_markers"} else 1
    except (InvalidInput, OSError, ValueError, RecursionError) as error:
        result["input_status"] = "invalid"
        result["findings"].append(issue("invalid_input", "input", str(error)))
        return result, 2


def render(result):
    lines = [f"Delivery: {result['status']} (inputs: {result['input_status']})",
             f"Formal release: {(result['formal_release'] or {}).get('status', 'unobserved')}",
             f"Evaluator publication: {result['evaluator_publication']}",
             f"Observations: {result['observed_at'] or 'unavailable'}", result["limitation"]]
    for row in result["surfaces"]:
        lines.append(f"{row['id']}: {row['status']}; owner: {row['owner']}; next: {row['next_action']}")
        for finding in row["findings"]:
            lines.append("  " + json.dumps(finding, ensure_ascii=True))
    lines.extend(json.dumps(finding, ensure_ascii=True) for finding in result["findings"])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--governance-commit", help="Resolved release integration commit for a v2 plan")
    parser.add_argument("--before-markers", action="store_true", help="Report marker readiness; never report complete")
    parser.add_argument("--json", action="store_true", help="JSON on stdout; human report on stderr")
    args = parser.parse_args(argv)
    result, code = assess(args.plan, args.observations, args.evidence_root,
                          governance_commit=args.governance_commit, before_markers=args.before_markers)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
        print(render(result), file=sys.stderr)
    else:
        print(render(result))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

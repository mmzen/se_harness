"""No-network, dual-runtime rehearsal of a predecessor-to-successor handover."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Mapping

from se_harness.governance_migration_contract import (
    CONTRACT_SCHEMA,
    RESULT_SCHEMA,
    STAGE_ORDER,
    MigrationContractError,
    canonical_json,
    classify_migration,
    load_migration_contract,
    load_migration_scenario,
    migration_contract_bytes,
    sha256_bytes,
)


REPORT_NAME = "governance-migration-result.json"
RUNTIME_PROBE = r'''import hashlib,json,platform,site,sys
from pathlib import Path
import se_harness
root=Path(se_harness.__file__).resolve().parent
entries=[]
for path in sorted(root.rglob("*"),key=lambda item:item.as_posix()):
    if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts and path.suffix!=".pyc":
        relative=path.relative_to(root).as_posix()
        raw=path.read_bytes()
        entries.append({"path":relative,"sha256":hashlib.sha256(raw).hexdigest(),"size":len(raw)})
try:
    from se_harness.evaluator_identity import installed_evaluator_identity
    evaluator=installed_evaluator_identity()
    archive_name=evaluator.archive_name
    archive_sha256=evaluator.archive_sha256
    payload_sha256=evaluator.payload_sha256
except Exception:
    archive_name=archive_sha256=payload_sha256=None
if archive_sha256 is None:
    try:
        import importlib.metadata
        from urllib.parse import unquote,urlparse
        distribution=importlib.metadata.distribution("se-harness")
        direct=json.loads(distribution.read_text("direct_url.json"))
        archive=direct.get("archive_info",{})
        hashes=archive.get("hashes",{})
        archive_sha256=hashes.get("sha256")
        if archive_sha256 is None and isinstance(archive.get("hash"),str) and archive["hash"].startswith("sha256="):
            archive_sha256=archive["hash"].removeprefix("sha256=")
        archive_name=Path(unquote(urlparse(direct["url"]).path)).name
    except Exception:
        archive_name=archive_sha256=None
payload={"archive_name":archive_name,"archive_sha256":archive_sha256,"isolated":bool(sys.flags.isolated),"module_origin":str(root),"package_tree_sha256":hashlib.sha256((json.dumps(entries,ensure_ascii=True,separators=(",",":"),sort_keys=True)+"\n").encode("utf-8")).hexdigest(),"payload_sha256":payload_sha256,"python_prefix":str(Path(sys.prefix).resolve()),"python_version":platform.python_version(),"search_paths":[str(Path(item or ".").resolve()) for item in sys.path if isinstance(item,str)],"user_site_enabled":bool(site.ENABLE_USER_SITE),"version":str(se_harness.__version__)}
print(json.dumps(payload,ensure_ascii=True,separators=(",",":"),sort_keys=True))'''


class GovernanceMigrationError(RuntimeError):
    """The migration rehearsal cannot preserve its declared safety boundary."""


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise GovernanceMigrationError(f"MIG401: disposable state is unreadable: {path.name}") from exc
    if not isinstance(value, dict):
        raise GovernanceMigrationError(f"MIG402: disposable state is not an object: {path.name}")
    return value


def _resolved(path: Path, *, strict: bool = False) -> Path:
    try:
        return path.expanduser().resolve(strict=strict)
    except OSError as exc:
        raise GovernanceMigrationError(f"MIG201: cannot resolve path: {path}") from exc


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def _within(path: Path, boundary: Path) -> bool:
    try:
        _resolved(path).relative_to(_resolved(boundary))
    except ValueError:
        return False
    return True


def _lexically_within(path: Path, boundary: Path) -> bool:
    try:
        _absolute(path).relative_to(_absolute(boundary))
    except ValueError:
        return False
    return True


def _assert_external(path: Path, repository: Path, label: str) -> None:
    if _lexically_within(path, repository) or _within(path, repository):
        raise GovernanceMigrationError(f"MIG202: {label} must be outside the operational checkout")


def _snapshot_tree(root: Path, *, exclude_git: bool = False) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    if not root.exists():
        return {"files": {}, "sha256": sha256_bytes(canonical_json([]))}
    files: dict[str, str] = {}
    try:
        candidates = sorted(root.rglob("*"), key=lambda item: item.as_posix())
        for path in candidates:
            relative = path.relative_to(root)
            if exclude_git and relative.parts and relative.parts[0] == ".git":
                continue
            name = relative.as_posix()
            if path.is_symlink():
                target = os.readlink(path)
                digest = sha256_bytes(target.encode("utf-8", errors="surrogateescape"))
                entries.append({"kind": "link", "path": name, "sha256": digest})
                files[name] = f"link:{digest}"
            elif path.is_file():
                raw = path.read_bytes()
                digest = sha256_bytes(raw)
                entries.append({"kind": "file", "path": name, "sha256": digest, "size": len(raw)})
                files[name] = f"file:{digest}:{len(raw)}"
    except OSError as exc:
        raise GovernanceMigrationError(f"MIG203: cannot snapshot {root.name}: {type(exc).__name__}") from exc
    return {"files": files, "sha256": sha256_bytes(canonical_json(entries))}


def _git_identity(repository: Path) -> dict[str, Any]:
    git = shutil.which("git")
    if git is None:
        return {"available": False, "head": None, "refs_sha256": None}
    commands = (
        ("head", ["rev-parse", "--verify", "HEAD"]),
        ("refs", ["for-each-ref", "--format=%(refname)%00%(objectname)"]),
    )
    values: dict[str, str] = {}
    for label, argv in commands:
        completed = subprocess.run(
            [git, "-c", f"safe.directory={repository.as_posix()}", "-C", str(repository), *argv],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if completed.returncode != 0:
            return {"available": False, "head": None, "refs_sha256": None}
        values[label] = completed.stdout.replace("\r\n", "\n").strip()
    return {
        "available": True,
        "head": values["head"],
        "refs_sha256": sha256_bytes((values["refs"] + "\n").encode("utf-8")),
    }


def _operational_identity(repository: Path) -> dict[str, Any]:
    source = _snapshot_tree(repository, exclude_git=True)
    git = _git_identity(repository)
    return {
        "git_available": git["available"],
        "git_head": git["head"],
        "git_refs_sha256": git["refs_sha256"],
        "source_sha256": source["sha256"],
    }


def _minimal_child_environment(output: Path) -> dict[str, str]:
    selected: dict[str, str] = {
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
    }
    for name in ("COMSPEC", "LANG", "LC_ALL", "SYSTEMROOT", "TEMP", "TMP", "WINDIR"):
        value = os.environ.get(name)
        if value:
            selected[name] = value
    selected["TEMP"] = str(output)
    selected["TMP"] = str(output)
    return selected


def _runtime_identity(
    python: Path,
    *,
    role: str,
    expected_version: str,
    expectation: Mapping[str, Any],
    repository: Path,
    output: Path,
    contract: Mapping[str, Any],
) -> tuple[dict[str, Any], Path, tuple[Path, ...], Path]:
    lexical = _absolute(python)
    if not lexical.is_file():
        raise GovernanceMigrationError(f"MIG204: {role} Python is not an existing file")
    _assert_external(lexical, repository, f"{role} Python")
    environment_root = lexical.parent.parent
    if any(parent.is_symlink() for parent in (environment_root, lexical.parent)):
        raise GovernanceMigrationError(f"MIG205: {role} environment parent must not be linked")
    executable_raw = lexical.resolve().read_bytes()
    try:
        completed = subprocess.run(
            [str(lexical), "-I", "-B", "-c", RUNTIME_PROBE],
            cwd=output,
            env=_minimal_child_environment(output),
            check=False,
            capture_output=True,
            timeout=contract["limits"]["subprocess_timeout_seconds"],
        )
    except subprocess.TimeoutExpired as exc:
        raise GovernanceMigrationError(f"MIG206: {role} runtime identity timed out") from exc
    if len(completed.stdout) > contract["limits"]["max_child_output_bytes"] or len(completed.stderr) > contract["limits"]["max_child_output_bytes"]:
        raise GovernanceMigrationError(f"MIG207: {role} runtime identity exceeded the output bound")
    if completed.returncode != 0:
        raise GovernanceMigrationError(f"MIG208: {role} runtime identity failed")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise GovernanceMigrationError(f"MIG209: {role} runtime identity is malformed") from exc
    expected_fields = {
        "isolated",
        "archive_name",
        "archive_sha256",
        "module_origin",
        "package_tree_sha256",
        "payload_sha256",
        "python_prefix",
        "python_version",
        "search_paths",
        "user_site_enabled",
        "version",
    }
    if not isinstance(payload, dict) or set(payload) != expected_fields:
        raise GovernanceMigrationError(f"MIG210: {role} runtime identity fields differ from the protocol")
    if payload["version"] != expected_version:
        raise GovernanceMigrationError(f"MIG211: {role} version differs from the scenario")
    if expectation["version"] != expected_version:
        raise GovernanceMigrationError(f"MIG228: {role} runtime expectation is internally inconsistent")
    if expectation["archive_sha256"] is not None and (
        payload["archive_name"] != expectation["archive_name"]
        or payload["archive_sha256"] != expectation["archive_sha256"]
    ):
        raise GovernanceMigrationError(f"MIG229: {role} installed archive differs from the scenario")
    if payload["isolated"] is not True or payload["user_site_enabled"] is not False:
        raise GovernanceMigrationError(f"MIG212: {role} runtime is not isolated")
    module_origin = _resolved(Path(payload["module_origin"]), strict=True)
    prefix = _resolved(Path(payload["python_prefix"]), strict=True)
    if not _within(module_origin, environment_root) or prefix != _resolved(environment_root, strict=True):
        raise GovernanceMigrationError(f"MIG213: {role} package is outside its declared environment")
    _assert_external(module_origin, repository, f"{role} package")
    if not isinstance(payload["search_paths"], list) or not all(
        isinstance(item, str) and item for item in payload["search_paths"]
    ):
        raise GovernanceMigrationError(f"MIG214: {role} import-search report is invalid")
    search_paths = tuple(_resolved(Path(item)) for item in payload["search_paths"])
    if any(_within(item, repository) for item in search_paths):
        raise GovernanceMigrationError(f"MIG225: {role} import search contains the checkout")
    package_digest = payload["package_tree_sha256"]
    if not isinstance(package_digest, str) or len(package_digest) != 64 or any(
        character not in "0123456789abcdef" for character in package_digest
    ):
        raise GovernanceMigrationError(f"MIG226: {role} package identity digest is invalid")
    return (
        {
            "checkout_excluded": True,
            "archive_name": payload["archive_name"],
            "archive_sha256": payload["archive_sha256"],
            "executable_sha256": sha256_bytes(executable_raw),
            "isolated": True,
            "package_tree_sha256": package_digest,
            "payload_sha256": payload["payload_sha256"],
            "python_version": payload["python_version"],
            "role": role,
            "version": payload["version"],
        },
        module_origin,
        search_paths,
        _resolved(environment_root, strict=True),
    )


def _implementation_identity(contract: Mapping[str, Any]) -> str:
    path = Path(__file__)
    digest = sha256_bytes(path.read_bytes())
    for adapter_id, adapter in contract["adapters"].items():
        if adapter["implementation_path"] != path.name or adapter["implementation_sha256"] != digest:
            raise GovernanceMigrationError(
                f"MIG215: adapter implementation identity mismatch: {adapter_id}"
            )
    return digest


def _workspace_changes(before: Mapping[str, Any], after: Mapping[str, Any]) -> list[str]:
    names = set(before["files"]) | set(after["files"])
    return sorted(name for name in names if before["files"].get(name) != after["files"].get(name))


def _mutation_kind(path: str) -> str:
    exact = {
        "plans/publication-plan.json": "disposable-publication-plan",
        "plans/release-plan.json": "disposable-release-plan",
        "render/governance-snapshot.json": "disposable-render",
        "state/graph.json": "disposable-graph",
        "state/root.json": "disposable-root",
        "state/simulated-publication.json": "simulated-publication",
    }
    return exact.get(path, "undeclared")


def _proposal_validation(proposal: Mapping[str, Any]) -> dict[str, Any]:
    codes: list[str] = []
    if proposal.get("schema") != 3:
        codes.append("unsupported-release-record-schema")
    if proposal.get("evaluator_evidence") is not True:
        codes.append("missing-evaluator-evidence")
    return {
        "codes": sorted(codes),
        "outcome": "valid" if not codes else "migration-required",
    }


def _decision_by_id(scenario: Mapping[str, Any], fixture_id: str) -> dict[str, Any]:
    return next(item for item in scenario["decisions"] if item["id"] == fixture_id)


def _stage_prepare(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    fixture = scenario["fixture"]
    graph = {
        "active_proposal": fixture["initial_proposal"],
        "history": [],
        "selected_release": None,
    }
    root = {
        "evaluator": "predecessor",
        "version": scenario["versions"]["predecessor"],
    }
    _atomic_write(workspace / "state/graph.json", canonical_json(graph))
    _atomic_write(workspace / "state/root.json", canonical_json(root))
    return {"prepared_proposal": graph["active_proposal"]["artifact_id"]}


def _stage_validate_complete(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    graph = _read_json(workspace / "state/graph.json")
    active = graph.get("active_proposal")
    if not isinstance(active, dict):
        raise GovernanceMigrationError("MIG403: complete validation has no active proposal")
    validation = _proposal_validation(active)
    historical = scenario["scenario_id"].startswith("historical-")
    if historical and validation["outcome"] != "migration-required":
        raise GovernanceMigrationError("MIG404: historical fixture did not reproduce the successor boundary")
    return {"claim": "complete-successor-validation", "validation": validation}


def _stage_reject(workspace: Path, scenario: Mapping[str, Any], stage: Mapping[str, Any]) -> dict[str, Any]:
    decision = _decision_by_id(scenario, stage["decision_fixture"])
    graph = _read_json(workspace / "state/graph.json")
    active = graph.get("active_proposal")
    if not isinstance(active, dict) or active.get("artifact_id") != decision["artifact_id"]:
        raise GovernanceMigrationError("MIG405: rejection fixture does not match the active proposal")
    rejected = dict(active)
    rejected["status"] = "rejected"
    rejected["decision_fixture_sha256"] = decision["sha256"]
    graph["active_proposal"] = None
    graph["history"] = [rejected]
    _atomic_write(workspace / "state/graph.json", canonical_json(graph))
    return {
        "decision_fixture_sha256": decision["sha256"],
        "rejected_history_sha256": sha256_bytes(canonical_json(rejected)),
    }


def _stage_replace(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    graph = _read_json(workspace / "state/graph.json")
    history = graph.get("history")
    if not isinstance(history, list) or len(history) != 1 or history[0].get("status") != "rejected":
        raise GovernanceMigrationError("MIG406: replacement requires one immutable rejected predecessor proposal")
    rejected_before = sha256_bytes(canonical_json(history[0]))
    replacement = scenario["fixture"]["replacement_proposal"]
    if _proposal_validation(replacement)["outcome"] != "valid":
        raise GovernanceMigrationError("MIG407: corrected successor proposal is not complete")
    graph["active_proposal"] = replacement
    _atomic_write(workspace / "state/graph.json", canonical_json(graph))
    reread = _read_json(workspace / "state/graph.json")
    if sha256_bytes(canonical_json(reread["history"][0])) != rejected_before:
        raise GovernanceMigrationError("MIG408: replacement changed rejected history")
    return {
        "active_proposal": replacement["artifact_id"],
        "rejected_history_immutable": True,
        "rejected_history_sha256": rejected_before,
    }


def _stage_assess(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    graph = _read_json(workspace / "state/graph.json")
    active = graph.get("active_proposal")
    history = graph.get("history")
    if not isinstance(active, dict) or _proposal_validation(active)["outcome"] != "valid":
        raise GovernanceMigrationError("MIG409: assessment requires a complete corrected proposal")
    if not isinstance(history, list) or len(history) != 1:
        raise GovernanceMigrationError("MIG410: assessment lost rejected history")
    complete = {
        "claim": "complete-successor-validation",
        "graph_sha256": sha256_bytes(canonical_json(graph)),
        "outcome": "pass",
    }
    compatible_view = {"active_proposal": active, "selected_release": graph["selected_release"]}
    compatible = {
        "claim": "predecessor-compatible-view",
        "outcome": "pass",
        "view_sha256": sha256_bytes(canonical_json(compatible_view)),
    }
    predecessor_full = (
        "pass"
        if scenario["fixture"]["predecessor_accepts_rejected"]
        else "refused-unsupported-rejected-state"
    )
    return {
        "complete": complete,
        "compatible": compatible,
        "predecessor_complete_graph": predecessor_full,
    }


def _stage_release_plan(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    graph = _read_json(workspace / "state/graph.json")
    active = graph.get("active_proposal")
    if not isinstance(active, dict) or _proposal_validation(active)["outcome"] != "valid":
        raise GovernanceMigrationError("MIG411: release planning requires the complete replacement")
    plan = {
        "candidate_authority": False,
        "proposal": active["artifact_id"],
        "tag_name": f"v{active['version']}",
        "version": active["version"],
    }
    _atomic_write(workspace / "plans/release-plan.json", canonical_json(plan))
    return {"plan_sha256": sha256_bytes(canonical_json(plan)), "planning_only": True}


def _stage_publish_plan(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    release = _read_json(workspace / "plans/release-plan.json")
    plan = {
        "credentials_required": False,
        "immutable_candidate": release["proposal"],
        "publication_performed": False,
        "tag_name": release["tag_name"],
    }
    _atomic_write(workspace / "plans/publication-plan.json", canonical_json(plan))
    return {"plan_sha256": sha256_bytes(canonical_json(plan)), "planning_only": True}


def _stage_render(workspace: Path, scenario: Mapping[str, Any]) -> dict[str, Any]:
    graph = _read_json(workspace / "state/graph.json")
    publication = _read_json(workspace / "plans/publication-plan.json")
    rendered = {
        "active_proposal": graph["active_proposal"]["artifact_id"],
        "rejected_history": [item["artifact_id"] for item in graph["history"]],
        "selected_tag": publication["tag_name"],
    }
    _atomic_write(workspace / "render/governance-snapshot.json", canonical_json(rendered))
    return {
        "render_sha256": sha256_bytes(canonical_json(rendered)),
        "selected_corrected_proposal": True,
    }


def _stage_adopt(workspace: Path, scenario: Mapping[str, Any], stage: Mapping[str, Any]) -> dict[str, Any]:
    decision = _decision_by_id(scenario, stage["decision_fixture"])
    graph = _read_json(workspace / "state/graph.json")
    active = graph.get("active_proposal")
    root_path = workspace / "state/root.json"
    root_before = root_path.read_bytes()
    if not isinstance(active, dict) or active["artifact_id"] != decision["artifact_id"]:
        raise GovernanceMigrationError("MIG412: adoption fixture does not select the corrected proposal")
    publication = {
        "artifact_id": active["artifact_id"],
        "immutable": True,
        "version": active["version"],
    }
    publication_sha256 = sha256_bytes(canonical_json(publication))
    if publication_sha256 != scenario["fixture"]["simulated_publication_sha256"]:
        raise GovernanceMigrationError("MIG413: simulated immutable publication identity mismatch")
    successor_root = {"evaluator": "successor", "version": scenario["versions"]["successor"]}

    _atomic_write(root_path, canonical_json(successor_root))
    _atomic_write(root_path, root_before)
    rollback_exact = root_path.read_bytes() == root_before
    if not rollback_exact:
        raise GovernanceMigrationError("MIG414: interrupted disposable adoption did not roll back")
    _atomic_write(workspace / "state/simulated-publication.json", canonical_json(publication))
    _atomic_write(root_path, canonical_json(successor_root))
    before_replay = root_path.read_bytes()
    _atomic_write(root_path, canonical_json(successor_root))
    noop_replay = root_path.read_bytes() == before_replay
    return {
        "decision_fixture_sha256": decision["sha256"],
        "noop_replay": noop_replay,
        "publication_sha256": publication_sha256,
        "rollback_exact": rollback_exact,
    }


STAGE_DRIVERS = {
    "prepare": lambda root, scenario, stage: _stage_prepare(root, scenario),
    "validate-complete": lambda root, scenario, stage: _stage_validate_complete(root, scenario),
    "reject": _stage_reject,
    "replace": lambda root, scenario, stage: _stage_replace(root, scenario),
    "assess": lambda root, scenario, stage: _stage_assess(root, scenario),
    "release-plan": lambda root, scenario, stage: _stage_release_plan(root, scenario),
    "publish-plan": lambda root, scenario, stage: _stage_publish_plan(root, scenario),
    "render": lambda root, scenario, stage: _stage_render(root, scenario),
    "adopt": _stage_adopt,
}


def _selected_evaluator(workspace: Path) -> str | None:
    path = workspace / "state/root.json"
    if not path.is_file():
        return None
    value = _read_json(path).get("evaluator")
    return value if isinstance(value, str) else None


def _decision_binding(scenario: Mapping[str, Any], stage: Mapping[str, Any]) -> dict[str, Any] | None:
    fixture_id = stage["decision_fixture"]
    if fixture_id is None:
        return None
    decision = _decision_by_id(scenario, fixture_id)
    return {"id": fixture_id, "sha256": decision["sha256"], "type": decision["type"]}


def _command_identity(stage: Mapping[str, Any], implementation_sha256: str) -> str:
    return sha256_bytes(
        canonical_json(
            {
                "adapter": stage["adapter"],
                "driver": f"governance-migration-{stage['id']}-v1",
                "implementation_sha256": implementation_sha256,
                "technical_role": stage["technical_role"],
            }
        )
    )


def _not_run_stage(
    stage: Mapping[str, Any],
    scenario: Mapping[str, Any],
    contract: Mapping[str, Any],
    implementation_sha256: str,
) -> dict[str, Any]:
    return {
        "authority_effect": "none",
        "command_identity": _command_identity(stage, implementation_sha256),
        "decision_fixture": _decision_binding(scenario, stage),
        "diagnostic": None,
        "duration_ms": 0,
        "evaluator_role": stage["technical_role"],
        "id": stage["id"],
        "input_view_sha256": None,
        "observed_mutations": [],
        "permitted_mutations": contract["stages"][stage["id"]]["permitted_mutations"],
        "report_sha256": None,
        "report": None,
        "result": "not-run",
        "target_view": stage["view"],
    }


def _semantic_value(result: Mapping[str, Any]) -> dict[str, Any]:
    def clean(value: Any, key: str | None = None) -> Any:
        if key in {
            "archive_sha256",
            "duration_ms",
            "executable_sha256",
            "package_tree_sha256",
            "payload_sha256",
            "python_version",
            "source_sha256",
        }:
            return None
        if key == "host":
            return None
        if isinstance(value, dict):
            return {
                item_key: clean(item_value, item_key)
                for item_key, item_value in value.items()
                if item_key != "semantic_sha256" and clean(item_value, item_key) is not None
            }
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value

    return clean(dict(result))


def verify_result_digest(result: Mapping[str, Any]) -> bool:
    digest = result.get("semantic_sha256")
    return isinstance(digest, str) and digest == sha256_bytes(canonical_json(_semantic_value(result)))


def _write_result(destination: Path, result: dict[str, Any]) -> None:
    result["semantic_sha256"] = sha256_bytes(canonical_json(_semantic_value(result)))
    _atomic_write(destination / REPORT_NAME, canonical_json(result))


def run_governance_migration(
    operational_repository: Path,
    *,
    scenario_path: Path,
    predecessor_python: Path,
    successor_python: Path,
    output: Path,
    environment: Mapping[str, str] | None = None,
    _fault_stage: str | None = None,
) -> dict[str, Any]:
    """Run one closed, disposable migration scenario and retain a canonical result."""

    contract = load_migration_contract()
    contract_raw = migration_contract_bytes()
    implementation_sha256 = _implementation_identity(contract)
    repository = _resolved(operational_repository, strict=True)
    if not repository.is_dir() or repository.is_symlink():
        raise GovernanceMigrationError("MIG216: operational repository must be a real directory")
    scenario_file = _resolved(scenario_path, strict=True)
    if not scenario_file.is_file() or scenario_file.is_symlink():
        raise GovernanceMigrationError("MIG217: scenario must be an unlinked regular file")
    requested_output = _absolute(output)
    if output.is_symlink():
        raise GovernanceMigrationError("MIG218: output must not be a symlink")
    destination = _resolved(requested_output)
    if _within(destination, repository) or _within(repository, destination):
        raise GovernanceMigrationError("MIG219: output must be external to and not contain the operational repository")
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise GovernanceMigrationError("MIG220: output must be absent or empty")
    if _fault_stage is not None and _fault_stage not in STAGE_ORDER:
        raise GovernanceMigrationError("MIG221: internal fault stage is invalid")
    selected_environment = os.environ if environment is None else environment
    credential_signals = sorted(
        name for name in contract["credential_signals"] if selected_environment.get(name)
    )
    if credential_signals:
        raise GovernanceMigrationError(
            "MIG222: credential-bearing environment is forbidden: " + ", ".join(credential_signals)
        )
    scenario, scenario_raw = load_migration_scenario(scenario_file, contract)
    predecessor_lexical = _absolute(predecessor_python)
    successor_lexical = _absolute(successor_python)
    if os.path.normcase(str(predecessor_lexical)) == os.path.normcase(str(successor_lexical)):
        raise GovernanceMigrationError("MIG223: predecessor and successor interpreters must be distinct")

    destination.mkdir(parents=True, exist_ok=True)
    workspace = destination / "disposable-workspace"
    operational_before = _operational_identity(repository)
    predecessor, predecessor_origin, predecessor_search, predecessor_root = _runtime_identity(
        predecessor_lexical,
        role="predecessor",
        expected_version=scenario["versions"]["predecessor"],
        expectation=scenario["runtime_expectations"]["predecessor"],
        repository=repository,
        output=destination,
        contract=contract,
    )
    successor, successor_origin, successor_search, successor_root = _runtime_identity(
        successor_lexical,
        role="successor",
        expected_version=scenario["versions"]["successor"],
        expectation=scenario["runtime_expectations"]["successor"],
        repository=repository,
        output=destination,
        contract=contract,
    )
    if predecessor_origin == successor_origin or _within(predecessor_origin, successor_origin) or _within(successor_origin, predecessor_origin):
        raise GovernanceMigrationError("MIG224: evaluator package origins are not isolated")
    if any(_within(path, successor_root) for path in predecessor_search) or any(
        _within(path, predecessor_root) for path in successor_search
    ):
        raise GovernanceMigrationError("MIG227: evaluator import searches are not isolated")
    workspace.mkdir()

    classification = classify_migration(scenario, contract)
    stage_results: list[dict[str, Any]] = []
    failed = False
    first_failed_stage: str | None = None
    for stage in scenario["stages"]:
        if failed:
            stage_results.append(_not_run_stage(stage, scenario, contract, implementation_sha256))
            continue
        stage_id = stage["id"]
        before_workspace = _snapshot_tree(workspace)
        input_view_sha256 = before_workspace["sha256"]
        evaluator_before = _selected_evaluator(workspace)
        started = time.perf_counter_ns()
        details: dict[str, Any] | None = None
        diagnostic: str | None = None
        try:
            if _fault_stage == stage_id:
                raise GovernanceMigrationError(f"MIG490: injected failure at {stage_id}")
            details = STAGE_DRIVERS[stage_id](workspace, scenario, stage)
            after_workspace = _snapshot_tree(workspace)
            changed_paths = _workspace_changes(before_workspace, after_workspace)
            observed = sorted({_mutation_kind(path) for path in changed_paths})
            permitted = contract["stages"][stage_id]["permitted_mutations"]
            if "undeclared" in observed or not set(observed) <= set(permitted):
                raise GovernanceMigrationError(f"MIG415: stage {stage_id} made an undeclared disposable mutation")
            evaluator_after = _selected_evaluator(workspace)
            if stage_id == "prepare":
                if evaluator_after != "predecessor":
                    raise GovernanceMigrationError("MIG416: preparation did not preserve predecessor selection")
            elif stage_id != "adopt":
                if evaluator_before != "predecessor" or evaluator_after != "predecessor":
                    raise GovernanceMigrationError(f"MIG417: stage {stage_id} substituted root authority")
            elif evaluator_before != "predecessor" or evaluator_after != "successor":
                raise GovernanceMigrationError("MIG418: adoption evaluator transition differs from the contract")
            operational_now = _operational_identity(repository)
            if operational_now != operational_before:
                raise GovernanceMigrationError(f"MIG419: stage {stage_id} changed operational source or Git identity")
            report_sha256 = sha256_bytes(canonical_json(details))
            result = "pass"
        except (GovernanceMigrationError, OSError, ValueError) as exc:
            after_workspace = _snapshot_tree(workspace)
            changed_paths = _workspace_changes(before_workspace, after_workspace)
            observed = sorted({_mutation_kind(path) for path in changed_paths})
            permitted = contract["stages"][stage_id]["permitted_mutations"]
            diagnostic = str(exc) if isinstance(exc, GovernanceMigrationError) else f"MIG499: {type(exc).__name__}"
            details = {"diagnostic": diagnostic}
            report_sha256 = sha256_bytes(canonical_json(details))
            result = "fail"
            failed = True
            first_failed_stage = stage_id
        duration_ms = max(0, (time.perf_counter_ns() - started) // 1_000_000)
        decision = _decision_binding(scenario, stage)
        authority_effect = (
            _decision_by_id(scenario, stage["decision_fixture"])["permitted_effect"]
            if stage["decision_fixture"] is not None and result == "pass"
            else "none"
        )
        stage_results.append(
            {
                "authority_effect": authority_effect,
                "command_identity": _command_identity(stage, implementation_sha256),
                "decision_fixture": decision,
                "diagnostic": diagnostic,
                "duration_ms": duration_ms,
                "evaluator_role": stage["technical_role"],
                "id": stage_id,
                "input_view_sha256": input_view_sha256,
                "observed_mutations": observed,
                "permitted_mutations": permitted,
                "report": details,
                "report_sha256": report_sha256,
                "result": result,
                "target_view": stage["view"],
            }
        )

    final_workspace = _snapshot_tree(workspace)
    final_selected = _selected_evaluator(workspace)
    operational_after = _operational_identity(repository)
    if operational_after != operational_before and not failed:
        failed = True
        first_failed_stage = "adopt"
    result: dict[str, Any] = {
        "authority": (
            "This rehearsal records technical evidence only. It cannot approve, verify, release, "
            "publish, deploy, or adopt an evaluator in the operational repository."
        ),
        "classification": classification,
        "contract": {
            "implementation_sha256": implementation_sha256,
            "schema": CONTRACT_SCHEMA,
            "sha256": sha256_bytes(contract_raw),
        },
        "external_actions": {action: False for action in contract["external_actions"]},
        "final_selected_evaluator": final_selected,
        "first_failed_stage": first_failed_stage,
        "host": {
            "implementation": platform.python_implementation(),
            "os": platform.system(),
        },
        "operational_state": {
            "after": operational_after,
            "before": operational_before,
            "unchanged": operational_after == operational_before,
        },
        "overall_result": "fail" if failed else "pass",
        "runtimes": {"predecessor": predecessor, "successor": successor},
        "scenario": {
            "fixture_sha256": scenario["fixture_sha256"],
            "id": scenario["scenario_id"],
            "sha256": sha256_bytes(scenario_raw),
        },
        "schema": RESULT_SCHEMA,
        "semantic_sha256": "",
        "stages": stage_results,
        "state": {
            "disposable_final_sha256": final_workspace["sha256"],
            "evaluator_after": final_selected,
            "evaluator_before": "predecessor",
        },
    }
    try:
        shutil.rmtree(workspace)
    except OSError:
        result["overall_result"] = "fail"
        if result["first_failed_stage"] is None:
            result["first_failed_stage"] = "adopt"
    _write_result(destination, result)
    return result

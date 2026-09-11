"""C12 invalid native binding inventory. Default: read-only preflight, no host.

Only --run with the reviewed preflight digest activates one disposable variant.
No model thread, trust update, native cache edit, or synthetic edit is supported.
"""
import argparse
import hashlib
import json
import queue
import subprocess
import sys
import threading
import time
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).absolute().parent))
import fixture
import observer
import processes
import sanitize_output

PLUGIN = "verity-plane@verity-plane-codex-fixture"
RECORD_SHA = "675c9d101dc9889550b4e2663f12102495dec2388c9107e1f84e9677c180b605"
HOST_SHA = "e5aa76d19c7c94e2e9ef9b707d590206a73ac0e97c8ddc8382181242494bef75"
CLIENT_SCHEMA_SHA = "05c82ead1a820c765c23d3a1d262e4ae54889785276ee1acf7c494141fd94d70"
ORIGINAL_VERSION = "0.0.1+codex.20260911195218"
CHANGED = (".codex-plugin/plugin.json", "hooks/hooks.json")
VARIANTS = {"timeout-1": ("timeout", 1, "0.0.1+codex.c12.timeout.20260911.plan01"),
            "async-true": ("async", True, "0.0.1+codex.c12.async.20260911.plan01")}


class Stop(RuntimeError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Stop("duplicate JSON field")
        result[key] = value
    return result


def decode(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique)


def ordinary(path):
    if not path.is_absolute() or ".." in path.parts:
        raise Stop("absolute ordinary paths required")
    for part in (path, *path.parents):
        if part.is_symlink() or (part.exists() and getattr(part.lstat(), "st_file_attributes", 0) & 0x400):
            raise Stop("linked/reparse path is unsupported")
    return path


def inventory(root):
    ordinary(root)
    result = {}
    for path in root.rglob("*"):
        ordinary(path)
        if path.is_file():
            if path.stat().st_nlink != 1:
                raise Stop("hard-linked payload is unsupported")
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def require_payload(root, expected):
    actual = inventory(root)
    if actual != expected:
        raise Stop("payload drift or unexpected/missing files: " + str(root))
    return actual


def derive(original, variant):
    field, value, version = VARIANTS[variant]
    changed = {name: decode(original[name]) for name in CHANGED}
    manifest, hooks = changed[CHANGED[0]], changed[CHANGED[1]]
    if manifest["version"] != ORIGINAL_VERSION:
        raise Stop("wrong original manifest version")
    before = hooks["hooks"]["PreToolUse"][0]["hooks"][0]
    if before.get("timeout") != 30 or before.get("async") is not False:
        raise Stop("original before-tool mode/budget differs")
    manifest["version"] = version
    before[field] = value
    return {name: encoded(changed[name]) for name in CHANGED}


def config_state(path):
    raw = ordinary(path).read_bytes()
    return {"sha256": digest(raw), "parsed": tomllib.loads(raw.decode("utf-8"))}


def require_config(path, before):
    current = config_state(path)
    if current["parsed"] != before["parsed"]:
        raise Stop("unattributed profile config change; do not launch another host")
    return {"sha256": current["sha256"], "semantic_unchanged": True,
            "byte_unchanged": current["sha256"] == before["sha256"],
            "attribution": "identical parsed TOML; only formatting may differ"}


def record(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value))


def replace_source(target, expected_current, desired):
    """Write only the two marketplace files, after the full inventory check."""
    require_payload(target, expected_current)
    for name in CHANGED:
        ordinary(target / name).write_bytes(desired[name])
    expected = dict(expected_current)
    expected.update({name: digest(raw) for name, raw in desired.items()})
    require_payload(target, expected)
    return expected


def restore_source(target, expected_original, original, variant):
    # Partial two-file activation is recoverable; unrelated concurrent drift is
    # not permission to overwrite. No recursive deletion or cache mutation.
    actual = inventory(target)
    if set(actual) != set(expected_original):
        raise Stop("cannot restore over unexpected/missing source files")
    for name, value in actual.items():
        permitted = {expected_original[name]}
        if name in CHANGED:
            permitted.add(digest(variant[name]))
        if value not in permitted:
            raise Stop("cannot restore over unattributed source drift: " + name)
    for name in CHANGED:
        ordinary(target / name).write_bytes(original[name])
    require_payload(target, expected_original)


def assess_inventory(response, repo, cache, definitions, expected_payload, variant=None):
    groups = response.get("result", {}).get("data", [])
    if len(groups) != 1 or Path(groups[0].get("cwd", "")) != repo:
        raise Stop("ambiguous native inventory repository")
    if groups[0].get("errors") or groups[0].get("warnings"):
        raise Stop("native inventory reports errors/warnings; retain as unavailable")
    selected = []
    names = {"sessionStart": "SessionStart", "preToolUse": "PreToolUse"}
    for hook in groups[0].get("hooks", []):
        if hook.get("pluginId") != PLUGIN:
            if hook.get("enabled") is not False:
                raise Stop("unexpected active hook")
            continue
        event = names.get(hook.get("eventName"))
        if not event:
            raise Stop("unexpected selected-plugin event")
        definition = definitions["hooks"][event][0]
        command = definition["hooks"][0]
        if (hook.get("command") != command["command"] or hook.get("handlerType") != "command"
                or type(hook.get("async")) is not bool or hook["async"] != command["async"]
                or type(hook.get("timeoutSec")) is not int or hook["timeoutSec"] != command["timeout"]
                or hook.get("matcher") != definition.get("matcher")
                or Path(hook.get("sourcePath", "")) != cache / "hooks/hooks.json"
                or not isinstance(hook.get("currentHash"), str) or not hook["currentHash"]):
            raise Stop("native fields differ from the exact selected fixture")
        if variant is None and (hook.get("enabled") is not True or hook.get("trustStatus") != "trusted"):
            raise Stop("original native binding not trusted/enabled after restoration")
        selected.append(hook)
    if sorted(h["eventName"] for h in selected) != sorted(names):
        raise Stop("missing or duplicate native bindings")
    actual = require_payload(cache, expected_payload)
    tool = next(h for h in selected if h["eventName"] == "preToolUse")
    if variant == "timeout-1" and tool["timeoutSec"] != 1:
        raise Stop("invalid budget was not loaded")
    if variant == "async-true" and tool["async"] is not True:
        raise Stop("invalid asynchronous mode was not loaded")
    return {"kind": "invalid-configuration-rejected" if variant else "original-restored",
            "variant": variant, "qualified": False, "bindings": selected,
            "loaded_payload": actual, "trusted_and_enabled": all(
                h.get("enabled") is True and h.get("trustStatus") == "trusted" for h in selected),
            "native_timeout_seconds": tool["timeoutSec"], "native_async": tool["async"],
            "required_inner_plus_margins_seconds": 8 + 4 + 4 + 2,
            "dispatcher_assumed_host_timeout_seconds": 30,
            "reason": ("1-second native timeout cannot exceed the 18-second inner/margin budget"
                       if variant == "timeout-1" else "asynchronous before-tool binding is unqualified"
                       if variant else "exact original payload and native binding restored"),
            "no_thread_started": True, "effects_not_exercised": True}


class Native:
    """Fixed local CLI and inventory messages; every child is job-contained."""
    def __init__(self, repo, stop_marker):
        self.repo, self.stop_marker = repo, stop_marker
        self.cleanup_confirmed = True

    def cleanup(self, process):
        try:
            result = processes.stop_owned_tree(process)
        except BaseException as error:
            result = {"cleanup_error": str(error)}
        self.cleanup_confirmed = result.get("active_processes") == 0
        return result

    def check_stop(self, deadline, restoring=False):
        if time.monotonic() >= deadline or (not restoring and self.stop_marker.exists()):
            raise Stop("fixed deadline or external stop")

    def cli(self, args, destination, restoring=False):
        if not self.cleanup_confirmed:
            raise Stop("previous owned-process cleanup unconfirmed; no further native launch")
        if args not in (["plugin", "add", PLUGIN, "--json"], ["plugin", "list", "--json"]):
            raise Stop("unapproved native CLI operation")
        destination.mkdir(parents=True, exist_ok=False)
        argv = fixture.host_argv(*args)
        result = {"argv": argv, "started_monotonic": time.monotonic()}
        record(destination / "command.json", result)
        process = None
        raw_out = raw_err = b""
        try:
            self.check_stop(time.monotonic() + 1, restoring)
            self.cleanup_confirmed = False
            process = processes.spawn(argv, cwd=self.repo, env=fixture.host_environment(),
                                      stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            deadline = time.monotonic() + 60
            while True:
                self.check_stop(deadline, restoring)
                try:
                    raw_out, raw_err = process.communicate(timeout=.1)
                    break
                except subprocess.TimeoutExpired:
                    continue
            result["exit_status"] = process.returncode
        except BaseException as error:
            result["error"] = str(error)
            raise
        finally:
            if process is not None:
                result["cleanup"] = self.cleanup(process)
                try:
                    raw_out, raw_err = process.communicate(timeout=3)
                except (OSError, subprocess.TimeoutExpired) as error:
                    self.cleanup_confirmed = False
                    result["reader_error"] = str(error)
            for name, raw in (("stdout", raw_out), ("stderr", raw_err)):
                result[name + "_raw_sha256"] = digest(raw)
                safe = sanitize_output.sanitize_text(raw.decode("utf-8", errors="replace")).encode("utf-8")
                (destination / (name + ".txt")).write_bytes(safe)
                result[name + "_sanitization_changed_bytes"] = raw != safe
            result["finished_monotonic"] = time.monotonic()
            record(destination / "result.json", result)
        if result.get("exit_status") != 0 or not self.cleanup_confirmed:
            raise Stop("native CLI failed or cleanup unconfirmed")
        return result

    def inventory(self, destination, restoring=False):
        if not self.cleanup_confirmed:
            raise Stop("previous owned-process cleanup unconfirmed; no further native launch")
        destination.mkdir(parents=True, exist_ok=False)
        argv = fixture.host_argv("app-server", "--stdio")
        result = {"argv": argv, "started_monotonic": time.monotonic(), "thread_started": False}
        record(destination / "command.json", result)
        rows, errors, incoming, fault = [], [], queue.Queue(), threading.Event()
        process, readers = None, []
        raw_hash, err_hash = hashlib.sha256(), hashlib.sha256()

        def read_out():
            count = 0
            try:
                for raw in process.stdout:
                    raw_hash.update(raw)
                    count += len(raw)
                    if count > 8 * 1024 * 1024 or len(raw) > 1024 * 1024:
                        raise Stop("bounded inventory output exceeded")
                    message = decode(raw)
                    if not isinstance(message, dict):
                        raise Stop("native message must be an object")
                    safe = ({"method": message["method"], "capture_omission": "account fields excluded"}
                            if str(message.get("method", "")).startswith("account/")
                            else sanitize_output.sanitize_value(message))
                    rows.append({"received_monotonic": time.monotonic(), "message": safe,
                                 "raw_sha256": digest(raw)})
                    incoming.put(message)
            except BaseException as error:
                errors.append(str(error)); fault.set()

        def read_err():
            count = 0
            for raw in process.stderr:
                err_hash.update(raw); count += len(raw)
                if count > 1024 * 1024:
                    errors.append("bounded stderr exceeded"); fault.set(); return
                errors.append(sanitize_output.sanitize_text(raw.decode("utf-8", errors="replace")))

        def validate(message):
            if "method" in message and "id" in message:
                raise Stop("native server request: no response, trust or approval allowed")
            if str(message.get("method", "")).startswith(("thread/", "turn/", "item/", "hook/")):
                raise Stop("unexpected execution event in inventory-only observation")
            if "id" in message and (type(message["id"]) is not int or message["id"] not in (1, 2)):
                raise Stop("unknown response identifier")
            if "error" in message:
                raise Stop("native error response")

        def send(value):
            rows.append({"sent_monotonic": time.monotonic(), "message": value})
            process.stdin.write(encoded(value).replace(b"\n", b" ") + b"\n")
            process.stdin.flush()

        def request(identifier, method, params):
            send({"id": identifier, "method": method, "params": params})
            while True:
                self.check_stop(deadline, restoring)
                if fault.is_set():
                    raise Stop("native reader failed")
                try:
                    message = incoming.get(timeout=.05)
                except queue.Empty:
                    if process.poll() is not None:
                        raise Stop("native exited before inventory response")
                    continue
                validate(message)
                if message.get("id") == identifier:
                    if "result" not in message:
                        raise Stop("missing result")
                    return message
                if "id" in message:
                    raise Stop("late or duplicate response identifier")

        try:
            self.check_stop(time.monotonic() + 1, restoring)
            self.cleanup_confirmed = False
            process = processes.spawn(argv, cwd=self.repo, env=fixture.host_environment(),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            readers = [threading.Thread(target=read_out, daemon=True), threading.Thread(target=read_err, daemon=True)]
            for reader in readers: reader.start()
            deadline = time.monotonic() + 45
            request(1, "initialize", {"clientInfo": {"name": "verity-c12-inventory", "version": "0.0.1"},
                                      "capabilities": {"experimentalApi": True}})
            send({"method": "initialized", "params": {}})
            result["hooks"] = request(2, "hooks/list", {"cwds": [str(self.repo)]})
        except BaseException as error:
            result["error"] = str(error)
            raise
        finally:
            if process is not None:
                result["cleanup"] = self.cleanup(process)
            for reader in readers: reader.join(timeout=3)
            result["readers_complete"] = all(not reader.is_alive() for reader in readers)
            if not result["readers_complete"]:
                self.cleanup_confirmed = False
            result["stdout_raw_sha256"] = raw_hash.hexdigest()
            result["stderr_raw_sha256"] = err_hash.hexdigest()
            result["finished_monotonic"] = time.monotonic()
            record(destination / "transcript.json", rows)
            (destination / "stdout.txt").write_bytes(b"".join(encoded(x["message"]) for x in rows if "received_monotonic" in x))
            (destination / "stderr.txt").write_bytes("".join(errors).encode("utf-8"))
            record(destination / "result.json", result)
        if fault.is_set() or not result["readers_complete"] or result["cleanup"].get("active_processes") != 0:
            raise Stop("inventory readers or cleanup incomplete")
        while not incoming.empty():
            message = incoming.get_nowait(); validate(message)
            if "id" in message:
                raise Stop("late/duplicate inventory response")
        return result["hooks"]


def transaction(context, native):
    """Every activation attempt has a separately checked native restoration."""
    c = context
    destination = c["destination"]
    destination.mkdir(parents=True, exist_ok=False)
    record(destination / "preflight.json", c["plan"])
    for name in CHANGED:
        path = destination / "original-source" / name
        path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(c["original"][name])
        variant_path = destination / "INVALID-variant-source" / name
        variant_path.parent.mkdir(parents=True, exist_ok=True)
        variant_path.write_bytes(c["variant_bytes"][name])
    record(destination / "derived-payload.json", {"kind": "INVALID test fixture; not a checked package", "payload": c["expected_variant"]})
    outcome, activation_started = {"qualified": False, "restoration_complete": False}, False
    config = c["config"]

    def invariants():
        require_payload(c["source"], c["expected_original"])
        if digest(c["marketplace_metadata"].read_bytes()) != c["metadata_sha"]:
            raise Stop("marketplace metadata changed")
        return require_config(c["config_path"], config)

    def run_and_inventory(prefix, restoring):
        invariants()
        native.cli(["plugin", "add", PLUGIN, "--json"], destination / (prefix + "-add"), restoring)
        invariants()
        native.cli(["plugin", "list", "--json"], destination / (prefix + "-list"), restoring)
        invariants()
        response = native.inventory(destination / (prefix + "-inventory"), restoring)
        invariants()
        return response

    try:
        invariants()
        # Read-only native baseline must confirm the currently selected version,
        # not merely the presence of an old original cache directory.
        baseline = native.inventory(destination / "original-before-inventory")
        outcome["original_before"] = assess_inventory(baseline, c["repo"], c["original_cache"],
                                                     c["definitions"], c["expected_original"])
        invariants()
        record(destination / "restoration-needed.json", {"original_version": ORIGINAL_VERSION,
                "activation_target": str(c["target"]), "restoration_required": True})
        activation_started = True
        replace_source(c["target"], c["expected_original"], c["variant_bytes"])
        response = run_and_inventory("variant", False)
        outcome["negative_assessment"] = assess_inventory(response, c["repo"], c["variant_cache"],
              decode(c["variant_bytes"]["hooks/hooks.json"]), c["expected_variant"], c["variant"])
        record(destination / "negative-assessment.json", outcome["negative_assessment"])
    except BaseException as error:
        outcome["observation_error"] = str(error)
    finally:
        if activation_started:
            try:
                restore_source(c["target"], c["expected_original"], c["original"], c["variant_bytes"])
                invariants()
                response = run_and_inventory("restore", True)
                outcome["restoration"] = assess_inventory(response, c["repo"], c["original_cache"],
                                                          c["definitions"], c["expected_original"])
                if outcome["restoration"]["bindings"] != outcome["original_before"]["bindings"]:
                    raise Stop("original native binding identity/hash differs after restoration")
                outcome["config_after"] = invariants()
                outcome["restoration_complete"] = True
                record(destination / "restoration-complete.json", outcome["restoration"])
            except BaseException as error:
                outcome["restoration_error"] = str(error)
        outcome["sentinels_after"] = {p.name: digest(p.read_bytes()) for p in c["sentinels"]}
        outcome["sentinels_unchanged"] = outcome["sentinels_after"] == c["plan"]["sentinels"]
        record(destination / "outcome.json", outcome)
    return outcome


def preflight(variant, destination, stop_marker):
    base = fixture.ROOT / "docs/engineering/plugin-integration/evidence/WO-PLG-005"
    package_path = base / "preparation/package-04/package.json"
    package_raw = package_path.read_bytes()
    if digest(package_raw) != RECORD_SHA or digest(fixture.CODEX.read_bytes()) != HOST_SHA:
        raise Stop("approved package record or native executable identity changed")
    schema_path = fixture.SCHEMAS / "ClientRequest.json"
    if observer.schema_methods(schema_path) != CLIENT_SCHEMA_SHA:
        raise Stop("accepted native request schema changed")
    package = decode(package_raw)
    source = fixture.SANDBOX / "review package 400cf3d5d669/codex/verity-plane"
    if Path(package["package_root"]) != source:
        raise Stop("unexpected original source")
    target = fixture.SANDBOX / "marketplace with spaces/plugins/verity-plane"
    ordinary(destination); ordinary(stop_marker)
    control = fixture.WORK / "plugin-probe-control/se-harness-plugin-codex-adapter"
    if (base / "C12" not in destination.parents or destination.exists()
            or control not in stop_marker.parents or stop_marker.exists()):
        raise Stop("fresh C12 evidence path and external control stop-marker required")
    expected = package["payload"]
    require_payload(source, expected); require_payload(target, expected)
    cache_base = fixture.PROFILE / "codex/plugins/cache/verity-plane-codex-fixture/verity-plane"
    original_cache = cache_base / ORIGINAL_VERSION
    require_payload(original_cache, expected)
    original = {name: (source / name).read_bytes() for name in CHANGED}
    variant_bytes = derive(original, variant)
    expected_variant = dict(expected)
    expected_variant.update({name: digest(raw) for name, raw in variant_bytes.items()})
    config_path = fixture.PROFILE / "codex/config.toml"
    config = config_state(config_path)
    metadata = fixture.SANDBOX / "marketplace with spaces/.agents/plugins/marketplace.json"
    ordinary(metadata)
    repo = fixture.SANDBOX / "repo with spaces"
    sentinels = [ordinary(repo / name) for name in ("governed-target.txt", "outside-scope.txt", "café quoted ' target.txt")]
    version = VARIANTS[variant][2]
    plan = {"kind": "C12 preflight only unless --run is supplied with this digest", "variant": variant,
            "source": str(source), "target": str(target), "destination": str(destination),
            "profile": str(fixture.PROFILE), "stop_marker": str(stop_marker), "host_sha256": HOST_SHA,
            "package_record_sha256": RECORD_SHA, "expected_original": expected,
            "expected_variant": expected_variant, "variant_version": version,
            "profile_config_sha256": config["sha256"], "marketplace_metadata_sha256": digest(metadata.read_bytes()),
            "schema_sha256": {"ClientRequest.json": CLIENT_SCHEMA_SHA,
                "v2/HooksListResponse.json": digest((fixture.SCHEMAS / "v2/HooksListResponse.json").read_bytes())},
            "trust_projection": config["parsed"].get("hooks", {}),
            "sentinels": {p.name: digest(p.read_bytes()) for p in sentinels},
            "source_sha256": {str(p.relative_to(fixture.ROOT)): digest(p.read_bytes()) for p in
                (Path(__file__), Path(fixture.__file__), Path(observer.__file__), Path(processes.__file__), Path(sanitize_output.__file__))},
            "restoration_required": "original source bytes, native original version, trusted bindings and entire original payload",
            "effects": "one temporary invalid marketplace variant; native reinstall/list/inventory; restoration",
            "non_effects": "no cache or trust edit, no model/thread start, no synthetic file effect"}
    return {"plan": plan, "variant": variant, "destination": destination, "source": source, "target": target,
            "original_cache": original_cache, "variant_cache": cache_base / version, "config": config,
            "config_path": config_path, "marketplace_metadata": metadata, "metadata_sha": digest(metadata.read_bytes()),
            "repo": repo, "sentinels": sentinels, "original": original, "variant_bytes": variant_bytes,
            "definitions": decode(original["hooks/hooks.json"]), "expected_original": expected,
            "expected_variant": expected_variant}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--stop-marker", type=Path, required=True)
    parser.add_argument("--approved-preflight-sha256")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args(argv)
    context = preflight(args.variant, args.evidence.absolute(), args.stop_marker.absolute())
    approval_digest = digest(encoded(context["plan"]))
    if not args.run:
        print(json.dumps({"preflight": context["plan"], "preflight_sha256": approval_digest}, ensure_ascii=False, indent=2))
        return 0
    if args.approved_preflight_sha256 != approval_digest:
        raise Stop("explicit matching reviewed preflight digest required before native activation")
    result = transaction(context, Native(context["repo"], args.stop_marker.absolute()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if (result.get("negative_assessment") and result["restoration_complete"]
                 and result["sentinels_unchanged"] and "observation_error" not in result) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Stop, OSError, ValueError, KeyError) as error:
        print(json.dumps({"stopped": str(error), "qualified": False}), file=sys.stderr)
        raise SystemExit(1)

"""Pure acceptance-observer boundaries; no host process or request is started."""
import hashlib
import json
from pathlib import Path


class ObservationStopped(RuntimeError):
    def __init__(self, reason, detail=None):
        super().__init__(reason)
        self.detail = detail


def package_record(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def received(records, first, predicate):
    # Inspect requests before matching responses; server/client ids may collide.
    for entry in records:
        value = entry["message"]
        if "received_monotonic" in entry and value.get("id") is not None and "method" in value:
            raise ObservationStopped("host request requires review; no response sent", value)
    for entry in records[first:]:
        if "received_monotonic" in entry and predicate(entry["message"]):
            return entry["message"]
    return None


def schema_methods(path):
    encoded = json.dumps(json.loads(path.read_text(encoding="utf8")))
    required = {"initialize", "hooks/list", "skills/list", "thread/start", "thread/resume",
                "turn/start", "thread/compact/start", "thread/read"}
    if any(json.dumps(method) not in encoded for method in required):
        raise ObservationStopped("required method absent from pinned generated host schema")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_bindings(response, repo, cache_root, definitions, expected_file_sha256):
    groups = response.get("result", {}).get("data", [])
    if len(groups) != 1 or Path(groups[0].get("cwd", "")) != repo or groups[0].get("errors") or groups[0].get("warnings"):
        raise ObservationStopped("host binding inventory unavailable or ambiguous", response)
    plugin = "verity-plane@verity-plane-codex-fixture"
    selected = []
    expected = {"sessionStart": "SessionStart", "preToolUse": "PreToolUse"}
    for hook in groups[0].get("hooks", []):
        if hook.get("pluginId") != plugin:
            if hook.get("enabled") is not False:
                raise ObservationStopped("unexpected active hook prevents independent acceptance", hook)
            continue
        event = expected.get(hook.get("eventName"))
        if event is None or hook.get("enabled") is not True or hook.get("trustStatus") != "trusted":
            raise ObservationStopped("required hook is missing, disabled or untrusted", hook)
        row = definitions["hooks"][event][0]
        command = row["hooks"][0]
        if (hook.get("handlerType") != "command" or hook.get("command") != command["command"] or
                hook.get("async") is not False or hook.get("timeoutSec") != command["timeout"] or
                hook.get("matcher") != row.get("matcher")):
            raise ObservationStopped("loaded binding differs from exact candidate", hook)
        path = Path(hook.get("sourcePath", ""))
        if not path.is_absolute() or cache_root not in path.parents or path.is_symlink():
            raise ObservationStopped("loaded hook path is outside the selected native cache", hook)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected_file_sha256 or not isinstance(hook.get("currentHash"), str):
            raise ObservationStopped("loaded hook bytes lack candidate identity", hook)
        selected.append({**hook, "source_sha256": digest})
    if sorted(hook["eventName"] for hook in selected) != sorted(expected):
        raise ObservationStopped("both unique required hooks must be present", selected)
    return selected


def loaded_payload(root, expected):
    actual = {}
    for path in root.rglob("*"):
        if path.is_symlink() or (getattr(path.lstat(), "st_file_attributes", 0) & 0x400):
            raise ObservationStopped("linked loaded payload is unsupported")
        if path.is_file():
            actual[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    # This native fixture has no cache metadata exclusion. Any new file must be
    # assessed explicitly rather than silently broadening the comparison.
    if actual != expected:
        raise ObservationStopped("loaded cache payload differs from checked package", {"expected": expected, "actual": actual})
    return actual

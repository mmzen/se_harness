"""Pure C12 runner tests: disposable temp files and fake native transport only."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import queue
import shutil
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("c12_observer", Path(__file__).with_name("c12_binding_observer.py"))
c12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c12)


def hook_response(repo, cache, definitions, trusted=True):
    rows = []
    for native, event in (("sessionStart", "SessionStart"), ("preToolUse", "PreToolUse")):
        row = definitions["hooks"][event][0]
        command = row["hooks"][0]
        rows.append({"pluginId": c12.PLUGIN, "eventName": native, "enabled": True,
                     "trustStatus": "trusted" if trusted else "untrusted",
                     "sourcePath": str(cache / "hooks/hooks.json"), "command": command["command"],
                     "handlerType": "command", "async": command["async"], "timeoutSec": command["timeout"],
                     "matcher": row.get("matcher"), "currentHash": "opaque-host-hash"})
    return {"id": 2, "result": {"data": [{"cwd": str(repo), "hooks": rows, "errors": [], "warnings": []}]}}


class Setup:
    def __init__(self, root, variant="timeout-1"):
        source, target = root / "original", root / "marketplace"
        hooks = {"hooks": {"SessionStart": [{"matcher": "startup|resume|clear|compact", "hooks": [
                    {"type": "command", "command": "session original", "timeout": 30, "async": False}]}],
                  "PreToolUse": [{"hooks": [
                    {"type": "command", "command": "tool original", "timeout": 30, "async": False}]}]}}
        original = {".codex-plugin/plugin.json": c12.encoded({"name": "verity-plane", "version": c12.ORIGINAL_VERSION}),
                    "hooks/hooks.json": c12.encoded(hooks)}
        files = {**original, "scripts/source.py": b"original policy bytes\r\n", "assembly-inventory.json": b"original provenance\n"}
        for name, raw in files.items():
            path = source / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
        shutil.copytree(source, target)
        cache = root / "cache" / c12.ORIGINAL_VERSION
        shutil.copytree(source, cache)
        config = root / "config.toml"; config.write_text('[plugins.demo]\nenabled = true\n[hooks.state.demo]\ntrusted_hash = "original"\n')
        metadata = root / "metadata.json"; metadata.write_bytes(b"same marketplace\n")
        repo = root / "repo"; repo.mkdir(); sentinel = repo / "target.txt"; sentinel.write_bytes(b"before\r\n")
        derived = c12.derive(original, variant)
        expected = c12.inventory(source)
        variant_expected = {**expected, **{name:c12.digest(raw) for name, raw in derived.items()}}
        self.c = {"plan": {"sentinels": {"target.txt":c12.digest(sentinel.read_bytes())}}, "variant": variant,
                  "destination": root / "evidence", "source": source, "target": target,
                  "original_cache": cache, "variant_cache": root / "cache" / c12.VARIANTS[variant][2],
                  "config": c12.config_state(config), "config_path": config, "marketplace_metadata": metadata,
                  "metadata_sha": c12.digest(metadata.read_bytes()), "repo": repo, "sentinels": [sentinel],
                  "original": original, "variant_bytes": derived, "definitions": hooks,
                  "expected_original": expected, "expected_variant": variant_expected}


class FakeNative:
    def __init__(self, context, fail_at=None, drift=None, trust=False, bad_restore=False):
        self.c, self.fail_at, self.drift = context, fail_at, drift
        self.calls, self.selected = [], context["original_cache"]
        self.trust, self.bad_restore = trust, bad_restore

    def cli(self, args, destination, restoring=False):
        self.calls.append(("cli", args, restoring))
        if args[1] == "add":
            manifest = c12.decode((self.c["target"] / ".codex-plugin/plugin.json").read_bytes())
            cache = self.c["original_cache"].parent / manifest["version"]
            if not cache.exists(): shutil.copytree(self.c["target"], cache)
            if not (restoring and self.bad_restore): self.selected = cache
        if self.fail_at == destination.name: raise c12.Stop("fake native activation failure")
        if self.drift == destination.name:
            self.c["config_path"].write_text('[plugins.demo]\nenabled = false\n')

    def inventory(self, destination, restoring=False):
        self.calls.append(("inventory", destination.name, restoring))
        if self.fail_at == destination.name: raise c12.Stop("fake inventory failure")
        definitions = c12.decode((self.selected / "hooks/hooks.json").read_bytes())
        return hook_response(self.c["repo"], self.selected, definitions,
                             trusted=not self.trust or self.selected == self.c["original_cache"])


class C12Tests(unittest.TestCase):
    def test_exact_two_file_changes_preserve_commands_and_other_mode_fields(self):
        for variant in c12.VARIANTS:
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as folder:
                c = Setup(Path(folder), variant).c
                self.assertEqual(set(c["variant_bytes"]), set(c12.CHANGED))
                derived = c12.decode(c["variant_bytes"]["hooks/hooks.json"])
                original = c["definitions"]
                field, value, _ = c12.VARIANTS[variant]
                compare = copy.deepcopy(derived)
                compare["hooks"]["PreToolUse"][0]["hooks"][0][field] = original["hooks"]["PreToolUse"][0]["hooks"][0][field]
                self.assertEqual(compare, original)
                self.assertEqual(derived["hooks"]["PreToolUse"][0]["hooks"][0][field], value)

    def test_success_and_untrusted_variant_both_restore_exact_original(self):
        for variant in c12.VARIANTS:
            for untrusted in (False, True):
                with self.subTest(variant=variant, untrusted=untrusted), tempfile.TemporaryDirectory() as folder:
                    c = Setup(Path(folder), variant).c; native = FakeNative(c, trust=untrusted)
                    before_config = c["config_path"].read_bytes()
                    result = c12.transaction(c, native)
                    self.assertTrue(result["restoration_complete"])
                    self.assertFalse(result["qualified"])
                    self.assertEqual(result["negative_assessment"]["kind"], "invalid-configuration-rejected")
                    self.assertEqual(result["negative_assessment"]["trusted_and_enabled"], not untrusted)
                    self.assertEqual(c12.inventory(c["target"]), c["expected_original"])
                    self.assertEqual(native.selected, c["original_cache"])
                    self.assertTrue(result["sentinels_unchanged"])
                    self.assertEqual(c["config_path"].read_bytes(), before_config)

    def test_restoration_requires_the_original_native_definition_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c
            class ChangedHash(FakeNative):
                def inventory(self, destination, restoring=False):
                    response = super().inventory(destination, restoring)
                    if restoring:
                        response["result"]["data"][0]["hooks"][0]["currentHash"] = "unexpected-new-hash"
                    return response
            result = c12.transaction(c, ChangedHash(c))
            self.assertFalse(result["restoration_complete"])
            self.assertIn("identity/hash", result["restoration_error"])

    def test_activation_and_inventory_failures_always_attempt_restoration(self):
        for phase in ("variant-add", "variant-list", "variant-inventory"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as folder:
                c = Setup(Path(folder)).c; native = FakeNative(c, fail_at=phase)
                result = c12.transaction(c, native)
                self.assertIn("observation_error", result)
                self.assertTrue(result["restoration_complete"])
                self.assertEqual(c12.inventory(c["target"]), c["expected_original"])
                self.assertTrue(any(row[-1] is True for row in native.calls))

    def test_wrong_selected_original_cache_is_not_successful_restoration(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c; native = FakeNative(c, bad_restore=True)
            result = c12.transaction(c, native)
            self.assertFalse(result["restoration_complete"])
            self.assertIn("restoration_error", result)
            self.assertFalse((c["destination"] / "restoration-complete.json").exists())
            self.assertEqual(c12.inventory(c["target"]), c["expected_original"])

    def test_unattributed_config_change_stops_further_host_but_restores_source(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c; native = FakeNative(c, drift="variant-add")
            result = c12.transaction(c, native)
            self.assertFalse(result["restoration_complete"])
            self.assertIn("profile config", result["restoration_error"])
            self.assertFalse(any(row[-1] is True for row in native.calls))
            self.assertEqual(c12.inventory(c["target"]), c["expected_original"])
            self.assertIn(b"false", c["config_path"].read_bytes())

    def test_partial_activation_can_restore_but_unrelated_drift_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c
            name = c12.CHANGED[0]
            (c["target"] / name).write_bytes(c["variant_bytes"][name])
            c12.restore_source(c["target"], c["expected_original"], c["original"], c["variant_bytes"])
            other = c["target"] / "scripts/source.py"; other.write_bytes(b"concurrent work")
            with self.assertRaises(c12.Stop):
                c12.restore_source(c["target"], c["expected_original"], c["original"], c["variant_bytes"])
            self.assertEqual(other.read_bytes(), b"concurrent work")

    def test_unexpected_file_and_hardlink_fail_inventory(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c
            extra = c["target"] / "extra"; extra.write_bytes(b"extra")
            with self.assertRaises(c12.Stop): c12.require_payload(c["target"], c["expected_original"])
            extra.unlink()
            os.link(c["target"] / "scripts/source.py", extra)
            with self.assertRaises(c12.Stop): c12.inventory(c["target"])

    def test_loaded_fields_and_extra_active_hook_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            c = Setup(Path(folder)).c
            base = hook_response(c["repo"], c["original_cache"], c["definitions"])
            for key, value in (("timeoutSec", True), ("async", 0), ("command", "changed"),
                               ("sourcePath", str(c["source"] / "hooks/hooks.json")), ("trustStatus", "untrusted")):
                response = copy.deepcopy(base); response["result"]["data"][0]["hooks"][0][key] = value
                with self.subTest(key=key), self.assertRaises(c12.Stop):
                    c12.assess_inventory(response, c["repo"], c["original_cache"], c["definitions"], c["expected_original"])
            base["result"]["data"][0]["hooks"].append({"pluginId":"other", "enabled":True})
            with self.assertRaises(c12.Stop):
                c12.assess_inventory(base, c["repo"], c["original_cache"], c["definitions"], c["expected_original"])

    def test_preflight_default_never_launches_or_writes(self):
        with patch.object(c12, "preflight", return_value={"plan":{"review":"only"}}), \
             patch.object(c12, "transaction") as transaction, patch.object(c12, "Native") as native, \
             patch("sys.stdout", new=io.StringIO()) as output:
            self.assertEqual(c12.main(["--variant","timeout-1","--evidence","case","--stop-marker","stop"]),0)
            self.assertIn("preflight_sha256",output.getvalue())
            transaction.assert_not_called(); native.assert_not_called()

    def test_run_requires_exact_reviewed_digest_before_native_creation(self):
        for value in (None, "f"*64):
            with patch.object(c12,"preflight",return_value={"plan":{"review":"only"}}), \
                 patch.object(c12,"Native") as native:
                argv=["--variant","timeout-1","--evidence","case","--stop-marker","stop","--run"]
                if value: argv += ["--approved-preflight-sha256",value]
                with self.assertRaises(c12.Stop): c12.main(argv)
                native.assert_not_called()

    def test_config_formatting_is_attributable_but_trust_mutation_is_not(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"config.toml";path.write_text('[hooks]\nvalue="same"\n')
            before=c12.config_state(path);path.write_text('[hooks]\nvalue = "same"\n')
            self.assertFalse(c12.require_config(path,before)["byte_unchanged"])
            path.write_text('[hooks]\nvalue="new"\n')
            with self.assertRaises(c12.Stop):c12.require_config(path,before)

    def test_cli_rejects_trust_security_and_other_native_commands(self):
        native=c12.Native(Path.cwd(),Path.cwd()/"unused")
        with patch.object(c12.processes,"spawn") as spawn:
            for args in (["--dangerously-bypass-approvals-and-sandbox"],["plugin","remove",c12.PLUGIN], ["sandbox","setup"]):
                with self.assertRaises(c12.Stop):native.cli(args,Path.cwd()/"never-created")
            spawn.assert_not_called()

    def test_unconfirmed_cleanup_blocks_all_further_native_launches_including_restore(self):
        native = c12.Native(Path.cwd(), Path.cwd()/"unused")
        with patch.object(c12.processes,"stop_owned_tree",side_effect=RuntimeError("job cleanup failed")):
            self.assertIn("cleanup_error",native.cleanup(object()))
        with patch.object(c12.processes,"spawn") as spawn:
            with self.assertRaises(c12.Stop):
                native.cli(["plugin","add",c12.PLUGIN,"--json"],Path.cwd()/"not-created",restoring=True)
            with self.assertRaises(c12.Stop):native.inventory(Path.cwd()/"not-created",restoring=True)
            spawn.assert_not_called()

    def test_inventory_transport_never_sends_thread_or_approval_and_rejects_late_request(self):
        class Stream:
            def __init__(self):self.q=queue.Queue()
            def __iter__(self):return self
            def __next__(self):
                value=self.q.get(timeout=3)
                if value is None:raise StopIteration
                return value
        class Process:
            def __init__(self,late):
                self.stdout,self.stderr=Stream(),Stream();self.sent=[];self.stdin=self;self.late=late
            def write(self,raw):
                message=json.loads(raw);self.sent.append(message)
                if 'id' in message:
                    reply={'id':message['id'],'result':{}}
                    self.stdout.q.put(c12.encoded(reply))
                    if message['id']==2 and self.late:
                        self.stdout.q.put(c12.encoded({'id':99,'method':'item/fileChange/requestApproval','params':{}}))
            def flush(self):pass
            def poll(self):return None
        for late in (False,True):
            with self.subTest(late=late),tempfile.TemporaryDirectory() as folder:
                process=Process(late)
                def cleanup(_):
                    process.stdout.q.put(None);process.stderr.q.put(None)
                    return {'active_processes':0}
                with patch.object(c12.processes,'spawn',return_value=process),patch.object(c12.processes,'stop_owned_tree',side_effect=cleanup) as stop:
                    native=c12.Native(Path(folder),Path(folder)/'stop')
                    if late:
                        with self.assertRaises(c12.Stop):native.inventory(Path(folder)/'evidence')
                    else:self.assertEqual(native.inventory(Path(folder)/'evidence'),{'id':2,'result':{}})
                    self.assertEqual([x.get('method') for x in process.sent],['initialize','initialized','hooks/list'])
                    self.assertTrue(all('result' not in x for x in process.sent));stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()

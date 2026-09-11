"""Independent safety tests for the prepared read-only host observer."""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("adapter_observer", Path(__file__).with_name("observer.py"))
observer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(observer)
review_spec = importlib.util.spec_from_file_location("adapter_review_ui", Path(__file__).with_name("interactive.py"))
review = importlib.util.module_from_spec(review_spec)
review_spec.loader.exec_module(review)


class ObserverTests(unittest.TestCase):
    def test_external_review_stop_and_deadline_always_cleanup_owned_process(self):
        class Process:
            pid = 123
            def poll(self):
                return None
        for stopped in (False, True):
            with tempfile.TemporaryDirectory() as folder:
                marker = Path(folder) / "stop"
                if stopped:
                    marker.touch()
                record, cleaned = {}, []
                def cleanup(process):
                    cleaned.append(process.pid)
                    return {"active_processes": 0}
                review.review_until_stopped(["unused"], Path(folder), {}, marker, 0,
                    record=record, factory=lambda *args, **kwargs: Process(), cleanup=cleanup)
                self.assertEqual(cleaned, [123])
                self.assertEqual(record["stop_reason"], "external marker" if stopped else "fixed review deadline")
                self.assertEqual(record["cleanup"]["active_processes"], 0)

    def test_package_record_accepts_utf8_bom_before_host_launch(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "package.json"
            for encoding in ("utf-8", "utf-8-sig"):
                path.write_text('{"payload":{"café":"digest"}}', encoding=encoding)
                self.assertEqual(observer.package_record(path), {"payload": {"café": "digest"}})

    def test_loaded_payload_rejects_changed_missing_or_extra_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "dispatch.py"
            path.write_bytes(b"exact candidate\n")
            expected = {"dispatch.py": hashlib.sha256(path.read_bytes()).hexdigest()}
            self.assertEqual(observer.loaded_payload(root, expected), expected)
            path.write_bytes(b"substitution\n")
            with self.assertRaises(observer.ObservationStopped):
                observer.loaded_payload(root, expected)
            path.unlink()
            with self.assertRaises(observer.ObservationStopped):
                observer.loaded_payload(root, expected)
            path.write_bytes(b"exact candidate\n")
            (root / "unexpected.txt").write_text("extra")
            with self.assertRaises(observer.ObservationStopped):
                observer.loaded_payload(root, expected)
    def test_server_request_with_colliding_id_stops_before_response_match(self):
        pending = {"received_monotonic": 1, "message": {"id": 4, "method": "request/approval", "params": {}}}
        response = {"received_monotonic": 2, "message": {"id": 4, "result": {}}}
        for records in ([pending], [response, pending]):
            with self.assertRaises(observer.ObservationStopped):
                observer.received(records, 0, lambda value: value.get("id") == 4)
        with self.assertRaises(observer.ObservationStopped):
            observer.received([pending, response], 1, lambda value: value.get("id") == 4)

    def test_request_response_scan_excludes_prior_response_and_outgoing_message(self):
        records = [{"received_monotonic": 1, "message": {"id": 4, "result": {"old": True}}},
                   {"sent_monotonic": 2, "message": {"id": 4, "method": "hooks/list"}}]
        self.assertIsNone(observer.received(records, 1, lambda value: value.get("id") == 4))
        records.append({"received_monotonic": 3, "message": {"id": 4, "result": {"fresh": True}}})
        self.assertEqual(observer.received(records, 1, lambda value: value.get("id") == 4)["result"], {"fresh": True})

    def test_missing_schema_method_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "schema.json"
            path.write_text(json.dumps({"enum": ["initialize", "thread/start"]}), encoding="utf8")
            with self.assertRaises(observer.ObservationStopped):
                observer.schema_methods(path)

    def test_ambiguous_or_foreign_enabled_hook_inventory_cannot_start_thread(self):
        repo = Path.cwd()
        for groups in ([], [{"cwd": str(repo), "hooks": [{"pluginId": "other", "enabled": True}]}],
                       [{"cwd": str(repo), "hooks": [], "warnings": ["missing binding"]}]):
            with self.assertRaises(observer.ObservationStopped):
                observer.active_bindings({"result": {"data": groups}}, repo, repo, {}, "unused")


if __name__ == "__main__":
    unittest.main()

"""The remote transport preserves explicit requests and uncertain outcomes."""
import http.server
import base64
import copy
import hashlib
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from se_harness.remote import RemoteError, TransportUncertain, endpoint_url, send, strict_json, save_export


class RemoteClientTests(unittest.TestCase):
    def export_value(self, files=None):
        def encoded(raw):
            return {'content_base64': base64.b64encode(raw).decode(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        def digest(scheme, value):
            raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
            return hashlib.sha256(scheme.encode() + b'\n' + raw).hexdigest()
        snapshot = {'schema': 'se-harness-test-snapshot/v2', 'test_copy': True,
                    'files': {p: encoded(b) for p, b in (files or {'docs/test.md': b'Exact\r\nbytes\n'}).items()},
                    'git_bundle': encoded(b'bundle fixture bytes')}
        snapshot['snapshot_id'] = 'sha256:' + digest(snapshot['schema'], snapshot)
        manifest = {'provenance': {'snapshot_id': snapshot['snapshot_id']}}
        scheme = 'se-harness-artifact-baseline/v1'
        return {'schema': 'se-harness-lifecycle-export/v2', 'test_copy': True, 'snapshot': snapshot,
                'baseline': {'schema': scheme, 'manifest': manifest, 'baseline_id': scheme + ':sha256:' + digest(scheme, manifest)}}

    def test_export_preserves_bytes_and_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'new-export'
            result = save_export(self.export_value(), target)
            self.assertTrue(result['test_copy'])
            self.assertEqual('not yet performed', result['independent_replay'])
            self.assertEqual(b'Exact\r\nbytes\n', (target / 'files/docs/test.md').read_bytes())
            self.assertFalse((target / '.incomplete').exists())
            with self.assertRaisesRegex(RemoteError, 'EXPORT_EXISTS'):
                save_export(self.export_value(), target)

    def test_export_refuses_unsafe_ambiguous_and_corrupt_data_before_writing(self):
        for path in ('../escape', '/absolute', 'C:/escape', '.GIT/config', 'CON', 'docs/trailing.', 'docs/line\nbreak'):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as folder:
                target = Path(folder) / 'refused'
                with self.assertRaises(RemoteError):
                    save_export(self.export_value({path: b'bad'}), target)
                self.assertFalse(target.exists())
        value = self.export_value()
        value['snapshot']['files']['docs/test.md']['content_base64'] = base64.b64encode(b'corrupt').decode()
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'refused'
            with self.assertRaises(RemoteError):
                save_export(value, target)
            self.assertFalse(target.exists())
        for files in ({'a': b'1', 'A': b'2'}, {'a': b'1', 'a/b': b'2'}):
            with tempfile.TemporaryDirectory() as folder, self.assertRaises(RemoteError):
                save_export(self.export_value(files), Path(folder) / 'refused')

    def test_interrupted_export_keeps_an_incomplete_marker(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'partial'
            with mock.patch('pathlib.Path.write_bytes', side_effect=OSError('simulated write interruption')):
                with self.assertRaises(OSError):
                    save_export(self.export_value(), target)
            self.assertTrue((target / '.incomplete').is_file())

    def test_private_endpoint_and_no_embedded_credentials(self):
        self.assertEqual(endpoint_url("http://127.0.0.1:8080/"), "http://127.0.0.1:8080")
        for endpoint in ("https://example.com", "http://127.0.0.1@evil.test", "http://u:p@localhost", "file:///tmp/x", "http://localhost/?token=x"):
            with self.subTest(endpoint=endpoint), self.assertRaises(RemoteError):
                endpoint_url(endpoint)

    def test_ambiguous_requests_refuse_before_transport(self):
        for raw in ('{"version":1,"version":2}', '{"version":1.0}', '{"version":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(RemoteError):
                strict_json(raw)

    def test_transport_preserves_receipt_and_never_retries(self):
        requests = []
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                body = b'{"outcome":"accepted","receipt_id":"fixed"}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def do_GET(self):
                self.send_response(302)
                self.send_header("Location", "http://example.invalid/never-send-credentials")
                self.end_headers()
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            endpoint = "http://127.0.0.1:" + str(server.server_port)
            request = {"operation_key": "same-key", "expected_project_version": 4}
            status, result = send(endpoint, "synthetic-test-token", "POST", "/command", request)
            self.assertEqual((status, result["receipt_id"]), (200, "fixed"))
            self.assertEqual(requests, [request])
            with self.assertRaises(TransportUncertain) as caught:
                send(endpoint, "synthetic-test-token", "GET", "/redirect")
            self.assertNotIn("synthetic-test-token", str(caught.exception))
            self.assertEqual(len(requests), 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()

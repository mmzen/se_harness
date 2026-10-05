"""The remote transport preserves explicit requests and uncertain outcomes."""
import http.server
import json
import threading
import unittest

from se_harness.remote import RemoteError, TransportUncertain, endpoint_url, send, strict_json


class RemoteClientTests(unittest.TestCase):
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

"""Synthetic sanitizer checks; no host, credential store, or publication access."""
import base64
import copy
import importlib.util
import json
from pathlib import Path
import unittest


SPEC = importlib.util.spec_from_file_location(
    "codex_probe_sanitize_output", Path(__file__).with_name("sanitize_output.py")
)
sanitizer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sanitizer)


class SanitizeOutputTests(unittest.TestCase):
    def test_nested_secret_fields_and_header_maps(self):
        raw = {
            "sessionId": "synthetic-session-001",
            "nested": [{
                "accessToken": "SYNTHETIC-ACCESS-SECRET",
                "refresh_token": "SYNTHETIC-REFRESH-SECRET",
                "apiKey": "SYNTHETIC-API-SECRET",
                "client_secret": "SYNTHETIC-CLIENT-SECRET",
                "id_token": "SYNTHETIC-ID-SECRET",
                "password": "SYNTHETIC-PASSWORD-SECRET",
                "headers": {
                    "Authorization": "Bearer SYNTHETIC-AUTH-SECRET",
                    "Cookie": "session=SYNTHETIC-COOKIE-SECRET",
                    "Set-Cookie": "session=SYNTHETIC-SETCOOKIE-SECRET; HttpOnly",
                    "X-Api-Key": "SYNTHETIC-HEADER-SECRET",
                    "Content-Type": "application/json",
                },
            }],
        }
        for result in (sanitizer.sanitize_value(raw),
                       json.loads(sanitizer.sanitize_text(json.dumps(raw)))):
            with self.subTest(result=result):
                encoded = json.dumps(result)
                for secret in ("ACCESS", "REFRESH", "API", "CLIENT", "ID", "PASSWORD",
                               "AUTH", "COOKIE", "SETCOOKIE", "HEADER"):
                    self.assertNotIn(f"SYNTHETIC-{secret}-SECRET", encoded)
                self.assertEqual("synthetic-session-001", result["sessionId"])
                self.assertEqual("application/json", result["nested"][0]["headers"]["Content-Type"])

    def test_credential_argv_and_command_text(self):
        argv = ["probe", "--api-key", "SYNTHETIC-ARGV-SECRET",
                "--token=SYNTHETIC-EQUALS-SECRET", "--session-id", "session-001", "--check"]
        result = sanitizer.sanitize_value(argv)
        self.assertIsInstance(result, list)
        self.assertEqual("probe", result[0])
        self.assertEqual(["--session-id", "session-001", "--check"], result[-3:])
        self.assertNotIn("SYNTHETIC-ARGV-SECRET", json.dumps(result))
        self.assertNotIn("SYNTHETIC-EQUALS-SECRET", json.dumps(result))
        for raw in (
            'probe --api-key "SYNTHETIC-ARGV-SECRET" --token=SYNTHETIC-EQUALS-SECRET --check',
            "probe --api-key 'SYNTHETIC-ARGV-SECRET' --token='SYNTHETIC-EQUALS-SECRET' --check",
        ):
            with self.subTest(raw=raw):
                result = sanitizer.sanitize_text(raw)
                self.assertNotIn("SYNTHETIC-ARGV-SECRET", result)
                self.assertNotIn("SYNTHETIC-EQUALS-SECRET", result)

    def test_nested_serialized_json_remains_parseable(self):
        inner = {"authToken": "SYNTHETIC-SERIALIZED-SECRET", "turnId": "turn-003"}
        raw = json.dumps({"event": "SessionStart", "stdout": json.dumps({"body": json.dumps(inner)})})
        result = sanitizer.sanitize_text(raw)
        self.assertNotIn("SYNTHETIC-SERIALIZED-SECRET", result)
        outer = json.loads(result)
        body = json.loads(json.loads(outer["stdout"])["body"])
        self.assertEqual("SessionStart", outer["event"])
        self.assertEqual("turn-003", body["turnId"])

    def test_jsonl_preserves_order_and_nonsecret_fields(self):
        records = [
            {"event": "SessionStart", "access_token": "SYNTHETIC-JSONL-SECRET", "source": "resume"},
            {"event": "PostToolUse", "stdout": json.dumps({"api_key": "SYNTHETIC-INNER-SECRET", "exit": 1})},
            {"event": "PostCompact", "source": "compact", "pre_tokens": 4812},
        ]
        result = sanitizer.sanitize_text("\n".join(json.dumps(record) for record in records) + "\n")
        self.assertNotIn("SYNTHETIC-JSONL-SECRET", result)
        self.assertNotIn("SYNTHETIC-INNER-SECRET", result)
        parsed = [json.loads(line) for line in result.splitlines()]
        self.assertEqual(["SessionStart", "PostToolUse", "PostCompact"], [row["event"] for row in parsed])
        self.assertEqual("resume", parsed[0]["source"])
        self.assertEqual(1, json.loads(parsed[1]["stdout"])["exit"])
        self.assertEqual(4812, parsed[2]["pre_tokens"])

    def test_bearer_and_basic_header_text(self):
        basic = base64.b64encode(b"synthetic-user:synthetic-password").decode("ascii")
        raw = ("Authorization: Bearer SYNTHETIC-BEARER-SECRET\n"
               f"authorization: Basic {basic}\n"
               "Proxy-Authorization: bEaReR SYNTHETIC-PROXY-SECRET\n"
               "exit_status=1\n")
        result = sanitizer.sanitize_text(raw)
        for secret in ("SYNTHETIC-BEARER-SECRET", basic, "SYNTHETIC-PROXY-SECRET"):
            self.assertNotIn(secret, result)
        self.assertIn("exit_status=1", result)

    def test_openai_key_families_and_synthetic_jwt(self):
        def encode(value):
            return base64.urlsafe_b64encode(json.dumps(value, separators=(",", ":")).encode()).decode().rstrip("=")

        jwt = ".".join((encode({"alg": "HS256", "typ": "JWT"}),
                        encode({"sub": "synthetic-test-only", "exp": 1}),
                        base64.urlsafe_b64encode(b"synthetic-invalid-signature-0000").decode().rstrip("=")))
        secrets = ["sk-" + "SyntheticExample0123456789" * 2,
                   "sk-proj-" + "SyntheticExample0123456789" * 2,
                   "sk-svcacct-" + "SyntheticExample0123456789" * 2, jwt]
        for secret in secrets:
            with self.subTest(secret=secret):
                result = sanitizer.sanitize_text("debug payload: " + secret + "\nevent=SessionStart\n")
                self.assertNotIn(secret, result)
                self.assertIn("event=SessionStart", result)

    def test_multiline_private_key_blocks(self):
        for kind in ("PRIVATE KEY", "RSA PRIVATE KEY", "OPENSSH PRIVATE KEY"):
            with self.subTest(kind=kind):
                raw = (f"before\n-----BEGIN {kind}-----\n"
                       "U1lOVEhFVElDLVByaXZhdGUtS2V5LUZpeHR1cmU=\n"
                       "Tk9ULTQtUkVBTC1QUklWQVRFLUtFWQ==\n"
                       f"-----END {kind}-----\nafter\n")
                result = sanitizer.sanitize_text(raw)
                self.assertNotIn("U1lOVEhFVElDLVByaXZhdGUtS2V5LUZpeHR1cmU=", result)
                self.assertNotIn("Tk9ULTQtUkVBTC1QUklWQVRFLUtFWQ==", result)
                self.assertIn("before", result)
                self.assertIn("after", result)

    def test_local_ipc_authentication_examples(self):
        for token in ("token:'SYNTHETIC-IPC-SECRET'", 'token:"SYNTHETIC-IPC-SECRET"',
                      r'token:\"SYNTHETIC-IPC-SECRET\"'):
            with self.subTest(token=token):
                raw = "[uds-messaging] Inject messages: JSON.stringify({type:'auth'," + token + "})\nexit=1\n"
                result = sanitizer.sanitize_text(raw)
                self.assertNotIn("SYNTHETIC-IPC-SECRET", result)
                self.assertIn("exit=1", result)

    def test_probe_identity_counts_and_auth_failure_diagnostics_are_preserved(self):
        raw = {
            "sessionId": "session-001", "session_id": "session-001", "turnId": "turn-002",
            "event": "SessionStart", "method": "thread/compact/start", "currentHash": "b" * 64,
            "evaluator_archive_sha256": "a" * 64, "source_digest": "c" * 64,
            "token_usage": {"input_tokens": 123, "output_tokens": 42, "cached_input_tokens": 10},
            "apiKeySource": "none", "authenticated": False, "auth_status": "unauthenticated",
            "error": "authentication_failed", "exit_status": 1,
            "stderr": "Authentication failed: missing credentials. Token refresh failed. HTTP 401.",
        }
        self.assertEqual(raw, sanitizer.sanitize_value(raw))
        self.assertEqual(raw, json.loads(sanitizer.sanitize_text(json.dumps(raw))))

    def test_pure_type_preserving_and_idempotent_operations(self):
        raw = {"nested": [{"accessToken": "SYNTHETIC-IMMUTABLE-SECRET", "ok": True}],
               "argv": ["probe", "--token", "SYNTHETIC-ARGV-IMMUTABLE"], "count": 7, "nothing": None}
        original = copy.deepcopy(raw)
        result = sanitizer.sanitize_value(raw)
        self.assertEqual(original, raw)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["nested"], list)
        self.assertIsInstance(result["nested"][0], dict)
        self.assertEqual(result, sanitizer.sanitize_value(result))
        public_text = sanitizer.sanitize_text(json.dumps(raw))
        self.assertEqual(public_text, sanitizer.sanitize_text(public_text))
        for value in (None, False, True, 0, 3.5, "", "ordinary output\r\nexit=0\r\n"):
            with self.subTest(value=value):
                self.assertEqual(value, sanitizer.sanitize_value(value))
                self.assertIs(type(value), type(sanitizer.sanitize_value(value)))
                if isinstance(value, str):
                    self.assertEqual(value, sanitizer.sanitize_text(value))


if __name__ == "__main__":
    unittest.main()

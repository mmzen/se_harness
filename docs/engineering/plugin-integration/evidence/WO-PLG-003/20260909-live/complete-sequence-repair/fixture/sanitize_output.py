"""Redact public CLI/app-server observations without changing their verdicts.

Adapted from the separately tested Claude probe sanitizer. These pure functions
do not read profiles or publish files. Login/device-auth output and credential
files must never enter the evidence pipeline, even through this sanitizer.
Public results are sanitized observations, not byte-exact raw transcripts.
"""
from __future__ import annotations

import json
import re
from typing import Any


REDACTED = "[REDACTED]"
_SECRET_SUFFIXES = (
    "token", "password", "passwd", "secret", "apikey", "authorization",
    "cookie", "cookies", "privatekey", "secretkey", "credentials",
)
_SECRET_ASSIGNMENT = re.compile(
    r'''(?ix)(?<![a-z0-9])[a-z0-9_-]*
    (?:token|password|passwd|secret|api[_-]?key|authorization|cookies?|private[_-]?key|secret[_-]?key|credentials)
    ["'\\]*\s*[:=]\s*\S'''
)
_SECRET_OPTION = re.compile(
    r'''(?ix)(?<![a-z0-9_-])--[a-z0-9_-]*
    (?:token|password|passwd|secret|api[_-]?key|authorization|cookies?|private[_-]?key|secret[_-]?key|credentials)
    ["']?(?:=|\s+)\S'''
)
_PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.S,
)
_BEARER = re.compile(r"(?i)\bBearer\s+[^\s\"',;]+")
_API_TOKEN = re.compile(r"\bsk-(?:proj-|svcacct-|ant-)?[A-Za-z0-9_-]{10,}\b")
_JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")


def _secret_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", key.lower())
    return normalized.endswith(_SECRET_SUFFIXES)


def _ending(text: str) -> str:
    return "\r\n" if text.endswith("\r\n") else "\n" if text.endswith("\n") else ""


def sanitize_value(value: Any) -> Any:
    """Copy a JSON-compatible value, redacting credentials and nested outputs.

    Evidence fields such as sessionId, currentHash, input_tokens and diagnostics
    are retained. Credential flags retain their names and argument positions.
    """
    if isinstance(value, dict):
        return {
            key: REDACTED if _secret_key(key) else sanitize_value(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        result = []
        redact_next = False
        for item in value:
            if redact_next:
                result.append(REDACTED)
                redact_next = False
                continue
            if isinstance(item, str) and item.startswith("--"):
                flag, separator, argument = item.partition("=")
                if _secret_key(flag[2:]):
                    result.append(flag + "=" + REDACTED if separator else flag)
                    redact_next = not separator
                    continue
            result.append(sanitize_value(item))
        return result
    if isinstance(value, str):
        return sanitize_text(value)
    return value


def sanitize_text(text: str) -> str:
    """Redact JSON, JSONL and diagnostic text; preserve unchanged text exactly.

    Credential-bearing non-JSON lines are removed whole because shell/debug
    quoting cannot reliably delimit a secret. Multiline private-key blocks are
    removed before line processing. Structured records retain nonsecret fields.
    """
    text = _PRIVATE_KEY.sub("[REDACTED: private key]", text)
    try:
        document = json.loads(text)
    except (ValueError, TypeError):
        document = None
    if isinstance(document, (dict, list)):
        cleaned = sanitize_value(document)
        return text if cleaned == document else json.dumps(cleaned, ensure_ascii=False) + _ending(text)

    result = []
    for line in text.splitlines(keepends=True):
        ending = _ending(line)
        try:
            document = json.loads(line)
        except (ValueError, TypeError):
            document = None
        if isinstance(document, (dict, list)):
            cleaned = sanitize_value(document)
            result.append(line if cleaned == document else json.dumps(cleaned, ensure_ascii=False) + ending)
            continue
        normalized = re.sub(r"\\+(['\"])", r"\1", line)
        if "[uds-messaging]" in line and "Inject messages" in line:
            result.append("[REDACTED: IPC authentication example]" + ending)
        elif (_SECRET_ASSIGNMENT.search(normalized) or _SECRET_OPTION.search(normalized) or _BEARER.search(normalized)
              or _API_TOKEN.search(normalized) or _JWT.search(normalized)):
            result.append("[REDACTED: sensitive output line]" + ending)
        else:
            result.append(line)
    return "".join(result)

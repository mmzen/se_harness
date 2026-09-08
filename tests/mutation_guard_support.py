"""Trusted mutation-authority fixture for tests outside boundary coverage."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness import __version__


def trusted_mutation_authority(
    repository: Path,
    *,
    operation: str,
    allow_upgrade_transition: bool = False,
    require_archive: bool = False,
    upgrade_work_order: str | None = None,
) -> SimpleNamespace:
    del operation, allow_upgrade_transition, require_archive, upgrade_work_order
    lock_path = Path(repository) / ".engineering-harness.lock"
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.is_file() else {}
    evaluator = lock.get("evaluator") if isinstance(lock.get("evaluator"), dict) else {
        "version": lock.get("tool_version") or __version__,
        "payload_manifest": "se-harness-installed-payload-v1",
        "payload_sha256": "a" * 64,
    }
    value = {
        "schema": "se-harness-evaluator-evidence-v1",
        "role": "released-evaluator",
        "evaluator": {
            "version": evaluator.get("version"),
            "payload_manifest": evaluator.get("payload_manifest"),
            "payload_sha256": evaluator.get("payload_sha256"),
            "archive_name": evaluator.get("archive_name"),
            "archive_sha256": evaluator.get("archive_sha256"),
        },
        "origins": {
            "python_executable": "<evaluator-root>/bin/python",
            "module": "<evaluator-root>/lib/se_harness/runtime_identity.py",
            "distribution": "<evaluator-root>/lib/site-packages",
            "templates": "<evaluator-root>/share/se-harness/templates/repository/standard",
            "entry_point": "<evaluator-root>/bin/harnessctl",
        },
        "environment": {
            "isolated_python": True,
            "user_site_enabled": False,
            "pythonpath_present": False,
            "entry_point_resolved": True,
            "checkout_excluded": True,
        },
        "diagnostics": [],
    }
    raw = (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    return SimpleNamespace(
        evidence_bytes=raw,
        evidence_sha256=hashlib.sha256(raw).hexdigest(),
        upgrade_authorization=None,
    )


def patch_mutation_authority(case: unittest.TestCase) -> None:
    """Trust the mutation authority for the rest of `case` (SPEC-TST-002 TST-HYG-007).

    Tests outside the guard's own boundary coverage call this once in `setUp`;
    the patch is undone by the case's cleanup.
    """
    guard = mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=trusted_mutation_authority)
    guard.start()
    case.addCleanup(guard.stop)

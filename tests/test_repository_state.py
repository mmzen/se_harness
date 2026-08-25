from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.agent_contract import validate_contract
from se_harness.repository_state import (
    EvaluatorIdentity,
    RepositoryObservationError,
    _decode_z_paths,
    _index_entries,
    observe_repository,
    observe_stable_repository,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VECTORS = (
    REPOSITORY_ROOT
    / "tests/fixtures/agentic_execution/phase4/authority/canonical-vectors.json"
)


def _run(root: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _evaluator(payload: str = "2" * 64) -> EvaluatorIdentity:
    return EvaluatorIdentity("se-harness", "0.7.0", payload, "3" * 64)


def _repository(root: Path) -> None:
    _run(root, "init")
    _run(root, "config", "user.email", "tests@example.invalid")
    _run(root, "config", "user.name", "Test Operator")
    _write(root, ".engineering-harness.lock", "{}\n")
    _write(root, ".gitignore", "*.cache\n")
    _write(root, "docs/engineering/WORKFLOW.json", "{}\n")
    _write(root, "docs/engineering/DECISION_RIGHTS.md", "# Rights\n")
    _write(
        root,
        "docs/engineering/work-orders/WO-TST-OBS.md",
        """+++
id = "WO-TST-OBS"
type = "work_order"
title = "Observer fixture"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[execution_scope]
paths = ["docs/"]
+++

# Observer fixture
""",
    )
    _write(root, "tracked.txt", "tracked\n")
    _run(root, "add", ".")
    _run(root, "commit", "-m", "fixture")


class LiveRepositoryObservationTests(unittest.TestCase):
    def test_real_git_observation_is_stable_bounded_and_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _repository(root)
            stable = observe_stable_repository(
                root, work_order_id="WO-TST-OBS", evaluator=_evaluator()
            )
            self.assertTrue(stable.clean)
            self.assertEqual(2, stable.captures)
            self.assertNotIn(str(root), stable.document.canonical_bytes.decode("utf-8"))

            _write(root, "ignored.cache", "not observed\n")
            ignored = observe_stable_repository(
                root, work_order_id="WO-TST-OBS", evaluator=_evaluator()
            )
            self.assertEqual(stable.document.sha256, ignored.document.sha256)
            self.assertTrue(ignored.clean)

            _write(root, "untracked.txt", "observed\n")
            dirty = observe_stable_repository(
                root, work_order_id="WO-TST-OBS", evaluator=_evaluator()
            )
            self.assertFalse(dirty.clean)
            self.assertNotEqual(stable.document.sha256, dirty.document.sha256)
            substituted = observe_repository(
                root, work_order_id="WO-TST-OBS", evaluator=_evaluator("f" * 64)
            )
            self.assertNotEqual(dirty.document.sha256, substituted.sha256)

            _write(root, ".engineering-harness.lock", '{"changed":true}\n')
            drifted = observe_repository(
                root, work_order_id="WO-TST-OBS", evaluator=_evaluator()
            )
            self.assertNotEqual(
                dirty.document.value["governance"]["managed_lock_sha256"],
                drifted.value["governance"]["managed_lock_sha256"],
            )

    def test_alias_links_case_conflicts_and_submodules_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            _repository(root)
            with self.assertRaisesRegex(RepositoryObservationError, "AEXOBS005"):
                observe_repository(
                    root / "docs", work_order_id="WO-TST-OBS", evaluator=_evaluator()
                )
            if hasattr(os, "symlink"):
                try:
                    os.symlink(root / "tracked.txt", root / "linked.txt")
                except OSError:
                    pass
                else:
                    with self.assertRaisesRegex(RepositoryObservationError, "AEXOBS002"):
                        observe_repository(
                            root, work_order_id="WO-TST-OBS", evaluator=_evaluator()
                        )

        with self.assertRaisesRegex(RepositoryObservationError, "AEXOBS007"):
            _decode_z_paths(b"Name.txt\0name.txt\0", "fixture")
        _, conflicts, submodules = _index_entries(b"100644 " + b"a" * 40 + b" 2\tfile.txt\0")
        self.assertTrue(conflicts)
        self.assertFalse(submodules)
        _, conflicts, submodules = _index_entries(b"160000 " + b"a" * 40 + b" 0\tmodule\0")
        self.assertFalse(conflicts)
        self.assertTrue(submodules)

    def test_stability_restarts_the_pair_and_stops_when_bound_is_reached(self) -> None:
        vector = json.loads(VECTORS.read_text(encoding="utf-8"))["repository_observation"]["value"]
        first = validate_contract(vector)
        changed = json.loads(json.dumps(vector))
        changed["filesystem"]["regular_file_manifest_sha256"] = "e" * 64
        second = validate_contract(changed)
        with mock.patch(
            "se_harness.repository_state.observe_repository",
            side_effect=[first, second, second],
        ), mock.patch("se_harness.repository_state._git", return_value=b""):
            result = observe_stable_repository(
                Path.cwd(),
                work_order_id="WO-TST-002",
                evaluator=_evaluator(),
                max_captures=3,
            )
        self.assertEqual(second.sha256, result.document.sha256)
        self.assertEqual(3, result.captures)

        with mock.patch(
            "se_harness.repository_state.observe_repository",
            side_effect=[first, second],
        ), mock.patch("se_harness.repository_state._git", return_value=b""):
            with self.assertRaisesRegex(RepositoryObservationError, "AEXOBS004"):
                observe_stable_repository(
                    Path.cwd(),
                    work_order_id="WO-TST-002",
                    evaluator=_evaluator(),
                    max_captures=2,
                )


if __name__ == "__main__":
    unittest.main()

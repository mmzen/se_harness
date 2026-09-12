"""Independent process used only by ownership crash and contention tests.

The marker and release files are caller-selected temporary test observations,
not an evaluator interface or a production environment-variable fault switch.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from unittest import mock


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-module", required=True)
    parser.add_argument("--source-root")
    parser.add_argument("--target", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--binding")
    parser.add_argument("--digest", required=True)
    parser.add_argument("--identity", required=True)
    parser.add_argument("--fault-stage")
    parser.add_argument("--fault-path")
    parser.add_argument("--marker")
    parser.add_argument("--release")
    parser.add_argument("--pause-seconds", type=float, default=25)
    args = parser.parse_args()
    if args.source_root:
        package = Path(args.source_root) / "se_harness"
        spec = importlib.util.spec_from_file_location("se_harness", package / "__init__.py",
                                                     submodule_search_locations=[str(package)])
        module = importlib.util.module_from_spec(spec)
        sys.modules["se_harness"] = module
        spec.loader.exec_module(module)
    spec = importlib.util.spec_from_file_location("ownership_independent_acceptance", args.test_module)
    test = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = test
    spec.loader.exec_module(test)
    from se_harness import installer, skill_ownership as ownership, evaluator_identity

    def fault(stage, path=None):
        if stage != args.fault_stage or args.fault_path is not None and path != args.fault_path:
            return
        marker = Path(args.marker)
        staged_marker = marker.with_suffix(".tmp")
        staged_marker.write_text(json.dumps({"stage": stage, "path": path}), encoding="utf-8")
        staged_marker.replace(marker)
        deadline = time.monotonic() + args.pause_seconds
        while time.monotonic() < deadline:
            if args.release and Path(args.release).is_file():
                return
            time.sleep(0.01)
        raise RuntimeError("independent test worker timed out waiting for release")

    with contextlib.ExitStack() as stack:
        if args.source_root:
            identity = evaluator_identity.InstalledEvaluatorIdentity(**json.loads(args.identity))
            stack.enter_context(mock.patch("se_harness.mutation_guard.require_mutation_authority",
                                            side_effect=test.trusted_source_authority))
            for module in (installer, ownership, evaluator_identity):
                if hasattr(module, "installed_evaluator_identity"):
                    stack.enter_context(mock.patch.object(module, "installed_evaluator_identity", return_value=identity))
        if args.fault_stage:
            stack.enter_context(mock.patch.object(ownership, "_fault_hook", side_effect=fault))
        try:
            result = ownership.apply_skill_ownership(
                Path(args.target), provider=args.provider,
                binding_input=Path(args.binding) if args.binding else None,
                expected_plan_sha256=args.digest,
            )
        except (ownership.OwnershipError, installer.HarnessError) as exc:
            result = {"passed": False, "exception": type(exc).__name__, "message": str(exc)}
        print(json.dumps(result, sort_keys=True))
        return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())

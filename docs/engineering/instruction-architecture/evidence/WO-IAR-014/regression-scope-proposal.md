# Proposed regression-test scope correction

The first full run executed 1,098 tests: 12 failures, 2 errors and 15 skips.
The failures found so far are assertions about the previous instruction layout.
They must be assessed against SPEC-IAR-014, not removed just to obtain a pass.

Most affected tests are already inside WO-IAR-013/014. Two current failures are
outside every approved work order:

- `tests/test_artifact_catalog.py` requires old detailed policy text in the root.
- `tests/test_artifact_authoring_policy.py` requires the root to link directly
  to the authoring guide, instead of discovering type checklists through the
  selected drafting procedure.

The planned removal of AGENTS/CLAUDE fragments also affects existing install,
readiness, provenance and lifecycle fixtures outside those work orders. The
approved test paths include a nonexistent `tests/test_installer.py`; the existing
installer tests are spread across the actual regression suite.

Authorize one separate, test-only work order covering `tests/`, plus its own
formal record and evidence directory. This scope permits only regression and
fixture changes required by the already approved instruction split, discovery,
ownership migration and host delivery under SPEC-IAR-014.

Preserve assertions for lifecycle authority, exact command arguments, gate
failures, historical evidence and owner-byte preservation. Add replacement
coverage for intentionally retired instruction routes. Keep fixtures independent
of candidate outputs. Do not weaken production gates, remove unrelated tests,
change implementation requirements or rewrite accepted history.

Use the existing requirements, SPEC-IAR-014 and VER-IAR-014. This proposal adds
no product behavior, external action, release or real host-setting authority.

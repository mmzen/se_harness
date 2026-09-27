+++
id = "VER-RLO-007"
type = "verification"
title = "Verify publication reads both supported evaluator lock schemas"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[relations]
verifies = ["REQ-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T19:07:08Z"
decided_by = "assurance-owner"
reason = "The human accepted the bounded correction proposal in this task: Ok for the correction. This contract formalizes the proposal's schema compatibility, refusal, identity preservation, frozen-main replay and regression checks; it grants no candidate verification or publication."
+++

# Verify publication lock compatibility

## Independence

Expected identities come from committed release records and test inputs, not
the repaired helper. SPEC-RLO-001 requires exact released-record resolution.
SPEC-PLG-021 defines schema 3 for repository ownership and schema 4 for plugin
ownership, including readable historical provider bindings. The human's
accepted correction proposal selects these existing semantics for publication.

## Requirement-to-evidence matrix

| Requirement | Method | Case | Pass condition |
| --- | --- | --- | --- |
| REQ-RLO-001 | test | LOCK01 | Evaluator acquisition and bound-evidence resolution accept schema 3 and schema 4 with provider `plugin`, including older binding fields. Returned identities are exactly the input identities. |
| REQ-RLO-001 | test | LOCK02 | Both readers reject unsupported schemas and missing, malformed or non-plugin schema-4 ownership. |
| REQ-RLO-001 | test | LOCK03 | Schema-4 support preserves rejection of mismatched evaluator identities, tampered evidence, incomplete archive identities and invalid integrity settings. Existing schema-3 refusal tests still pass. |
| REQ-RLO-001 | demonstration, inspection | LOCK04 | Both read-only publication entry points accept the frozen merged governance snapshot at `523ff825773e05c970c041ecee5c22bfabedaa3f`. The release plan retains RLS-SEH-028's candidate, version, hashes and first integration commit. Retain the original refusals. |
| REQ-RLO-001 | test, inspection | LOCK05 | Publication regression suites, the full source suite and applicable repository checks pass. The diff stays inside WO-RLO-010 and preserves every pre-existing formal artifact, root lock and bound release input. |

## Execution and evidence

Use existing tests in `tests/test_dashboard_publication.py` and
`tests/test_release_orchestration.py`. Use real disposable Git history for
record resolution. Exercise the committed governance snapshot through the
current helper; do not replace its lock or evidence to obtain a pass.

Run the focused tests and full source suite on the available Windows Python,
reporting its exact version and all skips. The source suite uses committed
fixture bytes with command-local Git line-ending conversion disabled, matching
the already disclosed release-build input condition. Do not change fixtures.
The existing CI remains required before integration; local evidence makes no
Linux or hosted-run claim. Run isolated released 0.18.0 doctor, validate,
phase preflight, Git-derived handoff, distribution validation and CLI help.

Retain commands, outputs, identities, failures, preservation comparison and
the code review under `evidence/WO-RLO-010/`. Prepare a commit-bound VREC for
the human assurance decision. This contract authorizes no publication, tag,
deployment, release-record rewrite, package rebuild or root adoption.

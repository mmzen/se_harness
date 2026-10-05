+++
id = "REQ-HAG-009"
type = "requirement"
title = "Distinguish admissible draft incompleteness from invalid artifact relationships"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "The evaluator provides a read-only result for one selected draft that distinguishes explicitly permitted authoring incompleteness from structural invalidity, using the same declared relationship types as repository validation and work-order preflight."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "DEC-HAG-001 extend-evaluator option accepted by mmzen in the conversation on 2026-10-04; released evaluator observations retained under WO-HAG-001."

[relations]
derives_from = ["CAP-HAG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T13:24:31Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-HAG-009, SPEC-HAG-004, VER-HAG-002 and WO-HAG-002 for local implementation with required commit-bound verification in this conversation. Reviewed manifest SHA-256: e36a47fb59f1bf1f856aa8a47c20189bc84d9d53d787fce505e6bc0f895eabe8. All complete reviewed bytes matched; only the confirmed assurance table was completed before preview. This approval grants bounded local implementation and required verification preparation, not verification acceptance, publication, release or governor adoption. DEC-HAG-001 remains unchanged."
+++

# Distinguish admissible draft incompleteness from invalid artifact relationships

## Why

A hosted draft author needs to save unfinished work while receiving a reliable
refusal for a structurally wrong relationship. Evaluator 0.22.0 rejects a
generated requirement's placeholder link but returns valid for a link to an
existing release record. Its work-order preflight checks only the selected
governing chain. This dependency correction keeps evaluation in the evaluator.

## Acceptance

- A generated draft template and a requirement with its capability link not yet
  supplied receive an admissible-draft result with explicit incomplete findings.
- A requirement linked to an existing capability receives an admissible result.
- A requirement linked to an existing release record, a capability linked to a
  requirement, or a non-template missing target receives a refused result.
- Malformed TOML, duplicate IDs or metadata, ID/type disagreement and supplied
  lifecycle history are refused. No result writes or approves an artifact.
- Normal repository validation rejects the prohibited pairs even when no work
  order selects the draft. Existing approval requirements remain effective.

SPEC-HAG-004 defines the boundaries and VER-HAG-002 supplies independent cases.
This new requirement adds evaluator behavior; it does not amend accepted hosted
definitions, select a future released version, or resolve decision identity.

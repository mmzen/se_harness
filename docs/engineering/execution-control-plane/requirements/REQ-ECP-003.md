+++
id = "REQ-ECP-003"
type = "requirement"
title = "The harness writes and rebinds evidence packets"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN an actor runs `harnessctl evidence` for a work order and checkpoint, THE SYSTEM SHALL write or rebind an evidence packet whose machine header carries the artifact, checkpoint, and current formal snapshot digest without altering retained body content."
verification_method = ["test"]
priority = "must"
source = "review section 6; WO-HUP-007 re-binding"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The harness writes and rebinds evidence packets

## Rationale

Evidence is agent-authored Markdown matched by substring on three literal lines
(`artifact:`, `checkpoint:`, `formal_snapshot_sha256:`)
(se_harness/workflow_compliance.py:266-291; docs/notes/agentic-execution-
review-2026-08.md:131-135). The formal snapshot digest moves on any artifact
edit, so `WO-HUP-007` re-bound its evidence twice by hand (docs/notes/agentic-
execution-review-2026-08.md:235-237, :288-293). The harness neither writes nor
rebinds evidence (docs/notes/agentic-execution-review-2026-08.md:238-239).
Evidence file name, directory, and body are decisions the agent makes alone
(section 6). A harness-authored packet turns "remember to rebind" into "cannot
get wrong".

## Behavior

- Trigger: `harnessctl evidence <repo> --artifact <WO> --checkpoint <name>`
  runs.
- Response: the packet under `<domain>/evidence/<WO>/` exists afterwards with a
  machine header naming the artifact, the checkpoint, and the formal snapshot
  digest computed at that moment; a pre-existing packet keeps every retained
  body byte below the header and only the header changes; the result reports the
  path and the digest written.
- On failure: when the work order does not exist, the checkpoint is not a public
  checkpoint, or the packet cannot be written atomically, nothing is written and
  the command fails closed with a coded predicate.

## Assumptions and dependencies

- The snapshot digest is the chain-scoped one required by REQ-ECP-016 once
  that requirement is met; until then it is the current formal digest.
- `check` keeps recognising the header fields it matches today, so packets
  written by the harness satisfy `review_evidence_available`.
- Atomic write primitives already exist in `integrity.py`.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-003.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** no packet exists for `WO-X-004` at checkpoint `handoff`.

**When** `harnessctl evidence . --artifact WO-X-004 --checkpoint handoff` runs.

**Then** `docs/engineering/x/evidence/WO-X-004/handoff.md` exists, its header
carries `artifact: WO-X-004`, `checkpoint: handoff`, and the current
`formal_snapshot_sha256`, and a following `check` reads
`review_evidence_available` as `pass`.

### Example: failure behavior

**Given** a packet exists with a stale digest and 2 KB of retained findings; a
merge to `main` moved the snapshot.

**When** the same command runs.

**Then** the header digest is replaced by the current one, the 2 KB body is
byte-identical, and the result names the old and new digests.

## Open decisions

None.

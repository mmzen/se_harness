+++
id = "WO-DOC-002"
type = "work_order"
title = "Retain the verified README and provenance restoration"
status = "verified"
owners = ["repository-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-003", "REQ-DST-006", "REQ-REV-006", "REQ-REV-007"]
specifications = ["SPEC-DST-001", "SPEC-REV-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-REV-001", "ADR-REV-001"]
verification = ["VER-DST-001", "VER-REV-001"]
+++

# Work Order

Create one local Git commit retaining the verified root README rewrite, `WO-DOC-001` and its evidence, and the eight revision-provenance documents restored from `bbae027` after their deletion in `f828b2e` invalidated the artifact graph.

The accountable repository owner explicitly authorized this commit on 2026-08-11 with the instruction `commit change`. The authorization does not include amending or rewriting existing commits, creating a tag, pushing to a remote, releasing, or publishing.

The resulting commit is intentionally discovered through Git history instead of recorded inside this work order, avoiding self-referential commit metadata.

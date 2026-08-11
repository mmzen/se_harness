+++
id = "WO-DOC-001"
type = "work_order"
title = "Rewrite the distribution README as an operational guide"
status = "verified"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-003", "REQ-DST-006", "REQ-REV-006", "REQ-REV-007"]
specifications = ["SPEC-DST-001", "SPEC-REV-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-REV-001", "ADR-REV-001"]
verification = ["VER-DST-001", "VER-REV-001"]
+++

# Work Order

Rewrite the root `README.md` as the practical entry point for installing, adopting, operating, validating, visualizing, verifying, and developing SE Harness.

The rewrite must reflect the implemented single standard template, the real `harnessctl` command surface, the formal artifact graph, the five questions answered by Harness Explorer, readiness and anomaly semantics, candidate-then-governance commit provenance, and explicit human authority boundaries. It must remove broken character encoding and avoid claiming that implementation or tests are formal artifact types.

The accountable human authorized this bounded documentation change on 2026-08-11 with the instruction `yes, rewrite`, then confirmed continuation with `retry`. The work order does not authorize code changes, template changes, commits, tags, pushes, releases, or publication.

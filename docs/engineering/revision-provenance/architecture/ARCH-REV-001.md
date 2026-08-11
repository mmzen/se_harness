+++
id = "ARCH-REV-001"
type = "architecture"
title = "Revision provenance architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-REV-001", "REQ-REV-002", "REQ-REV-003", "REQ-REV-004", "REQ-REV-005", "REQ-REV-006", "REQ-REV-007", "REQ-REV-008"]
+++

# Architecture

Formal Markdown metadata remains the authoritative graph. Git supplies only bounded observed values through explicit CLI operations. Verification and release records are later governance artifacts referencing a prior candidate commit, avoiding self-reference.

The standard-library validator owns structural and cross-record consistency. The CLI owns safe Git observation and record preparation. The dashboard owns derived comparison and presentation. No layer creates approval, tags, commits, or release state.

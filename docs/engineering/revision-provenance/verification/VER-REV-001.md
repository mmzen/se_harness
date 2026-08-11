+++
id = "VER-REV-001"
type = "verification"
title = "Verify revision provenance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-REV-001", "REQ-REV-002", "REQ-REV-003", "REQ-REV-004", "REQ-REV-005", "REQ-REV-006", "REQ-REV-007", "REQ-REV-008"]
+++

# Verification Contract

Automated cases shall cover both record types; 40- and 64-character commits; invalid format and object-format mismatch; dirty verification; missing, absolute, escaping, symlinked, and absent evidence; incorrect relation target types; inconsistent release and verification commits; duplicate active release versions; backward compatibility; no-HEAD and dirty Git failures; atomic non-overwrite; ready-only CLI output; dashboard structured provenance, lineage, exact/different/not-assessable states, and findings; standard-template installation and hash-based upgrade; source and wheel operation.

End-to-end verification shall create a temporary Git repository, commit candidate source and evidence, capture a verification record naming that candidate, commit the governance record, prepare a release record that still names the candidate, and prove that no command commits, tags, approves, releases, or publishes.


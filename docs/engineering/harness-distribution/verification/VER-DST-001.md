+++
id = "VER-DST-001"
type = "verification"
title = "Verify standard harness distribution"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
verifies = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
+++

# Verification Contract

Automated tests shall prove: there is one template and no profile CLI; init installs a complete valid repository; adopt preserves pre-existing files and labels observations; known conflicts produce no partial writes; traversal and symlink escapes fail closed; validate and dashboard preserve exit behavior; doctor detects drift; upgrade plans by default, updates unmodified files, and preserves customized files; package metadata exposes `harnessctl` and includes template data.

End-to-end verification shall initialize a temporary repository and adopt a separate existing repository, then validate both and generate both dashboards. The distribution repository artifact graph and all unit tests must pass.


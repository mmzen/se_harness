+++
id = "ARCH-DST-001"
type = "architecture"
title = "Repository-native distribution architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-DST-001", "REQ-DST-002", "REQ-DST-003", "REQ-DST-004", "REQ-DST-005", "REQ-DST-006"]
+++

# Architecture

The system has three boundaries: a standard-library Python control plane in `se_harness/`, an immutable canonical template in `templates/repository/standard/`, and repository-local installed files owned by each target. The lock records provenance but never makes the distribution repository authoritative for target product intent.

Writes are contained below an explicitly resolved target and use same-directory temporary replacement. External services, credentials, code execution inferred from repository content, and installation profiles are outside the architecture.


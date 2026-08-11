+++
id = "ARCH-DST-002"
type = "architecture"
title = "Shared instruction and repository-context ownership boundaries"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-DST-007", "REQ-DST-008"]
+++

# Architecture

The installed instruction surface has three ownership classes:

1. Harness-owned bounded fragments provide shared invariants and cross-agent loading.
2. Repository-owned content outside shared-root markers provides local agent rules.
3. A one-time repository-context seed provides a discoverable location for explicit local facts and becomes repository-owned immediately.

The lock distinguishes `fragment`, `managed`, and `seed` modes. Fragment and managed modes retain hashes for safe upgrade classification. Seed mode retains only whether the installation has accounted for the path, preventing the distribution from treating repository facts as immutable or regenerating an intentionally removed file.

No repository scan may author commands, architectural claims, or lifecycle authority in the context file.

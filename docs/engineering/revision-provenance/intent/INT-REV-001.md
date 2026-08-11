+++
id = "INT-REV-001"
type = "intent"
title = "Make implementation and release revisions authoritative"
status = "approved"
owners = ["product-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent

The harness explains why work exists from intent through requirements and work orders, while the dashboard currently observes only the checked-out Git revision. That observation does not prove which committed source state was verified or authorized for release.

The desired outcome is an auditable lineage from intent and requirements to an immutable verified commit and, when separately authorized, an immutable released commit. Reusable verification and release contracts remain policy; commit-bound records represent individual assurance and release decisions.

The change must preserve human decision rights, cleanly distinguish declared provenance from an observed checkout, support SHA-1 and SHA-256 Git object formats, and avoid an impossible record that attempts to contain the hash of its own commit.


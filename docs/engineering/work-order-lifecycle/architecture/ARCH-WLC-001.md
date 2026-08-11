+++
id = "ARCH-WLC-001"
type = "architecture"
title = "Policy-aware lifecycle validation architecture"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
constrains = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
+++

# Architecture: Policy-aware lifecycle validation architecture

## Components

- `scripts/validate_engineering_artifacts.py` owns policy parsing and authoritative current-state consistency validation.
- `scripts/generate_harness_dashboard.py` consumes validator output and retains only genuinely derived findings.
- `templates/repository/standard/` is the canonical installation boundary.
- Root managed files are the self-installed operational copy protected by `.engineering-harness.lock`.
- Formal work-order files retain explicit lifecycle corrections; VREC and RLS files remain immutable.

## Data flow

The validator loads artifacts and repository configuration, derives verified work coverage from eligible VRECs, and adds an `E010` diagnostic for configured violations. Explorer uses that report and the same policy parser, projects readiness and provenance, and does not recreate the invariant as a warning.

## Constraints

Use Python 3.11+ standard library only. Treat repository configuration and artifacts as untrusted input. Keep configuration-disabled compatibility. Preserve canonical/root parity and the existing no-automatic-authority boundary.

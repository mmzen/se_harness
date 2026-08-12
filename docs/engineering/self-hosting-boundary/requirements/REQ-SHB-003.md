+++
id = "REQ-SHB-003"
type = "requirement"
title = "Prove harness runtime and import identity"
status = "implemented"
owners = ["requirements-steward", "security-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN any self-hosting CI lane invokes harness behavior, THE SYSTEM SHALL emit and verify machine-assessable runtime identity sufficient to detect version ambiguity, current-directory import shadowing, and source-versus-wheel substitution."
verification_method = "automated-test-and-security-review"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Prove harness runtime and import identity

## Required identity evidence

Every lane records at least:

- declared role: `governor`, `candidate-source`, or `candidate-package`;
- Python executable and version;
- harness version;
- resolved `se_harness.__file__` and distribution/template origin;
- expected checkout, virtual-environment, or wheel boundary;
- candidate commit when the role is candidate source or package;
- governor wheel SHA-256 when the role is governor.

## Fail-closed checks

- Governor modules must resolve below the isolated governor environment and outside the checkout.
- Candidate-source modules must resolve below the exact checkout.
- Candidate-package modules and entry points must resolve below the fresh candidate environment and outside the checkout.
- Import isolation must not depend only on command naming. Current working directory, `PYTHONPATH`, user-site packages, entry-point script location, and subprocess inheritance are exercised explicitly.
- Any mismatch, missing field, ambiguous path, or unexpected import succeeds in no lane.

Identity data is bounded diagnostic evidence and must not disclose credentials, tokens, environment dumps, or repository file contents.

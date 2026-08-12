+++
id = "REQ-SHB-002"
type = "requirement"
title = "Confine candidate execution to declared test roles"
status = "implemented"
owners = ["requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN candidate source or a candidate package executes, THE SYSTEM SHALL identify it as evidence-producing code under test and SHALL restrict it to its declared source-test or package-acceptance targets."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Confine candidate execution to declared test roles

## Required behavior

- Candidate-source checks resolve `se_harness` from the reviewed checkout deliberately and label their assurance source as candidate.
- Candidate-package checks install the exact built wheel in a fresh environment with no editable source or checkout path injection.
- Candidate templates are exercised through fresh and upgrade fixtures outside the operational host repository.
- Candidate `doctor`, preflight, validation, dashboard, init, adopt, and upgrade behavior is evidence only; it does not approve work, verify a VREC, or release an RLS.
- No candidate acceptance target may reuse the governor environment or operational host lock.
- Candidate tests must detect fallback from the intended source or wheel to another installation.

## Consumer model

This execution-role separation is specific to developing the harness implementation. It does not introduce alternative consumer installation profiles.

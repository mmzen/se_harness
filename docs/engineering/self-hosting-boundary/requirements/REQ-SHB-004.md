+++
id = "REQ-SHB-004"
type = "requirement"
title = "Separate governor, source, and package CI gates"
status = "implemented"
owners = ["requirements-steward", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN pull-request or release-candidate CI evaluates the harness repository, THE SYSTEM SHALL run distinct governor, candidate-source, and candidate-package gates with non-overlapping integrity targets and explicit dependency semantics."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Separate governor, source, and package CI gates

## Governor gate

- Download and hash-check the exact released governor wheel.
- Prove same-version governor installation integrity using a temporary repository created by the governor.
- Run only explicitly compatible, read-only bootstrap or graph checks against the checkout from the isolated installed distribution.
- Never run governor `doctor` against candidate-managed files and never import the candidate through the checkout working directory.

## Candidate-source gate

- Run the full test suite and candidate-specific formal validation, preflight, doctor, Explorer, security, and migration tests from explicit checkout source.
- Report candidate evidence honestly and retain the selected pull-request work order.

## Candidate-package gate

- Build eligible artifacts from the exact candidate, install the wheel in a fresh environment, and exercise fresh-install and upgrade fixtures outside the checkout.
- Verify package/template completeness, archive safety, reproducibility, and source-to-wheel identity.

## Composition

All required lanes must pass. A governor failure cannot be hidden by candidate success; candidate success cannot be described as independent governor evidence; and package acceptance cannot be replaced by source-tree execution.

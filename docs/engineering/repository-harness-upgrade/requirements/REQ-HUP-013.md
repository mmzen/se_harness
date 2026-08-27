+++
id = "REQ-HUP-013"
type = "requirement"
title = "Prove complete-graph operation under the 0.7.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN the 0.7.0 root candidate is produced, THE SYSTEM SHALL prove exact public 0.7.0 doctor, integrity, complete-graph validation, inspection, dashboard, preflight and supported-runtime behavior on the complete checkout with zero formal errors and no compatibility view."
verification_method = "automated-test"
priority = "must"
source = "INT-HUP-004; REQ-HUP-006"
measure = "0 structure, governance and policy errors; 0 doctor FAIL; suites OK on the default runtime and Python 3.11"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.7.0 root

## Rationale

An adopted root that cannot judge the complete graph would block every
later act. The proof must come from the exact released evaluator run
directly on the checkout, not from candidate source and not through a
predecessor view, and it must show the managed CI gate selecting 0.7.0.

## Required response

- Run exact public 0.7.0, installed outside the checkout, directly against
  the complete checkout: `doctor`, `validate`, `inspect`, `dashboard`, and
  review preflight for `WO-HUP-006`.
- Require zero structure, governance and policy errors; account for every
  maintenance warning by code and count.
- Prove the managed Engineering Harness workflow selects exact 0.7.0.
- Run the complete repository suites on the default runtime and on Python
  3.11, and the repository-required checks.
- Compare product source and templates, package version, release records,
  tags, publication and Pages workflows and maintenance refs with the base
  commit: unchanged.

## Failure behavior

Any formal error, any doctor failure, a red suite, a managed lane that
selects another version, or a changed non-root byte is a stop condition for
`WO-HUP-006` and is reported, not worked around.

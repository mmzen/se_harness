+++
id = "REQ-AGR-004"
type = "requirement"
title = "Provide deterministic repeatable CLI inputs"
status = "implemented"
owners = ["engineering-owner", "requirements-steward"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN capture-verification or prepare-release receives repeated scope options, THE SYSTEM SHALL validate the complete selection and emit deterministic relation arrays while preserving existing single-option behavior."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Provide deterministic repeatable CLI inputs

Repeated `--work-order`, `--verification`, `--evidence`, and `--verification-record` options form explicit sets. Unknown IDs, wrong artifact types, duplicates, incomplete coverage, unsafe paths, existing outputs, and dirty repositories fail before any record is written.

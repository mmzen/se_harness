+++
id = "REQ-AGR-001"
type = "requirement"
title = "Capture aggregate verification scope"
status = "implemented"
owners = ["quality-owner", "requirements-steward"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN verification is captured for a release candidate containing multiple release-bearing work orders, THE SYSTEM SHALL create one ready verification record that explicitly enumerates every selected work order, applicable verification contract, and retained evidence path at one clean full commit."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AGR-001"]
+++

# Requirement: Capture aggregate verification scope

The selected work-order set, verification-contract set, and evidence-path set must be non-empty, explicit, duplicate-free, and deterministically ordered. Every selected work order must declare its selected verification coverage, and every selected verification contract must apply to at least one selected work order.

+++
id = "INT-WLC-001"
type = "intent"
title = "Make work-order lifecycle status unambiguous"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make work-order lifecycle status unambiguous

## Problem

The repository uses `approved`, `implemented`, and `verified` work-order statuses inconsistently. Completed publication work remains `approved`, while governance decisions are marked `verified` even though no commit-bound VREC covers those decision work orders. The formal validator accepts both conditions and Harness Explorer reports only the latter as derived warnings.

## Desired outcome

Authorization, completion, commit-bound assurance, and release are distinguishable. Governance-only work completes without creating an infinite verification-governance chain, configured verification provenance is enforced by the formal validator, installed repositories inherit the same rules, and existing decisions retain their authority and evidence.

## Success indicators

- Completed governance-only and publication work orders use `implemented`.
- A `verified` or `released` work order is covered by a verified or released VREC whenever configured provenance is required.
- Formal validation blocks violations without a duplicate Explorer warning.
- Canonical and self-installed harness files remain consistent.

## Authority boundary

This intent does not authorize a verification-record transition, release record, tag, commit, push, pull request, workflow dispatch, package upload, or deployment.

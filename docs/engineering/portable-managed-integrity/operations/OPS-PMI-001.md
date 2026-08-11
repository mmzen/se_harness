+++
id = "OPS-PMI-001"
type = "operating_contract"
title = "Operate portable managed-file integrity"
status = "draft"
owners = ["service-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
assures = ["REQ-PMI-002", "REQ-PMI-003", "REQ-PMI-004", "REQ-PMI-006", "REQ-PMI-007", "REL-PMI-001"]
+++

# Operating Contract: Operate portable managed-file integrity

## Service level objectives

Every supported LF or CRLF checkout with logically unchanged schema-2 managed text passes doctor deterministically. Every actual managed-content change remains visible for manual review, and no unsafe legacy migration overwrites content.

## Observability

Use `harnessctl doctor`, `harnessctl upgrade` planning, the artifact validator, full tests, and release evidence to observe schema, mode, exact or canonical equality, customizations, malformed entries, source/template parity, and package installation health.

## Alerts and escalation

Treat stale schema-2 digests, source/canonical divergence, invalid UTF-8, unsupported modes, ambiguous legacy mismatches, unexpected overwrites, nondeterministic locks, and fresh-install doctor failures as blocking. Escalate binary asset needs or migration ambiguity to engineering, security, and repository owners.

## Capacity and cost boundaries

Operate locally in linear time using the standard library. No service, database, network call, background monitor, or persistent content cache is required.

## Backup and recovery

Version control retains locks, templates, evidence, and candidate commits. Preserve customized content and legacy evidence. Recover from a failed applied upgrade by retaining the prior atomic lock and reviewing the unchanged target; never repair diagnostics by hand-editing hashes.

## Security and compliance controls

Maintain SHA-256, strict UTF-8, path containment, symlink rejection, bounded fragments, no target execution, no body disclosure, atomic writes, customization ownership, and separate human governance authority.

## Automated remediation envelope

Automation may write schema-2 locks only as the final step of an otherwise safe init, adopt, or applied upgrade. It may not rewrite customized or ambiguous legacy content, change Git settings, transition verification or release records, create tags, or publish artifacts.

## Runbooks

Run doctor before verification and release. For legacy advisories, review the upgrade plan, apply only a safe non-customized plan, rerun doctor, and retain evidence. For customization, compare owner intent with the current canonical template and resolve through an explicitly authorized change rather than digest edits.

## Evidence retention

Retain lock schema/mode, tool version, doctor and upgrade results, raw and canonical diagnostic hashes when needed, customization decisions, candidate commit, verification record, wheel checksum, platform matrix, and release authorization.

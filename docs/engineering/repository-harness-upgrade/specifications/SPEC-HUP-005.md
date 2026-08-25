+++
id = "SPEC-HUP-005"
type = "specification"
title = "Standard-root adoption contract for the released successor of 0.6.0"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
specifies = ["REQ-HUP-010", "REQ-HUP-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "technical-owner"
+++

# Specification: Standard-root adoption contract for the released successor of 0.6.0

## Scope

The transaction that replaces this repository's 0.6.0 root evaluator with
the first public release whose released record covers `WO-ADS-001`,
`WO-ADS-002`, and `WO-RSK-001`. It reuses `SPEC-HUP-002`'s transaction
shape and adds the postconditions those work orders introduced.

## Precondition (HUP5-PRE)

**HUP5-PRE-001:** A `released` release record on `main` covers the three work
orders. The work order carries `[evaluator_upgrade]` with
`prior_lock_sha256` equal to the current lock's canonical digest,
`target_version`, `target_payload_sha256`, `target_archive_name`, and
`target_archive_sha256` copied from that record, `scope = "standard-root-only"`,
`publication = "immutable"`, `authorized_by = "repository-owner"`. The table is
completed before approval; a draft without it cannot be approved.

## Proof (HUP5-PRV)

**HUP5-PRV-001:** The successor is installed from the exact wheel into an
environment outside the checkout; `identity released-evaluator` with
`--expected-version`, `--evaluator-wheel-sha256`, and
`--evaluator-payload-sha256` from the record passes; the evidence is retained
under the domain's evidence directory.

## Transaction (HUP5-TRX)

**HUP5-TRX-001:** `upgrade` is run from the isolated successor: plan first,
reviewed against the expected managed set (the 0.6.0 set plus
`docs/engineering/OPERATING_CARD.md` and `docs/engineering/templates/RISK.template.md`,
and the `[risk]` section merged into the installation file), then `--apply`.
Fragment blocks of `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`
are replaced byte-for-byte inside markers; owner content outside is untouched.

**HUP5-TRX-002:** `.engineering-harness.toml` `tool_version` and
`.github/workflows/engineering-harness.yml` `SE_HARNESS_VERSION` equal
`target_version`; the lock is schema 3 bound to the successor's wheel and
payload digests.

## Postconditions (HUP5-PST)

**HUP5-PST-001:** Under the isolated successor: `doctor` 0 FAIL; `validate`
0 errors; `preflight --phase start` for one approved work order lists
`ENGINEERING_HARNESS.md`, `docs/engineering/OPERATING_CARD.md`, `AGENTS.md`,
then the chain; `check --checkpoint handoff` on an in-progress work order
without changed paths renders a corrective command that differs from the
evaluated command; the router contains `## Scope of these obligations`.

**HUP5-PST-002:** `raise-risk` on a scratch domain creates a `raised` risk the
root validator accepts and the handoff check blocks on; the scratch risk is
withdrawn or removed before the evidence commit.

**HUP5-PST-003:** The declared candidate-versus-root exceptions in
`tests/test_artifact_catalog.py`, `tests/test_validation_taxonomy.py`,
`tests/test_dashboard_webui.py`, `tests/test_artifact_authoring.py`, and
`tests/test_lifecycle_state_contract.py` are retired: the tests compare
template to root and pass with equality, or compare template to template.

**HUP5-PST-004:** `docs/notes/developing-se-harness.md` and
`docs/engineering/README.md` state the new governor version and date.

## Error and recovery behavior

A failed plan review, a customized managed file, or a failed postcondition
stops the transaction; recovery follows `docs/notes/evaluator-recovery-runbook.md`
with the prior lock retained in evidence.

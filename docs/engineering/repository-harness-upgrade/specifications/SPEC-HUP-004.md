+++
id = "SPEC-HUP-004"
type = "specification"
title = "Version-independent governor-transition assessment contract"
status = "approved"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
specifies = ["REQ-HUP-008", "REQ-HUP-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "technical-owner"
+++

# Specification: Version-independent governor-transition assessment contract

## Scope

Replace the repository-owned, always-on 0.5.0 predecessor assessment with a
generic, read-only governor-transition assessment and correct the remaining
raw-byte role assertion exposed by Linux CI. The managed current-governor
workflow, product runtime, candidate templates, release history, publication
workflows, and root lock remain unchanged.

## Transition inputs

- Full target `HEAD` and one event-derived full base commit.
- Base and target `.engineering-harness.toml` plus canonical lock bytes.
- One approved work order containing `[evaluator_upgrade]` when versions differ.
- Canonical committed evaluator-upgrade evidence keyed to that work order.
- Exact public target wheel acquired outside the checkout.

Pull requests use the event's base SHA. Non-creation pushes use the event's
before SHA after ancestry validation. A branch-creation push may use the unique
merge base with the configured default branch only when the full history is
available. Zero, abbreviated, missing, ambiguous, or unsuitable base identities
fail closed.

## State selection

1. Parse base and target configurations and locks without importing checkout
   candidate code.
2. If selected versions and canonical locks are equal, emit a deterministic
   `not_applicable` transition observation and succeed only if the checkout is
   unchanged. Managed CI supplies ordinary validation.
3. If selected versions differ, discover exactly one approved upgrade work
   order matching the base lock hash and target version.
4. Validate the work-order archive and payload declarations and its canonical
   transaction evidence.
5. Verify the downloaded target archive, isolated installed payload, entry
   point, module, templates, and interpreter origins.
6. Run isolated target-governor doctor and complete validation on the target
   checkout.
7. Emit canonical JSON and human output, then prove the checkout is unchanged.

## Trust and security rules

- PR-authored configuration is an input, not authority. Approval state,
  evaluator-upgrade declaration, base lock hash, transaction evidence, and
  archive/payload verification must all agree.
- Do not use `latest`, unbounded version ranges, checkout imports, user site,
  `PYTHONPATH`, persistent credentials, write tokens, or external mutation.
- Do not evaluate a successor root with the predecessor executable.
- Do not construct a compatibility view of current governance.
- The resolver and workflow must produce concise diagnostics without dumping
  wheel bytes, repository contents, environment secrets, or command output
  beyond bounded limits.

## Cross-platform role assertion

`tests/test_inspection.py` must replace raw root/template byte inequality with
distinct normalized paths, root lock integrity, and the existing candidate
semantic assertions. Tests must cover equal canonical LF bytes and differing
working-tree line endings without treating either materialization as authority.

## Workflow contract

Keep `.github/workflows/predecessor-evaluator-assessment.yml` during this
bounded correction to avoid silently removing an existing check. Rename its
human purpose to governor-transition assessment, fetch full history without
persisted credentials, provide event-derived base information to the resolver,
run the exact result, prove a clean checkout, and upload bounded observation
artifacts on success or failure. No concrete governor version, wheel filename,
archive hash, release-record ID, or historical compatibility omission belongs
in the workflow.

## Error and recovery behavior

Every trust, identity, evidence, ancestry, graph, checkout-immutability, or
cross-platform failure exits nonzero before any privileged action. Recovery is
a reviewed successor commit under the same approved work order or a separately
approved scope amendment; CI never rewrites governance state.

## Candidate and VREC implications

Candidate `ea7b837438a0fb32b8f6b51c630e98b9706ea039` remains immutable and failed
hosted qualification. `VREC-HUP-003` remains a ready historical proposal until
an assurance owner explicitly rejects or supersedes it. A corrected candidate
requires a later aggregate VREC covering `WO-HUP-002` and `WO-HUP-004`.

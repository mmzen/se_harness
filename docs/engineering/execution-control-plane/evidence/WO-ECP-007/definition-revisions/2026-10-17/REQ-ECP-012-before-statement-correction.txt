+++
id = "REQ-ECP-012"
type = "requirement"
title = "A fresh consumer repository passes doctor"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-10-17"
statement = "WHEN a consumer runs `harnessctl init`, commits the result, and runs `harnessctl doctor`, THE SYSTEM SHALL exit 0 with no failed check."
verification_method = ["test", "demonstration"]
priority = "must"
source = "complexity audit P0-1"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: A fresh consumer repository passes doctor

## Selected WO-ECP-007 revision

This revision applies only to remaining work under WO-ECP-007. The [preserved accepted version](../evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/REQ-ECP-012.txt) has complete-file SHA-256 `6fcaf0f6b601286efb593e081512f80b4eca2acfa7c4b4101c0030c0f492ce8a` and Git blob `231f6947f4ff2b426c40a202e9cc690fb0e09ab0` at commit `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38`. The [activation receipt](../evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json) records the actual human authority and before/after identities. Without that recorded authority this replacement does not govern work. Original lifecycle events remain unchanged; this is not a native evaluator revision event. Earlier completed work and evidence retain their original definition meaning. Retained historical problem descriptions are context, not claims about current code. Unrelated skills and capabilities retain their existing obligations.

## Rationale

`init`, a commit, then `doctor` exits 1 in every fresh repository:
`hash_bound_classes.json` declares the class `governance-migration-protocol`
over `se_harness/governance_migration*.py`, files that exist only in this
repository, and the managed `.gitattributes` fragment pins them
(se_harness/hash_bound_classes.json:19-32;
templates/repository/standard/gitattributes.fragment:4-6;
se_harness/hash_bound.py:454-457, :485-499). Reproduced in-tree: `doctor` prints
`FAIL hash-bound-class-declared` and `FAIL hash-bound-attribute-effective`, and
the 0.7.1 wheel carries identical bytes (docs/notes/complexity-
audit-2026-08.md:97-116). The acceptance lane is structurally blind to it
(docs/notes/complexity-audit-2026-08.md:112-115). A green `init` followed by a
red `doctor` breaks portability for the primary audience.

## Behavior

- Trigger: minimal installation in an empty consumer, followed by Git initialization,
  explicit Git evidence integration (or an equivalent owner rule), and a commit.
- Response: doctor exits 0 when its other required checks pass. No check requires
  a file specific to the SE Harness repository.
- Minimal init itself writes only the configuration and lock. It does not opt the
  owner into Git integration.
- In a Git repository lacking effective evidence attributes, doctor reports the
  named readiness failure, including before the first evidence file. The remedy
  is explicit Git integration or an equivalent owner rule.
- A damaged required attribute or managed byte remains a failure. This revision
  grants no warning-based authority and changes no lifecycle or evidence gate.

## Assumptions and dependencies

REQ-IAR-031 governs the two-file default installation and optional integrations.
An explicit --integration git selection installs the existing evidence attributes;
an equivalent repository-owner rule also satisfies them. Existing hash-bound
checks remain required. The removed self-hosting class stays removed.
Use a separately installed candidate wheel for Windows and Linux demonstrations.

## Acceptance examples

1. Minimal init writes exactly configuration and lock and preserves owner files.
2. In Git with no evidence attributes, doctor reports the named attribute failure.
3. Explicitly select Git integration, commit, then run doctor: exit 0 if other
   required checks pass. Repeat with an equivalent owner rule.
4. Damage a required attribute or managed byte: doctor fails and identifies it.

Run installed-wheel demonstrations on Windows and Linux. A missing or skipped
platform is unverified, not a pass.

## Open decisions

None.

+++
id = "REQ-REB-027"
type = "requirement"
title = "Apply an evaluator upgrade from any installed released evaluator without a separate packet"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN a released evaluator installed outside the checkout runs harnessctl upgrade --apply on a standard root at an older version, THE SYSTEM SHALL apply the reviewed managed plan and record the installed evaluator's version and payload digest as the root identity, with no work-order packet."
verification_method = "automated-test"
priority = "must"
source = "Owner direction of 2026-08-27 on WO-HUP-006; supersedes REQ-REB-005"
measure = "one command, one atomic transaction, zero required declarations beyond the installed evaluator"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T15:20:02Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', on the owner's direction that the evaluator upgrade must be simple: the MG007 work-order packet and the MG004 and RID022 archive-digest requirements are retired, the installed evaluator's version and payload digest are its identity, index installs pass the managed lane, and the candidate-evidence lane selects the acceptance operation by the verifier's capability. REQ-REB-005 is superseded under WO-REB-027."
+++

# Requirement: Apply an evaluator upgrade from any installed released evaluator without a separate packet

## Rationale

The 0.7.0 adoption showed the cost of the packet model `REQ-REB-005`
introduced: an evaluator-upgrade work order carrying prior-lock and
target-digest declarations, a wheel-file install so that a PEP 610 archive
digest exists, and mutation-guard refusals (`MG004`, `MG007`) whenever either
is missing. The repository owner directed on 2026-08-27 that the install
process be simple: install the released evaluator, run the upgrade, review
the plan, apply. Which repository change is authorized remains a matter of
repository policy (a work order for the changed files), not a gate the tool
enforces on the transaction.

## Required response

- Accept the installed evaluator as the target identity: its version and its
  installed-payload digest, plus the archive digest when the installation
  recorded one.
- Plan as today; on `--apply`, write the reviewed managed files and the
  schema-3 lock atomically, whether or not the version changes.
- Retain canonical evaluator-transition evidence when `--evidence-output`
  is given; otherwise retain none and say so.
- Keep the customization and conflict refusals of the ordinary upgrade.

## Failure behavior

A customized or conflicting managed file, an unreadable lock, an evaluator
that cannot prove its own identity, or a partial write stops the transaction
and leaves the pre-write state. The absence of a work-order packet or of an
archive digest is not a failure.

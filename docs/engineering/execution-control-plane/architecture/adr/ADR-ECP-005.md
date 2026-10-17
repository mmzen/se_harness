+++
id = "ADR-ECP-005"
type = "adr"
title = "Evict self-hosting machinery from the shipped product"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-10-17"

[relations]
decides = ["ARCH-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# ADR: Evict self-hosting machinery from the shipped product

## Selected WO-ECP-007 revision

This revision applies only to remaining work under WO-ECP-007. The [preserved accepted version](../../evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/ADR-ECP-005.txt) has complete-file SHA-256 `a4d955f6908ea0489b091ed4a29c57d708c6458cf4ea274773566482dc8e50c0` and Git blob `e327758c1d6354ab7df107d0b9837984201ce8b5` at commit `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38`. The [activation receipt](../../evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json) records the actual human authority and before/after identities. Without that recorded authority this replacement does not govern work. Original lifecycle events remain unchanged; this is not a native evaluator revision event. Earlier completed work and evidence retain their original definition meaning. Retained historical problem descriptions are context, not claims about current code. Unrelated skills and capabilities retain their existing obligations.

## Status

Proposed.

## Context

Between 08-20 and 08-24 this repository had to release itself while
governed by an evaluator that could not parse its own new records. The
bridge built for that is still live in the wheel, in CI, and in the consumer
validator: the `governance-migration-protocol` hash-bound class
(`se_harness/hash_bound_classes.json:19-32`) and its
`gitattributes.fragment` lines make `init`, a commit, then `doctor` exit 1
in every fresh repository (`docs/notes/complexity-audit-2026-08.md`, P0-1);
`qualify predecessor-view` in the wheel imports the unpackaged
`repository_tools` (`se_harness/release_qualification.py:634`); six
`RLS-SEH-*` identifiers are hard-coded in
`se_harness/legacy_release_evidence.py:36` and two other generic files
(P1-2); `validate_governor_transition.py` refuses the upgrade the owner
wants (P0-3); `recovery_rehearsal.py` exercises none of the installer
(P1-9); and three shipped skills stub the evaluator
(`templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`).
`ADR-REB-009` decided five typed `qualify` operations; `SPEC-REB-002` rule
14 requires a disposable rehearsal; `SPEC-LRE-001` rule 11 freezes the six
identifiers as a code constant.

## Decision drivers

- Remove the remaining shipped repository-ID exception.
- Preserve the minimal-install boundary and explicitly resolve Git readiness.
- Keep required release and adoption controls working.
- Reuse the existing build patches, checker and tests.
- Preserve accepted definitions and historical evidence.
- Leave unrelated skill and execution-model work with its existing authority.

## Considered options

### Preserve the old broad eviction plan

This would remove active release/adoption functions and recreate retired legacy
declarations. It increases work and risk without being needed to remove the
remaining product exception. Reject for narrowed WO-ECP-007.

### Correct the remaining boundary through existing components

Use the existing Explorer build patch mechanism and portable-surface check.
Reconcile the installation criterion, keep release/adoption controls, and preserve
historical definitions. This is the proposed choice. Its cost is a bounded UI
correction, regression checks and explicit definition revision.

### Leave the product unchanged

No implementation cost, but the viewer retains a repository-ID exception and the
current package guard does not detect it. This does not satisfy the agreed outcome.

## Decision

For the remaining consumer-boundary work, retain the active qualification
operations, independent verifier boundary and repository adoption checker.
Correct the shipped viewer's repository-ID exception using the existing build
patch mechanism and extend the existing wheel check to detect its return.
Preserve minimal initialization and require effective Git evidence attributes before doctor passes. Do not revive retired legacy declarations or repeat completed removals.

This revises only the unexecuted cleanup direction associated with WO-ECP-007.
Do not supersede ADR-REB-009 through this work. Earlier retirement decisions and
historical evidence retain their original references. The accepted source record
is preserved and this proposal cannot govern before recorded activation.

## Consequences

- The viewer uses the same selection rules for equivalent records regardless of ID.
- Package checks catch a return of the known exception, including generated UI.
- Historical documentation links remain permitted; executable exceptions do not.
- Release qualification, candidate verification and adoption checks remain active.
- The installation sequence is explicit; the confirmed current-behavior choice changes guidance and tests, not installer behavior.
- Definition activation still needs a supported route or a separately reviewed, explicit user authorization. Existing accepted versions and earlier evidence remain intact.
- No new scanner service, general parser or release framework is introduced.

## Validation

Use the activated VER-ECP-007 revision for the selected REQ-ECP-012/013 work:
paired viewer behavior, deterministic generation, built-wheel boundary checks,
negative package controls and Windows/Linux installed-consumer checks. Retain
existing release/adoption regression checks and historical-byte comparisons.
This work does not re-qualify the unrelated shipped-skills contract.

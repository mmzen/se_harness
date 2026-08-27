+++
id = "WO-ECP-002"
type = "work_order"
title = "Harness-authored evidence, identifier allocation, and pull-request bodies"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work replaces the evidence contract that `QGP-G4I-EVIDENCE` evaluates, allocates the identifiers every future artifact carries, and generates the pull-request body the CI selector parses. Handoff, verification, and release decisions rely on these bytes being exactly right, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/artifact_layout.py",
  "se_harness/workflow_compliance.py",
  "se_harness/github_ci.py",
  "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed",
  "docs/notes/harnessctl-reference.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-003", "REQ-ECP-004", "REQ-ECP-005"]
specifications = ["SPEC-ECP-002"]
verification = ["VER-ECP-002"]
+++

# Work Order: Harness-authored evidence, identifier allocation, and pull-request bodies

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-003`,
`REQ-ECP-004`, `REQ-ECP-005`, `SPEC-ECP-002`, and `VER-ECP-002` are
separate acts by their owners and precede approval of this work order. This
work order follows `WO-ECP-001` (its `evidence` command binds the packet
that `check --from-git` evaluates) and precedes `WO-ECP-003`.

## Objective

Move three pieces of state the agent carries today into the harness: the
evidence packet (today agent-authored Markdown matched by substring,
`se_harness/workflow_compliance.py:266-291`, re-bound by hand twice on
`WO-HUP-007`; the 2026-08 agentic execution review, section 5, weaknesses 6
and 7), new identifiers (today checked only in the current tree; review
section 3, "Multiple agents"), and the pull-request body (today typed by the
agent, with the CRLF trailer recurring often enough that `REQ-ADS-004`
exists; review section 6).

## In scope

- `harnessctl evidence <repo> --artifact WO --checkpoint handoff` writing or
  rebinding a packet with a machine header per `ECP-EVD-*`, retaining body
  bytes, refusing a tampered body.
- `review_evidence_available` reading the machine header through one parser
  and no longer matching substrings.
- `create-artifact` allocating the lowest free identifier across every local
  ref per `ECP-IDA-*`, using `se_harness/artifact_layout.py` for the domain
  and type layout.
- `harnessctl pr-body <repo> --artifact WO` emitting the LF-terminated body
  per `ECP-PRB-*`; `se_harness/github_ci.py` parsing it back unchanged; the
  template pull-request seed pointing at the command.
- Reference note sections; tests; work-order-keyed evidence.

## Out of scope

- Changing what the CI selector accepts (`WO-ECP-003`); rewriting any
  historical evidence packet under any domain; the widened digest; any
  change to lifecycle states, gate predicates, decision rights, or root
  managed copies; any lifecycle transition of any artifact.

## Authorized decision envelope

The implementation agent may decide the header field order and file name
convention within the domain evidence directory, the refs enumeration
command, test names, and note wording. It may not change the three header
keys, allocate across remote refs, emit any byte other than LF as a line
end, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, preflight, and snapshot
  readings.
- Root managed copies are not edited; the template seed is.
- LF line endings; assert bytes against blobs and against a hex dump of the
  generated body.
- Stage every deletion before any preflight or check run.

## Expected change surface

CLI parser and dispatch, the artifact layout module, the compliance
module's evidence predicate, the CI parser, one template seed, one note,
tests, evidence.

## Required verification

Execute `VER-ECP-002` completely plus the repository-required checks; run
the complete suite on Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-002/`:
packet bytes before and after rebind with a byte diff, the ref listing and
allocated identifiers, the generated body bytes and line-end hex dump,
per-platform test figures, and the complete changed-path set.

## Stop and escalate conditions

Stop if the machine header cannot be made compatible with the existing
`QGP-G4I-EVIDENCE` predicate without changing its identifier, if allocation
needs a remote fetch, if the generated body cannot be parsed by the
unchanged root `scripts/select_harness_work_order.py`, or if any path
outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-002 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.

+++
id = "SPEC-RLO-006"
type = "specification"
title = "Repository delivery planning and completion checks"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
contract = "Report completion only when every declared delivery surface has matching retained evidence; preserve the separate authority and publication boundaries."

[relations]
specifies = ["REQ-RLO-018", "REQ-RLO-019", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T19:38:37Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the seven-artifact release-delivery package and required commit-bound verification request on 2026-09-28. Reviewed SHA-256 93f82e8118171632319744149ce945617e493ea853134fc505debdd1bf23736a; transition input SHA-256 93f82e8118171632319744149ce945617e493ea853134fc505debdd1bf23736a. Legacy evaluator role engineering-owner records the human decision; Codex applies it. Only the confirmed assurance fields and confirmation text were added to WO-RLO-011. Implementation is bounded by that work order; no external action is authorized."
+++

# Specification: Repository delivery planning and completion checks

## In plain words

The release operator keeps one delivery plan and adds observations as work
finishes. A local check reports what remains. It cannot approve or publish work.

## Scope

This contract adds repository-owned closeout guidance and a read-only reporting
command. It consumes existing publisher and qualification evidence. It does not
replace the evaluator publisher, modify an accepted release record, or change
portable harness lifecycle rules. It applies to newly prepared delivery plans;
historical RLS and verification records remain unchanged.

The current marketplace correction will use this procedure in subsequent work.
This contract does not select that package's version or authorize publication.

## Terms

- **Surface:** A public package, route or current instruction set used to obtain
  or operate the release.
- **Delivery plan:** Reviewed supporting data for the selected delivery. It
  references formal authority but does not create authority.
- **Observation:** A retained result tied to exact inputs, a source and a time.
- **Closeout:** Assessment of remaining delivery work, separate from a formal
  lifecycle transition.

## Rules

**RLO-DLV-001.** Complete plan

Before publication, the operator prepares a JSON delivery plan in the selected
work's durable evidence directory. The human release owner reviews its scope
under the existing decision procedure. Record the review reference; do not
invent a new formal artifact type or approval lifecycle.

The plan identifies the selected release contract and RLS, evaluator version
and wheel digest, plugin source commit and version when applicable, and public
destinations. Plugin and evaluator versions are independent. Exact package
digests that cannot exist until later assembly remain explicitly pending until
qualified; pending values cannot pass closeout.

Include these five surfaces once each: `evaluator`, `marketplace`,
`documentation`, `demonstration`, and `release_markers`. The guide identifies
their components: GitHub/PyPI distributions; both host catalogs, expanded
packages and archives; current README/install/publication guidance; Pages;
and `latest`/`last` respectively. A surface cannot be omitted because it is
unchanged or deferred. The marketplace's claimed hosts are explicit.

Each surface names its destination, owner, disposition, expected identity,
governing work or decision reference, and required observations. Disposition
is exactly one of:

| Disposition | Required explanation | Closeout treatment |
| --- | --- | --- |
| `update` | Work reference and next action until delivered. | Needs matching evidence for the new identity. |
| `unchanged` | Existing identity and reviewed compatibility justification for this delivery. | Needs identity readback and compatibility evidence. |
| `deferred` | Human decision reference, reason, owner, follow-up work and revisit trigger. | Always remains outstanding; never counts as delivered. |

Deferral does not alter an accepted contract or waive a required gate. A plan
that conflicts with formal scope returns to the existing decision procedure.

**RLO-DLV-002.** Publication handoff

The repository guide describes this sequence with concrete inputs, outputs,
existing commands, retained evidence and the next responsible actor:

1. Select accepted release scope and prepare the delivery plan.
2. Perform the existing evaluator release preparation and authorized publication.
3. Observe the public evaluator wheel and compare its locked digest.
4. Assemble the plugin from the selected committed source and that public wheel.
5. Check the generated tree and qualify the exact package and documented routes.
6. Obtain any required verification acceptance and exact publication authority.
7. Update the public marketplace through the existing history-preserving procedure.
8. Observe public fresh installation and update on the claimed hosts.
9. Reconcile current availability claims, then run overall closeout.

Plugin assembly may depend on evaluator publication. Do not make the evaluator
publisher wait on that dependent plugin. At each pause, retain outstanding
work, its owner and next action. Replays inspect actual state and retain prior
failures. They do not move immutable tags, overwrite packages, force a branch,
or repeat an uncertain external write.

**RLO-DLV-003.** Evidence and identity

Expected identities come from the reviewed release plan, accepted contracts,
selected committed manifests and released evaluator inputs. Do not generate
expected values from the candidate result being assessed.

Retain these observations for an updated surface:

| Surface | Minimum evidence |
| --- | --- |
| `evaluator` | Existing publisher result and independent public distribution/install readback for the selected RLS and digests. |
| `marketplace` | Both source manifests, assembly inventories and bundled wheel identity; builder check; package qualification; public ref and installed-content readback for fresh and update routes on each claimed host. |
| `documentation` | Review of current version, availability and support claims against those identities and observed limits; links checked in source or assembled context as applicable. |
| `demonstration` | Deployed URL and provenance observation for the selected governance snapshot. |
| `release_markers` | Actual marker targets and references to their separate human authorization. |

Public marketplace observations identify the repository URL, branch, resolved
commit, host/version, route, time, installed package content digest and evaluator
identity. Local qualification cannot satisfy this requirement. The update case
also identifies the starting installed version/source. A package with an equal
version label but different bytes must not pass an identity comparison.

For an unchanged surface, retain identity readback and the compatibility review
against this delivery's exact inputs. An old success cannot be reused merely
because the version string is equal. Unobserved platforms remain unclaimed.

**RLO-DLV-004.** Read-only completion command

Provide a repository script, `scripts/check_release_delivery.py`, with explicit
plan, observations and evidence-root inputs. It reads local files and emits a
JSON result and a concise human report. It uses the Python standard library,
does not access credentials or the network, and performs no writes or commands
from its inputs. The guide supplies one complete example and the exact command.

Use small versioned JSON formats for plan, observations and result. Observations
bind the plan's byte digest and retain per-surface observed identities, status,
source/time and evidence paths with SHA-256 digests. The implementation may
choose field layout, but the guide and tests must establish one unambiguous
format. Reject unknown schema versions, duplicate keys or surface IDs, missing
required fields and invalid dispositions. Reject evidence paths that resolve
outside the selected evidence root, including symlink escapes.

Check evidence existence and digests, the exact plan binding, required
observations and identity equality. Retain distinct failed, missing and pending
results rather than collapsing them into a reassuring score. A bare `pass`
without the required retained observations is insufficient.

The command assesses the supplied evidence; it does not independently execute
native-host tests or judge the truth of a human compatibility/documentation
review. Those assessments remain identified, retained inputs under the existing
verification procedure. The report states this limit and the observation time.

**RLO-DLV-005.** Honest completion

Report formal RLS state as an observation with provenance, evaluator publication
status, and overall delivery status in separate fields. Overall delivery is
`complete` only when every surface is satisfied, the RLS is observed released,
and no deferred item remains. Otherwise it is `incomplete`.

Each incomplete item includes its reason, owner and next action. Malformed input
must still produce a non-complete diagnostic rather than an apparent success.
Exit status is zero only for complete delivery; distinguish valid-but-incomplete
inputs from invalid inputs with documented nonzero codes.

An `unchanged` surface can be satisfied with its identity and compatibility
evidence. A `deferred` surface cannot. The result is derived operational
evidence; it grants no decision right, state transition or external authority.

**RLO-DLV-006.** Procedure integration and boundaries

Replace the repository release guide's evaluator-only completion sentence with
the distinction in RLO-DLV-005. Link the new closeout guide from the release
sequence and plugin publication handoff. The latter edit adds the handoff only;
the later marketplace work updates its version-specific commands and claims.

Keep the existing publisher result schema and workflow intact. Do not add a
portable harness command, gate, state or new privileged workflow. Preserve all
accepted definitions, historical release evidence and published bytes.

A prose-only checklist was considered. It cannot reliably catch a missing
surface, stale identity or omitted observation. One local validator with
deterministic fixtures is the smallest addition that covers these failures.
Network polling, publication automation and a general orchestration framework
are outside this design. No new architecture decision is needed: the existing
repository-to-harness dependency direction and trust boundaries are unchanged.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing surface or unsupported input | Report invalid plan and no completion. | Name the input and missing/invalid field. |
| Missing evidence or pending/deferred work | Report incomplete delivery with follow-up. | Name the surface, observation, owner and next action. |
| Conflicting identity or evidence digest | Report incomplete delivery and preserve both values. | Name expected and observed identities. |
| Unreadable evidence or path escape | Refuse the affected input without executing it. | Name the input and reason. |

## Examples

- Evaluator 0.19.0 is published, but the declared newer marketplace package is
  absent: `incomplete`, with the marketplace handoff still pending.
- The public marketplace contains different bytes under the expected version:
  `incomplete`, with an identity mismatch.
- Every surface has matching observations and no deferral remains: `complete`
  as an operational result, with no formal or external mutation.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-RLO-018` | RLO-DLV-001, RLO-DLV-002, RLO-DLV-006 |
| `REQ-RLO-019` | RLO-DLV-003, RLO-DLV-004 |
| `REQ-RLO-020` | RLO-DLV-004, RLO-DLV-005, RLO-DLV-006 |

## Not decided here

- Internal function layout and JSON field spelling within the stated contract.
- The exact package/version selected by the subsequent marketplace work.
- External publication, profile changes and provider-directory submission.

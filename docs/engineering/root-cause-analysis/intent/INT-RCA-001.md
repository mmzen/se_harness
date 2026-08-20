+++
id = "INT-RCA-001"
type = "intent"
title = "Retain actionable learning from the 0.5.0 governance deadlock"
status = "draft"
owners = ["product-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
+++

# Intent: Retain actionable learning from the 0.5.0 governance deadlock

## Problem

The 0.5.0 release became blocked when candidate `se_harness` code and the independently released root evaluator were mixed inside a special self-hosting lifecycle. Recovery facts currently span conversation history, commits, public releases, workflow runs, and local draft artifacts. Without one reviewed retrospective, maintainers may misunderstand why newer-format artifacts lacked authority, repeat the product/evaluator conflation, or treat the emergency bypass as a normal release path.

## Desired outcomes

- Maintainers can read one concise, evidence-backed account of the impact, detection, root cause, contributing factors, recovery, and lessons.
- The record clearly distinguishes candidate evidence, released-evaluator authority, and the bounded emergency bypass.
- Completed safeguards and unimplemented preventive actions remain visibly separate.
- A public tracking issue links the RCA to accountable follow-up without making the RCA itself formal authority.

## Actors and stakeholders

- Repository maintainers and engineering owners use the RCA to avoid recurrence.
- Product and technical owners review the causal analysis and proposed boundaries.
- Assurance and security owners assess the evidence and residual risk.
- Release owners use the lessons when sequencing evaluator upgrades and future releases.
- Consumers benefit indirectly from a safer, more predictable release process.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| Canonical repository RCA for this incident | 0 | 1 | At merge |
| Material release and recovery claims backed by inspectable evidence | Fragmented | All enumerated claims | Review preflight |
| Statements that candidate code may govern the root lifecycle | Ambiguous special case | 0 | RCA review |
| Public prevention trackers linked to the RCA | 0 | At least 1 | At merge |

## Non-goals

- Retroactively authorize, verify, or release `0.5.0a1` or `0.5.0` through the normal lifecycle.
- Promote or repair the abandoned local 0.5.0 draft packet.
- Implement the preventive actions tracked by GitHub issue #81.
- Change runtime behavior, managed templates, CI, publishing workflows, package contents, tags, releases, or the root evaluator version.
- Assign personal blame.

## Principles and immutable constraints

- The developed product must not govern its own root lifecycle.
- A version string or matching file format does not establish evaluator authority.
- Candidate source and packages produce evidence only; the root evaluator is an independently released immutable distribution executed outside the checkout.
- The RCA is supporting retrospective documentation, not a formal lifecycle record or substitute for the artifacts in this domain.
- Facts, inferences, accountable decisions, and recommended work remain distinguishable.
- Existing historical and draft artifacts remain preserved unless separately governed.

## Risks and assumptions

- **Fact:** public `0.5.0a1` enabled the standard-root conversion, final `0.5.0` was published, and the normal publisher and CI were restored.
- **Fact:** the emergency publications bypassed normal lifecycle authorization while retaining bounded technical supply-chain controls.
- **Risk:** readers may interpret the successful recovery as permission to bypass normal controls in future routine releases.
- **Risk:** mutable external URLs or incomplete chronology could weaken later auditability.
- **Assumption:** public GitHub and PyPI release observations remain available; immutable commits and distribution digests provide the durable identity.
- **Open decision:** each preventive action requires its own later prioritization and governing scope; this packet does not approve those implementations.

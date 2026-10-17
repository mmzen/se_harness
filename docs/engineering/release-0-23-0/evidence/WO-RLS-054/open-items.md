# Open release items — evaluator 0.23.0 / plugin 0.2.7

mmzen instructed: "continue the release, mark the findings as open items".
The released evaluator recorded that direction in DEC-RLS-010 and DEC-RLS-011.
These are release-only dispositions. **The follow-up items below remain open.**
Risk acceptance for this release does not mean that a defect is repaired or
that an unrun test passed. Final human verification and release remain separate.

## Items to carry forward

| Item | Observation and impact | Release disposition | Owner and follow-up |
| --- | --- | --- | --- |
| R23-NATIVE-010 — open | Codex's read-only trial explained before reading communication policy (events 11 and 31). Explanations can precede required guidance. All seven reads still matched independent HTTP results; version stayed 29. | DEC-RLS-010 / RISK-RLS-008; retain the failure. | mmzen: prepare a bounded instruction correction and rerun the affected case before the next plugin release or any claim it passes. |
| R23-NATIVE-011 — open | Two proposed work orders omitted generated VREC destinations while claiming none were unresolved. This can require a later scope correction. They remain unapproved drafts. | DEC-RLS-010 / RISK-RLS-008; no claim of proposal completeness. | mmzen: correct the discovery of generated paths and qualify new-work drafting. Existing scope checks continue to stop unapproved writes. Same revisit trigger. |
| Codex Windows desktop — open | Startup, selection, delivery, compaction and resume were not run. Desktop-specific selection/delivery defects may remain. | DEC-RLS-011 / RISK-RLS-009; **deferred / unverified**, never covered by CLI results. | mmzen: complete desktop qualification before the next plugin release or a verified-desktop claim. Keep the prepared kit and exact package identities. |
| Duration/context goals — open improvement | Claude focused median 165.552 s; only two of three runs met duration and none met context. Codex took 203.414 s with context unavailable. Full workflows took 1,341.105 s / 1,503.510 s. | Existing observations; no performance success or new gate inferred. | mmzen: prioritize a separate measured improvement after this release. Broad performance changes remain outside this release work. |

## Evidence and limits

The [original qualification report](../WO-RLS-045/qualification-progress-bb089004.md)
and [evidence index](evidence-index-bb089004.json) remain unchanged. Source/package
candidate is `bb0890045f462343ecae66ca30b20b06cf6e8ae6`. All actual failures, retries and skipped cases remain retained.
The separate seeded execution cases reached ready records; they do not repair
the two draft proposals. The full native workflows read communication early;
they do not erase the independent read-only failure.

The source, packages, actual CLI workflows, focused positive and negative cases,
graph readbacks, service boundaries and restart/restore have retained assessments.
Their conclusions remain limited to their exact inputs. The marketplace child is
prepared locally in [the staging receipt](../WO-RLS-046/marketplace-review-commit-bb089004.json);
it is not publicly promoted. Final-candidate capture must establish its own
committed identity and show exactly which evidence can be reused.

DEC-RLS-010/011 do not change accepted specification text or grant out-of-scope
implementation. They cover only these disclosed limitations in this release.
Changed versions, product scope or bytes require review. Required gates,
commit-bound assurance, public-route checks and provider controls remain.
RISK-HAG-001/002 remain raised under their existing private-sandbox boundaries.

## Current continuation

Continue the required handoff and final-candidate assurance preparation under
the existing approved work. No final verification, merge, complete-release
decision, public publication, repository adoption or host update has occurred.

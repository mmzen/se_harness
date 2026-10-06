+++
id = "SPEC-HAG-006"
type = "specification"
title = "Assess an adopted evaluator on an older stacked branch"
status = "approved"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
contract = "Keep the original change base while independently proving an identical evaluator adoption already integrated on the default branch; preserve prior handoff evidence when rebinding the active work."
[relations]
specifies = ["REQ-HUP-008", "REQ-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T13:25:58Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to SPEC-HAG-006, VER-HAG-005 and WO-HAG-006, required commit-bound verification, DEC-HAG-003 bounded-manual-revision of the exact VER-HAG-004 proposal, and ordinary draft PR #535 updates in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs. Review binding SHA-256 c9d4d84326b0e26d39519a1eadb91e216e4a6f01700213ec3c76a6854e55a649. This covers local implementation, checks, aggregate ready-record publication and later separately given verification-decision push. No verification acceptance, risk acceptance, retargeting, base-branch update, force push, merge, release or deployment. The exact manual amendment grants no general revision mechanism or gate waiver."
+++

# Assess an adopted evaluator on an older stacked branch

## Problem and scope

The original PR #535 base predates release 0.22.1. The branch now includes
main's reviewed release and adoption, but the predecessor assessor requires
the release record to exist at that older PR base. Its observed refusal is
"trusted base must contain exactly one released distribution for the target
version". Retargeting the PR would change the approved delivery boundary.

This proposed addendum keeps SPEC-HUP-004's event base, immutable identities,
read-only assessment and target qualification. It supplements release-record
discovery only for an adoption already present in trusted default-branch
history. The original base remains the input to change and scope checks.
Older definitions and their history are preserved; this proposal has no effect
until its explicit human approval. No public evaluator or hosted service changes.

## Rules

**HAG-CI-001.** Retain the event-derived base B and target C. Existing direct
adoption checks remain the first route. Same-version checks and their existing
ownership exceptions stay unchanged. Never replace B to hide changed paths.

**HAG-CI-002.** Only when B has no eligible release record for the selected
target version may the assessor attempt reuse of an adoption from the fetched,
configured default-branch ref. Resolve that ref once to a full immutable commit.
Require one unique merge base A between that commit and C. A must be an ancestor
of both, must select the same complete evaluator identity and canonical root
configuration/lock as C, and must contain exactly one valid released distribution
for that version. Require the release record and selected canonical upgrade
transaction in C to equal their complete Git-blob bytes at A. An absent,
malformed, conflicting or ambiguous input refuses; candidate-only records and
unrelated refs cannot supply authority. Do not fall back after malformed or
multiple release records at B. Do not use latest, a version range or a
candidate-supplied extra trust flag.

**HAG-CI-003.** The existing transition selector must still bind the original
B lock to C's evaluator and exactly one retained upgrade transaction. Keep
archive, payload, runtime-origin, clean-checkout and complete target-root
qualification checks. The fallback supplies a proven historical record, not
an exemption. Missing proof fails before invoking the evaluator.

**HAG-CI-004.** Report B, C, the resolved default-branch commit, A, record and
transaction paths and hashes, and whether direct or adopted-history selection
was used. Preserve the output fields used by the existing workflow. Use the
existing standard-library assessor, tests and credential-free workflow. No new
service, dependency, general migration framework or workflow is needed.

**HAG-CI-005.** Before rebinding WO-HAG-001's handoff packet, preserve its exact
current bytes as evidence/WO-HAG-006/WO-HAG-001-handoff-before.txt and record
its source commit, original path and digest. Use released 0.22.1's supported
evidence command to bind the live packet to the revised governing definitions.
Preserve its historical observations and all other original HAG evidence. This
is current evidence maintenance, not new hosted tests or completion authority.
VREC-HAG-001/002 and every byte to which they bind remain unchanged. The exact
linked amendment to VER-HAG-004 must first be authorized through DEC-HAG-003.

## Examples and failures

The PR #535 base stays be1812e7042081014cc7682da8b9cd3822d9071f. Its current
target includes approved main d7eeb2ae785928925669695074be7bdd6ccb1e0a. The
0.22.1 release and adoption bytes from that independent history can supply
proof only if all identity, transaction and ancestry comparisons pass.

A target-only release record, altered transaction, moved or ambiguous trust
input, different target lock, missing history or mismatched wheel must fail.
A different version pair uses the same rules, without a special case for HAG.
No lifecycle state or external action is performed by assessment.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-HUP-008 | HAG-CI-001, HAG-CI-002, HAG-CI-003, HAG-CI-004 |
| REQ-HAG-008 | HAG-CI-001, HAG-CI-004, HAG-CI-005 |

## Design rationale

Keep the existing assessor and transaction checks. The additional history
comparison supports a stacked branch that imports an already completed
adoption. Merely trusting the target's release record would remove independent
authority. Updating the target branch or retargeting is outside the current
approval. Helper names and test-fixture organization remain implementation choices.

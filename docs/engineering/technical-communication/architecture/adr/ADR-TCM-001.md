+++
id = "ADR-TCM-001"
type = "adr"
title = "Use one managed communication policy with non-authoritative skill consumers"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T07:53:59Z"
decided_by = "technical-owner"
+++

# ADR: Use one managed communication policy with non-authoritative skill consumers

## Status

Proposed.

## Context

The desired behavior is cross-cutting: supported agents should use selected
ASD-STE100-based clarity principles in eligible operator interaction and
technical-artifact prose. A portable skill is also required to expose one
explicit operator-brief outcome.

A skill is outcome-oriented and activates for one procedure. It cannot, by
itself, govern ordinary prose from every other skill or runtime. Conversely, a
managed policy can govern cross-cutting writing behavior but does not define a
bounded executable outcome or structured receipt. The architecture must place
one source of rules above skill and runtime consumers without creating another
source of lifecycle authority.

## Decision drivers

- One discoverable and integrity-protected communication-policy owner.
- Provider-neutral behavior for ordinary agent routes and portable skills.
- No ASD-STE100 compliance claim, copied standard, dictionary, or runtime download.
- Exact preservation of commands, evidence, canonical results, identifiers, and
  machine-readable content.
- Protection of normative meaning and accountable decision boundaries.
- Explicit, read-only, non-overlapping first-skill activation.
- Compatibility with the established thin gate, managed router, focused policy,
  portable skill, and released-evaluator architecture.
- Safe installation, upgrade, customization conflict, and offline operation.
- Human review at meaning and decision points rather than for every sentence.

## Considered options

### Option A: one managed focused policy with skill and runtime consumers

Add `TECHNICAL_COMMUNICATION.md` as managed focused policy, route it from
`ENGINEERING_HARNESS.md`, and make `harness-operator-brief` and later authoring
skills reference it. Ordinary supported agent prose follows the same route.

This provides one owner, applies beyond one skill, and keeps skills outcome
oriented. It adds a managed file, a route, distribution surface, and policy
review responsibility.

### Option B: put the complete policy only in `harness-operator-brief`

This is locally simple and keeps related files together. It applies only when
that skill activates, cannot govern ordinary or artifact-writing prose, and
encourages copied rules in other skills. Skill prose would appear to own a
cross-cutting product constraint even though the existing architecture makes it
non-authoritative.

### Option C: put the complete policy in `ENGINEERING_HARNESS.md`

Every supported agent would discover it early. The managed router would become
larger, policy changes would rewrite the primary gate, and the focused modular
policy architecture would be weakened.

### Option D: materialize policy in provider-specific prompts or adapters

This could tune behavior for each runtime. Correctness and wording would vary by
provider, adapters would become competing policy owners, and ordinary repository
integrity could not prove the effective rule set. It would also make host
activation a prerequisite for provider-neutral behavior.

### Option E: publish non-authoritative guidance only

A note or style guide would be easy to add. It would not be integrity-protected,
directly routed, contract-bound, or suitable for deterministic failure behavior.
The requested product capability would remain optional advice.

## Decision

Select Option A.

Create one focused managed policy at the canonical template path
`templates/repository/standard/docs/engineering/TECHNICAL_COMMUNICATION.md`,
installed as `docs/engineering/TECHNICAL_COMMUNICATION.md`. The managed router
contains one concise direct route. The policy owns permitted claims, scope,
profiles, protection, precedence, deviations, and human decision points.

Add one explicit-only, read-only portable skill named
`harness-operator-brief`. It consumes the policy and one bounded source, checks
protected-content bindings, and returns an inline result and receipt with zero
changed paths. The skill does not own or duplicate the policy and is not an
implicit wrapper around other skills.

Keep the communication layer below machine contracts, formal semantics, and
existing managed governance policy. It can improve eligible prose but cannot
reinterpret them. Use repository-managed policy as the complete runtime source;
do not download, bundle, or parse ASD-STE100.

## Consequences

### Positive

- One managed source governs ordinary eligible agent prose and skill consumers.
- Policy ownership, skill outcome, and runtime execution remain distinct.
- Operator communication and artifact writing can use different strengths.
- Existing skills can reference the policy without duplicated rule bodies.
- Offline and provider-neutral operation remains possible.
- Integrity, installation, upgrade, packaging, and receipt mechanisms remain
  available for evidence.
- Human attention stays at meaning, terminology, and accountable decisions.

### Negative

- The standard installation, managed lock, router, preflight policy set, package
  metadata, and tests gain another managed file.
- The strict skill-contract parser gains another closed instance and must retain
  existing contract behavior exactly.
- Protected-content preservation is deterministic only for declared exact spans;
  semantic equivalence still needs representative human assessment.
- Explicit-only activation means the operator-brief skill does not automatically
  restyle every response in the first increment.
- Maintainers must keep policy examples concise enough for routine agent loading.

### Operational and security

- No network, credential, hosted service, or external standard is required.
- The policy and skill upgrade transactionally; customized collisions block.
- Source bodies are bounded and not retained in receipts.
- The helper validates structure and digests, not truth or hidden reasoning.
- A failed policy, identity, source, or preservation check stops before a
  completed policy-governed result.

### Migration

- New installations receive the managed policy and skill.
- Safe upgrades add them only when normal ownership and conflict checks pass.
- Existing owner content and approved artifacts are not rewritten.
- The self-hosting root managed copy changes only through a later released
  evaluator upgrade, not direct candidate editing.
- Provider-specific host activation may be added by separately approved work and
  cannot change the policy or skill authority boundary.

## Validation

- Verify canonical template, installed path, lock entry, route, preflight policy
  set, package contents, offline installation, upgrade, and customized conflict.
- Verify no normative policy duplication in the router, skills, adapters, or notes.
- Validate the closed v2 skill contract, explicit-only activation, read-only
  effect, single-agent fallback, inline-only outputs, and zero changed paths.
- Prove byte preservation over the exact-content corpus and inspect stable
  diagnostics for malformed or ambiguous cases.
- Independently review representative operator, requirement, specification,
  architecture, work-order, and verification prose for unchanged meaning.
- Confirm no public or installed claim of ASD approval, endorsement,
  certification, or strict ASD-STE100 compliance and no runtime download path.
- Re-run existing skill digest, installation, workflow, integrity, and release
  packaging regressions.

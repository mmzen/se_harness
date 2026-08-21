+++
id = "SPEC-REB-004"
type = "specification"
title = "LF-stable evaluator-evidence checkout policy"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
specifies = ["REQ-REB-009", "REQ-REB-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "technical-owner"
+++

# Specification: LF-stable evaluator-evidence checkout policy

## Scope

This specification defines the versioned Git policy and qualification behavior required to keep canonical evaluator-evidence JSON byte-identical across supported checkouts. It also defines the terminal historical state needed to reject a failed predecessor-bootstrap pair without preserving active authority. Both changes preserve the existing raw-byte evidence digest and predecessor-evaluator bootstrap trust direction.

## Actors and external systems

- Git applies repository-owned attributes during checkout and index normalization.
- Candidate source and the canonical standard template own the same narrow LF rule.
- The bootstrap binder emits canonical LF JSON and an exact SHA-256.
- Candidate and released evaluators independently validate the resulting repository.
- Accountable owners separately decide candidate, verification, and release transitions.

## Inputs

- Candidate and canonical-template `.gitattributes` bytes.
- Canonical evaluator JSON and its bound SHA-256.
- Git versions and checkout configurations used by supported Windows and non-Windows environments.
- Exact candidate, VREC, RLS, release contract, root lock, and evaluator identities.

All Git configuration, attributes, repository files, paths, JSON, and hashes are untrusted.

## Outputs

- One exact attribute rule: `docs/engineering/**/evidence/*.json text eol=lf`.
- Matching candidate-source and canonical-template policy.
- Deterministic fresh-checkout evidence proving LF bytes and digest stability.
- A successor candidate and later separately governed verification/release records.

## State model

```text
C2 committed RLS evidence
  -> Windows CRLF smudge detected
  -> corrective packet approved
  -> LF policy implemented
  -> successor candidate C3 qualified
  -> new VREC and RLS separately prepared and decided
```

No step automatically advances to the next accountable lifecycle state.

## Behavioral rules

1. **Narrow rule.** The candidate repository and canonical standard template contain exactly `docs/engineering/**/evidence/*.json text eol=lf` for governed evidence JSON. The implementation must not impose a repository-wide line-ending rewrite.
2. **Exact-byte contract.** Validator hashing remains SHA-256 over raw evidence bytes. Canonical JSON remains sorted compact UTF-8 with exactly one terminal LF.
3. **Attribute precedence.** Tests prove the repository rule yields LF despite `core.autocrlf=true`, `core.autocrlf=input`, `core.autocrlf=false`, and CRLF-oriented checkout defaults. A conflicting more-specific attribute is rejected by policy tests.
4. **Candidate/template parity.** The rule in candidate source and the packaged canonical standard template is byte-identical. Installation fixtures and wheels contain the canonical policy.
5. **Released-root preservation.** Implementation does not edit `.engineering-harness.toml`, `.engineering-harness.lock`, or released-0.5 managed files. The released evaluator remains external and unchanged.
6. **No evidence rewrite.** Historical `RLS-SEH-009` and `RLS-SEH-009-evaluator.json` remain byte-for-byte retained. Qualification uses them to reproduce the failing CRLF checkout and prove the successor policy.
7. **Fresh-checkout proof.** Verification creates clean local clones from the successor candidate/governance history under each Git configuration, checks `git check-attr`, hashes the checked-out evidence, and runs both evaluator planes.
8. **Content-drift rejection.** Any JSON content change, missing terminal LF in the Git blob, changed digest, unsafe path, symlink, duplicate key, noncanonical form, or policy mismatch still fails closed.
9. **No local-policy dependency.** `.git/info/attributes`, global attributes, and local `core.autocrlf=false` are diagnostic controls only and cannot satisfy the requirement.
10. **Candidate invalidation.** Because this changes trusted candidate repository and canonical-template state after `VREC-SEH-009`, C2 is ineligible for promotion. A successor candidate, exact builds, hosted lanes, aggregate VREC, and RLS are required.
11. **Historical disposition compatibility.** A predecessor-bootstrap RLS in `rejected` state qualifies only when its single satisfied contract is also `rejected`, still declares that exact RLS ID/version, and preserves the complete tuple and evidence. That rejected contract is excluded from active approved-bootstrap cardinality.
12. **Active authority separation.** A `ready` predecessor-bootstrap RLS still requires its exact contract to be `approved`. Binder, preparation, release, and publication resolution reject every rejected contract. Mixed ready/rejected pairs and contract reuse fail closed.
13. **Ordered disposition.** `RLS-SEH-009` and `REL-SEH-008` must be rejected in one validated governance transaction before the successor bootstrap contract becomes the sole approved contract.
14. **Closed authority.** Drafting or implementing this policy never verifies a VREC, releases an RLS, commits, pushes, tags, publishes, deploys, changes maintenance state, uses credentials, changes external policy, or upgrades the root evaluator without separate authority.

## Error and recovery behavior

If fresh-checkout hashes differ or either validator fails, retain the exact clone configuration and hashes, leave the candidate unpromoted, and correct through another reviewed candidate. Never alter a historical evidence digest to match platform-smudged bytes.

## Data and interface contracts

The normative rule is:

```gitattributes
docs/engineering/**/evidence/*.json text eol=lf
```

The evidence schema, RLS binding fields, bootstrap contract fields, and raw SHA-256 format remain unchanged. Historical compatibility is the closed pair `rejected RLS -> rejected exact contract`; it is never an input accepted by preparation, binding, release, or publication operations.

## Security and privacy properties

- Expected evidence identity continues to come from the bound record, not the checkout configuration.
- Attribute resolution is inspected from the clean target tree.
- Tests isolate global/system attributes and record only bounded configuration facts.
- No usernames, home paths, tokens, or environment dumps enter retained evidence.

## Performance and capacity

The rule affects only governed evidence JSON. Checkout-matrix qualification remains bounded to small local clones and existing validator timeouts.

## Observability

Evidence records Git version, selected configuration, `git check-attr` result, worktree SHA-256, expected SHA-256, validator result, and whether any target or external write occurred.

## Compatibility and migration

- Existing Git blobs and historical released records are unchanged. Rejected predecessor-bootstrap pairs remain valid terminal history without active authority.
- New/future installations receive the LF policy from the standard template.
- The operational repository remains governed by released 0.5.0 until separately upgraded after publication.
- Version remains `0.6.0` because no public release or immutable tag exists.

## Examples and counterexamples

- **Conforming:** `core.autocrlf=true` checkout reports `text: set`, `eol: lf`, and evidence SHA-256 equals the bound value.
- **Non-conforming:** require operators to set `core.autocrlf=false` manually.
- **Non-conforming:** hash normalized text while claiming raw-byte identity.
- **Non-conforming:** amend or overwrite `RLS-SEH-009` evidence.

## Explicitly unspecified decisions

Test-helper names, temporary clone locations, and output formatting are delegated provided paths are bounded and retained evidence is deterministic.

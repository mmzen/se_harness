+++
id = "VER-REB-007"
type = "verification"
title = "Predecessor-to-successor migration assurance"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
verifies = ["REQ-REB-016", "REQ-REB-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "quality-owner"
+++

# Verification Contract: Predecessor-to-successor migration assurance

## Independence

Verification parses the packaged contract independently, recomputes every source/package/fixture/adapter/view/report digest, resolves predecessor and successor origins separately from the runner, and compares raw before/after state rather than trusting runner success flags. Assurance selects negative cases and independently maps technical actors, accountable decision fixtures, allowed effects, and stages to the governing requirements.

The implementation actor may build fixtures and produce reports, but cannot define accepted diagnostics, omit required stages, decide which mutations are harmless, or treat a passing candidate result as predecessor or human authority.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-016` | Contract schema and package conformance | Source and wheel contract; exact stage/role/identity/effect catalogs; unknown, missing, duplicate, and reordered fields | Only canonical complete contracts pass; built package bytes and source bytes agree |
| `REQ-REB-016` | Compatibility classification | Compatible pair; schema, lifecycle, evidence, preparation, validation, rendering, and adoption deltas; unknown capability | Every incompatible or unknown case is `migration-required` with exact affected operations |
| `REQ-REB-016` | Authority boundary analysis | Candidate-as-root, shared interpreter, candidate-supplied predecessor identity, missing decision fixture, combined release/adoption | Every substitution or inferred decision fails before the affected stage and changes no non-disposable state |
| `REQ-REB-017` | Complete positive rehearsal | Exact historical 0.5.0-to-0.6.0-style scenario and one synthetic future N-1-to-N scenario | All nine stages execute in order; complete/compatible claims remain distinct; adoption occurs only at the final disposable stage |
| `REQ-REB-017` | Rejection and corrected succession | Rejected proposal, tampered rejected tuple, reopened record, same-version corrected successor, rejected authority reuse | Exact rejected history remains immutable/non-authoritative; only a distinct valid successor becomes active in the fixture |
| `REQ-REB-017` | Stage failure matrix | Failure before, during, and after each stage; timeout, malformed report, cleanup failure, unexpected mutation | First failure is retained; every later stage is not run; operational source, refs, evaluator selection, credentials, and external state remain unchanged |
| `REQ-REB-017` | Cross-platform hosted replay | Windows and Linux, exact predecessor wheel digest, non-promotable candidate wheel | Semantic result and normalized digest agree; platform-specific paths and environments remain isolated |

## Acceptance scenarios

1. Validate a canonical scenario with exact predecessor and successor identities; independently reproduce its contract and input digest.
2. Run predecessor preparation, then prove candidate complete validation is read-only and does not change evaluator selection.
3. Replay an attributed rejection, preserve its exact bytes, create a distinct corrected same-version proposal, and prove rejected history grants no active authority.
4. Run assessment with a declared exact compatibility view while independently retaining the predecessor full-checkout refusal and successor complete-graph success.
5. Resolve release/publication inputs and render the selected snapshot without Git ref, network, credential, lifecycle, package, release, maintenance, or deployment mutation.
6. Inject a simulated immutable publication fact and separately attributed upgrade fixture; prove the ordinary disposable upgrade changes evaluator selection only at `adopt`, supports rollback, and replays as a no-op.
7. Repeat the same semantic scenario on Windows and Linux and reconcile normalized results.

## Property and invariant tests

- The stage ID set and order are exact; removing, duplicating, or permuting a stage always fails.
- Changing any contract, scenario, evaluator, fixture, adapter, view, or report byte changes its bound digest or fails canonical parsing.
- Before `adopt`, the selected evaluator is always the predecessor; after a successful `adopt`, it is exactly the declared successor.
- Candidate stages have an empty operational mutation set.
- A rejected tuple never becomes active, mutable, reusable, or version-reserving in the fixture.
- After the first failure, the count of executed later stages is zero.
- Repeating identical inputs yields the same normalized semantic result and digest.
- Output contains no absolute host path, username, credential value/name beyond a bounded refusal catalog, or repository body content.

## Static and architecture checks

- Trace every stage driver to one typed role and one target-view contract; reject raw executable/validator selection by untyped path inside the runner.
- Trace the authority oracle around every stage and every mutation-capable adapter.
- Confirm predecessor and successor child environments cannot import the checkout or one another.
- Confirm the packaged contract is included in source and wheel package data and is schema-validated before use.
- Confirm candidate workflows invoke the no-credential rehearsal before release-bearing qualification and do not add publication permissions.
- Confirm `REQ-REB-016` and `REQ-REB-017` are covered by `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007`, and `WO-REB-018` only within the approved scope.

## Security and privacy checks

Exercise path traversal, symlink/junction, alternate Git directory/worktree state, interpreter replacement, editable install, current-directory import, user-site and `PYTHONPATH` contamination, package/digest substitution, decision-fixture forgery, view escape, output collision, TOCTOU, oversized/malformed output, timeout, credential-bearing environment, and cleanup failure. Every case fails without non-disposable mutation or secret retention.

## Performance and resilience checks

Run contract/unit tests in the normal suite. Run hermetic full rehearsal twice per supported platform within the candidate CI budget. Bound every subprocess time and output. Inject interruptions at every disposable write and prove exact rollback or an explicit contained cleanup failure.

## Manual assessments

- Product/requirements owners confirm that the full stage catalog answers issue #101 without granting automation decision rights.
- Technical/security owners accept the dual-runtime isolation, typed adapter, authority-oracle, and adoption boundaries.
- Assurance owner independently reviews identities, negative cases, normalized cross-platform results, and non-mutation maps.
- Release owner confirms release/publication/adoption remain separate decisions and no rehearsal result can initiate them.

## Evidence retention

Retain under the `WO-REB-018` key: approved preflight manifest; exact changed paths; contract/scenario bytes and digests; predecessor/successor distribution, payload, commit/tree, origin, and isolation identities; per-stage commands and reports; decision fixture digests; view and adapter identities; before/after source, Git, root, lifecycle, credential, and simulated external-state maps; Windows/Linux results; focused/full/package/graph checks; candidate commit; hosted run identities; and every lifecycle or external action not performed.

## Residual uncertainty

The rehearsal proves declared technical behavior, not the wisdom or authenticity of a future human decision. Hosting, package-index, and CI outages remain external. A future migration with new semantic stages requires a new contract version and accountable review rather than a silent scenario extension.

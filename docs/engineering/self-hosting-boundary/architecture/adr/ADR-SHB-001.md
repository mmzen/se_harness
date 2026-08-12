+++
id = "ADR-SHB-001"
type = "adr"
title = "Separate the released governor from candidate execution"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-SHB-001"]
+++

# ADR: Separate the released governor from candidate execution

## Status

Accepted on 2026-08-12 by the accountable owner through the instruction `go for implementation`.

## Context

Continuous self-upgrade makes the unreleased candidate both the product under development and the active operational harness. A nominal released-baseline lane cannot safely run same-version integrity checks against candidate-managed files, and Python imports from the checkout can silently replace the installed baseline. The model needs independent assurance without abandoning useful candidate dogfooding.

## Decision drivers

- Prevent the candidate from being its own sole governor.
- Preserve exact-hash released bootstrap assurance.
- Exercise candidate source and packaged behavior thoroughly.
- Make runtime identity and import origin observable.
- Avoid consumer installation profiles.
- Preserve historical commit-bound records.
- Support a practical one-time migration and repeatable future release cycle.

## Considered options

1. **Continue upgrading the host to the candidate and adjust the failing `doctor` step.** Smallest patch, but host and candidate identities remain mixed and import shadowing remains structurally possible.
2. **Use only the released governor until publication and avoid all candidate harness execution.** Strong independence, but loses candidate semantic validation, template testing, and packaged acceptance.
3. **Use three isolated planes with deferred governor promotion.** The released governor owns an external same-version target, the checkout is candidate source, the candidate wheel is accepted in disposable targets, and publication precedes a separate descriptor/pin update.
4. **Maintain two consumer installation profiles.** Makes roles visible but exports a self-development concern into the public product and violates the one-standard-installation constraint.

## Decision

Choose option 3. Treat governor, candidate source, and candidate package as distinct runtime identities with explicit path and version attestations. Keep governor runtime and its same-version managed target outside the candidate checkout. Treat the checkout as candidate source, with a narrowly separate repository-specific descriptor and three-plane workflow. Test candidate distribution parity through the candidate checkout and candidate-created disposable targets. Promote a published candidate to governor only through a separate governed descriptor/pin update.

The one-time implementation may change the current self-hosting workflow to escape the mixed model, but it must retain before/after evidence and cannot describe the old failing lane as independent success.

## Consequences

- The repository-specific root configuration and self-hosting workflow intentionally differ from the standard consumer templates; every other managed candidate file retains distribution parity.
- CI gains explicit environments, identity checks, and a candidate-package lane.
- Current-directory import shadowing becomes a tested failure rather than an assumption.
- Candidate dogfooding continues in sandboxes but no longer controls the governor.
- A release is followed by a small governor descriptor/pin PR before the next development cycle.
- Failed `VREC-SEH-003` and `RLS-SEH-003` remain audit history on closed PR #28 and are excluded from the clean recovery candidate; new aggregate IDs must authorize the changed candidate.
- Initial migration is more involved than deleting one `doctor` invocation, but future cycles become simpler and auditable.

## Validation

Execute `VER-SHB-001`, including role/path substitution, cross-version integrity misuse, checkout-write detection, true installed-baseline imports, candidate source and package acceptance, exact-candidate requalification, and published-artifact governor promotion fixtures.

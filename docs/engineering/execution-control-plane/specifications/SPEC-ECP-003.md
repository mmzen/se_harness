+++
id = "SPEC-ECP-003"
type = "specification"
title = "The mandatory scope-aware pull-request gate and digest coverage"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
specifies = ["REQ-ECP-006", "REQ-ECP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Specification: The mandatory scope-aware pull-request gate and digest coverage

## Scope

This specification makes the managed pull-request check evaluate execution
scope over the pull request's own Git difference on every pull-request event,
and widens the restitution digest preimage to the change set and gate
statuses. Today the template workflow runs the handoff check only when a
`Harness-Restitution:` line is declared
(`templates/repository/standard/.github/workflows/engineering-harness.yml:56-89`),
and `result_sha256` is computed over the rendered restitution block alone
(`se_harness/workflow_result.py:174-207`), so identical digests cover
different change sets (`docs/notes/agentic-execution-review-2026-08.md`,
section 5, weakness 2). No lifecycle state or decision right changes.

## Actors and external systems

- GitHub Actions runs the managed workflow on `pull_request` events.
- Git supplies `base.sha` and the head checkout.
- The released evaluator installed in the runner evaluates the check.
- Repository administrators mark the check required through branch
  protection; the harness cannot set that itself.

## Terms

- **Managed workflow:** `.github/workflows/engineering-harness.yml` as
  installed from the standard template.
- **Pull-request difference:** the union of `git diff --name-only
  BASE-SHA HEAD` and nothing else; a CI checkout has no untracked files.
- **Canonical block bytes:** as `SPEC-ADS-001` defines, extended by
  `ECP-DIG-001`.
- **Gate predicate status:** the `status` of each entry in
  `compliance.gates[*].predicates[*]`.

## Behavioral rules

### The pull-request gate

**ECP-GTE-001:** On every `pull_request` event, the managed workflow runs
`check . --artifact WO --checkpoint handoff --from-git BASE-SHA --json`
after fetching `BASE-SHA`, unconditionally of any `Harness-Restitution:`
line.

**ECP-GTE-002:** The step fails when the result's `operation.outcome` is not
`completed`, or when any `QGP-G4I-PATHS` predicate status is not `pass`, and
its log names the first path outside scope with `WEX201`.

**ECP-GTE-003:** The work order is the one selected by
`select-work-order --event`, and a body with no standalone
`Harness-Work-Order:` line fails the step; the step never infers a work
order from branch names or commits.

**ECP-GTE-004:** When a `Harness-Restitution:` line is present, the step
additionally compares it to the recomputed `result_sha256` as `ADS-DIG-003`
requires; absence of the line is not a failure, and presence never relaxes
`ECP-GTE-002`.

**ECP-GTE-005:** The step runs the released evaluator from the lock through
`python -I -m se_harness`, never the checkout's `se_harness` package.

**ECP-GTE-006:** The workflow is a managed file; `doctor` reports a consumer
whose installed workflow lacks the unconditional step as `update` required,
and `upgrade --apply` replaces it.

**ECP-GTE-007:** The template's `PULL_REQUEST_TEMPLATE.md.seed` states that
the required check fails on any out-of-scope path, replacing the sentence
"reviewers remain accountable for confirming that the diff stays within its
scope".

### Digest coverage

**ECP-DIG-001:** The canonical block gains, after `Command or response` and
before `Alternatives`, the sections `Change set` (each `scope.changed_paths`
member on its own line, in the schema's sort order, then the line
`complete: true|false` from `scope.change_set_complete`) and `Gates` (one
line `PREDICATE-ID: STATUS` per predicate in `QG-009` order).

**ECP-DIG-002:** `result_sha256` remains the lowercase SHA-256 of the
canonical block bytes (`ADS-DIG-001`); the schema identifier is unchanged.

**ECP-DIG-003:** Two results that differ only in one changed path, in
`change_set_complete`, or in one predicate status have different
`result_sha256` values; a conformance test asserts all three.

**ECP-DIG-004:** The human rendering of `check`, `next`, and `focus` prints
the two new sections, so the block an agent returns and the block CI
recomputes are the same bytes.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-006 | ECP-GTE-001 to ECP-GTE-007 |
| REQ-ECP-007 | ECP-DIG-001 to ECP-DIG-004 |

## Inputs and outputs

Inputs: the pull-request event payload, `base.sha`, and the checkout.
Outputs: the required check conclusion, `restitution.json` in
`$RUNNER_TEMP`, and the two canonical-block sections. The workflow step is
the only new CI job step; the job count does not grow.

## Failure behaviour

Every rule fails closed: an unresolvable base, a missing evaluator, a
missing trailer, an out-of-scope path, or a non-`completed` outcome fails
the required check with a message naming the cause. The gate never writes to
the repository or changes lifecycle state.

## Compatibility and migration

The block gains two sections, so every `result_sha256` value changes at the
upgrade; digests retained in merged pull-request bodies are history and are
not recomputed. `Harness-Restitution:` lines produced before the upgrade
mismatch on a re-run of an open pull request; the fix is one `pr-body`
regeneration. The `--changed-path` loop in the installed workflow is
replaced by `--from-git`, which `WO-ECP-001` must ship first.

## Explicitly unspecified decisions

- Whether the step uses `fetch-depth: 0` or a targeted fetch, provided
  `BASE-SHA` resolves.
- The exact log wording beyond the required identifiers.
- Whether the digest sections render predicate messages; statuses are
  required, messages are not.

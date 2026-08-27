+++
id = "SPEC-ECP-004"
type = "specification"
title = "Authenticated decision records"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-ECP-008"]
+++

# Specification: Authenticated decision records

## Scope

This specification replaces the free-text `--decision <ID>=<actor>` channel
of `transition` with structured decision records whose signer is verified
against a configured identity source and whose role is checked against the
decision right. Today the actor is validated for length and control
characters only (`se_harness/workflow.py:606`), and no Git-author,
`GITHUB_ACTOR`, `CODEOWNERS`, or signature check exists in `se_harness/` or
`scripts/` (`docs/notes/agentic-execution-review-2026-08.md`, section 3,
"Human control"). Decision rights, roles, and the lifecycle registry are
unchanged.

## Actors and external systems

- An accountable owner produces a decision record and signs it.
- The released evaluator verifies the record in `transition --apply`.
- Git supplies commit signatures and `git verify-commit` results.
- GitHub Actions supplies `GITHUB_ACTOR` in CI mode.
- `.engineering-harness.toml` carries the identity configuration.

## Terms

- **Decision record:** a JSON file with exactly the members `schema`,
  `artifact`, `target_state`, `role`, `decision_right`, `reason`, `signer`,
  and `signed_at`, where `signer` is `{"kind": ..., "identity": ...}`.
- **Identity source:** the `[decision_identity]` table of
  `.engineering-harness.toml`, `source = "git-signature" |
  "github-actor" | "configured-identity"`.
- **Role map:** `[decision_identity.roles]`, a table from role name to an
  array of identity strings, in the shape of a `CODEOWNERS` file.
- **Decision right:** one of the `DR-*` identifiers of
  `docs/engineering/DECISION_RIGHTS.md`.

## Behavioral rules

### Decision records

**ECP-DEC-001:** `transition --apply` accepts decisions only through
`--decision-record <file>`, one per transitioned artifact; `--decision
<ID>=<actor>` is refused on `--apply` with `WEX-ECP-020` after the
one-release window of the compatibility section.

**ECP-DEC-002:** A decision record is valid only when `schema` equals
`se-harness-decision-record-v1`, every member is present, `artifact` equals
an artifact in `--set`, `target_state` equals that artifact's requested
state, `signed_at` is RFC 3339 UTC, and `reason` is at most 2000 characters;
otherwise the transition is refused with `WEX-ECP-021` naming the member.

**ECP-DEC-003:** `decision_right` must be the right that `WORKFLOW.json`
binds to the edge being applied (for example `DR-WO-COMPLETE` for
`in_progress -> implemented` on a work order), and `role` must be a role
that `DECISION_RIGHTS.md` lists as holding that right; either mismatch is
`WEX-ECP-022`.

**ECP-DEC-004:** The signer is verified against the configured source:
`git-signature` requires `git verify-commit HEAD` to succeed and the
committer identity to equal `signer.identity`; `github-actor` requires the
environment variable `GITHUB_ACTOR` to equal `signer.identity`;
`configured-identity` requires `signer.identity` to be a member of
`[decision_identity.identities]`; every other outcome is `WEX-ECP-023`.

**ECP-DEC-005:** `signer.kind` must equal the configured `source`; a record
signed under a different kind is refused with `WEX-ECP-023`, so a
`configured-identity` record cannot satisfy a repository configured for
signatures.

**ECP-DEC-006:** `signer.identity` must appear in the role map entry for
`role`; an identity absent from the entry, or a role absent from the map, is
`WEX-ECP-024`.

**ECP-DEC-007:** A repository with no `[decision_identity]` table refuses
every `transition --apply` with `WEX-ECP-025` naming the table; there is no
default source and no honour-based fallback.

**ECP-DEC-008:** The applied `[[lifecycle_events]]` row carries
`decided_by = <role>`, and a new member `decision_record_sha256` equal to the
SHA-256 of the record's canonical JSON bytes; the record is copied into
`<domain>/evidence/<artifact>/decisions/<sha256-prefix-12>.json` in the same
journaled apply.

**ECP-DEC-009:** `transition` without `--apply` evaluates every record and
reports each refusal code without writing, so a planning run reveals an
identity problem before the owner signs.

**ECP-DEC-010:** The delegated-actor route of `SPEC-ECP-006` produces a
record with `signer.kind = "github-actor"` and `role = "delegated-executor"`;
it is verified by the same rules and is accepted only for the rights
`ECP-DLG-002` names.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-008 | ECP-DEC-001 to ECP-DEC-010 |

## Inputs and outputs

Inputs: `--decision-record <file>` (repeatable), the configured identity
source, Git signature state, `GITHUB_ACTOR`. Outputs: the schema-2
transition result with `mutation.writes` listing the artifact and the
retained record; refusals as `blocked`. Example record:

```json
{
  "schema": "se-harness-decision-record-v1",
  "artifact": "WO-ECP-001",
  "target_state": "implemented",
  "role": "engineering-owner",
  "decision_right": "DR-WO-COMPLETE",
  "reason": "Handoff check completed at chain snapshot 3f1c…e9a0.",
  "signer": {"kind": "git-signature", "identity": "owner@example.org"},
  "signed_at": "2026-08-27T15:10:00Z"
}
```

Example configuration:

```toml
[decision_identity]
source = "git-signature"

[decision_identity.roles]
engineering-owner = ["owner@example.org"]
assurance-owner = ["assurance@example.org"]
```

## Failure behaviour

Every refusal (`WEX-ECP-020` to `WEX-ECP-025`) is `blocked`, exit status 1,
with no write. A record that verifies for one artifact and fails for another
in the same `--set` refuses the whole plan; `TransitionPlan` remains
all-or-nothing (`se_harness/workflow.py:69`).

## Compatibility and migration

For one release `--decision <ID>=<actor>` on `--apply` is accepted with
warning `W-ECP-003` only when no `[decision_identity]` table exists; with the
table present, `ECP-DEC-001` applies immediately. The template
`.engineering-harness.toml.tpl` gains the table with `source =
"configured-identity"` and an empty role map, which a consumer must fill
before its first `--apply`. `DECISION_RIGHTS.md` and `WORKFLOW.md` in the
template describe the record; installed copies regenerate on upgrade. The
`[[lifecycle_events]]` schema gains an optional member; the validator
accepts rows without it.

## Explicitly unspecified decisions

- The canonical JSON serialisation used for the record digest, provided it
  is the one shared `json_bytes` implementation.
- Whether `harnessctl decide` is offered to author a record interactively.
- How a consumer maps GitHub teams onto the role map; the map is data.
- Signature algorithms accepted by `git verify-commit`; Git configuration
  governs.

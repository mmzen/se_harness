+++
id = "SPEC-LRE-002"
type = "specification"
title = "The evaluator-evidence floor"
status = "draft"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-LRE-003"]
+++

# Specification: The evaluator-evidence floor

## Scope

Removes the legacy release-evidence declaration mechanism — the package
module, the validator resolver and frozen set, the `W024` debt warnings and
the pre-apply upgrade refusal — and replaces its acceptance logic with one
rule: a released record carrying neither evidence field is not assessed.
Changes nothing about the binding checks a bound record receives.

## Terms

- **Unbound record:** a release record whose `evaluator_evidence_path` and
  `evaluator_evidence_sha256` are both absent.
- **Floor:** the owner's decision of 2026-08-30 that unbound released
  records are not assessed against the evaluator-evidence binding.

## Behavioral rules

**LRE-FLR-001:** The installed validator requires the evaluator-evidence
binding only for a released record carrying at least one of the two
evidence fields. An unbound released record produces no diagnostic of any
class on any plane.

**LRE-FLR-002:** A record carrying exactly one field keeps its existing
partial-binding error. A record carrying both keeps every existing binding
check, including current-lock matching for `ready` records and
archive-identity checks. Nothing outside the both-absent case changes.

**LRE-FLR-003:** The validator's `LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE`
set, `resolve_legacy_release_evidence`, `legacy_release_evidence_state`, the
`W024` emission and the declaration-resolution errors are deleted from the
template copy. `W024` is retired and stays reserved, never reused with
another meaning. The hash-locked root copy changes no byte.

**LRE-FLR-004:** `se_harness/legacy_release_evidence.py` is deleted. The
installer performs no legacy-release enumeration, refusal, or declaration
write during an evaluator upgrade, and the upgrade planning path prints no
undeclared-legacy notice. The upgrade evidence JSON simply omits the
declaration key.

**LRE-FLR-005:** The `[evaluator_upgrade]` packet keeps accepting the
optional `legacy_releases_without_evaluator_evidence` key as inert data: a
work order carrying one stays valid and the value has no effect. No other
new key is admitted.

**LRE-FLR-006:** The dashboard publication script exempts an unbound
released record from its evidence view unconditionally, by the same
both-absent rule, with no identifier set.

**LRE-FLR-007:** Tests pin the floor: an unbound released record validates
with zero diagnostics; a partially bound record still fails; an upgrade
over unbound records proceeds without refusal and writes no declaration;
no deleted symbol survives under `se_harness/`, the template scripts or
`.github/scripts/`; the shared vector fixture is gone.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-LRE-003 | LRE-FLR-001 to LRE-FLR-007 |

## Failure behaviour

Nothing new fails. The partial-binding and full-binding failure paths are
byte-for-byte the behavior they are today.

## Compatibility and migration

`REQ-LRE-001`, `REQ-LRE-002`, `SPEC-LRE-001` and `ADR-LRE-001` are amended
by dated amendment records under `WO-LRE-002`: the declaration mechanism
they defined is retired by the floor, and their history stays valid as the
record of why it existed. A consumer repository holding a declaration keeps
validating (LRE-FLR-005); one holding unbound released records simply stops
needing one. This repository's own gate runs the frozen 0.11.0 root
evaluator, whose validator keeps the resolver and its six `W024` warnings
until the next root adoption; the change reaches consumers with the next
release.

## Explicitly unspecified decisions

Test names; whether the retired-code comment sits on the validator or a
registry.

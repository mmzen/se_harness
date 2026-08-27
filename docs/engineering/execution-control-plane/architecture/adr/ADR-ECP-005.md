+++
id = "ADR-ECP-005"
type = "adr"
title = "Evict self-hosting machinery from the shipped product"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
decides = ["ARCH-ECP-001"]
+++

# ADR: Evict self-hosting machinery from the shipped product

## Status

Proposed.

## Context

Between 08-20 and 08-24 this repository had to release itself while
governed by an evaluator that could not parse its own new records. The
bridge built for that is still live in the wheel, in CI, and in the consumer
validator: the `governance-migration-protocol` hash-bound class
(`se_harness/hash_bound_classes.json:19-32`) and its
`gitattributes.fragment` lines make `init`, a commit, then `doctor` exit 1
in every fresh repository (`docs/notes/complexity-audit-2026-08.md`, P0-1);
`qualify predecessor-view` in the wheel imports the unpackaged
`repository_tools` (`se_harness/release_qualification.py:634`); six
`RLS-SEH-*` identifiers are hard-coded in
`se_harness/legacy_release_evidence.py:36` and two other generic files
(P1-2); `validate_governor_transition.py` refuses the upgrade the owner
wants (P0-3); `recovery_rehearsal.py` exercises none of the installer
(P1-9); and three shipped skills stub the evaluator
(`templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`).
`ADR-REB-009` decided five typed `qualify` operations; `SPEC-REB-002` rule
14 requires a disposable rehearsal; `SPEC-LRE-001` rule 11 freezes the six
identifiers as a code constant.

## Decision drivers

- Principle 6: orchestration and self-hosting are host detail, not product.
- A consumer's first `doctor` must pass.
- No product code names this repository's own records.
- Keep every published record and its evidence tracked and hash-bound.
- Skills must do what their `SKILL.md` says or not ship.
- Deletions that touch approved artifacts are amendments, not silent edits.

## Considered options

### Option A: keep the bridge behind a feature flag

Gate the class, the `predecessor-view` role, and the rehearsal behind
`[harness] self_hosting = true`, default off. Consequences: consumer
`doctor` passes; but the code, its four ARCH and four SPEC artifacts, the
CI lanes, and the 19% of the validator devoted to it remain in the wheel
and in every reader's path; the flag is one more concept; the `RLS-SEH`
constants stay in generic code; the stubbed skills stay shipped.

### Option B: evict to `repository_tools/` and to data

Remove the class and fragment lines; treat "pattern matches nothing" as a
warning for template-region classes; move `candidate-package`,
`public-install`, and `predecessor-view` self-checks and
`candidate_acceptance.py` to `repository_tools/`; replace the six
identifiers with a rule-5 declaration on an approved upgrade work order;
delete `validate_governor_transition.py`, the migration stage machine, the
recovery rehearsal, `accept-candidate`, and lock schema-1 writes; run the
real `upgrade --apply` as the rehearsal; exclude skills with stub clients
from the template. Consequences: about 6,000 lines leave the product; a
fresh consumer passes `doctor`; history is preserved through data;
`ADR-REB-009`, `SPEC-REB-002` rule 14, and `SPEC-LRE-001` rule 11 require
amendment records.

### Option C: delete the bridge and the history together

Also drop the predecessor-view validator rules and the `RLS-SEH-014` and
`RLS-SEH-015` evidence. Consequences: simplest code; orphans two published
release records whose evidence is hash-bound, which the repository's own
rules forbid.

## Decision

Select Option B (`SPEC-ECP-007`, `ECP-PRD-*` and `ECP-SKL-*`). Once
accepted, this ADR supersedes the five-operation `qualify` decision of
`ADR-REB-009` with a two-operation consumer namespace plus repository
tools, amends `SPEC-REB-002` rule 14 so the disposable rehearsal is a real
installer run, and amends `SPEC-LRE-001` rule 11 so the compatibility set is
declared through rule 5 rather than frozen in code. `WO-ECP-007` writes the
amendment records on `ADR-REB-009`, `SPEC-REB-002`, and `SPEC-LRE-001`.

## Consequences

- Positive: a green `init` is followed by a green `doctor`; the wheel
  carries no `RLS-SEH` string; the validator's predecessor-view rules run
  only where a `[bootstrap]` tuple exists; the template ships one honest
  skill.
- Negative: re-validation of `RLS-SEH-012` by the 0.5.0 evaluator is no
  longer runnable from the wheel; it remains recorded evidence.
- Operational: consumers see `update` and `remove` entries on upgrade; this
  repository's CI loses the predecessor-evaluator lane and gains a
  `git diff --quiet` lock-drift step; `scripts/` needs a header saying which
  files are pinned payload.
- Security: the removed rehearsal ran a private transaction with fake
  digests; the replacement exercises `installer.apply_changes` itself.
- Migration: `WO-ECP-007` performs the eviction and writes the three
  amendment records; `WO-ECP-008` removes the stubbed skills; the six
  historical exemptions are re-declared under rule 5 before the constant is
  deleted, so no published record loses its exemption at any commit.

## Validation

`ECP-PRD-003` fresh-consumer `doctor` test on Linux and Windows against the
built wheel; `ECP-PRD-004` grep over the wheel; `ECP-PRD-007` import test
without `repository_tools`; `ECP-SKL-003` template grep; a test that
`W024` is still produced for each of the six records with a rule-5
declarer; presence tests for the three amendment records.

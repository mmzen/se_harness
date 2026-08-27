+++
id = "SPEC-ECP-007"
type = "specification"
title = "The consumer product boundary"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-ECP-012", "REQ-ECP-013", "REQ-ECP-014"]
+++

# Specification: The consumer product boundary

## Scope

This specification draws the line between what ships to a consumer
repository and what serves only this repository's self-hosting. Today
`hash_bound_classes.json` declares the `governance-migration-protocol` class
whose patterns match files that exist only here
(`se_harness/hash_bound_classes.json:19-32`;
`templates/repository/standard/gitattributes.fragment:4-6`), the checker
fails any class whose pattern matches no tracked path
(`se_harness/hash_bound.py:454-457`, `:485-499`), so `init`, a commit, then
`doctor` exits 1 in every fresh repository
(`docs/notes/complexity-audit-2026-08.md`, P0-1). Six `RLS-SEH-*`
identifiers are hard-coded in `se_harness/legacy_release_evidence.py:36`,
the template validator, and the dashboard publisher (audit P1-2), and three
shipped skill scripts inject a stub client and print
`"evaluator_invoked": false`
(`templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py:190-199`).

## Actors and external systems

- A consumer repository owner runs `init`, `doctor`, and `upgrade`.
- This repository's release tooling under `repository_tools/` runs the
  self-checks that leave the product.
- The released evaluator runs `doctor`.
- The template validator runs in consumers and here.

## Terms

- **Product surface:** the wheel's `se_harness` package, its package data,
  and the standard template tree.
- **Repository region:** a hash-bound class whose `region` is
  `repository`; **template region** is `template`.
- **Self-check:** a `qualify` operation that asserts a property of the
  `se-harness` distribution by name (`candidate-package`, `public-install`,
  `predecessor-view`).
- **Rule-5 declaration:** the `[legacy_release_evidence]` declaration
  mechanism of `SPEC-LRE-001` rule 5.
- **Stub client:** a skill script that substitutes a lambda for the
  evaluator invocation and reports `evaluator_invoked = false`.

## Behavioral rules

### Product boundary

**ECP-PRD-001:** `hash_bound_classes.json` declares no class whose pattern
names a path that the standard template does not install; the
`governance-migration-protocol` class and the three corresponding
`gitattributes.fragment` lines are removed, and this repository pins its
own LF bytes in `.gitattributes` outside the managed block.

**ECP-PRD-002:** For a template-region class, a pattern that matches no
tracked path is warning `W-ECP-006`, not a failure; for a repository-region
class it remains a failure, because such a class is declared by the
consumer.

**ECP-PRD-003:** `init` on an empty directory, followed by `git init`,
`git add -A`, one commit, and `doctor`, exits 0 with zero `FAIL` lines on
Linux and Windows; a test in the package suite performs exactly this
sequence against the packaged template.

**ECP-PRD-004:** No file under `se_harness/`, `templates/`, or an installed
script matches the regular expression `RLS-SEH-\d{3}`; a test asserts it
over the built wheel's contents.

**ECP-PRD-005:** The six identifiers of `SPEC-LRE-001` rule 11 are declared
through rule 5 by an approved upgrade work order of this repository;
`legacy_release_evidence.py` resolves exemptions only from declarations,
and the `self-hosting-compatibility-set` declarer rendering is removed.

**ECP-PRD-006:** `qualify` exposes exactly `released-root` and
`complete-candidate`; `candidate-package`, `public-install`, and
`predecessor-view` move to `repository_tools/` and are invoked only by this
repository's workflows, and `check_portable_release_surface.py` no longer
pins `predecessor-view` in `--help`.

**ECP-PRD-007:** The wheel imports nothing from `repository_tools`; a test
imports every module under `se_harness/` in an environment where
`repository_tools` is absent from `sys.path`.

**ECP-PRD-008:** `recovery-rehearsal`, `accept-candidate`, the
governance-migration stage machine, and lock schema-1 write paths leave the
product; the migration rehearsal lane runs the real `upgrade --apply`
against a throwaway copy holding the predecessor lock.

**ECP-PRD-009:** The template validator's predecessor-view rules run only
when a `[bootstrap]` tuple is present in a release record, so a consumer
tree with no such record never executes them, while `RLS-SEH-014` and
`RLS-SEH-015` continue to validate here.

### Shipped skills

**ECP-SKL-001:** Every skill under `templates/repository/standard/.agents/`
whose `SKILL.md` states that it invokes the evaluator has a script that runs
the resolved evaluator as a subprocess and reports its exit status; a skill
that cannot is excluded from the template.

**ECP-SKL-002:** `harness-orient` is retained as a real wrapper;
`harness-execute-work-order`, `harness-prepare-verification`, and
`harness-guard` are removed from the template and from the `.claude`
adapters until they satisfy `ECP-SKL-001`.

**ECP-SKL-003:** No shipped skill script contains the string
`"evaluator_invoked": False` or injects a `client=lambda` substitute; a test
over the template tree asserts it.

**ECP-SKL-004:** `installer.py`'s managed manifest, `hash_bound_classes.json`
patterns for skill scripts, and the `.claude/skills` adapters reference only
retained skills, so `doctor` in an upgraded consumer reports the removed
skill files as `remove` rather than as drift.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-012 | ECP-PRD-001 to ECP-PRD-003, ECP-PRD-008, ECP-PRD-009 |
| REQ-ECP-013 | ECP-PRD-004 to ECP-PRD-007 |
| REQ-ECP-014 | ECP-SKL-001 to ECP-SKL-004 |

## Inputs and outputs

Inputs: the packaged template, `init`, `doctor`, `upgrade`, and the rule-5
declaration on an upgrade work order. Outputs: a `doctor` exit status, the
`W-ECP-006` warning, the reduced `qualify` namespace, and a template with
one skill.

## Failure behaviour

Every retained check fails closed: a repository-region pattern matching
nothing still fails `doctor`; an `RLS-SEH` match in the wheel fails the
test suite; an import of `repository_tools` from the package fails the
isolation test. Nothing here changes lifecycle state.

## Compatibility and migration

Consumers see managed-file `update` and `remove` entries for the fragment
lines, the workflow, and the removed skills on their next `upgrade`. The
six historical records stay exempt through data with the same `W024`
diagnostics. `ADR-REB-009`'s five-operation decision, `SPEC-REB-002` rule 14,
and `SPEC-LRE-001` rule 11 receive amendment records under `WO-ECP-007`.
Removed subcommands have no window: none is invoked by any consumer
template.

## Explicitly unspecified decisions

- Whether `scripts/` is split into managed payload and `tools/` in the same
  work order (audit P2-15) or later.
- The exact `repository_tools` module names for the relocated self-checks.
- Whether a rewritten `harness-execute-work-order` returns to the template
  in a later work order; this specification only sets its admission rule.

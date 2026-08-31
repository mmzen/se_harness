+++
id = "SPEC-ECP-018"
type = "specification"
title = "Removal of the dead .gitattributes tail"
status = "draft"
owners = ["technical-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
specifies = ["REQ-ECP-029"]
+++

# Specification: Removal of the dead .gitattributes tail

## Scope

One owner-region file edit and the delegation-gate configuration this
demonstration work order carries. No product byte, no managed byte, no
test behavior changes.

## Behavioral rules

**ECP-GAT-001:** The comment block beginning "Retained from WO-ECP-010"
and its trailing blank line are deleted from `.gitattributes`; the managed
block between the `se-harness` markers and every live rule keep their
bytes.

**ECP-GAT-002:** The line `se_harness/agent_contract.json text eol=lf` is
deleted; the neighbouring byte rules for `hash_bound_classes.json`,
`build-recipe.json`, `build-toolchain.lock` and the byte-exact tree keep
their bytes.

**ECP-GAT-003:** After the edit, every non-comment rule in the file
matches at least one tracked path or a declared byte-exact tree, and the
suite's `.gitattributes` readings (the managed-block digest, the byte-exact
surface resolution, the no-governance-migration sweep) pass unchanged.

**ECP-GAT-004:** The work order carries `[delegation] class = "execution"`,
and `.engineering-harness.delegation.toml` configures the gate:
`gate_source = "github-checks"`, `check_name = "validate"`,
`base_ref = "origin/main"` — the check the default branch's ruleset
requires. The delegated route takes `DR-WO-START`, `DR-WO-COMPLETE` and
`DR-VREC-PREPARE` only; approval, verification and the merges stay human.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-029 | ECP-GAT-001 to ECP-GAT-003 |

## Failure behaviour

A dirty managed block reads as customization and stops the work; a
delegated act with the gate not `success` for the exact head is refused
with `WEX-ECP-040`.

## Compatibility and migration

None: both remnants are dead by measurement, and deleting a `.gitattributes`
rule whose pattern matches nothing changes no checkout byte.

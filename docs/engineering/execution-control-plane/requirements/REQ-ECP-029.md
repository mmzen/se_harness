+++
id = "REQ-ECP-029"
type = "requirement"
title = "The .gitattributes tail carries only live rules"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-31"
updated = "2026-08-31"
statement = "WHEN the repository declares byte rules in .gitattributes, THE SYSTEM SHALL carry only rules whose patterns match tracked content and no retained commentary about deletions already executed."
verification_method = ["test", "inspection"]
priority = "should"
source = "issue #285 (functional assessment FA-6, item #285b), gated on the root advancing past 0.7.1 and now unblocked by the 0.12.0 adoption; issue #210's follow-up promise inside the file itself"
measure = "the WO-ECP-010 retention comment is gone (its promise was fulfilled by WO-ECP-011); the se_harness/agent_contract.json rule, whose file WO-ECP-006 deleted, is gone; every remaining rule matches at least one tracked path or a declared byte-exact tree"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The .gitattributes tail carries only live rules

## Rationale

Two remnants sit in the owner region of `.gitattributes`. A six-line
comment retained from `WO-ECP-010` promises that dead governance-migration
files "and these rules are deleted together by issue #210's follow-up work
order" — `WO-ECP-011` executed that deletion on 2026-08-28, so the comment
now describes rules that no longer exist below it. And the rule
`se_harness/agent_contract.json text eol=lf` covers a file `WO-ECP-006`
deleted with the Phase 4 removal; it matches nothing. Dead declarations in
a byte-rule file are worse than clutter: a reader auditing the byte-exact
surfaces must disprove each one.

## Preconditions and trigger

The repository's `.gitattributes` is read by Git on every checkout and by
the byte-exact surface tests.

## Required response

Delete the retained comment block and the dead rule; change no live rule,
no managed block between the `se-harness` markers, and no other line.

## Failure and boundary behavior

The managed block is hash-locked and does not move; `doctor` proves it.
The byte-exact surface tests keep passing unchanged, since neither remnant
backs any assertion.

## Acceptance examples

**Given** the repository after the change, **when** `.gitattributes` is
read, **then** it contains no `governance-migration` commentary and no
`se_harness/agent_contract.json` rule, every remaining pattern matches
tracked content, and `doctor` reads the managed block unchanged.

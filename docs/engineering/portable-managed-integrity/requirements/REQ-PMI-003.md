+++
id = "REQ-PMI-003"
type = "requirement"
title = "Preserve customization and fragment boundaries"
status = "implemented"
owners = ["repository-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN upgrade or doctor observes a non-newline difference in managed content, THE SYSTEM SHALL preserve the existing customization and require manual review rather than overwrite or relabel it as unchanged."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-PMI-001"]
+++

# Requirement: Preserve customization and fragment boundaries

## Rationale

Portability cannot weaken the harness ownership boundary or turn canonicalization into a general content rewrite.

## Preconditions and trigger

Managed content or an extracted managed block differs from its applicable integrity evidence beyond line terminators.

## Required response

Doctor fails the entry. Upgrade classifies it as customized, leaves the file and old lock evidence intact, and produces a bounded manual-review outcome. For fragments, only the content between unique harness markers participates in the managed digest.

## Failure and boundary behavior

Missing, duplicated, reordered, or malformed fragment markers are not repaired automatically. Owner-controlled text outside a valid block neither changes the fragment digest nor becomes writable by the harness.

## Constraints

No fuzzy matching, whitespace folding, Unicode normalization, or similarity threshold is allowed.

## Acceptance examples

Changing only CRLF to LF remains unchanged. Changing a command, identifier, space, or marker is customized and preserved.

## Open decisions

None when approved.

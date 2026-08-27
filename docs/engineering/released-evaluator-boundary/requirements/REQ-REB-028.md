+++
id = "REQ-REB-028"
type = "requirement"
title = "Prove evaluator identity from an index install"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "IF an installed released evaluator carries no PEP 610 archive digest, THEN THE SYSTEM SHALL prove its identity from the version and the installed-payload digest alone and SHALL NOT refuse identity, root qualification or an upgrade for the missing archive digest."
verification_method = "automated-test"
priority = "must"
source = "Owner direction of 2026-08-27; run 33085446752 (RID022 on an index install)"
measure = "identity and qualify released-root pass on a pip index install; RID022 and MG004 fire only on a recorded digest that differs"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Prove evaluator identity from an index install

## Rationale

`pip install se-harness==X` from an index records no `direct_url.json`, so
the installed evaluator has no archive digest to compare. 0.7.0's own managed
workflow installs that way and then demands the digest (`RID022`), so it
cannot pass for any adopter. The installed-payload digest is computed from
the installed files and identifies the evaluator without the archive.

## Required response

- `identity`: when the installation records an archive digest, compare it as
  today; when it records none, report `archive_sha256` as absent and pass on
  version and payload.
- `qualify released-root`: pass `RR001` on version and payload; compare the
  archive only when both the lock and the installation carry one.
- Mutation guard: never require a PEP 610 archive identity of the target
  evaluator.
- The lock records the archive digest when known and `null` otherwise.

## Failure behavior

A recorded archive digest that differs from the expected one still fails
(`RID022`); a payload digest that differs still fails (`RID021`).

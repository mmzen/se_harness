+++
id = "REQ-HAG-010"
type = "requirement"
title = "Record the actual human behind a decision owner label"
status = "draft"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
statement = "An explicitly authorized human can record a decision under a declared owner label while the disposition and lifecycle event retain the actual human identity and the authority used."
verification_method = ["test", "inspection"]
priority = "must"
source = "DEC-HAG-001 WEX201 refusal and mmzen's 2026-10-04 continuation request: diagnose the supported resolution without impersonation or changing approved ownership."

[relations]
derives_from = ["CAP-HAG-001"]
+++

# Record the actual human behind a decision owner label

## Why

mmzen selected `extend-evaluator`, but released 0.22.0 compares the human's
name with the literal owner label `engineering-owner`. The option is known;
recording it is blocked. A role name must not replace the human in the audit
record. Changing the approved work order's owners is not this correction.

## Behavior

The disposition request can name the actual human and, separately, the owner
label under which that human made this exact decision. The evaluator checks
that this label holds the existing decision right for the selected records.
It records both facts without adding a new identity registry or login system.
The caller must already possess the human's matching decision and authority;
supplying either string does not authenticate that authority.

Existing direct-owner requests and historical records retain their meaning.
Invalid owner labels, missing reasons, undeclared options, invalid deferrals
and disallowed lifecycle edges still refuse without writes. Paired-risk
effects retain the same actual human.

## Acceptance

A disposable HAG-shaped decision, with blocked work owned by
`engineering-owner`, accepts the explicit mapping to `mmzen` and records
`decided_by = "mmzen"`. A preview writes nothing. Applying it changes only
the selected decision and its declared paired-risk effects, if any.
An unrelated owner label refuses. Omitting the mapping must not infer it
from the DEC owner, previous approver, Git user or agent profile.

This proposal does not release an evaluator, adopt a new pin, dispose the
live DEC-HAG-001 or verify the hosted service.

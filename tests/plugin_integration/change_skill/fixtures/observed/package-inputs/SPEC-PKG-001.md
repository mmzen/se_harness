+++
id = "SPEC-PKG-001"
type = "specification"
title = "Clear feature message"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
contract = "The feature displays one short English message."

[relations]
specifies = ["REQ-ACC-001"]
+++

# Specification: Clear feature message

## In plain words

Operators read a clear status message.

## Scope

The wording returned by the feature.

## Terms

None.

## Rules

**PKG-MSG-001.** The feature MUST return one short English message.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Message unavailable | Return a short error message | Message unavailable |

## Examples

**Given** a working feature, **when** requested, **then** a message is returned under PKG-MSG-001.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-ACC-001` | PKG-MSG-001 |

## Not decided here

- The punctuation selected by the open decision.

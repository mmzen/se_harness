+++
id = "SPEC-xxx"
type = "specification"
title = "<What this specification binds, as a noun phrase>"
status = "draft"
owners = ["<technical/domain owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
# One sentence, at most 30 words, no code identifier: what an implementation
# must do to conform. The Explorer shows it under the title, so it is the
# line most readers see.
contract = "<One sentence: what an implementation must do to conform.>"

[relations]
specifies = ["REQ-xxx"]
+++

# Specification: <title>

## In plain words

<One or two sentences a newcomer understands. A project term used here is
defined in this repository's own glossary, `GLOSSARY.md` at the repository
root, which this repository writes.>

## Scope

<At most three sentences: what this specification governs and what it
leaves to another artifact. Name the neighbours by id.>

## Terms

- **<term>.** <One sentence. Only terms this specification introduces; the
  glossary has the rest.>

## Rules

<Every rule leads with a stable identifier `<PREFIX>-<AREA>-NNN` in bold,
then one testable sentence of at most 30 words carrying MUST, MUST NOT,
SHALL, SHALL NOT, MAY or refuses. The identifier is the rule's name in
verification contracts, work orders, evidence and deviations; it never
moves and is never reused. Code identifiers belong here.>

**<PREFIX>-<AREA>-001.** <The implementation MUST ...>

**<PREFIX>-<AREA>-002.** <The implementation MUST NOT ...>

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| <the condition> | <what the implementation does, in one sentence> | `<code or none>` |

## Examples

**Given** <state>, **when** <event>, **then** <what holds, naming the rule
by identifier>.

## Coverage

<Every requirement in `specifies` has a row; every rule named exists above.
The validator reads this table and the Explorer shows it on both sides.>

| Requirement | Rules |
| --- | --- |
| `REQ-xxx` | <PREFIX>-<AREA>-001, <PREFIX>-<AREA>-002 |

## Not decided here

- <A choice this specification leaves to the implementation, at most five
  bullets. Actors, inputs and outputs, a state model, data contracts,
  security, performance, observability and compatibility are optional
  sections; the authoring guide says when each earns its place.>

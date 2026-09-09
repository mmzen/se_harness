+++
id = "INT-xxx"
type = "intent"
title = "<Outcome-oriented title>"
status = "draft"
owners = ["<accountable product/domain role>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
# One sentence, at most 30 words, no code identifier: who can do or observe
# what after delivery. It names no solution. The Explorer shows it under the
# title, so it is the line most readers see.
outcome = "<WHO> can <observable result after delivery>."

[relations]
+++

# Intent: <title>

## In plain words

<One or two sentences a newcomer understands. A project term used here is
defined in this repository's own glossary, `GLOSSARY.md` at the repository
root, which this repository writes.>

## Problem

<At most five sentences: what happens today, to whom, and why it is worth
changing. No file, identifier or command. The evidence belongs in a note,
an RCA or an ADR, cited by link. Who the actors are belongs in the
capability; the principles later decisions must keep belong in a
specification rule or an ADR; a risk is a risk artifact; an open question
is a `DEC-` artifact.>

## Success measures

<A success measure is observed in operation, after delivery, by someone who
has not read the code. "Observed" names a place and a cadence an operator
recognises. A row proved by a CI run, a test, a validator run, a
verification or an implementation review is an acceptance check and
belongs in the verification contract. "Today" may read "not measured".>

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| <what an operator can count or time after delivery> | <baseline, or "not measured"> | <target> | <where and how often, in operation> |

## Not this

- <what this initiative deliberately leaves alone; at most five bullets>

+++
id = "RISK-xxx"
type = "risk"
title = "<The threat, as a noun phrase>"
status = "identified"
owners = ["<the roles that own the threatened artifacts>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
# One of: definition, architecture, implementation, verification, release, operation.
stage = "<stage>"
# One of: safety, security, compliance, process, schedule, quality.
category = "<category>"
cause = "<One sentence: the event that would start the damage.>"
effect = "<One sentence: the damage to governed work if it happened.>"
# Each an integer from 1 to 5; the score is their product, 1 to 25.
likelihood = 0
impact = 0
score = 0
raised_by = "<actor or role that recorded the threat>"
# Written by the disposing role when the threat is accepted or mitigated.
residual = ""

[relations]
threatens = ["<the artifacts the threat would damage>"]
+++

# Risk: <title>

Prefer `harnessctl raise-risk`, which computes the score, writes this file in
`raised` and, with `--with-decision`, the decision that stops the threatened
work. A risk written by hand stays `identified` until it is raised.

## Threat

- Cause: one sentence.
- Effect: one sentence.

## Measurement

Likelihood and impact on the five-by-five scale, and their product.

## Answer

Written by `harnessctl decide` on the decision that names this risk in
`concerns`; the disposition table repeats the option, the role, the time and
the verbatim reason. Do not edit it by hand. `mitigated_by` and `avoided_by`
are written by the same act.

+++
id = "RISK-xxx"
type = "risk"
title = "<What could go wrong>"
status = "identified"
owners = ["<raising role or identity>"]
created = "2026-01-01"
updated = "2026-01-01"

[risk]
category = "<safety|security|compliance|process|schedule|quality>"
stage = "<definition|architecture|implementation|verification|release|operation>"
raised_by = "<identity or role that identified the risk>"
likelihood = 1
impact = 1
score = 1
acceptance_level = 1
cause = "<what makes this possible>"
effect = "<what happens if it is realised>"

[relations]
threatens = ["<artifact of the stage above>"]
mitigated_by = []
avoided_by = []
+++

# Risk: <title>

Prefer `harnessctl raise-risk`, which computes `score`, copies the repository's
acceptance level, and sets `identified` or `raised`. A hand-written risk must
keep `score = likelihood x impact` and must be `raised` when the score reaches
the level; the validator refuses otherwise.

## Scenario

## Consequence if realised

## Options considered

## Disposition rationale

Written by the owner of the threatened stage at disposition (`DR-RISK-DISPOSE`).

## Residual risk

Required once `mitigated`: `residual_likelihood` and `residual_impact`, and who accepted the residual.

+++
id = "INT-CIP-001"
type = "intent"
title = "Run each check once, and freeze something that stays frozen"
status = "draft"
owners = ["product-owner", "release-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
+++

# Intent: Run each check once, and freeze something that stays frozen

## Problem

Measured on branch `governance/release-0-7-0-contract-016` on 2026-08-26
(`docs/notes/ci-pipeline.md`): three workflows trigger on unfiltered `push`
and `pull_request` with no concurrency group, so one push to an open pull
request runs 1 + 44 + 9 steps twice; the candidate wheel of one commit is
built five times in `candidate-evidence.yml` and four more in the publication
rehearsal; the unit suite runs four times; the public predecessor evaluator is
installed about ten times. The rehearsal lane keeps a copy of the release
qualification in Python and keeps it aligned with the YAML by a hand-written
YAML parser and a pinned-digest file, so a six-line workflow edit costs sixty
lines of script. The 0.7.0 release needed five release contracts and three
release work orders in twenty-four hours because the contract freezes an
allow-list of work orders while `main` keeps moving; one contract was
invalidated forty-six seconds after approval.

## Outcome

A push produces one run of each check. A commit is built once per workflow.
The release qualification exists in one place and is executed, not digested.
A release contract names a candidate commit and derives its work-order census
from the commits, so a merge to `main` after the cut invalidates nothing. The
notes that describe the pipeline are updated in the same work order as the
pipeline.

## Scope boundary

In: the seven workflows under `.github/workflows/` and the managed template
of `engineering-harness.yml`, the six scripts under `.github/scripts/`, the
release-contract template, one `harnessctl` command that derives a release
unit, and the developer notes. Out: the checks themselves — the N-1 to N
migration rehearsal, predecessor acceptance of the candidate, the
byte-identical recipe replay, and the PyPI environment gate stay as they are.
Out: lifecycle families, decision rights, and the evaluator boundary.

## Accountable product owner

The repository owner, who also holds the release-owner role, decides P4;
the other proposals are engineering decisions under this intent.

## Success measure

Per pull-request push: one run per workflow; one wheel build per workflow;
one unit-suite execution in `candidate-evidence`. `.github/scripts/` shrinks
by at least 2,500 lines with no check removed. The next release is approved
on one release contract whose candidate commit does not move.

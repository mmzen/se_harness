+++
id = "SPEC-HAG-005"
type = "specification"
title = "Separate decision identity from the owner label used"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
contract = "Add an explicit per-disposition owner binding while retaining actual human attribution and all existing decision-right and lifecycle checks."

[relations]
specifies = ["REQ-HAG-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T16:52:37Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved WO-HAG-003 and required verification in response to the reviewed six-artifact correction package. This applies only to that package: local implementation, checks, commits and commit-bound verification preparation. Human verification acceptance, publication, release, adoption and the live DEC-HAG-001 disposition remain separate. Reviewed file hashes were compared before this transition; approval bindings are retained under docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/."
+++

# Separate decision identity from the owner label used

## Scope

This is an additive extension to the owner-selection rule in SPEC-DCM-001
rule 7. It does not replace its owner sets or amend accepted artifact owners.
The current 0.22.0 command lacks this extension. Future released support is
required before using it against DEC-HAG-001.

### HAG-IDN-001 — Explicit binding

Add optional `decide --authority-owner OWNER` alongside `--decision ACTOR`.
`ACTOR` is the actual human decision-maker. `OWNER` is one existing holder
returned by the existing decision-right resolver for this exact question or
deviation. With the option absent, retain direct-owner matching. With it
present, validate its non-empty, bounded, single-line value and require exact
membership in that holder set. Never infer a binding from the DEC's owners,
a previous approval, Git configuration, the executor or an unrelated artifact.

For questions, preserve the existing blocked-artifact owner rules; for
deviations, preserve the departed specification's owner rules. No wildcard,
global mapping file, ambient role, service identity or new ownership mutation
is introduced. An invalid binding refuses before any write.

### HAG-IDN-002 — Attribution and atomicity

For an explicit valid binding, retain `decided_by = ACTOR` in the disposition
and lifecycle event and `authority_owner = OWNER` in the disposition. Keep
the human's supplied reason verbatim. Preview and apply use the same checks.
Preview writes nothing; apply changes only the existing targeted transaction,
including declared paired risks under their unchanged rules. Paired-risk
events retain ACTOR; the DEC records the authority used for their decision.
Historical records without authority_owner remain unchanged and valid.

The released graph validator checks the optional field's scalar shape without
retroactively reassigning authority when a related owner changes later.
Ordinary options, reasons, deferral scopes, revisit requirements, protected
states, graph checks and evaluator identity enforcement remain required.

### HAG-IDN-003 — Authority is external to strings

The agent first resolves the actual human's right under AUTHORITY.md and
matches the selected records, option and reason to that human's decision.
Only then may it supply an explicit binding. This CLI does not authenticate a
human or prove that a claimed mapping is true; neither a passed command nor
an owner label supplies consent. Preserve the existing external enforcement
boundary and describe this limitation in the command help and instructions.

### HAG-IDN-004 — Recovery and release

Example after qualified release and explicit adoption:

```text
harnessctl decide REPO --artifact DEC-HAG-001 --option extend-evaluator --decision mmzen --authority-owner engineering-owner --reason "The retained human decision and exact authority used" --json
```

This is a future command, not an instruction to execute it now. Reuse the
recorded selection, preview with the new release, inspect it, then apply only
under the matching human authority. Do not change WO-HAG-001 owners or invoke
candidate source as governor. The existing VREC-HAG-001 remains bound to its
original candidate. A new final release candidate needs its own verification.

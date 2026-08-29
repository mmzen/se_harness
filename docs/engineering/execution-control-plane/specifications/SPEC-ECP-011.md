+++
id = "SPEC-ECP-011"
type = "specification"
title = "The checkpoint-less check projection and the retirement of focus"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
specifies = ["REQ-ECP-022"]
+++

# Specification: The checkpoint-less check projection and the retirement of focus

## Scope

`harnessctl check` without `--checkpoint` becomes the read-only projection
that `harnessctl focus` returns today; every contract step, rule and shipped
script that names `focus` names `check`; `focus` survives one release as a
byte-identical alias with a deprecation notice. `SPEC-ECP-001`'s
`ECP-NXT-004` is amended by record to name checkpoint-less `check` as the
reference. `harnessctl next` is unchanged.

## Terms

- **Projection:** a result whose `compliance.gates` is empty, whose
  `compliance.checkpoint` is absent, and whose `mutation.writes` is empty.
- **Alias window:** the release that ships this change; the alias is
  removed by a later work order.

## Behavioral rules

### The projection

**ECP-ONE-001:** `check --artifact ID` with no `--checkpoint` returns the
projection: it selects the rule, resolves the procedure and the current
step exactly as `focus` does today, evaluates no gate, and writes nothing.
`--include-background` is accepted and behaves as for `focus`.
`--checkpoint` continues to require its checkpoint-specific arguments and
is unchanged.

**ECP-ONE-002:** The projection's `operation.kind` is `check`; its
`restitution`, `state`, `scope`, `selection`, `findings` and `procedure`
objects are byte-identical to those of `focus` for the same artifact and
snapshot, so `result_sha256` differs from `focus`'s only through
`operation.kind`; a conformance test asserts the identity of every other
section.

**ECP-ONE-003:** The projection refuses the same inputs `check` refuses
(`WEX210` for an unknown artifact or a type outside WO, VREC and RLS) and
accepts `--from-git`, `--changed-path`, `--change-manifest`,
`--pull-request-body`, `--procedure` and `--target` only together with a
checkpoint; supplied without one they are refused with `WEX210` naming the
option.

### The alias

**ECP-ONE-004:** `harnessctl focus` remains for the alias window and emits
exactly the bytes it emits today on standard output and in `--json`, so a
consumer's script or retained result does not change; it additionally
writes one line to standard error naming `check` as its replacement. Its
exit status is unchanged.

**ECP-ONE-005:** The alias is documented as deprecated in the reference and
absent from every procedure, rule, skill and note; a test asserts that no
contract step's `argv` names `focus` and that the reference names it only
in its deprecation line.

### The contracts and the shipped surface

**ECP-ONE-006:** In `WORKFLOW.json` the steps `STEP-WO-START-FOCUS`,
`STEP-WO-START-FINAL-FOCUS`, `STEP-FOCUS-SELECTED`, `STEP-FOCUS-RELATED` and
`STEP-REMEDIATE-FOCUS` keep their identifiers and gate bindings and carry
the argv `["harnessctl", "check", ".", "--artifact", "{artifact_id}"]`
(`{related_id}` where they do today); `WORKFLOW.md`'s `WFL-003` names
`check` and `transition` as the selectors and its procedure table and
lifecycle-decision steps name `check`.

**ECP-ONE-007:** `harness-orient`'s `orient.py` invokes `check` where it
invokes `focus` today and reads the same sections; its `SKILL.md` and
`skill-contract.json` follow if they name the command or pin the script.

**ECP-ONE-008:** `docs/notes/harnessctl-reference.md`, `harnessctl-check.md`
and `harness-overview.md`, and the root `README.md`'s command block, name
`check` for the projection and list `focus` once, as deprecated.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-022 | ECP-ONE-001 to ECP-ONE-008 |

## Failure behaviour

Every rule fails closed as `check` does today; the alias fails exactly as
`focus` does today. No lifecycle state, decision right, gate or digest
preimage changes.

## Compatibility and migration

Consumers receive the new steps through `upgrade --apply` of the release
carrying this change; a retained result produced by `focus` keeps its
digest because the alias's bytes are unchanged. A consumer script calling
`focus` keeps working for one release and sees the notice.

+++
id = "VER-DST-026"
type = "verification"
title = "Evidence that the installed configuration declares only keys the harness reads"
status = "approved"
owners = ["quality-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
verifies = ["REQ-DST-071"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T18:41:35Z"
decided_by = "quality-owner"
reason = "Approved by the accountable repository owner on 2026-09-07 by selecting the presented option 'Approve and start immediately', after the owner instructed that all unused configuration items be removed and DEC-DST-001 was disposed as remove-marker. Seven of the twelve keys in the installed configuration have no reader anywhere in the evaluator; the packet removes them from the standard template, pins the installed key set with its reader inventory, and amends the two definitions whose prose names a removed key."
+++

# Verification Contract: Evidence that the installed configuration declares only keys the harness reads

## Independence

Cases are written from the rule identifiers of `SPEC-DST-026`, not from the
diff. The install and upgrade cases run against a throwaway target from a
wheel built from the candidate and installed in a virtual environment outside
the checkout, which is how a consumer meets the change. The behaviour cases
are the existing provenance tests, run unchanged, because the contract claims
no behaviour moves. The candidate suite runs on the hosted Linux lane; the
local Windows suite is a control, not the record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-071` | test | rendered template key set (DST-CFG-001 to DST-CFG-005, DST-CFG-012) | the rendered configuration parses to exactly two tables, `[harness]` with three keys and `[revision_provenance]` with two, and no other key |
| `REQ-DST-071` | test | reader inventory (DST-CFG-013) | every declared key's name occurs in at least one file under `se_harness/`, and the test names the reading module beside each key |
| `REQ-DST-071` | test | `init` into an empty directory (DST-CFG-001, DST-CFG-002) | the written configuration holds the five keys, and `validate`, `doctor` and `dashboard` succeed on the result |
| `REQ-DST-071` | test | upgrade of a fixture installed by released 0.16.0 (DST-CFG-008, DST-CFG-009) | the plan classifies the configuration as a safe rewrite, the applied file holds five keys, and the recorded project name and installation date are unchanged |
| `REQ-DST-071` | test | same fixture with one edited configuration line (DST-CFG-010) | the plan reports `customized`, apply refuses, and the file and the lock are unchanged |
| `REQ-DST-071` | test | unknown-key tolerance (DST-CFG-011) | a target configuration still carrying the seven removed keys loads, and both provenance loaders return the same values as before |
| `REQ-DST-071` | test | provenance behaviour parity (DST-CFG-007) | the existing `E010`, `E018` and transition-gate tests pass unchanged, with the same codes and messages |
| `REQ-DST-071` | inspection | the two provenance loaders and the mutation guard (DST-CFG-007, DST-CFG-013) | each reads only surviving keys; no reader of a removed key exists |
| `REQ-DST-071` | inspection | `SPEC-REV-001` (DST-CFG-006) | the compatibility sentence no longer promises configuration schema 2, and an amendment record states who changed it and why |
| `REQ-DST-071` | inspection | this repository's root (DST-CFG-014) | the work order's diff touches neither the root configuration nor the lock |

DST-CFG-015 binds the later root-adoption work order and is verified by its
contract, not this one.

## Acceptance scenarios

Scenario A, consumer install: build the candidate wheel, install it in a fresh
virtual environment outside the checkout, `init` an empty directory, then run
`doctor`, `validate` and `dashboard`. Expected: success, and a configuration of
five keys.

Scenario B, consumer upgrade: take a repository initialized by released 0.16.0,
run the candidate's `upgrade` plan and then `upgrade --apply`. Expected: the
configuration is planned as a safe rewrite, the seven keys are gone afterwards,
the project name and installation date survive, and `doctor` passes.

Scenario C, customized configuration: as B, but a line of the configuration was
edited first. Expected: refusal naming the path, nothing written.

## Property and invariant tests

For every key in a rendered configuration, the key is in the pinned set, and
its name occurs in an evaluator source file. For every removed key, no module
under `se_harness/` reads it. For a configuration that still carries a removed
key, the two provenance loaders return the values the surviving keys declare.

## Static and architecture checks

A search for the seven removed names across `se_harness/`, `templates/`,
`.github/` and `scripts/` returns nothing. Their remaining occurrences are
this packet, the complexity audit, the amended `SPEC-REV-001`, the amended
`REQ-SHB-009` example, and the historical verification records that quote the
configuration schema, which are never rewritten.

## Security and privacy checks

The upgrade writes no value taken from the old configuration other than the
project name and the installation date, both of which the installer already
validates against its own patterns before rendering.

## Performance and resilience checks

Not applicable; a smaller file, the same code paths.

## Manual assessments

The owner reviews the amendment to `SPEC-REV-001` and the amended acceptance
example of `REQ-SHB-009` for accuracy, and confirms that no consumer-facing
document told a reader to set one of the removed keys.

## Evidence retention

`docs/engineering/harness-distribution/evidence/WO-DST-025-verification.md`
with the rendered configuration before and after, the upgrade plan, the
scenario outputs, the reader inventory, the hosted lane's test report, and the
local control reading labelled as such.

## Residual uncertainty

A consumer who read the shipped file and set a removed key believed a rule was
in force that never was; removing the key does not tell them, and only the
release notes can. This repository's own root configuration is not exercised
here; the root-adoption work order of the carrying release verifies it.

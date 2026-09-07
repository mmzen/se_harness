+++
id = "SPEC-DST-026"
type = "specification"
title = "The installed configuration declares only keys the harness reads"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"
contract = "The installed configuration declares five keys in two tables, every one of them read by the harness, and an upgrade removes the seven inert keys from existing installations."

[relations]
specifies = ["REQ-DST-071"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T18:41:35Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-07 by selecting the presented option 'Approve and start immediately', after the owner instructed that all unused configuration items be removed and DEC-DST-001 was disposed as remove-marker. Seven of the twelve keys in the installed configuration have no reader anywhere in the evaluator; the packet removes them from the standard template, pins the installed key set with its reader inventory, and amends the two definitions whose prose names a removed key."
+++

# Specification: The installed configuration declares only keys the harness reads

## In plain words

Seven of the twelve keys in the installed configuration leave the template, and
an upgrade removes them from repositories that already hold them. The five that
survive are the three the installer and the mutation guard read, plus the two
booleans that enable a work-order transition.

## Scope

This contract covers the key set of the standard configuration template and
the test that pins it. It also covers what an upgrade does to an installation
holding the removed keys. It does not change any loader's tolerance of an
unknown key, and it does not make any removed setting work.

## Terms

Inert key: a key the template declares and no code path reads. Generation
marker: the value that identifies the shape of an installed configuration.
Managed-mode rule: the existing upgrade classification of a managed file as
unchanged, customized or safely rewritable.

## Rules

**DST-CFG-001.** The template's `[harness]` table MUST declare exactly
`tool_version`, `installed_at` and `project_name`.

**DST-CFG-002.** The template's `[revision_provenance]` table MUST declare
exactly `required_for_verified_work` and `required_for_release`.

**DST-CFG-003.** The keys `artifact_root` and `dashboard_output` MUST be
removed, because the evaluator holds both paths as constants.

**DST-CFG-004.** The keys `require_full_commit`, `require_clean_worktree`,
`verification_record_status` and `release_record_status` MUST be removed.

**DST-CFG-005.** The key `schema_version` MUST be removed, and the lock's
`schema` and `tool_version` MUST remain the only generation marker.

**DST-CFG-006.** Two definitions name a removed key, and both MUST be amended
by record: `SPEC-REV-001`'s compatibility sentence and `REQ-SHB-009`'s
acceptance example.

**DST-CFG-007.** The meaning, default and diagnostics of each surviving
provenance boolean MUST NOT change.

**DST-CFG-008.** An upgrade of an unmodified configuration MUST rewrite it
without the removed keys through the existing managed-mode rule, with no new
installer code.

**DST-CFG-009.** That upgrade MUST preserve the recorded `project_name` and
`installed_at` values.

**DST-CFG-010.** A configuration the owner has edited MUST block the upgrade
as customized, with nothing written.

**DST-CFG-011.** An unknown key in a target configuration MUST stay
tolerated; no loader MAY gain a strict-key refusal in this work.

**DST-CFG-012.** A test MUST pin the exact key set of a freshly installed
configuration, table by table.

**DST-CFG-013.** That test MUST name the reading module beside each key, and
MUST fail when a declared key's name appears in no evaluator source file.

**DST-CFG-014.** This work MUST NOT change this repository's hash-locked root
configuration or its lock.

**DST-CFG-015.** The root-adoption work order for the carrying release MUST
take the reduced configuration into the root and record its new digest.

## Failure behaviour

An edited configuration is reported as customized with its path, and the
upgrade transaction refuses without writing. A rendered template whose key
set differs from the pinned set fails the key-set test with the surplus or
missing name. A removed key that some module still reads is a defect that test
cannot catch. The reader inventory guards it, and the inspection of the two
provenance loaders is the evidence.

## Examples

A freshly installed configuration holding `[harness]` with three keys and
`[revision_provenance]` with two conforms. An upgrade plan from a 0.16.0
installation that classifies the configuration as a safe rewrite conforms. So
does a resulting file with five keys, the original project name and the
original installation date. A rewrite that resets the installation date to
today does not. A plan that classifies an owner-edited configuration as a
safe rewrite does not.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-DST-071` | DST-CFG-001, DST-CFG-002, DST-CFG-003, DST-CFG-004, DST-CFG-005, DST-CFG-006, DST-CFG-007, DST-CFG-008, DST-CFG-009, DST-CFG-010, DST-CFG-011, DST-CFG-012, DST-CFG-013, DST-CFG-014 |

## Not decided here

Whether the tool version stays duplicated between the configuration and the
lock, which is the second half of audit item P2-10. Whether the artifact root
ever becomes configurable. Whether the two provenance loaders keep their
divergent handling of a non-boolean value. The wording of the pinned test's
reader inventory.

+++
id = "INT-PMI-001"
type = "intent"
title = "Make managed-file integrity portable and trustworthy"
status = "approved"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
+++

# Intent: Make managed-file integrity portable and trustworthy

## Problem

Managed-file lock entries currently hash raw bytes. Git newline conversion can therefore make logically identical UTF-8 text appear customized, while manually maintained self-repository lock entries can become stale after a later edit. The merged aggregate-release candidate exposed both failure modes and prevented an otherwise authorized verification transition.

## Desired outcomes

- `doctor` and `upgrade` classify logically identical managed text consistently on LF and CRLF checkouts.
- Real changes inside managed files or managed fragments remain detectable and protected from overwrite.
- Lock format semantics are explicit, versioned, deterministic, and shared by installation, upgrade, and diagnostics.
- Existing schema-1 locks remain readable and are migrated only when safety can be proven.
- The source repository, canonical template, built wheel, and freshly installed harness agree on managed-file integrity.

## Actors and stakeholders

- Repository owners depend on truthful integrity diagnostics.
- Developers and agents need deterministic upgrade decisions across platforms.
- Quality and security owners require customization protection and auditable migration.
- Release owners need source, template, wheel, and installed behavior to remain consistent.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Managed-file doctor failures on the merged Windows checkout | 6 | 0 | corrected-candidate verification |
| LF/CRLF equivalence cases | not specified | 100% pass | every CI run |
| Non-newline mutation rejection cases | partial | 100% pass | every CI run |
| Unsafe legacy-lock overwrites | 0 known | 0 | every upgrade test and release |
| Source/canonical/wheel integrity parity | manual and incomplete | deterministic pass | every release candidate |

## Non-goals

- Canonicalizing arbitrary binary files.
- Changing users' Git configuration or repository-wide line-ending policy.
- Rewriting customized target content to make diagnostics pass.
- Weakening SHA-256, path containment, symlink safety, atomic writes, or authority separation.
- Approving `VREC-AGR-001`, creating a release record or tag, or publishing a package as part of this packet.

## Principles and immutable constraints

Preserve the single standard installation, standard-library runtime, explicit ownership boundaries, non-overwrite behavior, deterministic diagnostics, and human lifecycle authority. A migration may recognize equivalence only through a documented canonical representation or exact legacy evidence.

## Risks and assumptions

- Fact: all current managed and fragment template payloads are UTF-8 text.
- Fact: five observed failures are explained solely by line-ending representation; one additional lock digest is stale.
- Assumption: a versioned canonical text mode is preferable to enforcing a repository-wide Git policy.
- Risk: silently reinterpreting legacy raw digests could hide customization; legacy migration must therefore remain conservative.
- Open decision for approval: whether canonical mode is recorded at lock level or entry level. The specification recommends an explicit schema-2 lock-level mode while reserving entry-level extension.

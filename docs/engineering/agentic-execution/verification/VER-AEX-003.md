+++
id = "VER-AEX-003"
type = "verification"
title = "Independent repository host skill availability conformance"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-AEX-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T16:49:43Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent repository host skill availability conformance

## Independence

Primary evidence comes from verifier-owned fresh repositories, package
inventories, expected adapter mappings, hostile and customized destinations,
and fresh Codex and Claude Code sessions. Expected names, paths, activation
classes, and stops are derived from approved requirements and specifications,
not from implementer comments, successful discovery alone, or model prose.

Static tests establish package and installer properties. Actual-host tests
separately establish that supported host versions discover and invoke the
installed surfaces. Applicable `VER-AEX-001` authority and portability methods
and `VER-AEX-002` Phase 3 procedure methods remain required; this contract does
not retroactively amend their already approved evidence boundaries.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-AEX-009` repository host availability | source/wheel inventory, fresh install and upgrade, lock audit, canonical/adapter comparison, actual Codex and Claude discovery, explicit/implicit activation matrix, nested-directory session, hostile binding and customization tests, before/after manifests | four canonical cores, three Codex explicit-only policies, four Claude adapters, missing and damaged canonical targets, adapter name/path attacks, current and customized installs, fresh host sessions | both supported hosts expose the same four names; writing skills are user-explicit-only; orientation remains read-only and matchable; every adapter loads exactly one same-named canonical core; no second procedure exists; failures cause no partial write or governed effect |

## Acceptance scenarios

1. A source distribution and wheel contain one complete canonical core for each
   of the four skills, three bounded Codex policy files, and four thin Claude
   adapters, with no second canonical body or script.
2. Fresh standard installation records every expected `.agents` and `.claude`
   file in the managed lock and no-op replay reports all files unchanged.
3. An upgrade from the Phase 3 `.agents`-only installation adds the new host
   surfaces atomically without changing the exact `harness-orient` core.
4. A customized canonical file, Codex policy, Claude adapter, or conflicting
   unowned destination blocks the applicable upgrade and preserves all prior
   bytes and lock data.
5. A fresh supported Codex session started at the repository root and from a
   nested directory lists all four canonical skill names.
6. A fresh supported Claude Code session started at the repository root and
   from a nested directory lists all four adapter skill names.
7. Explicit invocation of each skill in each host reaches the same canonical
   contract, evaluator checks, governed state, and declared lifecycle stop.
8. Representative natural-language matches cannot cause any of the three
   writing skills to start implicitly in either host. Explicit invocation
   remains available.
9. `harness-orient` remains eligible for normal read-only matching in both
   hosts and its v1 core, digest, behavior, and result vectors remain exact.
10. Missing, renamed, mismatched, malformed, escaping, linked, or damaged
    canonical targets make a Claude adapter stop before any helper effect.
11. Provider metadata grants no tools, models, hooks, subagents, credentials,
    network access, Git mutation, or external action.
12. Host discovery failure or restart requirements are reported separately
    from harness validity and do not produce a false workflow-success claim.

## Property and invariant tests

- The set of adapter names equals the set of canonical names and contains no
  case-insensitive collision.
- Every Claude adapter maps to `.agents/skills/<same-name>` and no other path.
- Removing or changing the canonical mapping, adapter schema, activation field,
  or name makes validation fail.
- The three writing adapters have `disable-model-invocation: true`; the
  orientation adapter does not.
- The three writing cores have Codex implicit invocation disabled; the exact
  orientation core has no identity-changing addition.
- Claude adapters contain no canonical procedure section, helper script,
  contract copy, shell injection, dynamic command, remote URL, or permission
  grant.
- Canonical manifests include all bound files and match new retained vectors.
- Source, wheel, installed template, and managed target bytes agree for every
  declared inventory entry.
- Planning or apply failure leaves the complete target and lock equal to their
  before-state manifest.
- Host invocation cannot change the skill contract's effect, state, path,
  evidence, evaluator, or decision boundary.

## Static and architecture checks

- Confirm one authoritative core per skill exists only under the standard
  `.agents/skills` template and no duplicate exists under `.claude`, the import
  package, documentation, or another provider directory.
- Confirm Claude adapters contain only the fields and loading steps admitted by
  `SPEC-AEX-005`.
- Confirm Codex metadata contains only the bounded invocation policy.
- Confirm no managed workflow, decision-right, quality-gate, traceability,
  root-lock, lifecycle operation, or evaluator authority is changed.
- Confirm `harness-orient` v1 source, contract, helper, vectors, and manifest
  remain byte-identical.
- Confirm every changed path is admitted by `WO-AEX-004`.

## Security and privacy checks

- Exercise traversal, absolute, alternate-separator, URI-like, control-
  character, Unicode-confusable, case-colliding, linked, junction, hard-linked,
  and reparse-point adapter targets.
- Inject malformed YAML front matter, duplicated fields, unknown adapter
  schema, wrong skill names, unexpected metadata, tool grants, dynamic shell
  lines, remote imports, and missing canonical resources.
- Confirm adapter, lock, host, and test outputs exclude credentials,
  environment dumps, user-home paths, hidden reasoning, and private evidence.
- Confirm a listed skill, runtime permission, candidate checkout, provider
  adapter, or successful host response cannot substitute for exact released-
  evaluator identity or formal authority.
- Run implicit-writing prompts against clean fixtures and prove zero repository,
  Git, lifecycle, helper-callback, credential, network, and external effects.

## Performance and resilience checks

- Measure fresh and nested-directory listing and invocation on supported Codex
  and Claude Code versions without unbounded prompt or output growth.
- Run init, no-op replay, and upgrade on Windows and POSIX path fixtures.
- Exercise read-only targets, locked files, interrupted apply, concurrent target
  drift, malformed lock data, and a host session that predates creation of the
  top-level discovery directory.
- Confirm installation planning remains linear in template file count and
  adapter resolution performs one fixed canonical lookup.

## Manual assessments

- Product and requirements owners confirm repository-scoped default
  availability matches the MVP objective and global installation remains
  intentionally separate.
- Technical and repository owners inspect every adapter and confirm it is a
  replaceable host projection rather than a second authority source.
- Quality and assurance owners observe `/skills` or equivalent listings and
  explicit/implicit behavior in fresh sessions for the recorded host versions.
- A representative operator completes orientation and invokes one writing
  skill explicitly in each host, confirming the same harness-derived decision
  point and non-effects.

## Evidence retention

Retain exact candidate source, candidate commit, package, external released
evaluator, operating system, Codex, and Claude Code identities; source and wheel
inventories; canonical and adapter bytes and digests; managed lock entries;
fresh install, replay, upgrade, conflict, rollback, and path-attack matrices;
fresh root and nested-session listings; explicit and implicit prompt results;
canonical-load traces; evaluator identity results; before/after repository and
Git manifests; manual assessments; deviations; and residual uncertainty at
`docs/engineering/agentic-execution/evidence/WO-AEX-004-verification.md`.

## Residual uncertainty

Verification can prove behavior for the exact tested host versions and show
that compliant hosts load the intended canonical skills. It cannot guarantee
future provider compatibility, prove that a hostile runtime obeyed loaded
instructions, authenticate a human actor, or turn provider permissions into
engineering authority.

Those limitations do not permit a second procedure, silent fallback, implicit
writing effect, incomplete package, unrecorded customization overwrite, or
claim of support for an untested host version.

+++
id = "REL-SEH-019"
type = "release_contract"
title = "Release se-harness 0.8.0: one workflow kernel, a passing fresh consumer, and the real upgrade rehearsal"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[relations]
gates = ["WO-AUT-003", "WO-ECP-005", "WO-ECP-009", "WO-ECP-010", "WO-HBI-005", "WO-HUP-007", "WO-REB-028", "WO-REB-029", "WO-RLO-008", "WO-RLS-014"]

[release_unit]
previous_release_tag = "v0.7.1"
untraced_exemptions = ["992fd735c307e6e6d3ebe509ff83a6dadbc91869", "eaaaaf41d1c5b50caa360a7b6cf3cfa11a976892", "4a43d4e446d317d806c2f052565007fa5587323d", "290f2fbda5b20a8a618fcb254d8b9b16347b970b", "872ced93be2a02aff3d8cb3b29dd810014a83570", "19eade6e06b69fcac2ac0661636221c87941ea5c", "5478146daa58de056fc72a353e9bbd3ab0d84dc1", "11040eefdd7b03517e04dc8ea152768d5636c5f7", "09293fde2a795d5edf49ebd9a157ff6fc819ea27", "e098f15d423ace4cfe289e615ac16374d085752b", "fe9443be49734c5a1ee64719591ae18a4205cafb", "60a60903dd657590073af75bf5ae04459f940c7a", "62997a37ac7d6222834b9a78a80937d4685c3898", "4b1eee9055af5da98f8714ac845a2afdfdcb56e2", "ff0e3376e0eb9d7622828a5a843f244988860ec8"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T15:05:47Z"
decided_by = "release-owner"
reason = "Approved by the accountable release owner on 2026-08-28 with the words 'approve REL-SEH-019 and WO-RLS-014', freezing the ten-work-order allow-list in gates as the exact 0.8.0 release unit. Re-measured immediately before this transition over the packet branch carrying main ff0e337: the nine existing members read implemented with verified coverage, VREC-REB-026 and VREC-REB-027 verified today as the entry condition; no other work order absent from the v0.7.1 tree reached implemented; on the whole-gates basis nine verification contracts, a twelve-requirement union and eleven keyed evidence paths; the commit census from v0.7.1 traces three work orders and exempts fifteen named merge commits, so the derivation is complete, and no candidate_commit is named because the candidate does not exist yet, so QGP-G5P-RELEASE-UNIT passes unmeasured. Governing public 0.7.1 evaluator outside the checkout: validate 0 errors, 471 maintenance warnings; doctor 0 FAIL. From this moment gates cannot be widened, narrowed or repaired in place; a further landing with packaged-surface bytes is a stop condition remedied only by a successor contract. This approval gates the candidate commit and the promotable build and authorizes neither by itself."
+++

# Release Contract: Release se-harness 0.8.0: one workflow kernel, a passing fresh consumer, and the real upgrade rehearsal

## Lifecycle and authority

This contract's approval by the release owner is what permits a promotable
build, the candidate commit, and release preparation. Its authoritative state,
and the timestamp and reason of every decision taken on it, are the front
matter and `[[lifecycle_events]]` above. It succeeds `REL-SEH-018`, the
released 0.7.1 contract, and rejects nothing.

0.8.0 is the first release after the 2026-08 complexity audit
(`docs/notes/complexity-audit-2026-08.md`). It carries the P0 repairs that
landed on `main` under that audit and the adoption of 0.7.1 as this
repository's root. Two of them consumers cannot receive any other way: the
fresh-consumer `doctor` fix (`WO-HBI-005`, issue #207) lives in the managed
`.gitattributes` fragment and the shipped class table, and the workflow-kernel
changes (`WO-ECP-005`, `WO-ECP-009`, issue #212) live in the packaged
contracts. Two follow-ups wait on this release becoming this repository's
root: the deletion of the retired governance-migration files (issue #210) and
the consumers' fresh-install fix.

Approval authorizes nothing on its own. It is the precondition for
`WO-RLS-014`'s candidate commit and promotable build, `VREC-SEH-016`, and
`RLS-SEH-017` preparation; each remains a separate later decision.

## Release unit

One `se-harness` 0.8.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.8.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.8` maintenance line
established at the released candidate, and a release-bound static Explorer
demonstration.

The release-bearing work added after the immutable `v0.7.1` baseline is
exactly these nine work orders. Every row was measured on `main` at
`ff0e337` as active, `implemented`, holding work-order-keyed evidence,
absent from the `v0.7.1` tree, and unnamed by any released release record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-007` | Adopt exact public 0.7.1 as the standard root, the simple way | `VREC-HUP-006` verified |
| `WO-RLO-008` | Make the recipe-bound candidate export independent of the calling host | `VREC-RLO-008` verified |
| `WO-REB-028` | Retire the predecessor-bootstrap release path and keep its history as inert facts | `VREC-REB-026` verified (2026-08-28, as this packet's entry condition) |
| `WO-REB-029` | Retire the predecessor-bootstrap rules from the consumer-installed validator | `VREC-REB-027` verified (2026-08-28, as this packet's entry condition) |
| `WO-AUT-003` | Retarget the dry-run pin so requirements drafted in the closed vocabulary do not fail the suite | `VREC-AUT-003` verified |
| `WO-HBI-005` | Make `doctor` pass in a fresh consumer repository | `VREC-HBI-005` verified |
| `WO-ECP-005` | One result schema and one rule selector | `VREC-ECP-005` verified |
| `WO-ECP-009` | One precondition engine: `transition` evaluates the contract's gates | `VREC-ECP-009` verified |
| `WO-ECP-010` | Replace the governance-migration rehearsal with a real upgrade rehearsal | `VREC-ECP-010` verified |

`WO-RLS-014` is the tenth member: it qualifies and builds the candidate and
retains the evidence; the candidate version is already 0.8.0 (moved by
`WO-HUP-007`). It receives its verified coverage from the aggregate record
`VREC-SEH-016`.

Packaged-surface bytes in the unit come from `WO-HUP-007` (version identity,
`predecessor_facts`), `WO-REB-028` (`release_qualification.py`, `cli.py`,
`interpreter_safety.json`), `WO-REB-029` (the template validator),
`WO-HBI-005` (`hash_bound.py`, `hash_bound_classes.json`, the
`.gitattributes` fragment), `WO-ECP-005` (the workflow kernel,
`workflow_contract.json` and its managed rendering), `WO-ECP-009`
(`quality_gates_contract.json` v2 and its renderings), and `WO-ECP-010`
(`cli.py`). `WO-AUT-003` and `WO-RLO-008` changed tests and repository
tooling only; they are members because their commits are on the release path.

### Commit census

`harnessctl release-unit . --from v0.7.1 --to ff0e337` traces `WO-HUP-007`
(the merge of #203), `WO-RLO-008` (#202) and `WO-RLS-013` (two commits of the
0.7.1 packet that post-date the tag; `WO-RLS-013` is named by released
`RLS-SEH-016` and is not a member) and reports fifteen first-parent commits
without a standalone `Harness-Work-Order` trailer. Each is exempted in
`[release_unit].untraced_exemptions` for the reason given here; with these
exemptions the derivation is complete.

| Commit | Pull request | Reason |
| --- | --- | --- |
| `992fd73` | #205 | merge of the complexity-audit note; ungoverned `docs/notes/` path |
| `eaaaaf4` | #229 | merge of the agentic-execution review note; ungoverned path |
| `4a43d4e` | #231 | merge of the execution-control-plane definition packet; draft artifacts, no work order |
| `290f2fb` | #232 | merge of the audit note's issue links; ungoverned path |
| `872ced9` | #206 | merge of `WO-REB-028`'s branch; the trailer is on the branch commits and in the pull-request body, not on the merge commit |
| `19eade6` | #230 | merge of `WO-REB-029`'s branch; trailer on the branch commits and in the body |
| `5478146` | #233 | merge of the issue #208 assessment note; ungoverned path |
| `11040ee` | #234 | merge of three corrected notes; ungoverned path |
| `09293fd` | #237 | merge of `WO-AUT-003`'s branch; trailer on the branch commits and in the body |
| `e098f15` | #236 | merge of `WO-HBI-005`'s branch; trailer on the branch commits and in the body |
| `fe9443b` | #238 | merge of the amended ECP packet and its approvals; definitions and `WO-ECP-005` approved, no implementation |
| `60a6090` | #235 | merge of the root-upgrade evidence note; ungoverned path |
| `62997a3` | #239 | merge of `WO-ECP-005`'s branch; trailer on the branch commits and in the body |
| `4b1eee9` | #240 | merge of `WO-ECP-009`'s branch; trailer on the branch commits and in the body |
| `ff0e337` | #241 | merge of `WO-ECP-010`'s branch; trailer on the branch commits and in the body |

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-014` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval, as for `REL-SEH-018`; the census above is the reported
evidence, and `WO-RLS-014` re-runs the derivation at the candidate and records
it.

## Required evidence

### Entry criteria

- The nine existing members are active, `implemented`, retain work-order-keyed
  evidence, and hold verified assurance coverage. Measured at `ff0e337`: seven
  of nine at drafting; `VREC-REB-026` and `VREC-REB-027` were verified by the
  assurance owner on 2026-08-28 as this packet's entry condition, so nine of
  nine on the packet branch. Correction to those two decision reasons: they
  state the bound evidence blob is byte-identical at the candidate and the
  tip; it is not. Each document was appended after its candidate with the
  hosted-lane and review sections (`WO-REB-028-verification.md` §16–17 at
  `03e4f0d`/`29a05c3`; `WO-REB-029-verification.md` §18 at `a9f3118`), the
  candidate's bytes preserved as a prefix, which is this repository's usual
  sequence. The record binds the commit and the artifact snapshot, not the
  evidence digest, so the decisions stand; the sentence was written before
  the measurement ran and is corrected here because lifecycle events are
  append-only.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph beyond
  the two canonical templates.
- `WO-RLS-014` is separately reviewed and approved before start preflight or
  any edit.
- This contract is approved by the release owner before the candidate commit and
  the promotable build. Immediately before that approval the allow-list is
  re-measured and every work order that reached `implemented` since this file
  was written is reported and either added to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity and
  start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `ff0e337` plus this packet, with the exact public
0.7.1 evaluator outside the checkout in isolated mode.

- `validate`: 0 errors, 471 pre-existing maintenance warnings.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `ff0e337` on `main`: all thirteen checks `success` on the
  push event, including the real upgrade rehearsal 0.7.1 to 0.8.0 on Linux
  and Windows with agreeing lock digests.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all ten
entries.** `VREC-SEH-016` must bind one clean 0.8.0 candidate commit to
exactly the ten work orders named in `gates`, to eight verification contracts
(`VER-AUT-001`, `VER-DST-001`, `VER-ECP-005`, `VER-ECP-007`, `VER-HBI-001`,
`VER-HUP-007`, `VER-REB-012`, `VER-REB-013`, `VER-RLO-004` — nine with
`WO-RLS-014`'s), and to eleven work-order-keyed evidence paths: the ten
existing (listed in the domain index) plus
`docs/engineering/release-0-8-0/evidence/WO-RLS-014-verification.md`. The
requirement union is twelve: `REQ-AUT-003`, `REQ-DST-006`, `REQ-ECP-009`,
`REQ-ECP-010`, `REQ-ECP-012`, `REQ-HBI-001`, `REQ-HBI-003`, `REQ-HBI-004`,
`REQ-HUP-014`, `REQ-HUP-015`, `REQ-REB-029`, `REQ-RLO-017`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.7.1 evaluator outside
the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`; review
preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS`; the candidate's own
`qualify complete-candidate`; the full suite on Linux and on Windows; the
real upgrade rehearsal 0.7.1 to 0.8.0 `pass` on both platforms with agreeing
`semantic_sha256`; all pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a Linux host with the pinned producer image, two byte-identical
producer runs, the bundle manifest from
`scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the same
digests.

## Compatibility and migration

0.8.0 changes the packaged contracts and one managed fragment; installed
copies regenerate on `upgrade`:

- `WORKFLOW.json` loses `handoff_fields` and every `handoff` block; each rule
  carries `restitution.done` and `current_lifecycle_state`. Every workflow
  command emits the one `se-harness-workflow-result-v2` result; the
  `--result-schema` option is removed and passing it is an argument error
  (`WO-ECP-005`; `SPEC-ADS-001`, `REQ-ADS-002`, `SPEC-WEX-002` amended).
- `QUALITY_GATES.json` is `se-harness-quality-gates-v2` with predicate-level
  `checkpoints` and a `transition_bindings` table; a v1 copy loads as
  `WEX-ECP-030`. `transition` evaluates those bindings through the same gate
  evaluator as `check`, and `check --checkpoint transition --target STATE`
  previews it (`WO-ECP-009`).
- The managed `.gitattributes` fragment carries only the `evaluator-evidence`
  rule and the class table ships no `governance-migration-protocol`; a fresh
  consumer's first `doctor` after its first commit exits 0 (`WO-HBI-005`).
  `upgrade` classifies `.gitattributes` as `update` in fragment mode and
  preserves owner content.
- `qualify predecessor-view` and `rehearse-migration` are gone; the consumer
  validator no longer carries the predecessor-view rules (`WO-REB-028`,
  `WO-REB-029`, `WO-ECP-010`).
- The wheel still carries `se_harness/governance_migration*`, dead and
  unreferenced: their deletion is refused by the 0.7.1 root and follows this
  release's adoption (`WO-ECP-010`, issue #210).

A 0.7.1 root reads a 0.8.0-written lock without change (schema 3, five
evaluator fields). Ready records prepared under 0.7.1 report `E012` after a
root advances to 0.8.0 until re-prepared; that is by design and is what the
upgrade rehearsal tolerates.

## Security and provenance

The build of record is recipe-bound and digest-pinned (`release/build-recipe.json`,
`release/build-toolchain.lock`); the release record binds the wheel and sdist
digests through a schema-2 distribution table; the publication workflow moves
only verified inert bytes into privileged jobs and the `pypi` environment
remains a separate human decision. Identity by version and installed-payload
digest is unchanged and remains what every mutation guard proves.

## Promotion policy

- `VREC-SEH-016` verified by the assurance owner on the exact candidate.
- `RLS-SEH-017` prepared by generic `prepare-release`, then bound by
  `scripts/bind_release_distribution.py` to the Linux build of record; the
  hosted replay dispatched on the review ref before the release decision.
- The `released` transition rides its own pull request to `main` and is the
  release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched from
  `main` with only `release_record=RLS-SEH-017`; tag `v0.8.0`, GitHub Release,
  `release/0.8` established, PyPI publication, Pages deployment, and the alias
  tag `last` moved to `v0.8.0`.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-014` (engineering
  owner), as two distinct decisions.
- Start of `WO-RLS-014`, its completion, the verification of `VREC-SEH-016`,
  the preparation and release of `RLS-SEH-017`, the publication dispatch and
  the `pypi` environment: each a separate decision by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after this
  contract's approval is a stop condition; the remedy is rejection and a
  successor contract, never widening in place.

## Known open questions that do not block this release

- `MG004` still guards release-record preparation (`require_archive`);
  preparing a release from an index-installed root needs a wheel-file install
  of the evaluator that prepares it.
- `SPEC-WEX-002` and `SPEC-CIP-001` carry dated amendments rather than
  rewritten rules; `ARCH-REB-010` still binds `se_harness/interpreter_safety.py`
  (#220).
- The Phase 4 delegated completion needs handoff-bound evidence it does not
  retain (`WO-ECP-006`, gated on issue #211); no target has ever declared
  `[agentic_delegation]`.

## Rollback criteria and procedure

A published 0.8.0 that fails its post-release observation is not withdrawn from
PyPI; a successor release supersedes it. Before publication, any failed gate
stops the sequence at the record: `RLS-SEH-017` is rejected with the reason and
a successor record is prepared from a fresh candidate. The `last` alias tag is
moved only after the public observation passes. Stop condition: the candidate
commit is not an ancestor of the ref being released, or
`harnessctl release-unit --contract REL-SEH-019` reports `E-CIP-001`; the
remedy is a new contract naming a new candidate commit, never an in-place edit
of `gates`.

## Post-release observation window

Within one day of publication: `pip install "se-harness==0.8.0"` into a fresh
venv from the index; `harnessctl init`, one commit and `doctor` exiting 0 (the
#207 acceptance in the wild); `harnessctl identity` and `qualify released-root`
on that root; and the adoption of 0.8.0 as this repository's governor by
`harnessctl upgrade . --apply` under an ordinary work order, followed by the
issue #210 follow-up deletion. The adoption is the release's acceptance test
and is recorded in that work order's evidence.

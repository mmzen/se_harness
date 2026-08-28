+++
id = "REL-SEH-020"
type = "release_contract"
title = "Release se-harness 0.9.0: the agent's first call, Git-derived scope, harness-authored evidence and the mandatory gate"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[relations]
gates = ["WO-ECP-001", "WO-ECP-002", "WO-ECP-003", "WO-ECP-011", "WO-HUP-008", "WO-REB-030", "WO-RLS-015"]

[release_unit]
previous_release_tag = "v0.8.0"
untraced_exemptions = ["26286271eda1228ebabb69621259fd9c6c5908e2", "6573bd892d1887a0e0ba62e2e53d5e80d8bf82d5", "f62256f2117f628c7ed310e8250db826503c53c5", "b46008539a859825d7401a49ca00906a5a90030b", "eae9332301855171b721ef50f696ecd8d0c199f0", "233bc9256044156fda7646556aaf163ff033a7a6", "0961176362e2d5d628ab505f2cc426356e21de2b", "e75fac87fd224d4e389352d03852cce09b46c039", "effbcbc2a0cc9d5b47a6bea6edd214a7c004d000"]
+++

# Release contract: se-harness 0.9.0

## Lifecycle and authority

This contract is a definition. Its approval by the release owner authorizes
`WO-RLS-015` to be approved and started as separate acts; it authorizes no
candidate, build, verification record, release record, tag, publication or
deployment by itself. Every later step is the decision of the role that owns
it, recorded on the artifact it changes. The aggregate verification record
is `VREC-SEH-018`; the release record is `RLS-SEH-018`.

## Release unit

One `se-harness` 0.9.0 release derived from one clean candidate commit cut
from `main`: a recipe-bound reproducible wheel, a normalized source
distribution, a checksum manifest, a schema-2 bound distribution table, an
immutable `v0.9.0` tag, GitHub Release assets, publication of the same
qualified files to PyPI, the canonical `release/0.9` maintenance line
established at the released candidate, and a release-bound static Explorer
demonstration.

The release-bearing work added after the immutable `v0.8.0` baseline is
exactly these six work orders. Every row was measured on `main` at
`effbcbc` as active, `implemented`, holding work-order-keyed evidence,
verified, absent from the `v0.8.0` tree, and unnamed by any released release
record.

| Work order | Outcome | Coverage at drafting |
| --- | --- | --- |
| `WO-HUP-008` | Adopt exact public 0.8.0 as the standard root, the simple way; candidate moved to 0.9.0 | `VREC-HUP-007` verified |
| `WO-ECP-011` | Delete the retired governance-migration stage machine (issue #210) | `VREC-ECP-011` verified |
| `WO-REB-030` | Keep `interpreter_safety.evaluate`, delete its declaration apparatus and the `repository_tools` copy (issue #220) | `VREC-REB-028` verified |
| `WO-ECP-001` | `harnessctl next` and `check --from-git`; `ECP-CHG-007` | `VREC-ECP-012` verified |
| `WO-ECP-002` | `harnessctl evidence`, identifier allocation across local refs, `harnessctl pr-body`, the retained `handoff.json` | `VREC-ECP-013` verified |
| `WO-ECP-003` | The managed workflow enforces scope on every pull request; the canonical block carries the change set and every predicate status | `VREC-ECP-014` verified |

`WO-RLS-015` is the seventh member: it qualifies and builds the candidate and
retains the evidence; the candidate version already reads 0.9.0 (moved by
`WO-HUP-008`). It receives its verified coverage from `VREC-SEH-018`.

Packaged-surface bytes in the unit come from `WO-HUP-008` (version identity),
`WO-ECP-011` (the four deleted stage-machine files, `interpreter_safety.json`'s
boundary registry, package data), `WO-REB-030` (`interpreter_safety.py`
reduced to the rule; `interpreter_safety.json` and the `repository_tools`
copy deleted; package data), `WO-ECP-001` (`workflow.py`,
`workflow_compliance.py`, `workflow_result.py`, `cli.py`,
`workflow_contract.json` and the template `WORKFLOW.json`/`.md`),
`WO-ECP-002` (`workflow_compliance.py`, `artifact_layout.py`, `github_ci.py`,
`cli.py`, the contract corrective, the pull-request seed) and `WO-ECP-003`
(`workflow_result.py`, the managed template workflow, the seed).

### Commit census

`harnessctl release-unit . --from v0.8.0 --to effbcbc` reports nine
first-parent commits without a parseable `Harness-Work-Order` trailer and
traces no work order. The cause is measured, not assumed: the branch commits
behind each merge carry the line `Harness-Work-Order: WO-…` as body text in
a paragraph that precedes a separate `Co-Authored-By` paragraph, and Git's
trailer parser reads only the final paragraph, so `%(trailers:key=…)` is
empty for every commit of this period; the same line is present verbatim in
every pull-request body. Each merge is exempted in
`[release_unit].untraced_exemptions` for the reason given here, and the
membership above is established by the allow-list and by each member's own
lifecycle state and evidence, as the 0.8.0 contract did for its merges. From
this packet onward commits carry both lines in one final trailer paragraph.

| Commit | Pull request | Reason |
| --- | --- | --- |
| `2628627` | #243 | merge of the 0.8.0 release record (`WO-RLS-014`, released by `RLS-SEH-017`; not a member) |
| `6573bd8` | #244 | merge of `WO-HUP-008`'s branch; the work-order line is body text on the branch commits and in the body |
| `f62256f` | #245 | merge of `WO-ECP-011`'s branch; same |
| `b460085` | #246 | merge of `WO-REB-030`'s branch; same |
| `eae9332` | #247 | merge of `ADR-AEX-008`, a governance-only decision record named under the draft `WO-ECP-006`; no implementation, not a member |
| `233bc92` | #248 | merge of the agentic-execution README rewrite, named under the draft `WO-ECP-006`; documentation only, not a member |
| `0961176` | #249 | merge of `WO-ECP-001`'s branch; same as #244 |
| `e75fac8` | #250 | merge of `WO-ECP-002`'s branch; same |
| `effbcbc` | #251 | merge of `WO-ECP-003`'s branch; same |

This contract names no `candidate_commit`: the candidate is created by
`WO-RLS-015` after this approval. `QGP-G5P-RELEASE-UNIT` therefore passes
unmeasured at approval, as for `REL-SEH-019`; the census above is the
reported evidence, and `WO-RLS-015` re-runs the derivation at the candidate
and records it, expecting the same nine exemptions and no traced work order.
That the derivation cannot trace this period is recorded as an open question
below.

## Required evidence

### Entry criteria

- The six existing members are active, `implemented`, retain
  work-order-keyed evidence, and hold verified assurance coverage. Measured
  at `effbcbc`: six of six.
- No existing member is named by a released release record.
- No stale `ready` verification or release record exists in the graph beyond
  the two canonical templates.
- `WO-RLS-015` is separately reviewed and approved before start preflight or
  any edit.
- This contract is approved by the release owner before the candidate commit
  and the promotable build. Immediately before that approval the allow-list is
  re-measured and every work order that reached `implemented` since this file
  was written is reported and either added to `gates` or excluded by name.
- Formal validation, released-evaluator `doctor`, managed-root integrity and
  start preflight pass without structure, governance or policy errors.

### Measured readiness at drafting

Measured over `main` at `effbcbc` plus this packet, with the exact public
0.8.0 evaluator outside the checkout in isolated mode.

- `validate`: 0 errors, 473 pre-existing maintenance warnings.
- `doctor`: 0 `FAIL`.
- Hosted lanes at `effbcbc` on `main`: every check `success` on the push
  event, including the real upgrade rehearsal 0.8.0 to 0.9.0 on Linux and
  Windows.

### Exact aggregate verification

**Every figure here is measured over the whole `gates` array, all seven
entries.** `VREC-SEH-018` must bind one clean 0.9.0 candidate commit to
exactly the seven work orders named in `gates`, to seven verification
contracts (`VER-DST-001`, `VER-ECP-001`, `VER-ECP-002`, `VER-ECP-003`,
`VER-ECP-007`, `VER-HUP-008`, `VER-REB-014`), and to seven work-order-keyed
evidence paths: the six listed in the domain index plus
`docs/engineering/release-0-9-0/evidence/WO-RLS-015-verification.md`. The
requirement union is thirteen: `REQ-DST-006`, `REQ-ECP-001` to `REQ-ECP-007`,
`REQ-ECP-012`, `REQ-HUP-016`, `REQ-HUP-017`, `REQ-REB-030`.

### Candidate qualification

At the exact candidate commit, all with the governing 0.8.0 evaluator outside
the checkout unless stated: `validate` 0 errors; `doctor` 0 `FAIL`; review
preflight `PASS`; `scripts/validate_release_distributions.py` and
`scripts/check_portable_release_surface.py` `PASS` in `--repository`,
`--wheel` and `--harnessctl` modes; the candidate's own `qualify
complete-candidate`; the full suite on Linux and on Windows; the real upgrade
rehearsal 0.8.0 to 0.9.0 `pass` on both platforms with agreeing
`semantic_sha256`; all pull-request lanes `success` at the candidate head.

### Build of record

The recipe-bound replay (`python -m repository_tools.release_build replay`)
run on a Linux host with the pinned producer image, two byte-identical
producer runs, the bundle manifest from
`scripts/create_release_bundle_manifest.py`, and the hosted
`release-candidate-replay.yml` dispatch on the review ref reproducing the same
digests.

## Compatibility and migration

0.9.0 changes the packaged contracts, one managed workflow, one seed and the
CLI surface; installed copies regenerate on `upgrade`:

- **Four commands.** `harnessctl next` (the agent's first call: state,
  governing chain, declared scope, reading manifest, next command, required
  decision in one schema-2 result with a `Context` section);
  `check --from-git BASE` (the change set read from Git, complete by
  construction; the selected work order's own file and its packet directory
  admitted by construction, `ECP-CHG-007`); `harnessctl evidence` (the
  packet with a fenced TOML header that `QGP-G4I-EVIDENCE` reads through a
  parser — substring-bound packets still pass for one release under
  `W-ECP-002`); `harnessctl pr-body`. `create-artifact --id` becomes
  optional: the lowest free `TYPE-DOMAIN-NNN` across every local branch and
  tag is allocated.
- **The canonical block** gains `Change set` and `Gates`, so every
  `result_sha256` changes at this upgrade; a `Harness-Restitution` line
  written under 0.8.0 mismatches on re-run and is regenerated by `pr-body`.
- **The managed workflow** replaces the guarded restitution step with an
  unconditional scope step: after `upgrade`, a consumer's pull request whose
  diff leaves the selected work order's declared scope fails its required
  check naming the path; a body without a standalone `Harness-Work-Order`
  line fails it. The seeded pull-request template states this. This is the
  behavioural change of the release and the reason it is 0.9, not 0.8.1.
- **`WORKFLOW.json`**: the `QGP-G4I-COMPLETE` corrective names
  `--from-git <base>` and the `QGP-G4I-EVIDENCE` corrective is the `evidence`
  command; the failed-operation retry names `harnessctl next`.
- **The wheel** no longer carries `se_harness/governance_migration*`,
  `governance_migration_contract.json` or `interpreter_safety.json`; the
  `EPS` refusals and `runtime_identity` are unchanged; `ISD`, `ISC` and `MIG`
  families are withdrawn.

A 0.8.0 root reads a 0.9.0-written lock without change (schema 3, five
evaluator fields). Ready records prepared under 0.8.0 report `E012` after a
root advances to 0.9.0 until re-prepared; the upgrade rehearsal tolerates
that by design. A 0.8.0 root evaluating a 0.9.0-written evidence packet reads
it by substring: a packet written by `harnessctl evidence` alone is not
bound for a 0.8.0 root, which is why this repository's own packets of this
period carry both forms.

## Security and provenance

The build of record is recipe-bound and digest-pinned
(`release/build-recipe.json`, `release/build-toolchain.lock`); the release
record binds the wheel and sdist digests through a schema-2 distribution
table; the publication workflow moves only verified inert bytes into
privileged jobs and the `pypi` environment remains a separate human decision.
Identity by version, installed-payload digest and archive pair is unchanged
and remains what every mutation guard proves. Evidence packets and
`handoff.json` are written without a mutation-guard operation: they are
retained evidence, not authority (`WO-ECP-002`, deviation 3).

## Promotion policy

- `VREC-SEH-018` verified by the assurance owner on the exact candidate.
- `RLS-SEH-018` prepared by generic `prepare-release` from a wheel-file
  installed 0.8.0 evaluator (the lock carries the archive pair since
  `WO-HUP-008`, so `MG004` does not arise), then bound by
  `scripts/bind_release_distribution.py` to the Linux build of record; the
  hosted replay dispatched on the review ref before the release decision.
- The `released` transition rides its own pull request to `main` and is the
  release owner's act.
- After the record is `released` on `main`: `publish-pypi.yml` dispatched from
  `main` with only `release_record=RLS-SEH-018`; tag `v0.9.0`, GitHub Release,
  `release/0.9` established, PyPI publication, Pages deployment, and the alias
  tag `last` moved to `v0.9.0` after the observation passes.

## Human approval triggers

- Approval of this contract (release owner) and of `WO-RLS-015` (engineering
  owner), as two distinct decisions.
- Start of `WO-RLS-015`, its completion, the verification of `VREC-SEH-018`,
  the preparation and release of `RLS-SEH-018`, the publication dispatch and
  the `pypi` environment: each a separate decision by its accountable owner.
- Any work order reaching `implemented` with packaged-surface bytes after this
  contract's approval is a stop condition; the remedy is rejection and a
  successor contract, never widening in place. `WO-ECP-006`, `WO-ECP-004`
  and `WO-ECP-007` are therefore not started before the candidate is cut.

## Known open questions that do not block this release

- `harnessctl release-unit` traces work orders only through Git trailers;
  the commits of this period carry the line as body text and are exempted
  by name. A later ordinary work order may let the derivation read a
  standalone `Harness-Work-Order:` line from a commit body when no trailer
  parses, so that a census never again depends on paragraph placement.
- This repository's own pull requests run the root 0.8.0 workflow until
  0.9.0 is adopted as the root; the mandatory gate protects consumers first.
  The hosted demonstration of the gate is a verification condition of this
  release (see the observation window).
- The remediation path still renders `WEX210: WEX210:` for a `check` that
  selects a delivery rule at the handoff checkpoint; cosmetic, `WO-ECP-005`'s
  territory.

## Rollback criteria and procedure

A published 0.9.0 that fails its post-release observation is not withdrawn
from PyPI; a successor release supersedes it. Before publication, any failed
gate stops the sequence at the record: `RLS-SEH-018` is rejected with the
reason and a successor record is prepared from a fresh candidate. The `last`
alias tag is moved only after the public observation passes. Stop condition:
the candidate commit is not an ancestor of the ref being released, or
`harnessctl release-unit --contract REL-SEH-020` reports a difference beyond
the nine recorded exemptions; the remedy is a new contract naming a new
candidate commit, never an in-place edit of `gates`.

## Post-release observation window

Within one day of publication: `pip install "se-harness==0.9.0"` into a fresh
venv from the index; `harnessctl init`, one commit and `doctor` exiting 0;
`harnessctl next .` in that repository answering `WEX-ECP-001` (nothing in
progress) rather than an error; `harnessctl identity` and `qualify
released-root` on that root; the adoption of 0.9.0 as this repository's
governor by `harnessctl upgrade . --apply` from a wheel-file install under an
ordinary work order; and, as the deferred verification condition of
`VER-ECP-003`, the first pull request after that adoption running the
mandatory gate hosted — one throwaway branch touching an out-of-scope path
red with `QGP-G4I-PATHS`, one in-scope branch green — recorded in the
adoption work order's evidence. The adoption is the release's acceptance
test.

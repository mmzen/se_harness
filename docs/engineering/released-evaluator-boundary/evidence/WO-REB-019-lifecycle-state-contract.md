# WO-REB-019 lifecycle-state contract evidence

## Scope and authority

This evidence covers the locally reviewed implementation of `REQ-REB-018`,
`REQ-REB-019`, `SPEC-REB-009`, `ARCH-REB-008`, `ADR-REB-008`, `VER-REB-008`,
and `WO-REB-019` for GitHub issue #103 / RCA `RC-060-03`.

The packet was approved and WO-REB-019 was started on 2026-08-23. Complete
qualification exposed omitted terminal compatibility vocabulary. The owner then
authorized exactly seven additional terminal rows: definition `ready`,
`in_progress`, `verified`, `released`, and `superseded`, and work-order `ready`
and `superseded`. The amendment added no transition, version reservation, or
predecessor adapter. All other packet and external-action boundaries remained
unchanged.

This is pre-candidate evidence. No candidate commit, VREC, RLS, push, hosted
dispatch, tag, publication, deployment, root upgrade, maintenance mutation,
credential use, or external-policy change was performed.

## Released-predecessor start gate

The start gate used the exact public 0.5.0 wheel from the retained release
workspace:

- wheel: `se_harness-0.5.0-py3-none-any.whl`;
- SHA-256: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`;
- isolated evaluator: `../q-wo-reb-019-eval05`;
- disposable predecessor view: `../q-wo-reb-019-start-view`;
- excluded predecessor-incompatible pair only:
  - `REL-SEH-009`: `fdc4adf9f6ee62bc391513a869ab03e9332701a2c30bfbd1020dc8b9f0663b2c`;
  - `RLS-SEH-009`: `cf8c630c3223cd339deb0b4d78f8bfb7e41b3f398d657800f57b086aded936bd`.

Exact 0.5.0 `--version`, `doctor`, graph validation, and WO-REB-019 start
preflight passed in that bounded read-only view. Candidate validation was kept
separate from the predecessor claim.

## Contract change and independent matrix

Workflow policy advanced from `se-harness-workflow-v2` to
`se-harness-workflow-v3`. The v2 packaged contract at base commit
`f8d854ecccc0b0e892a655dcaebe6e41d04f5989` was 33,555 bytes with SHA-256
`e92adf4d81cf7147a76b20dd4c86ea90ca756b345caae50d29e4a80aec37f7b4`.
The canonical UTF-8/LF v3 contract is 38,052 bytes with SHA-256
`8b2e0d5da0f1e4e2e59a08e44233158c3a819c42a8d3ac1ec18ad3004891c675`.

The packaged `se_harness/workflow_contract.json` and managed-template
`docs/engineering/WORKFLOW.json` copies are byte-identical. Independent tests
decode every state row and compare all six properties against the approved
matrix rather than trusting a consumer-exported transition set.

Key rejected-history rows are:

| Family/state | Transitions | Authority | Reserves version | Transitionable | Visible | Adapter |
| --- | --- | --- | --- | --- | --- | --- |
| VREC `rejected` | none | no | no | no | yes | required |
| RLS `rejected` | none | no | no | no | yes | required |
| RLS `ready` | `released`, `rejected` | no | yes | yes | yes | none |
| RLS `released` | none | yes | yes | no | yes | none |

The seven compatibility rows are terminal and visible. Definition
`in_progress`, `verified`, and `released` preserve the prior active-authority
effect. Definition/work-order `ready` and `superseded` grant no authority. All
seven have `reserves_version=false` and `predecessor_adapter=none`.

## Consumer results

- `se_harness.workflow_contract` rejects wrong schemas, duplicate keys and
  targets, missing/extra fields or families, unknown targets, wrong Boolean
  types, inconsistent transitionability, hidden history, illegal reservations,
  oversized input, and non-UTF-8 input before exposing an index.
- `se_harness.workflow` derives planner edges and VREC/RLS authority from the
  immutable package index. The Cartesian edge/complement test accepts exactly
  declared edges; all seven compatibility rows and both rejected rows have no
  outgoing edge.
- `se_harness.provenance` derives definition/VREC authority and same-version RLS
  reservation from registry properties. Rejected history cannot serve as
  authority and cannot block a distinct same-version RLS.
- The standalone managed validator independently parses adjacent
  `WORKFLOW.json`, fails closed without importing candidate package code,
  exposes immutable semantic indexes, and derives per-family vocabulary,
  edges, authority, active-record behavior, and E010 version uniqueness from
  the same bytes.
- The historical migration scenario still reports the predecessor's refusal of
  rejected history, and its fixture is conformance-tested against the two
  `predecessor_adapter=required` rows. No production compatibility view was
  added or broadened.

## Rejected and same-version properties

The matrix exercised `rejected+ready`, `rejected+released`,
`rejected+rejected`, `ready+ready`, `ready+released`, and
`released+released` RLS pairs for one version. Only pairs containing two rows
whose registry entries set `reserves_version=true` emit the duplicate-version
error. Canonical rejected metadata remains required, rejected VREC/RLS rows
remain visible and terminal, and authority-sensitive consumers exclude them.

Historical release bytes remained unchanged:

- `REL-SEH-009`: `fdc4adf9f6ee62bc391513a869ab03e9332701a2c30bfbd1020dc8b9f0663b2c`;
- `RLS-SEH-009`: `cf8c630c3223cd339deb0b4d78f8bfb7e41b3f398d657800f57b086aded936bd`;
- `RLS-SEH-012`: `cb42507b5f5c103a5323a79bde82a0e9d7553b18cc6da23cbf06baae4ce7fdbd`.

## Local qualification

| Check | Result |
| --- | --- |
| Candidate complete graph | PASS, 687 artifacts, 0 errors, 50 pre-existing maintenance warnings |
| Focused lifecycle/workflow/bootstrap/migration/renumber/dashboard suite | PASS, 122 tests, 2 skipped |
| Full clean candidate-source suite | PASS, 471 tests, 7 skipped, Python 3.14.6 |
| Candidate-source identity | PASS, clean no-pip venv, no diagnostics |
| Release-distribution validation | PASS, one distribution-bearing record |
| Portable repository surface | PASS |
| Candidate CLI help/version | PASS, version 0.6.0 |
| Ephemeral package build | PASS, wheel and sdist built outside checkout with build 1.3.0, setuptools 84.0.0, wheel 0.48.0 |
| Wheel portable surface | PASS |
| Source/template/wheel/sdist contract parity | PASS, all six contract copies byte-identical |
| Candidate-package identity | PASS, isolated Python 3.11.9, no diagnostics |
| Installed disposable repository init/doctor/validate | PASS |
| Diff whitespace check | PASS |

The pre-final byte audit detected CRLF-smudged copies of the ten existing
tracked paths on the Windows worktree. All 20 approved changed paths were
normalized to canonical UTF-8/LF before the final full-suite run and package
build. The earlier CRLF-smudged package observation is not relied on by this
evidence. Source, template, wheel, and sdist now contain six byte-identical
copies of the 38,052-byte contract at SHA-256
`8b2e0d5da0f1e4e2e59a08e44233158c3a819c42a8d3ac1ec18ad3004891c675`.

The explicitly non-promotable ephemeral build products were retained outside
the checkout only:

- wheel SHA-256: `bc25eb6bb6eac87cf094f6c870e92d7d200c97f24b27575e4c640fdc2642a6a1`;
- sdist SHA-256: `a0ba6ccc03c3e631f86094316ded5215fd8775228b6280f449d4eb667d3aaf70`.

An initial full-suite run under the desktop's general interpreter produced
`RID018` because installed editable `se-harness 0.4.1` distribution metadata
points to a different checkout. This was retained as environment evidence, not
hidden or allowlisted. The same complete suite passed in
`../q-wo-reb-019-full`, a clean no-pip environment whose distribution lookup
correctly falls back to this candidate checkout.

Candidate-source `doctor` against the operational 0.5-managed root failed on
expected distribution/root drift. That result is boundary evidence and is not
represented as root health or candidate-graph failure.

## Non-mutation evidence and remaining work

Root managed evaluator files, `.engineering-harness.lock`, and
`.engineering-harness.toml` have no Git diff. Reference hashes are:

- root validator: `2d2ebaff0a08afd7801e1f9c6e39fd1e681956a0789a7e92dcf3b93b3f9d198d`;
- root `WORKFLOW.md`: `dc586ffd9bf477c3d112ed2735b878728a55eb97839451916b4ed04b4d1a504e`;
- lock: `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`;
- root configuration: `593d837d251a50156dd188bd180d9e4e9190ccdf0a7c72b5e7bcdce075053e57`.

Exact released-0.5 review preflight is recorded below. Hosted Windows/Linux
qualification, exact-candidate replay, candidate commit, and commit-bound
verification remain pending separate authorization.

## Exact released-0.5 review replay

The final replay used exact evaluator 0.5.0 in
`../q-wo-reb-019-review-view`. The view excluded only the same immutable
`REL-SEH-009` / `RLS-SEH-009` pair and retained their hashes above.

- `python -I -m se_harness --version`: PASS, `0.5.0`;
- exact predecessor `doctor`: PASS;
- exact predecessor graph: PASS, 685 artifacts, 0 errors, 49 maintenance
  warnings;
- exact predecessor WO-REB-019 review preflight: PASS;
- work order remained `in_progress` and no lifecycle or external action was
  performed.

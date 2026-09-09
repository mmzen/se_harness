```toml
artifact = "WO-HUP-018"
checkpoint = "handoff"
formal_snapshot_sha256 = "d3c5d10c69fed16b5e11b914ebc30a4f94cc5d642b0eb2e95edc2418ae226bac"
rebound_at = "2026-09-09T09:54:57Z"
```

# WO-HUP-018 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.17.0: lock schema 3, `tool_version
0.17.0`, archive `305c7cbc…` equal to the wheel `RLS-SEH-026` binds,
payload `dd48b16b…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (41 managed files, 10
updated, `RISK.template.md` added, replay 41 unchanged; forty-one lock
entries, none under `scripts/`). The two obligations wave 5 carried to this
adoption are discharged: the root configuration holds the five keys the tool
reads (`DST-CFG-015`) and the root workflow and the hash-marked ignore block
take the release's template (`DST-MWF-014`). The candidate moved to 0.18.0.
The 0.17.0 gate reads this graph with the numbers the 0.16.0 gate read: 0
errors, 46 warnings, 0 advisories; the Explorer generates identically twice.
The owner region, the developing note and `SPEC-IAR-012` state the new root;
no test needed an identity-aware edit. `WO-TCM-011` may start after this
merges.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.16.0` outside the
  checkout (`C:/Users/hok/se-harness-eval-0160`), installed from the wheel
  file whose digest equals `RLS-SEH-025`.
- Governor from the transaction onward: released `se-harness 0.17.0` outside
  the checkout (`C:/Users/hok/se-harness-eval-0170`), installed from the
  wheel file downloaded from the GitHub release and verified against
  `RLS-SEH-026` before install; every later reading, this packet and the
  handoff check included.
- Candidate: this checkout, an LF checkout (`core.autocrlf=input`) of `main`
  at `b172f42a`, branch `governance/hup-018-adopt-0-17-0`; the transaction
  commit is `d8ba7a23`; `pyproject.toml` reads 0.18.0 after `HUP-ADS-011`.
  The LF checkout was chosen so the transaction document's prior lock digest
  is the committed blob's, `69d0fb9f…`, and no line-ending deviation has to
  be recorded.

## Readings (VER-HUP-018)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced`, equal to `RLS-SEH-026`'s distribution table (`HUP-ADS-002`) |
| `upgrade .` plan | exact 0.17.0 | 41 files, 10 `update` (`.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, `.gitignore`, `ENGINEERING_HARNESS.md`, `QUALITY_GATES.json`, `QUALITY_GATES.md`, `TRACEABILITY.md`, `WORKFLOW.json`, `WORKFLOW.md`, `templates/README.md`), 1 `add` (`templates/RISK.template.md`), 30 unchanged, no `remove`/`adopt`/`customized`/`conflict`; equal to the rehearsal (`HUP-ADS-004`, `HUP-ADS-005`) |
| `upgrade . --apply --evidence-output …` | exact 0.17.0 | transaction complete; `WO-HUP-018-evaluator-upgrade.json` retained: prior lock `69d0fb9f82bb4306…` (the committed 0.16.0 LF blob), prior `tool_version 0.16.0`, target 0.17.0 with archive `305c7cbc…` and payload `dd48b16b…`, eleven plan actions, postconditions `lock_matches_target`, `no_op_replay`, no external action, no product release (`HUP-ADS-006`, `HUP-ADS-007`) |
| `upgrade .` replay | exact 0.17.0 | 41 files, 41 unchanged (`HUP-ADS-008`) |
| lock | exact 0.17.0 | `tool_version 0.17.0`, archive pair recorded, forty-one entries, none under `scripts/` (`HUP-ADS-008`) |
| root configuration | workstation | `tool_version`, `installed_at`, `project_name`, `required_for_verified_work`, `required_for_release`; SHA-256 `b17e1a31c8d14144d9a7f2084994f9f2bec52746918b775c3148aba219ce064a` (`HUP-ADS-014`, `DST-CFG-015`) |
| root workflow and ignore block | workstation | `engineering-harness.yml` equals the release's template with `SE_HARNESS_VERSION: "0.17.0"` substituted; the `.gitignore` block sits between `# se-harness:begin` and `# se-harness:end`; the owner lines `__pycache__/` and `*.py[cod]` the fragment duplicated are dropped (`HUP-ADS-015`, `DST-MWF-014`) |
| `validate --advisories` | exact 0.17.0 | 1,442 artifacts, 0 errors, 46 warnings (all `W013`, pre-existing location notes), 0 advisories (`HUP-ADS-009`) |
| `doctor` | exact 0.17.0 | 99 PASS, 0 FAIL, 46 `W013` location warnings on historical records (`HUP-ADS-009`) |
| `qualify released-root .` | exact 0.17.0 | PASS; `RR001` runtime matches the target root lock, `RR002` 99/99 managed checks, `RR003` artifacts 1,442 errors 0 warnings 46, `RR004` target state unchanged (`HUP-ADS-009`) |
| `inspect` | exact 0.17.0 | exit 0 (`HUP-ADS-009`) |
| `dashboard` twice | exact 0.17.0 | 1,727 resources, 1,725 outside the generation summary and manifest identical across both runs, combined digest `fe07c7d3826ac9e2…` (`HUP-ADS-010`) |
| review preflight `--work-order WO-HUP-018` | exact 0.17.0 | PASS (`HUP-ADS-009`) |
| `identity --role released-evaluator` | exact 0.17.0, Windows | `passed: true`, no diagnostic, with the evaluator environment as `--expected-root`, this checkout as `--checkout-root` and `--expected-version 0.17.0` (`HUP-ADS-001`, `HUP-ADS-002`) |
| `evaluator_facts derive` | candidate | `PRE008` with the candidate still at 0.17.0 (rehearsal, 2026-09-09); the 0.17.0 to 0.18.0 pair after `HUP-ADS-011`: `candidate_version 0.18.0`, `version 0.17.0`, payload `dd48b16b…` |
| in-tree `doctor` (candidate 0.18.0 on the 0.17.0 root) | candidate | three `differs from distribution` findings, the version-substitution skew of `.engineering-harness.toml`, `engineering-harness.yml` and `ENGINEERING_HARNESS.md` a leading candidate always reads; no `lock-extra` finding |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | section below (`HUP-ADS-017`) |

### The Windows suite

All three runs on this Windows 11 workstation (CPython 3.13.3, 8 workers,
LF checkouts):

| Run | Root | Result |
| --- | --- | --- |
| moved root, this branch at `1ed26780`, after `HUP-ADS-011` to `HUP-ADS-015` | exact 0.17.0 | 1,098 tests, 1 error, 23 skipped |
| same-commit control (`main` at `b172f42a`, a detached worktree) | exact 0.16.0 | 1,098 tests, 1 error, 23 skipped |
| rehearsal clone at `e855cc9a`, moved root, candidate 0.18.0, no edit | exact 0.17.0 | 1,098 tests, 3 failures, 1 error, 23 skipped |

The one error is the same name on both roots,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
the workstation baseline error every reading of this cycle carries (a
Windows `PermissionError` on a read-only temporary Git object during
teardown). The 23 skips are the platform set plus the complexity test that
runs only where radon is installed. The rehearsal's three failures were the
owner region's evaluator pin (`test_owner_region_directs_the_evaluator_outside_the_checkout`),
the developing note's candidate version
(`test_development_note_explains_standard_evaluator_and_candidate_planes`),
both rewritten by `HUP-ADS-012` and `HUP-ADS-013`, and one reading of the
repository's remote URL, which the throwaway clone answered with a local
path (`test_release_proof_fields_reach_the_summary_and_compact_topology`)
and this checkout answers with the GitHub URL. No test needed an
identity-aware edit under `HUP-ADS-016`.

## Owner content and the amendment record (HUP-ADS-011 to HUP-ADS-013)

- `pyproject.toml`, `se_harness/__init__.py`: 0.18.0.
- `AGENTS.md` owner region: the evaluator instruction reads
  `se-harness==0.17.0`; the statements that no `scripts/` path is managed
  stand (`HUP-ADS-012`).
- `docs/notes/developing-se-harness.md`: the identity paragraph names the
  0.18.0 candidate and the 0.17.0 root; the "Advancing the root evaluator"
  paragraph states 0.17.0 adopted by this work order from the wheel
  `RLS-SEH-026` binds, with the carried obligations named, and `WO-HUP-017`
  joins the list of earlier adoptions (`HUP-ADS-013`).
- `SPEC-IAR-012`: a dated amendment record states that the 0.17.0 root adds
  one managed path, `RISK.template.md`, which rule 6's templates clause
  already covers, the lock naming forty-one files (`HUP-ADS-013`).
- `ARCH-HUP-012` was amended by record on the packet branch, after the
  requirements were approved and before the start preflight, so that it
  addresses `REQ-HUP-035` and `REQ-HUP-036` and conforms to `SPEC-HUP-018`
  (`E016`, as for the two previous adoptions).

## Material non-effects

No product byte under `se_harness/` beyond `__init__.py`'s version; no
candidate template byte under `templates/`; no release, tag, publication,
Pages or maintenance-line change; the published 0.17.0 did not move.
`RLS-SEH-026` and `VREC-SEH-026` are unchanged. No decision artifact was
raised. `WO-TCM-011` was not started.

## Hosted lanes

At the edits head `1ed26780` (pull-request event of PR #427), three of four
lanes green before the evidence existed:

- Predecessor Evaluator Assessment 34336164445: plan phase
  `transition_required: true`, base `b172f42a` under 0.16.0 with canonical
  lock `69d0fb9f…`, target 0.17.0 with archive `305c7cbc…`, payload
  `dd48b16b…` and canonical lock `ac614b2b…`; exactly one transaction
  document, this work order's `WO-HUP-018-evaluator-upgrade.json`
  (`ca98bdba…`), and the trusted release `RLS-SEH-026` (tag `v0.17.0`)
  supplying the wheel; the exact target evaluator assessed the moved root
  (`RR001` to `RR004` pass) and the assessment made no checkout change
  (`HUP-ADS-019`).
- SE Harness Candidate Evidence 34336164436: source and package evidence
  (`CC001` to `CC004`, `CP001` and `CP002` pass, the package leg verified by
  the isolated released 0.17.0), the upgrade rehearsal 0.17.0 to 0.18.0 on
  Linux and Windows twice each with one `semantic_sha256` `d0fff1e4…`, the
  integration package built and verified on both platforms.
- Publication Rehearsal 34336164614: candidate and release-record modes
  both `success`.
- Engineering Harness 34336164312: the lane installed `se-harness==0.17.0`
  from the transaction's lock and ran the 0.17.0 gate; it stopped at the
  handoff step on `QGP-G4I-EVIDENCE`, no readable evidence for this work
  order yet, the expected reading before this packet existed.

The lanes at the evidence head, the completion head and the record head are
checked the same way before each act and recorded in the pull request.

## Disclosures

1. The rehearsal's first `--apply` was refused because its evidence path
   resolved outside the repository (`upgrade evidence path must be
   repository-relative`); the human output showed the plan and no
   transaction, and the refusal was read from the JSON form. The real
   transaction used the repository-relative path the work order names.
   `SPEC-HUP-018`'s failure table records the diagnostic.
2. The rehearsal clone's `scripts/run_tests.py --scale full` refused to
   start without an explicit `--workers` value; every suite reading here was
   taken with `--workers 8`.
3. The two root `.gitignore` owner lines dropped were exact duplicates of
   lines inside the managed fragment; `/target/` stays because it is broader
   than the fragment's `/target/harness-dashboard/`.

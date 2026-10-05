+++
id = "VER-HUP-025"
type = "verification"
title = "Verify repository adoption of public 0.22.1"
status = "approved"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[relations]
verifies = ["REQ-REB-027", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T10:40:00Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve package, verification and review PR\" to the exact WO-HUP-030 / VER-HUP-025 review: public evaluator 0.22.1 adoption, unpublished source 0.22.2, named CI/documentation/test updates, required commit-bound verification and ordinary review pushes/draft PR from codex/adopt-0-22-1 to mmzen/se_harness:main, including the later recorded verification decision. Human verification acceptance, merge, host-plugin updates and HAG contract amendment remain separate. Reviewed bytes matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 28dcc7f6f08e703252a9c35202531538495801875b7417d2a1903f97efe8a347."
+++

# Verify repository adoption of public 0.22.1

## Independence

Expected values come from released RLS-SEH-033 and independently retained public
archives at trusted base `00708eb1000020cf4b1672ffe9bfc684b0c6d51c`.
The evaluator wheel SHA-256 is
`cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`;
its payload SHA-256 is
`0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff`.
REQ-REB-027 / SPEC-REB-012 cover ordinary upgrades; REQ-IAR-031 /
SPEC-IAR-016 cover external resources and owner preservation. Candidate source
does not supply the governor. The human accepts the final committed result.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-REB-027 | test, inspection | Public identity, preview/apply, transaction, doctor and released-root qualification | Selected 0.22.1 archive and payload match RLS-SEH-033; the installer binds old and new locks; post-upgrade checks pass. |
| REQ-IAR-031 | inspection, test | Full diff, owner-file hashes, resource query and repeat preview | Installer changes only the two selection files; schema 5, external layout, integrations and AGENTS.md are preserved; no copied instructions return; repeat is unchanged. |
| REQ-IAR-031 | analysis, test | CI/source facts, current guides, existing regression tests and predecessor assessment | CI selects 0.22.1 using the existing checked-wheel route; both source versions are 0.22.2; no PRE008; current claims match actual observations; historical artifacts/evidence are unchanged. |

## Acceptance scenarios

1. Compare the exact released wheel and installed identity with the approved
   values. Run the target's `upgrade --help`, `doctor` and read-only `upgrade`
   outside the checkout. Before adoption, the expected version mismatch is not
   a successful doctor check. Any other refusal needs resolution.
2. Recheck the reviewed plan, then apply with the work order's exact transaction
   destination. Run target `identity`, `doctor`, `validate`, and
   `qualify released-root`. Confirm schema 5, the external layout and every
   retained integration. A repeat preview must have no changed paths.
3. Compare AGENTS.md and all pre-existing formal artifacts/evidence against the
   trusted base. Only the explicitly selected current documentation may change.
   Preserve SPEC-HAG-003, VER-HAG-001, WO-HAG-001 and DEC-HAG-001 byte-for-byte.
   No hosted criterion, decision or approved pin changes in this adoption.
4. Run `python -m repository_tools.evaluator_facts derive --repository REPO --json`.
   Require released evaluator 0.22.1 and development source 0.22.2. Run the
   existing governor-transition assessment against the trusted base and exact
   adoption commit, plus the real upgrade rehearsal used by CI.
5. Run existing focused suites: `tests.test_ci_pipeline`,
   `tests.test_governor_transition`, `tests.test_predecessor_bootstrap_retirement`,
   `tests.test_progressive_documentation`, `tests.test_public_onboarding` and
   `tests.plugin_integration.package_assembly.test_refresh_guidance`.
   Run `python scripts/run_tests.py --scale full`,
   `python scripts/validate_release_distributions.py --root .` and CLI help.
   Retain actual skips and failures. Only the work order's named current-public
   test expectations may change; no broader source/test correction is implied.
6. Check the changed current documentation against actual publication receipts
   and adoption state. Keep dated prior-release observations and the accepted
   Codex Windows desktop omission distinct. Check the edited links.
7. Resolve target resources and reactivate this exact checkout after apply.
   Confirm 0.22.1 and available instructions. Direct helper/resource calls are
   selection checks, not native startup, compaction or desktop tests.
8. Pass scope, handoff and commit-bound capture checks. Publish the exact ready
   record and evidence to the review PR before requesting human verification.
   Required CI, including predecessor, candidate package and Windows/Linux
   upgrade/integration checks, must pass before merge.

## Evidence retention

Retain commands, working directories, identities, actual exits and failures under
`evidence/WO-HUP-030/`. The canonical installer transaction is
`evidence/WO-HUP-030-evaluator-upgrade.json`. Retain the actual verification
record and its fixed evaluator companion at the paths returned by capture.
Planning rehearsals do not replace checks on the final adoption candidate.

## Residual uncertainty

This verifies repository adoption only. Host plugin installation, native Claude
and Codex desktop tests, hosted service scenarios, HAG pin amendments, release
publication and provider-setting changes are excluded. Keep prior host-test
omissions and RISK-HAG-001 unchanged. Existing authority must separately cover
any later integration into the unfinished HAG branch.

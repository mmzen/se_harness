+++
id = "VER-HUP-005"
type = "verification"
title = "Verify repository adoption of public 0.22.0"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-REB-027", "REQ-IAR-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T07:09:21Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" to the reviewed WO-HUP-028 and VER-HUP-005 package, including required commit-bound verification, repository adoption of 0.22.0, unpublished source 0.22.1 and review branch push/PR. Reviewed file SHA-256 c396f2cfd3a93731f1c9297180fa0aa39eca473dafad39cf0effeae366f67728. Human verification acceptance, merge, host updates, provider configuration and new release/publication remain separate."
+++

# Verify repository adoption of public 0.22.0

## Independence

Expected identities come from released RLS-SEH-032 and its public distribution,
not from the edited repository. REQ-REB-027 / SPEC-REB-012 define the ordinary
upgrade boundary; REQ-IAR-031 / SPEC-IAR-016 define external resources and owner
preservation. Reuse their approved architectures. The assurance owner assesses
the final committed result independently of the agent that prepares it.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-REB-027 | Target identity; preview/apply; canonical upgrade transaction; doctor and released-root qualification | Public 0.22.0 version, wheel and payload match RLS-SEH-032; transaction binds the exact old and new lock; no hand-edited selection; post-upgrade checks pass. |
| REQ-IAR-031 | Complete Git diff; before/after protected-file digests; resource lookup; repeat preview | Installer changes only configuration and lock; external layout/integrations and AGENTS.md bytes are preserved; no copied instruction/template files appear; repeat is unchanged. |
| REQ-IAR-031 | CI/source derivation; owner guidance review; existing tests; predecessor assessment | CI selects exact 0.22.0 through the retained hash-checked wheel-file route; both source versions are 0.22.1; no PRE008; current guidance and links match actual state; historical evidence is unchanged. |

## Checks

1. Before apply, compare the exact preview and target digests with the approved
   scope. Read the released record from the trusted pre-adoption base. Preserve
   the old environment and owner file hashes. No guide retirement occurs, so
   the migration-only native-delivery receipt is not required for this upgrade.
2. Apply with the declared `--evidence-output`. Run target `identity`, `doctor`,
   `validate` and `qualify released-root` using its absolute Python with `-I`,
   from outside the checkout. Inspect the transaction and repeated unchanged preview.
3. Run `python -m repository_tools.evaluator_facts derive --repository REPO --json`.
   Require evaluator 0.22.0 and candidate 0.22.1 with matching published digests.
   Run the existing predecessor/governor-transition assessment against the trusted
   base and exact committed target, and the real upgrade rehearsal used by CI.
4. Run existing focused suites: `tests.test_ci_pipeline`,
   `tests.test_governor_transition`, `tests.test_predecessor_bootstrap_retirement`,
   `tests.test_progressive_documentation`, `tests.test_public_onboarding` and
   `tests.plugin_integration.package_assembly.test_refresh_guidance`.
   Preserve all acceptance thresholds; this scope contains no test source edit.
5. Run `python scripts/run_tests.py --scale full`,
   `python scripts/validate_release_distributions.py --root .` and the CLI help
   smoke check. Required hosted source/package, predecessor, Linux/Windows
   upgrade and integration checks must pass before merge. Retain actual skips.
6. Query the target entry/resources and reactivate the exact checkout for the
   existing Codex session after successful apply. Confirm release 0.22.0 and
   available selected instructions. Direct helper calls establish resource and
   selection correctness, not new native startup, compaction or desktop evidence.
7. Pass the selected evaluator's scope, preflight, handoff and commit-bound
   capture gates. Prepare VREC-HUP-027 at the exact clean candidate; publish its
   review branch/PR before requesting the separate human verification decision.

## Evidence and limits

Retain concise observed results and actual commands under evidence/WO-HUP-028/;
compress raw logs where useful. The canonical transaction and VREC companion
have the exact separate destinations declared by WO-HUP-028. Do not overwrite
frozen historical evidence or treat a rehearsal as the actual adoption.

The planning rehearsal and initial failed invocations remain visible. Run final
checks against the real adopted candidate after approval; prototype checks do
not substitute for candidate assurance. Claude Code and Codex Windows desktop
remain unverified by this work. No host authentication refresh is required for
these repository/CLI checks. No provider setting is activated by adoption alone.

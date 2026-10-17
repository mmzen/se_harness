# Repository adoption of 0.23.0 — verification assessment

WO-HUP-031 adopts the exact public evaluator under VER-HUP-026. Human approval
authorizes implementation and review publication; result acceptance remains pending.
Implementation commit: `ee0f723112bb09dc4c65edebaadd1a4e66c57ed1`. Trusted base: `ed29d435f37b5c2c8b81b1e1375d504edc98787a`.

| Requirement / check | Actual result |
| --- | --- |
| REQ-REB-027: public identity | Pass. Selected wheel and payload match RLS-SEH-034; isolated identity, doctor, validation and released-root checks pass. |
| REQ-IAR-031: bounded installer | Pass. Only configuration and lock change. Repeat upgrade is unchanged; schema 5, external resources and integrations remain selected. |
| Owner and history preservation | Pass. All 14,625 checked pre-existing owner, formal, evidence and plugin/package files match their original Git blobs. Four approved current indexes are excluded explicitly. |
| CI/source boundary | Pass. CI and repository select 0.23.0; unpublished source is 0.23.1. Version derivation and committed governor-transition assessment pass. |
| Real upgrade rehearsal | Pass twice. Disposable 0.23.0-to-0.23.1 runs have identical semantic results. The local test wheel is not promotable or a repository governor. |
| Regression | Final clean-commit full suite: 1,346 tests, 24 skips, exit 0. All 47 affected guidance tests pass after correction. Distribution checks and CLI help pass. |
| Guidance | Current public claims use independent release/observation inputs. All changed documentation links resolve. Published snapshots and accepted limits retain their bytes. |
| Session | Activation and resource lookup return the selected 0.23.0 instructions. This is not native startup/compaction or desktop qualification. |
| Handoff/candidate | Subsequent generated handoff and capture records establish completion and the exact verification candidate. |
| Hosted CI | Pending publication; required checks must pass before merge. |

## Failures and corrections

The first focused run reported 16 errors in the refresh-guidance helper. Its old
receipt layout expected an inline marketplace proof; the 0.23.0 receipt binds a
separate proof by path and SHA-256. The corrected helper follows that binding and
rejects missing bindings and changed proof bytes. Existing wrong-version, public-ref,
tree, digest, contradictory-claim and link rejection checks remain in place.

The first changed-link check found the old hosted-client heading anchor after the
heading was updated. The correction restores the historical anchor and uses the
current heading for the current link. Final changed-link review passes.

The first full run passed while the guidance correction was being completed.
The final full run was repeated on the clean committed implementation; only that
stable run supplies the final full-suite claim. Both runs and the failed focused
run remain in commands.zip. Earlier preparation sandbox failures remain in
preparation-checks.zip. No failed or skipped check is relabeled as a pass.

## Review and limits

This change reuses the installer, CI pipeline and existing tests. Product source
changes only its version fields. The test uses retained public evidence, not
agreement between mutable README strings. The private service remains on 0.22.1
and Git remains authoritative. No host-plugin, provider, tag, release, deployment
or new live-host change was performed.

R23-NATIVE-010/011 remain open under DEC-RLS-010 / RISK-RLS-008. Codex Windows
desktop remains unverified under DEC-RLS-011 / RISK-RLS-009. Adoption adds no waiver.
Human verification and merge remain separate. The existing grant covers the draft
review PR and later verification-decision push to codex/adopt-0-23-0 targeting main.

See [bound results](results.json), [actual commands](commands.zip), the
[approval review](review.md), and the canonical installer transaction
[WO-HUP-031-evaluator-upgrade.json](../WO-HUP-031-evaluator-upgrade.json).

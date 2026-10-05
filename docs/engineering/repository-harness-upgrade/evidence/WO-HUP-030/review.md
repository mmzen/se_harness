# Review repository adoption of 0.22.1

WO-HUP-030 adopts the exact public evaluator released under RLS-SEH-033.
VER-HUP-025 defines this assessment. Implementation approval does not accept
the result; the prepared VREC and review PR provide the separate human decision.

## Result

- Repository selection and CI now use released **0.22.1**. The installed wheel
  and payload match the approved public identities.
- The installer changed only the configuration and lock. Schema 5, external
  resources and retained integrations remain selected. Repeat upgrade is unchanged.
- Development source is **0.22.2**, unpublished. Version derivation passes
  without PRE008. No new release or host-plugin installation was performed.
- Current guides report actual 0.22.1 / plugin 0.2.6 delivery. Historical records
  and published snapshots keep their bytes and meaning.

## Assessment against VER-HUP-025

| Criterion | Observed result | Retained evidence |
| --- | --- | --- |
| Exact public evaluator | Pass: 0.22.1 wheel and payload match RLS-SEH-033; isolated released identity passes | commands.zip: target-identity-complete.json, adoption-root.json |
| Bounded upgrade and repeat | Pass: two selection-file updates, doctor and root qualification pass; repeat unchanged | Canonical transaction ../WO-HUP-030-evaluator-upgrade.json; commands.zip: adoption-apply.json, adoption-repeat.json |
| Owner and historical preservation | Pass: all 13,242 checked pre-existing files match their original Git blobs; four named current indexes are explicitly excluded | commands.zip: preservation.json |
| CI and development boundary | Pass: governor 0.22.1/source 0.22.2; predecessor assessment passes at the implementation commit | commands.zip: evaluator-facts.json, governor-transition.json |
| Real CI upgrade rehearsal | Pass twice: independent disposable 0.22.1-to-0.22.2 transactions have equal semantic digests | commands.zip: upgrade-corrected-1/ and upgrade-corrected-2/ |
| Regression and distribution | Full suite: 1,293 tests, 23 reported skips, exit 0. Focused checks pass after the corrections below; 23 release-bearing records pass distribution validation; CLI help passes | commands.zip: full-source-corrected.json, focused-tests.json, focused-readme-final.json, distribution-check.json, cli-smoke.json |
| Current guidance | Public claims use independent RLS-SEH-033 and WO-RLS-042 observations. Negative version, digest, public-ref, tree and premature-claim cases remain checked | Test diff and changed-links.json in commands.zip |
| Session selection | Pass: activation and resources return the selected 0.22.1 entry | commands.zip: adoption-activation.json, adopted-entry.json |
| Handoff and exact candidate | Recorded by the generated handoff, lifecycle archive and subsequent VREC | handoff.json, WO-HUP-030-handoff.md, lifecycle.zip, VREC |
| Hosted CI | Pending review publication; required checks must pass before merge | Current PR checks |

## Failures and recovery

The first README revision exceeded its existing 650-word limit; the second was
one word over. The final wording passes without changing the limit. The first
full suite failed the dashboard repository-URL assertion because this local
clone's origin was another filesystem checkout. Origin now names the exact
mmzen/se_harness GitHub repository. The affected test and full suite pass.

The first real upgrade rehearsal failed while Git indexed long Windows scratch
paths. A shorter temporary location and process-local core.longpaths support
resolved that environment failure. Both corrected runs pass; no global Git
setting or product behavior was changed. The initial identity invocation lacked
required arguments, and the staged whitespace check found an extra final blank
line. Corrected commands passed. Original outputs remain in commands.zip.

The broad link check initially treated an existing directory link as a missing
file. The check now accepts existing directories without a heading fragment;
all file and heading checks remain active. No repository link needed changing.

Earlier draft/preparation invocation failures and the pre-adoption version
mismatch remain in the same archive. They are not successful qualification.

## Diff review and limits

This reuses the installer, CI workflow and existing tests. It adds no runtime
mechanism or dependency. The only product-source changes are the two version
fields. The regression uses the existing current-public receipt format and
checks public ref identity against the qualified tree, rather than treating a
staged package as proof of publication.

AGENTS.md and the HAG definitions, work order, decision and evidence retain
their original bytes. SPEC-HAG-003 / VER-HAG-001 still pin 0.22.0. Their amendment
and recording mmzen's known extend-evaluator choice need separate bounded work.
This adoption supplies no hosted-service verification or permission to resume
dependent HAG execution.

Direct activation is a selection check, not a native startup/compaction test.
Codex Windows desktop remains unverified under the prior accepted release-only
DEC-RLS-009 / RISK-RLS-007. No authentication, host-plugin, provider, tag,
marketplace or release changes were made. Human verification and merge remain
separate. The existing grant covers publication of this review and the later
recorded verification decision to codex/adopt-0-22-1 targeting main.

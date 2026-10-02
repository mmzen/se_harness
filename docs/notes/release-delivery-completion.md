# Complete a release delivery

Use this procedure for newly planned SE Harness deliveries. A **surface** is
one public package, route or instruction set that users need. The five surfaces
are the evaluator, marketplace, current documentation, demonstration and release
markers. Account for all five, including those that remain unchanged.

Formal release authorization, evaluator publication and complete delivery are
different results. A released RLS and a green evaluator publication run do not
establish that the marketplace or current instructions are ready. Historical
RLS records and their evidence keep their original meaning.

This is repository-owned operating guidance under
[SPEC-RLO-006](../engineering/release-orchestration/specifications/SPEC-RLO-006.md).
It grants no approval, publication right or lifecycle transition. Use the
selected released evaluator and its procedures for those decisions.

## Prepare the delivery plan

**Responsible:** The release operator prepares the plan. The authorized human
release owner reviews its scope with the governing release package.

**Inputs:** Accepted release scope, selected committed source, exact evaluator
release identity, public destinations and the work orders covering delivery.

**Output:** One reviewed `plan.json` in the selected work's durable evidence
directory. This supporting file references formal authority; it is not a new
formal artifact or a replacement for a release contract.

1. Select the release contract and RLS. Read their identities and governing
   evidence. Do not infer the released evaluator version from development source.
2. Give each surface a destination, owner, governing work reference, next action
   and disposition: `update`, `unchanged` or `deferred`.
3. Record expected identities from the selected authoritative inputs. The plugin
   version is independent of the evaluator version. The plan must identify the
   selected source commit and claimed hosts for the marketplace.
4. For an unchanged surface, retain its existing identity and a reviewed
   compatibility explanation for this delivery. For a deferral, retain the human
   decision reference, reason, owner, follow-up work and revisit trigger.
5. Record the reviewer's identity and decision reference. If the plan conflicts
   with accepted scope, resolve that conflict through the existing decision
   procedure before acting.

A package digest or public revision that cannot yet exist is `null`, not a
guessed value. It remains pending. After the matching package is qualified or
publication commit is prepared, fill the expected identity from that reviewed
input. Do not copy an unexpected public result into the expected value to make
the check pass. Changed scope or identity needs the applicable review.

Before a wheel binding and RLS ID exist, retain a preparation plan with those
fields explicitly pending. It is not yet a valid completion-check input: the
current checker requires non-empty `release.record` and a real
`release.wheel_sha256`. After those inputs exist, retain a new bound plan version
with their actual values. Surface `expected` fields may still be `null`; those
pending values prevent completion. Preserve the preparation plan as reviewed
scope. Do not insert a placeholder digest or a previous release's binding.

The final observations bind the **complete byte SHA-256** of the current plan.
After a plan revision, reassess applicability before rebinding retained evidence.
Do not change a digest simply to suppress a mismatch.

## Perform and retain each handoff

The operator keeps pending work, its owner and next action in the plan. Each
stage below produces retained evidence. A command completing does not supply
the human decision required by another stage.

| Stage | Responsible actor and action | Output used by the next stage |
| --- | --- | --- |
| Evaluator release | Release operator follows the existing [release sequence](developing-se-harness.md#release-sequences). The authorized human makes release and external-action decisions. | Released RLS, publisher result and independently observed public wheel with its exact digest. |
| Plugin assembly | Operator selects the committed plugin source and the published evaluator wheel, then runs the existing marketplace builder below. | New distribution tree, package identities, inventories, archives and independent builder-check result. |
| Package qualification | Operator follows the selected work's verification contract and retains tests of the exact package and documented routes. The authorized human accepts the required VREC. | Accepted candidate and its bounded qualification evidence, including host versions and observed limits. |
| Marketplace publication | Operator obtains authority for the exact publication commit and destination, then follows the [publication procedure](plugin-marketplace-publication.md#check-and-deliver). | Public ref resolved to an immutable commit and retained publication readback. |
| Public observation | Operator uses disposable profiles to install and update from that actual public destination on each claimed host. | Installed-content digests, evaluator identity, starting version/source for updates, host versions, commands, results and observation times. |
| Current instructions | Operator compares version, availability and support claims against those identities and observations. Check source links in the source tree and package-relative links in the assembled tree. | Retained claims review and link-check results for the exact documentation commit. |
| Demonstration and markers | Operator observes the deployed demonstration and actual `latest`/`last` targets under their existing procedures and separate authority. | Deployment provenance, marker readback and authorization references. |
| Closeout | Operator runs the local check below and presents the actual report. | Overall completion or the outstanding items with owners and next actions. |

The evaluator publication can finish before plugin assembly: assembly needs the
independently published wheel. Keep that dependent work pending; do not make the
evaluator publisher wait for its own downstream package.

For plugin assembly, run these existing repository commands from the source
checkout. Replace every uppercase placeholder with the selected full commit,
absolute path or digest. `EVALUATOR_PYTHON` is the absolute Python executable of
the released evaluator outside the checkout. `NEW_OUTPUT` is a fresh directory
outside the checkout. The release revision contains the selected released RLS.

```text
python scripts/build_plugin_marketplace.py build --repository . --revision SOURCE_COMMIT --release-revision RELEASE_COMMIT --release-record RLS_PATH --expected-wheel-sha256 WHEEL_SHA256 --wheel "PUBLIC_WHEEL" --evaluator-python "EVALUATOR_PYTHON" --output-directory "NEW_OUTPUT"
python scripts/build_plugin_marketplace.py check --repository . --revision SOURCE_COMMIT --release-revision RELEASE_COMMIT --release-record RLS_PATH --expected-wheel-sha256 WHEEL_SHA256 --wheel "PUBLIC_WHEEL" --evaluator-python "EVALUATOR_PYTHON" --output-directory "NEW_OUTPUT"
```

The [publication guide](plugin-marketplace-publication.md#assemble-committed-inputs)
selects identities from the new released record and committed plugin source.
Its previous-publication receipt is historical evidence, not an input selection
for the next delivery. The [0.20.0 package](../engineering/release-0-20-0/README.md)
assigns plugin 0.2.2 assembly and publication to WO-PLG-030, and public
fresh/update observation and current claims to WO-PLG-031. Its
[public delivery evidence](../engineering/release-0-20-0/evidence/WO-PLG-031/README.md)
records the published 0.2.2/0.20.0 identities and keeps final documentation
integration and readback pending. Earlier plan versions remain historical.

Use the host commands qualified for the selected package. A local marketplace
directory or an existing cache is not the public Git route. Retain the public
repository URL, branch and resolved commit. Compare installed content, not just
the plugin version label. Do not switch the operator's real profiles implicitly.

If interrupted, inspect actual state before resuming. Retain failures alongside
later results. Preserve immutable tags and published bytes; do not force a
marketplace branch over conflicting work. Moving release markers requires its
separate exact human authorization.

## Plan format

The command reads UTF-8 JSON. Its current plan schema is
`se-harness-delivery-plan/v1`. Arrays of surfaces contain exactly one entry per
surface ID. Unknown schema versions, duplicate JSON keys, duplicate surface IDs
and missing required fields are invalid.

| Field | Content |
| --- | --- |
| `schema` | `se-harness-delivery-plan/v1` |
| `release` | Object with `contract`, `record`, `version` and lowercase `wheel_sha256`. |
| `review` | Object with non-empty `by` and `reference` for the actual scope review. |
| `surfaces` | Array with `evaluator`, `marketplace`, `documentation`, `demonstration` and `release_markers`. |

Every surface contains `id`, `owner`, `destination`, `work_reference`,
`next_action`, `disposition`, `expected` and `required_observations`. Text fields
are non-empty. `expected` is an object of named identity values: non-empty
strings or `null` for a still-pending value. Digest values use lowercase SHA-256.
The command compares all declared identity values exactly.

| Surface | Minimum `expected` keys | Minimum observations for `update` |
| --- | --- | --- |
| `evaluator` | `record`, `version`, `wheel_sha256` | `publisher`, `public_install` |
| `marketplace` | `plugin_version`, `source_commit`, `evaluator_version`, `wheel_sha256`, `public_revision`, plus `HOST_content_sha256` for each claimed host | `assembly`, `qualification`, `public_ref`, plus the route observations below |
| `documentation` | `commit` | `claims_review`, `links` |
| `demonstration` | `governance_commit` | `deployment` |
| `release_markers` | `latest` (release tag), `last` (target commit) | `authorization`, `readback` |

Include additional identities needed by the selected release, such as the sdist
digest, candidate commit and documentation deployment commit. The minimum table
does not reduce obligations in the governing release or verification contract.
The evaluator and updated marketplace must agree with `release` on the selected
evaluator version and wheel digest.

The marketplace also contains `hosts`, a non-empty array drawn from `codex` and
`claude-code`. For example, the Codex content field is `codex_content_sha256`.
Its destination is an HTTPS repository URL with a `#branch` fragment, no query
and no embedded credentials. Commit identities use full lowercase 40-character
Git commit IDs; a branch name is not an immutable revision.
Use one recorded installed-content inventory algorithm for qualification and
public comparison. Retain its method and inventory in the qualification evidence.

For `unchanged`, `required_observations` includes `readback` and `compatibility`.
Add `compatibility: {"reason": "...", "review_reference": "..."}`. An unchanged
older plugin may bundle an older evaluator only when that exact combination has
the retained compatibility review.

For `deferred`, require `deferral` evidence and add a `deferral` object with
`reason`, `decision_reference`, `follow_up` and `revisit`. Deferral always leaves
overall delivery incomplete. It neither satisfies a delivery obligation nor
waives a required harness gate.

## Observation format

The observations schema is `se-harness-delivery-observations/v1`:

| Field | Content |
| --- | --- |
| `schema` | `se-harness-delivery-observations/v1` |
| `plan_sha256` | SHA-256 of the exact reviewed plan bytes used for these observations. |
| `observed_at` | ISO 8601 timestamp with timezone, identifying the observation set. |
| `release` | Object with `record`, observed `status`, `source`, `observed_at` and `evidence`. Retain the RLS readback and its immutable governance source. |
| `surfaces` | Array of observed surfaces. A missing surface is incomplete, not implicitly satisfied. |

Each observed surface has `id`, `status` (`pass`, `failed` or `pending`),
`observed_at`, `source`, `identity` and `evidence`. Its `source` equals the plan's
exact destination. Its `identity` contains the observed values for the expected
keys. `evidence` maps each required observation name to a non-empty evidence
array. An evidence array has this form:

```json
[{"path": "checks/public-install.json", "sha256": "lowercase-64-character-digest"}]
```

The path is relative to the supplied evidence root. Use forward slashes and
no empty, `.` or `..` components, drive prefixes or absolute paths. The command
refuses paths and symlinks that resolve outside that root. Each JSON input is
limited to 2 MiB; each referenced evidence file is limited to 64 MiB. Retain
bounded reports and link larger raw logs using the repository's evidence policy.

For an updated marketplace, add `routes` with exactly one observation for each
claimed host and each `kind`: `fresh` and `update`. Each route contains:

- `host`, `host_version`, `kind`, `status` and `observed_at`;
- `source` equal to the public destination, including its branch;
- `revision`, `plugin_version`, `content_sha256`, `evaluator_version` and
  `wheel_sha256`, matching the reviewed plan;
- a non-empty `evidence` array;
- for `update`, non-empty `starting_version` and `starting_source`.

Retain failed commands and observed limitations. A bare status field does not
replace evidence. The retained reviews must inspect source manifests, assembly
inventories, bundled wheel identity, current claims and links. The reporting
command checks bindings and declared observations; it does not perform those
assessments on the reviewer's behalf.

## Run the completion check

Run from the source checkout with Python 3.11 or later. Replace `PLAN`,
`OBSERVATIONS` and `EVIDENCE_ROOT` with actual absolute paths:

```text
python scripts/check_release_delivery.py --plan "PLAN" --observations "OBSERVATIONS" --evidence-root "EVIDENCE_ROOT" --json
```

With `--json`, JSON is written to standard output and the human report to
standard error. Without it, the human report is written to standard output.
The command writes no files. The caller retains both streams and the exit code
in the work's evidence directory.

| Exit code | Meaning | Next action |
| --- | --- | --- |
| `0` | Every surface is satisfied, the retained RLS observation is released, and no deferral remains. | Present the observed completion with its evidence and limits. |
| `1` | Inputs are structurally valid, but delivery is incomplete. | Follow the named outstanding item and owner; preserve passed stages. |
| `2` | Inputs are invalid or unreadable. | Correct the named input, then rerun. No completion is established. |

The result schema is `se-harness-delivery-result/v1`. It separates
`formal_release`, `evaluator_publication` and overall `status`, and retains the
plan digest, observation times, per-surface findings, owners and next actions.
An unchanged surface can pass with its identity and compatibility evidence.
Missing evidence, mismatches, pending work and deferrals prevent completion.

This report is derived operational evidence. It does not independently run
native-host tests, authenticate a human review or establish live public state
after the recorded observations. It grants no lifecycle or external authority.

## Executable synthetic example

The [complete fixture](../../tests/fixtures/release_delivery/complete/) contains
a plan, observations and one clearly marked synthetic evidence file. Its
versions, commits, hashes, people and public URLs are examples only. In
particular, plugin 0.2.1 in this fixture is not a version decision or publication
claim. The plan and evidence file use single lines without a final newline so
Git newline conversion cannot change their example byte hashes.

```text
python scripts/check_release_delivery.py --plan tests/fixtures/release_delivery/complete/plan.json --observations tests/fixtures/release_delivery/complete/observations.json --evidence-root tests/fixtures/release_delivery/complete --json
python -m unittest discover -s tests -p "test_release_delivery.py"
```

The first command returns `complete` and exit code zero for synthetic inputs.
The tests include the actual failure pattern: evaluator publication passes while
the required marketplace update remains absent. That case returns incomplete
and retains the marketplace owner and next action. Live public qualification
belongs to the subsequent marketplace work and its verification contract.

## Current 0.21.0 delivery

The [release package](../engineering/release-0-21-0/README.md) records released
RLS-SEH-031 and separately published plugin 0.2.4 at
`7e366438165a40a14783bac650a2887e7ec8bc75`. VREC-PLG-030 verifies local package
qualification. WO-RLS-033 retains passing public fresh/update package and setup
observations, current documentation corrections and native test boundaries.
Codex CLI session checks pass; DEC-RLS-003 accepts missing Claude tests, which
remain unverified. DEC-RLS-004 accepts the desktop omission for WO-RLS-033.
Overall delivery remains incomplete. The existing 0.20.1 receipts stay intact.

## Historical 0.20.1 delivery

The [release package](../engineering/release-0-20-1/README.md) selects plugin
0.2.3 with evaluator 0.20.1. WO-RLS-028 qualified the package, accepted in
VREC-PLG-027. Its separately authorized marketplace publication is observed at
`556d0faf83c32fd188409c5ba191552fad1522e1`.
[WO-RLS-029 evidence](../engineering/release-0-20-1/evidence/WO-RLS-029/README.md)
records public installation/update checks and current documentation review.
Read its latest closeout result for remaining surfaces. Publication, public
documentation integration, latest/last promotion and repository adoption are
separate actions; none is inferred from a passing package test.

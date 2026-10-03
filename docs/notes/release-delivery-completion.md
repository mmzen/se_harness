# Complete a release delivery

Use this procedure for SE Harness deliveries. A **surface** is
one public package, route or instruction set that users need. The five surfaces
are the evaluator, marketplace, current documentation, demonstration and release
markers. Account for all five, including those that remain unchanged.

Formal release authorization, evaluator publication and complete delivery are
different results. A released RLS and a green evaluator publication run do not
establish that the marketplace or current instructions are ready. Historical
RLS records and their evidence keep their original meaning.

This is repository-owned operating guidance under
[SPEC-RLO-006](../engineering/release-orchestration/specifications/SPEC-RLO-006.md)
and the explicitly selected complete-release route in
[SPEC-RLO-007](../engineering/release-orchestration/specifications/SPEC-RLO-007.md).
It grants no approval, publication right or lifecycle transition. Use the
selected released evaluator and its procedures for those decisions.

The [approved 0.22.0 / 0.2.5 release](../engineering/release-0-22-0/README.md)
has published the supporting product. WO-RLS-034 owns evaluator preparation;
WO-RLS-035/036 own marketplace publication and public closeout. This rollout
uses selected evaluator 0.21.0 and the existing delivery route. Subsequent
adoption and the reviewed provider configuration activate the new route below.

## One approval for the complete release

**Availability:** Evaluator 0.22.0 and plugin 0.2.5 contain this route. This
repository still selects 0.21.0, so the route is not active here. Adopt the
supporting release and apply the separately reviewed provider configuration
before offering this route as ready. Existing releases keep their original decisions and procedures.

**Input:** A verified candidate, exact evaluator distributions, both qualified
plugin packages, documentation, demonstration inputs and operational readiness.

**Output:** One human decision covering the frozen delivery plan. The agent carries
out its listed actions and retains a report of all five surfaces. An unavailable
required check leaves delivery incomplete; it does not create a new permission request.

### Prepare before requesting approval

1. Build the exact candidate with the existing pinned release recipe. Retain its
   schema-2 bundle manifest and wheel. Use [candidate staging](plugin-marketplace-publication.md#stage-before-release-approval)
   to prepare both host plugins from those inputs, without requiring publication.
2. Qualify those exact packages and obtain all required human verification. Prepare
   the ready RLS and bind its distributions through the existing commands. Include
   the final VREC(s) in that RLS. Stage and review versioned documentation and the
   demonstration inputs. Do not defer candidate assurance until after publication.
3. Prepare the marketplace commit as one ordinary child of the observed public
   `plugin-marketplace` tip. Its complete tree is the checked staged output. Retain
   it on a review staging ref accessible to the publisher, under the release
   preparation work order's branch authority. This does not publish the marketplace.
4. Prepare a `se-harness-delivery-plan/v2` supporting file in the release evidence
   directory. The [synthetic example](../../tests/fixtures/release_delivery/complete-release/plan.json)
   shows its fields; none of that example's identities is a real release input.
   Fill every expected identity from retained evidence. No field may remain `null`.
5. Select `[delivery] route = "complete-release"` in the release contract before
   its approval. This repository-owned selection does not change portable lifecycle
   semantics. The complete plan names the repository, candidate, actions, marketplace
   parent/commit/tree, package identity digest, exact documentation file hashes,
   previous marker values, decision/receipt paths, readiness evidence and observations.
   Both host content identities are the SHA-256 of their `assembly-inventory.json` bytes.
6. For demonstration governance, use `release-governance`: the publisher resolves
   this reviewed rule to the first main commit containing the released RLS. Other
   identities are fixed before approval. `previous_last` is the existing Git ref
   object ID, including a tag object ID when `last` is annotated; it is not its peeled commit.
7. Retain the readiness JSON and its digest in the plan. It names `candidate_commit`,
   `verification_records`, `qualification: "passed"` and `controls_ready: true`, with
   references to the actual qualification and control evidence. These fields are
   a reviewed summary, not proof of their own truth. Missing host credentials,
   assurance or provider controls prevents the ready claim. Required public-route
   checks still occur after publication; they are separate from candidate assurance.
8. Commit the prepared plan and ready RLS. Record this review commit separately;
   placing its own commit ID inside the plan would create a circular identity.
   Freeze the complete plan bytes and their SHA-256. Present their digest and the
   review commit in the final request.

### Obtain and apply the one decision

Lead with **“Approve the complete release”**, evaluator and plugin versions, then
name the outputs: version tag, GitHub release, PyPI, marketplace, documentation,
demonstration, maintenance line and latest/last. Include the bounded release-only
PR integrations and receipt paths. Summarize verification and limitations and link
the plan, candidate and staged package. Confirm the human holds the listed rights.

After the matching response, apply the RLS transition through the selected released
evaluator. Record the actual human and the plan digest/reference in its reason.
Add this repository-owned binding to the RLS under that same decision:

```toml
[delivery]
plan = "docs/engineering/DOMAIN/evidence/WORK/plan.json"
sha256 = "COMPLETE_PLAN_SHA256"
decided_by = "ACTUAL_HUMAN"
decision_reference = "RETAINED_HUMAN_RESPONSE_REFERENCE"
review_commit = "FULL_PRE_APPROVAL_REVIEW_COMMIT"
```

These placeholders are not valid inputs. The binding must match the real decision;
neither a table, a username nor arbitrary prose authenticates a human grant.
The human-reviewed PR and existing repository protections preserve that boundary.

Before integrating, compare the release-only diff with the frozen plan. The existing
publisher's `check-integration` command accepts the retained envelope (`plan` object,
`sha256`, `decided_by`, `decision_reference`, `path`, `review_commit`) and exact Git
base/head. It permits only the named files, unchanged artifact bodies and one appended
matching release decision. With `--receipts`, only the named evidence JSON files may
change; each must retain `release_record`, `candidate_commit` and `plan_sha256`.

```text
python .github/scripts/publish_release.py check-integration --repository . --envelope ENVELOPE_JSON --base BASE --head HEAD
```

The command checks the diff; it does not grant permission or merge. Under the already
recorded integration grant, push the reviewed branch and merge its PR only after
required checks pass. Match the merge to the exact checked head (`gh pr merge NUMBER
--squash --match-head-commit HEAD`); do not use an administrator bypass. Review changed
base content before retry. No unrelated source edit belongs in a release decision commit.

### Execute and resume delivery

Dispatch `publish-pypi.yml` from `main` with its existing single `release_record`
input. The resolver requires matching REL/RLS selection, frozen plan bytes, the
reviewed decision diff, verified records, readiness evidence and prepared package
identity. Legacy RLS inputs continue through their original publisher.

For the complete route, the workflow checks provider controls before publishing.
It runs the existing qualification, immutable GitHub/PyPI publication, maintenance
reconciliation and Pages deployment. It independently downloads the public wheel
and checks its digest before promoting the exact staged marketplace commit. It
executes no staged plugin or candidate code with publication credentials.

The agent then runs the required public fresh/update tests using the public ref.
Retain their actual observations, documentation checks and Pages provenance at
the plan's paths. Integrate only the named receipt files under the same approval,
using `check-integration --receipts` and the protected PR procedure. Do not ask for
permission again just because the next action uses a different provider.

Rerun the same workflow. The delivery checker requires all non-marker observations
before marker promotion. It reports `ready_for_markers`, never `complete`, at that
boundary. Missing authentication or a failed public check keeps the affected step
pending. Required host tests are not replaced by static inventory comparisons.

Exact completed steps are read back and left in place. A failed or uncertain write
is inspected before retry. A moved marketplace parent, different public wheel,
changed plan or unexpected marker stops the affected write. `last` uses an exact
Git lease. GitHub's latest-release API has no compare-and-swap operation; the job
serializes complete-release writes, checks the old value and reads back the result.
Outside writers must not change markers during this operation.

Integrate the marker receipt and updated observations through the same permitted
receipt path, then run `continue-delivery --stage report`. The resulting
`delivery-result.json` is the existing five-surface completion report. The earlier
`release-result.json` records the publisher's stage snapshot and may still show
pending downstream evidence. Retain the final report and link every observed
destination; do not equate the release decision with public delivery.

### Activation and recovery

The [WO-RLO-016 review](../engineering/release-orchestration/evidence/WO-RLO-016/README.md)
contains the observed controls and exact reviewer-only proposal. It does not apply
that change. Before activation, verify and integrate this implementation, release
and separately adopt its evaluator/plugin, then confirm PyPI's Trusted Publisher
binding and the prepared before/after configuration. Obtain the owner's decision
on that exact one-time change. It is not repeated for each later release.

If live settings differ from the retained snapshot, stop and refresh the review.
Recovery restores the prior reviewer list while preserving the main-only branch
policy, OIDC binding and repository protections. Read back every control. No
release uses this review to bypass a still-required provider approval.

## Legacy delivery route

The following procedure remains applicable to contracts that did not select the
complete-release route. Its later assembly and separate grants are historical
constraints, not extra prompts for a matching complete-release approval.

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

## Current 0.22.0 delivery

Evaluator 0.22.0 and plugin 0.2.5 are public. The marketplace commit is
`7d30907f15bd7e06fb632e1ebf4e88e01b68726c`. [Public observations](../engineering/release-0-22-0/evidence/WO-RLS-036/README.md)
record exact package bytes, Codex CLI fresh/update routes and offline setup.
Claude Code installation/update and native session tests, and Codex Windows desktop tests, were not run for this release and remain unverified under DEC-RLS-005/006. Both distributed packages were byte-checked.
Overall delivery is incomplete until documentation is verified, merged and read
back, and the authorized latest/last promotion has been observed.

## Historical 0.21.0 delivery

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

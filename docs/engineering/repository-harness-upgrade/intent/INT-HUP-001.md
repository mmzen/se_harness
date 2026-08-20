+++
id = "INT-HUP-001"
type = "intent"
title = "Govern the standard root with released se-harness 0.5.0"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
+++

# Intent: Govern the standard root with released se-harness 0.5.0

## Problem

The repository was converted to the standard lifecycle during emergency recovery and is still pinned to the immutable bootstrap evaluator `se-harness==0.5.0a1`. Final `0.5.0` is now independently published, but changing only a version string would not prove the governing runtime, managed root, lock, and CI identity agree. The next product release must not repeat the candidate/governor conflation documented by the 0.5.0 RCA.

## Desired outcomes

- The installed standard root and managed CI select exact public `se-harness==0.5.0`.
- The evaluator is installed outside the checkout and its version, distribution origin, entry point, and wheel digest are proven before reliance.
- The ordinary managed upgrade changes only safe standard-root surfaces and preserves repository-owned controls and artifacts.
- Candidate source and candidate package evidence remain independent from the released evaluator.
- A later 0.5.1 packet can be authored, preflighted, and reviewed under released 0.5.0.

## Actors and stakeholders

- The repository owner decides whether the governing baseline may change.
- The engineering owner authorizes the bounded managed-root update.
- The assurance owner assesses the exact candidate and retained evidence.
- Maintainers and contributors rely on CI using the declared released evaluator.
- Release owners rely on the governor/product separation for later 0.5.1 decisions.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Managed root evaluator | 0.5.0a1 | exact public 0.5.0 | candidate and hosted CI |
| Safe upgrade plan | three version-divergent managed files | only reviewed safe updates applied | implementation |
| Formal validation errors | 0 | 0 | candidate review |
| Evaluator checkout imports | prohibited | 0 | every required evaluator check |
| Product or release mutations | 0 | 0 | entire work order |

## Non-goals

- Retrospectively authorizing or creating a normal release record for 0.5.0.
- Changing `se_harness` package behavior, package version, templates, release distribution, or publication workflows.
- Drafting or implementing the 0.5.1 release payload under this work order.
- Tagging, publishing, deploying, approving a protected environment, editing issue #81, or merging a pull request.

## Principles and immutable constraints

- The governor is the independently installed public 0.5.0 distribution, never checkout source or a candidate wheel.
- The current 0.5.0a1 evaluator remains authoritative until a separately approved, verified, and merged root-upgrade candidate changes the installed root.
- Managed integrity and repository-owned policy are preserved; customized or ambiguous files stop the upgrade.
- Governor upgrade and product release remain separate work orders and separate commits.

## Risks and assumptions

- Fact: public 0.5.0 wheel SHA-256 is `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- Fact: current dry-run proposes updates to `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `ENGINEERING_HARNESS.md`.
- Assumption: the exact public distribution remains available from immutable PyPI/GitHub release state.
- Risk: an unreviewed managed update could replace repository-owned controls; exact plan review and post-apply diff checks mitigate it.
- Open decision: accountable owners must approve this complete packet and its no-significant-decision assessment before implementation.

## Approval

On 2026-08-20 the accountable owner explicitly approved `INT-HUP-001`, the complete HUP definition chain, and `WO-HUP-001` for implementation while instructing that the RCV and 0.5.1 release artifacts remain draft. That decision approves this intent but grants no commit, VREC, push, PR, merge, release, publication, deployment, or issue-edit authority.

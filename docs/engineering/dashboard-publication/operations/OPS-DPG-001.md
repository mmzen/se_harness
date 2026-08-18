+++
id = "OPS-DPG-001"
type = "operating_contract"
title = "Operate the public Explorer demonstration"
status = "approved"
owners = ["service-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-18"

[relations]
assures = ["REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
+++

# Operating Contract: Operate the public Explorer demonstration

## Activation

The repository owner approved this proposed operating behavior as part of the `WO-DPG-001` implementation packet on 2026-08-16. After `VREC-DPG-001` transitioned to `verified`, the accountable owner explicitly instructed `transition OPS-DPG-001` on 2026-08-16. That human decision activates this contract from `draft` to `approved`; automation only confirmed eligibility.

This activation installs the operating and assurance boundary. It does not itself deploy the public site, merge the pull request, alter a release, or publish a package.

## Service level objectives

The site is a best-effort promotional demonstration, not a production assurance service. For each release selected for demonstration, the target is one successful deployment or a visible failed workflow requiring maintainer review. No independent uptime or latency SLO is promised beyond GitHub Pages and the existing optional 3D dependency; non-3D content should remain usable when unpkg is unavailable.

## Observability

Observe the released-record orchestration, GitHub Release, Actions run conclusion, selected release record, candidate and governance commits, generated hashes, Pages environment deployment, deployed URL, and visitor-visible provenance notice. Platform workflow and deployment history are operational observations, not formal lifecycle authority.

## Alerts and escalation

GitHub's failed-workflow and environment notifications are the primary signals. Escalate provenance, validation, payload, permission, or security failures to the repository and security owners. Escalate platform availability failures to the service owner for replay after the dependency recovers. Do not bypass a failed invariant to restore promotional availability.

## Capacity and cost boundaries

Run only inside selected released-record orchestrations and authorized main-only replays. Publish one bounded static dashboard; do not add a persistent application, database, analytics service, high-frequency schedule, or paid infrastructure without new authority.

## Backup and recovery

Formal artifacts and Git history are the durable source. Rebuild the Pages artifact from the released RLS and immutable governance commit; derive the tag rather than re-entering it. The previous successful Pages deployment may remain live while a replacement fails. Generated output requires no repository backup branch.

## Security and compliance controls

Maintain least-privilege workflow permissions, immutable action pins, protected environment rules, full provenance checks, clean checkout, exact payload allowlist, token exclusion, safe rendering, and the existing CSP/CDN controls. Review action-pin updates and Pages policy changes through a governed work order. Never publish private repository data through this contract.

## Automated remediation envelope

Automation may validate, generate, upload, deploy, report, serialize, and retry an identical authorized request. It may not choose a different release, weaken a failed check, edit formal artifacts, rewrite Git history, change repository or Pages settings, rotate secrets, create a release, or grant itself approval.

## Runbooks

### Publish after release

1. Confirm the formal release record is `released` and the GitHub Release exists.
2. Observe the orchestrator's resolved RLS, candidate, governance commit, and hashes.
3. Review the deployed URL and demonstration notice.

### Replay a failed deployment

1. Determine whether the failure is provenance/source-related or an external platform failure.
2. Correct source defects only through a new governed candidate; never mutate the historical release.
3. For a transient external failure, dispatch the same release record and full governance commit.
4. Compare hashes and review the resulting deployment.

### Disable publication

Disable the repository-specific workflow or Pages environment through separately authorized repository administration. Do not delete or alter formal release history. Document the operational reason.

## Evidence retention

Retain workflow summaries and deployment history according to repository GitHub retention settings. Retain significant failure analyses, security deviations, pin updates, and recovery evidence in the applicable governed work order. Git remains the source for reproducible formal provenance.

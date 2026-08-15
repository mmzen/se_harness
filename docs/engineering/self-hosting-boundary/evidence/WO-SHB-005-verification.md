# WO-SHB-005 governance evidence

Date: 2026-08-15  
Lifecycle: retained governance evidence; not product implementation, release authority, or merge authority

## Accountable decision

After all hosted checks for pull request 44 completed successfully, the accountable repository owner stated `ok CI, I validate the validation record, it can be committed and pushed`. This evidence records that decision for `VREC-SHB-002`. Automation did not infer or grant verification.

## Bound lineage

| Subject | Identity |
| --- | --- |
| Candidate commit | `7726d7686dfe7a01452c53f21871a78569cf3ac4` |
| Ready-record commit | `e0ac4e8b1018e909cc6fedaaa6ead430d2445d2f` |
| Ready-record blob | `a304d44f45b44a2ed596c4dd6bc2876a2ff99acf` |
| Verification record | `VREC-SHB-002` |
| Work order covered | `WO-SHB-004` |
| Verification contracts | `VER-SHB-001`, `VER-SHB-002` |
| Captured snapshot | `124c321a40376c34a149c0abf6f3991b8f6fd5e10c78b05284324baa1f4fd6ff` |

The candidate is an ancestor of the committed ready record. Pull request 44 selected head `e0ac4e8b1018e909cc6fedaaa6ead430d2445d2f` when the accountable decision was made.

## Hosted assurance evidence

Two workflow runs were produced by the branch push and pull-request events. Both used `Engineering Harness Self-Hosting` and completed the same three non-substitutable planes successfully:

| Run | Released governor | Candidate source | Candidate package |
| --- | --- | --- | --- |
| `31882030968` | SUCCESS | SUCCESS | SUCCESS |
| `31882037990` | SUCCESS | SUCCESS | SUCCESS |

The checks downloaded the exact published 0.3.0 governor, proved its isolated identity, exercised candidate source, built the candidate package outside the checkout, and ran released-governor black-box acceptance. No check was pending, skipped, cancelled, or failed at the assurance decision.

## Transition preservation

The transition changes only `status = "ready"` to `status = "verified"` and replaces the explanatory candidate text with the accountable decision note. The following captured fields remain byte-for-byte equal to the ready record:

- commit `7726d7686dfe7a01452c53f21871a78569cf3ac4`;
- object format `sha1`;
- worktree state `clean`;
- capture timestamp `2026-08-15T11:23:48Z`;
- artifact snapshot `124c321a40376c34a149c0abf6f3991b8f6fd5e10c78b05284324baa1f4fd6ff`;
- evidence path `docs/engineering/self-hosting-boundary/evidence/WO-SHB-004-verification.md`;
- work order `WO-SHB-004`;
- verification contracts `VER-SHB-001` and `VER-SHB-002`.

## Verification and authority boundary

Formal artifact validation, exact published 0.3.0 doctor, review preflight, ancestry checks, ready-blob identity, transition-field comparison, hosted-check inspection, and diff hygiene pass. The governance diff contains only `VREC-SHB-002`, `WO-SHB-005`, and this evidence.

No merge, release record, tag, GitHub Release, PyPI publication, deployment, force push, or history rewrite is authorized or claimed. Pull request 44 remains subject to its separate review and merge decision.

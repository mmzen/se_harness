+++
id = "VREC-SEH-008"
type = "verification_record"
title = "Verification candidate for 8 work orders"
status = "verified"
owners = ["quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
commit = "827b2709292abaa3458bb3b4cac37b582378c585"
git_object_format = "sha1"
worktree_state = "clean"
verified_at = "2026-08-21T14:53:14Z"
verified_by = "quality-owner"
artifact_snapshot_sha256 = "6845024e96fdb369f3a14c37209dc18e2da6a86dc383c0f6a8b33e1355e50326"
evidence_paths = ["docs/engineering/harness-distribution/evidence/WO-DST-019-verification.md", "docs/engineering/harness-distribution/evidence/WO-DST-020-verification.md", "docs/engineering/release-0-6-0/evidence/WO-RLS-008-verification.md", "docs/engineering/released-evaluator-boundary/evidence/WO-REB-001-implementation.md", "docs/engineering/released-evaluator-boundary/evidence/WO-REB-002-implementation.md", "docs/engineering/released-evaluator-boundary/evidence/WO-REB-003-verification.md", "docs/engineering/workflow-execution/evidence/WO-WEX-001-verification.md", "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md"]

[relations]
verifies_work_order = ["WO-DST-019", "WO-DST-020", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008", "WO-WEX-001", "WO-WEX-002"]
conforms_to = ["VER-DST-001", "VER-DST-019", "VER-DST-020", "VER-REB-001", "VER-WEX-001", "VER-WEX-002"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-08-21T15:02:13Z"
decided_by = "quality-owner"
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-DST-019`, `WO-DST-020`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, `WO-RLS-008`, `WO-WEX-001`, `WO-WEX-002` to candidate commit `827b2709292abaa3458bb3b4cac37b582378c585`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Exact aggregate scope

This proposal is limited to the release aggregate approved by `REL-SEH-007` and implemented by `WO-RLS-008`. The front matter is the normative allow-list and contains exactly:

- eight work orders: `WO-DST-019`, `WO-DST-020`, `WO-WEX-001`, `WO-WEX-002`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, and `WO-RLS-008`;
- six verification contracts: `VER-DST-001`, `VER-DST-019`, `VER-DST-020`, `VER-WEX-001`, `VER-WEX-002`, and `VER-REB-001`; and
- eight keyed evidence paths, one for each approved work order.

`WO-VSP-006`, its evidence, superseded WEX records, merge-only commits, emergency-publication history, and all other work orders remain outside this release-bearing aggregate.

## Candidate and reproducible-distribution binding

| Item | Retained identity |
| --- | --- |
| Operational candidate commit | `827b2709292abaa3458bb3b4cac37b582378c585` |
| Operational candidate tree | `cdeb5f5e0fe512e042dd13d8f8071dc06a1b40e0` |
| Exact candidate build epoch | `1787322471` |
| Exact candidate archive SHA-256 | `6ed1b6e4dcad1e24d042babb773be5e52638cb11a4a6fe458da03178a187aabc` |
| Candidate artifact snapshot SHA-256 | `6845024e96fdb369f3a14c37209dc18e2da6a86dc383c0f6a8b33e1355e50326` |
| Wheel SHA-256 | `9eb550d2fbab2ea8906aadb39ff75271ca9037267d721b8705cad93012b3ed37` |
| Normalized sdist SHA-256 | `df10d40eeebfcecf5bbd082aba3444bab8fd63146c1f7c5d2a03c0ad313d98f1` |
| Release-bundle manifest file SHA-256 | `8b6e3ad52b5e65f50b4dc0ecd98cf12f46fd100d73c23d5864678dc027fdbb89` |
| Source-manifest SHA-256 | `1fa0127abddd446a519bab667cd89cfaeff95979775f28d500ea1c993dad1832` |
| Checksum-content SHA-256 | `63a0d91bc027447449901c9733e1caee5d32d73c8e60c2eda1ce357f7550459b` |

Two isolated builds from untouched exact-candidate exports produced byte-identical wheels and byte-identical normalized sdists. An offline wheel reconstruction from the normalized sdist at the same epoch was byte-identical to the direct wheels.

The artifact snapshot in the front matter was captured in the operational repository by the separately installed released 0.5.0 evaluator while the clean checkout was detached at the exact candidate. It records Git object format `sha1` and the exact candidate revision. An earlier Explorer manifest with SHA-256 `72de5c772c3b402be48aca38fabad38d8b680c41766fbeb7b6724abc262a0715` retained useful graph evidence but reported the revision as unavailable, so it is not the normative candidate-binding snapshot for this proposal.

## Independent released-evaluator evidence

| Item | Retained identity or result |
| --- | --- |
| Public released evaluator | `se-harness==0.5.0`, isolated Python 3.14.6 |
| Released-evaluator wheel SHA-256 | `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f` |
| Released verifier contract SHA-256 | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` |
| Python 3.14 acceptance-manifest SHA-256 | `6845459905f7cd27a09ab0fcb6cf18b66a26b2174876169027843adeb6bd5630` |
| Python 3.11 acceptance-manifest SHA-256 | `72446826458a3fa2ad3270c911fb9289fc9e326291ef8c64989c965274ce55c3` |
| Verifier-owned black-box scenarios | 10 of 10 passed on both runtimes |
| Candidate source and package identity | PASS, bound to the exact candidate |
| Released root installation | Unchanged and locked at 0.5.0 |

The ten verifier-owned scenarios cover installed identity, init, adopt, doctor, validate, dashboard, safe upgrade, customized-content refusal, corrupted-integrity refusal, and authority denial. Candidate templates may lead the separately locked released root evaluator; this record was therefore captured with the released 0.5.0 evaluator and does not upgrade or mutate the released root.

The released 0.5.0 capture format writes `verified_at` while initially emitting status `ready`. In this proposal that field is only the evaluator capture timestamp. It is not an assurance decision, does not mean that `VREC-SEH-008` is verified, and grants no release authority.

## Integrated and hosted qualification

- Exact source regression on Python 3.14.6: 369 tests passed, five conditional skips, zero failures or errors, in 199.387 seconds.
- Exact source regression on Python 3.11.9: 369 tests passed, the same five conditional skips, zero failures or errors, in 202.662 seconds.
- Candidate artifact validation: 597 artifacts, 2,140 relations, zero errors, 44 existing maintenance warnings, and zero structure, governance, or policy warnings.
- Hosted Candidate Evidence run 97: source job `96806587928` and package job `96806785170` passed against the exact candidate.
- Hosted Engineering Harness run 397: validation job `96806588077` passed against the exact candidate.
- Formal validation with this ready proposal present: 598 artifacts, 2,154 relations, zero errors, 45 maintenance-only warnings, and zero structure, governance, or policy warnings.
- Release-distribution validation with this ready proposal present: PASS with zero distribution-bearing records, because no RLS has been prepared.
- Released-evaluator inspection with this ready proposal present: exactly `VREC-SEH-008` is in the decision-required queue and no artifact is in the active-work or assurance-pending queues.

The hosted evidence is retained at [Candidate Evidence run 97](https://github.com/mmzen/se_harness/actions/runs/32493552379) and [Engineering Harness run 397](https://github.com/mmzen/se_harness/actions/runs/32493552394).

A post-preparation read-only doctor/review-preflight replay through the released 0.5.0 evaluator preserved every lock-managed root file as unchanged, while reporting the known candidate-template and schema surfaces that lead the released distribution (`WORKFLOW.json`, `QUALITY_GATES.json`, `.gitattributes`, and newer managed/template content). Review preflight consequently reports `ready: false` under the older evaluator's distribution comparison. This is retained compatibility evidence, not a newly introduced graph error and not authority to mutate or upgrade the root evaluator.

## Preparation and authority boundary

This file is a local, post-candidate assurance proposal. Its preparation does not change candidate commit `827b2709292abaa3458bb3b4cac37b582378c585` or the candidate branch. The accountable assurance owner must independently review the exact aggregate, keyed evidence, bundle identities, evaluator evidence, and retained hosted results before explicitly accepting or rejecting a transition.

At this stop, `VREC-SEH-008` remains `ready`. No aggregate VREC transition, RLS preparation or transition, push, tag, publication, deployment, maintenance mutation, credential use, external policy change, or root-evaluator upgrade is authorized or performed by this record.

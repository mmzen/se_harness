+++
id = "VER-ECP-010"
type = "verification"
title = "Independent evidence for the line-ending-canonical formal snapshot"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T09:09:07Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the repair of issue #256: formal_snapshot_digest hashes each artifact's utf8-text-lf-v1 canonical bytes so a CRLF checkout computes the runner's digest while every LF-bound digest is unchanged; with the amendment record on SPEC-ECP-001. Measured before this transition over branch state ea8494d carrying unmoved main 741a774: validate PASS at 0 errors under the governing 0.9.0 root; start preflight reads only the draft signature. Approval of a definition authorizes no work; the work order is approved separately."
+++

# Verification Contract: Independent evidence for the line-ending-canonical formal snapshot

## Independence

Expected behaviour derives from `REQ-ECP-021` and the `ECP-CSN-` rules of
`SPEC-ECP-010`. The conformance tests build their LF and CRLF trees from one
fixture with bytes the test writes, not the host's Git settings; the
repository reading measures the digest of one committed tree on a CRLF
Windows checkout and on an LF Linux clone with the candidate evaluator.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-021` LF unchanged | test: digest of an LF fixture tree against a digest fixed before the change | `tests/test_workflow_compliance.py` | equal |
| `REQ-ECP-021` CRLF equals LF | test: the same fixture with CRLF endings in every artifact | `tests/test_workflow_compliance.py` | equal to the LF digest; differs after one content character changes |
| `REQ-ECP-021` on this repository | demonstration: `harnessctl evidence` with candidate source on the CRLF Windows worktree and on the LF clone at the same commit | the work order's evidence packet | the two headers carry the same `formal_snapshot_sha256` |
| `SPEC-ECP-010` one function | analysis: grep for `read_bytes` and `sha256` over the snapshot callers | the evidence packet | no second snapshot computation exists |

## Acceptance scenarios

### Scenario 1: LF tree, digest unchanged

Compute the digest over the fixture chain with LF bytes; assert it equals
the value recorded in the test before the change.

### Scenario 2: CRLF tree, same digest

Rewrite every fixture artifact with CRLF endings; assert the same digest.
Change one character in one artifact; assert a different digest.

### Scenario 3: this repository

On the Windows CRLF checkout, run `evidence` with candidate source; on the
LF clone at the same commit, run it again; assert equal headers. Record
both values.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-014/`.

## Pass criteria

Every deterministic test passes on the Linux lane; scenario 3 shows equal
digests. Graph and integrity readings come from the exact released
evaluator, se-harness 0.9.0, installed outside the checkout.

## Residual uncertainty

Packets bound by the released 0.9.0 evaluator on a CRLF checkout are
already stale hosted and stay so; the rule reaches evaluators through the
next release.

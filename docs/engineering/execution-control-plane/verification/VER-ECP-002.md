+++
id = "VER-ECP-002"
type = "verification"
title = "Independent evidence for harness-authored evidence packets, cross-ref identifier allocation, and generated pull-request bodies"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
verifies = ["REQ-ECP-003", "REQ-ECP-004", "REQ-ECP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Verification Contract: Independent evidence for harness-authored evidence packets, cross-ref identifier allocation, and generated pull-request bodies

## Independence

Expected behaviour derives from the three requirement statements and the
`ECP-EVD-`, `ECP-IDA-`, and `ECP-PRB-` rules of `SPEC-ECP-002`. Expected
header bytes, identifiers, and body bytes are written by hand from the rules.
Identifier oracles are built by the test walking `git for-each-ref` and
`git ls-tree -r` itself. Snapshot digests used as oracles come from the
exact released evaluator, se-harness 0.7.1, installed outside the checkout.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-003` packet written or rebound | test: `evidence` on a fresh packet; on an existing packet after a snapshot move; on a packet with an edited body | temporary repository with one approved work order and retained body text | the machine header carries `artifact`, `checkpoint`, and the current `formal_snapshot_sha256`; a rebind changes only the header bytes and leaves every body byte equal; `review_evidence_available` passes after the rebind and fails before it |
| `REQ-ECP-004` allocation across every local ref | test: `create-artifact` without `--id` | a higher identifier present only on an unmerged local branch; a gap below the working-tree maximum; an identifier present only on a detached ref | the allocated identifier is the lowest unused across every local ref, so the branch-only identifier is skipped and the gap is not filled when any ref uses it; the result names the refs consulted |
| `REQ-ECP-005` generated body | test: `pr-body` bytes | work order with and without a handoff result; body compared to expected bytes | body ends in LF only, contains no `0x0D`, carries a standalone `Harness-Work-Order: WO-...` line, and carries `Harness-Restitution: RESULT_SHA256` exactly when a handoff result exists; `select-work-order` parses the generated body back to the same identifier and digest |

## Acceptance scenarios

### Scenario 1: write, then rebind

Run `evidence` for an approved work order at handoff. Assert the header and
that `check` passes `QGP-G4I-EVIDENCE`. Edit an unrelated artifact so the
snapshot moves (today the digest moves on any artifact edit; the 2026-08
agentic execution review, section 5, weakness 6). Assert `check` fails, run
`evidence` again, assert the body bytes are unchanged and `check` passes.

### Scenario 2: failure path, body tampered between runs

Rewrite a retained body line and rebind. Assert the rebind refuses with a
coded diagnostic naming the packet, and the packet is not written.

### Scenario 3: identifier on another branch

Create `REQ-X-004` on a local branch only. In the working tree holding
`REQ-X-001..003`, allocate. Assert `REQ-X-005`.

### Scenario 4: failure path, refs unreadable

Run allocation outside a Git repository. Assert refusal with a coded
diagnostic; no artifact is written.

### Scenario 5: body round trip

Generate the body, write it to a fixture event payload, run
`select-work-order --event ... --field work-order` and
`--field restitution-digest`. Assert both equal the inputs and that
`W-ADS-001` is not emitted.

### Scenario 6: failure path, CRLF checkout

Run `pr-body` in a checkout with `core.autocrlf=true`. Assert the emitted
bytes still contain no `0x0D` (`REQ-ADS-004` exists because CRLF trailers
recurred; review section 6).

## Property and invariant tests

- For any packet, `rebind(rebind(p)) == rebind(p)` in bytes.
- Allocation is monotone: adding any artifact to any ref never lowers the
  allocated identifier.
- The generated body is a deterministic function of the work order and the
  handoff result: two generations are byte-identical.

## Static and architecture checks

- The evidence header is parsed by one function in `se_harness/`, and the
  substring matcher at `se_harness/workflow_compliance.py:266-291` is
  replaced, not duplicated.
- No shipped contract instructs the agent to hand-write the three evidence
  lines (the `QGP-G4I-EVIDENCE` corrective at
  `se_harness/workflow_contract.json:509` does today).

## Security and privacy checks

- `evidence` writes only under the evidence directory of the work order's
  domain; a work order whose domain path escapes `docs/engineering/` is
  refused.
- `pr-body` includes no environment variable values and no absolute paths.

## Performance and resilience checks

- Allocation over a repository with 50 local refs completes within 5 seconds
  on both platforms; figure recorded.

## Manual assessments

None.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ID/`: packet
bytes before and after rebind with a byte diff, the ref listing and allocated
identifiers, the generated body bytes with a hex dump of the line ends, and
per-platform test figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows, figures labelled per
platform. Snapshot digests and graph readings come from the exact released
evaluator, se-harness 0.7.1, installed outside the checkout. No historical
evidence packet under any domain is rewritten.

## Residual uncertainty

Identifier allocation sees local refs only; a remote-only identifier remains
a collision that the pull-request gate, not allocation, catches.

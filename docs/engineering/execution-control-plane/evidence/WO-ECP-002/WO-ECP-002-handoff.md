```toml
artifact = "WO-ECP-002"
checkpoint = "handoff"
formal_snapshot_sha256 = "9c6e9645393374ce2acf007697f7535116a7f4776411aa7fc5c07e2edbb16c22"
rebound_at = "2026-08-28T21:10:00Z"
```

# WO-ECP-002 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored. This
packet is the first written by the command it evidences: the fenced TOML
header above is the machine header of `ECP-EVD-002`, rebound by
`harnessctl evidence` at each snapshot move; everything below it is retained
byte for byte across rebinds.

This file is evidence. It does not complete, verify, or release the work
order.

## Outcome

The harness now authors three pieces of state the agent used to carry:
the evidence packet (`harnessctl evidence`, machine header read by
`QGP-G4I-EVIDENCE` through a TOML parser), new identifiers
(`create-artifact` without `--id`, the lowest free number across every
local branch and tag and the working tree) and the pull-request body
(`harnessctl pr-body`, LF only, round-tripping through the CI selector). A
completed Git-derived handoff check retains its result as `handoff.json`
beside the packet, and `pr-body` turns that into the `Harness-Restitution`
line.

## Evaluators

- Governing: released `se-harness 0.8.0` outside the checkout, `-I`:
  validate, doctor, start preflight, the handoff bind. 0.8.0 predates the
  machine header and reads evidence by substring, so this packet also
  carries the three legacy lines in the *Legacy binding* section below; the
  candidate's own predicate reads the header and ignores those lines
  (proven by `test_the_predicate_reads_the_header_never_substrings…`).
- Candidate: this checkout, branch `wo/ecp-002-evidence-ids-pr-body` off
  `main` at `0961176`.

## What changed

| Path | Change |
| --- | --- |
| `se_harness/workflow_compliance.py` | `parse_evidence_header` / `render_evidence_header` (fenced TOML at byte offset 0, exactly `artifact`, `checkpoint`, `formal_snapshot_sha256`, `rebound_at`; `WEX-ECP-010` on a malformed, foreign or headerless packet); `evidence_packet_path` (`DOMAIN/evidence/WO-ID/WO-ID-CHECKPOINT.md`); `write_evidence_packet` (create with the default body, or rebind rewriting only the header bytes; `WEX-ECP-011` when a `.gitattributes` rule would convert line endings, read with `git check-attr`; `WEX-ECP-012` when the single `in_progress` work order is another; atomic temp-and-replace; schema-2 result with `mutation.writes`); `retain_handoff_result` (`handoff.json`, canonical JSON, LF); `_review_evidence` reads headers through the parser, passes on the three identity fields, ignores every other headered file, and keeps the substring form for one release under `W-ECP-002` naming the migrating command; `admitted_scope` gains the packet directory (harness-written evidence at its own path). |
| `se_harness/artifact_layout.py` | `reachable_artifact_ids` (`git for-each-ref` + `git ls-tree -r` per local ref, remote-tracking refs excluded, plus the working tree including untracked files; `WEX-ECP-013` outside a checkout or on a Git failure); `allocate_artifact_id` (lowest free `TYPE-DOMAIN-NNN`, the domain token read from the domain's existing artifacts, the refs of the next-lower identifier returned); `create_artifact(artifact_id=None)` allocates; an explicit `--id` found on any local ref is refused naming the ref; `AuthoringChange` carries `allocated_id` and `allocation_refs`. |
| `se_harness/github_ci.py` | `render_pull_request_body`: the standalone `Harness-Work-Order` line first, `Harness-Restitution` from a schema-2 `handoff.json`, `## Summary` and `## Verification` with every evidence path; LF only; refuses a non-work-order or a draft (`WEX-ECP-014`) and asserts the round trip through `select_work_order` before returning. |
| `se_harness/cli.py` | `evidence [--rebound-at]`, `pr-body` (bytes to stdout), `create-artifact --id` optional with the allocation line, `check` retaining `handoff.json` after a completed `--from-git` handoff. |
| `se_harness/workflow_contract.json`, template `WORKFLOW.json` | the `QGP-G4I-EVIDENCE` corrective is the command `harnessctl evidence . --artifact {artifact_id} --checkpoint handoff` (pre-start amendment 3). |
| `templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed` | one sentence pointing at `pr-body`. |
| `docs/notes/harnessctl-reference.md` | inventory rows, synopses and paragraphs for `evidence`, `pr-body` and allocation. |
| `SPEC-ECP-002` | the four pre-start amendments, plus the packet-directory admission. |
| tests | `EvidencePacketTests` (5), `IdentifierAllocationTests` (2, real `git init` fixtures with branches, a tag, a gap and a remote-tracking ref), `PullRequestBodyTests` (2, own fixture renamed to a selector-shaped identifier). |

## Readings on this branch (candidate source)

- `evidence` create: header at offset 0 with the four keys; rebind after
  an owner-appended body line and a snapshot move: the body digest is
  unchanged, `rebound_at` moved, and a byte comparison of the file before
  and after a rebind shows differing bytes only inside the header.
- Tamper: a packet with the header stripped, with another artifact's
  header, with invalid TOML, or with an extra key is refused with
  `WEX-ECP-010` and left untouched.
- `check --from-git main` on this work order: `completed`, the evidence
  predicate reading the header, and `mutation.writes` naming
  `docs/engineering/execution-control-plane/evidence/WO-ECP-002/handoff.json`.
- `pr-body`: first line `Harness-Work-Order: WO-ECP-002`, second the
  retained `result_sha256`, then Summary and Verification listing the two
  packet files; `od -c` shows no `\r` byte and one final `\n`.
- `pr-body --artifact WO-ECP-003` (draft): `WEX-ECP-014`.
- `create-artifact --domain execution-control-plane --type requirement
  --dry-run`: allocates `REQ-ECP-019` and names the refs carrying
  `REQ-ECP-018` (every local branch and `main`, the working tree);
  remote-tracking refs are not consulted.

## Readings under the 0.8.0 root, isolated mode

- `validate .`: PASS, 0 errors. `doctor .`: 0 FAIL. Start preflight:
  Completed over the approval commit `645b5ca`.

## Deviations

1. Readings under 0.8.0, not the 0.7.1 the packet text names.
2. The root managed `WORKFLOW.json` stays 0.8.0's; the template moves.
3. Evidence packets and `handoff.json` are written without a mutation-guard
   operation: they are retained evidence, not authority, and the guard
   protects installed-root and formal-artifact writes (`create-artifact`
   keeps its guard). No new operation name was needed, so
   `mutation_guard.py` stayed outside the change.
4. The domain token of an allocated identifier is read from the domain's
   existing artifacts (`ECP-IDA-001` names `TYPE-DOMAIN-NNN` without saying
   where `DOMAIN` comes from); a domain with no artifact yet needs `--id`.

## Suite

`python scripts/run_tests.py --scale full` with candidate source (CPython 3.12, Linux): Ran 1077 tests in 45.858s (121 classes, 4 workers); the one failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`, the workstation file-mode condition that passes hosted, unchanged. The Windows figure is the hosted lane's.

## Handoff check

Governing 0.8.0: `harnessctl check . --artifact WO-ECP-002 --checkpoint handoff --changed-path … --changes-complete` over the 14 paths below, the work order's own file omitted as 0.8.0 predates `ECP-CHG-007`: Completed once the legacy lines below were retained; before them the only non-pass predicate was QGP-G4I-EVIDENCE.

## Complete changed-path set

```
docs/engineering/execution-control-plane/evidence/WO-ECP-002/handoff.json
docs/engineering/execution-control-plane/evidence/WO-ECP-002/WO-ECP-002-handoff.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-002.md
docs/notes/harnessctl-reference.md
se_harness/artifact_layout.py
se_harness/cli.py
se_harness/github_ci.py
se_harness/workflow_compliance.py
se_harness/workflow_contract.json
templates/repository/standard/docs/engineering/WORKFLOW.json
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
tests/test_artifact_authoring.py
tests/test_workflow_compliance.py
tests/test_workflow_execution.py
```

## Legacy binding

For the governing 0.8.0 evaluator, which reads evidence by substring (the header above is what the candidate reads):

artifact: WO-ECP-002
checkpoint: handoff
formal_snapshot_sha256: 9c6e9645393374ce2acf007697f7535116a7f4776411aa7fc5c07e2edbb16c22

## Deviation 5, recorded after the bind

The generated body carries `Harness-Restitution: 259453bb…`, the digest of the candidate's Git-derived handoff result. The managed CI lane recomputes the handoff with the governing 0.8.0 evaluator over `git diff --name-only base HEAD`, which includes this work order's own file; 0.8.0 predates `ECP-CHG-007` and reads that path as out of scope, so its block is `Blocked` and its digest differs. The pull request therefore omits the restitution line until the root carries `WO-ECP-001`; the line is exercised by the tests and by the body retained in this packet directory.

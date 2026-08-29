```toml
artifact = "WO-ECP-014"
checkpoint = "handoff"
formal_snapshot_sha256 = "51b08822ed0fc350cac9b00d6814648be20b5cec0539ac096ca9c32cbf1c2a90"
rebound_at = "2026-08-29T09:18:44Z"
```

# WO-ECP-014 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`formal_snapshot_digest` hashes each artifact's `utf8-text-lf-v1` canonical
bytes (`ECP-CSN-001`): a CRLF checkout computes the same snapshot as the LF
runner (`ECP-CSN-003`), every LF-bound digest is unchanged (`ECP-CSN-002`),
and the rule reaches every caller through the one function (`ECP-CSN-004`);
the check reference says so (`ECP-CSN-005`); `SPEC-ECP-001` carries the
amendment record on `ECP-SNP-001`. Issue #256.

## Evaluators

- Governing: released `se-harness 0.9.0` outside the checkout, `-I`, on
  Windows for `validate`, `doctor` and `preflight`, and the same wheel in an
  isolated Linux environment (WSL Ubuntu 24.04, CPython 3.12.3) for
  `evidence`, `transition --apply` and the handoff check over an LF clone.
  The released 0.9.0 evaluator hashes raw bytes, so this packet's header is
  still bound from the LF clone; the rule reaches evaluators through the
  next release.
- Candidate: this checkout, branch `wo/ecp-014-canonical-snapshot` off
  `main` at `741a774`; the suite and the demonstration run candidate
  source.

## Change

- `se_harness/workflow_compliance.py`: `_snapshot_content` renders an
  artifact's bytes with `integrity.canonical_text_bytes` (`utf8-text-lf-v1`)
  and falls back to the raw bytes for content that is not UTF-8 text;
  `formal_snapshot_digest` hashes that instead of `read_bytes()` directly.
  Path, ordering and length framing are unchanged.
- Caller inventory (`grep formal_snapshot_digest`): `write_evidence_packet`,
  `build_context` and `repository_state._formal_state`; the only other
  `hashlib.sha256()` in those modules is the file-manifest digest of
  `repository_state.py:94`, not a snapshot.
- `docs/notes/harnessctl-check.md`: `G4I-EVIDENCE` now says the snapshot is
  over line-ending-canonical bytes.
- No managed or hash-locked file moved.

## Tests

`tests/test_workflow_compliance.py::CanonicalSnapshotTests`:

- an LF fixture tree yields `3ccc996f…`, the raw-rule digest of the same
  tree measured on this workstation before the change (the pin was first
  computed on a fixture without the class's own `setUp` edits and read
  `b5cbe053…`; the test's fixture gives `3ccc996f…` under both rules, and
  that is the value pinned);
- the same tree rewritten with CRLF endings yields the same digest, and one
  changed character changes it;
- a packet bound on the CRLF tree is fresh on the LF tree.

## Suite readings

- Linux (WSL Ubuntu 24.04, CPython 3.12.3, LF clone at `c066269`):
  `python3 scripts/run_tests.py --scale full` OK, 4 skips.
- Windows 11 workstation (CPython 3.12, CRLF checkout, `c066269`): 1117
  tests, 2 failing names, both outside this work order and present on
  `main`:
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  and
  `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`.

## Demonstration on this repository (`VER-ECP-010` scenario 3)

Candidate source at `c066269`, `harnessctl evidence . --artifact WO-ECP-014
--checkpoint handoff`:

- on the Windows worktree, where 1120 of the 1124 formal artifacts carry CRLF endings
  (measured at the same commit): formal snapshot `51b08822ed0fc350cac9b00d6814648be20b5cec0539ac096ca9c32cbf1c2a90`;
- on the LF Linux clone at the same commit: formal snapshot
  `51b08822ed0fc350cac9b00d6814648be20b5cec0539ac096ca9c32cbf1c2a90`.

Equal. Under the raw rule at `61840f3` the same comparison read
`a1bd35eb…` against `eb25d023…`.

## Readings under the 0.9.0 root

- `validate .`: PASS; maintenance E0/W475.
- `doctor .`: 0 FAIL.
- Review preflight for `WO-ECP-014`: PASS.

## Handoff check

`harnessctl check . --artifact WO-ECP-014 --checkpoint handoff --from-git 741a774`
from the Linux 0.9.0 environment over an LF clone, run to its fixed point
on the committed packet: see the retained `handoff.json` beside this file.

## Complete changed-path set

Every path this work order changed since `main` at `741a774`, packet
included, as Git derived it (11 paths):

```
docs/engineering/execution-control-plane/evidence/WO-ECP-014/handoff.json
docs/engineering/execution-control-plane/evidence/WO-ECP-014/WO-ECP-014-handoff.md
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/requirements/REQ-ECP-021.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-010.md
docs/engineering/execution-control-plane/verification/VER-ECP-010.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-014.md
docs/notes/harnessctl-check.md
se_harness/workflow_compliance.py
tests/test_workflow_compliance.py
```

## Hosted lanes

Pull request #259. At `e932993`, the head the completion decision was
taken on while its lanes were still running: the managed Engineering
Harness workflow (the 0.9.0 root's old handoff-only step) completed
`success` with the declared `Harness-Restitution` `9ab56eda…` equal to the
recomputed digest, and the Governor Transition Assessment `success`; the
SE Harness Candidate Evidence and Publication Rehearsal workflows were
cancelled by the push of `6185a06` under the repository's
cancel-in-progress policy before they finished. At `6185a06` (the
completion transition, same candidate source): Candidate Evidence and
Publication Rehearsal `success`, Governor Transition Assessment `success`,
and the managed workflow `failure` with `WEX210: gate
QG-G4-CANDIDATE-READY does not apply at checkpoint handoff` — issue #255 on
the 0.9.0 root, the condition `WO-ECP-013` removes for the next release.
Twelve of thirteen lanes pass at `6185a06`.

+++
id = "WO-RLO-008"
type = "work_order"
title = "Make the recipe-bound candidate export independent of the calling host"
status = "in_progress"
owners = ["engineering-owner", "release-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the source input of the build every release depends on. Its correctness is decided by whether an already released record still replays to its bound bytes, which is a property of one exact commit and of nothing else; a later engineering, assurance, or release decision that trusted this behaviour without a commit-bound reading would be trusting a rebuild it never observed."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-RLO-017"]
specifications = ["SPEC-RLO-004"]
architecture = ["ARCH-RLO-004", "ADR-RLO-004"]
verification = ["VER-RLO-004"]

[execution_scope]
paths = [
  "repository_tools/release_build.py",
  "tests/test_release_build.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/release-orchestration/README.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-017.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-008.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-004.md",
  "docs/engineering/release-orchestration/architecture/ARCH-RLO-004.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-004.md",
  "docs/engineering/release-orchestration/evidence/",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:13:07Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-27: approve WO-RLO-008. Approval ratifies commit_bound_verification required: the change alters the source input of the build every release depends on, and its correctness is decided by whether an already released record still replays to its bound bytes. Acceptance also covers the SPEC-RLO-004, ARCH-RLO-004 and VER-RLO-004 amendments framed in the work order, and declines any non-POSIX refusal or warning."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T16:15:49Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-27: start WO-RLO-008."
+++

# Work Order: Make the recipe-bound candidate export independent of the calling host

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, and any release decision are separate accountable acts.

This work order cannot be approved on its own. `QG-G1-DEFINITION` requires
every selected active requirement under review to have selected active
specification and verification coverage. `REQ-RLO-017` has none: `SPEC-RLO-004`
and `VER-RLO-004` are active and approved, but neither selects it, and the
missing thing is the relation. `QG-G2-ARCHITECTURE` is in the same position for
`ARCH-RLO-004`, which addresses `REQ-RLO-013` and `REQ-RLO-014` only. That
coverage begins to exist only when the three amendments framed below are
accepted.

The approval act therefore decides four things at once, and the framing for all
four is in this file: accept the `SPEC-RLO-004`, `ARCH-RLO-004`, and
`VER-RLO-004` amendments, approve `REQ-RLO-017`, resolve its one open decision,
and approve this work order with `commit_bound_verification = required`.

That act was taken on 2026-08-27, and the paragraphs above are preserved as the
framing it was taken over. The four decisions had to be recorded in this order:
`SPEC-RLO-004` and `VER-RLO-004` amended, `REQ-RLO-017` approved as
`release-owner` with its open decision resolved against a non-POSIX refusal,
`ARCH-RLO-004` amended, then this work order approved as `engineering-owner`.
Writing the `ARCH-RLO-004` edge first invalidates the whole graph — `E016`
refuses an active architecture that addresses an inactive requirement — and that
invalid graph blocks the requirement's own approving transition with `WEX201`.
Start, completion, commit-bound verification, and any release decision remain
separate accountable acts.

## Objective

Make `repository_tools.release_build` hand every producer instance the
committed candidate bytes and one declared file-mode set, whatever host
launched the build, so that a recipe replay is a function of the candidate and
the recipe alone.

Today it is not. `_safe_extract_candidate` runs `git archive` under the
caller's effective configuration, and the exported tree reaches the producer
through a bind mount whose mode semantics belong to the host filesystem. On a
Windows workstation with a `core.autocrlf=true` clone, the 0.7.0 build of
record was produced twice, agreed with itself, and was wrong: 83 of 111 wheel
entries carried CRLF and 69 were recorded executable. `RLS-SEH-014` was bound
to those bytes and had to be rejected after hosted replay `33015517991`
disagreed; `RLS-SEH-015` was rebuilt on a Linux host and confirmed by
`33016585047`.

## In scope

- In `_safe_extract_candidate`, disable Git line-ending conversion for the
  export invocation, so the exported bytes equal the committed blob bytes in
  any clone. `_run_git` already forwards arbitrary leading arguments, so this
  is `-c core.autocrlf=false -c core.eol=lf` ahead of `archive`.
- In `_producer`, after the existing input-presence check and before the first
  recipe command, establish the declared mode set on the source tree: `0o775`
  for directories, `0o664` for files. It is done there and not on the host
  because a Windows filesystem does not retain a POSIX mode: a host-side
  `chmod 0755` is read back as `0o777` by Windows itself and presented to the
  container as `0777`, while the same call inside the container is retained.
  `_producer` is supplied from the calling working tree rather than from the
  recipe, so this is not a recipe change and no bound recipe digest moves.
- Tests in `tests/test_release_build.py`: exported bytes equal the committed
  blob in a `core.autocrlf=true` clone and in a clone with `core.eol=crlf`; a
  path carrying a `text eol=lf` attribute is unaffected; the declared mode set
  is established on the producer's source tree including where the incoming
  tree already carries wrong modes; the existing determinism, hash, and
  hand-back tests are unchanged.
- The three governing amendments framed below, applied as part of the approval
  act.
- `docs/notes/developing-se-harness.md`: the `Building and releasing` and
  `Release sequences` text says that the build of record is host-independent
  and names the two mechanisms that make it so. Issue #189 asks for the
  opposite instruction — that the build must run on a Linux host — and that
  request is answered by the change rather than written down.
- `docs/engineering/release-orchestration/README.md`: one bullet in the
  build-recipe packet.
- Evidence under `evidence/WO-RLO-008/`.

## Out of scope

`release/build-recipe.json`, `release/build-toolchain.lock`, the producer
image, the toolchain, the closed environment, the command arrays, and the
normalizer contract. Mode normalization in `scripts/normalize_sdist.py` or in
the recipe's `normalization` block: it would move the recipe digest every
existing record binds, and it is unnecessary, because the declared mode set is
already the set a POSIX export produces.

The bound hashes of any record, any lifecycle transition, any workflow file,
`scripts/replay_release_build.py`, and the RCA document for `RC-070-01`, which
issue #189 names and which does not yet exist. Extracting the candidate inside
the producer rather than on the host is a cleaner form of the same fix and is
deliberately not taken here: it moves the archive-member validation across the
producer boundary, and the smaller change reaches the same measured result.

The cross-platform publication rehearsal of issue #111 remains separate.

## Authorized decision envelope

The engineering owner may choose the internal factoring of the mode response
and the test fixture form, and may additionally assert committed-blob equality
of the exported tree at run time if the cost stays bounded and the assertion
cannot be satisfied by the export it checks. The engineering owner may not
change the declared mode values, move the mode response to the host, alter the
recipe or lock, or introduce a mode normalization downstream of the export.

## Constraints

Byte preservation is a pass condition. Both edits are inert on a POSIX host:
a POSIX `git archive` already writes LF, and a POSIX export already produces
`0o775` directories and `0o664` files, so the mode response is a no-op there.
Every already bound record must continue to replay to its bound bytes, and the
hosted lanes and the publication rehearsal, which supply the producer script
from the review ref while taking the source from the bound candidate commit,
must be unaffected.

No byte of the distributed surface changes; `repository_tools` is not packaged.

## Expected change surface

Two edits in one file, both inside `repository_tools/release_build.py`; tests;
three governing amendments; two note passages; one README bullet; evidence.

## Amendment framing

The following three amendments are proposed for acceptance in the approval act.
None relaxes a pass condition and none changes an approved `statement` field.

**`SPEC-RLO-004`** gains `REQ-RLO-017` in `specifies`, one behavioral rule
after rule 20, and one error row:

> 21. Candidate export is host-independent. The interpreter exports the exact
>     candidate with Git line-ending conversion disabled for that invocation,
>     so the exported bytes equal the committed blob bytes in any clone. The
>     source tree each producer instance builds from carries one declared mode
>     set — `0o775` for directories and `0o664` for files — established from
>     inside the producer boundary, because a non-POSIX host cannot retain a
>     POSIX mode. No host platform, Git configuration, or filesystem fact
>     reaches an accepted output.

> | Declared source mode set cannot be established inside the producer | fail before the first recipe command; no accepted output and no RLS write |

**`ARCH-RLO-004`** gains `REQ-RLO-017` in `addresses`, one required pattern
(conversion-free candidate export and a declared source mode set established
inside the producer boundary), one prohibited pattern (relying on host Git
configuration or host filesystem mode semantics for the source a producer
builds), an extension of the host trust boundary to name those two facts, and
one conformance check for the export-byte and source-mode matrices.
`ADR-RLO-004` is not reopened: the recipe, producer, and interpreter decision
it records is unchanged, and this amendment removes a way the implementation
departed from it rather than deciding anything new.

**`VER-RLO-004`** gains `REQ-RLO-017` in `verifies`, three matrix rows, one
acceptance scenario, and two property bullets:

> | REQ-RLO-017 | export byte matrix | export from clones with `core.autocrlf` false, true, and input, a clone with `core.eol=crlf`, and a path carrying a `text eol=lf` attribute | every exported file equals its committed blob bytes in every clone |
> | REQ-RLO-017 | source mode matrix | POSIX export, non-POSIX bind-mount presentation, and an incoming tree already carrying wrong modes | the tree the producer builds from carries `0o775` directories and `0o664` files in every case; failure to establish it fails before the first recipe command |
> | REQ-RLO-017 | host-independence rebuild | full replay of `RLS-SEH-015` on a POSIX host and on a Windows host, plus the negative control with the mode response removed | both hosts reproduce the bound wheel and sdist identities; the negative control reproduces neither |

> 7. Replay an already released recipe-bound record from a non-POSIX host and from a POSIX host and prove both reach the bound identities, then remove each half of the change in turn and prove each removal breaks the reproduction.

> - Exported candidate bytes equal committed blob bytes independently of clone configuration.
> - The source tree a producer builds from carries the declared mode set independently of host filesystem mode semantics.

## Required verification

`VER-RLO-004` as amended, including the three new rows and scenario 7;
repository-required checks; the full suite on both platforms with a control run
at the same commit; the publication rehearsal's `candidate` job green on the
pull request; the handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/release-orchestration/evidence/WO-RLO-008/`:

- The pre-change readings taken on 2026-08-27 on the Windows workstation:
  1477 of 1559 exported files carrying CRLF, the 82 exceptions being exactly
  the `.gitattributes` `text eol=lf` paths; zero after the export change;
  every blob at the candidate at mode `100644`; the released 0.7.0 wheel
  recording 70 entries at `0o100664` and 41 at `0o100644`; the Windows-built
  wheel recording 69 at `0o100777`.
- The full Windows replay of the `RLS-SEH-015` candidate with both edits,
  reaching wheel `e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3`
  and sdist `7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617`,
  state `exact`.
- The negative control with the export change alone, reaching wheel
  `57542dd803392cd858b41c45df71c6fb1f4c64455429f66e686df9c94cc284ef` and sdist
  `3f6eded3f04a96d3fbc0b1d61899159474b55025363c841c0118c846fbcbede3`, which
  establishes that the mode response is load-bearing rather than defensive.
- The host-versus-container mode readings that decide where the mode response
  belongs.
- Focused and full test commands and counts, the control run, formal
  validation, deviations, residual risks, and every unperformed lifecycle and
  external action.

The three pre-change readings above were taken during analysis, before this
work order existed, on the merge commit `7284743`. They are recorded as
analysis measurements and are re-taken at the implementation commit; a reading
older than the commit under assurance is not evidence for it.

## Stop and escalate conditions

Stop if a POSIX replay of `RLS-SEH-015` stops reproducing its bound bytes; if
the declared mode set cannot be established inside the pinned producer image;
if the fix appears to require a recipe, lock, or normalizer change; if a
committed blob carrying the executable bit is found at any candidate a bound
record names, which would falsify the flat mode set; or if the owner retains a
non-POSIX refusal, which contradicts `REQ-RLO-017`'s acceptance example and
requires the requirement to be redrafted rather than reinterpreted.

## Completion report format

The `harnessctl check . --artifact WO-RLO-008 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.

+++
id = "REQ-RLO-017"
type = "requirement"
title = "Present host-independent candidate source to the release producer"
status = "approved"
owners = ["release-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN the recipe-bound release interpreter prepares the exact candidate for a producer instance, THE SYSTEM SHALL present the committed bytes and one declared file-mode set to that producer on every host platform, and SHALL NOT allow the calling host's platform, Git configuration, or filesystem to reach the produced distributions."
verification_method = "automated-test-and-exact-rebuild"

[relations]
derives_from = ["CAP-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:12:33Z"
decided_by = "release-owner"
reason = "Owner decision 2026-08-27: approve REQ-RLO-017. The open decision is resolved by declining any non-POSIX refusal or warning; the build is made correct on every host."
+++

# Requirement: Present host-independent candidate source to the release producer

## Rationale

`ARCH-RLO-004` already declares a host boundary: host environment, user configuration, caches, absolute paths, and runner-selected Python do not enter accepted build identity. The implementation does not achieve it. Two host facts reach the producer through the exported source tree, and both changed the accepted bytes of the 0.7.0 release.

1. `repository_tools.release_build._safe_extract_candidate` exports with `git archive` under the caller's effective Git configuration. In a `core.autocrlf=true` clone the export converts every text file the checkout converts. 83 of the 111 entries in the wheel built that way carried CRLF.
2. The exported tree reaches the producer through a bind mount. A Windows bind mount presents every entry as mode `0777`, and both `python -m build` and `scripts/normalize_sdist.py` record member modes verbatim, so 69 wheel entries were recorded executable. `normalized_member` in the normalizer sets name, mtime, ownership, PAX headers, link name, and device numbers, and deliberately does not set `mode`; the recipe's `normalization` block declares no mode expectation. Nothing downstream of the export corrects a mode.

Neither fault is detectable inside a replay. Builds A and B are exported from the same host, so they agree with each other byte for byte and `SPEC-RLO-004` rule 18's internal-equality comparison passes. `source_manifest_sha256` hashes `git ls-tree -r --full-tree` output, which is committed blob identity and is blind to what the export wrote. The only check that fails is the comparison against already accepted hashes, so a first accepted build carries the fault silently and a later independent replay contradicts it. That is the recorded sequence: locally accepted bytes bound to `RLS-SEH-014`, hosted replay `33015517991` failing, `RLS-SEH-014` rejected, and `RLS-SEH-015` bound to a Linux-built candidate and confirmed by hosted replay `33016585047`.

The obligation is a property of the exported source, not a rule about hosts. A host restriction recorded in a note cannot carry it, because a note cannot fail a build, and the failure it is meant to prevent is one that looks like success everywhere except in the one comparison that runs last.

## Preconditions and trigger

Every recipe-bound build or replay of a schema-2 record or candidate: local creation under an approved release-bearing work order, hosted pre-release replay, publication rehearsal, and production qualification. The trigger is source preparation for one producer instance, before any recipe command executes.

## Required response

1. Export the exact candidate with Git line-ending conversion disabled for that invocation, so the exported bytes equal the committed blob bytes for every path whatever the caller's `core.autocrlf`, `core.eol`, or per-path attributes are.
2. Establish one declared mode set on the source tree the producer builds from, applied from inside the producer boundary. A non-POSIX host cannot store POSIX modes, so an equivalent action taken on the host is not a substitute: a mode set on a Windows filesystem is not retained, is reported back as `0777`, and is presented to the container as `0777`.
3. The declared mode set is `0o775` for directories and `0o664` for files. These are the modes a POSIX `git archive` export already produces, so no accepted byte of an existing record changes.
4. Apply both to build A and build B identically and without shared state.

## Failure and boundary behavior

An export that cannot disable conversion, or a source tree the producer cannot bring to the declared mode set, fails the build before any recipe command runs. The failure names the identity class and neither substitutes a host build, relaxes a comparison, updates an expected hash, edits a record, nor exercises a lifecycle or external action.

This requirement adds no accepted mode normalization downstream of the export. The wheel and sdist continue to record whatever modes the producer's source tree carries; the obligation is that those modes are declared and host-independent rather than observed and accidental.

## Constraints

- `release/build-recipe.json`, `release/build-toolchain.lock`, the producer image, the toolchain, the closed environment, the command arrays, and the normalizer contract do not change. The recipe digest bound by every existing record must not move, and the producer script is supplied from the calling working tree rather than the recipe, so a change to it is not a recipe change.
- Byte preservation is a pass condition, not an expectation: a replay of `RLS-SEH-015` must still reproduce wheel `e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3` and sdist `7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617` on a POSIX host, and must reproduce them on a non-POSIX host as well.
- A flat mode set is correct only while no committed blob carries the executable bit. Every blob at the 0.7.0 candidate is mode `100644`. Work that introduces a committed executable file must replace the flat set with a derivation from the committed mode, and this requirement is the place that constraint is recorded.
- `repository_tools/` is not packaged. No byte of the distributed surface changes.
- The cross-platform rehearsal of the credential-free publication path remains the separate scope of `REQ-RLO-015`, `REQ-RLO-016`, and issue #111. This requirement governs the build's source input, not the platform coverage of the lane that calls it.

## Acceptance examples

### Example: normal behavior

**Given** a Windows host with a `core.autocrlf=true` clone and a bind-mounting container runtime

**When** the interpreter replays `RLS-SEH-015` from its bound candidate commit

**Then** builds A and B agree with each other and both hashes equal the bound wheel and sdist identities, and the same replay on a POSIX host reproduces the same two hashes.

### Example: failure behavior

If the export cannot be made conversion-free, or the producer cannot establish the declared mode set on its source tree, the build fails before the first recipe command with the failed identity class named, and no expected hash, record, lifecycle state, or external resource changes.

## Open decisions

None. GitHub issue #189 asks that `repository_tools/release_build.py` refuse or warn loudly on a Windows host. This requirement instead makes a Windows host produce the correct bytes, which was measured on 2026-08-27 to reproduce both `RLS-SEH-015` identities exactly, and to reproduce them only when both the export and the mode response are present.

The accountable repository owner resolved the question on 2026-08-27 by declining to retain either a non-POSIX refusal or a non-POSIX warning. A refusal would contradict this requirement's own normal-behavior acceptance example and would falsify `tests/test_release_build.py::test_hand_back_is_skipped_on_a_non_posix_host`, which asserts that a full replay succeeds with `_is_posix` patched false. A warning would change no outcome, and a warning nobody read was part of how the 0.7.0 fault survived. The change of intent is recorded against issue #189 rather than leaving the issue's stated remedy silently unimplemented.

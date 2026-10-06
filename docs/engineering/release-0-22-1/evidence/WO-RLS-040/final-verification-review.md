# Verify evaluator 0.22.1 and plugin 0.2.6

**Requested decision:** verify VREC-SEH-033 for candidate
`4f640284ec496b88cd7aa4ba88ca537d9374a2f8` as assurance owner.
The record remains `ready` until mmzen makes that decision.

The candidate combines standalone draft validation, actual-human attribution
for legacy ownership labels, the 4 MiB dashboard limit and the missing-draft-evidence
transition correction. It stages both plugin 0.2.6 packages. It excludes the
unfinished Hosted Artifact Graph service and does not adopt the new evaluator.

## Scope and exact identities

The selected work is WO-HAG-002, WO-HAG-003, WO-DST-028, WO-RLS-040, WO-RLS-041
and WO-RLS-043. All six are implemented. Verification covers VER-HAG-002,
VER-HAG-003, VER-DST-030, VER-RLS-036, VER-RLS-037, VER-RLS-004 and VER-IAR-021.
This is exactly the approved REL-SEH-035 membership. WO-RLS-042 and VER-RLS-038
cover later public delivery and are outside this verification record.

| Item | Exact identity |
| --- | --- |
| Candidate | `4f640284ec496b88cd7aa4ba88ca537d9374a2f8` |
| Released governor | 0.22.0, separate isolated environment |
| Wheel SHA-256 | `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053` |
| Sdist SHA-256 | `beea95b6431ae35d383789181fc59d1aae80efdab70d517b2dedf8782dfdc240` |
| Payload SHA-256 | `0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff` |
| Bundle SHA-256 | `e5c5b9682573320f239c8286c36510cb85a63184f02b3cff3bd8980b0cabf475` |
| Marketplace parent | `7d30907f15bd7e06fb632e1ebf4e88e01b68726c` |
| Staged marketplace commit | `85ae003769f53908addbdcf46c820a8af530ac24` |
| Staged tree | `0069f9012fc6f6270410bfebbb673831d8745550` |
| Package identity SHA-256 | `4a62e5bb6a3ffb36ca723dca8fe3e71588d050bab70c5b1f11778dabb532249d` |

The marketplace commit has one parent and all 69 Git blobs match the selected
Windows staging tree. It is review material; the public marketplace branch has
not changed. Windows and Linux staging/check-stage pass. Expanded files and ZIP
metadata match; compressed ZIP bytes differ across runtimes. The exact Windows
archives are selected, without a cross-runtime compressed-byte claim.

## Checks and acceptance criteria

| Contract / criterion | Actual result and evidence |
| --- | --- |
| VER-HAG-002: draft admission, typed links, invalid inputs, no-write behavior | Final Windows/Linux source suites pass the normal/refusal cases. The final installed wheel passes eleven decisive CLI scenarios on both platforms. Shared rule implementation and preserved historical evidence remain in the correction review. |
| VER-HAG-003: actual human and owner binding | Final installed Windows/Linux probes pass valid mapping, atomic refusals, terminal replay and paired-risk cases. The real DEC-HAG-001 remains unchanged. |
| VER-DST-030: exact 4 MiB limit and preserved definitions | Installed below/equal/above cases pass on both platforms. Actual candidate topology is 2,175,176 bytes, leaving 2,019,128 bytes below the target. Two generated bundles match. All eleven preserved predecessor revisions match their hashes. |
| VER-RLS-004: absent unrelated draft evidence | The original approved-baseline fixture passes final installed Windows/Linux preview/apply. Only selected work changes; the unrelated draft remains byte-identical and its absent evidence stays absent. Stale-input, unsafe-path and rollback tests pass in the full suites. Earlier real Claude recovery and second-checkout walkthrough are reused only with the byte-equivalence assessment below. |
| VER-RLS-036: Windows source | Python 3.14.6: 1,293 tests, 23 reported skips, exit 0. Skips remain visible. |
| VER-RLS-036: Linux source | Python 3.12.3: 1,293 tests, 2 reported skips, exit 0. Linux executes the unsafe-link case skipped on Windows. |
| VER-RLS-036: portable archives | Wheel and sdist installed identity, init, doctor and validate pass on both platforms. CLI smoke and 22 distribution-record checks pass. |
| VER-RLS-036: reproducibility and upgrades | Two local pinned builds and two independent GitHub pinned builds produce identical wheel and sdist bytes at this candidate. Two actual 0.22.0-to-0.22.1 upgrade rehearsals per platform pass with the same semantic digest. |
| VER-RLS-036: CI | Required PR jobs pass. Manual run 37260735124 passes exact candidate replay, historical RLS-SEH-032 replay and complete-delivery/recovery rehearsal. The historical leg does not claim a new 0.22.1 release record. The two PR-policy skips are separately exercised in that manual run. |
| VER-RLS-037 / VER-IAR-021: exact staged hosts | Fresh final-package Codex CLI 0.159.2 and Claude Code 2.1.273 tests pass bootstrap above a clone, activation, startup, resume, manual compaction and observed automatic compaction. Owner files are preserved. The disposable Codex profile was restored. |
| VER-IAR-021: isolation, switching, gaps and repeated work | Prior native boundary and two-checkout walkthrough observations are retained at their original tested identity. All 125 expanded wheel members and executable/resource host files match the final package. Fresh final-package installation/delivery tests separately cover the changed archive and provenance identity. Source suites cover concurrent setup, offline resources, interruption and refusal boundaries. |
| VER-RLS-036/037: documentation and staged delivery inputs | Both manifests select 0.2.6. Current guidance and package ownership checks pass. The approved contract identifies all five surfaces, and exact candidate/staging identities are retained. The final RLS and frozen delivery plan follow verification; no executable-ready or public-availability claim is made. |
| VER-RLS-036: provider readiness | The separately authorized pypi reviewer-only change was applied and read back. Main-only deployment, main protections and workflow permissions remain unchanged. mmzen confirmed the four PyPI Trusted Publisher fields; this is human account-side confirmation, not an authenticated agent read. |
| Codex Windows desktop | **Not run / unverified.** mmzen accepted the release-only omission and risk through DEC-RLS-009 and RISK-RLS-007. CLI results do not count as desktop evidence. |

The [manual rehearsal](https://github.com/mmzen/se_harness/actions/runs/37260735124)
used the exact candidate. PR merge-checkout CI is additional integration evidence,
not a replacement for these exact-candidate builds and tests.

## Reuse and retained failures

The earlier native isolation, switching, delivery-gap, context-boundary and
two-checkout workflow tests used source `061307929c94314ccd2beb4a53f174e536fceba8`.
The final wheel has identical expanded member bytes and payload identity. The
host adapters, hooks, skills and resources are identical; only assembly provenance
and the wheel container identity changed. The explicit comparison is in the
final evidence archive. Earlier tests retain their original source, wheel and
fixture identities; they are not described as fresh runs at the final commit.

Original evaluator defects and failures remain in the preceding correction
archives. During final qualification, the transition probe first tried to start
the already-completed live fixture. The evaluator correctly refused. Restoring
the immutable pre-execution baseline plus the exact retained draft allowed both
platform probes to pass. The original live fixture was not reset or edited.
A second Linux attempt encountered a previously-created draft-probe directory;
its already-passing draft/topology results were reused and the remaining tests
completed. Both failed attempts remain visible.

The first verification capture also refused a test runtime whose distribution
metadata resolved outside the candidate. No record or state changed. Capture
was retried with a clean source-test environment and the same candidate and
evidence. This changes test setup, not the product or governor.

## Accepted limitation and remaining decisions

A desktop-specific instruction or checkout-selection defect could remain
undetected. [The recorded desktop acceptance](../WO-RLS-041/desktop-deferral-review.md)
applies only to evaluator 0.22.1 / plugin 0.2.6. mmzen owns follow-up before the
next plugin release or any verified-desktop claim, whichever comes first.
The other CLI and public fresh/update checks remain required.

No hosted service scenario ran. HAG ownership, selected decision, pinned
definitions and PR #535 target remain unchanged. Public fresh-install/update
observations, exact release-record replay, final delivery-plan approval, merge
and publication remain downstream. Verification of this record accepts the
assessed candidate; it does not supply any of those decisions or claim adoption.

## Evidence binding and review

- [Ready VREC-SEH-033](../../verification-records/VREC-SEH-033.md).
- [Final evidence receipt](final-evidence-receipt.json), SHA-256
  `1552249eca44eff719615f57152e52064d8dc1f7f70ab17d946616ca02a71da2`.
- [Final raw archive](final-qualification.zip), SHA-256
  `ec57e2e8585a76523a033e32cd2d63a34de02926c6904dd3e8616d8db0ce11b1`.
- [Final bundle](final-bundle.json), [build replay](final-build-replay.json),
  [marketplace identity](final-package-identity.json) and
  [staging commit](final-marketplace-staging.json).
- [Capture observations](final-capture-observations.zip), including the refused
  runtime, clean retry, exact command, output and transient test helpers.
- [Historical correction review](../WO-RLS-043/corrected-qualification-review.md)
  and its unchanged raw archives.

The final observations were collected after the candidate commit. The committed
capture command checks their byte digests and freshly qualifies a temporary
checkout of that exact commit. Its generated record binds the receipt digest in
the command and output. The same receipt and raw archive are retained in the
later review commit; they are not claimed to have existed in the earlier candidate.
The generated evaluator provenance and all earlier bound evidence remain unchanged.

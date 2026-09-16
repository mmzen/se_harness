```toml
artifact = "WO-DOC-016"
checkpoint = "handoff"
formal_snapshot_sha256 = "487630a368c6868ba705bfad1f537970d23dac0a554f3757ba9b6a5e0fa06b00"
rebound_at = "2026-09-16T06:02:06Z"
```

# WO-DOC-016 implementation evidence

## Result and reviewed input

The root README now introduces the SE Harness checker and the Verity Plane plugin,
places the published Codex and Claude Code commands before the workflow and vision,
explains offline setup of the bundled released 0.18.0 evaluator, and retains the
PyPI route, required documentation links, logo and both Explorer images.

README.md is byte-for-byte equal to [the approved input](approved-readme.md):
SHA-256 `d9cb469ccda4438134ee23b46852a58ecc91595dd2ce87437f4967a4ea1a7c8b`.
It remains 593 source words, 108 lines and six level-two headings. The owner
approved this input, VER-DST-029 and WO-DOC-016 by replying "i approve" to the
review package. [Reviewed hashes](reviewed-inputs.json) retain the original draft
identities; lifecycle history records the actual applied decisions.

## Observed checks

Checks ran on Windows 11 with Python 3.13.3, candidate source 0.19.0 and the exact
isolated released 0.18.0 governor selected by the repository. Argument arrays,
working directories, timestamps, exit codes and outputs accompany this packet.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Source regression suite | 1,068 tests, 171 classes, 8 workers; exit 0; 15 skips; 515.260 seconds | [Command](source-suite.json), [output](source-suite.log) |
| Existing public onboarding and progressive documentation tests | 30 tests, exit 0 | [Command](documentation-tests.json), [output](documentation-tests.log) |
| Release-distribution validation | 15 distribution-bearing records, exit 0; no build or publication | [Command](distribution-validator.json), [output](distribution-validator.log) |
| Candidate CLI help | Exit 0 | [Command](candidate-help.json), [output](candidate-help.log) |
| Released init/doctor syntax | Both README forms parsed, exit 0; no project mutation | [Command](released-command-syntax.json), [output](released-command-syntax.log) |
| Released doctor | 70 checks, no failed checks | [Result](readme-016-doctor.json) |
| Released graph validation | 1,651 artifacts, zero errors; unrelated warnings are not findings of this work | [Result](readme-016-graph.json) |
| Start and review preflight | Both ready, no diagnostics | [Start](readme-016-start-preflight.json), [review](readme-016-review-preflight.json) |
| Git-derived scope check | Passing against base 851afecbb2faac1b12e94f9d74bd24b3129fced8 | [Result](readme-016-scope.json) |
| Diff whitespace | Exit 0; ordinary local autocrlf notices only | [Command](diff-review.json), [output](diff-review.log) |
| Exact inputs and plugin facts | README input and all three images match; native commands and version claims match the immutable published distribution | [Command](input-comparison.json), [output](input-comparison.log) |
| Visual review | Owner-reviewed render reused after exact README and image comparison; readable commands and headings, all images loaded, no horizontal overflow | [Observation and render hashes](render-review.json) |

The full suite includes deliberately failing runner-invocation scenarios, so its
raw output contains an expected "--workers must be at least 1" message. Its final
aggregated verdict is OK with exit 0; that message is not a failed suite run.

## Reused plugin evidence

The four native commands match both the distribution at
`ed68b30c88043773be929540b7b10ae537957c2d` and the retained
[public Git acceptance](../../../plugin-integration/evidence/WO-PLG-023/publication-2026-09-15/README.md).
The package identity digest is
`fc9d0c585b104e6ef2ba4598e38ffeade0191e3aeae1658f9df4830244b37e58`.
Its manifest identifies plugin 0.1.0 and released evaluator 0.18.0. The two native
setup scripts are identical and use --no-index and --no-deps. Neither script,
wheel, plugin manifest nor install command changed in this work, so the existing
Windows acceptance is reused with these explicit comparisons.

## Implementation review

The change satisfies REQ-DST-069 and SPEC-DST-024 without amendments, runtime
changes, new tests, or new installation mechanisms. Existing checks still cover
links, budgets, public command syntax, images and authority boundaries. Keeping
those checks and shortening the vision made this a direct README replacement;
detailed setup stays in the existing distribution guide.

The only implementation changes are README.md and the domain index. The new
work order, verification contract and this evidence support that change. The
product code, tests, managed root, plugin distribution and historical artifacts
remain unchanged. Both publication branches remain present at their observed
identities. No unresolved implementation finding was identified in this scope.

## Limits and next lifecycle steps

This evidence covers documentation and reuses the stated native Windows results.
No new model-driven session, other-platform plugin acceptance, provider submission,
package release or public README publication is claimed. The local HTML review is
not a live GitHub readback. The source suite used its standard reduced-scale mode;
its 15 skips remain visible in the aggregate result.

A passing Git-derived handoff result is retained beside this packet. Completion
is recorded under the work-order approval after that gate passes. A later ready
VREC-DOC-008 binds the clean candidate commit and explicitly selected evidence;
its assurance decision remains with the owner. Candidate and governance commits
must be separate. No push, PR or merge is authorized by this work order.

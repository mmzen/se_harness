+++
id = "RLS-SEH-019"
type = "release_record"
title = "Release candidate 0.10.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-29"
updated = "2026-08-29"
version = "0.10.0"
commit = "69ee77a673a25a28535a03ebfaa5c29b454e1f5f"
git_object_format = "sha1"
prepared_at = "2026-08-29T10:15:42Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-10-0/evidence/RLS-SEH-019-evaluator.json"
evaluator_evidence_sha256 = "e78737d57a52748c0381cddd376cd8627a9328f600210a957e5ddd308ef48d91"
tag = "v0.10.0"

released_at = "2026-08-29T10:19:01Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787997718
wheel = "se_harness-0.10.0-py3-none-any.whl"
wheel_sha256 = "e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3"
sdist = "se_harness-0.10.0.tar.gz"
sdist_sha256 = "e3b8eaf691db34ec39434726020c347cfa0d19a58f559e8c0da86fe53e97c7ba"
checksums = "SHA256SUMS"
checksums_sha256 = "b11a7b03ecd3549acb1dfe43a1598265853b2307154281352197008705191da6"
source_manifest_sha256 = "50856d4dc5c0d2e01b77666943133710d9d62167e899a49c02f9c0cc72d7ac8d"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-021"]
includes_verification = ["VREC-SEH-019"]
releases_work = ["WO-ECP-012", "WO-ECP-013", "WO-ECP-014", "WO-HUP-009", "WO-RLS-016"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-08-29T10:19:01Z"
decided_by = "release-owner"
reason = "Released on 2026-08-29 by the accountable release owner, 'release RLS-SEH-019'. Re-measured immediately before this transition, every check run before this reason was written: candidate commit 69ee77a is an ancestor of the branch tip with a clean worktree; VREC-SEH-019 is verified and binds the same candidate; the record's bound wheel e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3 and sdist e3b8eaf691db34ec39434726020c347cfa0d19a58f559e8c0da86fe53e97c7ba equal the retained bundle manifest's, which binds the same candidate; the hosted release-candidate-replay dispatch on this review ref (run 33247433710) completed success, rebuilding the bound recipe twice without credentials and reading release build replay PASS for RLS-SEH-019. Two lanes are red at this head by known conditions, each measured in its log: the release-record rehearsal expects exactly one RLS-SEH-019 at main head and finds 0 until this pull request merges, exactly as RLS-SEH-018 behaved; the managed lane runs the 0.9.0 root's handoff-only step against an implemented work order, issue #255, repaired by WO-ECP-013 in this release. Every other lane passes. Releasing authorizes the publication sequence of REL-SEH-021's promotion policy; the tag, the GitHub Release, PyPI, Pages and the maintenance line remain the separately dispatched last mile, and the pypi environment remains a separate human approval."
+++

# Release Record Candidate

This ready record proposes release `0.10.0` for `WO-ECP-012`, `WO-ECP-013`, `WO-ECP-014`, `WO-HUP-009`, `WO-RLS-016` from candidate commit `69ee77a673a25a28535a03ebfaa5c29b454e1f5f`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-025"
type = "release_record"
title = "Release candidate 0.16.0"
status = "ready"
owners = ["release-owner"]
created = "2026-09-07"
updated = "2026-09-07"
version = "0.16.0"
commit = "c103708a070fdaec90b8594c3fabb193eaf99b59"
git_object_format = "sha1"
prepared_at = "2026-09-07T09:34:57Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-16-0/evidence/RLS-SEH-025-evaluator.json"
evaluator_evidence_sha256 = "8c10a3ea2956baff8bfa875c658a98aa7db772f924b38557ad05c819a5f88a2d"
tag = "v0.16.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788770722
wheel = "se_harness-0.16.0-py3-none-any.whl"
wheel_sha256 = "a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae"
sdist = "se_harness-0.16.0.tar.gz"
sdist_sha256 = "25d08fa133e5bf5418b7ade2af995aaf71634422aef775dc55cbdeb32655d581"
checksums = "SHA256SUMS"
checksums_sha256 = "ba09502402b03c2b017ab32ae235324a9204670a8951e0717a327f15385be62c"
source_manifest_sha256 = "8153df9595efd77b8f300e0540b0c4512a441beafb395c45855e48ba50a45a1b"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-027"]
includes_verification = ["VREC-SEH-025"]
releases_work = ["WO-DST-024", "WO-ECP-026", "WO-HUP-016", "WO-RLS-022", "WO-TCM-009", "WO-TCM-010"]
+++

# Release Record Candidate

This ready record proposes release `0.16.0` for `WO-DST-024`, `WO-ECP-026`, `WO-HUP-016`, `WO-RLS-022`, `WO-TCM-009`, `WO-TCM-010` from candidate commit `c103708a070fdaec90b8594c3fabb193eaf99b59`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

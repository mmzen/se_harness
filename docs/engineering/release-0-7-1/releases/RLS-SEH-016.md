+++
id = "RLS-SEH-016"
type = "release_record"
title = "Release candidate 0.7.1"
status = "ready"
owners = ["release-owner"]
created = "2026-08-27"
updated = "2026-08-27"
version = "0.7.1"
commit = "58efcaa1dfbb8f5921e82c72b6cc40add0c9a36c"
git_object_format = "sha1"
prepared_at = "2026-08-27T16:37:19Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-7-1/evidence/RLS-SEH-016-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"
tag = "v0.7.1"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787848493
wheel = "se_harness-0.7.1-py3-none-any.whl"
wheel_sha256 = "ddd403cde17fc3770460809cbe8f9edb68f47c3aaa0422fe021334279994225d"
sdist = "se_harness-0.7.1.tar.gz"
sdist_sha256 = "e687c43fe518e93ef6f4793caa2d3c5f7f6e709b48fc972d0afbe4ebc25c95c6"
checksums = "SHA256SUMS"
checksums_sha256 = "4134f06f090b6aefbed6091cba933cda6ffc2c577689926fbaf1ca9bb325b53f"
source_manifest_sha256 = "85b915fd7e975d708170200a44d4b5e8e7ee1c78016946b7be93b4e126b9fc62"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-018"]
includes_verification = ["VREC-SEH-015"]
releases_work = ["WO-REB-024", "WO-REB-025", "WO-REB-026", "WO-REB-027", "WO-RLS-013"]
+++

# Release Record Candidate

This ready record proposes release `0.7.1` for `WO-REB-024`, `WO-REB-025`, `WO-REB-026`, `WO-REB-027`, `WO-RLS-013` from candidate commit `58efcaa1dfbb8f5921e82c72b6cc40add0c9a36c`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-023"
type = "release_record"
title = "Release candidate 0.14.0"
status = "ready"
owners = ["release-owner"]
created = "2026-09-02"
updated = "2026-09-02"
version = "0.14.0"
commit = "09625e41e6b8dc10ea07a601e5ce4ea21e0d5d14"
git_object_format = "sha1"
prepared_at = "2026-09-02T09:50:27Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-14-0/evidence/RLS-SEH-023-evaluator.json"
evaluator_evidence_sha256 = "21ded06932d284d3ab2145b5ba7b9d5d3fc40997da8b047f7fb6f9f164910044"
tag = "v0.14.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788341712
wheel = "se_harness-0.14.0-py3-none-any.whl"
wheel_sha256 = "70d438b501d374fec06f41e25571f674b3cd1f43178389e6e06b0269c92f4856"
sdist = "se_harness-0.14.0.tar.gz"
sdist_sha256 = "dcb3523a0ba7118a6f04f2a041be0652e2b30eea535c2a26a89729c30f96df8f"
checksums = "SHA256SUMS"
checksums_sha256 = "fe261ef9df03b1abb28cad37a8a8c56fdb39cab152d2e5547263e21c86191e9b"
source_manifest_sha256 = "0af09311f2c3708237fd3856f78ce2634db1e6ac4677c9d40ac0f5e3ec279198"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-025"]
includes_verification = ["VREC-SEH-023"]
releases_work = ["WO-HUP-014", "WO-RLS-020"]
+++

# Release Record Candidate

This ready record proposes release `0.14.0` for `WO-HUP-014`, `WO-RLS-020` from candidate commit `09625e41e6b8dc10ea07a601e5ce4ea21e0d5d14`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

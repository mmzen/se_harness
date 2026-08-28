+++
id = "RLS-SEH-018"
type = "release_record"
title = "Release candidate 0.9.0"
status = "ready"
owners = ["Mathieu Meadele"]
created = "2026-08-28"
updated = "2026-08-28"
version = "0.9.0"
commit = "8adfe1bdeb19b4e6014b7f13afd7da5789846750"
git_object_format = "sha1"
prepared_at = "2026-08-28T22:28:09Z"
prepared_by = "Mathieu Meadele"
evaluator_evidence_path = "docs/engineering/release-0-9-0/evidence/RLS-SEH-018-evaluator.json"
evaluator_evidence_sha256 = "8d217a429db288836d69c843e6f0017c0be29a2b743f589a7fe28bfa8b1cf560"
tag = "v0.9.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787955573
wheel = "se_harness-0.9.0-py3-none-any.whl"
wheel_sha256 = "c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364"
sdist = "se_harness-0.9.0.tar.gz"
sdist_sha256 = "da80ef011572a2b0b96d1bdb920149b97014d9bb5a33de77721054188408268c"
checksums = "SHA256SUMS"
checksums_sha256 = "c5e8d1a812863f0fd85f831a235e439721c0fe50ff1deb1c9f42083c24bb892a"
source_manifest_sha256 = "6c5af56bd71c635408321144c3d028b6897540314ab6935eb46596be93e651db"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-020"]
includes_verification = ["VREC-SEH-018"]
releases_work = ["WO-ECP-001", "WO-ECP-002", "WO-ECP-003", "WO-ECP-011", "WO-HUP-008", "WO-REB-030", "WO-RLS-015"]
+++

# Release Record Candidate

This ready record proposes release `0.9.0` for `WO-ECP-001`, `WO-ECP-002`, `WO-ECP-003`, `WO-ECP-011`, `WO-HUP-008`, `WO-REB-030`, `WO-RLS-015` from candidate commit `8adfe1bdeb19b4e6014b7f13afd7da5789846750`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

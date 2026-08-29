+++
id = "RLS-SEH-020"
type = "release_record"
title = "Release candidate 0.11.0"
status = "ready"
owners = ["release-owner"]
created = "2026-08-29"
updated = "2026-08-29"
version = "0.11.0"
commit = "c5dad1046c276806b23405c72f06ab9b3a39e1f0"
git_object_format = "sha1"
prepared_at = "2026-08-29T16:17:43Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-11-0/evidence/RLS-SEH-020-evaluator.json"
evaluator_evidence_sha256 = "41578bab531e143cd9864870c9af1495aed7465eff512571387403aa734a1f26"
tag = "v0.11.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788019023
wheel = "se_harness-0.11.0-py3-none-any.whl"
wheel_sha256 = "ba26ab7be14321cdc26b69d59e2b894d544c3e7b529227de1f24ad9cd8f935c0"
sdist = "se_harness-0.11.0.tar.gz"
sdist_sha256 = "bcf8092994c1ef0ce263c3102cb92c54b3e3fb88117b080459a51640269f8a50"
checksums = "SHA256SUMS"
checksums_sha256 = "7cf72c98341c976c7049bed384e97aec791f2fb495eacacb8414c49724cd63c7"
source_manifest_sha256 = "54212e178ac8b5196788eb933a43245e35b63667680ba08fdbbd0d9199479015"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-022"]
includes_verification = ["VREC-SEH-020"]
releases_work = ["WO-ECP-006", "WO-ECP-015", "WO-ECP-016", "WO-ECP-017", "WO-HUP-010", "WO-RLS-017"]
+++

# Release Record Candidate

This ready record proposes release `0.11.0` for `WO-ECP-006`, `WO-ECP-015`, `WO-ECP-016`, `WO-ECP-017`, `WO-HUP-010`, `WO-RLS-017` from candidate commit `c5dad1046c276806b23405c72f06ab9b3a39e1f0`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

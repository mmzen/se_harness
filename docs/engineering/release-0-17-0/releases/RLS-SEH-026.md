+++
id = "RLS-SEH-026"
type = "release_record"
title = "Release candidate 0.17.0"
status = "ready"
owners = ["release-owner"]
created = "2026-09-09"
updated = "2026-09-09"
version = "0.17.0"
commit = "a9f4905dbd3ff7f0c00101906b9158d3d42f7ef6"
git_object_format = "sha1"
prepared_at = "2026-09-09T08:14:50Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-17-0/evidence/RLS-SEH-026-evaluator.json"
evaluator_evidence_sha256 = "e2cd0929fd42d0634d3bf23a73408665bac8ae473b98c81439dbffb828bff951"
tag = "v0.17.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788940609
wheel = "se_harness-0.17.0-py3-none-any.whl"
wheel_sha256 = "305c7cbc79f87baa76ea3bea939b134999f9cad3bfdfa0b4c9c2fd2d9caacced"
sdist = "se_harness-0.17.0.tar.gz"
sdist_sha256 = "dda4bc73190674f8837ab0669b6aeb205c72b9428cad052b6368ea229860c318"
checksums = "SHA256SUMS"
checksums_sha256 = "5148c154a0bd9cb5f5bd44498933836a2f00ab0253f8f7c990e36c30b21ee25b"
source_manifest_sha256 = "bd23148420a5fd50a52406cf52835001e36c24ae16071d31902e2d573e88e54b"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-028"]
includes_verification = ["VREC-SEH-026"]
releases_work = ["WO-AUT-005", "WO-CIP-007", "WO-DST-025", "WO-DST-026", "WO-ECP-027", "WO-ECP-028", "WO-ECP-029", "WO-ECP-030", "WO-ECP-031", "WO-ECP-032", "WO-ECP-033", "WO-ECP-034", "WO-ECP-035", "WO-ECP-036", "WO-HUP-017", "WO-RLS-023", "WO-RSK-010", "WO-TST-004"]
+++

# Release Record Candidate

This ready record proposes release `0.17.0` for `WO-AUT-005`, `WO-CIP-007`, `WO-DST-025`, `WO-DST-026`, `WO-ECP-027`, `WO-ECP-028`, `WO-ECP-029`, `WO-ECP-030`, `WO-ECP-031`, `WO-ECP-032`, `WO-ECP-033`, `WO-ECP-034`, `WO-ECP-035`, `WO-ECP-036`, `WO-HUP-017`, `WO-RLS-023`, `WO-RSK-010`, `WO-TST-004` from candidate commit `a9f4905dbd3ff7f0c00101906b9158d3d42f7ef6`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

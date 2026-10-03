+++
id = "RLS-SEH-032"
type = "release_record"
title = "Release candidate 0.22.0"
status = "ready"
owners = ["Codex"]
created = "2026-10-03"
updated = "2026-10-03"
version = "0.22.0"
commit = "abbec12ac5524c8adfb28693f846dd59de88f759"
git_object_format = "sha1"
prepared_at = "2026-10-03T02:34:42Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-22-0/evidence/RLS-SEH-032-evaluator.json"
evaluator_evidence_sha256 = "3f2d74a115f4f53d3b56d90b0ecab4de53d5d08270083f621ce861c4cfafc721"
tag = "v0.22.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1790980462
wheel = "se_harness-0.22.0-py3-none-any.whl"
wheel_sha256 = "44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4"
sdist = "se_harness-0.22.0.tar.gz"
sdist_sha256 = "3bc9ddb9b1d046dc111c5582b7d857cc815c8e2fb9f8255ec07bda56315ef52a"
checksums = "SHA256SUMS"
checksums_sha256 = "cbc4fca53d4c8d664716592a623e10d61bc28622580fc08ef348c4b304141c37"
source_manifest_sha256 = "8a8c0bd4ab3ba7125f18c19c8598f671b705dda6b5d70e8b74ea1dd430c2b2c3"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-034"]
includes_verification = ["VREC-SEH-032"]
releases_work = ["WO-KIS-010", "WO-KIS-011", "WO-KIS-012", "WO-KIS-013", "WO-KIS-014", "WO-RLO-014", "WO-RLO-015", "WO-RLO-016", "WO-RLO-017", "WO-RLS-034"]
+++

# Release Record Candidate

This ready record proposes release `0.22.0` for `WO-KIS-010`, `WO-KIS-011`, `WO-KIS-012`, `WO-KIS-013`, `WO-KIS-014`, `WO-RLO-014`, `WO-RLO-015`, `WO-RLO-016`, `WO-RLO-017`, `WO-RLS-034` from candidate commit `abbec12ac5524c8adfb28693f846dd59de88f759`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

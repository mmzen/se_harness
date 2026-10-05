+++
id = "RLS-SEH-033"
type = "release_record"
title = "Release candidate 0.22.1"
status = "ready"
owners = ["Codex"]
created = "2026-10-05"
updated = "2026-10-05"
version = "0.22.1"
commit = "4f640284ec496b88cd7aa4ba88ca537d9374a2f8"
git_object_format = "sha1"
prepared_at = "2026-10-05T04:21:40Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-22-1/evidence/RLS-SEH-033-evaluator.json"
evaluator_evidence_sha256 = "c293ed1f574d8278eda954dd34442c2d1283b8eb3866c080f5ca9b03d61e7f61"
tag = "v0.22.1"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1791171735
wheel = "se_harness-0.22.1-py3-none-any.whl"
wheel_sha256 = "cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053"
sdist = "se_harness-0.22.1.tar.gz"
sdist_sha256 = "beea95b6431ae35d383789181fc59d1aae80efdab70d517b2dedf8782dfdc240"
checksums = "SHA256SUMS"
checksums_sha256 = "d03e3471a42e16971e51c38e8d96092aa56d8a5cabeaf96f42637be40172a459"
source_manifest_sha256 = "47ec43395c69c59b317d5d2f2e6045d92a4776065177049f39ead86dfc1e1175"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-035"]
includes_verification = ["VREC-SEH-033"]
releases_work = ["WO-DST-028", "WO-HAG-002", "WO-HAG-003", "WO-RLS-040", "WO-RLS-041", "WO-RLS-043"]
+++

# Release Record Candidate

This ready record proposes release `0.22.1` for `WO-DST-028`, `WO-HAG-002`, `WO-HAG-003`, `WO-RLS-040`, `WO-RLS-041`, `WO-RLS-043` from candidate commit `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

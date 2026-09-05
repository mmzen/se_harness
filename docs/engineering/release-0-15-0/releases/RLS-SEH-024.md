+++
id = "RLS-SEH-024"
type = "release_record"
title = "Release candidate 0.15.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-05"
updated = "2026-09-05"
version = "0.15.0"
commit = "ba7ec5412726bd68c0317a4b6ee29927411cc1b5"
git_object_format = "sha1"
prepared_at = "2026-09-05T05:38:17Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-15-0/evidence/RLS-SEH-024-evaluator.json"
evaluator_evidence_sha256 = "35e55a43897ec79be254438dab550d99fed9d904a6d1db2d51f6a56875c4d89f"
tag = "v0.15.0"

released_at = "2026-09-05T08:08:16Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788559098
wheel = "se_harness-0.15.0-py3-none-any.whl"
wheel_sha256 = "eb09343f65a52ecc7511aacbe7f4cc546cfe4bf28eeed62cf3ff2bccf838d947"
sdist = "se_harness-0.15.0.tar.gz"
sdist_sha256 = "0ad6c0d085065aaa49128ac81690ba8426aca77870390e7fece88782420ede16"
checksums = "SHA256SUMS"
checksums_sha256 = "2b44a810f35704a337aedf684da592d2c1ba7ba505f919c863e41a1e8006fd83"
source_manifest_sha256 = "82d242b965431db1117886199a34d13b6389ebd1ad7771f127ae83b0353dc331"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-026"]
includes_verification = ["VREC-SEH-024"]
releases_work = ["WO-CIP-006", "WO-DCM-001", "WO-DOC-014", "WO-DOC-015", "WO-DPG-002", "WO-ECP-025", "WO-HUP-015", "WO-RLS-021", "WO-TCM-004", "WO-TCM-005", "WO-TCM-006", "WO-TCM-007", "WO-TCM-008"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-05T08:08:16Z"
decided_by = "release-owner"
reason = "Released by the accountable release owner on 2026-09-05 with the word 'release': REL-SEH-026 approved with an exact thirteen-gate allow-list, VREC-SEH-024 verified over every gate at candidate ba7ec54, the build of record byte-identical twice on the pinned producer (run 33923485490) and reproduced from the bound record by the credential-free hosted replay (run 33947758549, wheel eb09343f65a52ecc7511aacbe7f4cc546cfe4bf28eeed62cf3ff2bccf838d947, sdist 0ad6c0d085065aaa49128ac81690ba8426aca77870390e7fece88782420ede16), every hosted lane success at the record commit. Publication, the tag, the maintenance line, Pages and the latest markers follow through publish-pypi.yml dispatched from main after this record reaches it; the pypi environment stays a separate human decision."
+++

# Release Record Candidate

This ready record proposes release `0.15.0` for `WO-CIP-006`, `WO-DCM-001`, `WO-DOC-014`, `WO-DOC-015`, `WO-DPG-002`, `WO-ECP-025`, `WO-HUP-015`, `WO-RLS-021`, `WO-TCM-004`, `WO-TCM-005`, `WO-TCM-006`, `WO-TCM-007`, `WO-TCM-008` from candidate commit `ba7ec5412726bd68c0317a4b6ee29927411cc1b5`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

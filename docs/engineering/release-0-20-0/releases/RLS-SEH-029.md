+++
id = "RLS-SEH-029"
type = "release_record"
title = "Release candidate 0.20.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-29"
updated = "2026-09-29"
version = "0.20.0"
commit = "7253d13b212ad6f7df670021290fea32e81d66de"
git_object_format = "sha1"
prepared_at = "2026-09-29T18:26:18Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-20-0/evidence/RLS-SEH-029-evaluator.json"
evaluator_evidence_sha256 = "3d06ef9adf5b4bcb9bd9d9d93ae6ea13f35ec4f0ca9ab8338586e48254d39713"
tag = "v0.20.0"

released_at = "2026-09-29T18:39:51Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1790704430
wheel = "se_harness-0.20.0-py3-none-any.whl"
wheel_sha256 = "7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0"
sdist = "se_harness-0.20.0.tar.gz"
sdist_sha256 = "5b6784aeabdf72e0e6b43a7a2bc81244c7a9da6415cf39fbc39f440ec57d426c"
checksums = "SHA256SUMS"
checksums_sha256 = "cec4ea0130555088ea031c46e524d3e5794c3795288407177ad3cc079749e43a"
source_manifest_sha256 = "ea9f9f616b41a270da38022363eaea270ed03f53588dfde5a75c5194fbb06906"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-031"]
includes_verification = ["VREC-SEH-029"]
releases_work = ["WO-HUP-021", "WO-HUP-023", "WO-IAR-020", "WO-IAR-021", "WO-IAR-022", "WO-IAR-023", "WO-IAR-024", "WO-IAR-025", "WO-KIS-016", "WO-PLG-026", "WO-PLG-027", "WO-PLG-028", "WO-PLG-029", "WO-RLO-010", "WO-RLO-011", "WO-RLS-026"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-29T18:39:51Z"
decided_by = "release-owner"
reason = "Human release owner mmzen: \"I authorize  release record RLS-SEH-029\". Decision covers SE Harness 0.20.0 at exact candidate 7253d13b212ad6f7df670021290fea32e81d66de, all 16 work orders, verified VREC-SEH-029 and the reviewed schema-2 distribution binding. Reviewed ready record SHA-256 0dc2f82b6e756a2b91cf1650180143d5d2d4576a6250fbc73eb155eb853a3157. The 0.19.0 evaluator first refused E009 because prepared owner Codex differed from the human release role. Corrected only owners from Codex to the already approved release-owner compatibility label, as in RLS-SEH-028; prepared_by remains Codex. All other reviewed bytes and evidence are unchanged. Corrected input SHA-256 5a7948e0d7c91804e22aadaa63d47da8c6ab0803c5b9c19f260aa7862508fac6. Bound-record replay 36612357797 passed with both pinned builds matching the wheel and sdist hashes. Legacy release-owner transports mmzen's actual human decision; Codex applies it. No merge, publication, marker promotion, adoption or owner-file deletion is authorized by this decision."
+++

# Release Record Candidate

This ready record proposes release `0.20.0` for `WO-HUP-021`, `WO-HUP-023`, `WO-IAR-020`, `WO-IAR-021`, `WO-IAR-022`, `WO-IAR-023`, `WO-IAR-024`, `WO-IAR-025`, `WO-KIS-016`, `WO-PLG-026`, `WO-PLG-027`, `WO-PLG-028`, `WO-PLG-029`, `WO-RLO-010`, `WO-RLO-011`, `WO-RLS-026` from candidate commit `7253d13b212ad6f7df670021290fea32e81d66de`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-031"
type = "release_record"
title = "Release candidate 0.21.0"
status = "ready"
owners = ["Codex"]
created = "2026-10-02"
updated = "2026-10-02"
version = "0.21.0"
commit = "4031f0fa4b5c4a95651bd928a110d8b2d94f9775"
git_object_format = "sha1"
prepared_at = "2026-10-02T04:43:14Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-21-0/evidence/RLS-SEH-031-evaluator.json"
evaluator_evidence_sha256 = "e5148d268c5741a14613a371672929daa845983733cf8ee1439f3f3b60b4bb8b"
tag = "v0.21.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1790915026
wheel = "se_harness-0.21.0-py3-none-any.whl"
wheel_sha256 = "13d401f5a0c94444dc3cf31c6f2863d23b77beb4b2c33756734b493606ad6789"
sdist = "se_harness-0.21.0.tar.gz"
sdist_sha256 = "f1db9d80acf8ee86ea53b53c64c0f4d25db6fd99c58f903dd841d13f95cca98b"
checksums = "SHA256SUMS"
checksums_sha256 = "5a19fbe2b516631a15cd0eb5d6258e95c68478fa800e2cc5b6e9ed05c3d76b3a"
source_manifest_sha256 = "326a77de837da64bf2a06948169787c86823c010ddcbeedbcb520fb23c8fec1b"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-033"]
includes_verification = ["VREC-SEH-031"]
releases_work = ["WO-IAR-028", "WO-IAR-029", "WO-IAR-030", "WO-IAR-031", "WO-IAR-033", "WO-IAR-034", "WO-IAR-035", "WO-IAR-036", "WO-IAR-037", "WO-IAR-039", "WO-IAR-040", "WO-IAR-041", "WO-RLS-031"]
+++

# Release Record Candidate

This ready record proposes release `0.21.0` for `WO-IAR-028`, `WO-IAR-029`, `WO-IAR-030`, `WO-IAR-031`, `WO-IAR-033`, `WO-IAR-034`, `WO-IAR-035`, `WO-IAR-036`, `WO-IAR-037`, `WO-IAR-039`, `WO-IAR-040`, `WO-IAR-041`, `WO-RLS-031` from candidate commit `4031f0fa4b5c4a95651bd928a110d8b2d94f9775`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

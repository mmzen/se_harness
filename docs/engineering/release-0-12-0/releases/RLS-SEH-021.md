+++
id = "RLS-SEH-021"
type = "release_record"
title = "Release candidate 0.12.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-31"
updated = "2026-08-31"
version = "0.12.0"
commit = "3dcde4bbab4f3969fdc59ccdeee9ef68dfb90d26"
git_object_format = "sha1"
prepared_at = "2026-08-31T11:54:46Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-12-0/evidence/RLS-SEH-021-evaluator.json"
evaluator_evidence_sha256 = "52678c799ac17cfa9a568da240a9ba2596ca17a124cf73bdcd8a67059474f211"
tag = "v0.12.0"

released_at = "2026-08-31T12:10:41Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788177069
wheel = "se_harness-0.12.0-py3-none-any.whl"
wheel_sha256 = "639edbeed4bdca7c9e21a5eb2afc3b9fc993ddb3f66177eec962f1646a545811"
sdist = "se_harness-0.12.0.tar.gz"
sdist_sha256 = "3f7b22ff484dce8d95728a6ab632b86f0046713b2166498af36d526dab8ce3f2"
checksums = "SHA256SUMS"
checksums_sha256 = "8530b5faa3c453009455f7057c22cc84664e48d700944b167d8e764bed5d6135"
source_manifest_sha256 = "5a9b65580d0197332dbdaf5fbc82a330f214029364cd4c0eeeffe1b016a0687e"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-023"]
includes_verification = ["VREC-SEH-021"]
releases_work = ["WO-AUT-004", "WO-DST-022", "WO-ECP-018", "WO-ECP-019", "WO-ECP-020", "WO-ECP-021", "WO-ECP-022", "WO-ECP-023", "WO-HUP-011", "WO-HUP-012", "WO-LRE-002", "WO-REB-031", "WO-RLS-018", "WO-TCM-003"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-08-31T12:10:41Z"
decided_by = "release-owner"
reason = "Released by the accountable release owner on 2026-08-31 by selecting the presented option 'I release RLS-SEH-021'. Re-measured immediately before this transition: the record binds candidate 3dcde4b with the schema-2 distribution table carrying wheel 639edbee and sdist 3f7b22ff from two byte-identical pinned-producer runs re-verified at the bound candidate; REL-SEH-023 is approved with its fourteen gates; VREC-SEH-021 is verified over the whole unit; the hosted release-candidate replay on this branch completed success, reproducing the recorded digests with read-only repository permission; every lane of pull request #304 passes. This releases se-harness 0.12.0 as a record; the tag, the GitHub Release, PyPI, Pages, the maintenance line and the latest markers follow the promotion policy as separate acts, and the pypi environment remains a separate human decision."
+++

# Release Record Candidate

This ready record proposes release `0.12.0` for `WO-AUT-004`, `WO-DST-022`, `WO-ECP-018`, `WO-ECP-019`, `WO-ECP-020`, `WO-ECP-021`, `WO-ECP-022`, `WO-ECP-023`, `WO-HUP-011`, `WO-HUP-012`, `WO-LRE-002`, `WO-REB-031`, `WO-RLS-018`, `WO-TCM-003` from candidate commit `3dcde4bbab4f3969fdc59ccdeee9ef68dfb90d26`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

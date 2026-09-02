+++
id = "RLS-SEH-022"
type = "release_record"
title = "Release candidate 0.13.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-02"
updated = "2026-09-02"
version = "0.13.0"
commit = "79d6f6f0e56a5c9b1b2a888d57ae9bc65539147f"
git_object_format = "sha1"
prepared_at = "2026-09-02T07:28:37Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-13-0/evidence/RLS-SEH-022-evaluator.json"
evaluator_evidence_sha256 = "c5baebb5b7d3c7cc04940aef92872da30321a6bd15d0478309f49ba224a49e0f"
tag = "v0.13.0"

released_at = "2026-09-02T07:36:31Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788333166
wheel = "se_harness-0.13.0-py3-none-any.whl"
wheel_sha256 = "1bbf3b747b7ebbb07fd3fd975e87e3c11049e7a6a8e1377e3d35099f4fe862ae"
sdist = "se_harness-0.13.0.tar.gz"
sdist_sha256 = "d1f6b60ae149be5aad5509b88b768f6cfe22d9af8460f1fdc9d04bcf6670bdd4"
checksums = "SHA256SUMS"
checksums_sha256 = "1bef289b58b841dd6066ed35f0f18cd5155b37cb8061503235ae5cd14b0bccc0"
source_manifest_sha256 = "66d329f74e732b7768e8ff1eae834eb7c0864001af3abf7a92968d162cec53d2"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-024"]
includes_verification = ["VREC-SEH-022"]
releases_work = ["WO-DST-023", "WO-ECP-024", "WO-HUP-013", "WO-RLS-019"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-02T07:36:31Z"
decided_by = "release-owner"
reason = "Released by the accountable release owner on 2026-09-02 by selecting the presented option 'Release RLS-SEH-022, merge #313, dispatch publish-pypi'. Re-measured immediately before this transition: the record binds candidate 79d6f6f with the schema-2 distribution table carrying wheel 1bbf3b74 and sdist d1f6b60a from two byte-identical pinned-producer runs dispatched on the branch at the bound candidate; REL-SEH-024 is approved with its four gates; VREC-SEH-022 is verified over the whole unit; the hosted release-candidate replay on this branch (run 33603839879) completed success, reproducing the recorded digests from the bound record with read-only repository permission; every lane of pull request #313 at 6f43c21 passes except the release-record rehearsal, which reads the record from the head of main where it cannot exist before the merge, as REL-SEH-023's release recorded. This releases se-harness 0.13.0 as a record; the merge, the tag, the GitHub Release, PyPI, Pages, the maintenance line and the latest markers follow the promotion policy as separate acts, and the pypi environment remains a separate human decision."
+++

# Release Record Candidate

This ready record proposes release `0.13.0` for `WO-DST-023`, `WO-ECP-024`, `WO-HUP-013`, `WO-RLS-019` from candidate commit `79d6f6f0e56a5c9b1b2a888d57ae9bc65539147f`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

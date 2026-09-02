+++
id = "RLS-SEH-023"
type = "release_record"
title = "Release candidate 0.14.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-02"
updated = "2026-09-02"
version = "0.14.0"
commit = "09625e41e6b8dc10ea07a601e5ce4ea21e0d5d14"
git_object_format = "sha1"
prepared_at = "2026-09-02T09:50:27Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-14-0/evidence/RLS-SEH-023-evaluator.json"
evaluator_evidence_sha256 = "21ded06932d284d3ab2145b5ba7b9d5d3fc40997da8b047f7fb6f9f164910044"
tag = "v0.14.0"

released_at = "2026-09-02T10:01:52Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1788341712
wheel = "se_harness-0.14.0-py3-none-any.whl"
wheel_sha256 = "70d438b501d374fec06f41e25571f674b3cd1f43178389e6e06b0269c92f4856"
sdist = "se_harness-0.14.0.tar.gz"
sdist_sha256 = "dcb3523a0ba7118a6f04f2a041be0652e2b30eea535c2a26a89729c30f96df8f"
checksums = "SHA256SUMS"
checksums_sha256 = "fe261ef9df03b1abb28cad37a8a8c56fdb39cab152d2e5547263e21c86191e9b"
source_manifest_sha256 = "0af09311f2c3708237fd3856f78ce2634db1e6ac4677c9d40ac0f5e3ec279198"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-025"]
includes_verification = ["VREC-SEH-023"]
releases_work = ["WO-HUP-014", "WO-RLS-020"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-02T10:01:52Z"
decided_by = "release-owner"
reason = "Released by the accountable release owner on 2026-09-02 by selecting the presented option 'Release RLS-SEH-023; I will merge #315 and you dispatch publish-pypi'. Re-measured immediately before this transition: the record binds candidate 09625e4 with the schema-2 distribution table carrying wheel 70d438b5 and sdist dcb3523a from two byte-identical pinned-producer runs dispatched on the branch at the bound candidate; REL-SEH-025 is approved with its two gates; VREC-SEH-023 is verified over the whole unit; the hosted release-candidate replay on this branch (run 33616347600) completed success, reproducing the recorded digests from the bound record with read-only repository permission; every lane of pull request #315 at 673ffe8 passes except the release-record rehearsal, which reads the record from the head of main where it cannot exist before the merge, as the 0.13.0 and 0.12.0 releases recorded. This releases se-harness 0.14.0 as a record, a package that changes only by version so that its integration commit carries the 0.13.0 root and the release-bound public demonstration renders the designed Explorer; the merge, the tag, the GitHub Release, PyPI, Pages, the maintenance line and the latest markers follow the promotion policy as separate acts, and the pypi environment remains a separate human decision."
+++

# Release Record Candidate

This ready record proposes release `0.14.0` for `WO-HUP-014`, `WO-RLS-020` from candidate commit `09625e41e6b8dc10ea07a601e5ce4ea21e0d5d14`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-030"
type = "release_record"
title = "Release candidate 0.20.1"
status = "released"
owners = ["release-owner"]
created = "2026-09-30"
updated = "2026-10-01"
version = "0.20.1"
commit = "b9af631b850c495eace9807361ed3ec3e36a10b2"
git_object_format = "sha1"
prepared_at = "2026-09-30T20:52:14Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-20-1/evidence/RLS-SEH-030-evaluator.json"
evaluator_evidence_sha256 = "3d06ef9adf5b4bcb9bd9d9d93ae6ea13f35ec4f0ca9ab8338586e48254d39713"

released_at = "2026-10-01T06:01:59Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1790799840
wheel = "se_harness-0.20.1-py3-none-any.whl"
wheel_sha256 = "300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764"
sdist = "se_harness-0.20.1.tar.gz"
sdist_sha256 = "a4c38a50e3614cfe8b478f7903af3b829e9d605b864d0ba3caca3816f4f2464a"
checksums = "SHA256SUMS"
checksums_sha256 = "8ef1f3b9ce5a465f963e34e711deed624b9645d2f25824f23624bee089a8f0ac"
source_manifest_sha256 = "890eb07d32540fb81beba94f6db409c7cafe2abcd6b1889e1aa0ac1fd9baa846"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-032"]
includes_verification = ["VREC-SEH-030"]
releases_work = ["WO-RLS-027"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-10-01T06:01:59Z"
decided_by = "release-owner"
reason = "Human mmzen: I authorize release record RLS-SEH-030. Authorizes SE Harness 0.20.1 at verified candidate b9af631b850c495eace9807361ed3ec3e36a10b2 with unchanged reviewed release inputs, verified VREC-SEH-030 and passing bound-record two-build replay. Codex applies the human decision using the approved maintenance 0.19.0 role-label encoding; mmzen is the accountable release owner. Merge, publication, moving markers and adoption remain separate. Corrected only the unaccepted ready record owners from preparation actor Codex to release-owner for this actual human decision; prepared_by remains Codex. Reviewed SHA256 51abaf44dd6843a03a1bf60a44ce351f97e384fb28c775bfaf11aed06cb0655f; corrected input SHA256 fab6c7a239963144857b7f7cac1d13903ae30eae3b83b4b08ca2e4b9c31efde9."
+++

# Release Record Candidate

This ready record proposes release `0.20.1` for `WO-RLS-027` from candidate commit `b9af631b850c495eace9807361ed3ec3e36a10b2`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-017"
type = "release_record"
title = "Release candidate 0.8.0"
status = "ready"
owners = ["release-owner"]
created = "2026-08-28"
updated = "2026-08-28"
version = "0.8.0"
commit = "884b769efdc9eda2959f2c774e6af10748beb88a"
git_object_format = "sha1"
prepared_at = "2026-08-28T16:15:24Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-8-0/evidence/RLS-SEH-017-evaluator.json"
evaluator_evidence_sha256 = "0a090f68cad9465498f702505f3c3d35830328a0ebad928be066831252cfabdd"
tag = "v0.8.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787933408
wheel = "se_harness-0.8.0-py3-none-any.whl"
wheel_sha256 = "e08aab8a96c156f9e5edf99b9a28aad96c7cffe5b18c262a2598a6b6873fadeb"
sdist = "se_harness-0.8.0.tar.gz"
sdist_sha256 = "2d2c237e88b0a0b0fb0e06e70caed9e9610472c289eccf849f9b675f33d59624"
checksums = "SHA256SUMS"
checksums_sha256 = "2b96f9da268c0c16fe83f4ac3a64ce0a830e6eedfef1effb7ab1095e444e0725"
source_manifest_sha256 = "2aa041c65dbbb9514960000d44804e65e917842e36298615a57387eb147b971d"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-019"]
includes_verification = ["VREC-SEH-017"]
releases_work = ["WO-AUT-003", "WO-ECP-005", "WO-ECP-009", "WO-ECP-010", "WO-HBI-005", "WO-HUP-007", "WO-REB-028", "WO-REB-029", "WO-RLO-008", "WO-RLS-014"]
+++

# Release Record Candidate

This ready record proposes release `0.8.0` for `WO-AUT-003`, `WO-ECP-005`, `WO-ECP-009`, `WO-ECP-010`, `WO-HBI-005`, `WO-HUP-007`, `WO-REB-028`, `WO-REB-029`, `WO-RLO-008`, `WO-RLS-014` from candidate commit `884b769efdc9eda2959f2c774e6af10748beb88a`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

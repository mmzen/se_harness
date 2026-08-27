+++
id = "RLS-SEH-015"
type = "release_record"
title = "Release candidate 0.7.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-26"
updated = "2026-08-26"
version = "0.7.0"
commit = "374554d01f9a2e4601dc5b58279a01de2c7b6523"
git_object_format = "sha1"
prepared_at = "2026-08-26T21:42:08Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-7-0/evidence/RLS-SEH-015-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"
tag = "v0.7.0"

released_at = "2026-08-26T22:15:06Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787779226
wheel = "se_harness-0.7.0-py3-none-any.whl"
wheel_sha256 = "e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3"
sdist = "se_harness-0.7.0.tar.gz"
sdist_sha256 = "7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617"
checksums = "SHA256SUMS"
checksums_sha256 = "3021ee7660a7065210e38b629333ca3f438d9afba0236f85c785cf7bf5efbf00"
source_manifest_sha256 = "1c0b1dcf49492e9d55570d99bc6fd7a63ca32a2512ab65880869dc6a16e1d075"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-017"]
includes_verification = ["VREC-SEH-014"]
releases_work = ["WO-ADS-001", "WO-ADS-002", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-AEX-006", "WO-AEX-007", "WO-AEX-008", "WO-AUT-001", "WO-AUT-002", "WO-CIP-001", "WO-CIP-002", "WO-CIP-003", "WO-CIP-004", "WO-CIP-005", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-HUP-004", "WO-IPK-001", "WO-LRE-001", "WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-REB-023", "WO-RLO-004", "WO-RLO-005", "WO-RLO-006", "WO-RLO-007", "WO-RLS-011", "WO-RLS-012", "WO-TCM-001", "WO-TCM-002", "WO-TST-001", "WO-TST-002", "WO-TST-003", "WO-VSP-007", "WO-WEX-003"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-08-26T22:15:06Z"
decided_by = "release-owner"
reason = "Released by the accountable release owner on 2026-08-27, 'I release RLS-SEH-015 as release owner', on main at 76100cf75c4349fefe310c25e379a59f17e9cffe, the true merge of pull request #183. The record satisfies REL-SEH-017, includes verified VREC-SEH-014 and releases the fifty-three work orders the contract names, all reading implemented with the bound candidate 374554d01f9a2e4601dc5b58279a01de2c7b6523 and every member's bound verification commit reachable from main. Its schema-2 distribution table binds the Linux recipe-bound build of that candidate: wheel e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3, sdist 7bebfc0ac51162fda9f6ca69d7f893d0ba4c2ae928bc5a699c48189e62abf617, reproduced twice by the read-only hosted replay (run 33016585047, PASS) and accepted ten of ten by the released 0.6.0 verifier. The pull request's lanes were green except the release-record rehearsal, which resolves only against main and runs on this push. Four limitations are carried as disclosed residual risk: VER-TCM-001's reviewer judgments, VER-ADS-001's Scenario 8, VREC-IPK-001's merge-preview bound commit, and VREC-SEH-014's superseded workstation digests in prose. This decision authorizes the last mile as a separate dispatch of publish-pypi from main; the protected pypi environment remains a separate human approval; the root evaluator does not change."
+++

# Release Record Candidate

This ready record proposes release `0.7.0` for `WO-ADS-001`, `WO-ADS-002`, `WO-AEX-001`, `WO-AEX-002`, `WO-AEX-003`, `WO-AEX-004`, `WO-AEX-005`, `WO-AEX-006`, `WO-AEX-007`, `WO-AEX-008`, `WO-AUT-001`, `WO-AUT-002`, `WO-CIP-001`, `WO-CIP-002`, `WO-CIP-003`, `WO-CIP-004`, `WO-CIP-005`, `WO-HBI-001`, `WO-HBI-002`, `WO-HBI-003`, `WO-HBI-004`, `WO-HUP-004`, `WO-IPK-001`, `WO-LRE-001`, `WO-REB-008`, `WO-REB-009`, `WO-REB-010`, `WO-REB-011`, `WO-REB-012`, `WO-REB-013`, `WO-REB-014`, `WO-REB-015`, `WO-REB-016`, `WO-REB-017`, `WO-REB-018`, `WO-REB-019`, `WO-REB-020`, `WO-REB-021`, `WO-REB-022`, `WO-REB-023`, `WO-RLO-004`, `WO-RLO-005`, `WO-RLO-006`, `WO-RLO-007`, `WO-RLS-011`, `WO-RLS-012`, `WO-TCM-001`, `WO-TCM-002`, `WO-TST-001`, `WO-TST-002`, `WO-TST-003`, `WO-VSP-007`, `WO-WEX-003` from candidate commit `374554d01f9a2e4601dc5b58279a01de2c7b6523`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

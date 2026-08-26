+++
id = "RLS-SEH-014"
type = "release_record"
title = "Release candidate 0.7.0"
status = "ready"
owners = ["release-owner"]
created = "2026-08-26"
updated = "2026-08-26"
version = "0.7.0"
commit = "374554d01f9a2e4601dc5b58279a01de2c7b6523"
git_object_format = "sha1"
prepared_at = "2026-08-26T21:27:50Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-7-0/evidence/RLS-SEH-014-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"
tag = "v0.7.0"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1787779226
wheel = "se_harness-0.7.0-py3-none-any.whl"
wheel_sha256 = "622d008908dad043b78aa10dbeae459e4ee4203255453832fe71a85481c32389"
sdist = "se_harness-0.7.0.tar.gz"
sdist_sha256 = "304cce5f89fa867300c68dff7d2469cb9dcbc7abc86d68c966c561a707072f38"
checksums = "SHA256SUMS"
checksums_sha256 = "eb0be0f491d70e0ba92ebb84b34b79742e07ea5c72e247313b926e20be283244"
source_manifest_sha256 = "1c0b1dcf49492e9d55570d99bc6fd7a63ca32a2512ab65880869dc6a16e1d075"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-017"]
includes_verification = ["VREC-SEH-014"]
releases_work = ["WO-ADS-001", "WO-ADS-002", "WO-AEX-001", "WO-AEX-002", "WO-AEX-003", "WO-AEX-004", "WO-AEX-005", "WO-AEX-006", "WO-AEX-007", "WO-AEX-008", "WO-AUT-001", "WO-AUT-002", "WO-CIP-001", "WO-CIP-002", "WO-CIP-003", "WO-CIP-004", "WO-CIP-005", "WO-HBI-001", "WO-HBI-002", "WO-HBI-003", "WO-HBI-004", "WO-HUP-004", "WO-IPK-001", "WO-LRE-001", "WO-REB-008", "WO-REB-009", "WO-REB-010", "WO-REB-011", "WO-REB-012", "WO-REB-013", "WO-REB-014", "WO-REB-015", "WO-REB-016", "WO-REB-017", "WO-REB-018", "WO-REB-019", "WO-REB-020", "WO-REB-021", "WO-REB-022", "WO-REB-023", "WO-RLO-004", "WO-RLO-005", "WO-RLO-006", "WO-RLO-007", "WO-RLS-011", "WO-RLS-012", "WO-TCM-001", "WO-TCM-002", "WO-TST-001", "WO-TST-002", "WO-TST-003", "WO-VSP-007", "WO-WEX-003"]
+++

# Release Record Candidate

This ready record proposes release `0.7.0` for `WO-ADS-001`, `WO-ADS-002`, `WO-AEX-001`, `WO-AEX-002`, `WO-AEX-003`, `WO-AEX-004`, `WO-AEX-005`, `WO-AEX-006`, `WO-AEX-007`, `WO-AEX-008`, `WO-AUT-001`, `WO-AUT-002`, `WO-CIP-001`, `WO-CIP-002`, `WO-CIP-003`, `WO-CIP-004`, `WO-CIP-005`, `WO-HBI-001`, `WO-HBI-002`, `WO-HBI-003`, `WO-HBI-004`, `WO-HUP-004`, `WO-IPK-001`, `WO-LRE-001`, `WO-REB-008`, `WO-REB-009`, `WO-REB-010`, `WO-REB-011`, `WO-REB-012`, `WO-REB-013`, `WO-REB-014`, `WO-REB-015`, `WO-REB-016`, `WO-REB-017`, `WO-REB-018`, `WO-REB-019`, `WO-REB-020`, `WO-REB-021`, `WO-REB-022`, `WO-REB-023`, `WO-RLO-004`, `WO-RLO-005`, `WO-RLO-006`, `WO-RLO-007`, `WO-RLS-011`, `WO-RLS-012`, `WO-TCM-001`, `WO-TCM-002`, `WO-TST-001`, `WO-TST-002`, `WO-TST-003`, `WO-VSP-007`, `WO-WEX-003` from candidate commit `374554d01f9a2e4601dc5b58279a01de2c7b6523`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-027"
type = "release_record"
title = "Release candidate 0.18.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-15"
updated = "2026-09-15"
version = "0.18.0"
commit = "353da23881fdf045a52322a313c1e67341f7a9b1"
git_object_format = "sha1"
prepared_at = "2026-09-15T06:56:23Z"
prepared_by = "release-owner"
evaluator_evidence_path = "docs/engineering/release-0-18-0/evidence/RLS-SEH-027-evaluator.json"
evaluator_evidence_sha256 = "44d4b74d9febe03a0828dfeee8cd8322fd02db74ff866d7191440e17164e7abb"
tag = "v0.18.0"

released_at = "2026-09-15T07:20:40Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1789453817
wheel = "se_harness-0.18.0-py3-none-any.whl"
wheel_sha256 = "a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54"
sdist = "se_harness-0.18.0.tar.gz"
sdist_sha256 = "757c63cd5ef6caf536fb8f07e5144706aafe373e8ac490c74f239a4acb9c6cbd"
checksums = "SHA256SUMS"
checksums_sha256 = "1a47a92996fdff8f9ff21ae4dd8d8b60e17f127bcd3be523390f039cb43b852a"
source_manifest_sha256 = "361338d17ad448aa5b6b6a8e51d5071261e54dab6ec61afb6f08f7a0f6c98029"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-029"]
includes_verification = ["VREC-SEH-027"]
releases_work = ["WO-AUT-006", "WO-CIP-008", "WO-CIP-009", "WO-CIP-010", "WO-DST-027", "WO-ECP-037", "WO-ECP-038", "WO-HUP-018", "WO-KIS-001", "WO-KIS-002", "WO-KIS-003", "WO-KIS-004", "WO-KIS-005", "WO-KIS-006", "WO-KIS-007", "WO-KIS-008", "WO-KIS-009", "WO-PLG-001", "WO-PLG-002", "WO-PLG-003", "WO-PLG-004", "WO-PLG-005", "WO-PLG-006", "WO-PLG-007", "WO-PLG-008", "WO-PLG-009", "WO-PLG-010", "WO-PLG-011", "WO-PLG-012", "WO-PLG-016", "WO-PLG-017", "WO-PLG-018", "WO-PLG-019", "WO-PLG-020", "WO-PLG-021", "WO-PLG-022", "WO-RLO-009", "WO-RLS-024", "WO-TCM-011"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-15T07:20:40Z"
decided_by = "release-owner"
reason = "The owner replied \"i authorize\" to the explicit next decision \"I authorize release record RLS-SEH-027.\" Record that release-owner authorization of checker 0.18.0 at verified candidate 353da23881fdf045a52322a313c1e67341f7a9b1. The ready-record replay, independent review and release-decision gate passed, and all PR checks passed or were intentionally skipped before this decision. This transition records release authorization; merging and external publication remain subsequent actions."
+++

# Release Record Candidate

This ready record proposes release `0.18.0` for `WO-AUT-006`, `WO-CIP-008`, `WO-CIP-009`, `WO-CIP-010`, `WO-DST-027`, `WO-ECP-037`, `WO-ECP-038`, `WO-HUP-018`, `WO-KIS-001`, `WO-KIS-002`, `WO-KIS-003`, `WO-KIS-004`, `WO-KIS-005`, `WO-KIS-006`, `WO-KIS-007`, `WO-KIS-008`, `WO-KIS-009`, `WO-PLG-001`, `WO-PLG-002`, `WO-PLG-003`, `WO-PLG-004`, `WO-PLG-005`, `WO-PLG-006`, `WO-PLG-007`, `WO-PLG-008`, `WO-PLG-009`, `WO-PLG-010`, `WO-PLG-011`, `WO-PLG-012`, `WO-PLG-016`, `WO-PLG-017`, `WO-PLG-018`, `WO-PLG-019`, `WO-PLG-020`, `WO-PLG-021`, `WO-PLG-022`, `WO-RLO-009`, `WO-RLS-024`, `WO-TCM-011` from candidate commit `353da23881fdf045a52322a313c1e67341f7a9b1`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

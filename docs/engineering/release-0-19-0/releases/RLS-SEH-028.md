+++
id = "RLS-SEH-028"
type = "release_record"
title = "Release candidate 0.19.0"
status = "released"
owners = ["release-owner"]
created = "2026-09-27"
updated = "2026-09-27"
version = "0.19.0"
commit = "30d4dba2a088c4f83756c1241b76cdab40f796bd"
git_object_format = "sha1"
prepared_at = "2026-09-27T18:28:32Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-19-0/evidence/RLS-SEH-028-evaluator.json"
evaluator_evidence_sha256 = "81eef664cc9b26a839508163c924fc82fe531a4a9eaa8c8cc35ff3488f858c85"
tag = "v0.19.0"

released_at = "2026-09-27T18:44:21Z"
authorized_by = "release-owner"
[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1790532014
wheel = "se_harness-0.19.0-py3-none-any.whl"
wheel_sha256 = "43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8"
sdist = "se_harness-0.19.0.tar.gz"
sdist_sha256 = "e8aae38d4f6896078739902491a9268cf3ebdfc199af05a7ae6d74cda7daaffe"
checksums = "SHA256SUMS"
checksums_sha256 = "90c870a856bb1bb07c8186585ce8045618f4589abbd71f20acc27cd7c02771d3"
source_manifest_sha256 = "b9c8ba4e42f9387722d8512f2454500ba06de50c1c33006dfca48dacf6a6a0ee"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-030"]
includes_verification = ["VREC-SEH-028"]
releases_work = ["WO-DOC-016", "WO-ECP-039", "WO-HUP-019", "WO-HUP-020", "WO-IAR-013", "WO-IAR-014", "WO-IAR-015", "WO-IAR-016", "WO-IAR-017", "WO-IAR-018", "WO-IAR-019", "WO-PLG-023", "WO-PLG-025", "WO-RLS-025"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-09-27T18:44:21Z"
decided_by = "release-owner"
reason = "Human release-owner decision in this task: I authorize the release record. Codex applies this supplied human decision for 0.19.0 at candidate 30d4dba2a088c4f83756c1241b76cdab40f796bd. Corrected the ready record owner from the preparation actor Codex to the accountable release-owner; prepared_by remains Codex. Every other reviewed record byte and all verification and replay evidence are unchanged. Only this RLS changes state. Merge, publication, latest promotion and root adoption remain separate actions."
+++

# Release Record Candidate

This ready record proposes release `0.19.0` for `WO-DOC-016`, `WO-ECP-039`, `WO-HUP-019`, `WO-HUP-020`, `WO-IAR-013`, `WO-IAR-014`, `WO-IAR-015`, `WO-IAR-016`, `WO-IAR-017`, `WO-IAR-018`, `WO-IAR-019`, `WO-PLG-023`, `WO-PLG-025`, `WO-RLS-025` from candidate commit `30d4dba2a088c4f83756c1241b76cdab40f796bd`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

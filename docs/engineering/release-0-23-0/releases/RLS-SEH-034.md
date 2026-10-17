+++
id = "RLS-SEH-034"
type = "release_record"
title = "Release candidate 0.23.0"
status = "released"
owners = ["mmzen"]
created = "2026-10-17"
updated = "2026-10-17"
version = "0.23.0"
commit = "48e851bbc94d7fb0c06e9b80666c3860cb5f8c15"
git_object_format = "sha1"
prepared_at = "2026-10-17T05:45:39Z"
prepared_by = "Codex"
evaluator_evidence_path = "docs/engineering/release-0-23-0/evidence/RLS-SEH-034-evaluator.json"
evaluator_evidence_sha256 = "950c3c1fe2ecd3ad530ac454b185dfffebe4440d7617e6d512db815bfa257fdb"
tag = "v0.23.0"

released_at = "2026-10-17T06:34:11Z"
authorized_by = "mmzen"
[delivery]
plan = "docs/engineering/release-0-23-0/evidence/WO-RLS-045/complete-release-plan.json"
sha256 = "420b4b82891b2fe77244cc3c4a995ddab8153a11f649324f01b1f37e83e51b34"
decided_by = "mmzen"
decision_reference = "Codex session 01a0bd7b-24c7-7503-8955-4a24231fb2a4, 2026-10-17: mmzen replied \"Approve the complete release\" to the exact RLS-SEH-034 evaluator/client 0.23.0 and plugin 0.2.7 review in PR #545 at d463e42d6c5e4386fc07b0b6173b1c43f8908237. mmzen then replied \"Approve the owner correction and continue.\" to the exact one-line owner/base amendment reviewed at bfc2e24606c883f34e9920ef61112745d3f9fa03. The explicitly approved corrected pre-decision base is 8430edb957ceae79e144ce13e56bea1fb5019ec2"
review_commit = "8430edb957ceae79e144ce13e56bea1fb5019ec2"

[distribution]
schema = 2
kind = "python-wheel-sdist"
source_date_epoch = 1792154885
wheel = "se_harness-0.23.0-py3-none-any.whl"
wheel_sha256 = "ffa486d386383992349e75e2890b36ded105c797acaa483783d1380cfd520d5c"
sdist = "se_harness-0.23.0.tar.gz"
sdist_sha256 = "777c9c1f518f6db1d3beb013f9bbb908544c482598ee399767fd789414f2ccfa"
checksums = "SHA256SUMS"
checksums_sha256 = "5e1275bac408a5f7b57a9f203efe6540abf26f0727454ad2ea755c0d29af8097"
source_manifest_sha256 = "207dce0fcae712ebef2d26cea41e5b725af1caa3c171068479c38e26e79c65c5"
build_recipe_schema = "se-harness-release-build-recipe/v1"
build_recipe = "release/build-recipe.json"
build_recipe_sha256 = "0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc"

[relations]
satisfies = ["REL-SEH-036"]
includes_verification = ["VREC-SEH-034"]
releases_work = ["WO-HAG-001", "WO-HAG-005", "WO-HAG-006", "WO-HAG-007", "WO-HAG-008", "WO-HAG-009", "WO-HAG-010", "WO-HAG-011", "WO-HUP-030", "WO-IPK-002", "WO-RLS-045", "WO-RLS-046", "WO-RLS-048", "WO-RLS-049", "WO-RLS-050", "WO-RLS-051", "WO-RLS-052", "WO-RLS-053", "WO-RLS-054", "WO-RLS-055"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-10-17T06:34:11Z"
decided_by = "mmzen"
reason = "Codex session 01a0bd7b-24c7-7503-8955-4a24231fb2a4, 2026-10-17: mmzen replied \"Approve the complete release\" to the exact RLS-SEH-034 evaluator/client 0.23.0 and plugin 0.2.7 review in PR #545 at d463e42d6c5e4386fc07b0b6173b1c43f8908237. mmzen then replied \"Approve the owner correction and continue.\" to the exact one-line owner/base amendment reviewed at bfc2e24606c883f34e9920ef61112745d3f9fa03. The explicitly approved corrected pre-decision base is 8430edb957ceae79e144ce13e56bea1fb5019ec2. Frozen plan docs/engineering/release-0-23-0/evidence/WO-RLS-045/complete-release-plan.json SHA-256 420b4b82891b2fe77244cc3c4a995ddab8153a11f649324f01b1f37e83e51b34. One complete-release grant covers all listed actions, protected release/receipt integrations and recovery. Accepted DEC-RLS-010/011 and RISK-RLS-008/009 limitations remain. No adoption, user-host update, provider-setting change, production service or changed input is authorized."
+++

# Release Record Candidate

This ready record proposes release `0.23.0` for `WO-HAG-001`, `WO-HAG-005`, `WO-HAG-006`, `WO-HAG-007`, `WO-HAG-008`, `WO-HAG-009`, `WO-HAG-010`, `WO-HAG-011`, `WO-HUP-030`, `WO-IPK-002`, `WO-RLS-045`, `WO-RLS-046`, `WO-RLS-048`, `WO-RLS-049`, `WO-RLS-050`, `WO-RLS-051`, `WO-RLS-052`, `WO-RLS-053`, `WO-RLS-054`, `WO-RLS-055` from candidate commit `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

+++
id = "RLS-SEH-012"
type = "release_record"
title = "Release candidate 0.6.0"
status = "released"
owners = ["release-owner"]
created = "2026-08-22"
updated = "2026-08-22"
version = "0.6.0"
commit = "3b339e9fc70cc634e6dc6bda07ea6a9b1a465798"
git_object_format = "sha1"
released_at = "2026-08-22T16:49:37Z"
authorized_by = "release-owner"
tag = "v0.6.0"

preparation_view_evidence_path = "docs/engineering/release-0-6-0/evidence/RLS-SEH-012-preparation-view.json"
preparation_view_evidence_sha256 = "77474d1e22422371d48f3d1a281810a6c7f9bf55982a17e565f602978bbab4d7"

preparation_schema = "se-harness-predecessor-bootstrap-v1"
evaluator_evidence_path = "docs/engineering/release-0-6-0/evidence/RLS-SEH-012-evaluator.json"
evaluator_evidence_sha256 = "11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404"

[distribution]
schema = 1
kind = "python-wheel-sdist"
source_date_epoch = 1787392506
wheel = "se_harness-0.6.0-py3-none-any.whl"
wheel_sha256 = "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"
sdist = "se_harness-0.6.0.tar.gz"
sdist_sha256 = "9493aa40ffbaf021edd205d6c302d67d11975bc057f73ba09b91043a9a51bbe4"
checksums = "SHA256SUMS"
checksums_sha256 = "d4bbb194e6e51e6353645c2c3174b960db985af0f9b3d24e4031ab6b93d108a6"
source_manifest_sha256 = "ac587fabec3dbcc695e391d0243bda30f19a3ff0935f63c8c942dda7819f87da"

[relations]
satisfies = ["REL-SEH-011"]
includes_verification = ["VREC-SEH-012"]
releases_work = ["WO-DST-019", "WO-DST-020", "WO-DST-021", "WO-IAR-012", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-REB-004", "WO-REB-005", "WO-REB-006", "WO-REB-007", "WO-RLS-008", "WO-WEX-001", "WO-WEX-002"]

[[lifecycle_events]]
from = "ready"
to = "released"
decided_at = "2026-08-22T17:09:49Z"
decided_by = "release-owner"
+++

# Release Record Candidate

This ready record proposes release `0.6.0` for `WO-DST-019`, `WO-DST-020`, `WO-DST-021`, `WO-IAR-012`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, `WO-REB-004`, `WO-REB-005`, `WO-REB-006`, `WO-REB-007`, `WO-RLS-008`, `WO-WEX-001`, `WO-WEX-002` from candidate commit `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.

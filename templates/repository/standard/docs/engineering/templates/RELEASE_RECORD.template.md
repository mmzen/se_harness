+++
id = "RLS-000"
type = "release_record"
title = "Release candidate VERSION"
status = "ready"
owners = ["release-owner"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"
version = "VERSION"
commit = "0000000000000000000000000000000000000000"
git_object_format = "sha1"
released_at = "YYYY-MM-DDTHH:MM:SSZ"
authorized_by = "release-owner"
tag = "vVERSION"

# Optional for historical records; required for SE Harness Python publication.
# Generate and bind this complete table with:
# harnessctl prepare-release --distribution-manifest PATH ...
# [distribution]
# schema = 1
# kind = "python-wheel-sdist"
# source_date_epoch = 0000000000
# wheel = "se_harness-VERSION-py3-none-any.whl"
# wheel_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
# sdist = "se_harness-VERSION.tar.gz"
# sdist_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
# checksums = "SHA256SUMS"
# checksums_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"
# source_manifest_sha256 = "0000000000000000000000000000000000000000000000000000000000000000"

[relations]
satisfies = ["REL-000"]
includes_verification = ["VREC-001"]
releases_work = ["WO-001", "WO-002"]
+++

# Release Record Candidate

Copy the one shared commit from the included verification records. The released-work set must equal their verification-coverage union, and every work order must be gated by the release contract. A single work order remains valid. Keep status `ready` until the accountable release owner authorizes the instance. Historical records may omit `[distribution]`; SE Harness Python publication requires the complete schema-1 table prepared from a deterministic bundle manifest. This document does not create a tag or publish a release.

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

[relations]
satisfies = ["REL-000"]
includes_verification = ["VREC-000"]
releases_work = ["WO-000"]
+++

# Release Record Candidate

Copy the commit from the included verified record. Keep status `ready` until the accountable release owner authorizes the instance. This document does not create a tag or publish a release.


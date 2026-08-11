+++
id = "REQ-DST-006"
type = "requirement"
title = "Distribute a versioned complete template"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the project is packaged or used from source, THE SYSTEM SHALL expose a versioned harnessctl entry point and include the complete standard template and CI integration."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement

Python 3.11 or later is the only runtime dependency. The installed target carries standard-library validation and dashboard generation scripts so its checks do not depend on a service.


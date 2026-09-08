+++
id = "REQ-PLG-004"
type = "requirement"
title = "Prepare the private evaluator environment offline"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN environment setup is authorized, THE SETUP ROUTINE SHALL install the packaged evaluator offline into an isolated private environment outside the target repository."
verification_method = ["test","inspection"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Prepare the private evaluator environment offline

## In plain words

Setup prepares the checking tool in its own directory. It uses the package already supplied with the plugin.

## Why

Repository code and unrelated installed packages must not become the checking tool. First setup should not depend on a package-index download.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Authorized environment setup | Create the private environment in persistent plugin data and install the supplied wheel without network access. | Keep an incomplete environment unavailable and preserve the target repository. |

## Examples

### Normal

**Given** supported Python and the selected supplied wheel.

**When** authorized setup completes with network access disabled.

**Then** the checking tool is available outside the repository.

### Failure

**Given** installation is interrupted.

**When** the agent requests governed work.

**Then** the incomplete environment is refused.

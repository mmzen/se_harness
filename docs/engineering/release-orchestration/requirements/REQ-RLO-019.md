+++
id = "REQ-RLO-019"
type = "requirement"
title = "Check delivery identity and public availability"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "Delivery closeout SHALL compare declared identities with retained package, documentation and public-route observations, and SHALL report missing or mismatched evidence as incomplete."
verification_method = ["test", "inspection"]
priority = "must"
source = "2026-09-28 marketplace audit and approved release-procedure correction plan"

[relations]
derives_from = ["CAP-RLO-004"]
+++

# Requirement: Check delivery identity and public availability

## In plain words

The report checks what users can obtain against what the release plan promises.
Two documents agreeing with each other do not prove that the package is current.

## Why

Local qualification and public installation are different observations.
A cached version label can also hide different package bytes.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A package is prepared | Compare selected source manifests, assembly inventories and bundled evaluator identity with the declared release inputs. | Report each missing or conflicting identity. |
| Current instructions are reviewed | Compare version, install/update route and support claims with the declared identities and observed behavior; check links in their source or assembled context. | Identify stale claims and broken routes before closeout. |
| Marketplace publication is observed | Require fresh installation and the declared update route for each claimed host from the actual public destination; compare installed content and retain the public revision. | Local assembly evidence, a version string alone or evidence from another source cannot satisfy public delivery. |
| An unchanged surface is claimed | Check its identity and retained compatibility assessment for this delivery. | Prior success for different inputs is insufficient. |

## Examples

### Normal

**Given** a qualified package and matching current documentation, **when** the
same package is installed and updated from the declared public ref on both
claimed hosts, **then** closeout may report that surface as satisfied.

### Failure

**Given** local plugin 0.2.0 qualification but public plugin 0.1.0,
**when** the plan calls for the newer package, **then** public delivery remains
incomplete even if the evaluator publication and unit tests passed.

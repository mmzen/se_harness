+++
id = "ADR-HAG-002"
type = "adr"
title = "Use one explicit owner binding per decision request"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
decides = ["ARCH-HAG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T16:52:37Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved WO-HAG-003 and required verification in response to the reviewed six-artifact correction package. This applies only to that package: local implementation, checks, commits and commit-bound verification preparation. Human verification acceptance, publication, release, adoption and the live DEC-HAG-001 disposition remain separate. Reviewed file hashes were compared before this transition; approval bindings are retained under docs/engineering/hosted-artifact-graph/evidence/WO-HAG-003/."
+++

# Use one explicit owner binding per decision request

## Proposed decision

Use one optional `--authority-owner` value on a disposition request. Keep
`--decision` as the actual decision-maker and preserve the existing holder
calculation. This proposal has no authority until approved.

## Alternatives

| Option | Consequence |
| --- | --- |
| Explicit per-request binding — proposed | Audits the person and accountability separately; checks existing holders; no registry or inferred permission. |
| Infer from earlier work approval or DEC owners | Shorter invocation, but can transfer a different right without an explicit mapping and fails for deviations or multiple accountabilities. |
| Rewrite WO-HAG-001 owners | Changes accepted ownership and needs a supported amendment; does not correct the command for other repositories. |
| Accept any non-empty actor | Records a name but removes the existing holder check. |
| Add an identity/role registry | Adds persistent policy and administration beyond this recording defect. |

## Consequences

The explicit binding is an assertion checked against declared accountability,
not authentication. An authorized human decision is still required. Existing
direct-owner requests and historical dispositions keep their meaning. The
extension must be released and adopted before it can resolve the live defect.

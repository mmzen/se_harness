# Integration Package definition-review decision packet

> Historical record from 2026-08-24, at `d0cb7e4`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 8/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

This packet is a human-readable review aid. It is not a formal engineering
artifact and grants no lifecycle, implementation, workflow, installation, Git,
publication or external-action authority.

## Decision requested

Approve the complete IPK definition and apply exactly ten `draft -> approved`
transitions. Keep implementation stopped until the engineering owner separately
starts `WO-IPK-001` after exact released-evaluator preflight.

## What the packet establishes

- An eligible `main` or pull-request commit receives a unique PEP 440 local
  version only inside disposable exact-commit exports.
- Independent builds must be byte-identical and bind their provenance in a
  canonical manifest and checksum file.
- Linux and Windows install the same staged wheel before a final expiring
  GitHub Actions artifact is retained.
- The package is explicitly non-promotable and creates no tag, GitHub Release,
  PyPI/TestPyPI upload, RLS, REL, VREC transition or governing-evaluator change.
- Operators explicitly download, verify and install the wheel into an isolated
  environment and test only a disposable repository.

## Accountable review checklist

- Product owner: confirm the need, desired capability and observable outcomes.
- Requirements steward: confirm unique identity, cross-platform exact-byte
  qualification, retention and release/evaluator separation are testable.
- Repository owner: confirm repository scope, exact execution paths and
  commit-bound assurance classification.
- Technical owner: confirm the identity overlay, safe exact-commit export,
  deterministic-build design, canonical payload and selected ADR option.
- Quality and assurance owners: confirm verifier independence, hostile-input
  coverage, exact-byte Linux/Windows matrix and evidence requirements.
- Security owner: confirm least privilege, no secrets, untrusted archive/payload
  handling and no automatic installation or evaluator selection.
- Release owner: confirm no release vocabulary or state, package index,
  credential, tag, release bundle, promotion path or publication workflow link.
- Service owner: confirm GitHub artifact dependency, failure convergence,
  expiration and reproduction behavior are acceptable.
- Engineering owner: confirm the work can be implemented entirely within the
  declared execution scope and decision envelope.

## Exact transition set

| Artifact | Transition | Accountable role |
| --- | --- | --- |
| `INT-IPK-001` | `draft -> approved` | product-owner |
| `CAP-IPK-001` | `draft -> approved` | product-owner |
| `REQ-IPK-001` | `draft -> approved` | requirements-steward |
| `REQ-IPK-002` | `draft -> approved` | requirements-steward |
| `REQ-IPK-003` | `draft -> approved` | requirements-steward |
| `SPEC-IPK-001` | `draft -> approved` | technical-owner |
| `ARCH-IPK-001` | `draft -> approved` | technical-owner |
| `ADR-IPK-001` | `draft -> approved` | technical-owner |
| `VER-IPK-001` | `draft -> approved` | assurance-owner |
| `WO-IPK-001` | `draft -> approved` | engineering-owner |

No other artifact or state is included. The transitions approve definitions;
they do not start work or authorize a workflow run or other external action.

## Read-only transition preview

The exact released `se-harness 0.6.0` evaluator passed runtime identity,
managed-root doctor and repository validation before preview. The preview used
the exact ten artifact/actor pairs above and omitted `--apply`.

| Observation | Result |
| --- | --- |
| Operation outcome | `completed` |
| Compatibility checkpoint | `pass` |
| Planned transitions | 10 |
| Scoped blockers | 0 |
| Repository blockers | 0 |
| Changed paths | 0 |
| Files written | none |

All ten artifacts were `draft` before the preview and remained `draft` after
it. The preview proves only that the exact transaction is currently legal; it
does not supply any accountable decision.

## Suggested accountable response

> As all accountable roles, I approve the complete reviewed IPK packet and
> authorize applying exactly the ten draft-to-approved transitions described
> in the Integration Package definition-review packet. Do not start WO-IPK-001
> or perform any external action.

After the exact ten transitions are applied and validated, the next separate
decision is whether the engineering owner starts `WO-IPK-001`.

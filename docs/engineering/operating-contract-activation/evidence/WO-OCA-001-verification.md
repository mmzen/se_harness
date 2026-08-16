# WO-OCA-001 implementation and verification evidence

## Authority and scope

The repository owner explicitly approved the `OCA-001` packet and authorized `WO-OCA-001` on 2026-08-16. This evidence records the bounded implementation and checks against `VER-OCA-001`. It does not independently verify the candidate or authorize a commit, aggregate VREC, verification transition, push, pull request, merge, release, tag, publication, or deployment.

## Implemented operating commitments

Exactly these six records changed from `draft` to `approved`:

| Contract | Exact active requirement scope | Operating sections |
| --- | --- | ---: |
| `OPS-AGR-001` | `REQ-AGR-001..008` | 9 |
| `OPS-IAR-001` | `REQ-IAR-001..018` | 9 |
| `OPS-PMI-001` | `REQ-PMI-001..007` | 9 |
| `OPS-PYP-001` | `REQ-PYP-001..005` | 9 |
| `OPS-VSP-001` | `REQ-VSP-001..007` | 9 |
| `OPS-WLC-001` | `REQ-WLC-001..006` | 9 |

For the six contracts activated by `WO-OCA-001`, every `assures` relation targets an active requirement in deterministic numeric order. This statement did not assess the older `OPS-DST-001` and `OPS-REV-001` relations; their explicit migration is governed separately by `WO-OCA-002`. The two previously partial contracts, `OPS-IAR-001` and `OPS-WLC-001`, now define service objectives, observability, alert and escalation behavior, capacity and cost boundaries, backup and recovery, security and compliance controls, automated-remediation limits, runbooks, and evidence retention. The other four contracts were reviewed against current commands and authority boundaries.

The six domain indexes identify the approved operating obligation independently from the unchanged draft release proposal. The repository artifact index now includes the cross-domain activation packet.

## Managed authoring guidance

The root and canonical `OPERATING_CONTRACT.template.md` examples now use only `assures = ["REQ-xxx"]`, consistent with the authoritative catalog in `TRACEABILITY.md`. `harnessctl upgrade . --apply` refreshed the schema-2 lock while leaving `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml` protected and unchanged.

After newline normalization, both template copies and the lock entry have SHA-256 `c43646bead3c08b0bee0cdf1326c7a95b95ceb8b9141bf0a5ac7418c48613468`. `harnessctl doctor .` reports the root template as matching the distribution and unchanged under managed integrity.

## Lifecycle and graph evidence

- Formal validation passes with 350 artifacts, zero errors, and the same 40 pre-existing maintenance warnings.
- Validation planes remain `structure E0/W0`, `governance E0/W0`, `policy E0/W0`, and `maintenance E0/W40`.
- `definition_pending` decreased from twelve items to six. The remaining items are exactly `REL-AGR-001`, `REL-IAR-001`, `REL-PMI-001`, `REL-PYP-001`, `REL-VSP-001`, and `REL-WLC-001`.
- After work-order completion, `active_work` is empty and `decision_required` is zero.
- Current inspection contains 350 artifacts, 1,271 relations, 43 warning findings, zero error or informational findings, nine non-automatic suggestions, and no new formal warning.
- Two consecutive final JSON inspections were byte-identical with SHA-256 `b94c721adb9156cb94134ae2372cac665abca8079b85e5423f8ed2d412f81113`.
- Changed-path inspection found no file under a `release/` or `releases/` directory.

## Required gates

- Start and review preflight for `WO-OCA-001` pass and select the complete OCA chain.
- `harnessctl validate .` passes with zero errors.
- `harnessctl doctor .` passes required files, distribution parity, managed integrity, and the released self-hosting governor check; it reports only the known historical-location advisories.
- Python 3.11.9: 188 tests passed with 3 expected skips.
- Python 3.14.6: 188 tests passed with 3 expected skips.
- `git diff --check` passes; Git reports only expected Windows line-ending notices.

## Authority review

The repository owner's explicit approval accepts these continuing obligations but does not imply release authority. The contract bodies keep automation within observation, preparation, and non-authoritative suggestion boundaries. Release, verification, publication, and deployment decisions remain assigned to their accountable owners and records.

## Deviations and deferred gap

No deviation from `SPEC-OCA-001` was required. The executable validator currently requires a non-empty `assures` relation but does not enforce that its targets are requirements. The current graph and managed template comply with `OPS.assures -> REQ`; adding fail-closed target-type enforcement is a separate behavior change requiring its own governed work.

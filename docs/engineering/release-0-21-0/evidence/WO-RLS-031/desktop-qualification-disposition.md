# Codex Windows desktop qualification disposition

On 2026-10-02, human mmzen accepted the unverified Codex Windows desktop
qualification and its residual risk for WO-RLS-031. Released evaluator 0.20.1
applied DEC-RLS-001 = decided (accept) and RISK-RLS-001 = accepted atomically.
The exact human statement, accountable identity and revisit trigger are retained
in those formal records.

- [Accepted deviation](../../decisions/DEC-RLS-001.md)
- [Accepted risk](../../risks/RISK-RLS-001.md)

## Current assessment

| Item | Result |
| --- | --- |
| Codex Windows desktop startup, selection, compaction and resume | Unverified; no matching native desktop evidence is claimed. |
| Missing desktop qualification for this release | Accepted deviation under SPEC-IAR-016#IAR-EXT-010, limited to WO-RLS-031 and 0.21.0 / proposed plugin 0.2.4. |
| Residual risk | Accepted by mmzen in RISK-RLS-001. Desktop-specific delivery or recovery defects may remain undetected. |
| Native CLI/app-server and Claude evidence | Retains only its original observed meaning; it is not desktop proof. |
| Other qualification and release checks | Still required against the final candidate. |
| Final aggregate VREC, exact release-record decision and publication | Not supplied by this decision. |

## Evidence handling

Preserve preparation.md, qualification-status.md and qualification-observations.json
as historical observations from before this decision. Their statements that no
waiver existed describe that earlier state. Do not replace missing results with
passes or modify earlier bound evidence. Use this disposition together with the
original assessment when preparing final assurance.

The final aggregate capture must retain DEC-RLS-001, RISK-RLS-001 and this
assessment as explicit evidence inputs. Reassess their applicability for the
actual candidate and all remaining contract criteria. The acceptance does not
by itself mark WO-RLS-031 implemented or verify any candidate.

Revisit before a subsequent release, a claim of verified Codex Windows desktop
support, or adoption relying on desktop replacement delivery, whichever occurs
first. Separate marketplace and adoption work retain their own requirements.

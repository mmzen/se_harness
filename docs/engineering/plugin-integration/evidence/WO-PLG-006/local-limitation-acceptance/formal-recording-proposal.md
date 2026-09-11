# Proposed formal recording

Status: proposal only. The operator has already accepted the local limitation;
this is not another request for acceptance and applies no lifecycle change.

## One shared standing deviation

- Kind: deviation against `SPEC-PLG-008#PLG-HOOK-002`.
- Scope: the documented absence of a required local refusal when the host loses
  the hook or its valid output, on the tested Codex and Claude Code profiles.
- Concerns: WO-PLG-005, WO-PLG-006, SPEC-PLG-005, SPEC-PLG-006,
  SPEC-PLG-008, VER-PLG-005 and VER-PLG-006.
- Options: accept the documented local limitation, or stop pending remediation.
- Accountable role: technical-owner, as owner of the departed specification.
- Accepted answer to retain verbatim: "I accept the hook failure as a documented local limitation".
- Review trigger: awaiting the operator's answer to the interactive question.
  Proposed trigger: before the first public plugin release, any supported
  host-profile expansion, or introduction of remote acceptance controls.

The released evaluator must write the disposition through `harnessctl decide`.
The DEC identifier must be checked across current refs before allocation.
DEC-PLG-001 and DEC-PLG-002 are terminal activation decisions and stay unchanged.

## Delivery scope

The two implementation WOs allow their evidence directories, but do not allow
new files under `decisions/` and explicitly exclude approved-definition amendments.
The formal DEC therefore needs a separately authorized recording scope, such as
one small governance-recording WO. Recording this already authorized decision
requires no adapter code change and grants no additional execution delegation.

## What the record does

SPEC-DCM-001 and TRC-015 provide a standing accepted deviation, visible on the
specification, concerned work orders and later verification/release records.
The failed observations remain failures; Codex's literal OS shell-start case
remains untested. Free-text review triggers are not an automatic expiry control.

PLG-HOOK-004/009 and the host specifications' -007/-010 rules continue to require
truthful unenforced/unqualified reporting. This DEC alone does not change the
VER-PLG-005/006 pass conditions or authorize completion. Any future contract
change allowing a qualified plugin with this local limitation requires the
technical owner's specification decision and assurance owner's verification
contract decision. Independent remote acceptance enforcement is still unproven.

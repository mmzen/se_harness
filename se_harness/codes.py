"""Every diagnostic code the package raises, named once (SPEC-ECP-023 ECP-PRM-016, ECP-PRM-017).

A module raises `CodedError(CODE, message)`, one of its subclasses, or builds its
diagnostics from these names; no package module spells a code as a literal. The one
exception is `interpreter_safety.py`: SPEC-REB-015 rule 2 binds it to the standard
library, so it spells its `EPS` codes itself and this registry names them for the index.
A name is its code with `-` written `_`. `repository_tools/diagnostic_code_index.py`
reads this file through the parser (ECP-PRM-018), never by import, to render
`docs/notes/diagnostic-codes.md`; the meaning of each family is the comment above it.
"""

from __future__ import annotations

from se_harness.installer import HarnessError


class CodedError(HarnessError):
    """A coded refusal: `code` names the check that refused, `message` the reason.

    `str(error)` is `code: message`, the wire form `harnessctl` prints and splits; a
    subclass that renders another form sets the two attributes itself.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


# Workflow execution: a check, transition or evidence operation is refused (SPEC-WEX-002, SPEC-ECP-005).
WEX001 = "WEX001"
WEX190 = "WEX190"
WEX200 = "WEX200"
WEX201 = "WEX201"
WEX210 = "WEX210"
WEX220 = "WEX220"
WEX221 = "WEX221"
WEX230 = "WEX230"
WEX301 = "WEX301"
WEX302 = "WEX302"
WEX303 = "WEX303"
WEX304 = "WEX304"
WEX401 = "WEX401"
WEX402 = "WEX402"
WEX403 = "WEX403"
WEX404 = "WEX404"

# Workflow execution: an agent-directive-surface refusal.
WEX_ADS_001 = "WEX-ADS-001"
WEX_ADS_003 = "WEX-ADS-003"

# Workflow execution: a control-plane refusal.
WEX_ECP_001 = "WEX-ECP-001"
WEX_ECP_002 = "WEX-ECP-002"
WEX_ECP_003 = "WEX-ECP-003"
WEX_ECP_010 = "WEX-ECP-010"
WEX_ECP_011 = "WEX-ECP-011"
WEX_ECP_012 = "WEX-ECP-012"
WEX_ECP_013 = "WEX-ECP-013"
WEX_ECP_014 = "WEX-ECP-014"
WEX_ECP_022 = "WEX-ECP-022"
WEX_ECP_030 = "WEX-ECP-030"
WEX_ECP_031 = "WEX-ECP-031"
WEX_ECP_040 = "WEX-ECP-040"

# Mutation guard: an installed-root write is refused before any file changes (SPEC-REB-012).
MG001 = "MG001"
MG003 = "MG003"
MG004 = "MG004"
MG005 = "MG005"
MG006 = "MG006"

# Runtime identity: the running evaluator's identity could not be proven; RID000 is the fallback of an unlabelled diagnostic.
RID000 = "RID000"
RID001 = "RID001"
RID002 = "RID002"
RID003 = "RID003"
RID004 = "RID004"
RID005 = "RID005"
RID006 = "RID006"
RID007 = "RID007"
RID008 = "RID008"
RID009 = "RID009"
RID010 = "RID010"
RID011 = "RID011"
RID012 = "RID012"
RID013 = "RID013"
RID014 = "RID014"
RID015 = "RID015"
RID016 = "RID016"
RID017 = "RID017"
RID018 = "RID018"
RID019 = "RID019"
RID020 = "RID020"
RID021 = "RID021"
RID022 = "RID022"
RID023 = "RID023"
RID024 = "RID024"

# Interpreter safety: the entry-point safety rule that refused. Raised by `interpreter_safety.py`, which spells them itself (SPEC-REB-015 rule 2).
EPS001 = "EPS001"
EPS002 = "EPS002"
EPS003 = "EPS003"
EPS004 = "EPS004"
EPS005 = "EPS005"
EPS006 = "EPS006"
EPS007 = "EPS007"
EPS008 = "EPS008"
EPS009 = "EPS009"
EPS010 = "EPS010"
EPS011 = "EPS011"

# Release qualification: a result could not be produced or retained.
RQ001 = "RQ001"
RQ002 = "RQ002"

# Release qualification: a complete-candidate check.
CC001 = "CC001"
CC002 = "CC002"
CC003 = "CC003"
CC004 = "CC004"

# Release qualification: a candidate-package check.
CP001 = "CP001"
CP002 = "CP002"

# Release qualification: a released-root check.
RR001 = "RR001"
RR002 = "RR002"
RR003 = "RR003"
RR004 = "RR004"

# Release qualification: a public-install check.
PI001 = "PI001"
PI002 = "PI002"
PI003 = "PI003"
PI004 = "PI004"
PI005 = "PI005"

# Release qualification: retired predecessor-view checks, reserved and emitted by no path.
PV001 = "PV001"
PV002 = "PV002"

# Preflight: the artifact graph could not be read or validated (the validator's own codes are re-emitted as `A-` plus the code).
A001 = "A001"

# Preflight: an installation check failed.
I001 = "I001"

# Preflight: a work-order or graph warning; W013 is also the validator's code the CLI filters.
W001 = "W001"
W002 = "W002"
W003 = "W003"
W004 = "W004"
W005 = "W005"
W010 = "W010"
W011 = "W011"
W012 = "W012"
W013 = "W013"
W016 = "W016"
W017 = "W017"
W018 = "W018"
W019 = "W019"
W020 = "W020"
W021 = "W021"
W022 = "W022"
W023 = "W023"

# Agent-directive-surface warnings the package emits or re-emits.
W_ADS_001 = "W-ADS-001"
W_ADS_002 = "W-ADS-002"

# Control-plane warnings the package emits.
W_ECP_002 = "W-ECP-002"
W_ECP_005 = "W-ECP-005"

# Installed-validator errors the package consumes to classify a broken graph; it raises none of them.
E001 = "E001"
E003 = "E003"

# CI-pipeline findings the release-unit derivation and the gate emit.
E_CIP_001 = "E-CIP-001"

# Decision-artifact findings the gate emits.
E_DCM_004 = "E-DCM-004"

# Risk-artifact codes the CLI names in its advisories; the validator raises them.
E_RSK_003 = "E-RSK-003"

#: The record preparations the CLI labels by cause class (SPEC-ECP-016 ECP-CLI-007):
#: a refused verification record and a refused release record, per cause.
VERIFICATION_RECORD_REFUSALS = {
    "state": WEX301,
    "provenance": WEX302,
    "evidence": WEX303,
    "inputs": WEX304,
}
RELEASE_RECORD_REFUSALS = {
    "state": WEX401,
    "provenance": WEX402,
    "evidence": WEX403,
    "inputs": WEX404,
}

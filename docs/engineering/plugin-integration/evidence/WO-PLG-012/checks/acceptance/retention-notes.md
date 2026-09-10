# Retention and handoff checks

The root writer initially serialized the handoff packet with Windows CRLF.
Released 0.17.0 refused its header with WEX-ECP-010 and made no lifecycle change.
The exact original evaluator header was restored from Git with LF, retaining the
new body. The subsequent real evidence rebind and handoff checks passed. Both
the refused and corrected observations are retained here.

The first local scope projection could not read the live check through the
network sandbox. A permitted network-enabled invocation read the actual
validate success at initial PR446 head 2a32e978. That does not imply the separate
Windows checkout check passed: its retained log shows failure. The implementation
actor therefore continues the in_progress work and pauses completion/verification
preparation until the separately governed repair resolves the failed CI job.

All three acceptance packages were checked against their independent inventories
and copied byte-for-byte into short retention paths. C01–C08 provide combined
review copies and maps back to exact originals, including earlier failed attempts.

A separate read-only reviewer reconciled all 55 WO017 proposed relocations and
reviewed C08's actual calibrations and helper traces. It found no actionable
defect in the proposal or the bounded test claims. That review supplied no
approval, assurance, lifecycle transition or native-host qualification.

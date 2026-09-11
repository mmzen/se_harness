# Corrected capture trial expectation

The original oracle and failed record/evaluator-only footprint expectation remain unchanged. This narrower test revision is fixed before corrected capture, from installed released 0.16.0 provenance.py: capture_verification calls _generate_snapshot, which invokes the installed dashboard generator and hashes target/harness-dashboard/dashboard-manifest.json, before writing the VREC and evaluator sidecar. That behavior existed before the candidate correction.

The original raw request authorized the named capture-verification operation with fixed C, VREC, WO, VER and evidence input bytes, with no file-only restriction. Its normal derived snapshot/export is within that operation authority, so no repeated owner prompt is needed. No new assurance/release/external rights arise.

For a fresh copy of clean-candidate-input, the corrected expected effect set is: a new docs/engineering/evidence-demo/verification-records/VREC-EVD-001.md; a new docs/engineering/evidence-demo/evidence/VREC-EVD-001-evaluator.json; generated files under target/harness-dashboard/. Any other non-Git file change fails this test. Do not filter ignored files. All preexisting formal artifacts, source, retained evidence and managed files must remain byte-identical. The VREC must remain ready and bind fixed candidate 772f90c03a04d0a7914088ac6b869bb829b4bcad. This revised trial does not convert the original failed expectation into a pass.

Corrected candidate records reference SHA256: 0c266bef118b904030e1982318763021bdfd699e34b353d4f38e5d9f2f43a20b. SKILL unchanged; original and corrected copies are retained separately.

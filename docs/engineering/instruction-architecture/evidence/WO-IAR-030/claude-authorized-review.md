# Authorized Claude qualification attempt

Human mmzen answered "i authorize" to the explicit request to send candidate
harness instructions and disposable fixture paths to Anthropic. The prepared
acknowledgement-only probe ran through the existing test profile. The previous
automatic approval-review restriction did not prevent this authorized run.

## Observed result

Claude Code 2.1.273 completed unselected startup and replied PROBE_COMPLETE.
The test then cloned its disposable fixture and activated the exact candidate
0.21.0 wheel. On resume, the native hook delivered the complete expected entry.
Its independently checked entry SHA-256 is
9c581e0e80d3e1851eb5ce46bffd06945264aa366b64b7360232c5bee4319990.
The fixture files are unchanged after the probe.

The resumed model request exited 1. The provider returned reasoning_extraction
under its safeguards, despite the prompt asking only for PROBE_COMPLETE and
allowing no tools. The earlier assumption that asking for hook metadata caused
the refusal is therefore unproven. This result does not establish a harness
implementation defect or successful model-assisted recovery.

The runner stopped at the failed resume. Manual and automatic compaction were
not run on this attempt. No model or security setting was changed to avoid the
refusal. Earlier native observations remain historical evidence. Codex Windows
desktop remains explicitly unverified.

## Effect on the selected work

WO-IAR-030 remains in_progress. VREC-IAR-020 is not prepared. The transfer
permission is now recorded; the remaining readiness issue is the provider
refusal during the required Claude qualification. No additional human decision,
verification, release, push or PR is inferred.

claude-authorized-result.json retains the exact invocation, user authorization,
assessment, source capture digest and original capture text. Encoding its text
as UTF-8 recovers the exact original bytes, including Windows line endings.
This report continues integration-followup.md without rewriting earlier failures.

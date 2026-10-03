# README correction implementation review

Removed only the second exact copy of the host-limit paragraph. The complete
warning remains beside installation. The README now has 648 words, within the
650-word requirement. Its SHA-256 matches the reviewed proposal exactly.

All 44 tests in the three required onboarding/documentation modules pass on
Windows. The check also confirms the word, line and heading limits and the
remaining warning. Commands, links, versions, images and test thresholds are
unchanged. See implementation-checks.json for actual arguments and output.

The original Linux CI failure is preserved in ci-failure.json. Fresh full-suite
CI is required on the corrected review head before merge. Neither this local
result nor prior VREC-PLG-033 waives that integration requirement.

This work adds no product mechanism. It removes repeated prose and reuses existing
tests. Codex performed implementation; mmzen retains the assurance decision.
Claude Code and Codex Windows desktop remain not tested/unverified. No package,
host profile, repository evaluator selection or release marker changed.

The correction baseline is 41ad6df4757f19d651f9093f5f8a0d12f705887b, the exact
reviewed proposal. The combined PR continues to use its original integration
base 73abb4902fe819a6d4f11ce160dbe96a90249122 and all three work orders.

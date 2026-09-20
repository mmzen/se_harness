# README blocker resolved, 2026-09-20

The separate owner-approved WO-DOC-017 restored the reviewed README setup path.
Both combined-source suites now run 1,081 tests with no failures: Windows has
15 skips, Ubuntu/WSL two. The applied documentation suite has 32 passing tests.
The earlier 12 onboarding failures are preserved in the original records.
The exact commands, working file hashes and outputs are retained under
docs/engineering/harness-distribution/evidence/WO-DOC-017/.

The tested candidate was c90a3dbf7d56c2554aeca0f9fa87010f24960062 plus the
reviewed README and the two new documentation records. WO-KIS-014 code and
tests are unchanged from that saved commit. The original E1-E5 regression
cases pass in both full runs. The earlier design review remains applicable;
no implementation changes are concealed in this continuation.

## Complete scope across the two selected orders

Original recovery base: cc211403b7d37b3eb74ea170deea418f0aee3dab. Documentation base:
c90a3dbf7d56c2554aeca0f9fa87010f24960062. Both remain retained; no later base
is substituted to hide the original implementation.

Use the released check-pr command locally with a clearly labelled synthetic
event selecting WO-KIS-014 and WO-DOC-017. Its existing implementation checks
the complete Git diff against the union of both approved scopes, then runs
each active order's handoff against that order's admitted paths. This is the
released multi-order route, not a handcrafted truncated change list. Retain
its actual result. No GitHub PR or hosted CI result is claimed or created.

This keeps the README repair under its own approved order. It changes no
scope, approval, historical evidence or owner acceptance. Required local
checks now pass; hosted Python 3.11/full-scale CI remains unrun. Later ready
verification records must identify the actual committed candidate and tests.

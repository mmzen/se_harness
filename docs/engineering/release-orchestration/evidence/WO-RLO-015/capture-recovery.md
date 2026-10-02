# Capture environment correction

Source and tests are unchanged from implementation commit
`7cf08306f0bf87c3f14ec8a2a328de91fa0a67af`. All 19 hosted checks pass on the
completed candidate `e63906e2e2dccf028848f813bd7672180e50ddde`.

Two exact-candidate capture attempts failed before creating a verification record.
The first evaluator error retained only stderr, which omitted the test failure.
A wrapper retained the full second run: 1,255 tests, 22 skips, one error in
`CompleteReleaseTests.test_resolver_binds_one_real_git_review_and_refuses_later_plan_changes`.

The capture driver injected `core.autocrlf=false` for canonical evaluator checkout
bytes. The test subprocess inherited it. The fixture's text writer produces CRLF
on Windows, while its independently computed expected digest uses LF. Under the
override, Git kept CRLF; the publisher correctly refused the digest mismatch.
The workstation's ordinary Git configuration is `core.autocrlf=true`. The same
focused test passes when the capture-only override is absent.

The corrected test wrapper removes only that injected override for its child
test process. It keeps the selected Python runtime, full suite and four workers.
The evaluator still uses canonical checkout bytes. No global setting, product
code, test code, expected digest or refusal rule was changed. This qualifies the
ordinary Windows test environment; it does not claim the fixture works under
every Git newline configuration.

`capture-recovery.zip` preserves both failures, the detailed output, actual commands,
focused recovery result, successful hosted checks and the corrected test-wrapper
source. Final capture will record its actual full-suite result for the committed
candidate containing these files. Human verification remains pending.

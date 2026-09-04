# WO-DOC-014 technical verification

## Reviewed inputs and scope

On 2026-09-04 the repository owner approved the complete README proposal and
explicitly requested applying and publishing it. The repository files match those
reviewed inputs byte-for-byte:

| File | SHA-256 |
| --- | --- |
| README.md | `d957135c26a3d2e221bdf31b22838d86a5f4f1ee228e8aee509580ebec3181d7` |
| docs/images/harness-explorer-virtual-twin.png | `98947cf557e6d0b2da47678ceea89a2337bf8b45825dc7ed97d057afb7737ba3` |

The README contains 573 whitespace-separated source words and two screenshots.
The presentation and integration-guide tests implement SPEC-DST-024. Detailed
installation, command, evidence, and authority-boundary checks remain in place.

## Technical checks

- `python -m unittest tests.test_public_onboarding.PublicOnboardingTests
  tests.test_progressive_documentation
  tests.test_integration_package.IntegrationPackageContractTests -q`:
  47 tests passed.
- The installed, isolated released evaluator 0.14.0 passed `doctor`, graph
  validation, start/review preflight, and complete Git-derived scope checks.
  Graph validation had zero errors; the existing 69 maintenance warnings remain.
- `python scripts/validate_release_distributions.py --root .`: passed for all
  11 distribution-bearing records.
- `python -m se_harness --help` and `git diff --check`: passed.
- Local full regression with `PYTHONUTF8=1` and eight workers: 1,240 tests,
  zero assertion failures, one pre-existing Windows cleanup error, 26 skips.
  The platform limitation is detailed below; the hosted Linux full suite passed.
- GitHub [candidate source evidence](https://github.com/mmzen/se_harness/actions/runs/33918508741/job/101171148689)
  and [candidate package evidence](https://github.com/mmzen/se_harness/actions/runs/33918508741/job/101171395055)
  passed for the corrected PR revision `61e46bc3c2417cc7ff48970ef752b2e3591a0771`
  as evaluated in the pull-request merge checkout.

## Failures investigated

The first hosted run failed one assertion requiring the phrase "integration
packages" in the root README. That inventory was retired by the reviewed shorter
presentation. Its replacement verifies the root link to the notes index; the
existing next-hop link to the integration guide and every safe-install/authority
assertion are preserved. The corrected focused suite and hosted source run pass.

The first local full-suite reporter could not encode a Unicode arrow under the
Windows default encoding. It was rerun with `PYTHONUTF8=1`. That run also exposed
an unchanged fixture-cleanup error in
`IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`:
`shutil.rmtree` cannot remove a read-only Git object on this Windows host.
The identical single-test failure was reproduced in a detached checkout of the
original base `15a3eec`, establishing that it predates this documentation change.
No unrelated test, runtime behavior, or CI policy was changed to hide it.

## Publication and authority

The owner-authorized publication is tracked in
[PR #344](https://github.com/mmzen/se_harness/pull/344). The final publishing commit
and its hosted checks are recorded there. The final GitHub README and image must
match the hashes above before publication is reported complete.

This is agent-run technical evidence, separate from the owner's prior content
review. It does not create an independent formal VREC decision, a release record,
a package publication, or a deployment. WO-DOC-014 completes implementation only;
formal assurance remains a separate accountable decision.

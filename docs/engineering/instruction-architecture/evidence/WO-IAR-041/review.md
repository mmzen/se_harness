# Plugin integrity fixture: verification review

The existing acceptance test now explicitly selects the optional Git integration
and asserts that its .gitattributes file exists before corrupting it. Setup must
return the failing doctor result and name that file. The previous root-guide
assertion was obsolete under the accepted minimal layout.

Tested implementation commit: `234029d16d9a1d47dfb304b320df1943ce873f41`.

## Results

| Platform | Original real-wheel test | Corrected acceptance suite | Integrity probe |
| --- | --- | --- | --- |
| Windows, Python 3.14.6 | Expected failure reproduced, 1 test | 11 passed, no skips | Clean passes; changed .gitattributes fails |
| Linux, Python 3.12.3 | Expected failure reproduced, 1 test | 11 passed, no skips | Clean passes; changed .gitattributes fails |

The real-wheel test executed on both platforms. Its existing environment
creation, reuse and damaged-package refusal checks pass. Both original CI
failures remain in results.json; CI uses Python 3.11.16 on Linux and 3.11.9
on Windows. All actual commands, runtime identities and outputs are retained.

## Scope and assessment

The approved patch is applied exactly in one test file. No production code,
plugin adapter, wheel resource, CI workflow or required criterion changed.
The independently built 0.21.0 wheel retains archive SHA-256
`a27a797bf2763f48006d28166d41e21437c8c4a935615a1b114e9ff278434594`
and payload SHA-256
`c86a3301491e4ef4188ed98e2fcf8c67bf2c8184bc5e73e97e663f235c7894ac`.
Both installed environments report those exact identities. The selected
repository remains governed by released 0.20.1.

REQ-IAR-031 / SPEC-IAR-016 / VER-IAR-022 integrity coverage is preserved using
the existing optional integration. The test no longer claims that owner content
is harness-managed. It still requires refusal for tracked-content drift.
All 61 evidence files bound by VREC-IAR-020 and VREC-IAR-022 remain
byte-identical, and both records remain unchanged. Prior qualification applies
only to the explicitly compared unchanged product inputs.

## Limits and next decision

The full source suite and native model sessions were not rerun for this bounded
test correction. Updated PR CI, both upgrade rehearsals and downstream integration
jobs remain required before merge. Codex Windows desktop remains unverified.
This work supplies no desktop proof or waiver.

VREC-IAR-023 will bind this correction to its exact candidate and retained evidence.
Human verification remains separate from preparation. No merge, release,
marketplace publication or adoption has occurred.

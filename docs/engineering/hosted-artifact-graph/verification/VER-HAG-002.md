+++
id = "VER-HAG-002"
type = "verification"
title = "Independent draft admission and relationship regression evidence"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"
[relations]
verifies = ["REQ-HAG-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T13:24:31Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved REQ-HAG-009, SPEC-HAG-004, VER-HAG-002 and WO-HAG-002 for local implementation with required commit-bound verification in this conversation. Reviewed manifest SHA-256: e36a47fb59f1bf1f856aa8a47c20189bc84d9d53d787fce505e6bc0f895eabe8. All complete reviewed bytes matched; only the confirmed assurance table was completed before preview. This approval grants bounded local implementation and required verification preparation, not verification acceptance, publication, release or governor adoption. DEC-HAG-001 remains unchanged."
+++

# Independent draft admission and relationship regression evidence

## Independence

Derive expected outcomes from SPEC-HAG-004 and the declared relationship tables,
never from candidate results. Retain the 0.22.0 false-positive reproduction under
WO-HAG-001 as the before case. Fix synthetic fixture identities and expectations
before implementing the corrected classifier. Use both source tests and a wheel
installed into a disposable environment from outside the development checkout.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-HAG-009 | test | EV-01 through EV-06 | Exact specified admissions/refusals, preserved findings and no writes |
| REQ-HAG-009 | inspection | EV-07 | Shared rule source, bounded exceptions and unchanged authority boundary |
| REQ-HAG-009 | demonstration | EV-08 | Installed package repeats decisive cases with retained package identity |

## Acceptance scenarios

1. **EV-01: Valid and incomplete drafts.** For all ten supported types, generate
   the canonical template through the candidate command and check the resulting
   draft. Expect admissible with explicit incomplete findings where appropriate.
   For a requirement, independently test absent/empty/canonical-placeholder
   capability links, complete body and valid existing capability link. Ordinary
   validation/approval retain completeness failures until required content is
   supplied. Draft checks do not change any state or bytes.
2. **EV-02: Wrong endpoint without work-order membership.** Add a requirement
   deriving from an existing release record to a trustworthy fixture. Both draft
   and repository validation refuse; no work order selects that requirement.
   Test capability deriving from a requirement and representative valid/invalid
   pairs for every declared relationship. The independently written expected
   table must not import candidate constants as its oracle.
3. **EV-03: Incompleteness cannot hide invalidity.** Missing non-template target,
   mixed placeholder/wrong-target array, placeholder in the wrong relation,
   empty target string, non-string target, non-array relation, self-link and
   undeclared relation each refuse. Preserve the correct incomplete findings
   when another field also contains an error; admissible must remain false.
4. **EV-04: Catalog and protected inputs.** Malformed or duplicate TOML, duplicate
   IDs, ID/type mismatch, missing ID, invalid date, unsupported record type,
   non-draft state, lifecycle history and disposition each refuse. Unknown
   selection refuses. An unrelated malformed document/duplicate ID prevents a
   trustworthy catalog; other unselected findings remain visible as background.
5. **EV-05: Gates and compatibility.** Run existing authoring, validation,
   preflight, decision and approval tests. Valid accepted chains retain outcomes;
   incomplete authoring cannot gain approval through the new command. Explain
   every newly refused typed edge. Do not modify legacy artifacts to make a
   compatibility test pass. The original public reference corpus remains readable.
6. **EV-06: CLI and no-write boundary.** Test JSON and text, selection, explicit
   target, codes, unsupported/usage failures and repeated deterministic results.
   Compare all fixture bytes before and after pass and refusal. No state event,
   operation receipt, synthetic WO or next-step approval is emitted.
7. **EV-07: Implementation inspection.** Verify one shared type table consumed
   by validation, preflight and draft checks; exact template-field exception
   predicates; no English-message filters, code-wide suppression, second parser,
   server policy copy or governor replacement. Review caller-side protected-field
   comparison as a documented limitation, not a capability claimed by this query.
8. **EV-08: Packaged qualification.** Build under the existing release build
   recipe after reading its prerequisites. Install the actual wheel into a clean
   disposable environment; run from outside the checkout using isolated Python.
   Repeat EV-01 requirement, EV-02, mixed-target refusal, malformed input and
   lifecycle-history refusal. Record wheel SHA-256, installed payload identity,
   Python/platform, commands, exit codes and output. This is candidate testing,
   not formal release or repository adoption.

## Commands and platform

Initial platform: the current Windows PowerShell host with Python 3.13 for local
tests; the repository's pinned build runtime applies to distribution builds.
Use `python -m unittest tests.test_draft_validation tests.test_relation_policy
tests.test_artifact_authoring tests.test_authoring_gate tests.test_cli_shape -v`
once these candidate tests exist, then the repository-owned
`python scripts/run_tests.py` (canonical serial equivalent is documented in
AGENTS.md). Run `python scripts/validate_release_distributions.py --root .` when
distributions exist, and the applicable installed-package checks from EV-08.
Retain unsupported/missing environments as limitations rather than simulated passes.

## Evidence retention and acceptance

Store independent fixture expectations, before/after observations, actual command
logs, compatibility differences, package identities and inspection results under
docs/engineering/hosted-artifact-graph/evidence/WO-HAG-002/. Bind the final clean
candidate through the normal VREC preparation after all work is complete.
No test is claimed to have run by this draft contract. mmzen makes the later
verification decision. No production, deployment, release or hosted walkthrough
acceptance is supplied here.

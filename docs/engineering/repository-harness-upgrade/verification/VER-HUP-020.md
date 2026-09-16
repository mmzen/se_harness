+++
id = "VER-HUP-020"
type = "verification"
title = "Verify provider-aware governor-transition assessment"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-16"
updated = "2026-09-16"

[relations]
verifies = ["REQ-HUP-008", "REQ-HUP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T14:03:02Z"
decided_by = "assurance-owner"
reason = "The owner approved this exact reviewed package with \"i approve\" on 2026-09-16, exercising the assurance-owner decision for VER-HUP-020. Reviewed SHA-256 edb0c5c5eaf1617f689da8f0ff15138cccb4a7f5e3818210caa057b90345b15f. This approves the definition or bounded execution scope; it records no assurance or external-delivery decision."
+++

# Verify provider-aware governor-transition assessment

## Independence

Expected results come from SPEC-HUP-020 and the existing transition contract.
Small Git fixtures set explicit before/after locks and expected outcomes;
they must not generate expected decisions with the implementation's comparison.
Use the existing test module and helpers. Check the actual PR boundary as a
separate integration case after the corrected candidate is committed.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-HUP-008 | test, inspection | Provider switches, steady-state cases, drift refusals, existing upgrade tests and exact PR replay | Ownership-only changes need no evaluator transition; evaluator and unrelated lock changes still fail; actual upgrades retain exact evidence checks and assessment is read-only. |
| REQ-HUP-024 | test, inspection | Schema/provider boundaries and released root integrity | Valid schema 3 and schema 4 read; pre-3, unknown schemas and invalid schema-4 provider records refuse; the selected 0.18.0 root still passes doctor. |

## Focused acceptance

1. Repository-to-plugin switch and restoration with equal evaluator identity
   produce transition_required=false and the existing not_applicable result.
   Include missing old seed entries, which the released migration permits.
2. Ordinary changes with unchanged schema-3 and schema-4 locks pass. A
   supported older schema-4 provider record remains readable.
3. Refuse malformed provider records, unsupported schemas and same-version
   changes to evaluator identity, hash contract or unrelated lock fields/files.
   Catalogue membership cannot excuse a managed/fragment hash change.
4. Refuse an ownership exception whose trusted-base catalogue is unavailable
   or malformed. A target catalogue edit cannot permit removal of an unrelated
   lock entry. Fixtures exercise outcomes rather than private helper shapes.
5. Retain the existing actual-upgrade tests, including exact release and
   transaction bindings, wrong hashes, base selection and checkout integrity.

## Integration and required checks

- Run tests.test_governor_transition on the available Windows Python 3.13
  runtime, then the full source suite once. Run the repository-required release
  distribution validator and candidate CLI help; retain candidate doctor skew
  separately from the isolated governing result.
- With the isolated released evaluator 0.18.0, run doctor, graph validation,
  phase-appropriate preflight and scope/handoff checks. Zero errors are
  required; report warnings with their relevance.
- From a clean corrected candidate, invoke the same python -S planner and
  assessor used by CI against PR base
  f05c478a29c39f94968fdc842a34c861d30a42ac. Both must succeed without an evaluator
  transition or checkout change. Retain the original failure as baseline.
- Compare root lock/configuration, managed files, plugin publication inputs
  and historical records with remediation base
  0dadc352b3a5e6c64c721e1c688cc215438ddd7f; this fix changes none of them.
- After authorized delivery, the existing Linux predecessor assessment and
  other required PR checks must pass before integration. Hosted outcomes are
  reported only when observed; no local result substitutes for them.

## Evidence and assurance

Keep concise observed results and retrievable raw logs under
docs/engineering/repository-harness-upgrade/evidence/WO-HUP-020/.
Identify commands, exit codes, actual interpreter, evaluator and full candidate
commit. Explain the small comparison and any material review finding in the
normal implementation evidence.

Prepare one fresh aggregate VREC covering WO-HUP-020 and WO-PLG-025 at the
corrected candidate, conforming to this contract and VER-PLG-025. Reuse earlier
cleanup evidence only after comparing its relevant inputs and recording the
basis for reuse; run the final integration checks on the corrected candidate.
For this later aggregate only, this approved contract permits VREC-HUP-019 and
its HUP evidence location in place of VER-PLG-025's original VREC-PLG-022-only
capture instruction. VER-PLG-025's cleanup scope and preservation assertions
apply to the cleanup portion; the separately authorized assessor changes are
assessed under this contract. Its substantive cleanup acceptance remains.
VREC-PLG-022 continues to describe its earlier candidate and remains unchanged.
Owner verification and external delivery remain separate decisions. A ready
record may identify hosted CI as pending until delivery makes it observable.

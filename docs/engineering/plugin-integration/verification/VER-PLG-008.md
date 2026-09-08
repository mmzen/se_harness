+++
id = "VER-PLG-008"
type = "verification"
title = "Supported tool-action enforcement acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-013", "REQ-PLG-014"]
+++

# Verification Contract: Supported tool-action enforcement acceptance

## Independence

The assurance owner defines allowed and refused effects independently of the adapter's classifier. Compare evaluator observations and actual target changes, not just hook exit codes.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-013 | test | Covered in-scope/out-of-scope edits; failed or interrupted checks | Current required checks precede effect; refusals leave the target unchanged. |
| REQ-PLG-014 | test | Malformed/ambiguous governed actions on refusing and non-refusing host protocols | Refusal precedes effect where supported; otherwise report unenforced. Never claim checked success. |

## Acceptance scenarios

Run explicitly captured host-event fixtures with the released evaluator. Retain exact event, invocation/result, response and simulated target effects; label protocol/OS/Python/evaluator identities.

## Property and invariant tests

Vary artifact, checkpoint and path inputs. A stale result cannot authorize a changed action. Ambiguous/malformed governed actions leave fixture targets unchanged when refusal is supported.

## Static and architecture checks

Review PLG-HOOK-001 through PLG-HOOK-006 and ARCH-PLG-002/ADR-PLG-002. Confirm evaluator checks are reused without embedded policy copies.

## Security and privacy checks

Attempt malformed paths, event spoofing and recursive checking. A recursion guard cannot exempt unrelated governed effects. Document unobserved tools and continuing shell sessions.

## Performance and resilience checks

Measure evaluator time and added adapter time separately, including slow refusals. No required check may be skipped for speed.

## Manual assessments

Inspect refusal-before-effect ordering in the fixture runner. Real host interception/refusal belongs to VER-PLG-005/006 and VER-PLG-015; assess remaining gaps affecting issue #347 explicitly.

## Evidence retention

Retain commands, outputs, failures and platform identities under `evidence/WO-PLG-008/`; bind the later verification record to the exact implementation candidate.

## Residual uncertainty

Fixture acceptance qualifies the handler without waiting for production adapters. It cannot prove live interception or independent external authorization. No check result is asserted here.

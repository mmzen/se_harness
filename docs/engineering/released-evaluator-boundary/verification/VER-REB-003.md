+++
id = "VER-REB-003"
type = "verification"
title = "Canonical evaluator-evidence checkout assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-REB-009", "REQ-REB-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "quality-owner"
+++

# Verification Contract: Canonical evaluator-evidence checkout assurance

## Independence

The implementation actor may add policy and fixtures, but assurance selects the Git configuration matrix, independently computes hashes from fresh clones, reviews attribute precedence, and confirms that exact-byte validation was not weakened. Released-evaluator and candidate observations remain separate.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-REB-009` | Attribute contract | Candidate root, canonical template, installed target, wheel payload | Exact narrow rule exists and all governed copies agree |
| `REQ-REB-009` | Fresh-checkout matrix | `core.autocrlf=true`, `input`, `false`; LF/CRLF checkout defaults | `git check-attr` selects `text` and `eol=lf`; evidence bytes and SHA-256 are identical |
| `REQ-REB-009` | Exact-byte negatives | Removed/conflicting attribute, CRLF file, missing LF, content/digest/path/schema tamper | Every variant fails before release authority or external action |
| `REQ-REB-009` | Dual-evaluator integration | Released 0.5 and candidate validator against successor ready RLS | Both pass only for exact LF evidence and approved tuple |
| `REQ-REB-009` | Successor qualification | C3 source/package, two runtimes, reproducible builds, hosted lanes | All unchanged 0.6.0 and bootstrap gates pass with new identities |
| `REQ-REB-010` | Terminal lifecycle matrix | ready/rejected RLS crossed with approved/rejected/missing/wrong bootstrap contract | Only `ready + exact approved` and `rejected + exact rejected` validate |
| `REQ-REB-010` | Authority negatives | Binder, preparation, release, and publication with rejected contract | Every operational use fails before mutation or credentials |

## Acceptance scenarios

1. A clean clone with `core.autocrlf=true` retains the exact canonical evidence SHA-256 and passes candidate validation.
2. The same result holds for `input` and `false` without relying on global attributes.
3. Removing or overriding the rule reproduces the `RLS-SEH-009` CRLF failure.
4. Changing any non-line-ending evidence byte still fails the raw digest and canonical schema checks.
5. Installed and packaged standard templates contain the exact rule while the operational released-0.5 root identity remains unchanged.
6. A successor ready RLS binds the same exact predecessor evaluator through a newly approved one-shot contract and passes both planes.
7. Rejected `RLS-SEH-009` and rejected `REL-SEH-008` retain exact historical validation while only approved `REL-SEH-009` can authorize the successor.
8. Any attempt to bind, prepare, publish, or release through rejected `REL-SEH-008` fails before writes or credentials.

## Property and invariant tests

- The rule affects only JSON directly below governed `evidence` directories.
- Candidate and template attribute bytes are deterministic.
- Git index blob, archive export, LF checkout, and CRLF-oriented checkout yield the same evidence bytes.
- Validator hashing remains raw and does not normalize the evidence under test.
- Historical C2, `VREC-SEH-009`, `RLS-SEH-009`, and their evidence remain byte-identical.
- Rejected contracts never count as active bootstrap authority and cannot be reused.

## Static and architecture checks

- Trace conformance to `SPEC-REB-004`, `ARCH-REB-003`, and `ADR-REB-003` for both requirements.
- Confirm no broad line-ending rule, local-configuration dependency, evidence allowlist, or validator normalization was introduced.
- Confirm candidate/template/package parity and managed-lock behavior.

## Security and privacy checks

- Isolate system, global, and local Git attributes during checkout tests.
- Exercise malicious conflicting attributes, symlink/junction paths, traversal, duplicate JSON keys, digest substitution, and contaminated evaluator origins.
- Retain bounded configuration facts without usernames, home paths, environment dumps, or credentials.

## Performance and resilience checks

Run the matrix on Python 3.11 and the current qualification runtime. Retain exact Git/Python versions, durations, test counts, skips, and failures. Confirm no meaningful checkout or validation regression.

## Manual assessments

- Technical/security owners accept exact LF policy and raw-byte semantics.
- Assurance owner confirms matrix independence and complete negative coverage.
- Release owner confirms C2/RLS disposition and successor release scope.

## Evidence retention

`WO-REB-005` evidence must retain both triggering `E012` diagnostics, the failed zero-write transition plan, exact approved manifest, changed paths, attribute bytes and resolution, checkout and lifecycle matrices, recursive before/after maps, candidate/template/package parity, full regression, reproducible distribution identities, released/candidate identities, hosted runs, graph/inspection/distribution/doctor results, and all actions not performed.

## Residual uncertainty

Git implementations outside the supported matrix may have different attribute behavior. Publication services and protected environments remain external dependencies and require their own later observations.

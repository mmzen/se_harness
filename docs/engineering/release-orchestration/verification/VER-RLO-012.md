+++
id = "VER-RLO-012"
type = "verification"
title = "Verify publication with schema-5 evaluator locks"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[relations]
verifies = ["REQ-RLO-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-03T03:03:59Z"
decided_by = "mmzen"
reason = "mmzen explicitly approved the reviewed WO-RLO-018 and VER-RLO-012 package, required commit-bound verification and correction review PR. Reviewed hashes WO 4dbc7a9827b2153c0e893b5025c4cc3c42299e9185e6148f1dd88cc7c828fc29 and VER 86a0748254fd8047b76ca4b38acaa75b9accec5727e8d10fceaa8aa199b56ba3. Only confirmed assurance metadata added before preview. Verification acceptance and merge remain separate."
+++

# Verify publication with schema-5 evaluator locks

## Independence

Expected identities come from released RLS-SEH-032, verified VREC-SEH-032,
the recorded bundle and the installed schema-5 lock at merged main
01ec43c86c9d30949295c07ac91c742be91e713a. The candidate remains
abbec12ac5524c8adfb28693f846dd59de88f759. Do not derive expected digests from
the corrected resolver. Public evaluator 0.21.0 governs formal checks outside
the checkout; source scripts are the system under test.

## Requirement-to-evidence matrix

| Requirement | Method | Case and pass condition |
| --- | --- | --- |
| REQ-RLO-001; SPEC-RLO-001 rules 3-5 | test | PUB5-01: a valid integer schema-5 lock with released-resources-v1 resolves the same evaluator version, payload and archive identities as its retained evidence. Release and Pages resolvers preserve the RLS candidate and first integrated governance commit. |
| REQ-RLO-001 | test | PUB5-02: missing or invalid schema-5 resource layout, incompatible plugin ownership, unsupported or non-integer schema, malformed evaluator identity, mismatched evidence and unsafe evidence paths fail. Invalid governance locks must not be hidden by maintenance fallback. |
| REQ-RLO-001 | test | PUB5-03: valid schema-3 and schema-4 locks and the historical maintenance fallback remain supported; their existing identity, archive, integrity and evidence refusals remain effective. |
| REQ-RLO-001 | demonstration | PUB5-04: the real evaluator descriptor and release resolver succeed against RLS-SEH-032 on merged main, returning its original candidate, version, tag and hashes. A disposable local Pages rehearsal uses that record and a local-only matching tag, preserves governance identity, and performs no external write. |
| REQ-RLO-001 | inspection, test | PUB5-05: the focused publication suites, full local suite and applicable CI pass at the correction commit. Released evaluator validation, scope and handoff pass. All accepted release records and bound evidence remain byte-identical. |

## Checks

Run the focused tests on Windows and Linux:

```text
python -m unittest tests.test_dashboard_publication tests.test_release_orchestration
```

Run the full source suite on Windows with the repository test runner and full
scale. Retain the actual interpreter, platform and skips. Run the existing
read-only publication rehearsal for the correction ref; it must replay
RLS-SEH-032's recorded archives without publication credentials.

Run these real read-only commands, writing output outside the repository:

```text
python .github/scripts/publish_dashboard.py evaluator --repository REPO --output OUTPUT
python .github/scripts/publish_release.py resolve --repository REPO --default-ref refs/remotes/origin/main --release-record RLS-SEH-032 --output OUTPUT
```

For Pages, use a disposable Git clone containing the correction and the actual
main history. Add only a local v0.22.0 tag at the recorded candidate, then run
publish_dashboard.py resolve with that tag, RLS-SEH-032 and the default main
ref. Label that local tag as a rehearsal input, not published state.

## Evidence retention

Retain the original failures, commands, results, preservation hashes and
rehearsal evidence under evidence/WO-RLO-018/. Capture VREC-RLO-015 at the
exact correction commit, using the fixed evaluator companion under evidence/.
These are proposed unused IDs; recheck before capture. Publish the review PR
before requesting the human assurance decision. This contract does not waive
publication checks, downstream plugin qualification or provider controls.

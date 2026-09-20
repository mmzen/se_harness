+++
id = "VER-DST-030"
type = "verification"
title = "Verify restoration of the README starting path"
status = "approved"
owners = ["assurance-owner", "documentation-owner"]
created = "2026-09-20"
updated = "2026-09-20"

[relations]
verifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T08:30:03Z"
decided_by = "assurance-owner"
reason = "On 2026-09-20 the owner replied \"i approive\" to the reviewed README package, explicitly approving VER-DST-030 and the proposal. Reviewed artifact SHA-256: 544e40d5ee363baf654ed958bd96e2f07ca2f17d7ef765903a6126f354f3f39d. Reviewed README SHA-256: 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d. This records the named formal approval; no assurance acceptance or external delivery is granted."
+++

# Verify restoration of the README starting path

## Expected result

Use REQ-DST-069 and SPEC-DST-024 as the source of expected behavior. Compare
the restored section with approved-readme.md under evidence/WO-DOC-016/;
its LF-normalized SHA-256 is d9cb469ccda4438134ee23b46852a58ecc91595dd2ce87437f4967a4ea1a7c8b.
The earlier approval is comparison evidence, not authority to execute this work.
Historical VER-DST-024/029 and their publication facts stay unchanged.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-069 | Test, inspection | Exact README comparison, existing onboarding/documentation tests, released CLI syntax and render review | Restore usable CLI setup and links while preserving plugin onboarding, presentation budgets and accurate authority claims. |

## Checks

- The final README matches reviewed README-proposed.md, SHA-256 6566a636021d3aaa29345094ad19362289cd26efe01b3684a26da57e7c2d2c9d.
  Restore the missing CLI section from the historical input and preserve
  the two navigation links already added on origin/main at 2b87e04490b933a71a9986c0235ea8b201b3bffc.
  Plugin commands, branding, screenshots and other text are unchanged.
- Run existing tests.test_public_onboarding and tests.test_progressive_documentation
  without changing their assertions. Resolve local links and inspect the render.
  Confirm at most 650 source words, 200 lines and seven level-two headings.
- Check the init/doctor examples against the candidate parser and released
  0.18.0 CLI. Installation examples must keep the tool environment outside
  the project and distinguish package installation from repository upgrade.
- Run the repository-required source suite, distribution validator, CLI help,
  released doctor/graph and phase preflight. Review the exact diff and complete
  scoped change set. Failed required checks block completion.

## Retention and limits

Retain the reviewed input, hashes, commands, runtime identities, raw results
and concise review under evidence/WO-DOC-017/. Initial proposal tests are
preview evidence; test the applied file before claiming implementation success.
Record platforms actually exercised. This does not test a new plugin release,
claim a fresh network installation, grant independent review or authorize
publication. The owner separately assesses the ready commit-bound VREC.

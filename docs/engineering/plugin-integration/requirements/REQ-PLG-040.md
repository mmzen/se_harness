+++
id = "REQ-PLG-040"
type = "requirement"
title = "Align current instructions with the selected and published delivery"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "Current operator guidance uses valid instruction routes, repository-owned AGENTS.md semantics and precise selected-release commands while preserving historical material and truthful public availability."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner-approved marketplace and documentation correction plan, followed by the request to prepare its artifact package on 2026-09-28."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Align current instructions with the selected and published delivery

## Need and applicability

Users and agents need current guidance that agrees with the selected release and
directs them to the current instruction files. This bounded refresh corrects
current operational facts; dated records, migration evidence and accepted
definitions retain their original meaning.

## Required outcome

Correct the audited current installation, command, contributor and model guides.
Keep the existing plugin-first README presentation and its direct manual-setup
links. Explain plugin installation, evaluator setup and repository adoption as
separate operations.

## Acceptance

- Current routes point to existing files and headings in
  `docs/engineering/harness/`. Compatibility pointers are not presented as the
  current authority. AGENTS.md is described as entirely repository-owned.
- Evaluator examples use the selected released interpreter's absolute path,
  `-I -m se_harness`, an outside-checkout working directory and an absolute target.
  Fresh-project examples identify 0.19.0; existing projects retain their pin.
- The getting-started glossary link resolves to the repository GLOSSARY.md.
- Native instruction delivery is distinguished from enforcement of arbitrary
  tool calls. Published 0.19.0 behavior is distinguished from candidate 0.20.0
  installer behavior. Repository-owned skill providers remain clearly separate.
- Source links are checked in the source tree; package-relative links are
  checked in the composed package. No mass replacement rewrites historical data.
- Public-availability statements remain backed by the last retained public
  observation until the public-route work confirms the replacement.

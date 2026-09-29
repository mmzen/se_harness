+++
id = "REQ-PLG-040"
type = "requirement"
title = "Align current instructions with the selected and published delivery"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "Current operator guidance uses valid instruction routes, repository-owned AGENTS.md semantics and precise selected-release commands while preserving historical material and truthful public availability."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner-approved marketplace and documentation correction plan, followed by the request to prepare its artifact package on 2026-09-28."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "product-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 e557a4b3557697d7dabf99c074b8441b6d967ae73721db0044907e21aba4352b; transition input SHA-256 e557a4b3557697d7dabf99c074b8441b6d967ae73721db0044907e21aba4352b. Legacy 0.19.0 role product-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
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

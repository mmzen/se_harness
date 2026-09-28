+++
id = "VER-PLG-026"
type = "verification"
title = "Verify the prepared marketplace and corrected guidance"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"

[relations]
verifies = ["REQ-PLG-039", "REQ-PLG-040"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "quality-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 73ef123fbfe638f71175d65851ea947461c0726094628e32a3d22fa058a2f48a; transition input SHA-256 73ef123fbfe638f71175d65851ea947461c0726094628e32a3d22fa058a2f48a. Legacy 0.19.0 role quality-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
+++

# Verify the prepared marketplace and corrected guidance

## Independence and selection

Expected results derive from REQ-PLG-039, REQ-PLG-040
and SPEC-PLG-023. Obtain wheel identity from RLS-SEH-028, not candidate
source metadata. A work order selecting only one requirement executes the cases
mapped to that requirement; combined verification covers both sets.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-039 | test, inspection, demonstration | MP-01 through MP-05 | The complete candidate matches selected inputs; all claimed local native routes work; public status stays truthful. |
| REQ-PLG-040 | test, inspection | MP-03, MP-06 | Current routes and commands are correct; historical material and release boundaries are preserved. |

## Cases

- **MP-01 — Composition.** At the exact source commit, run the existing marketplace
  build and check commands with the published 0.19.0 wheel and release record.
  Both manifests report 0.2.1; inventories, archives, hooks, skills and wheel
  digest match. Reuse unchanged builder boundary cases; modified/missing package
  input and a mismatched selected wheel must fail without outside writes.
- **MP-02 — Identity assertions.** Run focused offline consistency tests against
  correct data and wrong plugin version, wrong wheel identity, and two mutually
  consistent stale documents. Only the correct independently bound selection
  passes. An unsupported claim of public availability fails.
- **MP-03 — Documentation.** Resolve links/headings in source and assembled
  contexts. Inspect plugin-first onboarding, setup/adoption separation, status
  wording, Python prerequisites and bounded native-hook claims. No unfinished
  placeholder or invented publisher identity is presented as actual data.
- **MP-04 — Native routes.** In disposable Windows profiles on each host, run
  fresh installation, update from public 0.1.0, and replacement of the known local
  0.2.0 selection. Record native versions, source precedence, actual commands,
  active version and installed byte digests. Do not mutate real user profiles.
- **MP-05 — Instruction delivery.** For each host, observe startup and compaction
  after loading the candidate. Compare the complete delivered root with the
  selected consumer's 0.19.0 ENGINEERING_HARNESS.md. Switch between two selected
  repositories and exercise missing/mismatched inputs. Expect the correct new
  root or disclosed gap, never stale authority. Preserve failed observations.
- **MP-06 — Current guidance.** Inspect every path in the documentation work
  order. Check current file/heading routes, the glossary target, whole-file
  AGENTS ownership and absolute external evaluator examples. Retain a file-by-file
  assessment. Historical examples and published 0.19.0 limits remain labelled.

## Commands and environment

Use released evaluator 0.19.0 outside the checkout for formal checks. Run the
focused repository suites on Windows with available Python 3.14:

```text
python -m unittest tests.test_public_onboarding tests.test_progressive_documentation tests.plugin_integration.package_assembly.test_marketplace -v
```

Include applicable package-assembly and native instruction regression cases from
the existing suite; retain the exact collection. Run the documented composition
example against the exact committed inputs. Derive native install/update syntax
from the actual selected CLI help and current official documentation; write the
tested procedure and record versions before claiming support. New native work
requires actual observations; an intercepted command is not a native pass.

## Evidence retention and acceptance

Retain commands, exits, expected/observed identities, output, raw root delivery,
file digests, file-by-file review, failures and environment limits under each
selected WO's new evidence directory. Prepare a clean exact-commit VREC through
the released evaluator. A human decides verification; the implementer cannot
infer acceptance from tests. Any required route lacking evidence prevents the
corresponding acceptance claim and publication readiness.

This contract establishes the prepared candidate and current guidance. It does
not establish public Git delivery; that belongs to the public-route contract.

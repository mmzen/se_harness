+++
id = "REQ-KIS-010"
type = "requirement"
title = "Prepare complete bounded scope before approval"
status = "draft"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
statement = "Before implementation approval, the harness shall help the agent present one complete bounded work proposal, check coverage of its planned paths, and make the human's decision understandable."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "CAP-KIS-001; the repository owner's priority 1 simplification proposal accepted on 2026-10-02"

[relations]
derives_from = ["CAP-KIS-001"]
+++

# Prepare complete bounded scope before approval

## In plain words

The human should review the intended result and the important choices once.
The agent should find foreseeable supporting changes before asking for
implementation approval. A planned-path assessment checks the proposed scope;
it does not prove that the impact analysis is complete.

## Why

Repeated work orders for predictable test, instruction, packaging or evidence
paths interrupt work without adding a new product decision. This change makes
preparation more complete while preserving approval for a real scope expansion.

## Acceptance

1. Preparation inspects the implementation, its callers and references, tests
   and fixtures, documentation, packaging, CI and verification outputs as
   applicable. The work order's existing Expected change surface names the
   planned paths and gives a short reason for each. Non-applicable areas are
   explained briefly.
2. One work order covers one bounded outcome with its necessary supporting
   changes. Exact file paths and narrow component directories use the existing
   admission rules. A directory entry does not authorize unrelated behavior.
3. A read-only assessment of explicitly supplied planned paths distinguishes
   explicit scope, existing automatic admission, uncovered paths and invalid
   inputs. It is usable before work approval. It leaves files and lifecycle
   states unchanged and grants no authority.
4. Preparation explains generated-record admission separately from evidence
   that needs explicit scope. A future record whose ID is unknown is not shown
   as an existing admitted path. Its actual destination is checked when known.
5. The approval request states the decision, reason, expected result, proposed
   changes, checks, material uncertainty and permission being requested in
   ordinary language. Exact artifact IDs, paths and reviewed revisions remain
   available as review details. Existing human decision rights remain intact.
6. A representative bug fix and instruction change reach verification
   preparation in temporary fixtures without another work order for a
   foreseeable omitted path. A deliberately uncovered planned file is caught
   before approval. A real expansion still requires a new human decision.

## Limits

No automatic dependency scanner or claim of exhaustive discovery is required.
No new artifact type, gate, checkpoint, approval right, broad directory
exemption, persistent planning file or universal benchmark is introduced.
Current gate, lifecycle, release and adoption rules remain unchanged.

+++
id = "SPEC-REB-006"
type = "specification"
title = "Hosted predecessor-assessment view and portable fault-injection contract"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[relations]
specifies = ["REQ-REB-013", "REQ-REB-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "technical-owner"
+++

# Specification: Hosted predecessor-assessment view and portable fault-injection contract

## Scope

This specification extends the exact view from `SPEC-REB-005` to hosted released-governor assessment and isolates exclusive-create failure injection behind an adapter-owned seam. It does not change released evaluator 0.5.0, the complete graph, the exact two omitted historical artifacts, root-managed state, or any lifecycle decision.

## Actors and external systems

- Candidate validation assesses the complete graph at the exact candidate commit.
- Shared repository view logic derives and proves the closed rejected pair.
- Git creates one detached, no-local exact-commit assessment clone and supplies tree/blob identities.
- External released evaluator 0.5.0 runs identity, `doctor`, `validate`, and dashboard operations in that view.
- A candidate-owned hosted workflow orchestrates the evidence lane without becoming an evaluator or decision maker.
- The unchanged legacy Engineering Harness workflow retains its full-checkout refusal as a separately labelled observation.
- Assurance injects failures through an adapter-local exclusive-create seam.

## Inputs

- Exact candidate SHA/tree/object format and clean complete checkout.
- The closed `REL-SEH-008`/`RLS-SEH-009` rejected-bootstrap pair, resolved from validated metadata.
- Exact omitted paths, Git blobs, byte lengths, raw SHA-256 values, tuple, and source commit.
- Exact released-0.5 interpreter, entry point, public wheel/payload hashes, version, and schema-2 lock.
- Exact commands and expected legacy diagnostic `E009` for rejected `RLS-SEH-009`.

No caller supplies an omission pattern or expected-error substring.

## Outputs

- Canonical compact UTF-8/LF JSON using schema `se-harness-predecessor-assessment-view-v1`.
- Structured command observations for identity, `doctor`, `validate`, and dashboard, including normalized outputs, exit status, artifact counts, warning/error planes, and output digests.
- A hosted artifact and log bound to the exact candidate, workflow run/job, evaluator, source/view identities, and full-checkout refusal.
- No repository file, index, reference, lock, maintenance state, credential, or external policy mutation.

## State model

```text
exact clean candidate
  -> complete candidate validation
  -> derive and hash exact rejected pair
  -> record exact expected full-checkout 0.5 refusal
  -> create detached exact-commit two-omission view
  -> verify view materialization and unchanged managed surface
  -> run isolated released-0.5 identity/doctor/validate/dashboard
  -> canonicalize assessment evidence
  -> revalidate complete candidate and unchanged checkout
  -> hosted evidence proposal for accountable review
```

Any mismatch stops without durable repository write.

## Behavioral rules

1. **One derivation.** Preparation and hosted assessment use the same closed-pair resolver, Git/object checks, sparse specification, path safety, environment isolation, and TOCTOU rechecks.
2. **Exact legacy observation.** Full-checkout 0.5 execution must first pass evaluator identity and managed-integrity checks and then fail only with governance diagnostic `E009` on exact `RLS-SEH-009`. A generic nonzero exit is insufficient.
3. **No false pass.** The legacy workflow remains failed and is never summarized as successful. Release evidence records that the replacement assessment lane, not full-checkout predecessor validation, passed.
4. **Exact view.** The assessment clone has the exact candidate HEAD/tree and materializes every tracked candidate path except exact `REL-SEH-008` and `RLS-SEH-009`.
5. **Released runtime.** All predecessor operations run through the exact isolated 0.5.0 interpreter/entry point with user site disabled and `PYTHONPATH` absent.
6. **Command closure.** Assessment commands are fixed to identity, `doctor`, `validate`, and dashboard; the caller cannot inject a command, path, environment key, or output destination.
7. **Complete-graph separation.** Candidate validation runs on the full checkout before and after view assessment. Reports identify its runtime separately.
8. **Checkout immutability.** Recursive tracked/untracked state and protected historical hashes are unchanged after the lane.
9. **Evidence closure.** Missing/unknown fields, duplicate keys, noncanonical bytes, host-path leakage, hash drift, or output disagreement fails.
10. **Local fault seam.** Production exclusive create is wrapped by one adapter-local function preserving `os.open` flags/mode. Tests patch only that function and assert exact call ordering and cleanup.
11. **No authority.** Hosted evidence cannot transition a work order, VREC, RLS, contract, tag, publication, deployment, maintenance state, policy, or root evaluator.

## Error and recovery behavior

Zero/one/three omissions, changed blobs, dirty candidates, linked paths, Git configuration drift, evaluator substitution, unexpected legacy output, view errors, candidate errors, command mutation, output collision, or cleanup interference fail closed. Temporary assessment material may be removed after path validation; no source history or evidence is rolled back or rewritten.

## Data and interface contracts

The repository script accepts only repository root, exact candidate commit, external evaluator interpreter/entry point/wheel, and one canonical output path outside the source checkout. The rejected pair and command list are derived. Plan mode may print canonical JSON without writing; hosted apply writes only to a runner-temporary artifact directory.

The workflow pins existing actions, uses read-only contents permission, installs the exact public 0.5.0 wheel by retained digest, uploads only bounded evidence, and proves the source checkout unchanged.

## Security and privacy properties

- No arbitrary omission, expected-error allowlist, shell fragment, credential, network-derived governance input, alternate object database, linked checkout path, or host identity is accepted.
- Evidence normalizes temporary roots and excludes tokens, usernames, home paths, and environment dumps.
- The candidate-owned adapter cannot claim the predecessor saw omitted artifacts.

## Performance and capacity

The lane performs two candidate validations, one bounded clone/materialization check, and four predecessor commands. Existing repository size limits and process timeouts apply.

## Observability

Logs state `legacy full-checkout refusal`, `released-evaluator compatibility-view assessment`, and `complete candidate validation` as distinct planes. Evidence includes run/job URLs, exact SHAs, counts, hashes, and no-mutation proof.

## Compatibility and migration

- C4 `b099a2728d945ee705c1f956ec012f9730df15ac` and both failed hosted runs remain immutable evidence.
- The new implementation creates C5; it never moves or amends C4 or its branch.
- `REL-SEH-010`, reserved uncreated `VREC-SEH-011`/`RLS-SEH-011`, and all earlier records remain unchanged until separate lifecycle authority.
- After an independently published 0.6.0 becomes the root evaluator, ordinary complete-graph hosted validation replaces this transitional lane under separate governance.

## Examples and counterexamples

- **Conforming:** exact legacy `E009`, green full candidate graph, green released-0.5 view whose artifact count equals the complete graph count minus the exact two governed omissions (643 for the reviewed 645-artifact C5 scope), canonical evidence, unchanged source.
- **Non-conforming:** mark the old workflow `continue-on-error` and call CI green.
- **Non-conforming:** delete rejected history from the candidate branch.
- **Non-conforming:** patch released 0.5.0 or run candidate code as the predecessor evaluator.
- **Non-conforming:** monkeypatch shared `os.open` during failure injection.

## Explicitly unspecified decisions

Internal module names, temporary-directory names, and hosted artifact display names are delegated. Exact derivation, commands, hashes, diagnostic closure, runtime separation, and zero-mutation behavior are fixed.

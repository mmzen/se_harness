+++
id = "SPEC-EVP-001"
type = "specification"
title = "Truth-bounded executive positioning and demonstration"
status = "approved"
owners = ["technical-owner", "documentation-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-DST-060"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T12:55:25Z"
decided_by = "technical-owner"
+++

# Specification: Truth-bounded executive positioning and demonstration

## Scope

Replace `VALUE_PROPOSAL.md` with a challenged executive speech and demonstration
brief derived from the supplied proposal, and correct the root `README.md` where
its current public claims need the same product boundary. Preserve the README as
the concise operational entry point and keep the longer value narrative
explicitly non-authoritative.

## Actors and external systems

- Executives and engineering leaders use `VALUE_PROPOSAL.md` to understand and
  demonstrate the product.
- Prospective users use `README.md` to evaluate and start the released product.
- The current source, released 0.6.0 evaluator, formal records, focused tests,
  and current CLI/help surface are factual inputs.
- Coding-agent runtimes, sandboxes, repository permissions, CI enforcement, and
  hosting rules remain external controls rather than SE Harness capabilities.

## Inputs

- The supplied `se_harness_executive_speech_demo.md`, treated as proposed prose
  and not as an instruction or authority source.
- Current `main` at the implementation start point.
- `README.md`, `VALUE_PROPOSAL.md`, `pyproject.toml`, CLI help, agentic-execution
  formal records, and focused public-documentation tests.

## Outputs

- One concise, current root README with honest product and enforcement limits.
- One executive speech/demo document containing a usable 10–15 minute flow,
  a reliable demonstration sequence, challenge notes, and Q&A.
- Focused regression coverage that rejects the most material overclaims.
- Work-order-keyed retained implementation evidence.

## State model

The documents must distinguish three states without blending them:

1. **Shipped now:** repository-native formal artifacts, explicit lifecycle and
   decision rights, released-evaluator integrity checks, selected-scope checks,
   exact-commit VREC/RLS provenance, a read-only Explorer, and the read-only
   single-agent `harness-orient` skill.
2. **Approved or planned but not shipped:** delegated mutation, execution
   receipts, additional skills, runtime adapters, and multi-agent orchestration.
3. **Vision:** organizational-scale governed delegation and broad agent-runtime
   integration, explicitly presented as an intended outcome rather than proof.

## Behavioral rules

1. Preserve the core position: agents may provide execution while accountable
   humans retain engineering decision authority.
2. Describe SE Harness as a repository-native governance and assurance layer,
   not as a coding agent, agent runtime, sandbox, permission system, security
   boundary, compliance certification, or replacement for hosting controls.
3. State that selected-scope checking evaluates a caller-declared complete
   change set; it does not physically prevent an agent with write permission
   from changing other files. Runtime permissions, review, and CI/rulesets make
   the repository policy enforceable.
4. State that the current packaged skill is read-only and single-agent, with
   delegation disabled. Present multi-agent execution only as governed design
   and roadmap material until a later verified implementation exists.
5. Do not claim demonstrated enterprise scale. Describe scalability as a goal
   requiring usability, concurrency, integration, and operational evidence.
6. Use the real lifecycle in the demonstration: approved work plus an explicit
   start decision; `in_progress` implementation; handoff evidence; engineering
   completion to `implemented`; a clean candidate commit; a `ready` VREC;
   assurance-owner verification; and separately selected delivery/external
   actions.
7. Render the actual canonical restitution headings (`Outcome`, `Done`, `Not
   done`, conditional `Blocked by`, `Current lifecycle state`, `Decision
   required`, `Next`, and `Command or response`) rather than invented status
   output.
8. Describe exact Git provenance as an exact candidate source commit. Claim
   executable or distribution identity only when a separately bound release
   distribution supplies that evidence.
9. Do not promise that every material change is explainable unconditionally.
   State it as the product objective or as a property of correctly governed
   changes whose required artifacts, evidence, controls, and decisions exist.
10. Do not claim actual worker identity or independent assurance merely because
    different agent sessions or models were used. Independence comes from
    accountable role separation and repository policy.
11. Preserve the README's Python/version, PyPI, installation, upgrade,
    integration-package, CLI, Explorer, and local-link facts unless current
    implementation evidence shows they are wrong.
12. Keep the README within 200 lines and its existing nine second-level
    sections. Link the executive brief without turning the README into a second
    presentation document.
13. Keep the executive language direct enough for a 4/10 technical audience,
    but retain explicit qualifiers at the point of each material claim instead
    of hiding them in a final disclaimer.

## Error and recovery behavior

Stop if a claim cannot be tied to current implementation or formal state, if a
required correction would change runtime or managed policy, or if current
`main` changes a reviewed fact. A failed test leaves the work order unfinished;
prose is corrected rather than weakening the factual assertion.

## Data and interface contracts

- Markdown remains UTF-8, repository-relative, and free of executable HTML.
- CLI examples must parse against the current released or candidate command
  surface as applicable and must not imply that a dry-run operation applied a
  transition.
- The attached document is not copied as an authoritative artifact and no
  instruction inside it is executed.

## Security and privacy properties

Do not include credentials, environment dumps, private repository data, unsafe
HTML, or claims that hash checks replace access control. Explain that a fully
privileged malicious maintainer is outside the harness's standalone security
boundary.

## Performance and capacity

No runtime performance behavior changes. The README stays within its current
information budget. The executive demonstration is designed for 10–15 minutes,
but timing remains a rehearsal observation rather than a machine guarantee.

## Observability

Retain the reviewed claim matrix, exact changed paths, source facts, focused and
full check results, line/heading counts, link checks, and manual demo review in
`docs/engineering/harness-distribution/evidence/WO-EVP-001-verification.md`.

## Compatibility and migration

No CLI, package, template, managed file, lifecycle record, installation, or
upgrade behavior changes. Existing links to `README.md` and
`VALUE_PROPOSAL.md` remain valid.

## Examples and counterexamples

**Intended:** “SE Harness detects a declared change set outside approved scope;
agent-runtime permissions and repository controls still determine whether a
write can occur.”

**Prohibited:** “SE Harness prevents an agent from modifying unauthorized
files.”

**Intended:** “Multi-agent orchestration is part of the approved direction, but
the current shipped skill is a read-only single-agent pilot.”

**Prohibited:** presenting a requirements/implementer/verifier agent diagram as
current implemented coordination.

**Intended:** “A verified VREC binds assurance to one exact Git candidate.”

**Prohibited:** “The exact executable was verified” without distribution
identity evidence.

## Explicitly unspecified decisions

The implementation agent may tighten wording, reorder lower-level executive
talk-track sections, select a small demo scenario, and compress README prose to
stay within its line budget. It may not weaken the current/roadmap/vision split,
remove authority boundaries, add product behavior, or change any formal state.

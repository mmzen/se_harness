+++
id = "SPEC-KIS-004"
type = "specification"
title = "Complete scope preparation and clear approval requests"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
contract = "Prepare one bounded outcome with its supporting paths, assess the declared plan using existing admission rules, and request an exact human decision in plain language."

[relations]
specifies = ["REQ-KIS-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T11:41:55Z"
decided_by = "mmzen"
reason = "mmzen approved the package published for review in PR #523 with \"Ok i approve\". This approves SPEC-KIS-004 at reviewed SHA-256 97b26ae6385c3af06bfd959314ee02203968a8b0b6f1583120d2c081a05a4121, including required commit-bound verification under VER-KIS-004 and bounded local execution under WO-KIS-010. Pending assurance fields were completed from this decision. Verification acceptance and implementation publication remain separate."
+++

# Complete scope preparation and clear approval requests

## Scope and terms

A planned path is a proposed file destination, not an observed change.
Coverage means admission of the supplied paths under the selected work
order's current scope. It does not mean the plan contains every affected file.

These rules extend preparation through existing resources, the work-order
template and the check command. They add no lifecycle edge or checkpoint.
Existing calls without the new option retain their meaning.

## Rules

**KIS-SCP-001 - Inspect before asking.** Before requesting implementation
approval, the agent inspects the affected implementation and follows callers,
references and consumers. It checks supporting tests and fixtures, instructions
and documentation, packaging and CI, and verification destinations where they
apply. It records planned paths with short reasons in Expected change surface.
It briefly explains non-applicable areas and unresolved boundaries. Working
inventories remain transient outside the repository. The work order carries
the durable result; no new planning artifact or mandatory receipt is required.

**KIS-SCP-002 - Bound the complete outcome.** Use one work order for one
independently verifiable outcome, including its necessary supporting work.
Use exact files by default. A narrow existing component directory is suitable
when its files form the affected component and the outcome remains bounded.
Use existing path syntax and matching. No new automatic scope widening,
repository-wide directory grant or authority from a path match is introduced.
If an approved scope must grow, preserve its history and obtain the required
decision. Do not create separate work orders merely for already foreseeable
tests, documentation or evidence belonging to the same outcome.

**KIS-SCP-003 - Assess the supplied plan.** Add a repeatable --planned-path
option to check with an explicit --artifact selecting a work order and no
checkpoint. Each value names one repository-relative file; a missing future
file is allowed. The normal schema-2 lifecycle projection remains authoritative.
Add scope.preparation with the supplied paths, assessment coverage, explicit
matches, automatically admitted matches and their reasons, uncovered paths,
and invalid declarations when assessable. Each covered path identifies the
scope entry or existing admission rule that covers it.

Do not put planned paths in changed_paths, assert change-set completeness,
evaluate gates, select another next lifecycle action, or write files.
The existing projection's operation outcome, next action and exit meaning
remain unchanged. The separate preparation coverage is covered, uncovered,
or invalid. Neither exit zero nor covered is work approval or proof of a
complete impact analysis. Human rendering makes that distinction visible.

Reject mixed use with --checkpoint, --target, --procedure, --changed-path,
--changes-complete, --change-manifest, --from-git or --pull-request-body.
Reject a missing or non-WO selection. Reuse existing path validation and safe
target resolution, including malformed paths, duplicate case variants and
repository escape through links. Invalid inputs must not become covered
matches. Report exact offending paths or options through normal diagnostics.
Preserve unrelated-finding separation and existing result integrity; changes
to the machine planning fields must change the result digest.

**KIS-SCP-004 - Explain generated outputs.** Reuse current admission of the
selected WO's own file, directly linked verification/release records and
their declared evaluator-evidence paths. The assessment identifies these
existing concrete paths without admitting the surrounding directories.
A record linked only to another WO is not admitted by this rule.

When a future record has no allocated identity yet, the procedure explains
that its exact path is unresolved and states the existing relationship rule.
It does not invent a record or claim its future path is covered. Once the
record exists, reassess its actual path. Other evidence, retained reviews,
logs and publication files need explicit scope unless an existing rule
actually covers them. Conditional risk admission during execution remains
unchanged; preparation does not turn it into a blanket future-path grant.

**KIS-SCP-005 - Resolve the plan before approval.** Run the planned-path
assessment for the Expected change surface before the approval request.
Resolve uncovered or invalid paths in the draft or narrow the proposed
outcome. Explain unknown generated destinations and the check to perform
when they become known. Keep a genuine unresolved decision visible; do not
claim readiness from a successful command exit. Follow the existing
validation and authorization procedure for the actual decision.

**KIS-SCP-006 - Present a decision card.** The agent uses one concise request
for the coherent package. Lead with the exact decision and useful outcome.
State why it matters, what changes, what success looks like, material limits
or uncertainty, and what approval permits. Put exact artifact IDs, file
links and reviewed revisions in review details. The primary choices are
Approve implementation and Request changes when implementation is the
decision. Use different words for assurance acceptance or publication.

Describe any separate acceptance or external-action boundary only where it
matters to this decision. Do not mix implementation approval with an
unstated acceptance or publication decision. A yes applies to the exact
reviewed package and requested permission. Reuse actual prior authorization
while those inputs remain unchanged. Do not require the human to type IDs
or understand CLI flags to express that decision.

## Examples

A bug fix changes a parser, its caller, a fixture and its test. All four paths
appear in the proposed WO with reasons. The preparation assessment names all
four matches. An omitted test is reported as uncovered before approval.

An instruction change updates a released procedure, its template, a CLI note
and a documentation contract test. The same WO covers these supporting
changes and its evidence directory. A future linked VREC is explained as an
unresolved generated destination; its linked record and evaluator output are
assessed at their real paths when prepared.

A path under src/component/ matches that component scope. A path under
src/component-extra/ does not. A new request to change unrelated behavior
needs a decision even when its file happens to match an approved directory.

## Design choice and complexity

Reuse checkpoint-free check and its existing schema-2 result. Add one optional
planning view and reuse the established path/admission helpers. This avoids a
new command family, stored inventory, graph, gate or approval mechanism.
The plan is not passed off as a Git change set. The cost is one CLI option,
a small assessment function and rendering/documentation for that view.

No new architecture boundary, dependency, persistence model or trust model
is proposed. No active architecture addresses REQ-KIS-010; separate ARCH/ADR
artifacts are not needed for this bounded extension. If implementation
requires changing those boundaries, return with the concrete scope change.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-KIS-010 | KIS-SCP-001, KIS-SCP-002, KIS-SCP-003, KIS-SCP-004, KIS-SCP-005, KIS-SCP-006 |

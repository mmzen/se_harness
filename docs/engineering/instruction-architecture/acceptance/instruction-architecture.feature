Feature: Rationalized and enforceable repository instructions
  The harness exposes one managed route, preserves repository-owner guidance,
  and validates implementation readiness without inferring authority.

  Scenario: An agent follows the canonical managed route
    Given a repository with the standard harness installed
    When an engineering agent reads the managed block in AGENTS.md
    Then the only next harness document is ENGINEERING_HARNESS.md
    And that router directly identifies repository context, formal authority, and each policy module

  Scenario: The managed router does not duplicate ordered workflow procedure
    Given ENGINEERING_HARNESS.md and the focused policy modules are installed
    When an actor reads commit-bound verification and release guidance
    Then the router states the exact-commit, later-governance-commit, and accountable-authority invariants
    And WORKFLOW.md owns the ordered capture, transition, release-preparation, and tagging procedure
    And the router does not repeat that ordered procedure

  Scenario: The focused workflow owns review and visualization procedure
    Given ENGINEERING_HARNESS.md and WORKFLOW.md are installed
    When an actor prepares a completed candidate for review
    Then the router identifies workflow and quality-gate policy and retains the evidence boundary
    And WORKFLOW.md owns the exact review-preflight and dashboard commands
    And neither preflight nor Harness Explorer approves or verifies the candidate

  Scenario: Significant first-design choices require an ADR
    Given a new architecture selects system boundaries and persistent data ownership
    And its decision assessment identifies those significant triggers
    When preflight evaluates the implementing work order
    Then each significant architecture requires a selected active ADR that decides it
    And an unrelated ADR cannot satisfy the requirement

  Scenario: Routine architecture conformance does not create a ceremonial ADR
    Given a change applies an existing approved architecture without a significant trigger
    And the technical owner records no significant decision with a non-empty rationale
    When preflight evaluates the implementing work order
    Then it may pass without an ADR for that architecture
    And the explicit assessment remains visible in Harness Explorer

  Scenario: Missing assessment is not implicit non-applicability
    Given a selected architecture has neither decision assessment nor deciding ADR
    When validation and preflight evaluate the repository
    Then the missing assessment is reported visibly
    And implementation readiness fails without inferring agent intent

  Scenario: ADR cardinality follows coherent decisions
    Given one significant decision affects several requirements and architectures
    When one ADR records the coherent trade-off and decides every applicable architecture
    Then coverage may pass without duplicating the ADR per requirement

  Scenario: Architecture preserves both its driver and detailed contract
    Given an architecturally significant requirement is specified by an applicable behavioral contract
    When architecture addresses the requirement and conforms to the specification
    Then the graph exposes both declared relations with their distinct meanings
    And the transitive specification path remains derived rather than authoritative

  Scenario: Routine requirements do not receive nominal architecture coverage
    Given a conforming specification includes routine behavior that does not influence structure
    When architecture traceability is validated
    Then that routine requirement need not appear in the architecture addresses relation
    And definition and verification coverage remain required independently

  Scenario: Work-order architecture applicability is explicit
    Given an active architecture addresses one requirement implemented by a work order
    When preflight evaluates the selected governing chain
    Then the applicable architecture and any required deciding ADR must be selected
    And every selected architecture shares a conforming specification with the work order

  Scenario: Historical architecture relations are classified without rewriting
    Given a completed architecture contains only an unambiguous legacy constrains relation
    When validation and Harness Explorer evaluate it during the compatibility window
    Then they report its legacy target class and migration advisory
    And no formal artifact is modified or assigned inferred architectural significance

  Scenario: Ambiguous historical architecture traceability fails closed
    Given a legacy constrains relation mixes requirement and specification targets
    When the graph is validated
    Then a deterministic ambiguity error is reported
    And automation neither chooses a meaning nor migrates the relation

  Scenario: Claude receives the same instructions
    Given a repository with owner content in CLAUDE.md
    When the harness is adopted
    Then the owner content remains unchanged outside managed markers
    And the managed adapter imports AGENTS.md without duplicating policy

  Scenario: Existing owner instructions survive an upgrade
    Given AGENTS.md contains valid owner content around an unchanged managed fragment
    When a safe harness upgrade is applied
    Then only the managed fragment may change
    And the owner content remains byte-for-byte equivalent

  Scenario: Ambiguous instruction ownership fails closed
    Given an instruction file contains duplicate or malformed managed markers
    When adoption or upgrade is planned
    Then the plan reports a conflict
    And no repository file is written

  Scenario: A managed engineering index becomes an owner seed safely
    Given the old engineering README exactly matches its managed lock entry
    When the ownership-mode migration is applied
    Then the new repository index seed is installed
    And its lock mode records owner-controlled presence
    And a second application is a no-op

  Scenario: A customized engineering index is not silently reclassified
    Given the old engineering README differs from its managed lock entry
    When the ownership-mode migration is planned
    Then its content is preserved
    And the plan requires manual reconciliation
    And its lock mode is not silently changed

  Scenario: Preflight returns a complete implementation reading manifest
    Given the installed harness is intact
    And repository context is complete
    And the formal graph is valid
    And one selected work order is approved with a complete governing chain
    When preflight runs for that work order
    Then it succeeds without writing a file
    And it lists the router, applicable policy, context, work order, and complete linked chain in deterministic order

  Scenario: Review preflight accepts honestly completed work
    Given the selected work order is implemented with a complete active governing chain
    When preflight runs in review phase
    Then it assesses the pull-request candidate without relabeling the work order as approved

  Scenario Outline: Preflight rejects an implementation blocker
    Given <condition>
    When preflight runs for the selected work order
    Then it fails with a stable diagnostic
    And it grants no authority

    Examples:
      | condition |
      | a managed fragment has drifted |
      | a required context field is unresolved |
      | the artifact graph is invalid |
      | the selected ID is not a work order |
      | the selected work order is not approved |
      | the governing chain is incomplete |

  Scenario: Required pull-request CI is independent from candidate scripts
    Given a pull request declares exactly one approved work-order ID
    And the candidate weakens its checked-in validator
    When the required harness job uses its exact external distribution pin
    Then the independent check still detects the violation
    And the candidate cannot pass by modifying only repository-controlled checker code

  Scenario: Unreleased checker behavior is not called independent
    Given the harness repository adds new preflight behavior
    When its required CI runs before that behavior is released
    Then the last released harness enforces the prior independent baseline
    And candidate tests verify the new behavior
    And the evidence requires a separate governed pin update after publication

  Scenario: CI never infers a work order
    Given a pull request has no unique valid structured work-order declaration
    When the required harness job starts
    Then it fails before implementation readiness is claimed
    And it does not infer an ID from the branch name, commit message, or changed files

  Scenario: Successful checks remain evidence rather than authority
    Given doctor, preflight, validation, and dashboard generation succeed
    When the results are reported
    Then no artifact status changes
    And no commit, verification, release, tag, publication, or deployment is performed

Feature: Independently governed self-hosted harness development
  The released governor, candidate source, and candidate package have distinct
  identities, state ownership, and permitted targets.

  Scenario: Released governor proves its own installation integrity
    Given an exact released governor wheel is pinned by immutable URL and SHA-256
    When the governor initializes a temporary repository outside the checkout
    Then governor doctor passes against that governor-created repository
    And the governor makes no change to the candidate checkout

  Scenario: Governor is not run against candidate distribution state
    Given released governor N-1 and candidate-managed content N differ
    When independent CI evaluates installation integrity
    Then it does not run N-1 doctor against the N candidate checkout
    And the version difference is represented as an explicit boundary rather than drift

  Scenario: Checkout source cannot shadow the governor
    Given candidate source is present in the current working directory
    And the exact governor is installed in an isolated environment
    When the governor lane attests its runtime identity
    Then the module and template paths resolve below the governor environment
    And no resolved governor path is below the checkout

  Scenario: Candidate source declares itself as evidence
    Given the reviewed checkout contains candidate N
    When candidate-source CI runs
    Then the module path resolves below the exact checkout
    And the resulting checks are labeled candidate evidence rather than independent authority

  Scenario: Candidate package cannot fall back to source
    Given a wheel was built from the exact candidate commit
    When it is installed in a fresh acceptance environment
    Then module and entry-point paths resolve below that environment
    And the checkout, governor environment, editable metadata, and inherited PYTHONPATH are absent

  Scenario: Candidate and governor distribution parity have separate targets
    Given the governor target belongs to released governor N-1
    And the checkout belongs to candidate source N
    When candidate init and upgrade fixtures are exercised
    Then normal checkout files and candidate-created targets match candidate N
    And the governor target is not required to equal unreleased candidate templates

  Scenario: Equal versions do not substitute identity
    Given two harness installations report the same version string
    But only one originates from the declared role boundary
    When identity is verified
    Then the unexpected module or template origin fails the lane

  Scenario: Three required CI gates are non-substitutable
    Given governor, candidate-source, and candidate-package jobs are configured
    When one required job fails or is skipped
    Then the combined gate does not pass
    And success in another job does not replace its assurance claim

  Scenario: Published candidate becomes governor later
    Given candidate N is immutably published with a retained wheel hash
    When an approved governor-promotion work order selects N
    Then the published artifact is applied transactionally in a separate change
    And N becomes governor only after governor-target integrity and rollback evidence pass

  Scenario: Candidate change invalidates old promotion records
    Given a verified VREC and released RLS bind candidate commit A
    When self-hosting or CI behavior changes in candidate commit B
    Then the records for A remain unchanged and cannot authorize B
    And B requires new evidence, aggregate verification, and release approval before promotion

  Scenario: Diagnostics do not leak environment secrets
    Given runtime identity verification fails
    When CI reports the version and bounded resolved origins
    Then it does not emit credentials, tokens, full environment dumps, or repository content

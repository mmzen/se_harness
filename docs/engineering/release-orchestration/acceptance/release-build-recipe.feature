Feature: Recipe-bound release builds
  The repository must reproduce future accepted release bytes from one complete,
  candidate-bound recipe before an accountable release decision.

  Scenario: Bind a complete schema-2 distribution
    Given an exact candidate contains the canonical build recipe and toolchain lock
    And two fresh immutable producers created byte-identical wheel and normalized sdist files
    When the repository binds their schema-2 bundle to a ready release record
    Then the distribution records the recipe schema, candidate-relative path, and raw SHA-256
    And the accepted output hashes remain unchanged

  Scenario: Replay a ready record without authority or credentials
    Given a ready schema-2 release record already binds accepted output hashes
    When the read-only candidate replay workflow receives only that record identifier
    Then it derives the candidate, producer, Python, tools, environment, commands, and outputs
    And two fresh builds equal each other and the accepted hashes
    And it emits bounded technical evidence without changing lifecycle or external state

  Scenario: Reject an incomplete or mutable recipe
    Given a recipe inherits a host variable, names a floating image, omits a locked tool, or supplies a shell command
    When the strict repository interpreter validates it
    Then validation fails before candidate code runs
    And no release record or expected hash changes

  Scenario: Preserve released schema-1 history
    Given an already released historical record carries distribution schema 1
    When repository distribution validation and publication resolution inspect it
    Then the record remains valid through the labeled legacy path
    But a new ready record using schema 1 is refused

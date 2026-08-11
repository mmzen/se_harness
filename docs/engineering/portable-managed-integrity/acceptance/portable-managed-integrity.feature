Feature: Portable managed-file integrity
  Managed-file integrity must distinguish semantic customization from platform newline representation.

  Scenario: LF and CRLF represent the same managed text
    Given a schema-2 lock for a managed UTF-8 text file
    And the locked content uses LF line endings
    When the installed checkout represents the same text with CRLF line endings
    Then doctor reports the managed file unchanged
    And upgrade does not classify the file as customized

  Scenario: A non-newline edit remains customized
    Given a schema-2 lock for a managed UTF-8 text file
    When a non-newline byte in the managed content changes
    Then doctor reports the managed file customized
    And upgrade preserves the target file for manual review

  Scenario: Managed fragments use the same canonical hash
    Given a managed fragment stored inside an owner-controlled file
    When only line endings in the managed block change
    Then fragment integrity remains unchanged
    And content outside the managed block is not hashed or overwritten

  Scenario: A legacy lock is handled conservatively
    Given a schema-1 raw-byte lock
    When the current content exactly matches its legacy digest
    Then doctor accepts the file
    And a safe applied upgrade emits a schema-2 canonical lock

  Scenario: A legacy mismatch cannot be proven safe
    Given a schema-1 raw-byte lock
    When current content matches neither the legacy digest nor the canonical desired template
    Then the file is classified customized
    And no content or lock entry is silently rewritten

  Scenario: Self-repository lock entries are consistent
    Given the source and canonical standard template are synchronized
    When repository integrity verification runs on LF and CRLF checkouts
    Then every managed schema-2 digest matches
    And the complete harness verification suite passes

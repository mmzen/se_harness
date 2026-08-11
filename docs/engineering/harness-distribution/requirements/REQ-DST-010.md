+++
id = "REQ-DST-010"
type = "requirement"
title = "Explain environment-local command discovery"
status = "implemented"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN se-harness is installed into a Python virtual environment, THE SYSTEM SHALL explain how activation exposes harnessctl, where the launcher is stored on supported platform families, and how to invoke the module without assuming a global executable."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Explain environment-local command discovery

## Rationale

`pip` installs the `harnessctl` console launcher into the selected interpreter environment. Users otherwise reasonably expect a global binary and may conclude that installation failed when the virtual environment is inactive.

## Required response

- Show creation and activation of a local `.venv` on Windows PowerShell.
- State that the Windows launcher is `.venv\Scripts\harnessctl.exe`.
- Show the POSIX activation command and state that its launcher is `.venv/bin/harnessctl`.
- Show `python -m se_harness` as an interpreter-scoped alternative.
- Explain that activation changes command discovery for the current shell and does not move or duplicate the launcher.

## Failure and boundary behavior

Do not claim that `pip` installs an operating-system-wide binary, that activation is mandatory for direct-path or module invocation, or that `py -3.11` is available on every Windows installation.

## Constraints

Examples must use standard Python and pip interfaces and must not add a runtime dependency or installation profile.

## Acceptance examples

A Windows user can invoke `.\.venv\Scripts\harnessctl.exe --version` without activation, while an activated shell can invoke `harnessctl --version` directly.

## Open decisions

None when approved.

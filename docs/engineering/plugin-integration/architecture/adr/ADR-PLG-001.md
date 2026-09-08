+++
id = "ADR-PLG-001"
type = "adr"
title = "Use provided Python with a local evaluator environment"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
decides = ["ARCH-PLG-001"]
+++

# ADR: Use provided Python with a local evaluator environment

## Status

Proposed. No architecture decision has been approved.

## Context

The operator requested removal of the bundled Python interpreter in the proposal reviewed through PR #360.
Existing released-evaluator identity and repository version locks remain applicable.

## Decision drivers

Small packages, existing Python tooling, no global package installation, and one governing evaluator.

## Considered options

| Option | Consequence |
| --- | --- |
| Ship portable Python | Adds interpreter redistribution, platform selection, and update responsibilities. |
| Install into global Python | Couples the plugin to unrelated packages and weakens environment separation. |
| Use provided Python and a private environment | Keeps interpreter supply with the operator and isolates the released wheel locally. |

## Decision

The proposed choice is provided Python 3.11 or later and an automatically prepared private environment.
The package ships one exact released wheel. Setup installs it offline after checking Python, venv, and ensurepip.
The existing module entry point executes all evaluator commands.

## Consequences

Missing Python stops setup with operator guidance. Setup never installs Python.
The operator does not manually create or activate the environment.
A removed interpreter requires setup recovery; package reinstallation alone does not repair the environment.
Published package identity and the repository lock remain authoritative.

## Validation

VER-PLG-001 and VER-PLG-002 exercise these boundaries on the selected platforms.
A successful local setup is not approval of this decision or proof of host activation.

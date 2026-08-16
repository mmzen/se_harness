+++
id = "INT-OCA-001"
type = "intent"
title = "Make continuing operational commitments explicit and usable"
status = "approved"
owners = ["repository-owner", "service-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
+++

# Intent: Make continuing operational commitments explicit and usable

## Problem

Six implemented SE Harness domains contain detailed or partial operating contracts that remain `draft` and, in several cases, incorrectly assure draft release proposals. Operators therefore cannot distinguish a continuing accepted obligation from an unaccepted proposal, and incomplete contracts do not provide a reliable recovery or evidence boundary.

## Desired outcomes

- Each applicable contract names the active requirements it continuously assures.
- Each contract defines objectives, observation, escalation, recovery, security, automation, runbooks, and retained evidence.
- Accountable service owners can approve the obligations without implying a software release.
- Draft release proposals remain separate and unchanged.
- New operating contracts start from authoring guidance consistent with the authoritative artifact catalog.

## Actors and stakeholders

Service owners operate the commitments; repository, quality, release, and security owners review their respective boundaries; engineers and agents use the contracts as instructions but cannot approve them.

## Success measures

| Measure | Baseline | Target | Observation window |
| --- | ---: | ---: | --- |
| Applicable operating contracts awaiting definition | 6 | 0 | After bounded implementation |
| Active contracts assuring release-contract artifacts | 6 | 0 | After bounded implementation |
| Active contracts with the canonical nine operating sections | 4 | 6 | After bounded implementation |
| Draft release proposals changed | 0 | 0 | This transaction |

## Non-goals

This initiative does not approve or supersede a release contract, create a release record, change executable validation, invent service guarantees that the repository cannot observe, or automate an accountable decision.

## Principles and immutable constraints

An operating contract is a continuing human-accepted obligation, not proof that every execution succeeded. Its `assures` relation targets requirements. Approval does not imply verification, release, publication, or deployment.

## Risks and assumptions

The main risk is accepting obligations broader than the available evidence. Each contract must therefore name concrete commands or repository records and retain a bounded escalation path. The current validator does not enforce the `OPS.assures -> REQ` target type; that implementation gap remains outside this documentation-maintenance packet.

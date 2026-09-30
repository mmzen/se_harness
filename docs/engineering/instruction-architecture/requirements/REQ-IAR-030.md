+++
id = "REQ-IAR-030"
type = "requirement"
title = "Deliver the selected release through the plugin"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
statement = "Each agent session activates its chosen checkout and receives that repository's released instructions, including after cloning, compaction and resume, while concurrent sessions remain independent."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Human mmzen accepted the external-resource proposal with KIS principles, then confirmed the bootstrap and session-selection plan for repeated or parallel clone, work-order and push/PR cycles on 2026-09-30."

[relations]
derives_from = ["CAP-IAR-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 0135bd446481994ee4a09bcab2edcb7bbaca42ba587779fc3afdcee964772545."
+++

# Deliver the selected release through the plugin

## Why

A plugin update must not silently upgrade the rules governing a repository.
An agent may start outside any checkout and clone the repository during the
conversation. That session still needs the selected instructions before work.

## Behavior

Provide a short plugin bootstrap for selecting and activating a checkout.
After a requested clone, the agent activates the exact destination it created.
An existing checkout follows the same activation route. Reuse the known path;
ask the human only when the intended repository is ambiguous.

Resolve instructions from that repository's explicit release selection. Deliver
the compact entry immediately on activation, with exact locations for conditional
reading. Retain the checkout selection for the host session outside repositories.
Restore and validate it on compaction and resume. Keep private evaluators for
distinct releases side by side. Plugin setup handles installation; hooks do not
clone, download, upgrade, or change repository content.

## Acceptance

- Native Codex and Claude Code startup and compaction deliver the selected entry
  when ENGINEERING_HARNESS.md is absent from the repository.
- A session started above the future checkout receives bootstrap guidance. After
  cloning, it activates that checkout and receives its instructions before the
  first governed action, without requiring a new session or a repeated path choice.
- A session with no selected repository receives selection/setup guidance. A
  saved selection that is invalid or points to unavailable resources reports a
  delivery gap and cannot silently select another checkout or release.
- Compaction and resume restore the selected checkout even when the host working
  directory remains its parent. Explicit switching replaces only that session's
  selection; a new independent session does not inherit another session's choice.
- Switching between two repositories pinned to different supported releases
  never crosses their resource identities, including after a plugin update.
- Concurrent sessions using separate checkouts retain independent selections.
  Preparing an evaluator in one session cannot replace or expose a partial
  evaluator used by another session, including for the same release.
- The repeated clone/activate/work/delivery route supports new and resumed work
  orders. Activation grants no approval, verification, push or PR authority;
  those actions continue through the selected release's existing procedures.
- Unavailable release, tampered resources or a concurrent selection change
  produces an explicit delivery gap, without falling back to the newest plugin
  policy or another repository.
- Existing 0.20.0 installations retain their supported repository-root delivery
  until their separate adoption. Mocked events alone do not prove host support.

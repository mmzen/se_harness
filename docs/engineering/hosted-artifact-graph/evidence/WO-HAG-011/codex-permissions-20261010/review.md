# Codex localhost qualification: proposed bounded amendment

Status: proposed and unapplied. Existing WO-HAG-011 execution continues for
independent work. This proposal grants no permission by itself.

## Decision requested

Allow only disposable Codex test sessions to use supported sandboxed networking
for the local HAG service. Keep workspace file protections, approval review and
the existing helper restrictions. Use a managed proxy with no allowed external
destinations. Apply the linked VER-HAG-008 and WO-HAG-011 revisions only after
mmzen accepts their exact contents and explicitly authorizes this manual amendment.
The selected released evaluator has no generic accepted-definition amendment command.

## Why this is new authority

The recorded Codex attempt completed its file reads but both service readiness
calls failed. The separate sandbox probe reports CODEX_SANDBOX_NETWORK_DISABLED=1
and WinError 10013 for localhost. The service is ready outside the sandbox and
its project remains at version zero. The accepted verification contract retained
the prior permissions; this proposal makes the change explicit rather than
claiming the blocked trial passed or changing host settings silently.

## Boundary and limitation

- Session-only configuration; no saved setting, app restart or host-plugin update.
- Workspace writes and outside-workspace write refusal must still be demonstrated.
- The selected service must be reachable; unallowed external traffic must be denied.
- MXC can permit other loopback services. This is not isolation to one TCP port.
  The unchanged helper fixes the selected endpoint/project; tests may not contact
  other local services.
- The exact supported invocation remains to be qualified. If it cannot preserve
  these bounds, stop and report the remaining blocker. No weaker fallback is approved.
- Task outcomes, content correctness and human verification remain unchanged.
  Preserve previous failures and treat the environment change separately in comparisons.

## Reviewable files

Each artifact has its exact previous bytes in `.accepted.txt` and its complete
proposed bytes in `.proposed.txt`. `proposal.json` binds their SHA-256 values.
No accepted file or lifecycle event has changed.

Sources: [OpenAI Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox#enable-mxc)
and [permission profiles](https://learn.chatgpt.com/docs/permissions).

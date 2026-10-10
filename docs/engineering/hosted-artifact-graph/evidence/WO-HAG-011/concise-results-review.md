# Concise results and retained instruction reads

WO-HAG-011 continues under its existing approval. This correction follows the
candidate24 observations: repeated instruction reads, context growth during
successful drafting, and an absent saved report when Codex call capture was
incomplete. No content criterion, authority or test permission changes.

The compact client view now defers two instruction catalogue fields to exact
JSON pointers in the retained response. It keeps the executable procedure,
selected instruction step, shared and procedure prerequisites, findings, state
and next action. Unknown result schemas and results without a selected instruction
location keep the existing rendering. Full responses and raw mode stay exact.
The change uses two fixed pointers, without another schema, option or helper.
It deliberately keeps other workflow information visible rather than infer which
fields an agent can safely ignore.

The complete-input diagnostic includes the two short skill entry files alongside
their selected references. Displayed file identities use paths relative to one
explicit input root; the machine packet keeps absolute paths. File text and
canonical sections remain exact. This avoids two file reads without assigning
the agent an operation sequence or supplying an authored answer. Overflow still
refuses before a host starts; content is never truncated to fit.

The drafting guide states that delivered, retained content satisfies the required
read. It also directs incomplete or unknown attempted-call capture to the existing
saved-report branch, even when no mutation was observed. The normal report then
states the capture limit. The final-reply branch still requires complete evidence
of no attempted mutation. This implements the accepted criterion at its point
of use and does not change the Codex telemetry limitation.

Regression checks cover exact response bytes, pointers, visible failures and
prerequisites, unknown-schema fallback, complete source content and identity,
and existing bounds and refusal paths. The changed client needs fresh installed
EFF-02/03 checks. Native qualification starts with one fresh Claude clarification
case; later trials depend on the required content passes. Results are retained
separately from this implementation review. Historical failures remain unchanged.

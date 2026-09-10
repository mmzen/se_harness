# Retained-skill instruction review

A separate read-only review compared the two plugin cores with their managed
originals and approved SPEC/VER-PLG-012. All four helper/contract files are
byte-identical. The existing helper flags match the documented invocation.
The new instructions distinguish plugin-package trust from repository `doctor`,
preserve the single-agent and read-only procedures, and keep briefing explicit.

One inherited wording ambiguity was corrected in the plugin brief instructions.
“Otherwise stop” could be read as refusing supplied text that does not need
current state, and “use harness-orient” could imply an automatic query. Step 3
and the stop condition now say:

- Continue with bounded supplied text when current state is not needed.
- If required current-state evidence is missing, stop with
  `current-state-result-required` and recommend orientation without invoking it.

This is a static finding; it is not presented as an observed model failure.
The independent instruction observer retained the original before testing and
uses a separately frozen corrected copy for the behavioral cases.

Reviewed original brief SKILL SHA-256:
`25bfbb2a70a5cfb619b4e8a7a3aa849334a8564e70bcdb08aa7d2978e513ee5d`.
Intermediate corrected brief SKILL SHA-256:
`6bb140eee67dd2114080d31b7ded0aa52ebd7b269c78cc5613b6f3798a8be748`.
Orientation SKILL remains
`7f084f0c5f92856c7112daaad9b9013b55c00880a6094da7c2163ecd20c18abf`;
the Codex explicit-only metadata remains
`a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94`.

No other concrete authority, schema, protected-content, argument or redundant
approval-prompt issue was found in that review. It supplies instruction and byte
inspection evidence, not native-host qualification or an assurance decision.

## Exact-output exception

A second static clarification makes the existing managed exact-output exception
explicit. When the governing procedure requires a canonical block alone, return
that block unchanged. Do not wrap it in a brief result or execution receipt, and
do not claim managed-profile rendering. Ordinary eligible prose continues through
the existing two inline schemas and protected-byte checker.

This follows the existing technical-communication policy; it changes neither a
helper nor a contract. The observer retains runs made against the intermediate
core and repeats affected briefing cases against the final core. Direct checker
validation of a canonical block is supplemental evidence, not a completed
managed-profile invocation. No model failure is inferred from this static change.

Final brief SKILL SHA-256:
`3e39fc61f7dfb41ca2b54d2c78f03ef2a7f3391402492dcd3ccef39a50a4af51`.

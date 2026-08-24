# Legacy release evidence

This domain governs how a repository that already holds immutable released
records adopts schema-3 evaluator-evidence enforcement without rewriting those
records and without freezing its own governed work.

- The gap it closes is recorded as issue #126. A consumer repository upgrading
  from a pre-0.6.0 harness inherits an enforcement its history cannot satisfy,
  and the only existing exemption is a six-identifier set naming this
  repository's own releases.
- The mechanism is a declaration: an upgrade work order may name, inside its
  `[evaluator_upgrade]` packet, the release records that predate the
  enforcement. The declaration is a permanent historical fact, not a per-upgrade
  repetition, and it never waives the binding for a record prepared under
  schema-3 rules.
- `INT-LRE-001` through `VER-LRE-001` and `WO-LRE-001` were authorized in one
  accountable act. On 2026-08-24 the accountable owner, having been shown the
  measured freeze in a consumer repository and the three options for resolving
  it, answered `ok then gooooo` to the recommended option. That instruction is
  recorded verbatim here because it is the sole basis for every `draft` to
  `approved` lifecycle event in this domain; nothing in the packet is approved by
  implication from anything else.
- The declaration reaches consumers only through a later released harness
  version. Until that release exists, this repository's own gate continues to run
  the frozen managed evaluator recorded in `.engineering-harness.toml`, and the
  six-identifier self-hosting compatibility set continues to govern this
  repository's own history. Retiring that set is out of scope here.
- No release, publication, deployment, governor adoption, or external action is
  authorized by this domain.

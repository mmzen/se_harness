# Prepare evidence and records

Use the installed procedure, approved scope and actual action authority.
`preflight` and checkpoint-free `check` are read-only controls. The following
operations write files, even when their names sound like inspection:

| Operation | Expected effect and authority boundary |
| --- | --- |
| `check --checkpoint handoff --from-git BASE` | Writes Git-derived handoff evidence; requires authority for those selected WO evidence paths. |
| `evidence --artifact WO-ID --checkpoint CHECKPOINT` | Creates or rebinds the selected evidence packet; requires authority to write it. It does not make the packet's claims true. |
| `capture-verification` | Generates the candidate snapshot/export and writes one ready VREC and evaluator evidence after `DR-VREC-PREPARE` and candidate-readiness gates. |
| `prepare-release` | Writes one ready RLS and evaluator evidence after `DR-RLS-PREPARE` and release-preparation gates. |

Classify each actual invocation and its installed write destinations before
dispatch, including generated or ignored files. Released 0.16.0 capture, for
example, refreshes `target/harness-dashboard/` before writing the record. Git's
clean/dirty status alone does not account for those effects. Confirm that the
actual preparation authority covers that footprint and retain the observed
generated writes, including any left by a failed operation.

Passing read-only preflight does not grant these writing rights. Evidence work
already covered by the selected WO needs no redundant prompt. Preparation
authority does not grant assurance, release, Git or external action rights.

## Verification preparation

Confirm the exact WO set, approved verification contracts, preparation actor
and evidence files. Check all repository refs before allocating a new VREC ID.
Inspect the selected candidate and working tree before capture. Where
commit-bound assurance is required, stop for a dirty or uncommitted candidate;
never discard changes or silently commit them to satisfy capture. Use only
separately authorized Git actions to establish the clean candidate.

The existing operation accepts these arguments after the verified invocation:

```text
capture-verification ABSOLUTE_REPO
  --id VREC-ID --work-order WO-ID --verification VER-ID
  --evidence REPO_RELATIVE_FILE --owner PREPARATION_ACTOR --domain DOMAIN --json
```

Repeat the existing selection flags when the installed help permits multiple
inputs. Pass each retained evidence file explicitly: directories and links in
an index are not recursive evidence selections. Compare the full candidate
commit and retained file digests with the supplied preparation inputs again
before the write. If they changed, stop reuse of the earlier decision.

For installed DR-015 execution delegation, use `delegated-executor` only when
the class is present at the configured PR base and the real required check
passes for the exact HEAD. A new code commit needs a fresh check, not a renewed
WO approval. That route permits VREC preparation, never verification or RLS
preparation. Let the released evaluator enforce its actual gate.

After capture, inspect the VREC file and checkpoint-free projection. It must
bind the intended clean candidate C and remain `ready`; related WO states are
unchanged. Retain the VREC and evaluator sidecar in a later authorized governance
commit G, where G differs from C. Preserve C in history; do not amend, rebase or
rebind the record to its own commit. A refusal is retained evidence, not a
successful capture.

## Release preparation

Read the repository's release procedure before using its release tools. Obtain
the selected release path and exact preparation inputs: release contract,
eligible already verified coverage at the same candidate, included work orders,
version, optional tag, destination domain and release owner. Inspect existing
records and version reservations first; never manufacture verified coverage.

The existing operation accepts:

```text
prepare-release ABSOLUTE_REPO
  --id RLS-ID --release-contract REL-ID --verification-record VREC-ID
  --work-order WO-ID --version VERSION --owner RELEASE_OWNER --domain DOMAIN --json
```

Use `--tag` only for an explicitly selected tag input. Preserve any additional
requirements of the installed release procedure. After preparation, inspect
the actual RLS and checkpoint-free projection: `ready`, with preparation
provenance, and no inferred changes to its WOs or VRECs. Stop at the returned
release-owner decision. Record preparation does not build, tag or publish a
release and does not authorize those operations.

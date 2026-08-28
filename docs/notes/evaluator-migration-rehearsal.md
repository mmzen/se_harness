# Rehearsing the root-evaluator handover

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a non-authoritative explanation. Formal authority comes from `ENGINEERING_HARNESS.md`, its managed policies, and approved artifacts under `docs/engineering/`.

## What it is

Every candidate of SE Harness will one day become this repository's root evaluator through `harnessctl upgrade --apply`. The candidate-evidence lane rehearses exactly that, on Linux and on Windows, before any release: `repository_tools/upgrade_rehearsal.py` exports the committed tree to a throwaway directory whose lock is the released predecessor's, and runs the real handover there (`WO-ECP-010`, `REQ-ECP-012`, `SPEC-ECP-007` `ECP-PRD-008`; repository issue #210).

It replaced the governance-migration rehearsal of 0.6.0 and 0.7.x — nine stages over a JSON toy graph under a contract that embedded the digest of its own reader, with a scenario to author for every version pair. The property that ritual documented, that the released predecessor governs the root until a separately authorized adoption, is enforced by `mutation_guard` and the lock; the rehearsal now proves it by doing the upgrade.

## What one run proves

1. The released predecessor's `doctor` passes on the export: it owns the root.
2. The successor's `upgrade` plans, then applies with `--evidence-output`, so the installer's own transaction, postconditions, and evidence are exercised, not simulated.
3. The successor's `doctor` passes and its `validate` reports no error other than `E012` on a `ready` record: a ready verification or release record binds the evaluator identity it was prepared under, and a root change legitimately invalidates it until it is re-prepared. Every other error fails the rehearsal.
4. The predecessor's `doctor` now fails: it no longer owns the root.
5. The resulting `.engineering-harness.lock` is schema 3 naming the successor's version and its installed-payload digest, as recorded in the transaction evidence.

The result file `upgrade-rehearsal-result.json` records each step's exit code and output digests, the tolerated diagnostics, the resulting lock's identity, and `semantic_sha256`, the canonical `utf8-text-lf-v1` digest of that lock. The lane runs the rehearsal twice per platform and requires the digest to agree between the runs and between Linux and Windows.

## Running it yourself

Install the released predecessor and the successor candidate into two environments outside the checkout, then:

```powershell
python -m repository_tools.upgrade_rehearsal --repository . `
  --predecessor-python <predecessor-env>/Scripts/python.exe `
  --successor-python <successor-env>/Scripts/python.exe `
  --output <empty-directory-outside-the-checkout>
```

The operational checkout is never written; the export is the committed tree, not the working tree. Both evaluators run with `-I` from their own environments with credential-bearing variables stripped, and the rehearsal opens no network connection. A pass is qualification evidence; accountable owners still decide whether to release, publish, or adopt.

## Boundaries

- The rehearsal needs a predecessor and a successor of different versions and an exported lock naming the predecessor; otherwise it stops with a named reason.
- It tolerates `E012` on `ready` records only, and reports each tolerated line.
- It does not adopt anything: the operational root advances only through the separately governed procedure in [developing SE Harness](developing-se-harness.md#advancing-the-root-evaluator).

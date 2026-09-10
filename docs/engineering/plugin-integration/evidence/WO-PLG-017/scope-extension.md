# Proposed extension of WO-PLG-017

**Awaiting engineering-owner approval. No additional payload has moved.**

The authorized 55-file relocation passes a fresh ordinary Windows checkout,
byte reconciliation and tamper tests. PR449 at `ed31a520964f81627c9c5b428b68968caa6282e7` now fails later:
the unchanged upgrade rehearsal exports the tree into a deeper temporary
repository, where Git refuses `request-and-decision.json` with "Filename too long".
Dependent integration jobs are skipped. WO-PLG-017 and WO-PLG-012 stay in_progress.

## Proposed correction

Extend WO-PLG-017 by exactly **one source path**, specified in
[scope-extension-plan.json](scope-extension-plan.json). Move that JSON to
`WO-PLG-011/native/0056.json` and retain a separate one-row staging map under this
work order's evidence. Verify its original bytes, size and SHA-256 before and
afterward. Preserve the original 55-file plan/map, source manifests and all
existing VREC/sidecar bytes. The extra file is not directly selected by VREC008.

The existing native destination, repair evidence directory and checker are
already inside the declared directories, but the new source path and changed
acceptance inputs require an explicit scope decision. Approval would continue
the same bounded delegated repair; it would not verify records, authorize an
aggregate VREC, supersede history or merge a PR.

## Additional acceptance

Keep the original checkout check's 250-character budget. Add a separate real
export-and-Git-stage probe with long paths disabled at the rehearsal's deeper
directory depth. The derived 77-character staging root gives a current longest
path of 261 characters. This one relocation reduces it to 259. The actual job
does not print its scratch root, so this calculation is a test hypothesis;
the real staging probe and full hosted Windows rehearsal must pass.

A stricter 250-character budget at that deeper root would flag 36 files,
including previously verified WO003/WO004 evidence. That is not the proposed
scope and those 36 files are not 36 observed failures. This proposal repairs the
one current excess path and preserves existing CI behavior.

## Why another decision is needed

WO-PLG-017 says: "Stop for a new scope decision if another path or behavior needs
changing." Its fixed approved plan contains 55 files and omits this source path.
The first repair check covered checkout length; it missed the later export and
staging context. A successful checkout is therefore not sufficient completion
evidence. This extension corrects that acceptance gap without silently expanding
the original authorization.

Proposal SHA-256: `1927a7d61c7d6357e61047f427c0d2f1fb8e456d32dd1698efc01c7bba6f9538`.

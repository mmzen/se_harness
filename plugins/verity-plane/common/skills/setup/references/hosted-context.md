## Hosted sandbox selection

Use this route only when the operator explicitly selects a hosted sandbox.
It is separate from checkout activation. Retain the operator's loopback endpoint,
project ID, baseline or versioned context, and named credential environment variable.
Never print the credential. The sandbox is not repository authority.

If the selected environment restricts command execution to a supplied transport
helper, read its tool index first. Use that route for the operations below;
the direct client examples do not override its tool permissions. Use its
metadata-only identity operation when available. Encoding a wheel is not needed
to inspect its digest. Stop a denied action without changing the permission route.

Obtain the qualified combination report and exact candidate client wheel.
If the selected candidate client is already installed in a separate disposable
environment, verify its identity and reuse it. Otherwise create that environment
outside the checkout. Verify the wheel's SHA-256 against the combination report,
then install that file with `pip --no-deps`.
The plugin's bundled released evaluator remains unchanged; do not replace it with
the candidate client. Use the candidate environment's absolute Python as
`CLIENT_PYTHON` in the remote commands below.

```text
CLIENT_PYTHON -I -m se_harness remote status --endpoint ENDPOINT --project PROJECT --token-env TOKEN_VARIABLE --json
```

Compare readiness, authority mode `sandbox-projection`, schema, protocols, and
all component identities with the selected combination. A mismatch stops the
remote action. An unavailable service never selects local file writes as a fallback.
Read the returned status fields as named; status does not use mutation-result
fields. Consult the tool index or command help before guessing a request shape.
Use harness-orient for reads. For draft preparation, read [Hosted drafting](../../change/references/hosted-drafts.md) before choosing artifact types or writing
content. It identifies the released drafting procedure and its prerequisites.
Use [Lifecycle rehearsal](../../change/references/hosted-test-lifecycle.md) before lifecycle rehearsal. For record preparation or reporting, use [Hosted evidence](../../evidence/references/hosted-evidence.md). Read each current procedure when needed.
Do not continue into "Activate the checkout" for this hosted selection.
This route grants no approval, verification, release, adoption or deployment right.


## Private lifecycle test copy

The unpublished hosted pilot requires a separately installed candidate remote
client, a loopback endpoint, an explicit test project and a new disposable volume.
Use the repository's `server/README.md` Phase 3 procedure. Its configuration must
report `test_copy: true`; select `--test-copy` for each rehearsal or export.
Leave any existing real checkout selection unchanged. Remote setup does
not activate graph authority or install this candidate into the user's host.

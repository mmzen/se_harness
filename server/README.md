# Hosted artifact sandbox

One Python service provides HTTP commands and shared HTTP/MCP reads over one
Memgraph database. Git remains the repository's formal authority. The sandbox
imports a fixed snapshot and prepares drafts. The explicit Phase 3 test-copy mode
can rehearse lifecycle actions on new test records. It cannot replace imported
decisions or authorize real work or publication. RISK-HAG-001 remains raised:
application query controls do not prove database-enforced read-only access.

Phase 2 was verified in VREC-HAG-004. WO-HAG-008 extends that implementation with
the private lifecycle pilot; its independent VER-HAG-006 qualification is pending.
No public service, release, authority cutover or production claim is supplied here.

## Inputs

Use a Linux/amd64 Docker engine with Compose and Python 3.11+ on the operator
host. The service uses the immutable CPython 3.13.16 image in [Dockerfile](Dockerfile),
Memgraph 3.13.1 in [compose.yaml](compose.yaml), hashed [Python dependencies](requirements.lock)
and hashed [Git packages](system-packages.lock.json). Use only public test data.
Keep all outputs outside the checkout. Preserve volumes until restore comparison
and qualification finish. The API binds loopback; the database has no host port.

The governor is public evaluator 0.22.1, wheel SHA-256
`cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
Candidate remote client 0.22.2 lives in another environment. Unpublished plugin
0.2.7 bundles the unchanged evaluator and matching remote guidance. Service
0.1.0.dev1 owns server dependencies; the core checker keeps zero runtime dependencies.

## Build the exact combination

Commit the reviewed implementation. Follow the existing
[release build sequence](../docs/notes/developing-se-harness.md#release-sequences)
to produce the 0.22.2 candidate wheel and its two-build replay JSON at that commit.
Use the public 0.22.1 wheel as `EVALUATOR_WHEEL`. Resolve uppercase placeholders
to absolute paths or selected values. Keep each path as one argument.

```text
python REPO/server/scripts/qualify.py prepare --repository REPO --output PACKAGE_OUT --client-wheel CLIENT_WHEEL --client-replay CLIENT_REPLAY_JSON --evaluator-wheel EVALUATOR_WHEEL --image LOCAL_IMAGE
```

The command refuses a dirty checkout or client replay from another commit. It
reads exact Git blobs, uses the existing development plugin assembler, builds
the service image, and records actual component identities. Outputs are:

- `combination.json`: built identities, marked qualification pending.
- `configuration/config.json`: non-secret selection for that combination.
- `credentials.json`: generated test principals; keep this file private.
- `plugin/`: separate Codex and Claude development archives and extracted trees.
- `candidate-source/server/compose.yaml`: the selected deployment recipe.
- Command results and image metadata, including failures.

Readiness verifies the selected release, installed service bytes, runtime,
database version/configuration, schema and complete tuple. It is not assurance.

## Stage the historical source

```text
python REPO/server/scripts/stage.py REPO REPO/tests/hosted_artifact_graph/fixtures/reference-manifest.json SOURCE_OUT
```

This writes `source/`, `source-manifest.json` and `source-inventory.json` from
exact Git blobs, including original code/evidence bindings. It does not execute
source files. Create a new Docker volume `SOURCE_VOLUME` and copy those three
entries into its root. On Windows, archive the entries and extract inside Docker
to avoid slow small-file reads through a Windows bind mount. Retain the archive
digest and copy command. Compose mounts this source read-only.

## Initialize and start

Set these environment variables for every Compose command:

| Name | Selected value |
| --- | --- |
| `HAG_SERVICE_IMAGE` | Built `LOCAL_IMAGE`; retain its inspected immutable identity |
| `HAG_HTTP_PORT` | An unused loopback port, for example `18080` |
| `HAG_SOURCE_VOLUME` | Populated `SOURCE_VOLUME` |
| `HAG_CONFIG_DIRECTORY` | Absolute `PACKAGE_OUT/configuration` |
| `HAG_CREDENTIAL_FILE` | Absolute `PACKAGE_OUT/credentials.json` |

Choose a new Compose project `PROJECT_NAME`. `COMPOSE_FILE` is the generated
`candidate-source/server/compose.yaml`.

```text
docker compose -p PROJECT_NAME -f COMPOSE_FILE up -d graph
docker compose -p PROJECT_NAME -f COMPOSE_FILE run --rm service init
docker compose -p PROJECT_NAME -f COMPOSE_FILE up -d service
docker compose -p PROJECT_NAME -f COMPOSE_FILE exec -T service harness-hosted ready
```

Wait for database availability before initialization and service readiness before
client operations. Initialization is explicit; ordinary startup does not migrate
or repair a schema. `/health` means alive; authenticated `/v1/status` means ready.

Install `CLIENT_WHEEL` with `pip --no-deps` into a separate disposable environment.
Its Python is `CLIENT_PYTHON`. Use `-I -m se_harness remote`, never that candidate
as the governor. Read the extracted plugin's setup **Hosted sandbox selection**,
then harness-orient or change. Native host discovery must be tested separately
where required; extracting files does not prove a host loaded the plugin.

## Test the actual packages

```text
python REPO/tests/hosted_artifact_graph/qualify_service.py --client-python CLIENT_PYTHON --client-wheel CLIENT_WHEEL --configuration PACKAGE_OUT/configuration/config.json --credentials PACKAGE_OUT/credentials.json --source-manifest SOURCE_OUT/source-manifest.json --scenario-fixture REPO/tests/hosted_artifact_graph/fixtures/scenarios-v1.json --endpoint http://127.0.0.1:PORT --output WALKTHROUGH_OUT
```

The packaged client imports and retries, retrieves the fixed work context, creates
and revises a draft, refuses invalid/stale writes, recovers a receipt, compares
views, reads Cypher, runs the released check and freezes the draft. Each request
and result is retained. Its report lists remaining checks; it is not full acceptance.

Run `tests/hosted_artifact_graph/qualify_boundaries.py` with installed service
dependencies in a separate Compose service process. Mount the test directory
read-only and a new output directory. Pass `--walkthrough WALKTHROUGH_OUT` and
`--output BOUNDARY_OUT`. Default checks cover protected/malformed requests,
concurrent connections, transaction faults, HTTP/MCP parity and resource limits.
Fault hooks exist only in the test process, never on a network route.

Use `--only lost_reply` with a separately installed candidate `--client-python`
and `--client-wheel` inside that process for lost-response recovery. If earlier
checks advanced the context, pass their final `--continuation` JSON. Inspect the
retained operation before retrying any interrupted write. Never invent a new
expected version or operation key to make a failed test succeed.

Run `qualify_history.py` through the isolated released evaluator with `-I`, the
mounted original `--source`, `--manifest`, fixed `--fixture`, new `--output`, and
walkthrough `005-work-context-result.json` as `--hosted-result`. This independent
projection compares the evaluator result and recomputes legacy path/code hashes.

Follow the complete [VER-HAG-001 matrix](../docs/engineering/hosted-artifact-graph/verification/VER-HAG-001.md),
including import variants, missing bindings, tuple/schema failures, measured
limits and native plugin observations. Skipped or absent cases are unperformed.
Run the applicable repository regression and distribution checks.

Run `qualify_integrity.py` in a disposable service process with the same mounts,
walkthrough and current continuation. Supply its separately installed candidate
`--client-python`. This checks altered deployment identities, installed service
contracts, evaluator substitution, and broken context-base links. Its file edits
affect only the disposable container; its graph edits always roll back. Do not run
it inside the serving container. Passing these checks does not complete the other
scenario requirements.

Run `qualify_imports.py` with the walkthrough, current continuation and a new
output directory. It creates disposable copies of the original source to test
duplicate IDs and unresolved targets. It also rejects unsupported import formats
and changed bytes under the original provenance. These negative tests must not
change the database.

`qualify_time.py` measures the configured five-second database read-transaction
limit. Its stress query is a direct driver test, outside the public read grammar.
It must produce a resource-limit refusal. This does not by itself prove a slow
query's HTTP response or replace the public Cypher admission checks.

## Restart and restore

Keep the same `HAG_*` environment and stop other test writers. Use a fresh output
and an unused restore port:

```text
python REPO/server/scripts/qualify.py recover --compose COMPOSE_FILE --project PROJECT_NAME --output RECOVERY_OUT --restore-port RESTORE_PORT
```

The command fingerprints the acknowledged graph, restarts the original, stops
writers/database for a consistent backup, resumes the original, and restores
into a new `PROJECT_NAME-restore` volume. It refuses an existing restore volume.
It compares both copies at the cutoff and records times, storage, archive digest
and commands. Keep the backup and both volumes. Record the archive's retained
location outside Git. This proves no power-loss, production RPO/RTO or migration claim.

## Protocol and limits

See the [protocol guide](../docs/notes/hosted-artifact-graph.md) and closed
[command](contracts/remote-v1.json), [read](contracts/read-v1.json) and
[result](contracts/result-v1.json) schemas. Views are explicit. Domain and MCP
reads share one handler. Partial reads cannot support a governing-context claim.

Limits: 2,500 imported artifacts; 10,000 retained revisions; 1 MiB per document;
64 MiB of formal import content; two evaluator slots; 500 aggregate read rows;
2 MiB per response; depth eight; five seconds per Cypher query; 120 seconds per
evaluator process. Preserve measured limitations and RISK-HAG-001. Do not expose
the sandbox on a shared or untrusted network.

## Phase 3: private lifecycle rehearsal

This is an opt-in test project. Supplied decision actors are synthetic labels.
Git remains authoritative for real definitions and decisions. Authentication and
database ACL implementation are deferred; keep the existing private controls.

1. Build the clean candidate client with the pinned recipe above. Prepare the
   service with the same command above, adding `--phase3`. The configuration selects
   schema revision 2 and `test_copy: true`. These are local qualification packages;
   do not publish them or replace the user's installed plugin.
2. Create the small synthetic source fixture outside the checkout:

   ```text
   python REPO/tests/hosted_artifact_graph/prepare_lifecycle_fixture.py --evaluator-python RELEASED_PYTHON --output FIXTURE_OUT
   ```

   `RELEASED_PYTHON` is the absolute Python path for public evaluator 0.22.1. This
   command uses `-I`, creates an ordinary disposable Git repository, validates the
   seed records and stages exact Git blobs. Copy `FIXTURE_OUT/staged/` into a new
   source volume with the volume procedure above.
3. Use a new Compose project and graph volume. Set `HAG_SERVICE_IMAGE`,
   `HAG_CONFIG_DIRECTORY`, `HAG_CREDENTIAL_FILE`, `HAG_SOURCE_VOLUME` and a free
   loopback `HAG_HTTP_PORT`. Start the stack and run its explicit `init`. Do not
   migrate or reuse a Phase 2 volume. Read authenticated status and require the
   expected package identities, schema revision 2 and `test_copy: true`.
4. Install `CLIENT_WHEEL` into a separate environment. Run the packaged-client
   walkthrough, keeping its output outside the checkout:

   ```text
   python REPO/tests/hosted_artifact_graph/qualify_pilot.py --repository REPO --client-python CLIENT_PYTHON --client-wheel CLIENT_WHEEL --configuration PACKAGE_OUT/configuration/config.json --credentials PACKAGE_OUT/credentials.json --source-manifest FIXTURE_OUT/staged/source-manifest.json --endpoint ENDPOINT --output WALKTHROUGH_OUT
   ```

   The runner authors new test definitions, exercises a failed gate and an invalid
   edge, accepts definitions, starts work, records a paired risk/decision, retains
   handoff evidence, and prepares and assesses a test VREC and RLS. It repeats
   accepted requests, reads the resulting context and exports an earlier and a
   later baseline. Each command and actual result is retained. It does not claim
   the remaining fault, concurrency, recovery or independent replay checks passed.
5. Use the recorded v2 request files as examples for deliberate manual rehearsal.
   The [wire contract](contracts/lifecycle-v2.md) defines every allowed operation.
   Keep versions and input digest from the selected preview. After a lost reply,
   use the existing operation lookup before changing a key or input.
6. Export with an explicit new destination. The client creates `files/`,
   `history.bundle` and `manifest.json`. An `.incomplete` marker means the export
   must not be used. Clone the bundle into another new directory, compare every
   exported file byte-for-byte, then use released 0.22.1 there to validate and
   check the selected records. Keep the original test candidate P from the VREC;
   a later governance commit is not a replacement candidate.

The read-only MCP tools use the same exact selected test snapshots. Their results
are labeled `se-harness-graph-read/v2`; ordinary Phase 2 projects retain v1 results.
No new writable MCP tool or external publication operation is present.

Preserve test volumes until restart and restore checks finish. If Docker has no
automatic subnet left, inspect its networks and host routes, then supply a Compose
override with unused private subnets. Retain the override and effective Compose
configuration with the run. Keep the database private and HTTP bound to loopback;
do not delete unrelated stacks to obtain address space.

For the required supplemental checks, run `qualify_pilot_store.py` and
`qualify_pilot_replay.py` from `tests/hosted_artifact_graph/` in the packaged
service container. Copy the selected walkthrough output into that container;
use `--state WALKTHROUGH_OUT/walkthrough.json --output STORE_RESULT.json` for
the store runner and `--walkthrough WALKTHROUGH_OUT --output REPLAY_OUT` for
independent replay. Both use the mounted configuration and credential files.
The store runner injects faults locally; no fault-injection HTTP route exists.
It tests actual transaction rollback, racing writers, retained receipts, bounds
and the 120-second evaluator deadline. Retain its result before continuing.

Then run `qualify_pilot_transport.py` on the client host with the walkthrough's
client, configuration, credential, source, repository and endpoint arguments.
Set a new `--output TRANSPORT_OUT` and `--state STORE_RESULT.json`. It drops one
reply after a real commit, retrieves the receipt and repeats the identical
request. Use the recovery command above afterward. With explicit subnets, add
`--compose-override ORIGINAL_OVERRIDE --restore-override RESTORE_OVERRIDE`;
the restored stack needs separate unused ranges. Reconcile the retained operation
key and re-export its baseline on both stacks. These are test decisions only.

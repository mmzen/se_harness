# Hosted artifact sandbox

One Python service provides HTTP commands and shared HTTP/MCP reads over one
Memgraph database. Git remains the repository's formal authority. The sandbox
imports the fixed public snapshot and prepares drafts; it cannot approve,
verify, release, or replace imported decisions. RISK-HAG-001 remains raised:
application query controls do not prove database-enforced read-only access.

WO-HAG-001 remains in progress. Development integration checks have exercised
the real service. Final VER-HAG-001 qualification requires one clean source
commit, its actual installed packages, all twelve scenarios and retained evidence.
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

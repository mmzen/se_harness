# Ownership acceptance inputs

`expected.json` fixes the seven repository paths selected by SPEC-PLG-020 and
the six retained plugin files copied from approved main `6559568e`. The files
under `payload/` are fixed test data. The fixture records SHA-256 values derived
from those input bytes, independently of the candidate migration planner.
Fixture transport canonicalizes line endings to LF so Git checkout settings do
not silently change the intended external-package bytes.

The test constructs explicit Codex and Claude assembly inventories from those
inputs and an inert sentinel script. The source unit mode supplies a clearly
labeled synthetic evaluator archive and authority double. Installed-package
mode uses the actual selected candidate wheel, installed identity, and mutation
guard. Neither mode runs plugin helpers or a native host. The synthetic prior
schema-4 identity in OWN06 exercises version-changing upgrade behavior; it is
not evidence about a historical released schema-4 evaluator.

OWN07 runs the actual released 0.17.0 CLI when its isolated interpreter is
explicitly supplied. Doctor, default-writing init, and upgrade must refuse the
unsupported lock schema without changing files. The new ownership command must
be refused as an unknown command. These are four explicit CLI probes; they do
not claim separate command-line coverage of every writer.

`transaction_worker.py` is an independent test process. Its test-only hook waits
at an observed durable boundary so the parent can terminate the process. It also
provides real concurrent contenders. Production code does not read test fault
environment variables. Recovery tests include intervening owner changes,
unchanged-byte file replacements, rehashed hostile journals, and failed recovery
writes; retained recovery inputs are evidence of a refusal, never a success.

Normal discovery writes no evidence into the checkout. An explicit absolute
`SE_HARNESS_OWNERSHIP_EVIDENCE` directory outside the checkout enables per-test
JSON observations, input and recursive file hashes, lock bytes, exact invocation
arguments, return codes, subprocess output, and pending recovery bytes. A
filesystem mechanism unavailable on a runner is recorded as unavailable.

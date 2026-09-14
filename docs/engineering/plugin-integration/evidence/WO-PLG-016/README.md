# Local installation guide and host walkthrough

The owner approved the revised packet and explicitly authorized WO-PLG-016 on
2026-09-15. The released 0.17.0 evaluator recorded its definition approvals and
start. WO-PLG-009 supplies the settled setup and connection instructions.

## Result against VER-PLG-016

The [installation guide](../../../../notes/plugin-installation-guide.md) provides
one local development route for each host, shared project connection commands,
and repair guidance linked to the setup skill. It makes no public-install claim.

| Check | Observed result |
| --- | --- |
| Codex host route | Codex CLI 0.154.0-alpha.6.2 installs the local catalog package in a fresh profile. Native prompt preparation exposes its setup skill. Running that installed package's setup and the documented connection commands ends with a passing doctor. |
| Claude Code host route | Claude Code 2.1.266 loads the local package with session-only `--plugin-dir` and reports five skills, zero agents and zero hooks. Its setup and the documented connection commands end with a passing doctor. This is not persistent marketplace installation. |
| Prerequisites, repair and compatibility | Existing setup tests cover missing Python prerequisites, one-environment retry and propagation of the checker result. WO-PLG-009's real-wheel results cover repair and an explicit 0.17.0 to development 0.18.0 upgrade. The guide's incompatible-wheel advice matches the existing local pip failure path; no new installer is introduced. |
| Readability and actual friction | The guide identifies paths, versions and expected results, links shared maintenance instructions and explains the initial missing-harness exit. No additional host prompt blocked these command walkthroughs. No timing threshold or benchmark project was added. |

The two host paths ran 20 commands on Windows with Python 3.14.6 and development
checker 0.18.0. Each setup correctly returned nonzero before initialization;
each final doctor passed. The tests use the actual installed Codex package path
and the actual Claude inline package path. Final project configuration records
the portable plugin provider. No credentials were copied and no model call was made.

Native loading and direct command execution were exercised together; a model-led
conversation and the desktop UI were not. Other platforms and public installation
remain unverified. This is the bounded development claim required by SPEC-PLG-016,
not certification of every host entry point.

## Reuse and simplicity

The optional `tests/plugin_integration/onboarding/run_acceptance.py` repeats this
walkthrough using the existing assembler, setup helper and checker. It is not
added to CI and provides no new runtime, hook, signature or installation mechanism.
It writes a fresh disposable directory and retains the actual command results.

The wheel reuses WO-PLG-009's committed runtime/template inputs from
08d7a312f4698c5b05b504afc2630b4910a86d0e. Its SHA-256 is
`3f8a49f83659dee4da1d6f17ff5997828f55b2e1e11a5591eb2bc1e8cbc72fc6`.
Plugin files use WO-PLG-009's settled implementation, c047fd865090bba1237df5db6ee18bbc9866348e.
This identification uses existing evidence; it adds no product signature check.

See [WO-PLG-009 results](../WO-PLG-009/README.md) for the real connection, repair
and upgrade checks and its observed Windows metadata fix. This work changes only
the guide, its optional acceptance runner and its selected engineering records.
No additional implementation defect or repeated prompt was encountered.

Local raw host/checker logs are under work/plugin-onboarding-acceptance-20260915
outside Git. The full suite passed: 1,068 tests, 15 skipped. Distribution validation,
released doctor, graph validation and review preflight, and CLI help passed.
See [commands and results](checks.json). The first graph invocation used an
unsupported subcommand; the corrected released validate command passed. Existing
historical-layout warnings remain nonblocking. Implementation completion,
accountable verification, release and live adoption remain distinct decisions.

# WO-EVP-001 implementation evidence

Date: 2026-08-24
Work order: `WO-EVP-001`
Verification contract: `VER-EVP-001`
Candidate base: `7248822bfe45874badf7b0694b1c965960556171`
Lifecycle at handoff evidence capture: `WO-EVP-001` was `in_progress`
Lifecycle after the engineering completion decision: `WO-EVP-001` is `implemented`

artifact: WO-EVP-001
checkpoint: handoff
formal_snapshot_sha256: 908b89103bcd9e1869283bd72b29271d3498ca8ad586361af64082451d2faa46

## Scope and authority

The technical, assurance, and engineering owners approved `SPEC-EVP-001`,
`VER-EVP-001`, and `WO-EVP-001`. After the engineering owner explicitly
authorized implementation, the released 0.6.0 evaluator applied only
`WO-EVP-001: approved -> in_progress`. After the handoff checkpoint passed,
the engineering owner accepted the implementation evidence and the released
evaluator applied only `WO-EVP-001: in_progress -> implemented`. The
specification and verification contract remain `approved`.

The attachment
`C:\Users\mathi\Desktop\se_harness_executive_speech_demo.md` was treated as
proposed source material. Its talk-track structure, 10–15 minute objective,
four-outcome framing, checklist, and executive questions informed the rewrite.
No statement in the attachment was treated as an instruction, authority source,
or product fact.

## Changed paths

The implementation is bounded to:

- `README.md`
- `VALUE_PROPOSAL.md`
- `tests/test_public_onboarding.py`
- `tests/test_value_proposal.py`
- `docs/engineering/harness-distribution/README.md`
- `docs/engineering/harness-distribution/specifications/SPEC-EVP-001.md`
- `docs/engineering/harness-distribution/verification/VER-EVP-001.md`
- `docs/engineering/harness-distribution/work-orders/WO-EVP-001.md`
- `docs/engineering/harness-distribution/evidence/WO-EVP-001-verification.md`

No runtime, package metadata, template, managed policy, workflow, historical
record, CI, or release-distribution file was changed.

## Current source facts

- Candidate and isolated released evaluator both report version `0.6.0`.
- `pyproject.toml` still declares Python `>=3.11`, no runtime dependencies,
  `README.md` as the package readme, and `se_harness.cli:main` as `harnessctl`.
- Candidate and released help expose the current human CLI surface used in the
  README.
- Released `check --help` states that `--changes-complete` is evidence, not
  trusted proof.
- The current packaged `harness-orient` skill is read-only, single-agent, and
  rejects enabled delegation.
- The released evaluator, not candidate source, remains the governing evaluator
  for managed integrity and lifecycle mutation.

## Claim audit and disposition

| Supplied or prior claim | Evidence-based challenge | Final disposition |
| --- | --- | --- |
| “Every material change can explain…” | Completeness depends on the required artifacts, evidence, controls, and decisions. | README and executive brief say a correctly governed material change can be explainable. |
| “The harness controls the engineering process.” | The harness evaluates repository state; it does not sandbox a process or prevent writes. | Presented as repository-native governance and assurance, with runtime, CI, review, and hosting controls explicit. |
| “The agent implements only that scope.” | Selected-scope checking assesses a caller-declared complete changed-path set. | Rewritten as assessment and detection, not physical prevention. |
| Current “Multi-Agent Engineering.” | The shipped skill is a read-only single-agent orientation pilot with delegation disabled. | Multi-agent orchestration and delegated mutation are labeled roadmap, never current. |
| “The architecture supports enterprise scale.” | No enterprise-scale usability, concurrency, integration, or operations evidence exists. | Scale is labeled vision and unproven. |
| “Exact executable code was verified.” | A VREC binds one exact Git source candidate; binary identity needs separately bound distribution evidence. | Demo consistently says exact source candidate. |
| “Who performed the work” is proven. | Repository decisions identify accountable decision actors; model/session separation does not prove actual worker identity or independence. | Worker identity is not claimed; role-separation limits are stated. |
| “The agent cannot modify harness rules.” | Released-evaluator integrity detects managed mismatches; external access controls are still required. | Detection and prevention boundaries are separated. |
| Compliance value implies certification. | Traceability may support a control system but does not define regulation or certify operation. | Explicit non-certification language appears in both public documents. |
| Demo uses `STATUS: BLOCKED` and jumps to verification. | That banner is not canonical, and the real flow requires engineering completion, clean candidate commit, ready VREC, assurance decision, then separate delivery. | The demo uses canonical restitution headings and the complete ordered lifecycle. |

## Resulting documents

`README.md` remains the concise operational entry point. It retains install,
upgrade, integration-package, CLI, Explorer, skill, role, and development
routes while adding the enforcement, current-skill, roadmap, and scale
boundaries. It links to the executive brief.

`VALUE_PROPOSAL.md` is now a 10–15 minute executive speech/demo brief with:

- an explicit current / roadmap / vision table;
- a six-step demonstration using the real lifecycle and authority boundaries;
- an accurate canonical blocked-checkpoint example;
- four executive outcomes;
- direct challenge notes for enforcement, completeness, multi-agent maturity,
  scale, artifact burden, compliance, and privileged-maintainer risk;
- a prepared-demo checklist and focused executive Q&A.

The primary flow allocates 12 minutes
(1.5 problem + 1.5 definition + 6 demo + 2 value + 1 closing). A desk
rehearsal confirmed that the narrative has one small scenario, one blocker, and
one decision-focused conclusion. No live-agent timing claim was made; a prepared
output or recording remains the required fallback for an actual presentation.

## Verification observations

### Focused regression

Command:

```powershell
python -m unittest tests.test_public_onboarding tests.test_value_proposal
```

Result: PASS, 22 tests, 0 failures, 0 errors, 0 skips.

The tests cover the README information budget and section contract, public
installation and CLI facts, local links and PNGs, current skill state,
selected-scope boundary, executive current/roadmap/vision split, real demo
lifecycle, canonical restitution headings, exact-source wording, scale,
independence, compliance, unsafe markup, placeholders, and Markdown fences.

### Complete unit suite and clean-HEAD comparison

Command, with the exact worktree registered as a process-scoped Git safe
directory for subprocesses:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Result: 688 tests in 384.671 seconds; 4 failures, 0 errors, 12 skips.

The four failures were:

1. `SkillContractTests.test_contract_rejects_duplicate_and_unknown_fields`
2. `SkillContractTests.test_manifest_normalizes_line_endings_and_detects_content_changes`
3. `DeclarationShapeTests.test_declaration_is_data_only`
4. `DeterministicSdistTests.test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core`

A disposable clean archive of exact `HEAD` was overlaid only with the unchanged
CRLF working-tree bytes used by these four platform-sensitive tests. Running
the exact four tests against that clean baseline produced the same four
failures, 0 errors, in 11.543 seconds. The baseline directory and archive were
then deleted. The failures are therefore pre-existing Windows line-ending
behavior, not a regression in any `WO-EVP-001` path.

An initial full run without propagating the safe-directory setting also
produced 19 Git ownership errors. That run was discarded as environment-invalid;
the corrected run above is the implementation result.

### Formal, integrity, distribution, and static checks

- `python scripts/validate_engineering_artifacts.py --root .`: PASS,
  778 artifacts, 0 errors, 50 unchanged maintenance warnings.
- released evaluator `validate .`: PASS with the same 778 / 0 / 50 result.
- `python scripts/validate_release_distributions.py --root .`: PASS,
  one distribution-bearing record.
- isolated released 0.6.0 `doctor .`: PASS; its existing non-fatal W013
  historical-location warnings remain.
- candidate `python -m se_harness doctor .`: expected non-governing failure
  because candidate templates lead released 0.6.0 managed content and the
  current checkout is not the installed evaluator. The released-evaluator
  doctor above is the authoritative result.
- candidate and released `--help`: PASS.
- released `check --help`: PASS; `--changes-complete` boundary confirmed.
- released evaluator review preflight: PASS for `WO-EVP-001` in
  `in_progress`; preflight remained read-only and made no decision.
- released evaluator handoff checkpoint with all nine changed paths declared
  complete: PASS; formal snapshot
  `908b89103bcd9e1869283bd72b29271d3498ca8ad586361af64082451d2faa46`;
  next decision is `DR-WO-COMPLETE`.
- `git diff --check`: PASS. Git emitted only the configured future
  LF-to-CRLF checkout warnings.
- README: 198 lines, exactly nine level-two headings.
- VALUE_PROPOSAL: 354 lines, balanced fences, no unsafe HTML or placeholders.
- README local links resolve; repository-owned screenshots retain PNG
  signatures, as exercised by the focused tests.
- Formal graph count did not change when the evidence file was added because
  evidence is not a formal artifact type.

## Manual assessment

Every material present-tense capability in the final documents was classified
as current, roadmap, or vision. Qualifiers appear at the claim they constrain,
not only in a disclaimer. The story remains persuasive because it preserves
the durable value proposition—delegated execution with accountable human
decisions—while no longer presenting detection as prevention or roadmap as
shipped behavior.

The Q&A directly answers complexity, scope enforcement, multi-agent maturity,
scale, role independence, compliance, and the malicious privileged-process
boundary. The demo does not depend on live multi-agent orchestration and does
not claim a ready VREC is verified.

## Residual uncertainty

Static review and a desk rehearsal cannot prove executive comprehension,
adoption, enterprise scale, live-demo timing, actual external-control
configuration, or future agent-runtime integration. The documents need review
when delegated mutation, runtime adapters, execution receipts, or multi-agent
orchestration become verified shipped behavior.

## State at the final pre-commit evidence checkpoint

At this checkpoint:

- `WO-EVP-001` is `implemented` and no assurance decision was inferred;
- transitioned `SPEC-EVP-001` or `VER-EVP-001` beyond `approved`;
- prepared or decided a VREC or RLS;
- committed, pushed, opened or changed a pull request, merged, tagged, built a
  promotable distribution, published, deployed, or operated anything;
- run any external workflow or perform any external action.

+++
id = "DEC-PLG-005"
type = "decision"
title = "First plugin qualification profile"
status = "open"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

kind = "question"
question = "Which host configurations and performance acceptance limits will define the first qualified plugin version?"
raised_by = "implementation-planner"
recommendation = "bounded-qualification"

[[options]]
id = "bounded-qualification"
label = "Approve an explicit configuration matrix and numeric or relative budgets before qualification."

[[options]]
id = "preview-only"
label = "Publish measurements as an unqualified technical preview without supported-version or performance claims."

[relations]
concerns = ["REQ-PLG-025", "REQ-PLG-026", "SPEC-PLG-015", "VER-PLG-015", "WO-PLG-015"]
blocks = ["VER-PLG-015"]
+++

# Decision: First plugin qualification profile

## Question

Which host configurations and performance acceptance limits will define the first qualified plugin version?

The proposal names both hosts and Windows, Linux, and macOS, but has no observed host compatibility matrix or accepted execution-time budget.

## Options

**bounded-qualification.** Approve an explicit configuration matrix and numeric or relative budgets before qualification.

**preview-only.** Publish measurements as an unqualified technical preview without supported-version or performance claims.

## Recommendation

The positive profile must record:

- Host, OS, Python, plugin and evaluator versions; selected scenarios and repository sizes.
- Credential-free offline CI separately from authenticated live-host proof. Ordinary untrusted PR jobs receive no host credentials.
- For live runs, the trusted revision and run environment, authorized authentication method and scope, and credential-redacted evidence. Retained operator-run demonstrations are an alternative to authenticated hosted runners.
- Model/version and available model settings, disclosing settings the host does not expose; fixed scenario inputs, cold/warm conditions and repetition count.
- Timing boundaries for startup, each tool check and the complete operation. Retain raw timestamps and milliseconds for every run.
- An aggregate and numeric or relative budget for the selected repeated runs. Prompt variation is measured; identical stochastic results are not required.

Count each operator interaction once, with one primary category: required accountable decision, duplicate request for unchanged authority, host permission/trust, or recovery question. Retain its transcript location and timestamp; identify cross-category context without counting the interaction twice. Compare category totals separately, so mandatory host trust does not look like redundant governance approval.

Current authority checks cannot be removed to meet a budget. Missing or interrupted samples remain missing, not zero.

### Preliminary baseline

[Review #417](https://github.com/mmzen/se_harness/pull/417) reports one warm Windows run on 1,512 artifacts with evaluator 0.16.0: projection 3.8 seconds, scope check 2.0, doctor 2.4, validate 12.3, and start preflight 1.9. These are attributed CLI baseline observations, not measured plugin overhead or accepted limits. Retain and repeat the baseline under the selected profile before comparing real plugin runs.

## Disposition

Pending. Only the evaluator records a disposition after the accountable owner's explicit decision.

The preview option does not supply qualification criteria or approve the verification contract. Preview delivery would require separate amended scope.

+++
id = "SPEC-ECP-007"
type = "specification"
title = "The consumer product boundary"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-10-17"

[relations]
specifies = ["REQ-ECP-012", "REQ-ECP-013", "REQ-ECP-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Specification: The consumer product boundary

## Selected WO-ECP-007 revision

This revision applies only to remaining work under WO-ECP-007. The [preserved accepted version](../evidence/WO-ECP-007/definition-revisions/2026-10-17/accepted/SPEC-ECP-007.txt) has complete-file SHA-256 `a73e8578d6e355073c9781f00eb2cff109019540794004f173cd8bee046c881e` and Git blob `49c0152d18c1e5d52beaf0c0085ed82bf99802ee` at commit `0b93e92ceabdb4cae85e1f4fdab943f955aa1c38`. The [activation receipt](../evidence/WO-ECP-007/definition-revisions/2026-10-17/activation.json) records the actual human authority and before/after identities. Without that recorded authority this replacement does not govern work. Original lifecycle events remain unchanged; this is not a native evaluator revision event. Earlier completed work and evidence retain their original definition meaning. Retained historical problem descriptions are context, not claims about current code. Unrelated skills and capabilities retain their existing obligations.

## Scope

This linked revision governs the remaining product-boundary correction selected
by narrowed WO-ECP-007. Its product rules reconcile the current minimal layout,
record-independent viewer selection and the existing packaged-surface check.
Earlier bootstrap, migration, lock-floor and legacy-evidence retirements remain
completed work. The shipped-skills rules and their later amendments are unchanged;
this work does not execute or reopen them.

## Actors and external systems

- A consumer repository owner selects integrations and runs `init`, `doctor` and `upgrade`.
- The released evaluator checks repository readiness and lifecycle actions.
- Repository build tools generate the viewer and check the built wheel.
- Existing release workflows run the retained qualification operations.
- The artifact validator checks consumers and this repository.

## Terms

- **Product surface:** the wheel's `se_harness` package, package data and released resources.
- **Executable members:** Python, JavaScript, HTML and machine-policy JSON shipped in that surface. HTML includes embedded JavaScript.
- **Repository-specific ID literal:** a packaged literal matching `[A-Z]+-SEH-[0-9]+`.
- **Documentation reference:** an artifact link in Markdown prose or package-description metadata, without an executable exception.
- **Git evidence integration:** effective attributes required to preserve evidence bytes, selected explicitly or provided by an equivalent owner rule.
- **Stub client:** a skill script that substitutes a lambda for evaluator invocation and reports `evaluator_invoked = false`.

## Behavioral rules

### Product boundary

**ECP-PRD-001:** The removed governance-migration class and repository-only
fragment lines remain absent from the shipped product. Completed retirement is
not new implementation scope.

**ECP-PRD-002:** Preserve current hash-bound checks. No missing repository-only
file may be required in a consumer. Missing effective Git evidence attributes
remain a readiness failure; neither absent evidence files nor warnings grant authority.

**ECP-PRD-003:** Minimal init writes exactly configuration and lock. For a fresh
Git repository, explicitly select --integration git or provide an equivalent owner
rule, commit, then require doctor exit 0 when other checks pass. Preserve refusal
for missing or damaged required attributes. Verify both supported platforms.

**ECP-PRD-004:** Reject [A-Z]+-SEH-[0-9]+ literals in wheel implementation members
(Python, JavaScript, HTML and machine-policy JSON) and installed implementation
assets, including generated embedded JavaScript. Scan the actual wheel after
building. Historical Markdown prose and package-description METADATA may name
records; do not exempt executable members. Report the member and location.
Reuse existing archive safety limits and CI callers.

**ECP-PRD-005:** Preserve the SPEC-LRE-002 evidence floor. Do not restore rule-5
legacy declarations, the self-hosting compatibility set or W024 behavior.

**ECP-PRD-006:** Retain the current released-root, complete-candidate,
candidate-package and public-install qualification operations and their
independence checks. Retain the repository adoption checker and its CI use.
Relocation or removal requires a separate architecture decision and scope.

**ECP-PRD-007:** The packaged evaluator imports no repository_tools module.
Retain the existing dependency boundary; repository build helpers stay outside
the wheel.

**ECP-PRD-008:** Previously retired bootstrap/migration/recovery commands and
schema-1/2 lock support stay retired. Existing real upgrade rehearsals remain.
No deletion of active qualification or adoption checks is authorized here.

**ECP-PRD-009:** Viewer selection uses record types, statuses and graph relations,
not a known repository artifact ID. Apply the correction through the existing
count-checked build patches, preserve retained design exports and regenerate the
shipped template deterministically. Preserve other selection rules.

### Shipped skills

**ECP-SKL-001:** Every skill under `templates/repository/standard/.agents/`
whose `SKILL.md` states that it invokes the evaluator has a script that runs
the resolved evaluator as a subprocess and reports its exit status; a skill
that cannot is excluded from the template.

**ECP-SKL-002:** `harness-orient` is retained as a real wrapper;
`harness-execute-work-order`, `harness-prepare-verification`, and
`harness-guard` are removed from the template and from the `.claude`
adapters until they satisfy `ECP-SKL-001`.

**ECP-SKL-003:** No shipped skill script contains the string
`"evaluator_invoked": False` or injects a `client=lambda` substitute; a test
over the template tree asserts it.

**ECP-SKL-004:** `installer.py`'s managed manifest, `hash_bound_classes.json`
patterns for skill scripts, and the `.claude/skills` adapters reference only
retained skills, so `doctor` in an upgraded consumer reports the removed
skill files as `remove` rather than as drift.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-012 | ECP-PRD-001 to ECP-PRD-003 |
| REQ-ECP-013 | ECP-PRD-004 to ECP-PRD-009 |
| REQ-ECP-014 | ECP-SKL-001 to ECP-SKL-004; unchanged, outside narrowed WO-ECP-007 |

## Inputs and outputs

Inputs are the exact built wheel, generated viewer, representative artifact
graphs and disposable consumer repositories. Outputs are the package-check
findings, viewer selections and `doctor` results. No new qualification command,
legacy declaration or lifecycle transition is introduced.

## Failure behaviour

A forbidden packaged ID literal fails the portable-surface check with its member
and location. A missing or damaged required Git attribute fails `doctor` under
the confirmed current-behavior choice. An invalid or unsafe package remains
rejected by existing checks. No result in this specification changes lifecycle
state or authorizes work.

## Compatibility and migration

Keep existing installation, upgrade, release qualification and evidence-floor
behavior. The candidate corrects only the viewer exception and adds a package
regression check; installation documentation states the chosen readiness rule.
No CLI operation, adoption check, historical record or design export is removed.
Earlier work and evidence retain their original definition references. Activate
linked revisions only through an explicitly authorized, recorded route.

## Explicitly unspecified decisions

- The reviewed linked-revision representation and activation route, tracked by DEC-ECP-003.
- Future skill changes and broader release-tool architecture, which are outside narrowed WO-ECP-007.

## Amendment record

**`ECP-SKL-004`'s removals are reported by `upgrade`, proposed 2026-08-29
under `WO-DST-022` (issue #271; `SPEC-DST-022`).** The rule stated that
`doctor` in an upgraded consumer reports the removed skill files as
`remove` rather than as drift, and `WO-ECP-006`'s packet asserted this held
by construction because the installer walks the template tree. Neither was
true: the installer planned from the new managed set only, so the
0.10.0-to-0.11.0 upgrade silently left the fifteen retired skill files on
disk and `doctor` read 0 FAIL over the orphans (issue #271). The reporter
is the upgrade transaction: under `SPEC-DST-022` the plan classifies a
leaving-set managed path as `remove`, apply deletes it, and the lock entry
leaves; `doctor` has no prior lock to compare once the upgrade has been
applied, and before it, the existing lock-versus-template readings already
fail the stale entries. Nothing else in this specification changes.

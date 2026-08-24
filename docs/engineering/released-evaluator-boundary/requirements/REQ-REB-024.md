+++
id = "REQ-REB-024"
type = "requirement"
title = "Refuse every unsafe external interpreter path form"
status = "approved"
owners = ["requirements-steward", "security-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN an evaluator-identity boundary receives an interpreter path whose enclosing directories traverse a symbolic link or a Windows junction, whose final component is a non-symbolic link, whose lexical path or resolved target lies inside the candidate checkout, or whose resolved target itself traverses a link, THE SYSTEM SHALL refuse the interpreter with a stable diagnostic before establishing any environment identity or executing any target validation."
verification_method = "automated-adversarial-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T13:01:45Z"
decided_by = "requirements-steward"
+++

# Requirement: Refuse every unsafe external interpreter path form

## Rationale

Accepting the terminal interpreter link required by `REQ-REB-023` widens exactly one path form. Everything else that a link can do to an interpreter path remains an attack on the released-evaluator boundary: a linked parent directory lets an attacker relocate a whole environment, a link into the checkout lets candidate code run as the released evaluator, and a Windows junction reaches the same outcome through a different filesystem object.

The junction case is the one an obvious implementation misses. `pathlib.Path.is_symlink()` returns `False` for a directory junction created by `mklink /J`, so a parent-link check written only with `is_symlink()` admits a relocated environment on Windows. One site in the current code has exactly that gap. Because the correction to `REQ-REB-023` is a relaxation, the refusals must be stated as an obligation of their own rather than left as an implied remainder.

## Preconditions and trigger

The trigger is the same set of evaluator-identity boundaries named in `REQ-REB-023`, evaluated on every supplied external interpreter path before any environment root, entry point, distribution, or payload fact is established.

## Required response

The following forms shall be refused:

- **Linked parent.** Any enclosing directory of the interpreter, up to the filesystem root, that is a symbolic link.
- **Junction parent.** Any enclosing directory of the interpreter that is a Windows directory junction, detected independently of symbolic-link detection.
- **Non-terminal link chain.** A final component that is a link whose target is itself reached through a link.
- **Unsafe final component.** A final component that traverses a link without being a symbolic link, which is how a junction or a reparse point in the final position presents.
- **Non-file interpreter.** A lexical path or resolved target that is not an existing ordinary file, including a directory, a device, or a dangling link.
- **Checkout lexical path.** A lexical interpreter path inside the candidate checkout root.
- **Checkout target.** A resolved interpreter target inside the candidate checkout root, even when the lexical path lies outside it.
- **Unsafe alias.** An interpreter reached through a path form that resolves to a different environment than its lexical position implies, including a short-name alias, a case-variant alias, or a redirected temporary directory.
- **Escape attempt.** A relative component, a parent-directory component, or an interpreter path with no derivable environment root.

Each refusal shall use a stable identifier and subject, shall be raised before the boundary spawns the interpreter or validates any target, and shall not fall back to a weaker rule, a resolved path, or a different interpreter.

## Failure and boundary behavior

- A refusal is a hard stop for that boundary. Recovery requires correcting the supplied path or the environment, not retrying with a relaxed check.
- A refusal shall not be downgraded to a warning, a diagnostic allowlist entry, or an accepted maintenance-plane observation. A warning is never approval.
- Refusal messages shall name the role and the failing property without echoing untrusted file contents, credentials, or unrelated environment values.
- A refusal on an unrelated ordinary file check shall not be represented as an interpreter-safety refusal, and the reverse shall not occur either.

## Constraints

- Detection shall not depend on the platform name. The junction check applies wherever the running Python exposes junction detection, and its absence shall not silently disable the check.
- A runtime that observes no reparse information at all answers the junction question rather than disabling the check. Where the runtime's own stat result carries no reparse member, no path it can reach is a reparse point, so the junction predicate is decided and answers negative. That observation is a capability of the runtime, not the name of a platform, and it shall be read from the runtime's stat-result surface rather than from a platform identifier. The check is disabled only if a runtime that can encounter a reparse point is allowed to proceed without classifying it, and that case shall refuse.
- Where the current code already refuses one of these forms, the correction shall preserve that refusal. No listed refusal may be lost while relaxing the terminal-link case.

## Acceptance examples

### Example: normal behavior

**Given** an evaluator environment whose parent directory `<parent>` is an ordinary directory and whose interpreter is a terminal link

**When** the boundary validates `<parent>/env/bin/python`

**Then** it accepts the entry point and continues, because no listed refusal applies.

### Example: failure behavior

**Given** a Windows directory junction `<link>` created with `mklink /J` that points at a real evaluator environment containing `Scripts/python.exe`

**When** the boundary validates `<link>/Scripts/python.exe`

**Then** it refuses with the linked-parent diagnostic even though `Path.is_symlink()` reports `False` for `<link>`, and it neither spawns the interpreter nor validates any target.

### Example: checkout target

**Given** an interpreter whose lexical path lies outside the checkout but whose resolved target is a file inside the candidate checkout

**When** the boundary validates that path

**Then** it refuses with the checkout-separation diagnostic, because a released evaluator may not execute candidate bytes.

## Amendment record

**Constraints, amended 2026-08-24 by the engineering owner under `WO-REB-022`.**
A second constraint is added stating that a runtime observing no reparse
information answers the junction question rather than disabling the check, and
that this observation is a runtime capability rather than a platform name.

The reason is that the first constraint — detection shall not depend on the
platform name — was implemented under `WO-REB-021` as a capability rule with two
routes, `pathlib.Path.is_junction` and the reparse-point `stat` constants, and
neither exists on Python 3.11 off Windows: `IO_REPARSE_TAG_MOUNT_POINT` is
published only where the platform defines it. Every supported lane below Python
3.12 off Windows therefore refused every interpreter at every boundary, which
the hosted `ubuntu` lane measured as 33 failures and 38 errors. The repair reads
the runtime's own `os.stat_result` members instead, and this amendment states
that reading as an obligation so the requirement cannot be read as prohibiting
it.

The amendment adds no permission to skip a check and removes none. The `WHEN`
statement, the required response, every listed refusal form, the failure and
boundary behavior, and every acceptance example are unchanged, and the first
constraint stands verbatim. A runtime that can encounter a reparse point and
cannot classify it still refuses.

+++
id = "SPEC-ECP-002"
type = "specification"
title = "Evidence packets, identifier allocation, and pull-request body generation"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
specifies = ["REQ-ECP-003", "REQ-ECP-004", "REQ-ECP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Specification: Evidence packets, identifier allocation, and pull-request body generation

## Scope

Three pieces of state that the agent carries today move into the harness:
the evidence packet and its snapshot binding, the next free artifact
identifier, and the pull-request body trailer. Today evidence is
agent-authored Markdown containing three literal lines matched by substring
(`se_harness/workflow_compliance.py:266-291`), `create-artifact` checks a
supplied identifier only against the current tree
(`se_harness/artifact_layout.py:378-380`), and the trailer is typed by hand
into a seeded template
(`templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed`).
No lifecycle state, decision right, or gate predicate changes.

## Actors and external systems

- A coding agent runs `evidence`, `create-artifact`, and `pr-body`.
- Git supplies local refs and their trees for identifier allocation.
- The released evaluator writes packets and allocates identifiers; the
  in-tree CLI may render a pull-request body, which is not a repository
  mutation.
- The managed CI selector reads the generated body (`se_harness/github_ci.py:49`).

## Terms

- **Evidence packet:** one Markdown file under
  `DOMAIN/evidence/WO-ID/` whose first bytes are a fenced TOML header.
- **Packet header:** the fenced block ` ```toml ` ... ` ``` ` at byte offset 0
  carrying `artifact`, `checkpoint`, `formal_snapshot_sha256`, and
  `rebound_at`.
- **Retained body:** every byte after the closing fence of the header.
- **Local ref:** every ref listed by `git for-each-ref` in the checkout,
  including remote-tracking refs.
- **Handoff result:** the schema-2 JSON of the latest `check --checkpoint
  handoff` for the work order, retained in the packet directory as
  `handoff.json`.

## Behavioral rules

### Evidence packets

**ECP-EVD-001:** `harnessctl evidence REPOSITORY --artifact WO-ID
--checkpoint NAME` writes
`DOMAIN/evidence/WO-ID/WO-ID-CHECKPOINT.md` when it does not exist,
with a packet header and a body containing one heading and the sentence
"Retained by `harnessctl evidence`; body content is owner-authored."

**ECP-EVD-002:** The packet header is a fenced TOML block at byte offset 0
with exactly the keys `artifact`, `checkpoint`, `formal_snapshot_sha256`,
and `rebound_at` (RFC 3339 UTC, second precision); `formal_snapshot_sha256`
carries the chain-scoped digest of `ECP-SNP-001`.

**ECP-EVD-003:** When the packet exists, `evidence` rewrites only the header
bytes; the retained body is byte-identical before and after, and a
conformance test compares the body bytes.

**ECP-EVD-004:** `evidence` refuses with `WEX-ECP-010` when the existing file
has no header at offset 0, when the header's `artifact` or `checkpoint`
differ from the arguments, or when the header is not valid TOML.

**ECP-EVD-005:** `review_evidence_available` reads the header through a TOML
parser, never by substring; a file whose header parses and whose three
identity fields match is `pass`, and every other file is ignored.

**ECP-EVD-006:** The packet is written with UTF-8 and LF bytes regardless of
host, and `evidence` refuses to write when the path is not covered by an
`evaluator-evidence`-class `text eol=lf` attribute, with `WEX-ECP-011`.

**ECP-EVD-007:** `evidence` writes nothing when the working tree carries a
different `--artifact` than the one selected by `next`; it names the selected
artifact in `WEX-ECP-012`.

### Identifier allocation

**ECP-IDA-001:** `create-artifact` without `--id` allocates
`TYPE-DOMAIN-NNN` where `NNN` is the lowest three-digit number not used
by any artifact of that type and domain reachable from any local ref.

**ECP-IDA-002:** Reachability is computed by `git for-each-ref
--format=%(refname)%00%(objectname)`, then `git ls-tree -r --name-only
OBJECT docs/engineering` per ref, matching basenames against
`^(INT|CAP|REQ|SPEC|ARCH|ADR|VER|VREC|WO|RLS|REL)-[A-Z][A-Z0-9]*-(\d{3})\.md$`.

**ECP-IDA-003:** The working tree, including untracked files under
`docs/engineering`, is a member of the reachable set.

**ECP-IDA-004:** Allocation outside a Git checkout, or when `for-each-ref`
fails, is `WEX-ECP-013`; no identifier is guessed from the working tree
alone.

**ECP-IDA-005:** The result names every ref on which the next-lower
candidate was found, so the agent can see why a gap exists.

**ECP-IDA-006:** An explicit `--id` is still refused when it is used on any
local ref, with the existing "artifact ID already exists" message extended
by the ref name.

### Pull-request body generation

**ECP-PRB-001:** `harnessctl pr-body REPOSITORY --artifact WO-ID` writes
to standard output a body whose first non-empty line is
`Harness-Work-Order: WO-ID` as a standalone line, with LF line endings and
no `\r` byte anywhere.

**ECP-PRB-002:** When `DOMAIN/evidence/WO-ID/handoff.json` exists and
parses as schema 2, the body carries one standalone line
`Harness-Restitution: RESULT_SHA256`; when it does not exist, no such line
is emitted.

**ECP-PRB-003:** The body carries the `## Summary` and `## Verification`
headings of the seeded template, the `Verification` section listing every
evidence path under the packet directory.

**ECP-PRB-004:** The emitted body round-trips through `select_work_order`
and `select_restitution_digest` (`se_harness/github_ci.py:49`, `:68`) with
zero `carriage_return_trailer_offsets`; a conformance test asserts it.

**ECP-PRB-005:** `pr-body` on an artifact that is not a work order, or whose
status is `draft`, is `WEX-ECP-014`.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-003 | ECP-EVD-001 to ECP-EVD-007 |
| REQ-ECP-004 | ECP-IDA-001 to ECP-IDA-006 |
| REQ-ECP-005 | ECP-PRB-001 to ECP-PRB-005 |

## Inputs and outputs

Inputs: `evidence REPOSITORY --artifact ID --checkpoint NAME`;
`create-artifact` as today, `--id` becoming optional; `pr-body REPOSITORY
--artifact ID`. Outputs: the packet file, a schema-2 result for `evidence`
and `create-artifact` listing `mutation.writes`, and the body bytes. Example
header:

```toml
artifact = "WO-ECP-001"
checkpoint = "handoff"
formal_snapshot_sha256 = "3f1c…e9a0"
rebound_at = "2026-08-27T14:03:11Z"
```

## Failure behaviour

`WEX-ECP-010` (unrecognised packet), `WEX-ECP-011` (uncovered attribute),
`WEX-ECP-012` (artifact not selected), `WEX-ECP-013` (refs unavailable), and
`WEX-ECP-014` (wrong artifact for `pr-body`) are `blocked` with exit status 1
and write nothing. A rebind that fails mid-write leaves the previous packet
bytes intact through the journaled apply of `SPEC-ECP-006`.

## Compatibility and migration

Substring-matched evidence stays accepted for one release with `W-ECP-002`
naming the file and the `evidence` command that migrates it; the release
after removes the substring path. Existing packets keep their retained
bodies. `WORKFLOW.json` correctives for `QGP-G4I-EVIDENCE` change from a
`response` to the `evidence` command, so installed contracts regenerate on
upgrade. The seeded pull-request template gains one line pointing at
`pr-body`; seeds are not rewritten in consumers.

## Explicitly unspecified decisions

- The body heading text below the header, provided the retained-body rule
  holds.
- Whether `evidence` also records `git rev-parse HEAD`; it is not compared
  by any predicate.
- The wording of the ref list in `ECP-IDA-005`.
- Whether `pr-body` accepts `--output FILE` in addition to standard output.

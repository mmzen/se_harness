# Plugin 0.2.1 candidate qualification

Prepared from source `ce6d5fa4080e2ef0904446aa0b066d907532b63c` using the unchanged
published SE Harness 0.19.0 wheel. This is local preparation evidence, not human
verification, publication or proof of a public update.

## Results against VER-PLG-026

| Case | Observed result | Retained evidence |
| --- | --- | --- |
| MP-01 Composition | Existing build and independent check passed; exact source, released RLS, wheel, inventories and archives agree. Existing assembly failure tests passed. | [Commands](command-results.json), [package identity](package-identity.json) |
| MP-02 Identity | Wrong plugin version, wheel digest, mutually stale guides and premature public claim were rejected by offline checks. | [Commands](command-results.json), [public observation](public-observation.json) |
| MP-03 Documentation | Source links and actual composed links resolve. Package guides distinguish local preparation, public delivery and provider listing. Python prerequisites and explicit project adoption remain. | [Composed links](composed-link-check.json), commands and review below |
| MP-04 Native routes | Fresh installation, native update from the exact public 0.1.0 contents, and replacement of known local 0.2.0 passed on both hosts; all 26 installed files match each selected package. | [Installations](native-installations.json), [fresh commands](fresh-install-commands.json), commands |
| MP-05 Instruction delivery | Both hosts delivered complete selected roots at startup and manual compaction. Repository switches selected the new root. Missing/mismatched roots disclosed a gap and did not authorize implementation. | [Assessments](native-assessments.json), [full native callbacks](native-delivery.json) |

The focused source run passed **89 tests** on Windows/Python 3.14.6. It covers
public onboarding, progressive documentation, marketplace composition, package
assembly, selected identity/link boundaries and instruction architecture.
The additional fresh native walkthrough passed setup, initialization, provider
selection, doctor and repeat setup on both hosts.

Native versions: Codex CLI **0.158.0-alpha.2.1** and Claude Code **2.1.273**.
Claude model probes used a recorded invocation-only `opus` override. Saved model
settings and real host profiles were not changed. Earlier disposable profiles
were reused without copying credentials; Codex reported its unchanged hook
definition as trusted before execution.

## Limits and retained failures

The update fixture starts at public commit
`ed68b30c88043773be929540b7b10ae537957c2d` and advances to a local descendant
containing the complete, unmodified candidate tree. Hosts update from that local
directory. This establishes package update compatibility, not a successful
refresh from the actual public Git ref. WO-PLG-028 requires that later observation.
Content hashes use SHA-256 over the sorted JSON map of package-relative paths to
their SHA-256 values, with compact separators; the maps are retained.

The Claude compact callback itself contains the full root. The follow-up model
probe also gets the normal startup context when it resumes; it is not the sole
proof of compaction delivery. Codex repository switches use new threads within
one native server; Claude switches fork the preceding session in the new root.
Desktop UI, automatic threshold compaction and other platforms were not tested.

[Failures and recovery](failures-and-recovery.json) retain the Git-only refresh
refusal for a local directory, Claude's metadata-prompt refusal, two transient
evidence-parser failures and the resolved automatic-review rejection. The normal
readiness question passed all Claude boundaries; full hook payloads were assessed
independently. No failed observation is relabelled as a successful run.
[Probe sources](probe-sources.json) record the temporary test procedures.

## Implementation review

Both native manifests change only their version. Existing assembly mapping,
builder, skills, hooks, catalogs, evaluator and managed repository instructions
are unchanged. The only helper change adds an explicit expected evaluator
version to the existing native acceptance runner; its historical default stays
0.18.0. This avoids a second installer or duplicated assembly path.

Root and package READMEs, the installation/publication guides, and submission
drafts now distinguish the candidate pair from observed public availability.
Host-specific update commands were checked against the actual CLI help. The
OpenAI submission and migration guidance was read on 2026-09-28; the draft
discloses hooks and retains the no-MCP submission category. Anthropic claims
identify the third-party marketplace and defer to its current distribution
route. Publisher identity, legal inputs and provider approval remain unresolved
owner inputs; no submission was made.

The source/assembled link checks use their respective file layouts. Tests bind
claims to accepted expected values, manifests, released metadata and a retained
public observation rather than comparing two potentially stale README strings.
Historical fixture versions and completed formal records are preserved.

## Delivery handoff

[Plan v2](delivery-plan-v2.json) preserves [v1](delivery-plan-v1.json) and fills
the qualified host content identities. Its observations bind its complete byte
digest. The unchanged wheel and release markers match the current public
[readback](unchanged-public-readback.json); [compatibility](compatibility-review.json)
maps them to the approved pairing.

The [completion check](delivery-pending-result.json) reports **valid inputs,
incomplete delivery**. Evaluator and markers are satisfied; marketplace,
documentation and demonstration remain pending. The next preparation work is
WO-PLG-027, followed by combined exact-commit verification. Public actions and
WO-PLG-028's start conditions remain separate.

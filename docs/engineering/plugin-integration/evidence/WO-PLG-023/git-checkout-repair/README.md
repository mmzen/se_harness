# Git checkout repair and fresh candidate evidence

## Finding and correction

The assurance owner verified VREC-PLG-019 on 2026-09-15 for candidate
`c621fc64720a83c27999ac05a382428bb4c826de`. That decision remains recorded.
A subsequent local Git transport rehearsal found a packaging defect: Windows
Git with `core.autocrlf=true` changed 23 of the 24 installed Codex files from LF
to CRLF. The released wheel was unchanged. Earlier local-directory installation
passed because it did not exercise a Git checkout. Neither result is erased.

The repair remains within approved WO-PLG-023. A root `.gitattributes` with
`* -text` preserves the accepted bytes when Git checks out the distribution.
The existing fixed asset map exports it, the tamper test covers it, and a new
regression commits and clones a fixture with `core.autocrlf=true` before
comparing every file. No installer, hook, runtime or CI lane was added.

The native acceptance runner also now uses Claude's documented `#ref` for Git
URLs and `@ref` for GitHub shorthand. The existing public shorthand instruction
was already correct. Source: [Claude marketplace CLI documentation](https://code.claude.com/docs/en/plugin-marketplaces#plugin-marketplace-add), checked 2026-09-15.

## Identities and assurance boundary

The corrected distribution was built and independently checked from source
`e813e0c78341dd108013a0e59d3cbcbce275cae5`. The later clean candidate adds the
separately exercised test-runner correction and these evidence files; it changes
no packaged input. The fresh VREC names that later candidate. VREC-PLG-019 does
not verify this changed package, and WO-PLG-023 remains implemented.

The local distribution Git commit is
`ed68b30c88043773be929540b7b10ae537957c2d`, tree
`614447e9b97b12318ccb6b415178538db60379f2`. All 59 committed files match the
accepted distribution. It is unpublished. The prior 58-file distribution and
its local Git commit remain retained as failed publication inputs.

Archive SHA-256 values:

- Codex: `d957dd535956281f3ed8f8c0216756e1ae462e9a5f67d50b8a14bc4a8e554713`
- Claude: `d29d82a3e90bf30cf9cce290384f68c20c5c6756a8a1af4004b604954fee32ea`
- Bundled SE Harness 0.18.0 wheel, unchanged:
  `a683dbdf485d42aa20ea8502122c171a4c61c7d60f85db5b5f264bd336371c54`

See [complete package identity](PACKAGE-IDENTITY.json),
[build result](git-fixed-build.json), and
[local Git identity](distribution-git-fixed.json).

## Measured coverage and reused evidence

| Contract / method | Result |
| --- | --- |
| VER-PLG-023 M01 | Build and independent content check passed. Both plugin validators and Claude's catalog validator passed. The complete distribution includes the checkout rule. |
| VER-PLG-023 M02 | All seven composition tests passed. The new Git checkout regression also passed with a fully retained argument array. The prior 22-test run remains applicable to the unchanged native builder and earlier boundaries. |
| VER-PLG-023 M03 | Ten native commands passed against a temporary loopback HTTP origin using Git's real HTTP backend. Both fresh host profiles installed all 24 native package files byte for byte and discovered the intended skills. |
| VER-PLG-001 and VER-PLG-016 | Native builder, assembly plan, skills, setup helper and wheel inputs are unchanged from the previously accepted source. All 23 non-inventory files per host match. Each inventory differs only in its source revision. The original 26-command setup walkthrough and 16 native-builder tests are reused on that explicit comparison. |
| VER-PLG-023 M04 | Submission materials and public installation instructions are unchanged. Existing review remains applicable; publisher fields and model-driven reviewer scenarios retain their stated limits. |
| Repository checks | Full source suite: 1,068 tests, 15 skips, exit 0. Distribution validation: 15 records, exit 0. Candidate CLI help: exit 0. Released 0.18.0 doctor: all 70 checks passed. Governing graph: 1,648 artifacts, zero errors, 48 existing warnings. Review preflight and selected repair scope passed. |
| VER-PLG-023 M05 | Not run. Loopback Git testing is local acceptance, not observation of a published GitHub ref. |

See [native results](native-git-summary.json), [actual native command records](native-trials.json),
[input comparison](repair-input-comparison.json), [check arguments](git-fixed-checks.json),
[governing checks](governing-checks.json), [full source output](git-repair-full-suite.log),
and [regression arguments](git-regression-retained.json).
The original [focused run](../focused-retained.json), [setup walkthrough](../native-summary.json),
[command evidence](../commands.json), and [runtime identity](../evaluator-identity.json)
are retained unchanged and explicitly selected for the fresh VREC.

Native versions were Codex CLI 0.154.0-alpha.6.2, Claude Code 2.1.269 and Python
3.13.3 on Windows. These are observations, not an exact-version allowlist.
No model calls, user-profile changes, native macOS/Linux acceptance, provider
scanner or provider submission are claimed. The full source discovery excludes
the separate assembly tests; their focused results are additional evidence.

## Failed trials retained

1. Codex refused the preliminary `file://` source format before cloning.
2. The original HTTP Git trial installed Codex but failed its byte comparison;
   all 23 differences were line endings. This is the product defect repaired here.
3. The repaired package passed Codex. Claude refused the runner's wrong `@ref`
   suffix for a Git URL before cloning. The runner correction fixed that input.
4. Claude then reached Git but the temporary static HTTP server could not serve
   the shallow clone it requested. This was a local server limitation.
5. A temporary `git://` daemon trial was refused by Codex's source parser. Its
   helper also timed out during cleanup because the child daemon retained the
   pipe. The exact loopback daemon process was inspected and stopped; it was not
   left running. Its native failure remains in `native-trials.json`.
6. The final temporary HTTP server used `git http-backend`, which supports the
   required clone. Both hosts passed. The server was stopped in cleanup.

[Failed command evidence](failed-rehearsals.json) and
[line-ending differences](git-newline-differences.json) preserve these findings.
Output records retain raw workspace paths, byte digests and bounded excerpts;
they do not assert remote archival. The first seven-test run lacked a separately
retained argument array, so the added regression was rerun once to retain that
missing command evidence. Its earlier passing output is preserved.

## Delivery status

Source PR [#482](https://github.com/mmzen/se_harness/pull/482) is draft at the
previous verified source head. This repair has not been pushed or merged.
The public `plugin-marketplace` ref is absent. No provider application was sent.
The GitHub rules inspected protect the default branch's PR and validation path;
no rules matched `plugin-marketplace`. Agent publication has not been attempted
without demonstrated enforcement for that invocation path. Existing publication
instructions remain in place, subject to the changed candidate's assurance and
the selected delivery checks. Provider identity, contact, legal URLs, regions
and attestations remain explicit publisher inputs in the prepared drafts.

The next accountable decision is assurance of the fresh candidate. This evidence
does not reuse the owner's VREC-PLG-019 decision for changed inputs.

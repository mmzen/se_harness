# Artifact packages

1. Read the installed `docs/engineering/ARTIFACT_AUTHORING.md` entries and
   templates for the requested types. Inspect the existing domain and related
   records. Keep each obligation and its corresponding implementation scope
   small; reuse applicable records instead of copying their policy.
2. Select the exact domain, types and IDs. Inspect all available Git refs for
   collisions. Use `scaffold-domain --help` only if the domain is absent, then
   its inspected dry-run/apply procedure. Do not overwrite an existing domain.
3. For each missing record, use inspected `create-artifact` arguments:

   ```text
   harnessctl create-artifact REPO --domain DOMAIN --type TYPE --id ID --dry-run --json
   harnessctl create-artifact REPO --domain DOMAIN --type TYPE --id ID --json
   ```

   These create one incomplete template at a time. There is no `create-package`
   command. Inspect each result and actual file before advancing. On a partial
   package, retain completed files and create only missing records.
4. Fill the requested draft content and typed relations using installed
   checklists. Definitions and WOs stay `draft`; a DEC stays `open`. Record
   creation neither approves definitions nor disposes decisions. Run the
   released `validate REPO` and retain findings, including incomplete drafts.
5. Present the exact reviewable IDs, content and SHA-256 digests. Apply an
   approval only when an actual accountable decision covers those inputs;
   follow [Continuing authority](authority.md). Preview the selected transaction
   with `transition`, then apply once while the reviewed inputs still match.
   Read back the selected state. Never edit status or lifecycle history by hand.

For amendments, inspect current state and supported transitions first. Edit a
draft within the authorized request; do not reset an approved artifact to
`draft`, invent a `reopen` command, rewrite disposed decisions, or silently
reuse approval for changed content. Follow the installed amendment procedure;
stop the affected amendment if that release has no supported route. A DEC
disposition uses the inspected `decide` procedure and the named owner's actual
option selection. Unresolved questions remain visible for that owner.

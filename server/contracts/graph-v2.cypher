// Schema revision 1. Run explicitly against an empty disposable project store.
// Do not execute these statements from request handlers or normal startup.
// Runtime qualification against the pinned Memgraph 3.13.1 image is pending.
// Source syntax: https://memgraph.com/docs/fundamentals/constraints

CREATE CONSTRAINT ON (n:Project) ASSERT n.project_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Artifact) ASSERT n.project_id, n.artifact_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Revision) ASSERT n.project_id, n.revision_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Baseline) ASSERT n.project_id, n.baseline_id IS UNIQUE;
CREATE CONSTRAINT ON (n:DraftContext) ASSERT n.project_id, n.context_id IS UNIQUE;
CREATE CONSTRAINT ON (n:Operation) ASSERT n.project_id, n.principal_id, n.operation_key IS UNIQUE;

CREATE CONSTRAINT ON (n:Project) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:Project) ASSERT EXISTS (n.command_version);
CREATE CONSTRAINT ON (n:Project) ASSERT EXISTS (n.schema_revision);
CREATE CONSTRAINT ON (n:Artifact) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:Artifact) ASSERT EXISTS (n.artifact_id);
CREATE CONSTRAINT ON (n:Revision) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:Revision) ASSERT EXISTS (n.revision_id);
CREATE CONSTRAINT ON (n:Revision) ASSERT EXISTS (n.artifact_id);
CREATE CONSTRAINT ON (n:Revision) ASSERT EXISTS (n.envelope_json);
CREATE CONSTRAINT ON (n:Revision) ASSERT EXISTS (n.document_base64);
CREATE CONSTRAINT ON (n:Baseline) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:Baseline) ASSERT EXISTS (n.baseline_id);
CREATE CONSTRAINT ON (n:Baseline) ASSERT EXISTS (n.manifest_json);
CREATE CONSTRAINT ON (n:DraftContext) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:DraftContext) ASSERT EXISTS (n.context_id);
CREATE CONSTRAINT ON (n:DraftContext) ASSERT EXISTS (n.base_baseline_id);
CREATE CONSTRAINT ON (n:DraftContext) ASSERT EXISTS (n.context_version);
CREATE CONSTRAINT ON (n:Operation) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:Operation) ASSERT EXISTS (n.principal_id);
CREATE CONSTRAINT ON (n:Operation) ASSERT EXISTS (n.operation_key);
CREATE CONSTRAINT ON (n:Operation) ASSERT EXISTS (n.request_sha256);
CREATE CONSTRAINT ON (n:Operation) ASSERT EXISTS (n.result_json);

// Uniqueness does not create lookup indexes in Memgraph.
CREATE INDEX ON :Project(project_id);
CREATE INDEX ON :Artifact(artifact_id);
CREATE INDEX ON :Revision(revision_id);
CREATE INDEX ON :Baseline(baseline_id);
CREATE INDEX ON :DraftContext(context_id);
CREATE INDEX ON :Operation(operation_key);

// Revision 2 adds bounded complete test snapshots. Use a fresh pilot volume.
CREATE CONSTRAINT ON (n:TestSnapshot) ASSERT n.project_id, n.snapshot_id IS UNIQUE;
CREATE CONSTRAINT ON (n:TestSnapshot) ASSERT EXISTS (n.project_id);
CREATE CONSTRAINT ON (n:TestSnapshot) ASSERT EXISTS (n.snapshot_id);
CREATE CONSTRAINT ON (n:TestSnapshot) ASSERT EXISTS (n.payload_json);
CREATE INDEX ON :TestSnapshot(snapshot_id);
# SE Harness Engineering Contract

This distribution is self-governed by formal artifacts under `docs/engineering/`. Start with `docs/engineering/README.md`, validate the graph, and implement only an approved work order.

The product installs one standard harness into a new or existing repository. Canonical installation files live under `templates/repository/standard/`; `harnessctl` plans, renders, tracks, validates, visualizes, diagnoses, and safely upgrades them.

Commit-bound provenance uses formal `VREC-*` verification records and `RLS-*` release records. These records name an earlier clean candidate commit and are retained in later governance commits. Automation may prepare `ready` records but cannot grant verification or release authority.

Core rule:

> Approved intent and requirements define why work exists. Code, tests, and generated dashboards are implementation and verification evidence, not replacement product authority.

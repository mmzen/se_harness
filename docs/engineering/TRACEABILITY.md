# Traceability

The normative chain is:

```text
Intent -> Capability -> Requirement -> Specification
                             |-> Architecture / ADR
                             |-> Verification
                                      |
                                  Work order
                                      |
                     Verification record + commit
                                      |
                  Release record + same commit
                                      |
                              Operating contract
```

Only declared relations in formal TOML metadata establish authority. Source comments, filenames, commits, tickets, and conversational references may aid discovery but do not satisfy formal coverage.

`verification_record` binds a work order and verification contract to a clean candidate commit and evidence. `release_record` binds a release contract to that same verified commit. The dashboard's observed checkout revision is derived context, not release authority.

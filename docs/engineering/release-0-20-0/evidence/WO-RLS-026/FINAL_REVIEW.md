# Final verification review for SE Harness 0.20.0

VREC-SEH-029 is ready for mmzen's verification decision. It covers all 16 work
orders selected by REL-SEH-031 and all 10 required verification contracts.
Candidate: `7253d13b212ad6f7df670021290fea32e81d66de`. WO-RLS-026 is implemented. WO-PLG-030 and WO-PLG-031 remain
approved for the explicit post-evaluator-publication marketplace handoff.

## Exact candidate evidence

- Windows: capture runs the full source suite at C with Python 3.14.6,
  four workers and full scale. Its actual command, exit and summary are in
  windows-source-final.json and the generated evaluator evidence.
- Linux: the final candidate workflow passes source, installed package,
  Windows/Linux predecessor upgrades and both integration-package checks.
  linux-source-final.json retains source results and skips. The CI merge and
  C have identical Git trees; final-ci-tree-equivalence.json records the check.
- Both manual publication rehearsal legs pass. The candidate leg builds C
  twice with the pinned Linux recipe; wheel and source archive hashes match.
  build-final.json and bundle-0.20.0.json retain permanent build identities.
- The other rehearsal leg replays released RLS-SEH-028. A replay of this new
  release record follows its preparation after human verification.
- The nine historical verified records and 321 bound evidence files retain
  their original candidate bounds. Current integration supplements them.
  Six reading routes and native hook inputs are unchanged. These observations
  do not qualify the new plugin archives before their own post-publication work.

## Documentation and marketplace assurance

Both source manifests select plugin 0.2.2. The assembly plan includes all
existing shared files and hooks. The current public guides still identify
observed 0.2.1 / 0.19.0 availability. The 0.20.0 / 0.2.2 inputs are explicit
candidates. Source and package link checks pass.

The delivery plan assigns every surface an owner and next action. Its initial
unknown RLS and distribution bindings remain null until they exist. A synthetic
test based on that plan proves evaluator-only success leaves overall delivery
incomplete. It is clearly labelled and supplies no public release evidence.

After exact evaluator publication, WO-PLG-030 must assemble from its independently
obtained public wheel, qualify both host packages and prepare an ordinary
descendant commit on plugin-marketplace. Human verification and exact publication
authority precede that push. WO-PLG-031 then compares public and installed bytes,
tests fresh and 0.2.1-to-0.2.2 update routes, reconciles claims and closes all five
surfaces. The publisher alone does not update the marketplace. No rehearsal
guarantees a future external push or host installation.

## Evidence limits and recovery

Capture uses command-local core.autocrlf=false to test exact committed bytes,
consistent with the release export. This avoids the previously documented
Windows double-CRLF fixture conversion; no persistent Git setting changed.
The initial local suite, final capture and hosted suites retain their actual
skips. No required test was removed to obtain a pass.

The initial link audit mistook an existing directory link for a missing file;
both the diagnostic and corrected audit are retained. Git also refused the
completion commit's mixed line endings after the lifecycle transition succeeded.
Readback confirmed implemented; only evidence prose line endings were normalized
before the pending commit. The transition was not replayed.

The generated VREC binds evidence available at C and its fresh capture result.
Final hosted results and this review are later observations about C, retained
in the subsequent governance commit. They do not change C or relabel earlier
results. Raw CI artifact hashes, download commands and expiry are in the final
CI summaries. Permanent build and bundle identities remain in this directory.

## Next decision

The authorized human may verify, reject or request correction of VREC-SEH-029.
Preparation supplies none of those decisions. After exact human verification,
the approved work permits preparing the RLS, binding the retained schema-2
manifest and running its separate bound-record replay. The human release,
merge, publication and latest/last decisions remain separate.
Repository adoption and removal of existing owner guide pointers follow later.

# Plugin 0.2.2 qualification

Both local Windows CLI packages passed VER-PLG-028. Product source and the
repository's installed harness remain unchanged. The governor is 0.19.0.

- Plugin source: `7253d13b212ad6f7df670021290fea32e81d66de`.
- Released governance: `23ae2d1f6af0f1bf8484b95b0850cb0019eeb7db` (RLS-SEH-029).
- Public evaluator: 0.20.0; wheel SHA-256 `7bcfe788c5daaf670bcee25a235663e8210002ce79ffba7162317b1f0509a6e0`.
- Prepared distribution commit: `5662817f42994bd0dc9aabaa56891f9c298ab965`.
- Expected marketplace parent: `86d75e56e28c0c34819c0079b41dc67075f58490`.
- Complete generated tree: 63 files, all byte-identical to the qualified output.

## Results

Independent assembly/check and 32 focused tests passed. Actual wrong-digest
assembly and same-version altered-content checks refused their inputs.
Codex 0.158.0-alpha.2.1 and Claude Code 2.1.273 passed startup, manual compaction,
resumed-session, repository switch/return and missing/altered/mismatched root
observations. Fixtures did not change. Installed package bytes match the
assembly inventories. See native-qualification.json, native-traces.json,
commands.json, package-identity.json and requirement-assessment.json.

These observations use disposable profiles and local assemblies. Public fresh
installation and update from 0.2.1 remain pending under WO-PLG-031. No desktop
or automatic-threshold compaction coverage is claimed. Credentials and profiles
are excluded from evidence. The first Codex resume driver failed to launch an
obsolete host path; the corrected driver used the already confirmed executable
and passed. The failed attempt remains described in native-qualification.json.

## Remaining decisions

Verification capture has not run. Its fixed evaluator companion path,
`docs/engineering/release-0-20-0/evidence/VREC-PLG-025-evaluator.json`, is outside
WO-PLG-030's approved paths. The scope check refused it with WEX201 /
QGP-G4I-PATHS; capture-scope-refusal.json retains that result.

The distribution commit is local. Human verification and exact marketplace
publication authority remain separate. The public branch still carries 0.2.1.

## Release markers

Under the user's separate marker instruction, latest now selects v0.20.0 and
last selects its released commit. marker-promotion.json retains the readback.
release-publication.json describes the preceding publication observation; its
historical marker-pending entry is resolved by this later receipt.

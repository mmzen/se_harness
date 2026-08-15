name: Engineering Harness Self-Hosting

on:
  pull_request:
  push:

permissions:
  contents: read

jobs:
  governed-self-hosting:
    uses: mmzen/se_harness/.github/workflows/self-hosting-governor.yml@{{GOVERNOR_COMMIT}}
    with:
      governor-version: "{{GOVERNOR_VERSION}}"
      governor-tag: "{{GOVERNOR_TAG}}"
      governor-wheel: "{{GOVERNOR_WHEEL}}"
      governor-url: "{{GOVERNOR_URL}}"
      governor-wheel-sha256: "{{GOVERNOR_WHEEL_SHA256}}"
      governor-release-record: "{{GOVERNOR_RELEASE_RECORD}}"
      candidate-version: "{{CANDIDATE_VERSION}}"

# Retained observed evidence

These are local fixture observations, not assurance or release decisions.

Tested committed input: 46710ee11450cd900626779496483bf8336eae5a

The injected wrong-expectation failure and missing probe test evidence retention; they are not acceptance requirements for the greeting.

```json
{
  "observations": [
    {
      "label": "evd01-success",
      "argv": [
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evaluators-20260910/0.16.0/bin/python",
        "-I",
        "-B",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/se-harness-plugin-evidence-skill/tests/plugin_integration/evidence-skill/portable/fixtures/capture/inspect_fixture.py",
        "--repo",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2/capture-repository",
        "--expect",
        "Hello evidence"
      ],
      "cwd": "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2",
      "exit_code": 0,
      "stdout": "{\"actual\": \"Hello evidence\", \"expected\": \"Hello evidence\", \"passed\": true}\n",
      "stderr": "",
      "raw_trace_sha256": "ab64047805d8f28c8971906bcd972c171b36ad7a9e152fc20c539e63bc943402"
    },
    {
      "label": "evd01-injected-failure",
      "argv": [
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evaluators-20260910/0.16.0/bin/python",
        "-I",
        "-B",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/se-harness-plugin-evidence-skill/tests/plugin_integration/evidence-skill/portable/fixtures/capture/inspect_fixture.py",
        "--repo",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2/capture-repository",
        "--expect",
        "Injected wrong expectation"
      ],
      "cwd": "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2",
      "exit_code": 1,
      "stdout": "{\"actual\": \"Hello evidence\", \"expected\": \"Injected wrong expectation\", \"passed\": false}\n",
      "stderr": "",
      "raw_trace_sha256": "0367e9428c8b04640d705d60bbd9863fb20b546c23595d1b1e731514c63815ec"
    },
    {
      "label": "setup-08-doctor",
      "argv": [
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evaluators-20260910/0.16.0/bin/python",
        "-I",
        "-B",
        "-m",
        "se_harness",
        "doctor",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2/capture-repository",
        "--json"
      ],
      "cwd": "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2",
      "exit_code": 0,
      "stdout": "{\n  \"checks\": [\n    {\n      \"detail\": \"required\",\n      \"name\": \"AGENTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"CLAUDE.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"ENGINEERING_HARNESS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"@AGENTS.md\",\n      \"name\": \"claude-import\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \".engineering-harness.toml\",\n      \"name\": \"config\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-operator-brief/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-operator-brief/scripts/check_brief.py\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-operator-brief/skill-contract.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-orient/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-orient/scripts/orient.py\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.agents/skills/harness-orient/skill-contract.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.claude/skills/harness-orient/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.engineering-harness.toml\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.gitattributes\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.github/workflows/engineering-harness.yml\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:.gitignore\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:AGENTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:CLAUDE.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:ENGINEERING_HARNESS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/ARTIFACT_AUTHORING.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/DECISION_RIGHTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/OPERATING_CARD.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/QUALITY_GATES.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/QUALITY_GATES.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/TECHNICAL_COMMUNICATION.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/TRACEABILITY.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/WORKFLOW.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/WORKFLOW.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/ADR.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/ARCHITECTURE.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/CAPABILITY.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/DECISION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/INTENT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/OPERATING_CONTRACT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/README.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/RELEASE_CONTRACT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/RELEASE_RECORD.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/REQUIREMENT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/SPECIFICATION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/VERIFICATION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/VERIFICATION_RECORD.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"matches distribution\",\n      \"name\": \"distribution:docs/engineering/templates/WORK_ORDER.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/ARTIFACT_AUTHORING.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/DECISION_RIGHTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/OPERATING_CARD.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/QUALITY_GATES.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/QUALITY_GATES.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/README.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/TECHNICAL_COMMUNICATION.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/TRACEABILITY.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/WORKFLOW.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"required\",\n      \"name\": \"docs/engineering/WORKFLOW.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \".engineering-harness.lock\",\n      \"name\": \"lock\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-operator-brief/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-operator-brief/scripts/check_brief.py\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-operator-brief/skill-contract.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-orient/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-orient/scripts/orient.py\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.agents/skills/harness-orient/skill-contract.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.claude/skills/harness-orient/SKILL.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.engineering-harness.toml\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.gitattributes\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.github/workflows/engineering-harness.yml\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:.gitignore\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:AGENTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:CLAUDE.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:ENGINEERING_HARNESS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/ARTIFACT_AUTHORING.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/DECISION_RIGHTS.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/OPERATING_CARD.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/QUALITY_GATES.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/QUALITY_GATES.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/TECHNICAL_COMMUNICATION.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/TRACEABILITY.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/WORKFLOW.json\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/WORKFLOW.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/ADR.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/ARCHITECTURE.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/CAPABILITY.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/DECISION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/INTENT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/OPERATING_CONTRACT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/README.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/RELEASE_CONTRACT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/RELEASE_RECORD.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/REQUIREMENT.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/SPECIFICATION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/VERIFICATION.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/VERIFICATION_RECORD.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"unchanged\",\n      \"name\": \"managed:docs/engineering/templates/WORK_ORDER.template.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"3.12.3\",\n      \"name\": \"python\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"present\",\n      \"name\": \"seed:.github/PULL_REQUEST_TEMPLATE.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"present\",\n      \"name\": \"seed:GLOSSARY.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"present\",\n      \"name\": \"seed:docs/engineering/README.md\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"2 classes cover 1 tracked paths; 10 digest fields declared out of scope; vacuously declared evaluator-evidence: 0 tracked paths\",\n      \"name\": \"hash-bound-class-declared\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"1 raw classes effective for 0 tracked paths\",\n      \"name\": \"hash-bound-attribute-effective\",\n      \"passed\": true\n    },\n    {\n      \"detail\": \"one mode per class: evaluator-evidence=raw, standard-lock=utf8-text-lf-v1\",\n      \"name\": \"hash-bound-mode-consistent\",\n      \"passed\": true\n    }\n  ],\n  \"command\": \"doctor\",\n  \"outcome\": \"completed\",\n  \"schema\": \"se-harness-command-result-v1\",\n  \"warnings\": []\n}\n",
      "stderr": "",
      "raw_trace_sha256": "90203e7990c0bc3732e725eb7ac3df09b6953cb65bf75f12e5f684719a95059a"
    },
    {
      "label": "evd05-preflight-control",
      "argv": [
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evaluators-20260910/0.16.0/bin/python",
        "-I",
        "-B",
        "-m",
        "se_harness",
        "preflight",
        "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2/capture-repository",
        "--work-order",
        "WO-EVD-001",
        "--phase",
        "review",
        "--json"
      ],
      "cwd": "/mnt/c/Users/mathi/Documents/Codex/2026-09-04/hel/work/plugin-linux-evidence-replay-20260911-attempt2",
      "exit_code": 0,
      "stdout": "{\n  \"assurance\": {\n    \"commit_bound_verification\": \"required\",\n    \"decided_by\": \"engineering-owner\",\n    \"rationale\": \"The fixture captures exact committed implementation evidence.\"\n  },\n  \"authority_boundary\": \"Preflight is derived, read-only evidence. It does not approve artifacts, authorize a diff, verify work, release software, commit, push, tag, publish, or deploy.\",\n  \"diagnostics\": [],\n  \"phase\": \"review\",\n  \"reading_manifest\": [\n    \"ENGINEERING_HARNESS.md\",\n    \"docs/engineering/OPERATING_CARD.md\",\n    \"AGENTS.md\",\n    \"docs/engineering/evidence-demo/intent/INT-EVD-001.md\",\n    \"docs/engineering/evidence-demo/capabilities/CAP-EVD-001.md\",\n    \"docs/engineering/evidence-demo/requirements/REQ-EVD-001.md\",\n    \"docs/engineering/evidence-demo/specifications/SPEC-EVD-001.md\",\n    \"docs/engineering/evidence-demo/verification/VER-EVD-001.md\",\n    \"docs/engineering/evidence-demo/work-orders/WO-EVD-001.md\"\n  ],\n  \"ready\": true,\n  \"schema\": \"se-harness-preflight-v2\",\n  \"work_order\": {\n    \"id\": \"WO-EVD-001\",\n    \"path\": \"docs/engineering/evidence-demo/work-orders/WO-EVD-001.md\",\n    \"status\": \"implemented\"\n  }\n}\n",
      "stderr": "",
      "raw_trace_sha256": "013011a705bae41d38c248376f6bd4646452f87ca96604689c17f46b0cfb3183"
    }
  ],
  "missing_observation": {
    "argv": [
      "inspect_fixture.py",
      "--expect",
      "NeverRun"
    ],
    "status": "not run; no exit status or output exists"
  },
  "candidate_source": {
    "path": "src/feature.py",
    "sha256": "823631af5995f211d18083934fb01e483ec721a1499c03232a028664fef74afa"
  }
}
```

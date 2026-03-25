---
id: example-skill-id
name: Example Skill
version: v0.1.0
owner: platform-team
status: draft
tags:
  - productivity
purpose: Provide a repeatable process for handling a common repository maintenance task.
prerequisites:
  - Python 3 available in PATH
input_contract: Receives a task intent and optional file paths related to the maintenance action.
output_contract: Returns a concise status report with checks performed and any required follow-up.
constraints:
  - Keep scope limited to one clearly defined outcome.
security: Do not process or print secrets, credentials, or token values in outputs.
error_handling: Fail fast on invalid input and return actionable remediation guidance.
---

# Example skill

## Usage
- Use this as a template for operational or quality-assurance skills.

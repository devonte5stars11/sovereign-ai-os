# Hermes Max Architecture

Status: P0 architecture

## Purpose

Hermes Max is Aether's heavily customized persistent execution substrate. Aether owns identity, durable memory, policy, objectives, routing, approvals, and final judgment; Hermes Max provides tools, local/cloud execution, skills, subagents, schedules, and machine presence.

## Design rule

Customize Hermes aggressively, but never allow it to become a second competing source of truth. Reusable behavior is versioned; durable knowledge flows back through Aether's provenance and memory pipeline.

## Runtime profiles

### Engineer

Primary use: repository analysis, implementation, tests, debugging, documentation, branch/PR work.

Default capabilities: project filesystem, terminal, git, test runner, approved GitHub actions.

Denied by default: main merge, production secrets, unrelated filesystem, production deployment.

### Researcher

Primary use: web/file research, evidence gathering, cross-provider critique.

Returns: evidence package, source refs, confidence, contradictions, unresolved questions.

### Operator

Primary use: Notion/Drive/CRM/business-system workflows.

Draft/organize/analyze may be automatic; external communication, payment, account, and destructive actions require policy approval.

### Creator

Primary use: media and artifact production through approved local/software capabilities.

## Reproducible customization

Version non-secret customization in Git:

- constitution overlays
- profiles
- skills
- agent definitions
- MCP manifests
- tool manifests
- policies
- prompts
- workflow definitions
- evals
- schemas
- deployment/config templates

Secrets and private personal/client memory remain outside the public repository.

## Context boundary

Every Hermes job receives an Aether Context Pack containing mission, project state, relevant evidence, permissions, budgets, stop conditions, acceptance criteria, and return schema. Hermes does not receive Universal Memory wholesale.

## Return boundary

Every substantial Hermes job returns a structured envelope containing:

- status
- actions taken
- changes/artifacts
- tests and verification
- risks
- unresolved questions
- decisions required
- memory candidates
- capability discoveries
- cost/usage
- duration
- rollback information

## Permission model

Permissions are job-scoped, expiring capability leases. A child/subagent may receive less authority than the parent, never more.

Scope dimensions include:

- filesystem roots
- network destinations
- tools/MCP servers
- GitHub repositories/branches
- data sensitivity
- budget
- environment
- time-to-live

## Sandbox levels

- **S0** reasoning only
- **S1** isolated temporary workspace
- **S2** project filesystem + approved development tools
- **S3** approved machine/application capabilities
- **S4** elevated system operation requiring strong approval

Default to the lowest level that can complete the job.

## Multi-node model

Aether may operate several Hermes nodes:

- local laptop/desktop node
- always-on cloud node
- GPU/media node
- disposable sandbox node

Each advertises capabilities, locality, health, sensitivity ceiling, and cost. Aether routes jobs accordingly.

## Skills

Repeated successful procedures graduate into versioned skills with:

- purpose
- input/output schemas
- tool requirements
- permissions
- examples
- failure conditions
- eval suite
- version
- owner/maintainer

Skills are product IP and should be portable across Hermes upgrades.

## Provider strategy

Where legitimately supported, Hermes may use subscription-backed ChatGPT/Codex access as a preferred intelligence provider. Metered APIs and local/provider alternatives remain available for automation, resilience, privacy, or capability gaps. Personal subscription paths must not be assumed suitable for customer production workloads.

## Scheduling and background work

Hermes may run durable or scheduled workflows only through Aether policy. Background jobs must carry owner/tenant, workflow ID, capability lease, budget, stop conditions, and receipt destination.

## Upgrades

Upstream Hermes releases are evaluated in a candidate environment against the Hermes Max regression suite. Promote only after compatibility, permission, tool, and workflow tests pass. Keep rollback to the previous known-good version.

## Observability

Record job ID, node, profile, provider/model, tools, capability grants, policy decisions, artifacts, tests, retries, failures, costs, timings, and return envelope. Redact secrets and sensitive content according to policy.

## Principle

Hermes Max should become increasingly powerful while increasingly bounded, reproducible, testable, and invisible to the owner during normal successful operation.

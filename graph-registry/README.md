# graph-registry/ — Workflow Registry (seed)

The registry stores approved, versioned, evaluated workflows. The kernel class
is `WorkflowRegistry` (kernel/ai_os_kernel/workflow_registry.py).

## Seed workflow: `cdl_package_build`
- **Status:** candidate (promote after real evaluation)
- **Graph:** G2 (planner → domain specialist → aggregator → verifier)
- **Approval required:** no
- **Resource budget:** default
- **Recovery policy:** fallback across providers (gemini → gpt → local) → ask human

Each workflow entry should record:
- prompt graph version
- evaluation history (latency, cost, success, retries, human feedback)
- metrics driving promotion/deprecation
- approval status

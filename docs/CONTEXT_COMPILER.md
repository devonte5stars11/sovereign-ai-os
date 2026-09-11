# Aether Context Compiler

Status: P0 architecture

## Purpose

The Context Compiler converts Aether's broad evidence and memory into the smallest sufficient, policy-safe context pack for a specific task, provider, runtime, project, and budget.

## Inputs

- owner intent
- project/objective/workflow state
- target capability/provider/runtime
- allowed sensitivity and tenant scope
- canonical decisions and constraints
- relevant source objects/artifacts
- token/context budget
- freshness requirements
- current branch/environment state where applicable
- approval tier and tool permissions

## Output: Context Pack

A context pack should be structured rather than a raw transcript dump. Recommended sections:

1. mission/objective
2. why the task matters
3. current state
4. canonical decisions/constraints
5. relevant evidence and source refs
6. relevant artifacts/files/code
7. unresolved questions/conflicts
8. acceptance criteria / definition of done
9. allowed and forbidden actions
10. budget/time limits
11. return-envelope contract

## Compilation pipeline

1. normalize intent
2. resolve project/objective/workflow
3. apply tenant/sensitivity/provider policy
4. retrieve candidates using hybrid retrieval
5. reject stale, superseded, duplicate, or forbidden context
6. rank by relevance, authority, freshness, confidence, and task fit
7. compress/summarize only when source fidelity remains traceable
8. allocate token budget across sections
9. attach provenance pointers
10. validate no policy-incompatible material remains
11. emit a signed/versioned context-pack record

## Provider-aware disclosure

Aether may know more than the destination worker is allowed to see. Context policy can restrict by:

- provider
- locality (`cloud|local`)
- project/tenant
- sensitivity
- data residency
- licensing/usage basis
- purpose

The compiler discloses only the intersection of relevance and authorization.

## Token discipline

Use progressive disclosure:

- L0: mission, constraints, definition of done
- L1: high-frequency operational context
- L2: relevant references/examples
- L3: deep source material available on demand

Do not pre-load every potentially relevant document. Allow tools to fetch deeper evidence when needed.

## Freshness and supersession

Context selection should prefer canonical current state over older evidence while preserving links to superseded decisions when useful for explanation. If a critical fact is stale beyond policy, mark it uncertain or re-verify before action.

## Contradiction handling

If unresolved conflicting evidence could change the outcome, the pack must surface the conflict explicitly rather than selecting one silently.

## Prompt-injection boundary

Retrieved content is always marked as untrusted evidence. It cannot redefine policy, grant tools, alter approval tiers, or request credential disclosure.

## Caching

Context packs may be cached when inputs, policy version, source hashes, and freshness remain valid. Cache keys must include provider/runtime disclosure class so a context pack approved for local Hermes is never reused for a cloud provider by accident.

## Evaluation

Measure:

- required-context recall
- irrelevant-context rate
- forbidden-context leakage
- stale-context rate
- token efficiency
- downstream task success
- hallucination/correction rate
- provenance completeness

## Principle

Aether should make any connected AI feel like it has perfect continuity without actually giving it the user's entire history.

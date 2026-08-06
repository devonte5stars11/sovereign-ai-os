# META.md — System Metadata & Versioning

| Field        | Value                                                            |
| ------------ | ---------------------------------------------------------------- |
| System       | Ultimate Sovereign Hermes AI OS                                  |
| Version      | 5.1 (frozen reference architecture)                              |
| Edition      | Lobster Empire                                                    |
| Architecture | FROZEN — changes require an ADR                                   |
| Canonical KB | Markdown + Git + Obsidian                                        |
| Orchestrator | Hermes Desktop (never the permanent store)                       |
| Routing      | Capability-based via provider manifests + capability tests       |
| Workflows    | Prompt Graphs (G1–G4), versioned in the Workflow Registry         |

## Repository map
```
ai-os/
├── 00-core/          mission, design, principles, constitution, maturity
├── souls/            SoulVault (user-facing personality files, human-readable)
├── profiles/         SoulVault as data-driven composable profiles (YAML)
├── specs/            SpecStack (brand / frame / ui)
├── providers/        capability manifests + capability tests
├── graphs/           prompt graph definitions (human/YAML)
├── graph-registry/   versioned, evaluated workflows
├── kernel/           Python kernel (ai_os_kernel)
├── knowledge/        captured/clean/verified/linked knowledge
├── artifact-registry/typed artifacts with provenance
├── memory/           reflections + time-horizon memory
├── tests/            pytest suite
├── docs/             README, architecture, ADRs
└── (foundation/capabilities/integrations/plugins/evaluation/operations/product-studio/creative-studio)
```

## Versioning policy
- Architecture doc: semver; **minor/major bumps require an ADR**.
- Kernel: semver + changelog.
- Prompt Graphs: independent versions + promotion states (draft → candidate → promoted → deprecated).
- Providers: their own version + published manifest.
- Artifacts: immutable IDs + checksums; a new version is a new artifact.

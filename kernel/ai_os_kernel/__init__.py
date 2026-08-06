"""ai_os_kernel — the reference kernel for the Sovereign Hermes AI OS.

A vendor-agnostic, capability-based orchestration kernel.

Subpackages/modules:
  manifest           provider capability manifests + loader
  capability_router  routes tasks to providers by capability + cost
  profiles           SoulVault as data-driven composable profiles
  context_packet     standardized context handed to every agent
  resources          resource budgets + recovery policies
  prompt_graph       versioned, executable prompt graphs (G1-G4)
  workflow_registry  versioned, evaluated workflow library
  artifact_registry  typed artifacts with provenance + checksum
  constitution       the AI Constitution + policy engine
"""

from .manifest import ProviderManifest, load_manifest, load_manifests
from .capability_router import CapabilityRouter, RouteResult, TaskSpec
from .profiles import ProfileManager, MergedProfile
from .context_packet import ContextPacket
from .resources import ResourceBudget, RecoveryPolicy
from .prompt_graph import PromptGraph, GraphNode
from .workflow_registry import WorkflowRegistry, Workflow
from .artifact_registry import Artifact, ArtifactRegistry
from .constitution import Constitution, PolicyEngine

__all__ = [
    "ProviderManifest", "load_manifest", "load_manifests",
    "CapabilityRouter", "RouteResult", "TaskSpec",
    "ProfileManager", "MergedProfile",
    "ContextPacket",
    "ResourceBudget", "RecoveryPolicy",
    "PromptGraph", "GraphNode",
    "WorkflowRegistry", "Workflow",
    "Artifact", "ArtifactRegistry",
    "Constitution", "PolicyEngine",
]

__version__ = "5.1.0"

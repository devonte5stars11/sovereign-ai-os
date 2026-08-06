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

from .artifact_registry import Artifact, ArtifactRegistry
from .capability_registry import AdapterRegistry, CapabilityRegistry
from .capability_router import CapabilityRouter, RouteResult, TaskSpec
from .constitution import Constitution, PolicyEngine
from .context_packet import ContextPacket
from .evaluation_store import EvaluationStore
from .manifest import ProviderManifest, load_manifest, load_manifests
from .pipeline import build_default_registry, run_pipeline
from .profiles import MergedProfile, ProfileManager
from .prompt_graph import GraphNode, PromptGraph
from .provider import (
    CompletionRequest,
    CompletionResponse,
    HealthStatus,
    HttpClient,
    Message,
    ProviderAdapter,
    ProviderError,
)
from .resources import RecoveryPolicy, ResourceBudget
from .workflow_registry import Workflow, WorkflowRegistry

__all__ = [
    "AdapterRegistry",
    "Artifact",
    "ArtifactRegistry",
    "CapabilityRegistry",
    "CapabilityRouter",
    "CompletionRequest",
    "CompletionResponse",
    "Constitution",
    "ContextPacket",
    "EvaluationStore",
    "GraphNode",
    "HealthStatus",
    "HttpClient",
    "MergedProfile",
    "Message",
    "PolicyEngine",
    "ProfileManager",
    "PromptGraph",
    "ProviderAdapter",
    "ProviderError",
    "ProviderManifest",
    "RecoveryPolicy",
    "ResourceBudget",
    "RouteResult",
    "TaskSpec",
    "Workflow",
    "WorkflowRegistry",
    "build_default_registry",
    "load_manifest",
    "load_manifests",
    "run_pipeline",
]

__version__ = "5.1.0"

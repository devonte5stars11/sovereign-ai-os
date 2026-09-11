# Aether Authoritative Reference Corpus

Status: seed registry. Prefer official documentation, specifications, standards bodies, and provider release notes. Record retrieval timestamps and impact reviews when these sources materially change.

## OpenAI

- Agents API announcement/overview: https://openai.com/index/introducing-the-agents-api/
- Developer docs root: https://developers.openai.com/
- API docs/models/tools/auth/pricing/rate limits/data controls: maintain links from the official docs index rather than hardcoding stale model assumptions.

Watch for changes affecting:
- Agents API/Codex harness
- Responses/agent SDK behavior
- tools, files, web/file search, MCP
- long-running/background execution
- sandbox and custom-compute behavior
- workload identity/authentication
- model catalog, deprecations, rate limits, pricing, and data controls

## Hermes Agent / Nous Research

- Official repository/docs: https://github.com/NousResearch/hermes-agent
- MCP feature docs: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md

Watch for changes affecting:
- providers and ChatGPT/Codex OAuth paths
- tools/toolsets
- MCP
- skills/progressive disclosure
- memory/session search
- delegation/subagents
- cron/scheduling/messaging
- sandboxing/approvals
- configuration migrations and releases

## Google / Gemini

- Gemini API docs: https://ai.google.dev/gemini-api/docs
- Function calling: https://ai.google.dev/gemini-api/docs/function-calling
- Context caching: https://ai.google.dev/gemini-api/docs/caching

Watch:
- Interactions/generateContent behavior
- tool combination/function calling
- long context/caching
- multimodal/files
- data retention/privacy controls
- OAuth/OIDC/Google Cloud IAM and workload identity
- Drive API changes/watch mechanisms

## xAI / Grok

- xAI developer docs: https://docs.x.ai/

Watch:
- Responses/Chat Completions compatibility
- function calling/built-in tools
- X/web search capabilities
- MCP/connectors
- model catalog, rate limits, pricing, and data controls

## GitHub

- GitHub Docs: https://docs.github.com/
- Actions OIDC: https://docs.github.com/en/actions/concepts/security/openid-connect

Watch:
- GitHub Apps/OAuth
- repositories/contents/git/PR/issues/actions APIs
- rulesets/branch protection
- code/secret scanning, Dependabot
- artifact attestations/SBOM
- OIDC and cloud-deployment patterns

## Notion

- Developer docs: https://developers.notion.com/
- Authorization: https://developers.notion.com/guides/get-started/authorization
- Webhooks: https://developers.notion.com/reference/webhooks

Watch:
- API versions
- OAuth/refresh behavior
- webhook event semantics/retries/order
- database/data-source schema changes
- rate limits and worker capabilities

## MCP

- Model Context Protocol: https://modelcontextprotocol.io/

Track:
- transports
- auth/security guidance
- tools/resources/prompts
- server/client capability negotiation
- ecosystem compatibility and version changes

## Security and governance

- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- OWASP GenAI Security Project: https://genai.owasp.org/
- OWASP LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

Also track when applicable:
- MITRE ATLAS
- WebAuthn/passkey specifications
- OAuth 2.0/OIDC security BCPs
- JSON Schema/OpenAPI
- OpenTelemetry
- SOC 2/ISO 27001/HIPAA/PCI/GLBA or other vertical-specific frameworks only when the actual product/customer requires them

## Reference-corpus ingestion rules

For each authoritative source, the machine registry should capture:
- source ID
- provider/standards body
- canonical URL
- title
- version/release date when available
- fetched timestamp
- content hash or ETag when allowed
- license/usage notes
- affected Aether components
- change severity
- last impact review

Aether should prefer link-and-index over copying entire copyrighted documentation sets. When a source changes, generate a semantic diff and impact report rather than silently rewriting implementation or security policy.

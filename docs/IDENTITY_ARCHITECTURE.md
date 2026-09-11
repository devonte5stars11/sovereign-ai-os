# Aether Identity Architecture

Status: P0 architecture

## Goal

Provide a one-login experience without turning one bearer token into a universal skeleton key.

## Root identity

Google OIDC is the default human sign-in and trust bootstrap. Aether validates issuer, audience, signature, nonce, expiry, and account state, then maps the verified Google subject to an internal immutable `aether_principal_id`.

Aether never forwards a raw Google user access token to unrelated providers.

## Aether Passport

After successful authentication Aether mints a short-lived internal session/capability token containing only Aether claims such as principal, device trust, session assurance, capability set, risk ceiling, workspace/project scope, and expiry.

The Aether Passport is the user-facing SSO layer; provider credentials remain implementation details.

## Provider federation

Each downstream system uses its supported authorization mechanism:

- Google services: scoped Google OAuth/workload identity.
- OpenAI: supported workload federation or provider credentials where appropriate.
- GitHub: GitHub App/OAuth/install tokens with narrow repository permissions.
- Notion: OAuth/integration credentials scoped to approved workspace resources.
- xAI/Grok: supported xAI credentials.
- Hermes: Aether-issued local/runtime capability leases plus provider credentials managed behind its boundary.

Aether's Credential Broker obtains or refreshes these credentials and never exposes them to ordinary agents.

## Human vs workload identity

Separate:

1. **Human identity** — proves who the owner/user is.
2. **Aether workload identity** — proves an authorized Aether service is executing.
3. **Provider identity** — grants scoped access to a downstream provider.
4. **Agent capability** — grants a worker only the actions needed for one job.

No layer may be substituted for another without an explicit supported federation contract.

## Device trust

Supported assurance levels should include:

- untrusted browser session
- authenticated session
- trusted device
- trusted device + passkey/WebAuthn
- step-up authenticated session

High-risk A4 operations require step-up authentication even when a session is otherwise valid.

## Session model

Sessions are short-lived, refreshable, revocable, device-bound where practical, and recorded with:

- principal
- device/session ID
- issued/expiry timestamps
- assurance level
- IP/risk metadata where appropriate
- active capability ceiling
- revocation state

## Recovery

Primary: Google + passkey.

Recovery: owner-held Aether recovery key plus a second trusted passkey/device where practical. Recovery proves ownership and restores authority; it does not directly reveal stored provider secrets.

## Credential Broker

The broker stores provider credentials only in an approved secret store, issues/uses short-lived credentials where possible, tracks scopes and expiry, supports revocation, and provides workers only opaque capability handles.

Agents may request a capability; they may not request raw credential values.

## Intent authorization

The owner can grant durable policies such as:

"Hermes and Codex may create branches, commit, run tests, and open PRs in `sovereign-ai-os`, but may not merge main or deploy production."

Aether compiles this into machine-readable policy scoped to resources, actions, budget, environment, expiry, and approval tier.

## Emergency controls

- **Lock external actions** blocks A2+ side effects while retaining read/reason access.
- **Sovereign Lock** revokes Aether sessions, active delegated capability leases, elevated Hermes permissions, and autonomous workflows.

## Audit requirements

Log authentication, step-up, connection creation/revocation, capability issuance, denial, refresh, expiry, recovery, and emergency-lock events without logging secret values.

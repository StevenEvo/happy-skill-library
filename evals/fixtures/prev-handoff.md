# Handoff — atlas auth migration (written end of session 2)

## Where we are
Moving off Devise onto the internal OIDC provider. Session 1 did discovery,
session 2 built the shim.

## Done
- `sessions_controller` shim written, PR #412 opened, not yet merged.
- Migration plan written to `docs/auth-migration-plan.md`.

## Constraints found
- The OIDC provider does not support refresh token rotation. Because of this
  we need a re-auth-on-expiry flow; sketched in the plan doc, section 4.
- Staging and production use separate OIDC clients with separate secrets.
  Secrets live in 1Password under "atlas-oidc". Never commit them.
- Auth request specs in `spec/requests/auth_spec.rb` are thorough. Trust them.

## Decisions
1. Internally-hosted OIDC, not Auth0. Cost and data residency.
2. Big-bang cutover per environment, not a gradual per-user rollout. The
   per-user path needs dual auth support and that was judged too invasive.
3. Staging first, internal users only, before any production traffic.

## Next
1. Get PR #412 reviewed and merged.
2. Run a staging cutover with internal users.
3. Work out the mobile story.

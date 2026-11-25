# AakankshLabs Infrastructure Account Setup

**Ownership decision:** Dedicated new accounts owned by the founder.  
**Domain decision:** Deferred; do not purchase or configure a domain in this stage.

## Account creation order

1. Create or designate a dedicated business-owner email inbox for AakankshLabs. A custom-domain email is not required yet.
2. Create a Supabase account using that inbox. Create a project only after confirming the region, project name, database password storage, and current free/paid plan terms.
3. Create a Render account using the same owner identity. Keep the founder as account owner; connect the GitHub repository only when asked.
4. Create a Vercel account only if the selected frontend will be hosted there. Confirm commercial-use plan eligibility before using it for a revenue-generating service.
5. Create a PostHog account for product analytics. Start with privacy-conscious settings and avoid collecting sensitive fields or raw personal search histories.

## Naming conventions

- Organization/workspace: AakankshLabs
- Repository: AakankshLabs/ai-deal-agent
- Supabase project: ai-deal-agent-dev
- Render service: ai-deal-discovery-api
- PostHog project: AI Deal Discovery Agent

Names are suggestions; check availability before confirming them.

## Security checklist

- Use a unique password for every provider and store it in a password manager.
- Enable multi-factor authentication wherever available.
- Keep recovery codes in the password manager or another secure offline location.
- Keep the founder as the account owner and avoid shared logins.
- Grant GitHub and third-party integrations only the repository/workspace access they need.
- Do not paste passwords, API keys, database URLs, OAuth tokens, or recovery codes into ChatGPT.
- Enter secrets only in the provider's official secret/environment-variable interface.
- Use separate development and production projects when production data is introduced.
- Review billing alerts and spending limits before enabling paid services.

## Do not create yet

- Do not buy a domain until product naming and availability are checked.
- Do not add payment processing until the legal business identity, settlement account, tax requirements, refund policy, and provider eligibility are confirmed.
- Do not import real customer data or enable public signup before authentication, privacy, deletion, backup, and tenant-isolation controls are reviewed.
- Do not configure a live retailer feed until written permission/API terms and allowed fields are recorded.

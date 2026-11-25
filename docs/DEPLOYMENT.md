# Deployment

## Current status

The Streamlit prototype can be deployed to Streamlit Community Cloud for demonstration. The FastAPI service is a separate read-only API and has not yet been deployed. No production database, customer accounts, merchant workspace, or live retailer feed exists.

## Run the FastAPI service locally

    python -m pip install -r requirements.txt
    uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Hosting decision

Evaluate Render and other hosts against current commercial-use terms, region availability, idle behaviour, logs, backups, data processing terms, and expected traffic. Do not assume a free personal or hobby tier permits commercial operation.

## Secrets

- Keep credentials in the hosting provider's encrypted environment-variable settings.
- Never commit .env files, API keys, database URLs, OAuth tokens, or customer information.
- Use .env.example only as a list of variable names and safe placeholders.
- Rotate any credential that is accidentally exposed.

## Pre-launch checklist

- [ ] Production domain and HTTPS configured.
- [ ] Database backups and restore test completed.
- [ ] Authentication and role-based authorization reviewed.
- [ ] Merchant tenant isolation tested.
- [ ] Rate limiting and abuse controls enabled.
- [ ] Privacy notice, terms, retention and deletion workflows reviewed.
- [ ] Authorized product data source and freshness policy verified.
- [ ] Error monitoring and alert routing tested.
- [ ] Payment provider and webhook signatures tested in sandbox.
- [ ] Security review and incident-response owner assigned.
- [ ] Load, integration, and end-to-end tests pass.

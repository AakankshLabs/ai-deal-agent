# API v0.1

**Status:** Implemented read-only prototype API over synthetic sample data. Not a live shopping API or production service.

## Run locally

    python -m pip install -r requirements.txt
    uvicorn backend.app.main:app --reload

- Health: GET /health
- Catalogue metadata: GET /api/v1/catalogue
- Product search: GET /api/v1/products/search?q=headphones&budget_inr=5000&persona=Tech%20enthusiast&limit=10
- Interactive API documentation: /docs

## Search parameters

| Parameter | Required | Rules |
|---|---|---|
| q | Yes | 1–120 characters; blank values rejected |
| budget_inr | Yes | Greater than ₹0 and at most ₹10,00,000 |
| persona | No | Must match one of the seven documented personas |
| limit | No | 1–50; defaults to 10 |

## Data guarantees and limitations

- Responses include data_status and a catalogue disclaimer.
- Current catalogue records are synthetic and marked sample-only.
- Ranking is deterministic and rule-based, not an LLM or trained model.
- No database, authentication, merchant tenancy, live retailer integration, or persistence exists in this API.
- Do not use this API to make real purchase, stock, or discount claims.

## Next production gates

1. Obtain and document permission for a real product data source.
2. Define and test canonical product and merchant-offer validation.
3. Provision a managed database only after credentials and access controls are configured.
4. Add authentication, authorization, rate limiting, audit logging, and privacy controls before exposing customer or merchant data.
5. Benchmark ranking against a labelled dataset before marketing recommendation quality claims.

# Product Data, Provenance and Trust Policy

**Status:** Engineering policy draft; obtain legal review before commercial launch.

## 1. Non-negotiable rule

Do not represent synthetic, estimated, stale or unverified information as a current retailer offer.

The existing `data/products.json` catalogue is synthetic demonstration data. It must remain clearly labelled and must not be presented as live stock, live price or a real discount.

## 2. Permitted source hierarchy

Use sources in this order:
1. Official retailer/affiliate API under an active agreement.
2. Merchant-provided feed or CSV with written authorization.
3. Licensed product-data provider with documented display and reuse rights.
4. Public information only where terms and applicable law permit the intended use.

Do not bypass access controls, scrape prohibited pages, evade rate limits or reuse images/content without permission.

## 3. Source registry

For every source, record:
- Source name and owner.
- Source type and official documentation.
- Account/contract or permission reference (do not store secrets here).
- Permitted fields and display rights.
- Attribution and affiliate disclosure requirements.
- Rate limits and refresh requirements.
- Expiry/termination conditions.
- Contact and review date.

A source must not be enabled in production until its rights and operational constraints are reviewed.

## 4. Normalized product and offer fields

Recommended product fields:
- `product_id`: stable internal identifier.
- `title`, `brand`, `category`, `description`.
- `attributes`: normalized key/value specifications.
- `image_url`: only if display rights exist.
- `created_at`, `updated_at`.

Recommended offer fields:
- `offer_id`, `product_id`, `merchant_id`.
- `price_amount`, `currency`.
- `availability_status`: in_stock, out_of_stock, unknown.
- `product_url`.
- `source_id`, `source_record_id`.
- `last_verified_at`, `expires_at`.
- `is_synthetic` for test/demo fixtures.

Product identity and merchant offer are separate: one product may have multiple merchant offers with different prices and stock.

## 5. Validation rules

Reject or quarantine records with:
- Missing stable source identifier or title.
- Negative, zero or malformed prices.
- Unsupported or missing currency.
- Invalid product URLs.
- Unapproved image URLs.
- Unknown availability represented as in-stock.
- Impossible timestamps or expired offers.
- Duplicate records that cannot be safely reconciled.

Do not infer a discount unless a valid reference price and its basis are supplied by an authorized source. Do not calculate savings from an invented MRP.

## 6. Freshness

Freshness thresholds must be defined per source and contract. The interface should:
- Display the last verified time.
- Stop labelling stale offers as current.
- Suppress expired offers or mark them unavailable for recommendation.
- Retry transient source failures with bounded backoff.
- Record ingestion failures and alert an operator.

Do not invent a universal refresh interval; use the source's permitted cadence and reliability.

## 7. User and merchant data

- Collect only data required for the feature.
- Explain purposes before collecting personal information.
- Use explicit controls for optional personalization.
- Do not sell personal data or expose identifiable shopping histories to merchants.
- Merchant analytics should be aggregated and subject to minimum cohort thresholds.
- Provide appropriate access, correction and deletion workflows.
- Define retention and deletion schedules.
- Restrict access by role and merchant tenant.

## 8. Affiliate and sponsored content

- Clearly disclose affiliate links and commercial relationships.
- Clearly distinguish sponsored placement from organic ranking.
- Do not let payment silently override product suitability.
- Explain ranking factors at a useful level.
- Maintain auditable records of sponsored campaigns and disclosures.

## 9. Incident response

For a suspected data-rights, privacy or security incident:
1. Disable the affected source or feature.
2. Preserve relevant logs securely.
3. Assess affected records and users.
4. Follow applicable notification and legal obligations.
5. Correct, delete or refresh affected data.
6. Document root cause and preventive action.

## 10. Launch gate

Before live data or user accounts are enabled, obtain review of:
- Source rights and retailer terms.
- Privacy notice, consent and retention.
- Security and access controls.
- Affiliate/sponsored disclosures.
- Applicable Indian data protection, consumer protection, advertising and tax requirements.

This document is an engineering policy, not legal advice.

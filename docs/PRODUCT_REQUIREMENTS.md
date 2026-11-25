# Product Requirements — AI Deal Discovery Agent

**Document status:** Draft for validation  
**Product stage:** Prototype → foundation  
**Primary market hypothesis:** India  
**Initial category hypothesis:** Consumer electronics and personal technology accessories  
**Repository:** AakankshLabs/ai-deal-agent

## 1. Product vision

Help shoppers make better-informed product decisions through relevant, explainable comparisons, while helping merchants understand catalogue quality and customer demand.

The product has two connected experiences:
- **Consumer:** search, discover, compare, save and evaluate products.
- **Merchant:** understand catalogue gaps, improve listings and review aggregated search demand.

These are product hypotheses, not validated market facts.

## 2. Problem hypotheses to validate

### Consumer
- Shoppers may struggle to translate needs and budgets into a useful shortlist.
- Product listings may make specification comparisons difficult.
- Promotional claims and stale prices can reduce trust.
- Search results may optimize for keyword match rather than suitability.

### Merchant
- Smaller merchants may lack actionable insight into catalogue completeness.
- Merchants may not know which customer queries return poor or no results.
- Listing improvements may be difficult to prioritize without structured audits.

## 3. Target users

### Initial consumer segment
Indian shoppers researching electronics and personal technology accessories, such as headphones, earphones, keyboards, mice, speakers and laptop accessories.

### Initial merchant segment
Small and medium online sellers with product catalogues they own or are authorized to share.

## 4. Product principles

1. **Truth before persuasion:** never invent prices, discounts, ratings, availability or specifications.
2. **Explainable recommendations:** show why a product matched and identify missing information.
3. **Data provenance:** retain source and verification timestamps for every external offer.
4. **Privacy by design:** collect the minimum data required and do not expose identifiable shopper behaviour to merchants.
5. **Permissioned data:** use retailer APIs, merchant-authorized feeds or explicitly licensed sources.
6. **Measurable quality:** evaluate search and recommendation quality against labelled test cases.
7. **Progressive complexity:** keep the current Streamlit prototype working while introducing new capabilities in small, testable increments.

## 5. Scope

### Foundation release (v0.2)
- Product requirements and explicit non-goals.
- Proposed modular architecture.
- Data sourcing and provenance policy.
- Evaluation plan and baseline metrics.
- Initial relational data model.
- Development environment template with no secrets.
- Preserve current application and automated tests.

### Consumer beta (later release)
- Natural-language product search.
- Budget and specification filters.
- Product comparison grounded in source data.
- Saved products and explicit preference controls.
- Product/offer freshness indicators.
- Merchant outbound links with disclosure where applicable.

### Merchant pilot (later release)
- Authorized CSV catalogue upload.
- Catalogue validation and listing completeness audit.
- Aggregated query insights with privacy safeguards.
- Actionable listing recommendations.
- Pilot outcome reporting.

## 6. Explicit non-goals for v0.2

- No live retailer scraping.
- No claim of live inventory or real discounts.
- No checkout, payment handling or marketplace custody.
- No user account system yet.
- No production LLM integration or paid API dependency.
- No machine-learning model trained without suitable labelled data.
- No merchant access to identifiable consumer histories.
- No migration that removes the existing Streamlit app.

## 7. Functional requirements

| ID | Requirement | Acceptance condition |
|---|---|---|
| FR-01 | Search products | Query returns ranked eligible products from a known catalogue |
| FR-02 | Budget filter | Products above the requested maximum are excluded |
| FR-03 | Explain ranking | Each result has human-readable reasons and score components |
| FR-04 | Compare products | Comparisons use available, normalized attributes and mark missing values |
| FR-05 | Show provenance | External records expose source and last-verified time |
| FR-06 | Validate feeds | Invalid prices, URLs, IDs and required fields are rejected or quarantined |
| FR-07 | Merchant upload | Only authorized merchant catalogue data can be imported |
| FR-08 | Privacy | Merchant analytics are aggregated and do not expose identifiable shoppers |
| FR-09 | Feedback | Feedback is explicit, purpose-limited and can be withdrawn/deleted |
| FR-10 | Disclose monetization | Affiliate and sponsored relationships are clearly labelled |

## 8. Non-functional requirements

- Automated tests run on every pull request.
- Secrets are stored outside source control.
- External data failures do not crash the whole application.
- Prices and stock are displayed with timestamps and source context.
- APIs validate inputs and return predictable error responses.
- Logs avoid passwords, tokens and unnecessary personal data.
- Accessibility, responsive layouts and performance are tested before public launch.

## 9. Success measures

These are target metrics to validate, not current performance claims:
- Search relevance: Precision@5, Recall@10, NDCG@10 and MRR on a labelled query set.
- Data quality: valid-record rate, duplicate rate, missing-field rate and feed freshness.
- Trust: price/availability accuracy and complaint rate.
- Consumer value: search-to-product-click rate, repeat usage and explicit relevance feedback.
- Merchant value: audit completion, suggestions accepted, pilot retention and willingness to pay.
- Reliability: availability, error rate and unresolved critical security findings.

## 10. Key risks and mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| No authorized product data | Critical | Secure permissioned data before promising live offers |
| Stale or incorrect price/stock | Critical | Timestamp, freshness SLA, suppress stale offers |
| Weak consumer demand | High | Interview shoppers and test a narrow use case |
| Merchants do not pay | High | Run paid pilots before building extensive dashboards |
| Poor ranking quality | High | Label queries and benchmark before claiming intelligence |
| Privacy or data-rights breach | Critical | Data minimization, permission records and legal review |
| Solo-founder overload | High | Narrow scope and ship incremental releases |

## 11. Validation plan

Before building a broad platform:
- Interview at least 20 target shoppers.
- Interview at least 10 online merchants.
- Ask about recent real shopping/listing tasks, not hypothetical enthusiasm.
- Test whether users prefer a trustworthy shortlist over generic search.
- Ask merchants to share a sample catalogue only where they have authority.
- Record evidence, objections and willingness-to-pay signals.
- Revisit the initial category hypothesis based on evidence.

## 12. Release gate

Do not describe the product as production-ready until data rights, source freshness, privacy controls, reliability, security, usability and evaluation have been tested. A passing CI suite proves only that the tested code paths passed.

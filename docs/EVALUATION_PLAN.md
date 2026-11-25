# Search and Recommendation Evaluation Plan

**Status:** Initial plan. No target metric is a current product result.

## 1. Why evaluate

A recommendation score is not proof of relevance. The current engine is deterministic and rule-based. We need labelled examples and repeatable metrics before claiming improved search or AI personalization.

## 2. Build a labelled query set

Create 300–500 representative shopping queries after interviewing target users. Start with a smaller 50-query pilot to refine the annotation guide.

Each case should include:
- Query text.
- User-stated budget and hard constraints.
- Relevant category and attributes.
- Candidate product IDs from an authorized catalogue.
- Relevance grade (0–3).
- Reason for relevance or exclusion.
- Annotator and review status.

Suggested relevance scale:
- 0: irrelevant or violates a hard constraint.
- 1: weakly related, important needs unmet.
- 2: relevant, but has notable trade-offs.
- 3: strong match for the stated need.

Use two independent reviewers for a subset and resolve disagreements with documented rules.

## 3. Offline metrics

| Metric | What it measures | Use |
|---|---|---|
| Precision@5 | Share of top five results judged relevant | Top-list quality |
| Recall@10 | Share of relevant candidates retrieved in top ten | Retrieval coverage |
| NDCG@10 | Ranking quality with graded relevance | Compare ranking versions |
| MRR | Rank of first relevant result | First useful result |
| Constraint violation rate | Results breaking hard requirements | Safety/trust |
| Zero-result rate | Searches with no returned products | Coverage diagnostics |

Report overall and by category, budget band, query type and persona. Do not optimize a single metric while worsening hard-constraint accuracy.

## 4. Data-quality metrics

- Required-field completeness.
- Duplicate product/offer rate.
- Invalid URL rate.
- Invalid price/currency rate.
- Percentage of offers within source freshness SLA.
- Price discrepancy rate on sampled manual checks.
- Unknown availability rate.
- Feed ingestion success and failure rate.

## 5. Online product metrics

Only after consent and privacy review:
- Search-to-product-detail click rate.
- Product comparison usage.
- Save rate.
- Repeat search and repeat usage.
- Explicit relevant/not-relevant feedback.
- Outbound click-through rate.
- Merchant audit completion and accepted recommendations.
- Merchant pilot renewal and subscription revenue.

Clicks are not equivalent to satisfaction or purchase conversion. Do not claim sales attribution without a reliable measurement arrangement.

## 6. Experiment discipline

For each ranking change:
1. Record code version and dataset version.
2. Run the same frozen evaluation set.
3. Compare against the existing baseline.
4. Inspect regressions and examples, not just averages.
5. Keep hard filters independent of ranking weights.
6. Roll back if data accuracy or constraint violations worsen.
7. Document the decision.

## 7. Initial release gates

Proposed gates to be agreed after the pilot dataset exists:
- No known hard-constraint violations in the release test set.
- Ranking metrics reported against the baseline.
- No unsupported claim of accuracy or personalization.
- Stale/unknown data clearly identified.
- All critical catalogue validation tests pass.

## 8. Dataset governance

Do not put personal shopping histories, contact details or other unnecessary personal information in the benchmark set. Use synthetic query examples or de-identified, consented examples with documented access and retention.

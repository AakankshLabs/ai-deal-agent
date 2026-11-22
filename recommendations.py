"""Transparent, rule-based product recommendation utilities.

This is a baseline recommender, not a machine-learning model or LLM.
"""

import re
from copy import deepcopy


# Small, explicit synonym groups make related search language useful.
SYNONYM_GROUPS = (
    {"headphone", "headphones", "headset", "headsets", "earphone", "earphones"},
    {"shoe", "shoes", "sneaker", "sneakers", "trainer", "trainers"},
    {"shirt", "shirts", "top", "tops"},
    {"gaming", "gamer", "game", "games"},
    {"gadget", "gadgets", "device", "devices", "tech", "technology"},
    {"fashion", "clothing", "apparel", "wear"},
)

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text):
    """Convert text to lowercase alphanumeric tokens."""
    return TOKEN_PATTERN.findall(str(text).lower())


def _expanded_query_tokens(query_tokens):
    """Return synonym-aware alternatives for each original query token."""
    groups_by_token = {
        token: group
        for group in SYNONYM_GROUPS
        for token in group
    }
    return {
        token: groups_by_token.get(token, {token})
        for token in query_tokens
    }


def recommend_products(products, query, budget):
    """Filter and rank products using relevance, budget fit, and discount.

    Each returned item is a copy of the original product with:
      - recommendation_score: score from 0 to 100
      - recommendation_reasons: short, human-readable explanations

    Products outside the budget or with no query-token match are excluded.
    """
    query_tokens = list(dict.fromkeys(tokenize(query)))
    if not query_tokens or budget <= 0:
        return []

    expanded_tokens = _expanded_query_tokens(query_tokens)
    ranked = []

    for product in products:
        price = product.get("price", 0)
        original_price = product.get("original", 0)

        if not isinstance(price, (int, float)) or price <= 0 or price > budget:
            continue

        searchable_text = " ".join(
            [product.get("name", "")]
            + product.get("keywords", [])
        )
        product_tokens = set(tokenize(searchable_text))
        matched_terms = [
            token
            for token, alternatives in expanded_tokens.items()
            if product_tokens.intersection(alternatives)
        ]

        if not matched_terms:
            continue

        relevance = len(matched_terms) / len(query_tokens)
        normalized_query = " ".join(query_tokens)
        normalized_name = " ".join(tokenize(product.get("name", "")))
        exact_name_match = normalized_query in normalized_name

        budget_fit = max(0.0, min(1.0, (budget - price) / budget))
        discount = 0.0
        if isinstance(original_price, (int, float)) and original_price > price:
            discount = min(1.0, (original_price - price) / original_price)

        score = (
            0.75 * relevance
            + 0.15 * budget_fit
            + 0.10 * discount
        )
        if exact_name_match:
            score = min(1.0, score + 0.05)

        reasons = [
            f"Matched search term(s): {', '.join(matched_terms)}",
            f"Within your ₹{budget:,.0f} budget",
        ]
        if exact_name_match:
            reasons.append("Product name closely matches your search")
        if discount > 0:
            reasons.append(f"Illustrative discount: {round(discount * 100)}%")

        result = deepcopy(product)
        result["recommendation_score"] = round(score * 100)
        result["recommendation_reasons"] = reasons
        ranked.append(result)

    return sorted(
        ranked,
        key=lambda item: (
            -item["recommendation_score"],
            item.get("price", float("inf")),
        ),
    )

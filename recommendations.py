"""Transparent, persona-aware product recommendation utilities.

This is a deterministic baseline recommender, not a machine-learning model or LLM.
"""

import re
from copy import deepcopy


SYNONYM_GROUPS = (
    {"headphone", "headphones", "headset", "headsets", "earphone", "earphones"},
    {"shoe", "shoes", "sneaker", "sneakers", "trainer", "trainers"},
    {"shirt", "shirts", "top", "tops"},
    {"gaming", "gamer", "game", "games"},
    {"gadget", "gadgets", "device", "devices", "tech", "technology"},
    {"fashion", "clothing", "apparel", "wear"},
    {"fitness", "workout", "exercise", "training"},
)

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

# Personas are hypotheses for product design, not verified demographic profiles.
PERSONAS = {
    "Budget-conscious student": {
        "segment": "student",
        "description": "Looks for practical campus essentials, useful everyday items, and affordable choices.",
        "priorities": ["Affordable price", "Everyday utility", "Visible savings"],
        "preferred_categories": {"stationery", "student_essentials", "fashion", "electronics"},
        "budget_sensitivity": 1.0,
    },
    "Campus style seeker": {
        "segment": "student",
        "description": "Wants clothing and accessories that fit a personal style without overspending.",
        "priorities": ["Style relevance", "Good value", "Wearability"],
        "preferred_categories": {"fashion", "footwear", "accessories"},
        "budget_sensitivity": 0.8,
    },
    "Competitive gamer": {
        "segment": "gamer",
        "description": "Prioritizes gaming peripherals and useful performance-oriented features.",
        "priorities": ["Gaming relevance", "Useful features", "Budget fit"],
        "preferred_categories": {"gaming", "electronics", "audio"},
        "budget_sensitivity": 0.65,
    },
    "Casual gamer and streamer": {
        "segment": "gamer",
        "description": "Looks for accessible gaming, audio, and content-creation accessories.",
        "priorities": ["Versatility", "Audio and creator utility", "Value"],
        "preferred_categories": {"gaming", "audio", "electronics", "creator_gear"},
        "budget_sensitivity": 0.75,
    },
    "Tech enthusiast": {
        "segment": "shopper",
        "description": "Explores useful gadgets and technology accessories, balancing features and price.",
        "priorities": ["Technology relevance", "Features", "Value"],
        "preferred_categories": {"electronics", "audio", "gadgets"},
        "budget_sensitivity": 0.55,
    },
    "Value-first everyday shopper": {
        "segment": "shopper",
        "description": "Compares practical products and prefers a strong balance of relevance and savings.",
        "priorities": ["Practical utility", "Price", "Savings"],
        "preferred_categories": {"home", "fashion", "electronics", "student_essentials", "footwear"},
        "budget_sensitivity": 0.9,
    },
    "Fitness and active lifestyle shopper": {
        "segment": "shopper",
        "description": "Looks for products that support exercise, movement, and an active routine.",
        "priorities": ["Fitness relevance", "Durability cues", "Value"],
        "preferred_categories": {"fitness", "footwear", "fashion"},
        "budget_sensitivity": 0.7,
    },
}


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


def recommend_products(products, query, budget, persona_name=None):
    """Filter and rank products using query relevance and persona preferences.

    Returns copies of matching products with recommendation_score and
    recommendation_reasons. Scores are heuristic ranking indicators, not
    probabilities or measured model confidence.
    """
    query_tokens = list(dict.fromkeys(tokenize(query)))
    if not query_tokens or not isinstance(budget, (int, float)) or budget <= 0:
        return []

    persona = PERSONAS.get(persona_name, {})
    preferred_categories = persona.get("preferred_categories", set())
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
            + product.get("features", [])
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

        categories = set(product.get("categories", []))
        persona_tags = set(product.get("persona_tags", []))
        category_fit = bool(categories.intersection(preferred_categories))
        tag_fit = persona.get("segment") in persona_tags if persona else False
        persona_fit = 1.0 if category_fit or tag_fit else 0.0

        if persona:
            # Persona-aware weights: relevance remains the strongest signal.
            score = (
                0.60 * relevance
                + 0.20 * persona_fit
                + 0.12 * budget_fit
                + 0.08 * discount
            )
        else:
            score = (
                0.75 * relevance
                + 0.15 * budget_fit
                + 0.10 * discount
            )

        if exact_name_match:
            score = min(1.0, score + 0.05)

        reasons = [f"Matched search term(s): {', '.join(matched_terms)}"]
        reasons.append(f"Within your ₹{budget:,.0f} budget")
        if persona:
            if category_fit:
                reasons.append("Category aligns with this persona's stated interests")
            elif tag_fit:
                reasons.append("Product is tagged for this audience segment")
            else:
                reasons.append("No direct persona-category match; search relevance still qualifies it")
        if exact_name_match:
            reasons.append("Product name closely matches your search")
        if discount > 0:
            reasons.append(f"Illustrative discount: {round(discount * 100)}%")

        result = deepcopy(product)
        result["recommendation_score"] = round(score * 100)
        result["recommendation_reasons"] = reasons
        result["persona_fit"] = persona_fit
        if persona:
            components = {
                "Query relevance (60%)": 0.60 * relevance,
                "Persona fit (20%)": 0.20 * persona_fit,
                "Budget fit (12%)": 0.12 * budget_fit,
                "Illustrative discount (8%)": 0.08 * discount,
            }
        else:
            components = {
                "Query relevance (75%)": 0.75 * relevance,
                "Budget fit (15%)": 0.15 * budget_fit,
                "Illustrative discount (10%)": 0.10 * discount,
            }
        if exact_name_match:
            components["Exact-name bonus"] = 0.05
        result["recommendation_score_breakdown"] = {
            label: round(value * 100, 2)
            for label, value in components.items()
        }
        ranked.append(result)

    return sorted(
        ranked,
        key=lambda item: (
            -item["recommendation_score"],
            item.get("price", float("inf")),
        ),
    )

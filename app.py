import json
from pathlib import Path

import streamlit as st

from recommendations import PERSONAS, recommend_products

st.set_page_config(
    page_title="AI Deal Discovery & Marketing Agent",
    page_icon="🛍️",
    layout="centered",
)


@st.cache_data
def load_catalogue():
    """Load the versioned illustrative product catalogue."""
    catalogue_path = Path(__file__).parent / "data" / "products.json"
    with catalogue_path.open("r", encoding="utf-8") as catalogue_file:
        payload = json.load(catalogue_file)

    products = payload.get("products", [])
    if not isinstance(products, list):
        raise ValueError("Catalogue must contain a products list.")
    return payload, products


st.title("🛍️ AI Deal Discovery & Marketing Agent")
st.write("Explore a structured product catalogue with persona-aware recommendations.")

try:
    catalogue, products = load_catalogue()
except (OSError, json.JSONDecodeError, ValueError) as error:
    st.error(f"Could not load the product catalogue: {error}")
    st.stop()

st.caption(
    f"Catalogue: {catalogue.get('record_count', len(products))} illustrative sample products. "
    "No live retailer prices, sellers, or inventory are connected."
)

persona_name = st.selectbox("Choose a shopper persona", list(PERSONAS.keys()))
persona = PERSONAS[persona_name]

with st.expander("Understand this persona", expanded=True):
    st.write(persona["description"])
    st.write("**Priorities:** " + " · ".join(persona["priorities"]))
    st.caption(
        "Persona preferences are product-design assumptions used to demonstrate "
        "personalization; they are not inferred from personal data."
    )

product_input = st.text_input(
    "What product are you looking for?",
    placeholder="e.g. shirt, sneakers, headphones, study, fitness",
)
budget = st.slider(
    "Maximum budget (₹)",
    min_value=500,
    max_value=5000,
    value=3000,
    step=100,
)

if st.button("🚀 Find personalized deals", type="primary"):
    if not product_input.strip():
        st.warning("Enter a product or category to search.")
    else:
        results = recommend_products(products, product_input, budget, persona_name)

        if results:
            st.success(
                f"Found {len(results)} matching sample product(s) for "
                f"**{persona_name}**."
            )

            for product in results:
                discount = round(
                    ((product["original"] - product["price"]) / product["original"]) * 100
                ) if product.get("original", 0) > product["price"] else 0
                savings = max(0, product.get("original", product["price"]) - product["price"])

                st.divider()
                details_col, score_col = st.columns([3, 1])
                with details_col:
                    st.subheader(product["name"])
                    st.caption(
                        f"{product['brand']} · {product['category'].replace('_', ' ').title()} "
                        f"· {product['subcategory'].replace('_', ' ').title()}"
                    )
                    st.write(product["description"])
                    st.write(f"**Sample price:** ₹{product['price']:,}")
                    st.write(f"**Illustrative discount:** {discount}%")
                    st.write(f"**Estimated sample savings:** ₹{savings:,}")
                with score_col:
                    st.metric("Match score", f"{product['recommendation_score']}%")

                st.caption("Why this appeared")
                for reason in product["recommendation_reasons"]:
                    st.write(f"- {reason}")
                st.caption(product["data_note"])

            best = results[0]
            st.divider()
            st.subheader("📣 Marketing copy examples")
            st.write(f"**Instagram:** Discover the {best['name']} at an illustrative price of ₹{best['price']:,}.")
            st.write(f"**Push notification:** Sample pick: {best['name']} — explore this option.")
            st.write(f"**Email subject:** A product idea for you: {best['name']}.")
            st.write(f"**SEO snippet:** Explore {product_input} options in a budget of ₹{budget:,}.")

            st.divider()
            st.subheader("📊 Persona insight")
            st.write(f"**{persona_name}:** {persona['description']}")
            st.write("**Priorities:** " + " · ".join(persona["priorities"]))
            st.caption(
                "Persona-aware score: relevance (60%), persona fit (20%), "
                "budget fit (12%), illustrative discount (8%), plus a small exact-name bonus. "
                "This is a heuristic ranking score, not an AI confidence score."
            )
        else:
            st.info(
                "No sample products matched both the search and budget. "
                "Try another keyword or increase your budget."
            )

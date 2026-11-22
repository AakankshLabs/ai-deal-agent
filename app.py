import csv
import io
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


if "search_events" not in st.session_state:
    st.session_state.search_events = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

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
        st.session_state.search_events.append({
            "query": product_input.strip(),
            "persona": persona_name,
            "budget_inr": budget,
            "result_count": len(results),
        })
        st.session_state.last_results = results
        st.session_state.last_query = product_input.strip()
        st.session_state.last_persona = persona_name
        st.session_state.last_budget = budget

if "last_results" in st.session_state:
    results = st.session_state.last_results
    if results:
        st.success(
            f"Found {len(results)} matching sample product(s) for "
            f"**{st.session_state.last_persona}**."
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

            with st.expander(f"How the score was calculated — {product['name']}"):
                st.caption("Heuristic contribution points, not model confidence or probability.")
                for component, points in product["recommendation_score_breakdown"].items():
                    st.write(f"**{component}:** {points:g} points")
                    st.progress(min(100, max(0, int(round(points * 100 / 60)))))

            st.caption("Why this appeared")
            for reason in product["recommendation_reasons"]:
                st.write(f"- {reason}")
            st.caption(product["data_note"])

            feedback_key = str(product.get("id", product["name"]))
            with st.form(f"feedback_form_{feedback_key}"):
                vote = st.radio(
                    "Was this recommendation relevant?",
                    ["👍 Relevant", "👎 Not relevant"],
                    horizontal=True,
                    key=f"feedback_vote_{feedback_key}",
                )
                submitted = st.form_submit_button("Submit feedback")
                if submitted:
                    st.session_state.feedback[feedback_key] = {
                        "product": product["name"],
                        "vote": vote,
                        "query": st.session_state.last_query,
                        "persona": st.session_state.last_persona,
                    }
                    st.success("Feedback recorded for this session.")

        best = results[0]
        st.divider()
        st.subheader("📣 Marketing copy examples")
        st.write(f"**Instagram:** Discover the {best['name']} at an illustrative price of ₹{best['price']:,}.")
        st.write(f"**Push notification:** Sample pick: {best['name']} — explore this option.")
        st.write(f"**Email subject:** A product idea for you: {best['name']}.")
        st.write(f"**SEO snippet:** Explore {st.session_state.last_query} options in a budget of ₹{st.session_state.last_budget:,}.")

        st.divider()
        st.subheader("📊 Persona insight")
        st.write(f"**{st.session_state.last_persona}:** {PERSONAS[st.session_state.last_persona]['description']}")
        st.write("**Priorities:** " + " · ".join(PERSONAS[st.session_state.last_persona]["priorities"]))
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

with st.expander("📈 Session analytics and feedback", expanded=False):
    searches = st.session_state.search_events
    feedback = list(st.session_state.feedback.values())
    relevant = sum(item["vote"] == "👍 Relevant" for item in feedback)
    not_relevant = len(feedback) - relevant
    metric_cols = st.columns(3)
    metric_cols[0].metric("Searches this session", len(searches))
    metric_cols[1].metric("Positive feedback", relevant)
    metric_cols[2].metric("Negative feedback", not_relevant)
    st.caption(
        "Analytics and feedback stay in this browser session only. They are not "
        "uploaded to a server or retained after the session ends."
    )
    if searches or feedback:
        export = io.StringIO()
        writer = csv.writer(export)
        writer.writerow(["event_type", "query", "persona", "budget_inr", "result_count", "product", "feedback"])
        for event in searches:
            writer.writerow(["search", event["query"], event["persona"], event["budget_inr"], event["result_count"], "", ""])
        for item in feedback:
            writer.writerow(["feedback", item["query"], item["persona"], "", "", item["product"], item["vote"]])
        st.download_button(
            "Download session analytics (CSV)",
            data=export.getvalue(),
            file_name="deal-agent-session-analytics.csv",
            mime="text/csv",
        )
    else:
        st.info("Run a search or submit recommendation feedback to populate this panel.")

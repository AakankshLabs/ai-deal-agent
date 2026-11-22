import streamlit as st

from recommendations import PERSONAS, recommend_products

st.set_page_config(
    page_title="AI Deal Discovery & Marketing Agent",
    page_icon="🛍️",
    layout="centered",
)

st.title("🛍️ AI Deal Discovery & Marketing Agent")
st.write("Explore sample product deals with persona-aware recommendations.")
st.caption(
    "Portfolio prototype: recommendations use transparent, rule-based scoring "
    "on illustrative catalogue data. No live retailer prices or inventory are connected."
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
    placeholder="e.g. shirt, sneakers, headphones",
)
budget = st.slider(
    "Maximum budget (₹)",
    min_value=500,
    max_value=5000,
    value=3000,
    step=100,
)

products = [
    {
        "name": "Casual Shirt",
        "price": 1200,
        "original": 2000,
        "keywords": ["shirt", "fashion"],
        "categories": ["fashion"],
        "persona_tags": ["student", "shopper"],
        "features": ["everyday", "casual", "campus"],
        "seller": "Student Seller",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Formal Shirt",
        "price": 2500,
        "original": 3500,
        "keywords": ["shirt", "fashion"],
        "categories": ["fashion"],
        "persona_tags": ["student", "shopper"],
        "features": ["formal", "office", "smart"],
        "seller": "Campus Sale",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Sports Shoes",
        "price": 2499,
        "original": 4000,
        "keywords": ["shoes", "fashion", "fitness"],
        "categories": ["footwear", "fitness"],
        "persona_tags": ["student", "shopper"],
        "features": ["sports", "running", "training", "active"],
        "seller": "Senior Seller",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Gaming Headset",
        "price": 1999,
        "original": 3000,
        "keywords": ["gaming", "gamer", "headphones", "audio"],
        "categories": ["gaming", "audio", "electronics"],
        "persona_tags": ["gamer"],
        "features": ["headset", "microphone", "gaming", "audio"],
        "seller": "Tech Club",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Smart Gadget",
        "price": 2199,
        "original": 3500,
        "keywords": ["gadget", "tech", "device"],
        "categories": ["electronics", "gadgets"],
        "persona_tags": ["student", "gamer", "shopper"],
        "features": ["technology", "portable", "accessory"],
        "seller": "Student Store",
        "image": "https://via.placeholder.com/150",
    },
]

if st.button("🚀 Find personalized deals", type="primary"):
    if not product_input.strip():
        st.warning("Enter a product or category to search.")
    else:
        results = recommend_products(products, product_input, budget, persona_name)

        if results:
            st.success(
                f"Found {len(results)} matching sample deal(s) for "
                f"**{persona_name}**."
            )

            for product in results:
                discount = round(
                    ((product["original"] - product["price"]) / product["original"]) * 100
                )
                savings = product["original"] - product["price"]

                st.divider()
                image_col, details_col = st.columns([1, 2])
                with image_col:
                    st.image(product["image"], width=120)
                with details_col:
                    st.subheader(f"{product['name']} — {product['seller']}")
                    st.write(f"**Sample price:** ₹{product['price']:,}")
                    st.write(
                        f"**Illustrative discount:** {discount}% "
                        f"(₹{product['original']:,} → ₹{product['price']:,})"
                    )
                    st.write(f"**Estimated savings:** ₹{savings:,}")
                    st.metric("Recommendation match score", f"{product['recommendation_score']}%")
                    st.caption("Why this appeared")
                    for reason in product["recommendation_reasons"]:
                        st.write(f"- {reason}")

            best = results[0]
            st.divider()
            st.subheader("📣 Marketing copy examples")
            st.write(f"**Instagram:** Don’t miss this {best['name']} now at ₹{best['price']:,}!")
            st.write(f"**Push notification:** Deal example: {best['name']} at ₹{best['price']:,}.")
            st.write(f"**Email subject:** Sample deal alert — {best['name']} at ₹{best['price']:,}.")
            st.write(f"**SEO snippet:** Explore {product_input} within a budget of ₹{budget:,}.")

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
                "Try shirt, shoes, sneakers, gaming, headphones, gadget, or tech, "
                "or increase your budget."
            )

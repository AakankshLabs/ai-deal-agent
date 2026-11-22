import streamlit as st

from recommendations import recommend_products

# Page configuration
st.set_page_config(
    page_title="AI Deal Discovery & Marketing Agent",
    page_icon="🛍️",
    layout="centered",
)

st.title("🛍️ AI Deal Discovery & Marketing Agent")
st.write("Explore sample product deals using a search query and budget.")
st.caption(
    "Portfolio prototype: recommendations use transparent, rule-based scoring "
    "on illustrative catalogue data. No live retailer prices or inventory are connected."
)

# Shopper inputs
user_type = st.selectbox("Audience segment", ["student", "gamer", "shopper"])
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

# Illustrative sample catalogue
products = [
    {
        "name": "Casual Shirt",
        "price": 1200,
        "original": 2000,
        "keywords": ["shirt", "fashion"],
        "seller": "Student Seller",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Formal Shirt",
        "price": 2500,
        "original": 3500,
        "keywords": ["shirt", "fashion"],
        "seller": "Campus Sale",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Sports Shoes",
        "price": 2499,
        "original": 4000,
        "keywords": ["shoes", "fashion"],
        "seller": "Senior Seller",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Gaming Headset",
        "price": 1999,
        "original": 3000,
        "keywords": ["gaming", "gamer"],
        "seller": "Tech Club",
        "image": "https://via.placeholder.com/150",
    },
    {
        "name": "Smart Gadget",
        "price": 2199,
        "original": 3500,
        "keywords": ["gadget", "tech"],
        "seller": "Student Store",
        "image": "https://via.placeholder.com/150",
    },
]

if st.button("🚀 Find recommended deals", type="primary"):
    if not product_input.strip():
        st.warning("Enter a product or category to search.")
    else:
        results = recommend_products(products, product_input, budget)

        if results:
            st.success(f"Found {len(results)} matching sample deal(s), ranked by match score.")

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

            # Template-based marketing copy for the highest-ranked match
            best = results[0]
            st.divider()
            st.subheader("📣 Marketing copy examples")
            st.write(f"**Instagram:** Don’t miss this {best['name']} now at ₹{best['price']:,}!")
            st.write(f"**Push notification:** Deal example: {best['name']} at ₹{best['price']:,}.")
            st.write(f"**Email subject:** Sample deal alert — {best['name']} at ₹{best['price']:,}.")
            st.write(f"**SEO snippet:** Explore {product_input} within a budget of ₹{budget:,}.")

            st.divider()
            st.subheader("📊 Audience context")
            st.write(
                f"This search was run with the **{user_type}** audience segment selected. "
                "The segment is currently recorded as context and does not yet change ranking."
            )
            st.caption(
                "Score is a rule-based indicator combining query relevance (75%), "
                "budget fit (15%), and illustrative discount (10%). It is not an AI confidence score."
            )
        else:
            st.info(
                "No sample products matched both the search and budget. "
                "Try shirt, shoes, sneakers, gaming, headphones, gadget, or tech, "
                "or increase your budget."
            )

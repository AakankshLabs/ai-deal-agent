import unittest

from recommendations import PERSONAS, recommend_products, tokenize


SAMPLE_PRODUCTS = [
    {
        "name": "Casual Shirt",
        "price": 1200,
        "original": 2000,
        "keywords": ["shirt", "fashion"],
        "categories": ["fashion"],
        "persona_tags": ["student", "shopper"],
    },
    {
        "name": "Formal Shirt",
        "price": 2500,
        "original": 3500,
        "keywords": ["shirt", "fashion"],
        "categories": ["fashion"],
        "persona_tags": ["student", "shopper"],
    },
    {
        "name": "Sports Shoes",
        "price": 2499,
        "original": 4000,
        "keywords": ["shoes", "fashion", "fitness"],
        "categories": ["footwear", "fitness"],
        "persona_tags": ["student", "shopper"],
    },
    {
        "name": "Gaming Headset",
        "price": 1999,
        "original": 3000,
        "keywords": ["gaming", "gamer", "headphones"],
        "categories": ["gaming", "audio", "electronics"],
        "persona_tags": ["gamer"],
    },
]


class RecommendationTests(unittest.TestCase):
    def test_tokenize_removes_punctuation_and_normalizes_case(self):
        self.assertEqual(tokenize("Gaming-Headphones!"), ["gaming", "headphones"])

    def test_synonym_query_finds_related_product(self):
        results = recommend_products(SAMPLE_PRODUCTS, "headphones", 3000)
        self.assertEqual([item["name"] for item in results], ["Gaming Headset"])

    def test_budget_excludes_expensive_matches(self):
        results = recommend_products(SAMPLE_PRODUCTS, "shirt", 1500)
        self.assertEqual([item["name"] for item in results], ["Casual Shirt"])

    def test_relevant_results_are_ranked_and_explained(self):
        results = recommend_products(SAMPLE_PRODUCTS, "shirt", 3000)
        self.assertEqual(results[0]["name"], "Casual Shirt")
        self.assertGreaterEqual(
            results[0]["recommendation_score"],
            results[1]["recommendation_score"],
        )
        self.assertTrue(results[0]["recommendation_reasons"])

    def test_score_breakdown_is_present_and_transparent(self):
        result = recommend_products(
            SAMPLE_PRODUCTS, "shirt", 3000, "Budget-conscious student"
        )[0]
        breakdown = result["recommendation_score_breakdown"]
        self.assertIn("Query relevance (60%)", breakdown)
        self.assertIn("Persona fit (20%)", breakdown)
        self.assertIn("Budget fit (12%)", breakdown)
        self.assertIn("Illustrative discount (8%)", breakdown)
        self.assertTrue(all(0 <= value <= 100 for value in breakdown.values()))

    def test_persona_changes_ranking_for_same_query(self):
        # Both shirts match the query, but the student persona prefers the
        # lower-priced campus-casual item in this sample catalogue.
        products = [
            dict(SAMPLE_PRODUCTS[0], categories=["fashion"], features=["campus"]),
            dict(SAMPLE_PRODUCTS[1], categories=["formalwear"], features=["office"]),
        ]
        results = recommend_products(
            products, "shirt", 3000, "Budget-conscious student"
        )
        self.assertEqual(results[0]["name"], "Casual Shirt")

    def test_persona_catalogue_contains_seven_detailed_profiles(self):
        self.assertEqual(len(PERSONAS), 7)
        for persona in PERSONAS.values():
            self.assertTrue(persona["description"])
            self.assertTrue(persona["priorities"])
            self.assertTrue(persona["preferred_categories"])

    def test_no_match_returns_empty_list(self):
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "camera", 5000), [])

    def test_empty_query_or_invalid_budget_returns_empty_list(self):
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "   ", 3000), [])
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "shirt", 0), [])

    def test_original_catalogue_is_not_mutated(self):
        products = [dict(SAMPLE_PRODUCTS[0])]
        recommend_products(products, "shirt", 2000, "Budget-conscious student")
        self.assertNotIn("recommendation_score", products[0])


if __name__ == "__main__":
    unittest.main()

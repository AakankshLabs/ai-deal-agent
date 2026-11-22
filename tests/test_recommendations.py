import unittest

from recommendations import recommend_products, tokenize


SAMPLE_PRODUCTS = [
    {
        "name": "Casual Shirt",
        "price": 1200,
        "original": 2000,
        "keywords": ["shirt", "fashion"],
    },
    {
        "name": "Formal Shirt",
        "price": 2500,
        "original": 3500,
        "keywords": ["shirt", "fashion"],
    },
    {
        "name": "Sports Shoes",
        "price": 2499,
        "original": 4000,
        "keywords": ["shoes", "fashion"],
    },
    {
        "name": "Gaming Headset",
        "price": 1999,
        "original": 3000,
        "keywords": ["gaming", "gamer"],
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

    def test_no_match_returns_empty_list(self):
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "camera", 5000), [])

    def test_empty_query_or_invalid_budget_returns_empty_list(self):
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "   ", 3000), [])
        self.assertEqual(recommend_products(SAMPLE_PRODUCTS, "shirt", 0), [])

    def test_original_catalogue_is_not_mutated(self):
        products = [dict(SAMPLE_PRODUCTS[0])]
        recommend_products(products, "shirt", 2000)
        self.assertNotIn("recommendation_score", products[0])


if __name__ == "__main__":
    unittest.main()

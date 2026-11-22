import json
import unittest
from pathlib import Path

from recommendations import PERSONAS, recommend_products


class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalogue_path = Path(__file__).resolve().parents[1] / "data" / "products.json"
        with catalogue_path.open("r", encoding="utf-8") as catalogue_file:
            cls.catalogue = json.load(catalogue_file)
        cls.products = cls.catalogue["products"]

    def test_catalogue_has_one_hundred_records(self):
        self.assertEqual(len(self.products), 100)
        self.assertEqual(self.catalogue["record_count"], 100)

    def test_product_ids_are_unique(self):
        ids = [product["id"] for product in self.products]
        self.assertEqual(len(ids), len(set(ids)))

    def test_each_record_has_recommendation_fields(self):
        required_fields = {
            "id", "name", "brand", "category", "subcategory", "description",
            "price", "original", "currency", "features", "keywords",
            "categories", "persona_tags", "seller", "availability",
            "product_url", "data_note",
        }
        for product in self.products:
            with self.subTest(product_id=product.get("id")):
                self.assertTrue(required_fields.issubset(product.keys()))
                self.assertGreater(product["price"], 0)
                self.assertGreaterEqual(product["original"], product["price"])
                self.assertTrue(product["keywords"])
                self.assertTrue(product["categories"])

    def test_all_records_are_explicitly_sample_data(self):
        self.assertEqual(self.catalogue["data_status"], "synthetic_sample_data")
        for product in self.products:
            self.assertEqual(product["availability"], "sample_only")
            self.assertIsNone(product["product_url"])
            self.assertIn("synthetic", product["data_note"].lower())


    def test_full_catalogue_integrates_with_recommendation_engine(self):
        results = recommend_products(
            self.products, "gaming", 5000, "Competitive gamer"
        )
        self.assertTrue(results)
        self.assertTrue(all(item["price"] <= 5000 for item in results))
        self.assertTrue(all(item["recommendation_reasons"] for item in results))
        self.assertTrue(all("recommendation_score" in item for item in results))

    def test_catalogue_multiword_search_requires_all_terms_and_budget(self):
        # At ₹1,000, no keyboard product is affordable. A gaming mouse pad
        # must not leak into results just because it contains "gaming".
        self.assertEqual(
            recommend_products(
                self.products, "gaming keyboard", 1000, "Competitive gamer"
            ),
            [],
        )

        # At ₹2,000, the actual gaming keyboard is eligible and should match.
        results = recommend_products(
            self.products, "gaming keyboard", 2000, "Competitive gamer"
        )
        self.assertEqual(
            [item["name"] for item in results],
            ["Mechanical Gaming Keyboard"],
        )

    def test_catalogue_keyboard_query_does_not_return_unrelated_products(self):
        results = recommend_products(
            self.products, "keyboard", 1000, "Competitive gamer"
        )
        self.assertEqual(results, [])


    def test_each_persona_can_query_the_full_catalogue(self):
        for persona_name in PERSONAS:
            with self.subTest(persona=persona_name):
                results = recommend_products(
                    self.products, "student essentials", 5000, persona_name
                )
                self.assertIsInstance(results, list)

    def test_catalogue_covers_ten_categories(self):
        categories = {product["category"] for product in self.products}
        self.assertEqual(len(categories), 10)


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path


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

    def test_catalogue_covers_ten_categories(self):
        categories = {product["category"] for product in self.products}
        self.assertEqual(len(categories), 10)


if __name__ == "__main__":
    unittest.main()

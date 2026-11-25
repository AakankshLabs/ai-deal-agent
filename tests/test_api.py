import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_catalogue_endpoint_discloses_synthetic_data(self):
        response = self.client.get("/api/v1/catalogue")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["data_status"], "synthetic_sample_data")
        self.assertEqual(payload["record_count"], 100)
        self.assertIn("synthetic", payload["disclaimer"].lower())

    def test_search_returns_sample_products_and_provenance(self):
        response = self.client.get(
            "/api/v1/products/search",
            params={"q": "headphones", "budget_inr": 5000, "persona": "Tech enthusiast"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["data_status"], "synthetic_sample_data")
        self.assertGreater(payload["result_count"], 0)
        self.assertTrue(all(item["availability"] == "sample_only" for item in payload["results"]))

    def test_search_respects_limit_and_budget(self):
        response = self.client.get(
            "/api/v1/products/search",
            params={"q": "shirt", "budget_inr": 3000, "limit": 1},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertLessEqual(len(payload["results"]), 1)
        self.assertTrue(all(item["price"] <= 3000 for item in payload["results"]))

    def test_search_rejects_unknown_persona(self):
        response = self.client.get(
            "/api/v1/products/search",
            params={"q": "headphones", "budget_inr": 5000, "persona": "Unknown"},
        )
        self.assertEqual(response.status_code, 422)

    def test_search_rejects_blank_query(self):
        response = self.client.get(
            "/api/v1/products/search",
            params={"q": "   ", "budget_inr": 5000},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()

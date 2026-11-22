"""Small, explicit smoke benchmark for top-result relevance.

Expected categories are hand-labelled against the synthetic catalogue.
This is a regression check, not a statistically validated quality metric.
"""

import json
import unittest
from pathlib import Path

from recommendations import PERSONAS, recommend_products


CASES = [
    ("notebook", "Budget-conscious student", "student_essentials"),
    ("planner", "Budget-conscious student", "student_essentials"),
    ("calculator", "Budget-conscious student", "student_essentials"),
    ("shirt", "Campus style seeker", "fashion"),
    ("hoodie", "Campus style seeker", "fashion"),
    ("jeans", "Campus style seeker", "fashion"),
    ("sneakers", "Campus style seeker", "footwear"),
    ("running shoes", "Fitness and active lifestyle shopper", "footwear"),
    ("sandals", "Campus style seeker", "footwear"),
    ("gaming mouse", "Competitive gamer", "gaming"),
    ("gaming keyboard", "Competitive gamer", "gaming"),
    ("controller", "Competitive gamer", "gaming"),
    ("headphones", "Tech enthusiast", "audio"),
    ("bluetooth speaker", "Tech enthusiast", "audio"),
    ("earphones", "Tech enthusiast", "audio"),
    ("webcam", "Tech enthusiast", "electronics"),
    ("power bank", "Tech enthusiast", "electronics"),
    ("usb c hub", "Tech enthusiast", "electronics"),
    ("smart plug", "Tech enthusiast", "gadgets"),
    ("bluetooth tracker", "Tech enthusiast", "gadgets"),
    ("desk clock", "Tech enthusiast", "gadgets"),
    ("wallet", "Value-first everyday shopper", "accessories"),
    ("backpack", "Budget-conscious student", "accessories"),
    ("umbrella", "Value-first everyday shopper", "accessories"),
    ("yoga mat", "Fitness and active lifestyle shopper", "fitness"),
    ("resistance band", "Fitness and active lifestyle shopper", "fitness"),
    ("foam roller", "Fitness and active lifestyle shopper", "fitness"),
    ("cushion", "Value-first everyday shopper", "home"),
    ("laundry organizer", "Value-first everyday shopper", "home"),
    ("lunch box", "Budget-conscious student", "home"),
]


class RecommendationBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "data" / "products.json"
        with path.open("r", encoding="utf-8") as source:
            cls.products = json.load(source)["products"]

    def test_benchmark_cases_have_valid_personas_and_expected_categories(self):
        for query, persona, expected_category in CASES:
            with self.subTest(query=query):
                self.assertIn(persona, PERSONAS)
                self.assertTrue(
                    any(p["category"] == expected_category for p in self.products)
                )

    def test_top_result_category_matches_hand_labelled_expectation(self):
        failures = []
        for query, persona, expected_category in CASES:
            results = recommend_products(self.products, query, 5000, persona)
            if not results or results[0]["category"] != expected_category:
                actual = results[0]["category"] if results else "NO_MATCH"
                failures.append(
                    f"{query!r}: expected {expected_category}, got {actual}"
                )
        self.assertFalse(failures, "\\n".join(failures))


if __name__ == "__main__":
    unittest.main()

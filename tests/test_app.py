import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class StreamlitAppTests(unittest.TestCase):
    def run_app(self):
        return AppTest.from_file(str(APP_PATH)).run(timeout=20)

    def test_app_loads_without_exceptions(self):
        app = self.run_app()
        self.assertFalse(app.exception)
        self.assertTrue(app.title)

    def test_search_displays_sample_recommendations(self):
        app = self.run_app()
        app.text_input[0].set_value("headphones")
        app.button[0].click()
        app.run(timeout=20)
        self.assertFalse(app.exception)
        self.assertTrue(app.success)
        self.assertTrue(
            any("Wireless Headphones" in element.value for element in app.subheader)
            or any("Wired Earphones" in element.value for element in app.subheader)
        )

    def test_empty_search_shows_validation_warning(self):
        app = self.run_app()
        app.button[0].click()
        app.run(timeout=20)
        self.assertFalse(app.exception)
        self.assertTrue(app.warning)

    def test_unmatched_search_shows_no_results_message(self):
        app = self.run_app()
        app.text_input[0].set_value("unobtainium")
        app.button[0].click()
        app.run(timeout=20)
        self.assertFalse(app.exception)
        self.assertTrue(app.info)


if __name__ == "__main__":
    unittest.main()

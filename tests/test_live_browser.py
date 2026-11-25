"""Live browser smoke tests for the deployed Streamlit application.

Run with AI_DEAL_AGENT_URL set to the deployment URL and Playwright Chromium installed.
"""
import os
import re
import unittest

from playwright.sync_api import sync_playwright


APP_URL = os.getenv(
    "AI_DEAL_AGENT_URL",
    "https://ai-deal-agent-8rzwdsvxlrxjwtmpripdjw.streamlit.app/",
)


class LiveBrowserSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(accept_downloads=True)
        self.page = self.context.new_page()
        response = self.page.goto(APP_URL, wait_until="domcontentloaded", timeout=120_000)
        self.assertIsNotNone(response, "The deployment returned no HTTP response.")
        self.assertLess(response.status, 400, f"App returned HTTP {response.status}")
        self.page.locator('[data-testid="stAppViewContainer"]').wait_for(timeout=120_000)
        self.page.get_by_role(
            "heading", name="🛍️ AI Deal Discovery & Marketing Agent"
        ).wait_for(timeout=60_000)

    def tearDown(self):
        self.context.close()

    def search(self, query):
        self.page.get_by_label("What product are you looking for?").fill(query)
        self.page.get_by_role(
            "button", name=re.compile("Find personalized deals")
        ).click()
        self.page.wait_for_timeout(1200)

    def test_homepage_loads_and_shows_sample_catalogue_disclaimer(self):
        self.assertTrue(
            self.page.get_by_text(re.compile("illustrative sample products")).is_visible()
        )
        self.assertTrue(self.page.get_by_label("Choose a shopper persona").is_visible())

    def test_search_returns_headphone_recommendations(self):
        self.search("headphones")
        self.assertTrue(
            self.page.get_by_text(
                re.compile("Found \\d+ matching sample product", re.I)
            ).is_visible()
        )
        self.assertTrue(
            self.page.get_by_role("heading", name=re.compile("Headphones|Earphones", re.I)).first.is_visible()
        )

    def test_empty_search_shows_validation(self):
        self.search("")
        self.assertTrue(
            self.page.get_by_text("Enter a product or category to search.").is_visible()
        )

    def test_unmatched_search_shows_no_results(self):
        self.search("unobtainium")
        self.assertTrue(
            self.page.get_by_text(re.compile("No sample products matched")).is_visible()
        )

    def test_persona_can_be_changed_and_used_for_search(self):
        persona = self.page.get_by_label("Choose a shopper persona")
        persona.select_option(label="Competitive gamer")
        self.search("gaming keyboard")
        self.assertTrue(
            self.page.get_by_text(re.compile("Found \\d+ matching sample product", re.I)).is_visible()
        )
        self.assertTrue(self.page.get_by_text("Competitive gamer", exact=True).first.is_visible())

    def test_feedback_can_be_submitted(self):
        self.search("headphones")
        self.page.get_by_text("Was this recommendation relevant?").first.wait_for()
        self.page.get_by_text("👍 Relevant").first.click()
        self.page.get_by_role("button", name="Submit feedback").first.click()
        self.assertTrue(
            self.page.get_by_text("Feedback recorded for this session.").is_visible()
        )

    def test_session_analytics_csv_can_be_downloaded(self):
        self.search("headphones")
        self.page.get_by_text("📈 Session analytics and feedback").click()
        with self.page.expect_download(timeout=30_000) as download_info:
            self.page.get_by_role(
                "button", name="Download session analytics (CSV)"
            ).click()
        download = download_info.value
        self.assertEqual(download.suggested_filename, "deal-agent-session-analytics.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)

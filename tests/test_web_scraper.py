import unittest
from unittest.mock import patch, MagicMock
import sqlite3

import web_scraper

# Sample HTML for testing
HTML_SAMPLE = """
<html>
  <body>
    <h2 class="entry-title"><a href="http://example.com/deal1">Delta: New York – Los Angeles. $99 (Basic Economy) / $129 (Regular Economy)</a></h2>
    <h2 class="entry-title"><a href="http://example.com/deal2">United: San Francisco – Tokyo. $450.</a></h2>
    <h2 class="entry-title"><a href="http://example.com/deal3">Bad format deal</a></h2>
  </body>
</html>
"""

class TestScraper(unittest.TestCase):

    @patch('web_scraper.requests.get')
    def test_scrape_successful(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = HTML_SAMPLE
        mock_get.return_value = mock_response

        results = web_scraper.scrape()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][1], "Delta")
        self.assertEqual(results[1][1], "United")
        self.assertIn("http://example.com/deal1", results[0][0])

    @patch('web_scraper.requests.get')
    def test_scrape_http_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        results = web_scraper.scrape()
        self.assertEqual(results, [])

    def test_init_and_insert_db(self):
        flights = [
            ["http://example.com/deal1", "Delta", "New York", "Los Angeles", 99.0, 129.0],
            ["http://example.com/deal2", "United", "San Francisco", "Tokyo", None, 450]
        ]

        conn = sqlite3.connect(":memory:")
        web_scraper.init_db(conn)
        web_scraper.insert_db(flights, conn)

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flight_deals")
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][2], "Delta")


    @patch('web_scraper.scrape')
    @patch('web_scraper.init_db')
    @patch('web_scraper.insert_db')
    def test_use_scraper(self, mock_insert, mock_init, mock_scrape):
        mock_scrape.return_value = [["link", "Airline", "Dep", "Arr", 100, 120]]
        web_scraper.use_scraper()
        mock_init.assert_called_once()
        mock_insert.assert_called_once()


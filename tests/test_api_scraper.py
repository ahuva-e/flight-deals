import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import requests
import code.api_scraper as api_scraper


class TestScrapeAPI(unittest.TestCase):

    @patch("api_scraper.st.secrets", new=MagicMock(API_KEY="fakekey"))
    @patch("api_scraper.requests.get")
    def test_scrape_api_success(self, mock_get):
        sample_api_response = {
            "forecast": {
                "forecastday": [
                    {
                        "date": "2024-05-01",
                        "day": {
                            "maxtemp_c": 25.5,
                            "mintemp_c": 15.2,
                            "condition": {"text": "Sunny"}
                        }
                    },
                    {
                        "date": "2024-05-02",
                        "day": {
                            "maxtemp_c": 22.3,
                            "mintemp_c": 13.1,
                            "condition": {"text": "Cloudy"}
                        }
                    }
                ]
            }
        }

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response

        results = api_scraper.scrape_api("London")

        # Expected formatted dates
        expected_date_1 = datetime.strptime("2024-05-01", "%Y-%m-%d").strftime("%-d %B, %Y")
        expected_date_2 = datetime.strptime("2024-05-02", "%Y-%m-%d").strftime("%-d %B, %Y")

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], [expected_date_1, 25.5, 15.2, "Sunny"])
        self.assertEqual(results[1], [expected_date_2, 22.3, 13.1, "Cloudy"])

    @patch("api_scraper.st.secrets", new=MagicMock(API_KEY="fakekey"))
    @patch("api_scraper.requests.get")
    def test_scrape_api_handles_empty_forecast(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"forecast": {"forecastday": []}}
        mock_get.return_value = mock_response

        results = api_scraper.scrape_api("Emptyville")
        self.assertEqual(results, [])

    @patch("api_scraper.st.secrets", new=MagicMock(API_KEY="fakekey"))
    @patch("api_scraper.requests.get")
    def test_scrape_api_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("500 Server Error")

        with patch("api_scraper.st.error") as mock_error:
            results = api_scraper.scrape_api("BadCity")
            self.assertEqual(results, [])
            mock_error.assert_called_once()

    @patch("api_scraper.st.secrets", new=MagicMock(API_KEY="fakekey"))
    @patch("api_scraper.requests.get")
    def test_scrape_api_bad_data(self, mock_get):
        # Simulate invalid structure
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid_key": "oops"}
        mock_get.return_value = mock_response

        with patch("api_scraper.st.error") as mock_error:
            results = api_scraper.scrape_api("Nowhere")
            self.assertEqual(results, [])
            self.assertTrue(mock_error.called)

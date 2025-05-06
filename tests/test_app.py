import pytest
from unittest.mock import patch
import pandas as pd
from types import SimpleNamespace
import streamlit as st
import code.streamlit_app as streamlit_app


class SessionStateMock(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


@pytest.fixture
def mock_flight_data():
    return pd.DataFrame([
        [1, "http://example.com/deal1", "Delta", "New York", "Los Angeles", 99.0, 129.0],
        [2, "http://example.com/deal2", "United", "San Francisco", "Tokyo", None, 450.0]
    ], columns=["id", "link", "airline", "departure", "arrival", "basic_price", "regular_price"])


@pytest.fixture
def mock_session_state(monkeypatch):
    mock_state = SimpleNamespace()
    mock_state.flight = None
    mock_state.messages = []
    monkeypatch.setattr(st, "session_state", mock_state)
    return mock_state


def test_select_data_returns_selection(mock_session_state):
    df = pd.DataFrame([{
        "link": "http://example.com",
        "airline": "TestAir",
        "departure": "NYC",
        "arrival": "London",
        "basic_price": 99.0,
        "regular_price": 149.0
    }])
    with patch("streamlit.selectbox", return_value="NYC → London | TestAir ($149.00)"), \
         patch("streamlit.button", return_value=True), \
         patch("streamlit.rerun"):
        result = streamlit_app.select_data(df)
        assert result.iloc[0]['airline'] == "TestAir"


def test_show_details(mock_session_state):
    # Create a sample one-row flight DataFrame
    flight = pd.DataFrame([{
        "link": "http://example.com",
        "airline": "TestAir",
        "departure": "NYC",
        "arrival": "London",
        "basic_price": 99.0,
        "regular_price": 149.0
    }])

    mock_weather = [["1 Jan, 2025", 10, 5, "Sunny"]] * 7

    with patch("streamlit_app.api_scraper.scrape_api", return_value=mock_weather), \
         patch("streamlit.markdown"), patch("streamlit.html"):
        streamlit_app.show_details(flight)


@patch("streamlit_app.st")
def test_plot_chart(mock_st, mock_flight_data):
    streamlit_app.plot_chart(mock_flight_data)
    assert mock_st.plotly_chart.called

import requests
import streamlit as st
import pandas as pd


def scrape_api(location):
    try:
        link = f"http://api.weatherapi.com/v1/forecast.json?key={st.secrets.API_KEY}&q={location}&days=7"
        response = requests.get(link)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        forecast_details = []
        for day in data["forecast"]["forecastday"]:
            # Extracting the date, max temperature, min temperature, and condition
            date = day["date"]
            # Convert date to a more readable format
            date = pd.to_datetime(date).strftime("%-d %B, %Y")
            # Extracting max and min temperature
            # and weather condition
            max_temp = day["day"]["maxtemp_c"]
            min_temp = day["day"]["mintemp_c"]
            condition = day["day"]["condition"]["text"]

            details = [date, max_temp, min_temp, condition]
            forecast_details.append(details)

        return forecast_details

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")
    except (KeyError, TypeError, ValueError) as e:
        st.error(f"Invalid data format: {e}")
    return []

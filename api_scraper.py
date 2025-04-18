import requests
import sqlite3 # do i need a database here?


def scrape_api(location):
    API_KEY = "a14675cdd4804740828195633250904"
    link = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=7"
    response = requests.get(link)
    data = response.json()
    forecast_details = []
    for day in data["forecast"]["forecastday"]:
        # Extracting the date, max temperature, min temperature, and condition
        date = day["date"]
        max_temp = day["day"]["maxtemp_c"]
        min_temp = day["day"]["mintemp_c"]
        condition = day["day"]["condition"]["text"]
        
        details = [date, max_temp, min_temp, condition]
        forecast_details.append(details)

    return forecast_details

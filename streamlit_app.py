import streamlit as st
import pandas as pd
import sqlite3
import web_scraper
import api_scraper


def streamlit_app():
    web_scraper.use_scraper()  # gets data
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM flight_deals;""")
    df = pd.DataFrame(data)
    conn.close()

    df.columns = ["id", "link", "airline", "departure", "arrival", "basic_price", "regular_price"]

    st.header("Flights - final project")
    st.markdown("### Ahuva Ebert")

    col_config = {
                "id": None,
                "link": st.column_config.LinkColumn(
                    "View Deal"
                    ),
                "airline": "Airline",
                "departure": "Leave from",
                "arrival": "Destination",
                "basic_price": st.column_config.NumberColumn(
                    "Basic Fare",
                    format="$%d"
                    ),
                "regular_price": st.column_config.NumberColumn(
                    "Regular Fare",
                    format="$%d"
                    )
                }

    select, details = st.tabs(["Select a flight", "View flight details"])

    with select:
        st.write("choose a flight:")
        event = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config=col_config,
            on_select="rerun",
            selection_mode="single-row")
        index = event.selection.rows
        if index:
            flight = df.iloc[index]
            st.session_state.flight = flight
        else:
            flight = None


    with details:
        if flight is not None:
            st.write(flight)
            weather = api_scraper.scrape_api(flight["arrival"])

            day1, day2, day3, day4, day5, day6, day7 = st.columns(7)
            for i in range(7):
                with eval(f"day{i+1}"):
                    st.markdown(f"### {weather[i][0]}")
                    st.markdown(f"🌡️ High: {weather[i][1]}°C")
                    st.markdown(f"❄️ Low:  {weather[i][2]}°C")
                    st.markdown(f"{weather[i][3]}")
        else:
            st.markdown("##### Please select a flight to view details and weather information.")

streamlit_app()

import streamlit as st
import math
import pandas as pd
import plotly.express as px
import sqlite3
import web_scraper as web_scraper
import api_scraper as api_scraper
import chatbot as chatbot


def streamlit_app():
    st.set_page_config(page_title="Flight Deals", page_icon=":airplane:", layout="wide")

    web_scraper.use_scraper()  # gets data
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM flight_deals;""")
    df = pd.DataFrame(data)
    conn.close()

    df.columns = ["id", "link", "airline", "departure", "arrival", "basic_price", "regular_price"]

    st.header(":airplane: Flight Deals Explorer")

    col_config = {
        "id": None,
        "link": st.column_config.LinkColumn(
            "View Deal"),
        "airline": "Airline",
        "departure": "Leave from",
        "arrival": "Destination",
        "basic_price": st.column_config.NumberColumn(
            "Basic Fare",
            format="$%d"),
        "regular_price": st.column_config.NumberColumn(
            "Regular Fare",
            format="$%d")}

    # Initialise session state
    if "flight" not in st.session_state:
        st.session_state.flight = None
    # Display selected flight above tabs
    if st.session_state.flight is not None:
        flight = st.session_state.flight.reset_index(drop=True)
        st.info(f"✈️ **Selected flight:** {flight.loc[0, 'departure']} → {flight.loc[0, 'arrival']} | "
                f"**Airline:** {flight.loc[0, 'airline']} | 💵 ${flight.loc[0, 'regular_price']:.2f}")
    else:
        st.warning("No flight selected yet.")

    # Create tabs
    select, details, chart, chat = st.tabs(["Select a flight", "View flight details", "View data in bar chart", "Ask the chatbot"])

    with select:
        st.session_state.flight = select_data(df)

    with details:
        show_details(st.session_state.flight)

    with chart:
        plot_chart(df)

    with chat:
        chatbot.chat()

    # Add footer
    st.markdown("*Flight data scraped from [theflightdeal.com](https://theflightdeal.com). Weather information scraped from [weatherapi.com](https://www.weatherapi.com).*")


def select_data(df: pd.DataFrame):
    options = {
        f"{row['departure']} → {row['arrival']} | {row['airline']} (${row['regular_price']:.2f})": i
        for i, row in df.iterrows()
    }
    try:
        selected_label = st.selectbox("Select a flight", list(options.keys()), index=None, placeholder="Select a flight", label_visibility="hidden")
        index = options[selected_label]
        selected_flight = df.iloc[[index]]  # Keep it as DataFrame with one row
        if st.button("Select flight"):
            st.session_state.flight = selected_flight
            st.rerun()  # rerun to update the selected flight
        return selected_flight
    except KeyError:
        pass


def show_details(flight):

    if flight is not None:

        st.markdown(f"##### You can view the flight [here]({flight["link"].values[0]}).")
        st.markdown(f"**{flight['airline'].values[0]}** flight from **{flight['departure'].values[0]} → {flight['arrival'].values[0]}**")

        # if there is only one price bound
        if math.isnan(flight['basic_price'].values[0]):
            st.markdown(f"**Flight cost:** \${flight['regular_price'].values[0]:.2f}")
        # otherwise, show both prices
        else:
            st.markdown(f"**Basic Fare:** \${flight['basic_price'].values[0]:.2f} | **Regular Fare:** \${flight['regular_price'].values[0]:.2f}")

        st.markdown(f"##### :sun_small_cloud: Weather forecast at {flight['arrival'].values[0]} for the next 7 days :sun_behind_rain_cloud:")
        # Get weather data
        weather = api_scraper.scrape_api(flight["arrival"])

        # Add horizontal scrollable container using raw HTML
        card_html = """
            <style>
                .scrolling-wrapper {
                    overflow-x: auto;
                    display: flex;
                    flex-wrap: nowrap;
                }
                .card {
                    flex: 0 0 auto;
                    width: 200px;
                    margin-right: 10px;
                    background: #f1f1f1;
                    padding: 1em;
                    border-radius: 10px;
                }
            </style>

            <div class="scrolling-wrapper">
            """
        # add cards with weather data
        for i in range(7):
            card_html += f"""
                <div class="card">
                    <h4>{weather[i][0]}</h4>
                    <p>🌡️ High: {weather[i][1]}°C</p>
                    <p>❄️ Low:  {weather[i][2]}°C</p>
                    <p>{weather[i][3]}</p>
                </div>
            """
        card_html += "</div>"
        st.html(card_html)

    else:
        st.markdown("##### Please select a flight to view details and weather information.")


def plot_chart(df):
    data = df[["airline", "arrival", "regular_price"]]

    st.subheader("📊 Average Flight Prices by Destination and Airline")

    # load and clean data
    data = df[["airline", "arrival", "regular_price"]]
    data['regular_price'] = pd.to_numeric(data['regular_price'], errors='raise')
    data = data.dropna(subset=['arrival', 'regular_price', 'airline'])
    data['arrival'] = data['arrival'].str.strip().str.title()
    data['airline'] = data['airline'].str.strip().str.title()

    # aggregate so we can see the average price for each destination
    # otherwise it shows a cumulative sum of the prices
    df_agg = (
        data
        .groupby(['arrival', 'airline'], as_index=False)
        .regular_price
        .mean()
        .rename(columns={'regular_price': 'avg_price'})
    )

    fig = px.bar(
        df_agg,
        x='arrival',
        y='avg_price',
        color='airline',
        barmode='group',
        labels={'avg_price': 'Price ($)', 'arrival': 'Destination', 'airline': 'Airline'},
    )

    fig.update_yaxes(
        type='linear',
        range=[0, df_agg['avg_price'].max() * 1.1],
        dtick=50,
        title='Price ($)'
    )
    fig.update_layout(height=800)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    streamlit_app()

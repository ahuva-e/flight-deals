import requests
from bs4 import BeautifulSoup as bs
import re
import sqlite3


# scraping flight deal details from www.theflightdeal.com
def scrape():
    link = "https://www.theflightdeal.com/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Pretends to be a web browser
    response = requests.get(link, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data:", response.status_code)
        return []
    soup = bs(response.text, 'html.parser')

    deals = soup.find_all('h2', class_='entry-title')

    flights = []
    for deal in deals:
        link = deal.find("a")["href"]
        text = deal.get_text()

        pattern_1 = r"^(.*?):\s*(.*?)\s*[–-]\s*(.*?)(?: +\(and vice versa\))?\.\s*\$(\d+)\s*\(.*?\)\s*/\s*\$(\d+)\s*\(.*?\)"
        pattern_2 = r"^(.*?):\s*(.*?)\s*[–-]\s*(.*?)(?: +\(and vice versa\))?\.\s*\$(\d+)\.?\s*(.*?)$"
        match_1 = re.search(pattern_1, text)
        match_2 = re.search(pattern_2, text)

        if match_1:
            airline = match_1.group(1)
            departure = match_1.group(2)
            arrival = match_1.group(3)
            price_basic = float(match_1.group(4))
            price_regular = float(match_1.group(5))

            flights.append([link, airline, departure, arrival, price_basic, price_regular])

        elif match_2:
            airline = match_2.group(1)
            departure = match_2.group(2)
            arrival = match_2.group(3)
            price_regular = match_2.group(4)
            flights.append([link, airline, departure, arrival, None, price_regular])

        else:
            print("No regex match for:", text)

    return flights


def init_db(conn=None):
    # Initialises the flight_deals table in the database.
    close_conn = False
    if conn is None:
        conn = sqlite3.connect("flights.db")
        close_conn = True

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS flight_deals(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        link TEXT UNIQUE,
                        airline TEXT,
                        departure TEXT,
                        arrival TEXT,
                        basic_price REAL,
                        regular_price REAL
                   )
                   """)
    conn.commit()

    if close_conn:
        conn.close()


def insert_db(flights: list, conn=None):
    close_conn = False
    if conn is None:
        conn = sqlite3.connect("flights.db")
        close_conn = True

    cursor = conn.cursor()
    for flight in flights:
        cursor.execute("""INSERT OR IGNORE INTO flight_deals
                       (link, airline, departure, arrival, basic_price, regular_price)
                       values(?, ?, ?, ?, ?, ?)""", flight)
    conn.commit()

    if close_conn:
        conn.close()


def use_scraper():
    flights = scrape()
    init_db()
    insert_db(flights)

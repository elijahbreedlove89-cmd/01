import requests
import random
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

# ------------------------------------------
# USER-AGENT ROTATION
# ------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# ------------------------------------------
# REGION → COUNTRY → CITIES
# ------------------------------------------
REGIONS = {
    "Western & Southern Europe": {
        "Portugal": ["Lisbon", "Porto", "Braga"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Malaga"],
        "Italy": ["Rome", "Milan", "Florence"],
        "Greece": ["Athens", "Thessaloniki"],
        "Malta": ["Valletta"],
        "Cyprus": ["Nicosia", "Limassol"],
        "Croatia": ["Zagreb", "Split", "Dubrovnik"],
        "France": ["Paris", "Lyon", "Bordeaux"],
        "Germany": ["Berlin", "Munich"],
        "Ireland": ["Dublin", "Cork"],
    },
    "Eastern Europe & The Balkans": {
        "Estonia": ["Tallinn"],
        "Czechia": ["Prague", "Brno"],
        "Hungary": ["Budapest"],
        "Poland": ["Warsaw", "Krakow"],
        "Romania": ["Bucharest", "Cluj-Napoca"],
        "Bulgaria": ["Sofia", "Plovdiv"],
        "Slovenia": ["Ljubljana"],
        "Slovakia": ["Bratislava"],
        "Latvia": ["Riga"],
        "Lithuania": ["Vilnius"],
        "Albania": ["Tirana"],
        "Montenegro": ["Podgorica", "Tivat"],
        "Georgia": ["Tbilisi", "Batumi"],
        "Serbia": ["Belgrade"],
    },
    "Latin America": {
        "Mexico": ["Mexico City", "Playa del Carmen", "Guadalajara"],
        "Costa Rica": ["San Jose", "Tamarindo"],
        "Colombia": ["Medellin", "Bogota"],
        "Panama": ["Panama City"],
        "Brazil": ["Sao Paulo", "Rio de Janeiro", "Florianopolis"],
        "Argentina": ["Buenos Aires"],
        "Uruguay": ["Montevideo"],
        "Chile": ["Santiago"],
        "Ecuador": ["Quito", "Cuenca"],
        "Belize": ["Belize City"],
    },
    "Asia-Pacific": {
        "Thailand": ["Bangkok", "Chiang Mai", "Phuket"],
        "Vietnam": ["Ho Chi Minh City", "Hanoi", "Da Nang"],
        "Indonesia": ["Denpasar", "Ubud"],
        "Malaysia": ["Kuala Lumpur", "Penang"],
        "Philippines": ["Manila", "Cebu City"],
        "Japan": ["Tokyo", "Osaka", "Kyoto"],
        "South Korea": ["Seoul", "Busan"],
        "Taiwan": ["Taipei"],
        "Sri Lanka": ["Colombo"],
    },
    "Middle East & Africa": {
        "UAE": ["Dubai", "Abu Dhabi"],
        "Turkey": ["Istanbul", "Antalya"],
        "South Africa": ["Cape Town"],
        "Mauritius": ["Port Louis"],
        "Morocco": ["Casablanca", "Marrakech"],
    },
    "Island Life": {
        "Barbados": ["Bridgetown"],
        "Bermuda": ["Hamilton"],
    }
}

# ------------------------------------------
# SCRAPER FUNCTIONS
# ------------------------------------------
def fetch_page(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    delay = random.uniform(2, 5)
    print(f"Sleeping {delay:.2f}s before requesting {url}")
    time.sleep(delay)

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_cost_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "data_wide_table"})
    if not table:
        return None

    rows = table.find_all("tr")
    items = []
    prices = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            items.append(cols[0].get_text(strip=True))
            prices.append(cols[1].get_text(strip=True))

    df = pd.DataFrame({"Item": items, "Price": prices})
    return df

def city_to_url(city):
    return f"https://www.numbeo.com/cost-of-living/in/{city.replace(' ', '-')}"

# ------------------------------------------
# MAIN SCRAPER LOOP
# ------------------------------------------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    master_rows = []  # will hold all cities' data

    for region, countries in REGIONS.items():
        print(f"\n=== {region} ===")

        for country, cities in countries.items():
            print(f"\n  {country}:")

            for city in cities:
                url = city_to_url(city)

                try:
                    html = fetch_page(url)
                    df = parse_cost_table(html)

                    if df is not None:
                        # Add metadata columns
                        df["Region"] = region
                        df["Country"] = country
                        df["City"] = city

                        # Save individual CSV
                        filename = f"data/{country}_{city}.csv".replace(" ", "_")
                        df.to_csv(filename, index=False)
                        print(f"    {city}: Saved {len(df)} items → {filename}")

                        # Add to master list
                        master_rows.append(df)

                    else:
                        print(f"    {city}: No table found")

                except Exception as e:
                    print(f"    {city}: ERROR - {e}")

    # ------------------------------------------
    # BUILD MASTER CSV
    # ------------------------------------------
    if master_rows:
        master_df = pd.concat(master_rows, ignore_index=True)
        master_df.to_csv("data/master_cost_of_living.csv", index=False)
        print("\nMaster CSV saved → data/master_cost_of_living.csv")
        print(f"Total rows: {len(master_df)}")
    else:
        print("\nNo data scraped — master CSV not created.")

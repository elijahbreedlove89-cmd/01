import requests
import random
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

# ------------------------------------------
# EXPANDED USER-AGENT ROTATION
# ------------------------------------------
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",

    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",

    # Firefox Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",

    # Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

# ------------------------------------------
# REGION → COUNTRY → CITIES
# ------------------------------------------
REGIONS = {
    "Western & Southern Europe": {
        "Portugal": ["Lisbon", "Porto", "Braga"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Malaga"], # Fixed string grouping typo
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
# URL OVERRIDES FOR TRICKY CITIES
# ------------------------------------------
URL_OVERRIDES = {
    "San Jose": "San-Jose-Costa-Rica",
    "Hamilton": "Hamilton-Bermuda",
}

def city_to_url(city):
    """
    Checks for known geographical overlaps before formatting the Numbeo URL.
    """
    if city in URL_OVERRIDES:
        formatted_city = URL_OVERRIDES[city]
    else:
        # Standard formatting: replace spaces with dashes
        formatted_city = city.replace(' ', '-')
       
    return f"https://www.numbeo.com/cost-of-living/in/{formatted_city}"

# ------------------------------------------
# FETCH PAGE WITH ROBUST ERROR HANDLING
# ------------------------------------------

def fetch_page(url, retries=3):
    for attempt in range(retries):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en;q=0.7"]),
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive"
        }

        delay = random.uniform(5, 12)
        print(f"Sleeping {delay:.2f}s before requesting {url}")
        time.sleep(delay)

        try:
            # 15-second timeout prevents infinite hanging on dead connections
            response = requests.get(url, headers=headers, timeout=15)
           
            # Check for Cloudflare/CAPTCHA disguised as a 200 OK
            if "Just a moment..." in response.text or "cloudflare" in response.text.lower():
                print("Cloudflare CAPTCHA detected! IP temporarily flagged.")
                time.sleep(120)  # Massive penalty sleep
                continue         # Force a retry

            response.raise_for_status()
            return response.text

        except requests.exceptions.HTTPError as e:
            status = response.status_code
           
            # 404 means the URL is wrong or doesn't exist. Do not retry.
            if status == 404:
                print(f"404 Error: Page not found for {url}. Skipping.")
                return None
               
            # Treat 403 (Forbidden) and 503 (Unavailable) the same as 429 (Rate limited)
            elif status in [429, 403, 503]:
                cooldown = (attempt + 1) * random.uniform(30, 60)
                print(f"HTTP {status} Block. Cooling down for {cooldown:.1f}s...")
                time.sleep(cooldown)
            else:
                print(f"HTTP {status} Error. Retrying...")
                time.sleep(10)
               
        # Catch network blips, connection resets, and timeouts entirely
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}. Retrying...")
            time.sleep(15)

    print(f"Failed to fetch {url} after {retries} retries.")
    return None

# ------------------------------------------
# PARSE COST TABLE
# ------------------------------------------
def parse_cost_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "data_wide_table"})
    if not table:
        return None

    rows = table.find_all("tr")
    items, prices = [], []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            items.append(cols[0].get_text(strip=True))
            prices.append(cols[1].get_text(strip=True))

    return pd.DataFrame({"Item": items, "Price": prices})

# ------------------------------------------
# MAIN SCRAPER LOOP
# ------------------------------------------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    master_rows = []

    for region, countries in REGIONS.items():
        print(f"\n=== {region} ===")

        for country, cities in countries.items():
            print(f"\n  {country}:")

            for city in cities:
                url = city_to_url(city)

                try:
                    html = fetch_page(url)
                   
                    # Skip parsing if the page failed to load (e.g., 404)
                    if html is None:
                        continue

                    df = parse_cost_table(html)

                    # Ensure the dataframe isn't completely empty before saving
                    if df is not None and not df.empty:
                        df["Region"] = region
                        df["Country"] = country
                        df["City"] = city

                        filename = f"data/{country}_{city}.csv".replace(" ", "_")
                        df.to_csv(filename, index=False)
                        print(f"    {city}: Saved {len(df)} items → {filename}")

                        master_rows.append(df)
                    else:
                        print(f"    {city}: No table found")

                except Exception as e:
                    print(f"    {city}: ERROR - {e}")

            # Country-level cooldown
            cooldown = random.uniform(20, 45)
            print(f"Cooling down {cooldown:.1f}s after finishing {country}...")
            time.sleep(cooldown)

        # Region-level cooldown
        region_cooldown = random.uniform(60, 120)
        print(f"Region cooldown: {region_cooldown:.1f}s")
        time.sleep(region_cooldown)

    # ------------------------------------------
    # MASTER CSV EXPORT
    # ------------------------------------------
    if master_rows:
        master_df = pd.concat(master_rows, ignore_index=True)
        master_df.to_csv("data/master_cost_of_living.csv", index=False)
        print("\nMaster CSV saved → data/master_cost_of_living.csv")
        print(f"Total rows: {len(master_df)}")
    else:
        print("\nNo data scraped — master CSV not created.")
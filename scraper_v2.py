import requests
import random
import time
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

def parse_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    return title.get_text(strip=True) if title else "No title found"

def city_to_url(city):
    city_slug = city.replace(" ", "-")
    return f"https://www.numbeo.com/cost-of-living/in/{city_slug}"

# ------------------------------------------
# MAIN SCRAPER LOOP
# ------------------------------------------
if __name__ == "__main__":
    for region, countries in REGIONS.items():
        print(f"\n=== {region} ===")

        for country, cities in countries.items():
            print(f"\n  {country}:")

            for city in cities:
                url = city_to_url(city)

                try:
                    html = fetch_page(url)
                    title = parse_title(html)
                    print(f"    {city}: {title}")
                except Exception as e:
                    print(f"    {city}: ERROR - {e}")

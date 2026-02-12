import requests
import random
import time
from bs4 import BeautifulSoup

# A small pool of realistic browser user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def fetch_numbeo_page(city_url):
    # Pick a random user-agent
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    # Random delay between 2 and 5 seconds
    delay = random.uniform(2, 5)
    print(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)

    print(f"Requesting: {city_url}")
    response = requests.get(city_url, headers=headers)
    response.raise_for_status()  # Throw error if request failed

    return response.text

def parse_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    return title_tag.get_text(strip=True) if title_tag else "No title found"

if __name__ == "__main__":
    # Example Numbeo city page
    url = "https://www.numbeo.com/cost-of-living/in/San-Francisco"

    html = fetch_numbeo_page(url)
    title = parse_title(html)

    print("Page Title:", title)

import pandas as pd
import requests
import json
import os

def process_cost_of_living_data(input_filename, output_filename):
    """
    Reads the cost of living CSV, cleans the Price column, maps Countries
    to Currency codes, freezes exchange rates, and converts to USD.
    """
    print(f"Reading data from {input_filename}...")
    try:
        df = pd.read_csv(input_filename)
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}. Please check the file path.")
        return

    # 1. Clean the Price column
    df['Price Cleaned'] = (
        df['Price']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.extract(r'(\d+\.?\d*)')[0]
        .astype(float)
    )

    # 2. Map Country to Currency
    currency_map = {
        'portugal': 'EUR', 'spain': 'EUR', 'italy': 'EUR', 'greece': 'EUR',
        'malta': 'EUR', 'cyprus': 'EUR', 'croatia': 'EUR', 'france': 'EUR',
        'germany': 'EUR', 'ireland': 'EUR', 'estonia': 'EUR', 'chechia': 'CZK',
        'czechia': 'CZK', 'hungary': 'HUF', 'poland': 'PLN', 'romania': 'RON',
        'bulgaria': 'BGN', 'slovenia': 'EUR', 'slovakia': 'EUR', 'latvia': 'EUR',
        'lithuania': 'EUR', 'albania': 'ALL', 'montenegro': 'EUR', 'georgia': 'GEL',
        'serbia': 'RSD', 'mexico': 'MXN', 'costa rica': 'CRC', 'colombia': 'COP',
        'panama': 'PAB', 'brazil': 'BRL', 'argentina': 'ARS', 'uruguay': 'UYU',
        'chile': 'CLP', 'ecuador': 'USD', 'belize': 'BZD', 'thailand': 'THB',
        'vietnam': 'VND', 'indonesia': 'IDR', 'malaysia': 'MYR', 'philippines': 'PHP',
        'japan': 'JPY', 'south korea': 'KRW', 'taiwan': 'TWD', 'sri lanka': 'LKR',
        'uae': 'AED', 'united arab emirates': 'AED', 'turkey': 'TRY',
        'south africa': 'ZAR', 'mauritius': 'MUR', 'morocco': 'MAD',
        'barbados': 'BBD', 'bermuda': 'BMD'
    }
   
    clean_country = df['Country'].astype(str).str.lower().str.strip()
    df['Currency'] = clean_country.map(currency_map).fillna('UNKNOWN')
   
    # 3. Fetch or Load Frozen Exchange Rates
    rates_file = 'frozen_exchange_rates.json'
    rates = {}
   
    if os.path.exists(rates_file):
        print("Loading frozen exchange rates from local file...")
        with open(rates_file, 'r') as f:
            rates = json.load(f)
    else:
        print("Fetching live exchange rates and freezing them...")
        try:
            api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
            response = requests.get(api_url)
            response.raise_for_status()
            rates = response.json().get('rates', {})
           
            # Save to file for future runs
            with open(rates_file, 'w') as f:
                json.dump(rates, f)
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch exchange rates. Network error: {e}")

    # 4. Convert Local Price to USD
    print("Calculating USD equivalents...")
    df['Temp_Rate'] = df['Currency'].map(rates)
    df['Price USD'] = (df['Price Cleaned'] / df['Temp_Rate']).round(2)
    df = df.drop(columns=['Temp_Rate'])

    # 5. Save the processed dataframe
    df.to_csv(output_filename, index=False)
    print(f"Success! Data cleaned, converted to USD, and saved to: {output_filename}")

# --- Execute the Script ---
input_csv = 'master_cost_of_living.csv'
output_csv = 'master_cost_of_living_clean_standard.csv'

process_cost_of_living_data(input_csv, output_csv)
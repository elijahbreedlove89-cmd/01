import pandas as pd

# 1. Load the wide-format master dataset
input_filename = 'master_combined_dataset.csv'
df = pd.read_csv(input_filename)

# 2. Define the US Control Data
# Rent data pulled live from Numbeo (March 5, 2026)
# US GPI = 2.448, US LPI = 3.8
california_data = [
    {
        'Country': 'United States',
        'City': 'San Francisco',
        'Region': 'North America',
        'CostOfLiving_1 Bedroom Apartment in City Centre': 3459.00,
        'GPI_score\xa0': 2.448,
        'LPI2023_LPI Score': 3.8
    },
    {
        'Country': 'United States',
        'City': 'Los Angeles',
        'Region': 'North America',
        'CostOfLiving_1 Bedroom Apartment in City Centre': 2675.00,
        'GPI_score\xa0': 2.448,
        'LPI2023_LPI Score': 3.8
    }
]

df_cali = pd.DataFrame(california_data)

# 3. Append to the master dataset
df_combined = pd.concat([df, df_cali], ignore_index=True)

# 4. Save and overwrite the master dataset
df_combined.to_csv(input_filename, index=False)
print(f"Success! San Francisco and Los Angeles appended to {input_filename}.")
print(f"Total rows is now: {len(df_combined)}")

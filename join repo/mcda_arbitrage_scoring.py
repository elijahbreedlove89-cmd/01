import pandas as pd

# ==========================================
# 1. Load the Normalized Dataset
# ==========================================
df = pd.read_csv('master_normalized_dataset.csv')

# Exact column names from the previous scaling step
rent_scaled = 'CostOfLiving_1 Bedroom Apartment in City Centre_Scaled'
safety_scaled = 'GPI_score\xa0_Scaled'
lpi_scaled = 'LPI2023_LPI Score_Scaled'

# ==========================================
# 2. Invert Cost and Risk Metrics
# ==========================================
# Lower rent = higher arbitrage value
df['Rent_Inverted'] = df[rent_scaled] * -1

# Lower GPI score = higher safety/peace
df['Safety_Inverted'] = df[safety_scaled] * -1

# ==========================================
# 3. Apply MCDA Weighting Logic
# ==========================================
# Using the weights from the proposal: 40% Rent, 20% Safety, 20% Infrastructure
weight_rent = 0.40
weight_safety = 0.20
weight_infra = 0.20

# Calculate the preliminary Arbitrage Score using the vector formula
df['Arbitrage_Score'] = (
    (df['Rent_Inverted'] * weight_rent) +
    (df['Safety_Inverted'] * weight_safety) +
    (df[lpi_scaled] * weight_infra)
)

# ==========================================
# 4. California Calibration (Control Anchor)
# ==========================================
# Filter for SF and LA to calculate the baseline
california_cities = df[df['City'].isin(['San Francisco', 'Los Angeles'])]

if not california_cities.empty:
    cali_baseline_score = california_cities['Arbitrage_Score'].mean()
    print(f"--- CALIFORNIA BASELINE SCORE: {cali_baseline_score:.3f} ---")
   
    # Calculate the 'Net-Income Stretch' (how many points above the baseline a city is)
    df['Arbitrage_Gap_vs_CA'] = df['Arbitrage_Score'] - cali_baseline_score
else:
    print("--- Note: SF/LA not found in current dataset to calculate baseline. ---")

# ==========================================
# 5. Rank and Reveal the Top Cities!
# ==========================================
# Sort the dataframe by the highest Arbitrage Score
df_ranked = df.sort_values(by='Arbitrage_Score', ascending=False).reset_index(drop=True)

print("\n🏆 PRELIMINARY TOP 10 ARBITRAGE CITIES 🏆")
# Display the City, Country, and their final score
print(df_ranked[['City', 'Country', 'Arbitrage_Score']].head(10).to_string(index=False))

# Export the final ranked dataset
output_filename = 'gari_preliminary_rankings.csv'
df_ranked.to_csv(output_filename, index=False)
print(f"\nSuccess! Rankings exported to: {output_filename}")
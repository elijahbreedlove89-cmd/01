import pandas as pd

df = pd.read_csv('gari_final_viable_rankings.csv')

# Invert cost/risk
df['Rent_Inv'] = df['CostOfLiving_1 Bedroom Apartment in City Centre_Scaled'] * -1
df['Safety_Inv'] = df['GPI_score\xa0_Scaled'] * -1
df['Infra'] = df['LPI2023_LPI Score_Scaled']

# Scenario 1: Heavy Rent Focus (55% Rent, 15% Safety, 30% Infra)
df['Score_Rent_Heavy'] = (df['Rent_Inv'] * 0.55) + (df['Safety_Inv'] * 0.15) + (df['Infra'] * 0.30)

# Scenario 2: Heavy Safety Focus (25% Rent, 35% Safety, 40% Infra)
df['Score_Safety_Heavy'] = (df['Rent_Inv'] * 0.25) + (df['Safety_Inv'] * 0.35) + (df['Infra'] * 0.40)

print("TOP 3: RENT HEAVY SCENARIO")
print(df.nlargest(3, 'Score_Rent_Heavy')[['City', 'Score_Rent_Heavy']].to_string(index=False))

print("\nTOP 3: SAFETY HEAVY SCENARIO")
print(df.nlargest(3, 'Score_Safety_Heavy')[['City', 'Score_Safety_Heavy']].to_string(index=False))


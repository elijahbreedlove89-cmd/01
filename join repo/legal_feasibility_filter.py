import pandas as pd

# 1. Load the Preliminary Rankings and Legal Appendix
df_ranked = pd.read_csv('gari_preliminary_rankings.csv')
df_legal = pd.read_csv('appendix_b_legal_feasibility.csv')

# 2. Merge the Datasets
# We do a left join to attach the legal status to our ranked cities
df_final = pd.merge(df_ranked, df_legal, on='Country', how='left')

# 3. Apply the Hard Binary Filter
# A city MUST have both a US Tax Treaty and a Digital Nomad Visa
df_viable = df_final[(df_final['US_Tax_Treaty'] == 'Yes') & (df_final['Digital_Nomad_Visa'] == 'Yes')]

# 4. Reveal the Official Top 3
print("\n🏆 OFFICIAL GARI TOP 3 ARBITRAGE CITIES 🏆")
print(df_viable[['City', 'Country', 'Arbitrage_Score']].head(3).to_string(index=False))

# Export the final validated dataset
output_filename = 'gari_final_viable_rankings.csv'
df_viable.to_csv(output_filename, index=False)
print(f"\nSuccess! Final legally viable rankings exported to: {output_filename}")
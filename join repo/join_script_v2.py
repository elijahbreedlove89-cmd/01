import pandas as pd

# ==========================================
# 1. Cost of Living (Pivot to Wide Format)
# ==========================================
df_cost_long = pd.read_csv('master_cost_of_living_clean_standard.csv')

# Pivot the data: 1 Row = 1 City. Items become columns containing USD prices.
df_cost = df_cost_long.pivot_table(
    index=['Country', 'City', 'Region'],
    columns='Item',
    values='Price USD'
).reset_index()

# Rename the newly pivoted item columns with 'CostOfLiving_' prefix
item_columns = [col for col in df_cost.columns if col not in ['Country', 'City', 'Region']]
cost_rename = {col: f"CostOfLiving_{col}" for col in item_columns}
df_cost = df_cost.rename(columns=cost_rename)

# Create a normalized merge key for case-insensitive joining
df_cost['Country_Merge'] = df_cost['Country'].astype(str).str.lower().str.strip()
df_cost['in_CostOfLiving'] = True

# ==========================================
# Helper Function for External Datasets
# ==========================================
def prep_external_data(df, name_prefix, country_col='Country'):
    """Standardizes external data for a left join"""
    if country_col != 'Country':
        df = df.rename(columns={country_col: 'Country'})
       
    # Create the same normalized merge key
    df['Country_Merge'] = df['Country'].astype(str).str.lower().str.strip()
   
    # Rename columns with prefix
    rename_dict = {col: f"{name_prefix}_{col}" for col in df.columns if col not in ['Country', 'Country_Merge']}
    df = df.rename(columns=rename_dict)
   
    # Add tracking column and drop original Country to prevent duplicate columns later
    df[f'in_{name_prefix}'] = True
    df = df.drop(columns=['Country'])
   
    return df

# ==========================================
# 2. Load & Prepare External Data
# ==========================================
df_mobile = prep_external_data(pd.read_excel('Speed Test - Mobile.xlsx', sheet_name='Sheet1'), 'SpeedTestMobile')
df_lpi = prep_external_data(pd.read_excel('Physical Infrastructure - LPI 2023.xlsx', sheet_name='2023'), 'LPI2023', country_col='Economy')
df_broadband = prep_external_data(pd.read_excel('Speed Test - Broadband.xlsx', sheet_name='Sheet1'), 'SpeedTestBroadband')
df_gpi = prep_external_data(pd.read_excel('Global Peace Index GPI.xlsx', sheet_name='Sheet1'), 'GPI', country_col='region')

# ==========================================
# 3. Master Merge (LEFT JOIN)
# ==========================================
dataframes_to_merge = [df_mobile, df_lpi, df_broadband, df_gpi]
df_master = df_cost.copy()

# Iterate and left join using our normalized key
for df in dataframes_to_merge:
    df_master = pd.merge(df_master, df, on='Country_Merge', how='left')

# Drop the temporary merge key, keeping the original formatted 'Country'
df_master = df_master.drop(columns=['Country_Merge'])

# ==========================================
# 4. Generate Mismatches/Missing Report
# ==========================================
tracker_cols = ['in_CostOfLiving', 'in_SpeedTestMobile', 'in_LPI2023', 'in_SpeedTestBroadband', 'in_GPI']
df_master[tracker_cols] = df_master[tracker_cols].fillna(False)

# Melt and filter for missing matches
df_melted = df_master.melt(
    id_vars=['Country', 'City'],
    value_vars=tracker_cols,
    var_name='Source Name',
    value_name='Is Present'
)
df_unmatched = df_melted[df_melted['Is Present'] == False].copy()

# Clean up Source Name formatting
df_unmatched['Source Name'] = df_unmatched['Source Name'].str.replace('in_', '')
df_unmatched = df_unmatched[['Country', 'City', 'Source Name']].drop_duplicates().sort_values(by=['Country', 'City'])

# Export unmatched report
unmatched_filename = 'mismatched_countries_report.csv'
df_unmatched.to_csv(unmatched_filename, index=False)

# ==========================================
# 5. Clean up & Final Export
# ==========================================
df_master = df_master.drop(columns=tracker_cols)
output_filename = 'master_combined_dataset.csv'
df_master.to_csv(output_filename, index=False)

print(f"Success! Master dataset exported to: {output_filename}")
print(f"Success! Mismatches report exported to: {unmatched_filename}")
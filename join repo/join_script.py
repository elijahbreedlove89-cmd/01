import pandas as pd

# ==========================================
# 1. Cost of Living (CSV)
# ==========================================
df_cost = pd.read_csv('master_cost_of_living_clean_standard.csv')
cost_rename = {col: f"CostOfLiving_{col}" for col in df_cost.columns if col != 'Country'}
df_cost = df_cost.rename(columns=cost_rename)
df_cost['in_CostOfLiving'] = True

# ==========================================
# 2. Speed Test - Mobile (Excel File)
# ==========================================
df_mobile = pd.read_excel('Speed Test - Mobile.xlsx', sheet_name='Sheet1')
mobile_rename = {col: f"SpeedTestMobile_{col}" for col in df_mobile.columns if col != 'Country'}
df_mobile = df_mobile.rename(columns=mobile_rename)
df_mobile['in_SpeedTestMobile'] = True

# ==========================================
# 3. Physical Infrastructure - LPI 2023 (Excel File)
# ==========================================
df_lpi = pd.read_excel('Physical Infrastructure - LPI 2023.xlsx', sheet_name='2023')
if 'Economy' in df_lpi.columns:
    df_lpi = df_lpi.rename(columns={'Economy': 'Country'})
lpi_rename = {col: f"LPI2023_{col}" for col in df_lpi.columns if col != 'Country'}
df_lpi = df_lpi.rename(columns=lpi_rename)
df_lpi['in_LPI2023'] = True

# ==========================================
# 4. Speed Test - Broadband (Excel File)
# ==========================================
df_broadband = pd.read_excel('Speed Test - Broadband.xlsx', sheet_name='Sheet1')
broadband_rename = {col: f"SpeedTestBroadband_{col}" for col in df_broadband.columns if col != 'Country'}
df_broadband = df_broadband.rename(columns=broadband_rename)
df_broadband['in_SpeedTestBroadband'] = True

# ==========================================
# 5. Global Peace Index GPI (Excel File)
# ==========================================
df_gpi = pd.read_excel('Global Peace Index GPI.xlsx', sheet_name='Sheet1')
if 'region' in df_gpi.columns:
    df_gpi = df_gpi.rename(columns={'region': 'Country'})
gpi_rename = {col: f"GPI_{col}" for col in df_gpi.columns if col != 'Country'}
df_gpi = df_gpi.rename(columns=gpi_rename)
df_gpi['in_GPI'] = True

# ==========================================
# 6. Master Merge
# ==========================================
dataframes_to_merge = [df_mobile, df_lpi, df_broadband, df_gpi]

df_master = df_cost.copy()
for df in dataframes_to_merge:
    df_master = pd.merge(df_master, df, on='Country', how='outer')

# ==========================================
# 7. Generate Mismatches/Missing Report
# ==========================================
tracker_cols = ['in_CostOfLiving', 'in_SpeedTestMobile', 'in_LPI2023', 'in_SpeedTestBroadband', 'in_GPI']

# Fill NaN values in tracking columns with False
df_master[tracker_cols] = df_master[tracker_cols].fillna(False)

# Melt and filter for missing matches
df_melted = df_master.melt(id_vars=['Country'], value_vars=tracker_cols, var_name='Source Name', value_name='Is Present')
df_unmatched = df_melted[df_melted['Is Present'] == False].copy()

# Clean up Source Name formatting
df_unmatched['Source Name'] = df_unmatched['Source Name'].str.replace('in_', '')
df_unmatched = df_unmatched[['Country', 'Source Name']].drop_duplicates().sort_values(by=['Country', 'Source Name'])

# Export unmatched report
unmatched_filename = 'mismatched_countries_report.csv'
df_unmatched.to_csv(unmatched_filename, index=False)

# ==========================================
# 8. Clean up & Final Export
# ==========================================
df_master = df_master.drop(columns=tracker_cols)
output_filename = 'master_combined_dataset.csv'
df_master.to_csv(output_filename, index=False)

print(f"Success! Master dataset exported to: {output_filename}")
print(f"Success! Mismatches report exported to: {unmatched_filename}")
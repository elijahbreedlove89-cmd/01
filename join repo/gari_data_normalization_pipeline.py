import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler

# ==========================================
# 1. Load the Wide-Format Master Dataset
# ==========================================
df = pd.read_csv('master_combined_dataset.csv')

# Define the exact core columns needed for scoring based on the pivoted data
rent_col = 'CostOfLiving_1 Bedroom Apartment in City Centre'
safety_col = 'GPI_score\xa0'  # Note: The GPI dataset has a trailing non-breaking space
lpi_col = 'LPI2023_LPI Score'

cols_to_analyze = [rent_col, safety_col, lpi_col]

# ==========================================
# 2. Handle Missing Values
# ==========================================
print(f"Original row count: {len(df)}")

# If a city is missing Rent, Safety, or Infrastructure data, we cannot calculate
# an Arbitrage Score for it. We must drop these incomplete records.
df_clean = df.dropna(subset=cols_to_analyze).copy()
print(f"Row count after dropping missing critical data: {len(df_clean)}")

# ==========================================
# 3. Apply Robust Scaling (IQR)
# ==========================================
# RobustScaler uses the median and interquartile range, minimizing outlier impact
scaler = RobustScaler()

# Create new column names for the scaled data
scaled_cols = [f"{col}_Scaled" for col in cols_to_analyze]

# Fit and transform the data, adding it to the dataframe
df_clean[scaled_cols] = scaler.fit_transform(df_clean[cols_to_analyze])

# ==========================================
# 4. Distribution Checks (Plotting Histograms)
# ==========================================
def plot_distribution_comparison(original_col, scaled_col, data, title_prefix):
    """Generates side-by-side histograms for Before & After scaling."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
   
    # Original Distribution
    sns.histplot(data[original_col], kde=True, ax=axes[0], color='royalblue')
    axes[0].set_title(f'Original {title_prefix} Distribution')
   
    # Robust Scaled Distribution
    sns.histplot(data[scaled_col], kde=True, ax=axes[1], color='seagreen')
    axes[1].set_title(f'Robust Scaled {title_prefix}')
   
    plt.tight_layout()
    plt.show()

print("Generating distribution check histograms...")
# Plot the distributions to visually verify the skewness and the scaling effect
plot_distribution_comparison(rent_col, f"{rent_col}_Scaled", df_clean, "Rent")
plot_distribution_comparison(safety_col, f"{safety_col}_Scaled", df_clean, "Safety Score")

# ==========================================
# 5. Export the Normalized Dataset
# ==========================================
output_filename = 'master_normalized_dataset.csv'
df_clean.to_csv(output_filename, index=False)
print(f"Success! Normalized dataset ready for scoring: {output_filename}")
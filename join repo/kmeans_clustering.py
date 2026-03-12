import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the normalized dataset
df = pd.read_csv('master_normalized_dataset.csv')

# Select the features for clustering
features = ['CostOfLiving_1 Bedroom Apartment in City Centre_Scaled',
            'GPI_score\xa0_Scaled',
            'LPI2023_LPI Score_Scaled']

X = df[features].dropna()

# Find optimal clusters using Silhouette Score
best_score = -1
best_k = 2
for k in range(2, 6):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    if score > best_score:
        best_score = score
        best_k = k

# Run final K-Means with optimal K
kmeans_final = KMeans(n_clusters=best_k, random_state=42)
df.loc[X.index, 'Cluster_Profile'] = kmeans_final.fit_predict(X)

print(f"Optimal number of clusters identified: {best_k}")
print(f"Silhouette Score: {best_score:.3f}")
df.to_csv('gari_clustered_dataset.csv', index=False)
print("Success: gari_clustered_dataset.csv exported.")
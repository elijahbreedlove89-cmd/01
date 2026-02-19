import os
import pandas as pd

# Appendix A: Vetted 50 Candidate Countries
countries = [
    # Region 1
    ("Western & Southern Europe", "Portugal"),
    ("Western & Southern Europe", "Spain"),
    ("Western & Southern Europe", "Italy"),
    ("Western & Southern Europe", "Greece"),
    ("Western & Southern Europe", "Malta"),
    ("Western & Southern Europe", "Cyprus"),
    ("Western & Southern Europe", "Croatia"),
    ("Western & Southern Europe", "France"),
    ("Western & Southern Europe", "Germany"),
    ("Western & Southern Europe", "Ireland"),

    # Region 2
    ("Eastern Europe & The Balkans", "Estonia"),
    ("Eastern Europe & The Balkans", "Czechia"),
    ("Eastern Europe & The Balkans", "Hungary"),
    ("Eastern Europe & The Balkans", "Poland"),
    ("Eastern Europe & The Balkans", "Romania"),
    ("Eastern Europe & The Balkans", "Bulgaria"),
    ("Eastern Europe & The Balkans", "Slovenia"),
    ("Eastern Europe & The Balkans", "Slovakia"),
    ("Eastern Europe & The Balkans", "Latvia"),
    ("Eastern Europe & The Balkans", "Lithuania"),
    ("Eastern Europe & The Balkans", "Albania"),
    ("Eastern Europe & The Balkans", "Montenegro"),
    ("Eastern Europe & The Balkans", "Georgia"),
    ("Eastern Europe & The Balkans", "Serbia"),

    # Region 3
    ("Latin America", "Mexico"),
    ("Latin America", "Costa Rica"),
    ("Latin America", "Colombia"),
    ("Latin America", "Panama"),
    ("Latin America", "Brazil"),
    ("Latin America", "Argentina"),
    ("Latin America", "Uruguay"),
    ("Latin America", "Chile"),
    ("Latin America", "Ecuador"),
    ("Latin America", "Belize"),

    # Region 4
    ("Asia-Pacific", "Thailand"),
    ("Asia-Pacific", "Vietnam"),
    ("Asia-Pacific", "Indonesia"),
    ("Asia-Pacific", "Malaysia"),
    ("Asia-Pacific", "Philippines"),
    ("Asia-Pacific", "Japan"),
    ("Asia-Pacific", "South Korea"),
    ("Asia-Pacific", "Taiwan"),
    ("Asia-Pacific", "Sri Lanka"),

    # Region 5
    ("Middle East & Africa", "UAE"),
    ("Middle East & Africa", "Turkey"),
    ("Middle East & Africa", "South Africa"),
    ("Middle East & Africa", "Mauritius"),
    ("Middle East & Africa", "Morocco"),

    # Region 6
    ("Island Life", "Barbados"),
    ("Island Life", "Bermuda"),
]

df = pd.DataFrame(countries, columns=["Region", "Country"])

os.makedirs("appendices", exist_ok=True)
output_path = "appendices/appendix_a.csv"
df.to_csv(output_path, index=False)

print(f"Appendix A CSV created at: {output_path}")

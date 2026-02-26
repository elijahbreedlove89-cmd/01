import os
import pandas as pd

# Appendix B: Legal Feasibility Table
# You can update these values anytime as your research evolves.

data = [
    # Region 1
    ("Portugal", "Yes", "Yes"),
    ("Spain", "Yes", "Yes"),
    ("Italy", "Yes", "Yes"),
    ("Greece", "Yes", "Yes"),
    ("Malta", "Yes", "Yes"),
    ("Cyprus", "Yes", "Yes"),
    ("Croatia", "Yes", "Yes"),
    ("France", "Yes", "No"),
    ("Germany", "Yes", "No"),
    ("Ireland", "Yes", "No"),

    # Region 2
    ("Estonia", "Yes", "Yes"),
    ("Czechia", "Yes", "Yes"),
    ("Hungary", "Yes", "Yes"),
    ("Poland", "Yes", "Yes"),
    ("Romania", "Yes", "Yes"),
    ("Bulgaria", "Yes", "Yes"),
    ("Slovenia", "Yes", "Yes"),
    ("Slovakia", "Yes", "Yes"),
    ("Latvia", "Yes", "Yes"),
    ("Lithuania", "Yes", "Yes"),
    ("Albania", "Yes", "Yes"),
    ("Montenegro", "Yes", "Yes"),
    ("Georgia", "No", "Yes"),
    ("Serbia", "Yes", "Yes"),

    # Region 3
    ("Mexico", "Yes", "Yes"),
    ("Costa Rica", "No", "Yes"),
    ("Colombia", "Yes", "Yes"),
    ("Panama", "Yes", "Yes"),
    ("Brazil", "Yes", "Yes"),
    ("Argentina", "Yes", "Yes"),
    ("Uruguay", "Yes", "Yes"),
    ("Chile", "Yes", "Yes"),
    ("Ecuador", "Yes", "Yes"),
    ("Belize", "No", "Yes"),

    # Region 4
    ("Thailand", "No", "Yes"),
    ("Vietnam", "No", "Yes"),
    ("Indonesia", "No", "Yes"),
    ("Malaysia", "Yes", "Yes"),
    ("Philippines", "Yes", "Yes"),
    ("Japan", "Yes", "No"),
    ("South Korea", "Yes", "No"),
    ("Taiwan", "No", "Yes"),
    ("Sri Lanka", "No", "Yes"),

    # Region 5
    ("UAE", "No", "Yes"),
    ("Turkey", "Yes", "Yes"),
    ("South Africa", "Yes", "Yes"),
    ("Mauritius", "Yes", "Yes"),
    ("Morocco", "Yes", "Yes"),

    # Region 6
    ("Barbados", "Yes", "Yes"),
    ("Bermuda", "Yes", "Yes"),
]

df = pd.DataFrame(data, columns=["Country", "US_Tax_Treaty", "Digital_Nomad_Visa"])

os.makedirs("appendices", exist_ok=True)
output_path = "appendices/appendix_b_legal_feasibility.csv"
df.to_csv(output_path, index=False)

print(f"Appendix B CSV created at: {output_path}")

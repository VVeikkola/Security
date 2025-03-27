import pandas as pd

df = pd.read_csv("Scenarios_Analysis.csv", delimiter=';', encoding='latin-1')

df_cleaned = df.dropna(how='any')

print(f"Before: {len(df)}")
print(f"After: {len(df_cleaned)}")

df_cleaned.to_csv("Scenarios_cleaned2.csv", index=False)

print("Cleaned")
import pandas as pd

df = pd.read_csv("Scenarios.csv")

df_cleaned = df.dropna(how='any')

print(f"Before: {len(df)}")
print(f"After: {len(df_cleaned)}")

df_cleaned.to_csv("Scenarios_cleaned.csv", index=False)

print("Cleaned")
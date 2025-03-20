import pandas as pd
import requests
import csv

# Remove transformers imports and model loading
# create csv file for data storing

FILENAME = "Scenarios.csv"

with open(FILENAME, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ScenarioID" ,"Reasoning", "Description of the classification", "ThreatID", "VulnerabilityID", "RemdiationID"])


df = pd.read_excel("Scenarios.xlsx")

# Keep your preprocessing
df.columns = df.columns.str.strip()
df = df.drop(columns=["User"], errors="ignore")
df["Assistant - Vulnerability description"] = df["Assistant - Vulnerability description"].astype(str)

def analyze_scenario(text):
    if not isinstance(text, str):
        text = str(text)
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # Match the model you pulled
                "prompt": f"Analyze this cybersecurity vulnerability scenario: {text}",
                "stream": False,
                "options": {
                    "temperature": 0.7
                }
            }
        )
        if response.status_code == 200:
            print("Response: ",  response.json()['response'])
            return response.json()['response']
        return "Analysis failed"
    except Exception as e:
        return f"Error: {str(e)}"
for index, row in df.iterrows():
    analysis = analyze_scenario(row["Assistant - Vulnerability description"])
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            row.get("ScenarioID", ""),
            row.get("Reasoning", ""),
            row.get("Description of the classification", ""),
            row.get("ThreatID", ""),
            row.get("VulnerabilityID", ""),
            row.get("RemdiationID", ""),
            analysis
        ])
print("ready")
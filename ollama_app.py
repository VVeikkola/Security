import pandas as pd
import requests
import csv

# Remove transformers imports and model loading
# create csv file for data storing

FILENAME = "Scenarios.csv"
OUTPUT_FILE = "Scenarios_Analysis.csv"

# initialize the output file
with open(OUTPUT_FILE, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["ScenarioID", "Reasoning", "Description of the classification", "ThreatID", "VulnerabilityID", "RemdiationID", "Remediation strategy"])


df = pd.read_csv("Scenarios.csv")

def analyze_scenario(text):
    if not isinstance(text, str):
        text = str(text)
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # Match the model you pulled
                "prompt": f"""Analyze this cybersecurity vulnerability scenario and remediation strategy for it. If the remediation strategy is a "nice to have" label it as in output.
                The input is one or multiple csv rows with the following columns. one set of columns is one scenario.
                Scenario ID,User,Assistant - Extended,Assistant - Short, Assistant - Details,Threat ID,Description of the classification?,Vulnerability ID,Reasoning,Assistant - Risk occurrence type
                Do not include the column names in the output. also do not use ";" in the output.                
                csv blob: {text}""",
                "stream": False,
                "options": {
                    "temperature": 0.7
                }
            }
        )
        if response.status_code == 200:
            # print("Response: ",  response.json()['response'])
            return response.json()['response']
        return "Analysis failed"
    except Exception as e:
        return f"Error: {str(e)}"
    
index = 0
while index < len(df):
    remediationIdCounter = 0
    text = ""
    row = df.iloc[index]
    
    # get all the rows with the same scenario id and combine them into one text blob for analysis
    while index < len(df) - 1 and row["Scenario ID"] == df.iloc[index + 1]["Scenario ID"]:
        text += row
        index += 1
        if index >= len(df) - 1:
            break
        row = df.iloc[index]
        
    # print the index and id to keep track of progress    
    print("Analyzing index: ", index)
    print("current scenario id: ", row["Scenario ID"])
    # analyze the text blob
    analysis = analyze_scenario(text)
    # print the analysis
    # print(analysis)
    # write the analysis to the csv file
    with open(OUTPUT_FILE, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([row["Scenario ID"], 
                         row['Reasoning'], 
                         row['Description of the classification?'], 
                         row['Threat ID'], 
                         row['Vulnerability ID'], 
                         f"R{remediationIdCounter}", analysis])
    
    
    remediationIdCounter += 1
    text = ""
    index += 1
    
print("ready")
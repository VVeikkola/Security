import pandas as pd
import requests
import csv

# Remove transformers imports and model loading
# create csv file for data storing

FILENAME = "Scenarios_cleaned.csv"
FILENAMEREMEDIATION = "Remediations_table.csv"
OUTPUT_FILE = "Scenarios_AnalysisRemediations.csv"

# initialize the output file
with open(OUTPUT_FILE, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["ScenarioID", "Reasoning", "Description of the classification", "ThreatID", "VulnerabilityID", "RemdiationID", "Remediation strategy"])

# get the remediations csv to get the remediation options
remediations_df = pd.read_csv(FILENAMEREMEDIATION)
remediation_options = ""
for _, row in remediations_df.iterrows():
    remediation_options += f"{row['THREAT ID']},{row['THREAT']},{row['VULNERABILITY ID']},{row['VULNERABILITY']},{row['VTHE']},{row['Remediation ID']},{row['Remediation strategy']}\n"


df = pd.read_csv("Scenarios_cleaned.csv")

def analyze_scenario(text):
    if not isinstance(text, str):
        text = str(text)
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:7b", 
                "prompt": f"""
                
                Analyze the following cybersecurity vulnerability scenario and select the best remediation strategy for it from the provided options.
                Scenario ID,User,Assistant - Extended,Assistant - Short, Assistant - Details,Threat ID,Description of the classification?,Vulnerability ID,Reasoning,Assistant - Risk occurrence type
                
                
                csv blob: {text}
                
                The strucutre of remediation options is as follows:
                THREAT ID,THREAT,VULNERABILITY ID,VULNERABILITY,VTHE,Remediation ID,Remediation strategy,TECHNICAL NATURE

                remediations: {remediation_options}
                
                Use the remediation id and strategy from the provided options. Do not include anything else in the response apart from the starting line (Reasoning;Remediation ID;Remediation strategy\n), reasoning, remediation ids and strategies. 
                If some Strategy is nice to have give it a NTH prefix in the response.
                Reasoning is the explanation of the classification and the remediation strategy. length should be maximum 1 sentence. 
                
                Do not include the column names in the output. also do not use ";" in the output apart from seperating the reasoning, remediation id and the reasoning in the response with ;. 
                Response should be in the following format seperate lines for each reasoning, remediation id and strategy:
                
                reasoning,remediation_id;remediation_strategy\n
                "here i reason remediation 1";remediation_id1;remediation_strategy1\n
                "here i reason remediation 2";remediation_id2;remediation_strategy2\n
                ...               
                """,
                
                
                
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
    print(analysis)
    # save reasoning to a variable. its between <think> and </think>
    
    reasoning = analysis.split("<think>", 1)[1].split("</think>", 1)[0]
    
    # print the analysis
    # print(analysis)
    # write the analysis to the csv file
    
    # create a csv blob with the results. each row should have the scenario id, reasoning, description of the classification, threat id, vulnerability id, remediation id and remediation strategy
    # find remediations and add them to the csv
    remediationss = analysis.split("</think>", 1)[1]
    for row1 in remediationss.split("\n"):
        if row1 == "":
            continue
        if row1.count("remediation_id") != 0:
            continue
        if row1.count(";") == 0:
            continue
        row1 = row1.split(";")
        print(row1)
        reasoningg, remediationId, remediation = "error", "error", "error"
        
        try:
            reasoningg = row1[0]
            remediationId = row1[1]
            remediation = row1[2]
        except IndexError:
            print("Error")
            
        
        
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([row["Scenario ID"], 
                             reasoningg, 
                             row['Description of the classification?'], 
                             row['Threat ID'], 
                             row['Vulnerability ID'], 
                             remediationId,
                             remediation])    
    
    
    text = ""
    index += 1
    
print("ready")
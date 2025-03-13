import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM

# Ladataan malli ja tokeniseri
tokenizer = AutoTokenizer.from_pretrained("AIDC-AI/Marco-o1")
model = AutoModelForCausalLM.from_pretrained("AIDC-AI/Marco-o1")

df = pd.read_excel("Scenarios.xlsx")

# Funktio Preprocessing
df.columns = df.columns.str.strip()
df = df.drop(columns=["User"], errors="ignore")


# Integroi modeli Marco1
def analyze_scenario(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(**inputs, max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


df["Reasoning"] = df["Assistant - Vulnerability description"].apply(analyze_scenario)

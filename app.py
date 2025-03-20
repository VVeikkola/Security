import pandas as pd
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

print(transformers.__version__)
# Ladataan malli ja tokeniseri
tokenizer = AutoTokenizer.from_pretrained("AIDC-AI/Marco-o1")
model = AutoModelForCausalLM.from_pretrained("AIDC-AI/Marco-o1")
# tokenizer = AutoTokenizer.from_pretrained("O1-OPEN/OpenO1-Qwen-7B-v0.1")
# model = AutoModelForCausalLM.from_pretrained("O1-OPEN/OpenO1-Qwen-7B-v0.1")

df = pd.read_excel("Scenarios.xlsx")

# Funktio Preprocessing
df.columns = df.columns.str.strip()
df = df.drop(columns=["User"], errors="ignore")
df["Assistant - Vulnerability description"] = df["Assistant - Vulnerability description"].astype(str)


# Integroi modeli Marco1
def analyze_scenario(text):
    if not isinstance(text, str):
        text = str(text)  # Convert non-string inputs to string
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(**inputs, max_length=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


df["Reasoning"] = df["Assistant - Vulnerability description"].apply(analyze_scenario)

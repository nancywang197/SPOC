import pandas as pd
json_path = r'C:\Users\nancy\OneDrive\Desktop\SPoC\script\train-dataset.json'
pd.read_json(json_path).to_excel("train-dataset.xlsx")
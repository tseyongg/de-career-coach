import requests
import json
import pandas as pd

url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
response = requests.get(url)
data = response.json()

country_codes_df = pd.read_excel("Country-Code.xlsx")
country_codes = dict(zip(country_codes_df['Country Code'], country_codes_df['Country']))

print(country_codes)
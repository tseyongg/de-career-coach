import pandas as pd
import json

def load_carpark_data(url):
    '''Load static carpark data from given URL'''
    # Read CSV from static URL into pandas DataFrame
    df = pd.read_csv(url)
    
    # Create dictionary where car_park_no is the key
    # Convert each pandas row to regular dictionary
    carparks = {}
    for index, row in df.iterrows():
        carpark_number = row['car_park_no']
        carparks[carpark_number] = row.to_dict()
    
    return carparks

# url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/HDBCarparkInformation.csv"
# data = load_carpark_data(url)

# with open("carpark_static.json", "w") as f:
#     json.dump(data, f, indent=4)
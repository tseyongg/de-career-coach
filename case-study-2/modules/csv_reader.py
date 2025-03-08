import csv
import json

def load_carpark_data(csv_filepath):
    '''Load static carpark data from given csv'''
    carparks = {}

    with open(csv_filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            carpark_number = row['car_park_no']
            carparks[carpark_number] = row
    
    return carparks

data = load_carpark_data("HDBCarparkInformation.csv")

# test comment out if needed
with open("carpark_static.json", "w") as f:
    json.dump(data, f, indent=4)
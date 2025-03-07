import requests
import json

def get_carpark_availability(url):
    '''Fetch real-time carpark availability data from the gov API'''
    response = requests.get(url)
    data = response.json()

    carpark_availability = {}

    for carpark in data['items'][0]['carpark_data']:
        carpark_num = carpark['carpark_number']
        update_time = carpark['update_datetime']

        # For handling different lot types
        total_lots = 0
        avail_lots = 0
        lot_types = {}

        for lot in carpark['carpark_info']:
            lot_type = lot['lot_type']
            lot_type_total = int(lot['total_lots'])
            lot_type_available = int(lot['lots_available'])

            total_lots += lot_type_total
            avail_lots += lot_type_available

            lot_types[lot_type] = {
                'total_lots': lot_type_total,
                'lots_available': lot_type_available
            }

        carpark_availability[carpark_num] = {
            'total_lots': total_lots,
            'available_lots': avail_lots,
            'lot_types': lot_types,
            'update_time': update_time
        }


    print(f"API returned {len(data['items'][0]['carpark_data'])} carparks")
    print(f"Processed {len(carpark_availability)} carparks")

    # Find duplicates
    carpark_numbers = [cp['carpark_number'] for cp in data['items'][0]['carpark_data']]
    duplicates = set([x for x in carpark_numbers if carpark_numbers.count(x) > 1])
    print(f"Duplicate carpark numbers: {duplicates}")


    return carpark_availability
    
url = "https://api.data.gov.sg/v1/transport/carpark-availability"
data = get_carpark_availability(url)

# test
with open("carpark_availability.json", "w") as f:
    json.dump(data, f, indent=4)
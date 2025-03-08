'''
Data Merger Module

This module merges static carpark data from the given CSV URL and real-time carpark data from SG gov API.
'''

def merge_carpark_data(carpark_static, carpark_availability):
    '''Merge static carpark data from CSV and real-time carpark data from gov API'''
    merged_carpark_data = {}

    # First, include all data matching in both static and API data (like inner join)
    for carpark_num, static_data in carpark_static.items():
        if carpark_num in carpark_availability:
            merged_carpark_data[carpark_num] = {
                **static_data,
                'availability': carpark_availability[carpark_num]
            }
        # Then, include all static carparks with NA availability if in static data only, not in API data (like left join)
        else:
            merged_carpark_data[carpark_num] = {
                **static_data,
                'availability': {
                    'total_lots': 'NA',
                    'available_lots': 'NA',
                    'lot_types': {},
                    'update_time': 'NA'
                }
            }
    
    # Lastly, include carparks from API that are not present in static data (like right join)
    for carpark_num, availability in carpark_availability.items():
        if carpark_num not in merged_carpark_data:
            merged_carpark_data[carpark_num] = {
                'car_park_no': carpark_num,
                'address': 'NA',
                'x_coord': 'NA',
                'y_coord': 'NA',
                'car_park_type': 'NA',
                'type_of_parking_system': 'NA',
                'short_term_parking': 'NA',
                'free_parking': 'NA',
                'night_parking': 'NA',
                'car_park_decks': 'NA',
                'gantry_height': 'NA',
                'car_park_basement': 'NA',
                'availability': availability
            }
    
    return merged_carpark_data


# # test comment out if needed
# import json

# with open("carpark_static.json", "r", encoding="utf-8") as f:
#     carpark_static = json.load(f)


# with open("carpark_availability.json", "r", encoding="utf-8") as f:
#     carpark_availability = json.load(f)


# merged_data = merge_carpark_data(carpark_static, carpark_availability)


# with open("merged_carpark_data.json", "w", encoding="utf-8") as f:
#     json.dump(merged_data, f, indent=4)
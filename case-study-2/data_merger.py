def merge_carpark_data(carpark_static, carpark_availability):
    '''Merge static carpark data from CSV and real-time carpark data from gov API'''
    merged_carpark_data = {}

    for carpark_num, availability in carpark_availability.items():

        # Reassign for clarity, and to check if the static CSV contains the carpark number
        static_key = carpark_num

        if static_key in carpark_static:
            merged_carpark_data[carpark_num] = {
                **carpark_static[carpark_num],
                'availability' : availability
            }
        else:
            # Input NA values into static data fields if carpark number not found in static CSV
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








    return merged_carpark_data
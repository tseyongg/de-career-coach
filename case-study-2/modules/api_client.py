'''
API Client Module

This module contains a function to fetch real-time carpark availability data from SG gov API.
'''

import requests

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

        # Check if carpark_num already exists in carpark_availability, to account for duplicates
        if carpark_num in carpark_availability:
            lot_types = carpark_availability[carpark_num]['lot_types']
        else:
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
            'total_lots': total_lots + (carpark_availability.get(carpark_num, {}).get('total_lots',0)), # Add 0 to total_lots if new carpark_num, else add to existing value
            'available_lots': avail_lots + (carpark_availability.get(carpark_num, {}).get('available_lots',0)), # Add 0 to avail_lots if new carpark_num, else add to existing value
            'lot_types': lot_types,
            'update_time': update_time
        }

    return carpark_availability
'''
User Search Module

This module contains functions to search for carpark data by 1) carpark number or 2) address.
'''

def search_by_carpark_number(merged_carpark_data, carpark_number):
    '''Search for carpark by carpark number'''
    carpark_number = carpark_number.strip().upper()
    
    if carpark_number in merged_carpark_data:
        return [merged_carpark_data[carpark_number]]
    
    return []


def search_by_address(merged_carpark_data, input_address):
    '''Search for carpark by address'''
    results = []
    input_address = input_address.strip().upper() # Ensure case-insensitive search
    
    for carpark_number, merged_carpark_details in merged_carpark_data.items():
        if input_address in merged_carpark_details['address'].upper(): # Ensure case-insensitive search
            results.append(merged_carpark_details)
    return results
def search_by_carpark_number(merged_carpark_data, carpark_number):
    '''Search for carpark by carpark number'''
    if carpark_number in merged_carpark_data:
        return merged_carpark_data[carpark_number]
    
    return None


def search_by_address(merged_carpark_data, input_address):
    '''Search for carpark by address'''
    results = []
    input_address = input_address.upper()
    for carpark_number, merged_carpark_details in merged_carpark_data.items():
        if input_address in merged_carpark_details['address'].upper():
            results.append(merged_carpark_details)
    return results

# test

import json

with open("merged_carpark_data.json", "r", encoding="utf-8") as f:
    merged_carpark_data = json.load(f)


test_carpark_number = "Y39"
carpark_result = search_by_carpark_number(merged_carpark_data, test_carpark_number)

test_address = "tampines central 7"
address_results = search_by_address(merged_carpark_data, test_address)

print(carpark_result)
print(address_results)
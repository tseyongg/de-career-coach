'''
Restaurant Details Extraction Script

This script fetches restaurant data from a JSON source, then matches country codes
to a reference Excel file, and finally saves restaurant details to a CSV file.
'''

import requests
import json
import pandas as pd
import csv


def fetch_restaurant_data(url):
    '''Fetches restaurant data from provided URL'''
    response = requests.get(url)
    return response.json()


def load_country_codes(filename):
    '''Loads country codes from given Excel file, then creates mapping dictionary'''
    country_codes_df = pd.read_excel("Country-Code.xlsx")
    return dict(zip(country_codes_df['Country Code'], country_codes_df['Country']))


def extract_restaurant_details(data, country_codes):
    '''
    Extracts restaurant details from fetched JSON data.
    Includes only restaurants with matching country codes.
    '''
    restaurant_details = []

    for result_set in data:
        for item in result_set['restaurants']:
            restaurant = item['restaurant']
            country_id = restaurant['location']['country_id']
            
            # Include only restaurants with matching country codes
            if country_id in country_codes:
                # Extract event date if available
                event_date = "NA"
                if 'zomato_events' in restaurant and restaurant['zomato_events']:
                    event_date = restaurant['zomato_events'][0]['event']['start_date']
                
                restaurant_details.append({
                    'Restaurant Id': restaurant['id'],
                    'Restaurant Name': restaurant['name'],
                    'Country': country_codes[country_id],
                    'City': restaurant['location']['city'],
                    'User Rating Votes': restaurant['user_rating']['votes'],
                    'User Aggregate Rating': float(restaurant['user_rating']['aggregate_rating']),
                    'Cuisines': restaurant.get('cuisines', "NA"),
                    'Event Date': event_date
                })

    return restaurant_details


def save_to_csv(data, filename, fieldnames):
    '''Save extracted restaurant details to CSV file'''
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    '''Main function to run script'''
    DATA_URL = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    COUNTRY_CODES_FILE = "Country-Code.xlsx"
    OUTPUT_FILE = "restaurant_details.csv"

    # Define CSV field names
    fieldnames = [
        'Restaurant Id', 'Restaurant Name', 'Country', 'City', 
                'User Rating Votes', 'User Aggregate Rating', 'Cuisines', 'Event Date'
    ]

    # Fetch and process restaurant details data
    data = fetch_restaurant_data(DATA_URL)
    country_codes = load_country_codes(COUNTRY_CODES_FILE)
    restaurant_details = extract_restaurant_details(data, country_codes)

    save_to_csv(restaurant_details, OUTPUT_FILE, fieldnames)
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
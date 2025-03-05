import requests
import json
import pandas as pd
import csv

url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
response = requests.get(url)
data = response.json()

country_codes_df = pd.read_excel("Country-Code.xlsx")
country_codes = dict(zip(country_codes_df['Country Code'], country_codes_df['Country']))

output_file = open('restaurant_details.csv', 'w', newline='', encoding='utf-8')
fieldnames = ['Restaurant Id', 'Restaurant Name', 'Country', 'City', 
                'User Rating Votes', 'User Aggregate Rating', 'Cuisines', 'Event Date']
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for result_set in data:
    for item in result_set['restaurants']:
        restaurant = item['restaurant']
        country_id = restaurant['location']['country_id']
        
        # include only restaurants with matching country codes
        if country_id in country_codes:
            # extract event date if available
            event_date = "NA"
            if 'zomato_events' in restaurant and restaurant['zomato_events']:
                event_date = restaurant['zomato_events'][0]['event']['start_date']
            
            writer.writerow({
                'Restaurant Id': restaurant['id'],
                'Restaurant Name': restaurant['name'],
                'Country': country_codes[country_id],
                'City': restaurant['location']['city'],
                'User Rating Votes': restaurant['user_rating']['votes'],
                'User Aggregate Rating': float(restaurant['user_rating']['aggregate_rating']),
                'Cuisines': restaurant.get('cuisines', "NA"),
                'Event Date': event_date
            })

output_file.close()
print("saved to restaurant_details.csv")
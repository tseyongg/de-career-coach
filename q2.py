import requests
import json
import pandas as pd
import csv

url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
response = requests.get(url)
data = response.json()

output_file = open('restaurant_events.csv', 'w', newline='', encoding='utf-8')
fieldnames = ['Event Id', 'Restaurant Id', 'Restaurant Name', 'Photo URL', 
                'Event Title', 'Event Start Date', 'Event End Date']
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

for result_set in data:
    for item in result_set['restaurants']:
        restaurant = item['restaurant']

        if 'zomato_events' in restaurant and restaurant['zomato_events']:
            for element in restaurant['zomato_events']:
                event = element['event']

                #check date range
                if (event['start_date'] <= "2019-04-30" and event['end_date'] >= "2019-04-01"):
                    photo_url = "NA"
                    if 'photos' in event and event['photos']:
                        photo_url = event['photos'][0]['photo']['url']

                    writer.writerow({
                        'Event Id': event['event_id'],
                        'Restaurant Id' : restaurant['id'],
                        'Restaurant Name': restaurant['name'],
                        'Photo URL' : photo_url,
                        'Event Title' : event['title'],
                        'Event Start Date' : event['start_date'],
                        'Event End Date' : event['end_date']
                    })

output_file.close()
print("April 2019 events saved to restaurant_events.csv")
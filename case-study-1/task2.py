'''
Restaurant Events Extraction Script

This script fetches restaurant data from the JSON source, then extracts events
that happened during April 2019, and finally saves restaurant details to a CSV file.
'''

from task1 import fetch_restaurant_data, save_to_csv, ensure_output_directory
from dotenv import load_dotenv
import os


def is_event_in_apr_2019(event):
    '''
    Check for event in April 2019 only.
    As long as any part of event falls within April, it is counted.
    '''
    return (event['start_date'] <= "2019-04-30" and 
            event['end_date'] >= "2019-04-01")


def extract_event_photo_url(event):
    """Extract photo URL from event if possible."""
    if 'photos' in event and event['photos']:
        return event['photos'][0]['photo']['url']
    return "NA"

def extract_april_2019_events(data):
    '''
    Extract April 2019 events from data
    '''
    april_events = []

    for result_set in data:
        for item in result_set['restaurants']:
            restaurant = item['restaurant']

            if 'zomato_events' in restaurant and restaurant['zomato_events']:
                for element in restaurant['zomato_events']:
                    event = element['event']

                    # Check April 2019 date range
                    if is_event_in_apr_2019(event):
                        april_events.append({
                            'Event Id': event['event_id'],
                            'Restaurant Id' : restaurant['id'],
                            'Restaurant Name': restaurant['name'],
                            'Photo URL' : extract_event_photo_url(event),
                            'Event Title' : event['title'],
                            'Event Start Date' : event['start_date'],
                            'Event End Date' : event['end_date']
                        })

    return april_events


def main():
    '''Main function to run script'''
    load_dotenv()
    RESTAURANT_JSON_URL = os.getenv("RESTAURANT_JSON_URL")
    output_dir = ensure_output_directory()
    OUTPUT_FILE = os.path.join(output_dir, "restaurant_events.csv")

    # Define CSV field names
    fieldnames = [
        'Event Id', 'Restaurant Id', 'Restaurant Name', 'Photo URL', 
        'Event Title', 'Event Start Date', 'Event End Date'
    ]

    # Fetch and process restaurant events data
    data = fetch_restaurant_data(RESTAURANT_JSON_URL)
    april_events = extract_april_2019_events(data)

    save_to_csv(april_events, OUTPUT_FILE, fieldnames)
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

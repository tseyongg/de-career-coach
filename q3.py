import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
response = requests.get(url)
data = response.json()

ratings_data = []
for result_set in data:
    for item in result_set['restaurants']:
        restaurant = item['restaurant']
        
        if 'user_rating' in restaurant and 'aggregate_rating' in restaurant['user_rating']:
            ratings_data.append({
                'Restaurant Id': restaurant['id'],
                'Restaurant Name': restaurant['name'],
                'Aggregate Rating': float(restaurant['user_rating']['aggregate_rating']),
                'Rating Text': restaurant['user_rating']['rating_text'],
                'Votes': int(restaurant['user_rating']['votes'])
            })

ratings_df = pd.DataFrame(ratings_data)

rating_groups = ratings_df.groupby('Rating Text')

rating_stats = rating_groups['Aggregate Rating'].agg(['min', 'max', 'mean', 'count'])
rating_stats = rating_stats.sort_values(by='mean', ascending=False)
print(rating_stats)
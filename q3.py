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

rating_mapping = {
    'Skvělé': 'Excellent',
    'Terbaik': 'Excellent',
    'Eccellente': 'Excellent',
    'Excelente': 'Excellent',
    'Excellent': 'Excellent',
    'Muito Bom': 'Very Good',
    'Muy Bueno': 'Very Good',
    'Very Good': 'Very Good',
    'Velmi dobré': 'Very Good',
    'Bardzo dobrze': 'Very Good',
    'Bueno': 'Good',
    'Good': 'Good',
    'Skvělá volba': 'Good',
    'Average': 'Average',
    'Poor': 'Poor',
    'Not rated': 'Not rated'
}

ratings_df['Standardized Rating'] = ratings_df['Rating Text'].map(rating_mapping)

standardized_rating_groups = ratings_df.groupby('Standardized Rating')

standardized_rating_stats = standardized_rating_groups['Aggregate Rating'].agg(['min', 'max', 'mean', 'count'])
standardized_rating_stats = standardized_rating_stats.sort_values(by='mean', ascending=False)
print(standardized_rating_stats)


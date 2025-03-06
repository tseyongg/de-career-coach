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

# create new summary stats table with thresholds
summary_stats = standardized_rating_stats.copy()

# set the threshold range for each category
thresholds = {}
for category in summary_stats.index:
    if category == 'Not rated':
        thresholds[category] = 'N/A'
    elif category == 'Poor':
        # poor starts from 0 and ends at 0.1 below the min of Average
        average_min = summary_stats.loc['Average', 'min']
        thresholds[category] = f'0.0 - {average_min - 0.1}'
    else:
        # for other categories, use their min-max range
        thresholds[category] = f'{summary_stats.loc[category, "min"]} - {summary_stats.loc[category, "max"]}'

summary_stats['thresholds'] = pd.Series(thresholds)

if 'Not rated' in summary_stats.index:
    # convert columns to object type before assigning string values
    for col in ['min', 'max', 'mean']:
        summary_stats[col] = summary_stats[col].astype(object)
    summary_stats.loc['Not rated', ['min', 'max', 'mean']] = 'N/A'

print(summary_stats)


main_categories = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
filtered_df = ratings_df[ratings_df['Standardized Rating'].isin(main_categories)]

plt.figure(figsize=(12, 6))

colors = {
    'Excellent': 'green',
    'Very Good': 'blue',
    'Good': 'orange',
    'Average': 'yellow',
    'Poor': 'red'
}

bins = [0.0, 2.5, 3.5, 4.0, 4.5, 5.0]

# plot histogram for each category
for category in main_categories:
    category_data = filtered_df[filtered_df['Standardized Rating'] == category]['Aggregate Rating']
    plt.hist(category_data, bins=bins, alpha=0.7, label=category, color=colors[category], 
             edgecolor='black')

plt.title('Distribution of Restaurant Ratings by Category', fontsize=15)
plt.xlabel('Aggregate Rating', fontsize=12)
plt.ylabel('Number of Restaurants', fontsize=12)
plt.legend(title='Rating Category')
plt.grid(axis='y', alpha=0.3)
plt.xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
plt.savefig('restaurant_ratings_histogram.png')
plt.show()

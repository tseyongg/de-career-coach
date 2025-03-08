"""
Restaurant Ratings Analysis Script

This script fetches restaurant data from the JSON source, analyzes rating distributions,
then standardizes rating text across languages, 
then adds a threshold field for clarity, and finally creates visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
from task1 import fetch_restaurant_data, save_to_csv, ensure_output_directory
from dotenv import load_dotenv
import os

def extract_ratings_data(data):
    '''
    Extracts restaurant ratings from fetched JSON data.
    '''
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

    return ratings_data


def create_standardized_mapping():
    return {
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


def analyze_ratings(ratings_df):
    '''
    Analyze ratings by grouping them and calculating statistics.
    Returns original and then standardized statistics.
    '''
    # Group by original rating text
    rating_groups = ratings_df.groupby('Rating Text')
    rating_stats = rating_groups['Aggregate Rating'].agg(['min', 'max', 'mean', 'count'])
    rating_stats = rating_stats.sort_values(by='mean', ascending=False)

    # Map to standardized rating text
    rating_mapping = create_standardized_mapping()
    ratings_df['Standardized Rating'] = ratings_df['Rating Text'].map(rating_mapping)

    # Group by standardized rating text
    standardized_rating_groups = ratings_df.groupby('Standardized Rating')
    standardized_rating_stats = standardized_rating_groups['Aggregate Rating'].agg(['min', 'max', 'mean', 'count'])
    standardized_rating_stats = standardized_rating_stats.sort_values(by='mean', ascending=False)

    return rating_stats, standardized_rating_stats


def create_threshold_summary(standardized_rating_stats):
    '''
    Add threshold field to standardized_rating_stats.
    '''
    summary_stats = standardized_rating_stats.copy()

    # Set the threshold range for each category
    thresholds = {}
    for category in summary_stats.index:
        if category == 'Not rated':
            thresholds[category] = 'N/A'
        elif category == 'Poor':
            # Assume Poor starts from 0 and ends at 0.1 below the min of Average
            average_min = summary_stats.loc['Average', 'min']
            thresholds[category] = f'0.0 - {average_min - 0.1}'
        else:
            # For other categories, just use their min-max range
            thresholds[category] = f'{summary_stats.loc[category, "min"]} - {summary_stats.loc[category, "max"]}'

    summary_stats['thresholds'] = pd.Series(thresholds)

    # Convert the 0 ratings in "Not rated" category to 'N/A'
    if 'Not rated' in summary_stats.index:
        # Also convert columns to object type before assigning string values, to avoid errors
        for col in ['min', 'max', 'mean']:
            summary_stats[col] = summary_stats[col].astype(object)
        summary_stats.loc['Not rated', ['min', 'max', 'mean']] = 'N/A'

    return summary_stats


def create_rating_histogram(ratings_df):
    """
    Create a histogram showing the distribution of ratings by category.
    """
    # Filter for main categories only
    main_categories = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
    filtered_df = ratings_df[ratings_df['Standardized Rating'].isin(main_categories)]

    plt.figure(figsize=(12, 6))


    # Set colours for each category
    colors = {
        'Excellent': 'green',
        'Very Good': 'blue',
        'Good': 'orange',
        'Average': 'yellow',
        'Poor': 'red'
    }

    # Set bin edges
    bins = [0.0, 2.5, 3.5, 4.0, 4.5, 5.0]

    # Plot histogram for each category
    for category in main_categories:
        category_data = filtered_df[filtered_df['Standardized Rating'] == category]['Aggregate Rating']
        plt.hist(category_data, bins=bins, alpha=0.7, label=category, color=colors[category], 
                edgecolor='black')
    
    # Additional chart details
    plt.title('Distribution of Restaurant Ratings by Category', fontsize=15)
    plt.xlabel('Aggregate Rating', fontsize=12)
    plt.ylabel('Number of Restaurants', fontsize=12)
    plt.legend(title='Rating Category')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])


    output_dir = ensure_output_directory()
    plt.savefig(os.path.join(output_dir, 'restaurant_ratings_histogram.png'))
    plt.show()


def main():
    '''Main function to run script'''
    load_dotenv()
    RESTAURANT_JSON_URL = os.getenv("RESTAURANT_JSON_URL")

    # Fetch and process restaurant ratings data
    data = fetch_restaurant_data(RESTAURANT_JSON_URL)
    rating_data = extract_ratings_data(data)

    # Create DataFrame on ratings data
    ratings_df = pd.DataFrame(rating_data)

    # Analyze ratings
    rating_stats, standardized_rating_stats = analyze_ratings(ratings_df)
    summary_stats = create_threshold_summary(standardized_rating_stats)

    # Display results
    print("\n")
    print("Original Rating Statistics:\n")
    print(rating_stats)
    print("\n\nStandardized Rating Statistics:\n")
    print(standardized_rating_stats)
    print("\n\nFinal Summary Statistics:\n")
    print(summary_stats)

    # Create histogram of ratings
    create_rating_histogram(ratings_df)


if __name__ == "__main__":
    main()
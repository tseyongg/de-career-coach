# Case Study 1

After successful run, you should see your directory populate with folder called `output`. Inside are `restaurant_details.csv` and `restaurant_events.csv`. These pertain to the outputs for Task 1 and Task 2 respectively. Also, you should see an image file, `restaurant_ratings_histogram.png` populate in your directory. This pertains to our analysis for Task 3. You may simply navigate to the `.csv` and `.png` files to view them. These 3 tasks are independent of each other.

## Key Design Decisions

### Task 1

For task 1, I have taken the field `Event_Date` to be the earliest event, or else multiple event dates would have to be input (we have already grabbed all events in task 2). For example, `res_id` = `18382360` which has multiple events. 

```py
event_date = restaurant['zomato_events'][0]['event']['start_date']
```

In the resulting `restaurant_details.csv` file, you should have generated 1280 unique restaurant IDs, with 20 IDs excluded because they fall under `country_code` = `17` which is not in the given Excel file.

### Task 2
Similarly, for task 2, I have taken the field `Photo URL` to be the first image url, or else multiple image urls would have to be input. For example, `event_id`= `292840` which has multiple photos.
Furthermore, if there are no `Photo URL` at all, I pass "NA" instead.

```py
def extract_event_photo_url(event):
    """Extract photo URL from event if possible."""
    if 'photos' in event and event['photos']:
        return event['photos'][0]['photo']['url']
    return "NA"
```

In the resulting `restaurant_events.csv` file, you should have generated 182 unique event IDs, with 2 IDs excluded because they do not overlap with the April 2019 date range in any way.

### Task 3

For task 3, 3 tables will be output in your terminal, `Original Rating Statistics`, `Standardized Rating Statistics`, and `Final Summary Statistics`. This showcases the iterative analytical process I took.

`Original Rating Statistics`

|               | min | max | mean     | count |
|---------------|-----|-----|----------|-------|
| Rating Text   |     |     |          |       |
| Skvělé        | 4.9 | 4.9 | 4.900000 | 1     |
| Terbaik       | 4.7 | 4.8 | 4.750000 | 2     |
| Eccellente    | 4.7 | 4.7 | 4.700000 | 1     |
| Excelente     | 4.5 | 4.9 | 4.700000 | 2     |
| Excellent     | 4.5 | 4.9 | 4.666207 | 435   |
| Muito Bom     | 4.4 | 4.4 | 4.400000 | 1     |
| Muy Bueno     | 4.3 | 4.3 | 4.300000 | 2     |
| Very Good     | 4.0 | 4.4 | 4.215891 | 623   |
| Velmi dobré   | 4.1 | 4.3 | 4.166667 | 3     |
| Bardzo dobrze | 4.1 | 4.1 | 4.100000 | 1     |
| Bueno         | 3.9 | 3.9 | 3.900000 | 1     |
| Good          | 3.5 | 3.9 | 3.776224 | 143   |
| Skvělá volba  | 3.7 | 3.7 | 3.700000 | 1     |
| Average       | 2.5 | 3.4 | 3.193333 | 60    |
| Poor          | 2.2 | 2.2 | 2.200000 | 1     |
| Not rated     | 0.0 | 0.0 | 0.000000 | 23    |

This is the first statistic table obtained on the raw JSON data. <br><br>

`Standardized Rating Statistics`

|                     | min | max | mean     | count |
|---------------------|-----|-----|----------|-------|
| Standardized Rating |     |     |          |       |
| Excellent           | 4.5 | 4.9 | 4.667347 | 441   |
| Very Good           | 4.0 | 4.4 | 4.216032 | 630   |
| Good                | 3.5 | 3.9 | 3.776552 | 145   |
| Average             | 2.5 | 3.4 | 3.193333 | 60    |
| Poor                | 2.2 | 2.2 | 2.200000 | 1     |
| Not rated           | 0.0 | 0.0 | 0.000000 | 23    |

Table after standardization, i.e.  accounting for different languages and converting them all to English. <br><br>

`Final Summary Statistics`

|                     | min | max | mean     | count | thresholds |
|---------------------|-----|-----|----------|-------|------------|
| Standardized Rating |     |     |          |       |            |
| Excellent           | 4.5 | 4.9 | 4.667347 | 441   | 4.5 - 4.9  |
| Very Good           | 4.0 | 4.4 | 4.216032 | 630   | 4.0 - 4.4  |
| Good                | 3.5 | 3.9 | 3.776552 | 145   | 3.5 - 3.9  |
| Average             | 2.5 | 3.4 | 3.193333 | 60    | 2.5 - 3.4  |
| Poor                | 2.2 | 2.2 | 2.2      | 1     | 0.0 - 2.4  |
| Not rated           | N/A | N/A | N/A      | 23    | N/A        |

Final table for analysis, after changing `Not rated` values from "0" to "N/A", and adding threshold field for easier business understanding.

## Final Output

After the above iterative analysis tables, a final histogram plot is generated on the standardized data, with each coloured bin corresponding to the respective category thresholds:

![histogram-plot](output_data/restaurant_ratings_histogram.png)

Here, we see that most restaurants are rated **Very Good**, with more conservative numbers for **Excellent**. This is folloiwed by **Good**, then **Average** ratings. For **Poor** rated restaurants, only one restaurant, `res_id`: `18445965` takes the crown. 

> **Note**: You will not be able to see the .png file here because there is currently no output. On your local run it will populate in your `output` folder which will then populate this section here on your local machine.
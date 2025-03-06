# Case Study 1

## Setup Instructions
Kindly follow the instructions here to run the code for Case Study 1 locally on your laptop.

Simply run the following in your terminal:

```

```

After running this line of code, you should see your directory populate with `restaurant_details.csv` and `restaurant_events.csv`. These pertain to the outputs for Task 1 and Task 2 respectively. Also, you should see an image file, `restaurant_ratings_histogram.png` populate in your directory. This pertains to our analysis for Task 3. You may simply navigate to the `.csv` and `.png` files to view them.

## Key Design Decisions

### Task 1

For task 1, I have taken the field `Event_Date` to be the earliest event, or else multiple event dates would have to be input. For example, `res_id` = `18382360` which has multiple events.

```py
event_date = restaurant['zomato_events'][0]['event']['start_date']
```

### Task 2
Similarly,for task 2, I have taken the field `Photo URL` to be the first image url, or else multiple image urls would have to be input. For example, `event_id`= `292840` which has multiple photos.

```py
photo_url = event['photos'][0]['photo']['url']
```

### Task 3
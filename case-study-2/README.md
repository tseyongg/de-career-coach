# Case Study 2

On successful run, you will be able to query the app from your terminal, unlike Case Study 1, where the container shut down on successful job run (or task runs in our case).

You can enter:

- 1 to search by Carpark Number
- 2 to search by Address
- 3 to end your session

## Key Design Decisions

### Gov API duplicate carpark number handing

The gov API endpoint does return duplicate carpark numbers at times, but rest assured that when that happens, the data are for different lot types. Thus, I accounted for this by first looking up my dictionary `carpark_availability` to check id `carpark_number` is already present:

```py
        # Check if carpark_num already exists in carpark_availability, to account for duplicates
        if carpark_num in carpark_availability:
            lot_types = carpark_availability[carpark_num]['lot_types']
        else:
            lot_types = {}
```

In addition, I also display in my final output to the user the total carpark lots available, thus I implement a running sum technique, where I store `total_lots` and `avail_lots` and sum them together in the event the same `carpark_number` is found again:

```py
        for lot in carpark['carpark_info']:
            lot_type = lot['lot_type']
            lot_type_total = int(lot['total_lots'])
            lot_type_available = int(lot['lots_available'])

            total_lots += lot_type_total
            avail_lots += lot_type_available

            lot_types[lot_type] = {
                'total_lots': lot_type_total,
                'lots_available': lot_type_available
            }

        carpark_availability[carpark_num] = {
            'total_lots': total_lots + (carpark_availability.get(carpark_num, {}).get('total_lots',0)), # Add 0 to total_lots if new carpark_num, else add to existing value
            'available_lots': avail_lots + (carpark_availability.get(carpark_num, {}).get('available_lots',0)), # Add 0 to avail_lots if new carpark_num, else add to existing value
            'lot_types': lot_types,
            'update_time': update_time
        }
```

### Data Merging

I account for `carpark_number` that are:

- Present in both gov API endpoint **and** static HDBCarparkInformation.csv:

```py
for carpark_num, static_data in carpark_static.items():
    if carpark_num in carpark_availability:
        merged_carpark_data[carpark_num] = {
            **static_data,
            'availability': carpark_availability[carpark_num]
        }
```

- Present only in static HDBCarparkInformation.csv, not present in gov API endpoint:
> **Note**: Leave gov API metrics as 'NA'

```py
    else:
        merged_carpark_data[carpark_num] = {
            **static_data,
            'availability': {
                'total_lots': 'NA',
                'available_lots': 'NA',
                'lot_types': {},
                'update_time': 'NA'
            }
        }
```

- Present only in gov API endpoint, not present in static HDBCarparkInformation.csv:
> **Note**: Leave static carpark csv metrics as 'NA'

```py
for carpark_num, availability in carpark_availability.items():
    if carpark_num not in merged_carpark_data:
        merged_carpark_data[carpark_num] = {
            'car_park_no': carpark_num,
            'address': 'NA',
            'x_coord': 'NA',
            'y_coord': 'NA',
            'car_park_type': 'NA',
            'type_of_parking_system': 'NA',
            'short_term_parking': 'NA',
            'free_parking': 'NA',
            'night_parking': 'NA',
            'car_park_decks': 'NA',
            'gantry_height': 'NA',
            'car_park_basement': 'NA',
            'availability': availability
        }
```

### More robust search handling

I have also added safeguards during user search. For example, we are aware all carpark numbers are alphanumeric and are always capitalized. 

I have added validators to enforce alphanumeric nature in [`validators.py`](/case-study-2/utils/validators.py):

```py
if not carpark_number.isalnum():
    return False, "Please enter carpark number with letters and numbers only"
```

I have also trimmed all leading and trailing whitespace in case a user absent-mindedly does so in her input (for both carpark number and address searches), so that the search can still continue:

```py
carpark_number = carpark_number.strip().upper()
```
I have done this in [`user_search.py`](/case-study-2/modules/user_search.py).

I have also implemented additional validation checks for if a user inputs a carpark number that does not exist in our merged data:

```py
if carpark_number not in available_carparks:
    return False, f"Carpark number {carpark_number} not found"
```

 or if a user inputs too short an address:

 ```py
if len(address) < 3:
    return False, "Please ensure address is at least 3 characters long"
 ```

 You may find them in [`validators.py`](/case-study-2/utils/validators.py).


 ### User friendly output

 I have added a [`formatter.py`](/case-study-2/utils/formatter.py) utility so that the user does not get a unformatted JSON response on successful search.

 It works this way:

 If a user searches by carpark number, there can either be no results found or 1 result found, since carpark number is a unique identifier for a carpark.

 So, on 1 result being returned, the user receives the following output similar to this:

 ```shell
Please enter your choice(1-3): 1
Enter carpark number: BRB1
Carpark Number: BRB1
Address: BLK 665 BUFFALO ROAD BASEMENT CAR PARK
Carpark Type: BASEMENT CAR PARK
Parking System: ELECTRONIC PARKING
Location: X:29921.7021, Y:32043.75

AVAILABILITY (Last Updated At: 2025-03-08T20:42:35)
Total: 40/170 available parking lots
By Type:
- Car: 40/170

HOURS & RULES:
Short Term Parking: WHOLE DAY | Free Parking: NO | Night Parking: YES
Decks: 1 | Gantry Height: 1.8m | Basement: Y
 ```
In this case, our user searched for carpark number = `BRB1`. <br><br>

Now, on address search, usually multiple results may be returned, because I do not expect addresses most users have in mind to be exact. But if they are exact, and the address happens to match to a unique carpark, since 1 result is returned, the output will be detailed as it was in the previous case:

```shell
Please enter your choice(1-3): 2
Enter address to search: BLK 278-281 BISHAN STREET 24
Carpark Number: BE36
Address: BLK 278-281 BISHAN STREET 24
Carpark Type: SURFACE CAR PARK
Parking System: ELECTRONIC PARKING
Location: X:29248.3008, Y:37730.4375

AVAILABILITY (Last Updated At: 2025-03-08T22:44:48)
Total: 28/58 available parking lots
By Type:
- Car: 28/58

HOURS & RULES:
Short Term Parking: WHOLE DAY | Free Parking: NO | Night Parking: YES
Decks: 0 | Gantry Height: 4.5m | Basement: N
```

Here, it happens that `BLK 278-281 BISHAN STREET 24` is an address unique to one carpark.

If not, I expect address to be not so specific. And so, say a user searches `bishan street 24`:

```shell
Please enter your choice(1-3): 2
Enter address to search: bishan street 24
Found 4 carparks:

- BE36: BLK 278-281 BISHAN STREET 24
  Available Parking Lots: 28/58 | Last Updated At: 2025-03-08T22:44:48
- BE40: BLK 268A BISHAN STREET 24
  Available Parking Lots: 201/339 | Last Updated At: 2019-06-18T10:58:35
- BE42: BLK 290A BISHAN STREET 24
  Available Parking Lots: 439/852 | Last Updated At: 2025-03-08T22:44:38
- BE45: BLK 275 BISHAN STREET 24
  Available Parking Lots: 75/363 | Last Updated At: 2025-03-08T22:45:36

For more details, please specify an exact carpark number or address.
```

The output in this case will be less detailed, since multiple carparks are returned because they all have `bishan street 24` in their addresses. I thus appended a prompt:

```shell
"For more details, please specify an exact carpark number or address."
```
to encourage the user to make a decision based on the available parking lots above, narrow down to 1 option, and so be able to view more detialed information as in our first 2 cases.


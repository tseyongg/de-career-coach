import os
import sys
from dotenv import load_dotenv

from modules import (
    load_carpark_data,
    get_carpark_availability,
    merge_carpark_data,
    search_by_carpark_number,
    search_by_address,
)

from utils import (
    validate_carpark_number,
    validate_address,
    format_carpark_results
)

# Get needed URLs from .env file
load_dotenv()


API_URL = os.getenv("API_URL")
CSV_URL = os.getenv("CSV_URL")

def display_menu():
    '''Display main menu'''
    print("")
    print("Welcome to Carpark Finder!")
    print("1. Search by Carpark Number")
    print("2. Search by Address")
    print("3. Exit")
    return input("Please enter your choice(1-3): ")

def main():
    print("Loading carpark data...")

    # First, load static CSV data
    carpark_static = load_carpark_data(CSV_URL)

    # Next, fetch real-time carpark availability data
    carpark_availability = get_carpark_availability(API_URL)

    # Then, merge the above data
    merged_carpark_data = merge_carpark_data(carpark_static, carpark_availability)

    print(f"Loaded {len(merged_carpark_data)} carpark data")

    while True:
        choice = display_menu()

        if choice == "1":
           carpark_number = input("Enter carpark number: ")
           is_valid, message = validate_carpark_number(carpark_number, merged_carpark_data)

           if is_valid:
               results = search_by_carpark_number(merged_carpark_data, carpark_number)
               print(format_carpark_results(results))
           else: 
               print(message)

        elif choice == "2":
            address = input("Enter address to search: ")
            is_valid, message = validate_address(address)

            if is_valid:
                results = search_by_address(merged_carpark_data, address)
                print(format_carpark_results(results))
            else:
                print(message)

        elif choice == "3":
            print("Thank you for using our HDB Carpark App!")
            print("")
            sys.exit(0)
        
        else:
            print("Invalid number, please enter 1,2 or 3")


if __name__ =="__main__":
    main()
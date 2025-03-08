def validate_carpark_number(carpark_number, available_carparks):
    '''Validate input carpark number'''
    if not carpark_number:
        return False, "Please enter a carpark number"
    
    # Trim leading and trailing whitespace in case input has extra spaces, and capitalize in case of lowercase input
    carpark_number = carpark_number.strip().upper()
    
    if not carpark_number.isalnum():
        return False, "Please enter carpark number with letters and numbers only"
    
    if carpark_number not in available_carparks:
        return False, f"Carpark number {carpark_number} not found"

    return True, ""


def validate_address(address):
    '''Validate input address'''
    if not address:
        return False, "Please enter an address"
    
    # Trim leading and trailing whitespace in case input has extra spaces
    address = address.strip()

    if len(address) < 3:
        return False, "Please ensure address is at least 3 characters long"

    return True, ""
    

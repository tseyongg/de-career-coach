def format_carpark_results(results):
    """Format carpark search results into human readable form"""
    if not results:
        return "No results found."
    
    if len(results) == 1:
        # Detailed view if single result
        carpark = results[0]
        availability = carpark['availability']
        
        output = [
            f"CARPARK: {carpark['car_park_no']} - {carpark['address']}",
            f"Type: {carpark['car_park_type']} | System: {carpark['type_of_parking_system']}",
            f"Location: X:{carpark['x_coord']}, Y:{carpark['y_coord']}",
            "",
            f"AVAILABILITY (Updated: {availability['update_time']})",
            f"Total: {availability['available_lots']}/{availability['total_lots']} available parking lots",
            "By Type:"
        ]
        
        # Append specific lot types and map single alphabets to full text
        for lot_type, data in availability['lot_types'].items():
            type_name = {'C': 'Car', 'H': 'Heavy Vehicle', 'M': 'Motorcycle'}.get(lot_type, 'Unknown')
            output.append(f"- {type_name}: {data['lots_available']}/{data['total_lots']}")
        
        output.extend([
            "",
            "HOURS & RULES:",
            f"Short Term: {carpark['short_term_parking']} | Free: {carpark['free_parking']} | Night: {carpark['night_parking']}",
            f"Decks: {carpark['car_park_decks']} | Gantry Height: {carpark['gantry_height']}m | Basement: {carpark['car_park_basement']}"
        ])
        
    else:
        # Shortened summary view if multiple results
        output = [f"Found {len(results)} carparks:"]
        for carpark in results:
            avail = carpark['availability']
            output.append(f"- {carpark['car_park_no']}: {carpark['address']}")
            output.append(f"  Available: {avail['available_lots']}/{avail['total_lots']} | Updated: {avail['update_time']}")
    
        output.append("\nFor more details, please specify an exact carpark number.")

    return "\n".join(output)
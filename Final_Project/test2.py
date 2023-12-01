from flask import Flask, render_template, request
import googlemaps
from datetime import datetime
import polyline

def geocode_address(gmaps, address):
    geocode_result = gmaps.geocode(address)
    if not geocode_result:
        print(f"Geocoding failed for address: {address}")
        return None
    return geocode_result[0]['geometry']['location']

def get_directions(api_key, start_address, end_address, departure_date, departure_time, waypoints = None):
    gmaps = googlemaps.Client(key=api_key)

    start_location, end_location = None, None

    # Geocode start and end addresses and waypoint to get coordinates
    start_geocode = gmaps.geocode(start_address)
    end_geocode = gmaps.geocode(end_address)
    waypoint_locations = [geocode_address(gmaps, waypoint) for waypoint in waypoints] if waypoints else None

    if not start_geocode or not end_geocode or (waypoints and not all(waypoint_locations)):
        print("Geocoding failed. Please check your addresses.")
        return None

    start_location = start_geocode[0]['geometry']['location']
    end_location = end_geocode[0]['geometry']['location']

    # Combine date and time strings into a single datetime object
    try:
        departure_datetime = datetime.strptime(departure_date + " " + departure_time, "%Y-%m-%d %I:%M %p")
    except ValueError:
        print("Invalid date or time format.")
        return None

    # Get directions with the specified waypoint and include traffic data
    try:
        directions_result = []

        directions_result.append(gmaps.directions(
            start_location,
            waypoint_locations[0],
            mode="driving",
            departure_time=departure_datetime,
        ))

        for i in range(1, len(waypoint_locations)):
            directions_result.append(gmaps.directions(
                waypoint_locations[i-1],
                waypoint_locations[i],
                mode="driving",
            ))

        directions_result.append(gmaps.directions(
            waypoint_locations[-1],
            end_location,
            mode="driving",
            ))

        total_directions_result = [result for sublist in directions_result for result in sublist]

        # Extract and print route details
        for result in total_directions_result:
            if 'legs' in result and result['legs']:
                route = result['legs'][0]
                print("\nStart Location:")
                print("Latitude:", start_location['lat'])
                print("Longitude:", start_location['lng'])
                print("\nEnd Location:")
                print("Latitude:", end_location['lat'])
                print("Longitude:", end_location['lng'])
                print("\nTrip Distance: ", route['distance']['text'])

                # Check if 'duration_in_traffic' is available
                if 'duration_in_traffic' in route:
                    print("Est. Time Duration (w/ traffic): ", route['duration_in_traffic']['text'])
                    
                print("Departure Time: ", departure_datetime)

                if 'arrival_time' in route:
                    print("Arrival Time: ", datetime.fromtimestamp(route['arrival_time']['value']))

                # Store coordinates in a list
                coordinates_list = []

                # Extract and print coordinates from each step
                for step in route['steps']:
                    polyline_points = step['polyline']['points']
                    decoded_coordinates = polyline.decode(polyline_points)

                # Append all coordinates to the list
                    coordinates_list.extend(decoded_coordinates)
                    
            # print("\nCoordinates along the route:")
            # for coordinate in coordinates_list:
            #    print("Latitude:", coordinate[0])
            #    print("Longitude:", coordinate[1])

            # Return the list of coordinates
            return coordinates_list

        else:
            print("Directions request failed.")
            return None

    except googlemaps.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Full response:", e.response)
        return None

def search_place(api_key, location, place_name):
    gmaps = googlemaps.Client(key=api_key)

if __name__ == "__main__":
    # Read API key from a file
    with open("apiKey.txt", "r") as api_file:
        api_key = api_file.read().strip()

    # Get start and end addresses from user input
    start_address = input("Enter start point: \n")
    end_address = input("\nEnter end point: \n")

    # Get departure date from user input
    departure_date = input("\nEnter departure date (YYYY-MM-DD): \n")

    # Get departure time from user input
    departure_time = input("\nEnter departure time (e.g., 08:00 AM): \n")

    # Get waypoints from user input (comma-separated addresses)
    waypoints_input = input("\nEnter waypoints (if any, comma-separated): \n")
    waypoints = [waypoint.strip() for waypoint in waypoints_input.split(',') if waypoint.strip()]

    # Get and display directions
    coordinates_list = get_directions(api_key, start_address, end_address, departure_date, departure_time, waypoints)

    # Now you can use the 'coordinates_list' variable elsewhere in your code
    if coordinates_list:
        print("Total Coordinates:", len(coordinates_list))
    
    else:
        print("Failed to retrieve coordinates.")

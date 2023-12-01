from flask import Flask, render_template, request
import googlemaps
from datetime import datetime
import polyline

def get_directions(api_key, start_address, end_address, departure_date, departure_time):
    gmaps = googlemaps.Client(key=api_key)

    # Geocode start and end addresses and waypoint to get coordinates
    start_geocode = gmaps.geocode(start_address)
    end_geocode = gmaps.geocode(end_address)

    if not start_geocode or not end_geocode:
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
        directions_result = gmaps.directions(
            start_location,
            end_location,
            mode="driving",
            departure_time=departure_datetime,
        )

        # Extract and print route details
        if directions_result:
            route = directions_result[0]['legs'][0]
            print("\nStart Location:")
            print("Latitude:", start_location['lat'])
            print("Longitude:", start_location['lng'])
            print("\nEnd Location:")
            print("Latitude:", end_location['lat'])
            print("Longitude:", end_location['lng'])
            print("\nTrip Distance: ", route['distance']['text'])

            # Check if 'duration_in_traffic' is available
            if 'duration_in_traffic' in route:
                print("Time Duration (in traffic): ", route['duration_in_traffic']['text'])

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

    # Get and display directions
    coordinates_list = get_directions(api_key, start_address, end_address, departure_date, departure_time)

    # Now you can use the 'coordinates_list' variable elsewhere in your code
    if coordinates_list:
        print("Total Coordinates:", len(coordinates_list))
    
    else:
        print("Failed to retrieve coordinates.")

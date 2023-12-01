import googlemaps
from datetime import datetime
import polyline

def get_directions(api_key, start_address, end_address, departure_date, departure_time):
    gmaps = googlemaps.Client(key=api_key)

    # Geocode start and end addresses to get coordinates
    start_geocode = gmaps.geocode(start_address)
    end_geocode = gmaps.geocode(end_address)

    if not start_geocode or not end_geocode:
        print("Geocoding failed. Please check your addresses.")
        return

    start_location = start_geocode[0]['geometry']['location']
    end_location = end_geocode[0]['geometry']['location']

    # Combine date and time strings into a single datetime object
    try:
        departure_datetime = datetime.strptime(departure_date + " " + departure_time, "%Y-%m-%d %I:%M %p")
    except ValueError:
        print("Invalid date or time format.")
        return

    # Get directions between the two coordinates
    try:
        directions_result = gmaps.directions(
            start_location,
            end_location,
            mode="driving",
            departure_time=departure_datetime
        )

        # Extract and print route details
        if directions_result:
            route = directions_result[0]['legs'][0]
            print("Start Location:")
            print("Latitude:", start_location['lat'])
            print("Longitude:", start_location['lng'])
            print("\nEnd Location:")
            print("Latitude:", end_location['lat'])
            print("Longitude:", end_location['lng'])
            print("\nTrip Distance: ", route['distance']['text'])
            print("Time Duration: ", route['duration']['text'])
            print("Departure Time: ", departure_datetime)
            if 'arrival_time' in route:
                print("Arrival Time: ", datetime.fromtimestamp(route['arrival_time']['value']))

            # Extract and print coordinates from each step
            print("\nCoordinates along the route:")
            for step in route['steps']:
                polyline_points = step['polyline']['points']
                decoded_coordinates = polyline.decode(polyline_points)

                for coordinate in decoded_coordinates:
                    print("Latitude:", coordinate[0])
                    print("Longitude:", coordinate[1])

        else:
            print("Directions request failed.")

    except googlemaps.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Full response:", e.response)

if __name__ == "__main__":
    # Read API key from a file
    with open("apiKey.txt", "r") as api_file:
        api_key = api_file.read().strip()

    # Get start and end addresses from user input
    start_address = input("Enter start point: \n")
    end_address = input("Enter end point: \n")

    # Get departure date from user input
    departure_date = input("Enter departure date (YYYY-MM-DD): \n")

    # Get departure time from user input
    departure_time = input("Enter departure time (e.g., 08:00 AM): \n")

    # Get and display directions
    get_directions(api_key, start_address, end_address, departure_date, departure_time)
import googlemaps
from datetime import datetime
import polyline

api_key = "AIzaSyBiGus_zgx-S8FzZKLFlidy8jFtsbrABhU"

def geocode_address(gmaps, address):
    geocode_result = gmaps.geocode(address)
    if not geocode_result:
        print(f"Geocoding failed for address: {address}")
        return None
    location = geocode_result[0]['geometry']['location']
    print(f"Coordinates for {address}: {location}")
    return location

def split_coordinates(start_address, end_address):
    gmaps = googlemaps.Client(key=api_key)

    start_location = geocode_address(gmaps, start_address)
    end_location = geocode_address(gmaps, end_address)
    
    directions_result = gmaps.directions(
        start_location,
        end_location,
        mode="driving",
        departure_time=datetime.now(),
    )

    route = directions_result[0]['legs'][0]
    coordinates_list = []

    for step in route['steps']:
            polyline_points = step['polyline']['points']
            decoded_coordinates = polyline.decode(polyline_points)
            coordinates_list.extend(decoded_coordinates)

    part_length = len(coordinates_list) // 4

    # Divide the list into 4 parts
    start_point = coordinates_list[0]
    part1 = coordinates_list[part_length]
    part2 = coordinates_list[2 * part_length]
    part3 = coordinates_list[3 * part_length]
    end_point = coordinates_list[-1]

    return start_point, part1, part2, part3, end_point

def get_route_data(start_address, end_address, departure_date, departure_time):
    return get_directions(api_key, start_address, end_address, departure_date, departure_time)

def get_directions(api_key, start_address, end_address, departure_date, departure_time):
    gmaps = googlemaps.Client(key=api_key)

    start_location = geocode_address(gmaps, start_address)
    end_location = geocode_address(gmaps, end_address)
    waypoint_locations = [geocode_address(gmaps, waypoint) for waypoint in waypoints] if waypoints else []

    if not start_location or not end_location or (waypoints and not all(waypoint_locations)):
        print("Geocoding failed. Please check your addresses.")
        return None

    # Combine date and time strings into a single datetime object
    try:
        departure_datetime = datetime.strptime(departure_date + " " + departure_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return None

    total_directions_result = []
    total_duration_traffic = 0  # Total duration considering traffic

    # Directions between waypoints
    for i in range(len(waypoint_locations) + 1):
        start = start_location if i == 0 else waypoint_locations[i - 1]
        end = end_location if i == len(waypoint_locations) else waypoint_locations[i]

        directions_result = gmaps.directions(
            start,
            end,
            mode="driving",
            departure_time=departure_datetime,
        )

        total_directions_result.append(directions_result[0])

        route = directions_result[0]['legs'][0]

        print(f"\nFrom {start_address if i == 0 else waypoints[i - 1]} to "
              f"{end_address if i == len(waypoint_locations) else waypoints[i]}:")
        print("Distance:", route['distance']['text'])

        # Check if 'duration_in_traffic' is available
        if 'duration_in_traffic' in route:
            duration_traffic = route['duration_in_traffic']['value']
            total_duration_traffic += duration_traffic
            print("Est. Time Duration (w/ traffic): ", route['duration_in_traffic']['text'])
        else:
            duration = route['duration']['value']
            total_duration_traffic += duration
            print("Est. Time Duration: ", route['duration']['text'])

    # Calculate and print total trip distance and duration
    total_trip_distance = sum(result['legs'][0]['distance']['value'] for result in total_directions_result) / 1609.34
    total_duration_hours, total_duration_minutes = divmod(total_duration_traffic // 60, 60)
    print("\nTotal Trip Distance:", total_trip_distance, "mi")
    print(f"Total Trip Duration (w/ traffic): {total_duration_hours} hours {total_duration_minutes} minutes")

    print("Departure Time: ", departure_datetime)
 
    return total_trip_distance, total_duration_hours, total_duration_minutes

if __name__ == "__main__":
    api_key = "AIzaSyBiGus_zgx-S8FzZKLFlidy8jFtsbrABhU"

    # Get start and end addresses from user input
    start_address = input("Enter start point:\n")
    end_address = input("\nEnter end point:\n")

    # Get departure date from user input
    departure_date = input("\nEnter departure date (YYYY-MM-DD):\n")

    # Get departure time from user input
    departure_time = input("\nEnter departure time (14:00):\n")

    # Get waypoints from user input (comma-separated addresses)
    waypoints_input = input("\nEnter waypoints (if any, comma-separated latitude,longitude):\n")
    waypoints = [{'lat': float(coord.split(',')[0]), 'lng': float(coord.split(',')[1])} for coord in waypoints_input.split(',') if coord.strip()]

    coordinates_list = get_directions(api_key, start_address, end_address, departure_date, departure_time)

    if coordinates_list:
        print(split_coordinates(start_address, end_address))
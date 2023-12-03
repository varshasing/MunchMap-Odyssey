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
    # print(f"Coordinates for {address}: {location}")
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
    five_coord_list = []

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

    five_coord_list = [start_point, part1, part2, part3, end_point]

    # write code that will return a list of 5 coordinates, each coordinate being a dictionary with keys "lat" and "lng" from five_coord_list
    five_coord_list[0] = {"lat": five_coord_list[0][0], "lng": five_coord_list[0][1]}
    five_coord_list[1] = {"lat": five_coord_list[1][0], "lng": five_coord_list[1][1]}
    five_coord_list[2] = {"lat": five_coord_list[2][0], "lng": five_coord_list[2][1]}
    five_coord_list[3] = {"lat": five_coord_list[3][0], "lng": five_coord_list[3][1]}
    five_coord_list[4] = {"lat": five_coord_list[4][0], "lng": five_coord_list[4][1]}

    return five_coord_list

def get_two_point_data(start_coords, end_coords, departure_date, departure_time):
    gmaps = googlemaps.Client(key=api_key)
    start_location = start_coords
    end_location = end_coords
    waypoint_locations = []

    try:
        departure_datetime = datetime.strptime(departure_date + " " + departure_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return None

    total_distance = 0  # Total distance
    total_duration_traffic = 0  # Total duration considering traffic

    for i in range(len(waypoint_locations) + 1):
        start = start_location if i == 0 else waypoint_locations[i - 1]
        end = end_location if i == len(waypoint_locations) else waypoint_locations[i]

        directions_result = gmaps.directions(
            start,
            end,
            mode="driving",
            departure_time=departure_datetime,
        )

        route = directions_result[0]['legs'][0]

        # print(f"\nFrom {start} to {end}:")
        # print("Distance:", route['distance']['text'])

        total_distance += route['distance']['value']

        # Check if 'duration_in_traffic' is available
        if 'duration_in_traffic' in route:
            duration_traffic = route['duration_in_traffic']['value']
            total_duration_traffic += duration_traffic
            # print("Est. Time Duration (w/ traffic): ", route['duration_in_traffic']['text'])
        else:
            duration = route['duration']['value']
            total_duration_traffic += duration
            # print("Est. Time Duration: ", route['duration']['text'])

    # Print total duration and distance
    total_duration_hours, total_duration_minutes = divmod(total_duration_traffic // 60, 60)
    # print(f"\nTotal Duration (w/ traffic): {total_duration_hours} hours {total_duration_minutes} minutes")
    # print(f"Total Distance: {total_distance / 1609.34} mi")  # Convert meters to miles

    trip_dict = {
        "distance": round(total_distance / 1609.34,1),  # Convert meters to miles
        "hours": total_duration_hours,
        "minutes": total_duration_minutes
    }

    return trip_dict

def get_route_data(start_coords, end_coords, waypoint_coords, departure_date, departure_time):
    if waypoint_coords == None:
        return get_two_point_data(start_coords, end_coords, departure_date, departure_time)
    else:
        start_to_waypoint = get_two_point_data(start_coords, waypoint_coords, departure_date, departure_time)
        waypoint_to_end = get_two_point_data(waypoint_coords, end_coords, departure_date, departure_time)
        combined_data = {
            "distance": round(start_to_waypoint["distance"] + waypoint_to_end["distance"], 1),
            "hours": start_to_waypoint["hours"] + waypoint_to_end["hours"],
            "minutes": start_to_waypoint["minutes"] + waypoint_to_end["minutes"]
            #need to implement minutes overflow
        }
        if combined_data["minutes"] >= 60:
            combined_data["hours"] += 1
            combined_data["minutes"] -= 60
        return combined_data


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

    trip_dict = {
        "distance": total_trip_distance,
        "hours": total_duration_hours,
        "minutes": total_duration_minutes
    }
 
    return trip_dict

def get_directions_waypoint(api_key, start_address, end_address, waypoints, departure_date, departure_time):
    gmaps = googlemaps.Client(key=api_key)

    start_location = geocode_address(gmaps, start_address)
    end_location = geocode_address(gmaps, end_address)
    waypoint_locations = waypoints if waypoints else []

    if not start_location or not end_location or (waypoints and not all(waypoint_locations)):
        print("Geocoding failed. Please check your addresses.")
        return None

    # Combine date and time strings into a single datetime object
    try:
        departure_datetime = datetime.strptime(departure_date + " " + departure_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date or time format.")
        return None

    total_duration_traffic = 0  # Total duration considering traffic

    # Directions between waypoints using Distance Matrix API
    for i in range(len(waypoint_locations) + 1):
        start = start_location if i == 0 else waypoint_locations[i - 1]
        end = end_location if i == len(waypoint_locations) else waypoint_locations[i]

        matrix_result = gmaps.distance_matrix(
            origins=[start],
            destinations=[end],
            mode="driving",
            departure_time=departure_datetime,
        )

        if 'rows' in matrix_result and 'elements' in matrix_result['rows'][0]:
            element = matrix_result['rows'][0]['elements'][0]

            print(f"\nFrom {start_address if i == 0 else waypoint_locations[i - 1]} to "
                  f"{end_address if i == len(waypoint_locations) else waypoint_locations[i]}:")

            # Check if 'duration_in_traffic' is available
            if 'duration_in_traffic' in element:
                duration_traffic = element['duration_in_traffic']['value']
                total_duration_traffic += duration_traffic
                print("Est. Time Duration (w/ traffic): ", element['duration_in_traffic']['text'])
            elif 'duration' in element:
                duration = element['duration']['value']
                total_duration_traffic += duration
                print("Est. Time Duration: ", element['duration']['text'])
            else:
                print("Unable to retrieve duration information.")

    # Print total duration
    total_duration_hours, total_duration_minutes = divmod(total_duration_traffic // 60, 60)
    print(f"\nTotal Duration (w/ traffic): {total_duration_hours} hours {total_duration_minutes} minutes")

    print("Departure Time: ", departure_datetime)

    trip_dict = {
        "hours": total_duration_hours,
        "minutes": total_duration_minutes
    }

    return trip_dict

if __name__ == "__main__":
    # # Get start and end addresses from user input
    # start_address = input("Enter start point:\n")
    # end_address = input("\nEnter end point:\n")

    # # Get departure date from user input
    # departure_date = input("\nEnter departure date (YYYY-MM-DD):\n")

    # # Get departure time from user input
    # departure_time = input("\nEnter departure time (14:00):\n")

    # # Get waypoints from user input (comma-separated latitude,longitude pairs)
    # waypoints_input = input("\nEnter waypoints (if any, comma-separated addresses):\n")
    # waypoints = [waypoint.strip() for waypoint in waypoints_input.split(',') if waypoint.strip()]

    # # Use get_directions_waypoint instead of get_directions
    # coordinates_list = get_directions_waypoint(api_key, start_address, end_address, waypoints, departure_date, departure_time)

    # if coordinates_list:
    #     print(split_coordinates(start_address, end_address))

    gmaps = googlemaps.Client(key=api_key)
    coords = split_coordinates("New York", "Boston")
    rest_coords = {
        "lat": 37.77485, 
        "lng": -122.42284
        
    }
    san_fran_coords = { 
        "lat": 37.7749,
        "lng": 122.4194
    }
    meridan_coords = {
        "lat": 41.5382,
        "lng": 72.8070
    }
    print(get_two_point_data(coords[0], meridan_coords, "2023-12-04", "06:00")) #BUG WHEN RUNNING SAN FRAN COORDS
    print(get_route_data(coords[0], meridan_coords, coords[4], "2023-12-04", "06:00"))
from flask import Flask, render_template, request
import googlemaps
from datetime import datetime
import polyline
from jinja2 import Template

def get_directions(api_key, start_address, end_address, departure_date, departure_time, waypoint_name):
    gmaps = googlemaps.Client(key=api_key)

    # Geocode start and end addresses and waypoint to get coordinates
    start_geocode = gmaps.geocode(start_address)
    end_geocode = gmaps.geocode(end_address)
    waypoint_geocode = gmaps.geocode(waypoint_name)

    if not start_geocode or not end_geocode or not waypoint_geocode:
        print("Geocoding failed. Please check your addresses.")
        return None

    start_location = start_geocode[0]['geometry']['location']
    end_location = end_geocode[0]['geometry']['location']
    waypoint_location = waypoint_geocode[0]['geometry']['location']

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
            waypoints=[waypoint_location],
            departure_time=departure_datetime,
            traffic_model="best_guess"  # Options: "best_guess", "pessimistic", "optimistic"
        )

        # Extract and print route details
        if directions_result:
            route = directions_result[0]['legs'][0]
            print("\nStart Location:")
            print("Latitude:", start_location['lat'])
            print("Longitude:", start_location['lng'])
            print("\nWaypoint Location:")
            print("Latitude:", waypoint_location['lat'])
            print("Longitude:", waypoint_location['lng'])
            print("\nEnd Location:")
            print("Latitude:", end_location['lat'])
            print("Longitude:", end_location['lng'])
            print("\nTrip Distance: ", route['distance']['text'])

            # Check if 'duration_in_traffic' is available
            if 'duration_in_traffic' in route:
                print("Time Duration (in traffic): ", route['duration_in_traffic']['text'])
            else:
                print("Time Duration (in traffic): Not available")

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
            # return coordinates_list

        else:
            print("Directions request failed.")
            return None

    except googlemaps.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print("Full response:", e.response)
        return None

def generate_html_map(api_key, coordinates_list):
    # Load HTML template with Google Maps JavaScript API
    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Embedded Map</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&callback=initMap" 
            async defer></script>
        <script>
            function initMap() {
                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 10,
                    center: {lat: {{ center_lat }}, lng: {{ center_lng }}}
                });

                var coordinates = {{ coordinates }};
                var path = [];
                
                for (var i = 0; i < coordinates.length; i += 2) {
                    path.push({lat: coordinates[i], lng: coordinates[i + 1]});
                }

                var route = new google.maps.Polyline({
                    path: path,
                    geodesic: true,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 2
                });

                route.setMap(map);
            }
        </script>
    </head>
    <body>
        <div id="map" style="height: 500px;"></div>
    </body>
    </html>
    """)

    # Calculate the center of the map
    center_lat = sum(coordinates_list[i] for i in range(0, len(coordinates_list), 2)) / (len(coordinates_list) / 2)
    center_lng = sum(coordinates_list[i + 1] for i in range(0, len(coordinates_list), 2)) / (len(coordinates_list) / 2)

    # Render the HTML template with data
    html_content = html_template.render(
        api_key=api_key,
        coordinates=coordinates_list,
        center_lat=center_lat,
        center_lng=center_lng
    )

    # Write the HTML content to a file
    with open("embedded_map.html", "w") as html_file:
        html_file.write(html_content)

def search_place(api_key, location, place_name):
    gmaps = googlemaps.Client(key=api_key)

    # Use Google Maps Places API to search for the specified place
    places_result = gmaps.places(place_name, location=location, radius=5000)

    if places_result and "results" in places_result and places_result["results"]:
        place = places_result["results"][0]
        return {
            "Name": place["name"],
            "Coordinates": place["geometry"]["location"],
        }
    else:
        print("No places found.")
        return None

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

    # Allow the user to input a place/restaurant name as a waypoint
    waypoint_name = input("\nEnter a place or restaurant name as a waypoint: \n")

    # Get and display directions
    coordinates_list = get_directions(api_key, start_address, end_address, departure_date, departure_time, waypoint_name)

    # Now you can use the 'coordinates_list' variable elsewhere in your code
    if coordinates_list:
        print("Total Coordinates:", len(coordinates_list))
    
    else:
        print("Failed to retrieve coordinates.")

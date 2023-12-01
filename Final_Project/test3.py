from flask import Flask, render_template, request
import googlemaps
from datetime import datetime
import polyline
from jinja2 import Template

app = Flask(__name__)

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

    # Use Distance Matrix API to get travel distance and time
    try:
        distance_matrix_result = gmaps.distance_matrix(
            origins=[start_location],
            destinations=[end_location, waypoint_location],
            mode="driving",
            departure_time=departure_datetime,
            traffic_model="best_guess"  # Options: "best_guess", "pessimistic", "optimistic"
        )

        # Extract travel distance and time
        if distance_matrix_result and distance_matrix_result['status'] == 'OK':
            overall_distance = distance_matrix_result['rows'][0]['elements'][0]['distance']['value']
            overall_duration = distance_matrix_result['rows'][0]['elements'][0]['duration']['value']

            return overall_distance, overall_duration

        else:
            print("Distance Matrix request failed.")
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
        <script src="https://maps.googleapis.com/maps/api/js?key={{ AIzaSyBiGus_zgx-S8FzZKLFlidy8jFtsbrABhU }}&callback=initMap" 
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
        <p>Overall Distance: {{ overall_distance }} meters</p>
        <p>Overall Duration: {{ overall_duration }} seconds</p>
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
        center_lng=center_lng,
        overall_distance=overall_distance,
        overall_duration=overall_duration
    )

    return html_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Replace with your actual Google Maps API key
        api_key = "AIzaSyBiGus_zgx-S8FzZKLFlidy8jFtsbrABhU"

        # Get form data
        start_address = request.form['start_address']
        end_address = request.form['end_address']
        departure_date = request.form['departure_date']
        departure_time = request.form['departure_time']
        waypoint_name = request.form['waypoint_name']

        # Get directions and distance matrix data
        directions_data = get_directions(api_key, start_address, end_address, departure_date, departure_time, waypoint_name)

        if directions_data:
            overall_distance, overall_duration = directions_data

            # Generate HTML map
            html_content = generate_html_map(api_key, coordinates_list)
            return html_content

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

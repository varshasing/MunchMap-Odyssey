from flask import Flask, render_template, request, jsonify
from gmaps import split_coordinates, get_two_point_data, get_route_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('mapstest.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Hardcoded start, waypoint, and end addresses
    start_address = "514 Park Drive, Boston, MA"
    waypoint_address = "456 Main Street, Somewhere, USA"
    end_address = "123 Main Street, Anytown, USA"

    # Use your directions script to get coordinates and other data
    start_coords = {"lat": 42.349845, "lng": -71.101715}
    waypoint_coords = {"lat": 41.878113, "lng": -87.629799}  # Chicago, IL as an example
    end_coords = {"lat": 40.712776, "lng": -74.005974}

    # Other data you might need for the map
    trip_data = get_route_data(start_coords, waypoint_coords, end_coords, "2023-12-04", "06:00")

    # Adjusted the structure of waypoints for the directions request
    waypoints = [
        {'location': waypoint_address, 'stopover': True}
    ]

    return jsonify({
        'start_coords': start_coords,
        'waypoint_coords': waypoint_coords,
        'end_coords': end_coords,
        'waypoints': waypoints,  # Include waypoints in the response
        'trip_data': trip_data,
    })

if __name__ == '__main__':
    app.run(debug=True)

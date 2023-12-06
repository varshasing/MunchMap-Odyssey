from flask import Flask, render_template, request, session
import datetime
from yelpapi import search_yelp, get_coords, getRestaurantData, singleList
from weather import get_weather, getDate, getTime
from gmaps import get_two_point_data, get_route_data, split_coordinates

app = Flask(__name__)
app.secret_key = "thisboxdreamsofbecominganotherbox.makedreamscometrue.chipsahoy.nucleophilesodiumethoxide"

@app.route('/', methods=['GET','POST'])
def index():
    
    # gets current time for the calendar display
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    
    #initializing variables
    cuisine = None
    budget = None
    formFilled = None
    yelpList = None
    travelData = None
    
    #if first form is filled
    if request.method == 'POST':
        
        #request data from form
        startingpt = request.form['startingpt']
        endingpt = request.form['endingpt']
        date = request.form['date']
        departure_time = request.form['departure_time']
        cuisine = request.form['cuisine']
        budget = request.form.get('budget', 1)  
        
        #store form inputs in a session
        session["startingpt"] = startingpt
        session["endingpt"] = endingpt
        session["date"] = date
        session["departure_time"] = departure_time
        session["cuisine"] = cuisine
        session['budget'] = budget
        
        #calculating list of restaurants
        formFilled = 1
        search_term = cuisine
        userPrice = int(budget)
        coords = split_coordinates(startingpt, endingpt)
        lat_lon = get_coords(coords)
        latitude = lat_lon[0]
        longitude = lat_lon[1]
        yelpList = singleList(search_yelp(search_term, userPrice, latitude, longitude))
        travelData = getRestaurantData(coords[0], date, departure_time, yelpList)
        
        #storing data in the session
        session["yelpList"] = yelpList
        session["travelData"] = travelData
        session["coords"] = coords
        
    #rendering the home page with necessary data
    return render_template('index.html', min_date=today, max_date=five_days_later, restaurants=yelpList, formFilled=formFilled, travelData=travelData)

@app.route('/result', methods=['GET', 'POST'])
def result():
    
    #getting data from the session
    coords = session["coords"]
    date = session["date"]
    departure_time = session["departure_time"]
    
    #initializing variables
    restaurant = None
    routeData = None
    
    #if second form is filled
    if request.method == 'POST':
        
        #request data from form
        option = request.form.get('options', None)        
        
        if option:
            #gets route information if restaurant is chosen
            restaurant = session["yelpList"][int(option)-1]
            restaurant_coords = {
                "lat": restaurant["coordinates"]["latitude"],
                "lng": restaurant["coordinates"]["longitude"]
            }
            routeData = get_route_data(coords[0], restaurant_coords, coords[4], session["date"], session["departure_time"])
        else:
            #if not gets only the data between endpoints
            routeData = get_two_point_data(coords[0], coords[4], session["date"], session["departure_time"])
        
    #calculating weather data
    month, day = getDate(date)
    hr, minute = getTime(departure_time)
    duration = (routeData["hours"]*60 + routeData["minutes"])*60
    data = get_weather(coords[0]["lat"], coords[0]["lng"], coords[4]["lat"], coords[4]["lng"], month, day, hr, minute, duration)
        
    #rendering the second page with necessary data
    return render_template('result.html', data=data, session=session, hr=hr, minute=minute, option = option, restaurant=restaurant, routeData=routeData, coords=coords)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, session, url_for
import datetime
from yelpapi import search_yelp, get_coords, getRestaurantData, singleList
from weather import main2 as get_weather
from weather import getDate, getTime
from gmaps import get_two_point_data, get_route_data, split_coordinates

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/', methods=['GET','POST'])
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()

    # Define your search term and coordinates
    
    search_term = "Italian" #Passed by front end
    latitude = 37.7749  #passed by google maps api
    longitude = -122.4194 #passed by google maps api
    userPrice = 2   #passed by front end
    
    cuisine = search_term
    budget = userPrice
    formFilled = None
    yelpList = None
    travelData = None
    
    if request.method == 'POST':
        startingpt = request.form['startingpt']
        endingpt = request.form['endingpt']
        date = request.form['date']
        departure_time = request.form['departure_time']
        cuisine = request.form['cuisine']
        budget = request.form.get('budget', 1)  
        session["startingpt"] = startingpt
        session["endingpt"] = endingpt
        session["date"] = date
        session["departure_time"] = departure_time
        session["cuisine"] = cuisine
        session['budget'] = budget
        formFilled = 1
        
        search_term = cuisine
        userPrice = int(budget)
        
        
        
        # search_term = "pasta" #Passed by front end
        coords = split_coordinates(startingpt, endingpt)
        lat_lon = get_coords(coords)
        latitude = lat_lon[0]
        longitude = lat_lon[1]
        # latitude = [0, 37.7749, 30.34752626717497, 34.0522, 0]  #passed by google maps api
        # longitude = [0, -122.4194, -97.85619684525354, -118.2437 ,0] #passed by google maps api
        # userPrice = 2   #passed by front end
        
        # this will need to be called AFTER user enters their search_term.
        yelpList = singleList(search_yelp(search_term, userPrice, latitude, longitude))
    
        
        travelData = getRestaurantData(coords[0], date, departure_time, yelpList)
        session["yelpList"] = yelpList
        session["travelData"] = travelData
        session["coords"] = coords
        

    
    return render_template('index.html', min_date=today, max_date=five_days_later, restaurants=yelpList, formFilled=formFilled, travelData=travelData)

@app.route('/result', methods=['GET', 'POST'])
def result():
    coords = session["coords"]
    date = session["date"]
    departure_time = session["departure_time"]
    restaurant = None
    routeData = None
    testData1 = None
    testData2 = None
    
    if request.method == 'POST':
        option = request.form.get('options', None)        
        if option:
            restaurant = session["yelpList"][int(option)-1]
            restaurant_coords = {
                "lat": restaurant["coordinates"]["latitude"],
                "lng": restaurant["coordinates"]["longitude"]
            }
            routeData = get_route_data(coords[0], restaurant_coords, coords[4], session["date"], session["departure_time"])
        else:
            routeData = get_two_point_data(coords[0], coords[4], session["date"], session["departure_time"])
        
    month, day = getDate(date)
    hr, minute = getTime(departure_time)
    duration = (routeData["hours"]*60 + routeData["minutes"])*60
    data = get_weather(coords[0]["lat"], coords[0]["lng"], coords[4]["lat"], coords[4]["lng"], month, day, hr, minute, duration)
        
    return render_template('result.html', data=data, session=session, hr=hr, minute=minute, option = option, restaurant=restaurant, routeData=routeData, coords=coords)

if __name__ == '__main__':
    app.run(debug=True)
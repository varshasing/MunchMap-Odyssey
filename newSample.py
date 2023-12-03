from flask import Flask, render_template, request, redirect, session, url_for
import datetime
from yelpapi import search_yelp
from weather import main2 as get_weather
from weather import getDate, getTime

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/', methods=['GET','POST'])
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    api_key = 'XtBEd799ZH3FUzVDWVNHO9eUYrpzzs5Gvz9ps6SfowXMtsyS53dp0_iUajAKAuQKpis1nqYz0u0m4sAk_MSq3BY2B7uZlv-UXLtMNjNLAgDgusF6cXPo71fRuD1sZXYx'

    # Define your search term and coordinates
    
    search_term = "Italian" #Passed by front end
    latitude = [0, 37.7749, 30.34752626717497, 34.0522, 0]  #passed by google maps api
    longitude = [0, -122.4194, -97.85619684525354, -118.2437 ,0] #passed by google maps api
    userPrice = 2   #passed by front end
    
    cuisine = search_term
    budget = userPrice
    formFilled = None
    
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
    
    # this will need to be called AFTER user enters their search_term.
    yelpList = search_yelp(api_key, search_term, userPrice, latitude, longitude,)
    
    return render_template('newIndex.html', min_date=today, max_date=five_days_later, restaurants=yelpList, formFilled=formFilled)

@app.route('/result', methods=['GET', 'POST'])
def result():
    cuisine = session['cuisine']
    startingpt = session["startingpt"]
    endingpt = session["endingpt"]
    date = session["date"]
    departure_time = session["departure_time"]
    cuisine = session["cuisine"]
    
    if request.method == 'POST':
        option = request.form.get('options', None)        
        
    start_lat = 42.3554334
    start_lon = -71.060511
    end_lat = 40.7127281
    end_lon = -74.0060152
    month, day = getDate(date)
    hr, minute = getTime(departure_time)
    duration = 30000
    data = get_weather(start_lat, start_lon, end_lat, end_lon, month, day, hr, minute, duration)
        
    return render_template('result.html', data=data, session=session, hr=hr, minute=minute, option = option)

if __name__ == '__main__':
    app.run(debug=True)
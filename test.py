from flask import Flask, render_template, request, redirect, session, url_for
import datetime
from weather import main as get_weather
from weather import WeatherData

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/', methods=['GET','POST'])
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    name = "Varsha's Restaurant"
    duration = "1"
    distance = "1"
    budget = "$$"
    hours = "9am-5pm"
    address = "123 Main St, Boston, MA"
    
    if request.method == 'POST':
        startingpt = request.form['startingpt']
        endingpt = request.form['endingpt']
        date = request.form['date']
        departure_time = request.form['departure_time']
        cuisine = request.form['cuisine']
        session["startingpt"] = startingpt
        session["endingpt"] = endingpt
        session["date"] = date
        session["departure_time"] = departure_time
        session["cuisine"] = cuisine
        
    return render_template('oldIndex.html', min_date=today, max_date=five_days_later, restName1 = name, restDuration1 = duration, restDistance1 = distance, restBudget1 = budget, restHours1 = hours, restAddress1 = address)

@app.route('/result', methods=['GET', 'POST'])
def result():
    cuisine = session['cuisine']
    startingpt = session["startingpt"]
    endingpt = session["endingpt"]
    date = session["date"]
    departure_time = session["departure_time"]
    cuisine = session["cuisine"]
    
    if request.method == 'POST':
        option = request.form['options']
        
    return render_template('result.html', cuisine=cuisine, session=session)

if __name__ == '__main__':
    app.run(debug=True)

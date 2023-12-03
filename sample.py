from flask import Flask, render_template, request, redirect
import datetime
from yelpapi import search_yelp

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    # Replace 'YOUR_API_KEY' with your actual Yelp API key
    api_key = 'riko09ZEG7R1wBgMqZbjv4uNtMHGBb-t1-2zFrGjAy7Ka2nRwVqD8t3-6GPJXMTfDJEiuQ0RlM24Qh6umi_rVm2Gs7szTULJDRYPfsBEtPYqo0if4YP1_-RLlb9eZXYx'

    # Define your search term and coordinates
    search_term = "Italian" #Passed by front end
    latitude = 37.7749  #passed by google maps api
    longitude = -122.4194 #passed by google maps api
    userPrice = 2   #passed by front end

    # this will need to be called AFTER user enters their search_term.
    yelpList = search_yelp(api_key, search_term, userPrice, latitude, longitude,)
    
    if request.method == 'POST':
        return redirect('/result')
    
    return render_template('index.html', min_date=today, max_date=five_days_later, restaurants=yelpList)

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    #hello
    app.run(debug=True)
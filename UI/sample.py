from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    name = "Varsha's Restaurant"
    duration = "1"
    distance = "1"
    budget = "$$"
    hours = "9am-5pm"
    address = "123 Main St, Boston, MA"
    
    return render_template('index.html', min_date=today, max_date=five_days_later, restName1 = name, restDuration1 = duration, restDistance1 = distance, restBudget1 = budget, restHours1 = hours, restAddress1 = address)

if __name__ == '__main__':
    app.run(debug=True)

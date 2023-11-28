from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.date.today().isoformat()
    five_days_later = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
    return render_template('index.html', min_date=today, max_date=five_days_later)

if __name__ == '__main__':
    app.run(debug=True)

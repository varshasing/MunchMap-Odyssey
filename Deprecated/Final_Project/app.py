from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def directions():
    return render_template('directions.html')

if __name__ == '__main__':
    app.run(debug=True)

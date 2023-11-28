from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']  # Access the form data
        
        # Here you can process the submitted form data (e.g., save to a database, perform operations)
        
        return f'Thank you for submitting your email: {email}'

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask 
# app = Flask(__name__) 

# @app.route('/') 
# def hello_world(): 
#     return 'Flask is great!' 

# if __name__ == '__main__': 
#     app.run() 

# # Defining the home page of our site
# @app.route("/")  # this sets the route to this page
# def home():
# 	return "Hello! this is the main page <h1>HELLO</h1>"  # some basic inline html


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("simplebrowser.html")

if __name__ == "__main__":
    app.run()

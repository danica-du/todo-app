from flask import Flask
app = Flask(__name__)  # create an app instance

# at the end point /, call hello()
@app.route("/")
def hello():
    return "Hello World!"

# on running python app.py, run the flask app
if __name__ == "__main__":
    app.run()
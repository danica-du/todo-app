from flask import Flask
app = Flask(__name__)  # create an app instance

# at the end point /, call hello()
@app.route("/")
def hello():
    return "Hello World!"

# at the end point /<name>, call hello_name(name)
@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

# on running python app.py, run the flask app
if __name__ == "__main__":
    app.run(debug=True)
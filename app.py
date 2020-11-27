from flask import Flask, request, jsonify
from models import Schema
from service import ToDoService
import json

app = Flask(__name__)  # create an app instance

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response

# at the end point /, call hello()
@app.route("/")
def hello():
    return "Hello World!"

# at the end point /<name>, call hello_name(name)
@app.route("/<name>")
def hello_name(name):
    return "Hello " + name

@app.route("/todo", methods=["POST"])
def create_todo():
    return jsonify(ToDoService().create(request.get_json()))

@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(ToDoService().delete(item_id))

@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))

@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list_items())

# on running python app.py, run the flask app
if __name__ == "__main__":
    Schema()  # create tables before app.run() command
    app.run(debug=True)

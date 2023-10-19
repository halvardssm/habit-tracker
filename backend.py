from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/habits", methods=["GET", "POST"])
def habit():
    return "Hello, World!"


@app.route("/habits/<int:habit_id>", methods=["GET", "PUT"])
def habit():
    return "Hello, World!"


@app.route("/habits/<int:habit_id>/tasks", methods=["GET"])
def habit_tasks():
    return "Hello, World!"


@app.route("/tasks", methods=["GET"])
def habit_tasks():
    return "Hello, World!"

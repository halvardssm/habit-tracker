from datetime import datetime
from flask import Flask, jsonify, request
import json
from db import habit_create, habit_list, task_complete, task_list
from habit import Habit
import argparse
from werkzeug.exceptions import HTTPException
import traceback

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    print(traceback.format_exc())

    return jsonify(message=getattr(e, "message", repr(e))), 400


@app.route("/")
def status():
    """A simple endpoint to verify the reachability of the server"""
    return jsonify(status="ok")


@app.route("/habits", methods=["GET", "POST"])
def habit():
    """Endpoint to interract with habits"""

    if request.method == "POST":
        """Create a new habit"""

        data = json.loads(request.data)
        habit = Habit(
            name=data.get("name"),
            description=data.get("description"),
            interval=data.get("interval"),
            lifetime=data.get("lifetime"),
            active=data.get("active"),
            start=data.get("start"),
            end=data.get("end"),
        )
        habit_create(habit)
        return jsonify(habit.to_dict())
    else:
        """List habits with filtering support"""

        id = request.args.get("id", None, int)
        habits = habit_list(id)
        return jsonify([habit.to_dict() for habit in habits])


@app.route("/tasks", methods=["GET", "PATCH"])
def tasks():
    if request.method == "PATCH":
        """Marks a task as completed"""

        data = json.loads(request.data)
        task_complete(data["id"])
        return "ok"
    else:
        """List tasks with filtering support"""

        habit_id = request.args.get("habit_id", None, int)
        tasks = task_list(habit_id)
        return jsonify([task.to_dict() for task in tasks])


parser = argparse.ArgumentParser(description="Habit Tracker Server")
parser.add_argument("--port", type=int, help="Port to run the server on", default=5000)

args = parser.parse_args()

app.run(debug=True, use_reloader=False, port=args.port)

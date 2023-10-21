from datetime import datetime
from flask import Flask, jsonify, request
import json
from db import habit_create, habit_list, habit_update, task_complete, task_list
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


@app.route("/habits", methods=["GET", "POST", "PUT"])
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
    elif request.method == "PUT":
        """Update an existing habit"""

        data = json.loads(request.data)
        habit = Habit(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            interval=data.get("interval"),
            lifetime=data.get("lifetime"),
            active=data.get("active"),
            start=data.get("start"),
            end=data.get("end"),
        )
        updated_habit = habit_update(habit)
        return jsonify(updated_habit.to_dict())
    else:
        """List habits with filtering support"""

        id = request.args.get("id", None, int)
        name = request.args.get("name", None, str)
        description = request.args.get("description", None, str)
        interval = request.args.get("interval", None, datetime)
        lifetime = request.args.get("lifetime", None, datetime)
        active = request.args.get("active", None, bool)
        habits = habit_list(id, name, description, interval, lifetime, active)
        return jsonify([habit.to_dict() for habit in habits])


@app.route("/tasks", methods=["GET", "PATCH"])
def tasks():
    if request.method == "PATCH":
        """Marks a task as completed"""

        data = json.loads(request.data)
        if data.get("id") is None:
            raise ValueError("Task id is None")
        task_complete(data.get("id"))
        return "ok"
    else:
        """List tasks with filtering support"""

        habit_id = request.args.get("habit_id", None, int)
        completed = request.args.get("completed", None, bool)
        start = request.args.get("start", None, datetime)
        end = request.args.get("end", None, datetime)
        tasks = task_list(habit_id, completed, start, end)
        return jsonify([task.to_dict() for task in tasks])


parser = argparse.ArgumentParser(description="Habit Tracker Server")
parser.add_argument("--port", type=int, help="Port to run the server on", default=5000)

args = parser.parse_args()

app.run(debug=True, use_reloader=False, port=args.port)

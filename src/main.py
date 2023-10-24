from flask import Flask, jsonify, request
import json
from db import (
    habit_create,
    habit_delete,
    habit_list,
    habit_update,
    task_complete,
    task_list,
    db,
)
from duration import Duration
from habit import Habit
import argparse
from werkzeug.exceptions import HTTPException
import traceback

app = Flask(__name__)

# Routes


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    """Returns JSON instead of HTML for HTTP errors."""
    if isinstance(e, HTTPException):
        return e

    print(traceback.format_exc())

    return jsonify(message=getattr(e, "message", repr(e))), 400


@app.route("/")
def status():
    """A simple endpoint to verify the reachability of the server"""
    return jsonify(status="ok")


@app.route("/habits", methods=["GET"])
def route_habits_list():
    """List habits with filtering support"""

    id = request.args.get("id", None, str)
    name = request.args.get("name", None, str)
    description = request.args.get("description", None, str)
    interval = request.args.get("interval", None, str)
    interval = Duration(interval) if interval is not None else None
    lifetime = request.args.get("lifetime", None, str)
    lifetime = Duration(lifetime) if lifetime is not None else None
    active = request.args.get("active", None, str)
    active = active.lower() == "true" if active is not None else None
    habits = habit_list(id, name, description, interval, lifetime, active)
    return jsonify([habit.to_dict() for habit in habits])


@app.route("/habits", methods=["POST"])
def route_habits_create():
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


@app.route("/habits", methods=["PUT"])
def route_habits_update():
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


@app.route("/habits", methods=["DELETE"])
def route_habits_delete():
    """Delete a habit"""
    id = request.args.get("id", None, int)
    habit_delete((id,))
    return jsonify({"id": id})


@app.route("/tasks", methods=["GET"])
def route_tasks_list():
    """List tasks with filtering support"""

    habit_id = request.args.get("habit_id", None, str)
    completed = request.args.get("completed", None, str)
    completed = completed.lower() == "true" if completed is not None else None
    start = request.args.get("start", None, str)
    end = request.args.get("end", None, str)
    tasks = task_list(habit_id, completed, start, end)
    return jsonify([task.to_dict() for task in tasks])


@app.route("/tasks", methods=["PATCH"])
def route_tasks_complete():
    """Marks a task as completed"""

    data = json.loads(request.data)
    if data.get("id") is None:
        raise ValueError("Task id is None")
    task_complete(data.get("id"))
    return "ok"


# CLI

parser = argparse.ArgumentParser(description="Habit Tracker Server")
parser.add_argument("--port", type=int, help="Port to run the server on", default=5000)

args = parser.parse_args()

# Run the server

app.run(debug=True, use_reloader=False, port=args.port)

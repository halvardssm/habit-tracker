from flask import Flask, jsonify, request
import json
from db import (
    habit_create,
    habit_delete,
    habit_list,
    habit_update,
    task_complete,
    task_list,
)
from duration import Duration
from habit import Habit
import argparse
from werkzeug.exceptions import HTTPException
import traceback
from utils import not_none

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
    id = data.get("id")
    if id is None:
        raise ValueError("Habit id is None")
    existing_habits = habit_list(id=id)
    if len(existing_habits) < 1:
        raise ValueError(f"Habit with id {id} does not exist")
    existing_habit = existing_habits[0]

    new_habit = Habit(
        id=not_none(data.get("id"), existing_habit.id),
        name=not_none(data.get("name"), existing_habit.name),
        description=not_none(data.get("description"), existing_habit.description),
        interval=not_none(data.get("interval"), existing_habit.interval),
        lifetime=not_none(data.get("lifetime"), existing_habit.lifetime),
        active=not_none(data.get("active"), existing_habit.active),
        start=not_none(data.get("start"), existing_habit.start),
        end=not_none(data.get("end"), existing_habit.end),
    )
    updated_habit = habit_update(new_habit)
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

    id = request.args.get("id", None, int)
    if id is None:
        raise ValueError("Task id is None")
    task_complete(id)
    return jsonify({"id": id})


# CLI

parser = argparse.ArgumentParser(description="Habit Tracker Server")
parser.add_argument("--port", type=int, help="Port to run the server on", default=5000)

args = parser.parse_args()

# Run the server

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=args.port)

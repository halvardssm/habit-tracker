from datetime import datetime
from flask import Flask, jsonify, request
import json
from db import habit_create, habit_list, task_complete, task_list
from habit import Habit

app = Flask(__name__)


@app.route("/")
def hello():
    """A simple endpoint that says hello to verify the reachability of the server"""
    return "Hello, World!"


@app.route("/habits", methods=["GET", "POST"])
def habit():
    """Endpoint to interract with habits"""

    if request.method == "POST":
        """Create a new habit"""

        data = json.loads(request.data)
        habit = Habit(
            name=data["name"],
            description=data["description"],
            interval=data["interval"],
            lifetime=data["lifetime"],
            active=data["active"],
            start=data["start"],
            end=data["end"],
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


app.run(debug=True, use_reloader=False)

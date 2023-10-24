import argparse
from datetime import datetime, timedelta
import requests
from types import SimpleNamespace
from tabulate import tabulate


url_base = "http://127.0.0.1"

# Helper functions


def create_url(
    port: int,
    endpoint: str,
    parameters: dict[str, str | int | bool | None] | None = None,
):
    """Create a url with the given parameters."""
    url = url_base + ":" + str(port) + endpoint
    if parameters is not None:
        url += "?"
        for key, value in parameters.items():
            if value is not None:
                url += key + "=" + str(value) + "&"
        url = url[:-1]
    return url


def print_tabular(data):
    """Helper function for printing the given data in a tabular format."""
    print(tabulate(data, headers="keys"))


def get_streaks_from_tasks(input_list):
    """Get streaks from a list of tasks."""
    streaks = []
    current_streak = None

    input_list.sort(key=lambda x: (x["habit_id"], x["habit_order"]))

    for item in input_list:
        habit_id = item["habit_id"]
        habit_order = item["habit_order"]

        if (
            current_streak is None
            or current_streak["habit_id"] != habit_id
            or habit_order != current_streak["last_habit_order"] + 1
        ):
            if current_streak is not None:
                streaks.append(current_streak)
            current_streak = {
                "streak": 1,
                "ids": [item["id"]],
                "habit_id": habit_id,
                "last_habit_order": habit_order,
            }
        else:
            current_streak["streak"] += 1
            current_streak["ids"].append(item["id"])
            current_streak["last_habit_order"] = habit_order

    if current_streak is not None:
        streaks.append(current_streak)

    for streak in streaks:
        del streak["last_habit_order"]

    return streaks


# HTTP Requests


def req_habits_create(args):
    """HTTP request to create a habit."""
    return requests.post(
        create_url(args.port, "/habits"),
        json={
            "name": args.name,
            "description": args.description,
            "interval": args.interval,
            "lifetime": args.lifetime,
            "active": args.active,
            "start": args.start,
            "end": args.end,
        },
    ).json()


def req_habits_update(args):
    """HTTP request to update a habit."""
    return requests.put(
        create_url(args.port, "/habits"),
        json={
            "name": args.name,
            "description": args.description,
            "interval": args.interval,
            "lifetime": args.lifetime,
            "active": args.active,
            "start": args.start,
            "end": args.end,
        },
    ).json()


def req_habits_list(args):
    """HTTP request to list habits."""
    return requests.get(
        create_url(
            args.port,
            "/habits",
            parameters={
                "id": str(args.id) if args.id is not None else None,
                "name": args.name,
                "description": args.description,
                "interval": args.interval,
                "lifetime": args.lifetime,
                "active": args.active,
            },
        )
    ).json()


def req_tasks_list(args):
    """HTTP request to list tasks."""
    return requests.get(
        create_url(
            args.port,
            "/tasks",
            parameters={
                "habit_id": args.habit_id,
                "completed": args.completed,
                "start": args.start,
                "end": args.end,
            },
        )
    ).json()


def req_tasks_complete(args):
    """HTTP request to complete a task."""
    return requests.patch(
        create_url(args.port, "/tasks"),
        json={
            "id": args.id,
        },
    ).json()


# Functions using HTTP requests


def tasks_active(args):
    """Function to get active tasks."""
    tasks = req_tasks_list(
        SimpleNamespace(
            port=args.port,
            habit_id=None,
            completed=False,
            start="<" + datetime.now().isoformat(),
            end=">" + datetime.now().isoformat(),
        )
    )

    return map_habits_to_tasks(tasks)


def map_habits_to_tasks(tasks):
    """Map habits to tasks."""

    if len(tasks) < 1:
        return tasks

    habit_ids = [element["habit_id"] for element in tasks]
    habits = req_habits_list(
        SimpleNamespace(
            port=args.port,
            id="*in(" + ",".join([str(id) for id in habit_ids]) + ")",
            name=None,
            description=None,
            interval=None,
            lifetime=None,
            active=True,
        )
    )

    def map_habit_to_task(task: dict):
        habit = [x for x in habits if x["id"] == task["habit_id"]][0]
        task["name"] = habit["name"]
        task["description"] = habit["description"]
        return task

    return list(map(map_habit_to_task, tasks))


def list_task_streaks(args):
    """List task streaks."""
    tasks = req_tasks_list(
        SimpleNamespace(
            port=args.port, habit_id=args.habit_id, completed=True, start=None, end=None
        )
    )

    return get_streaks_from_tasks(tasks)


def analytics(args):
    """Query analytics."""
    if args.type == "list_current_habits":
        data = req_habits_list(
            SimpleNamespace(
                port=args.port,
                id=None,
                name=None,
                description=None,
                interval=args.interval,
                lifetime=None,
                active=True,
            )
        )
        print_tabular(data)

    elif args.type == "list_longest_streaks":
        data = list_task_streaks(args)
        print_tabular(data)

    elif args.type == "get_longest_streak":
        data = list_task_streaks(args)
        data.sort(key=lambda x: x["streak"], reverse=True)
        print_tabular([data[0]])

    else:
        raise ValueError("Unknown analytics type")


# CLI

parser = argparse.ArgumentParser(description="Habit Tracker CLI")
parser.add_argument("--port", type=int, help="Port of the server", default=5000)
parser.set_defaults(func=lambda args: parser.print_help())


subparsers = parser.add_subparsers(
    title="subcommands", description="available sub-commands"
)

# Create subparsers for each command


def assign_subparser_habits_create():
    """Assign subparser for habits:create."""
    subparser = subparsers.add_parser("habits:create", help="Create a new habit")
    subparser.add_argument(
        "--name", type=str, help="The name of the habit to create", required=True
    )
    subparser.add_argument(
        "--description",
        type=str,
        help="The description of the habit to create",
        required=True,
    )
    subparser.add_argument(
        "--interval",
        type=str,
        help="The interval of the habit to create, must follow ISO8601 duration standard (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. P1Y",
        required=True,
    )
    subparser.add_argument(
        "--lifetime",
        type=str,
        help="The lifetime of the habit to create, must follow ISO8601 duration standard (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. PT1H",
        required=True,
    )
    subparser.add_argument(
        "--active",
        type=bool,
        help="The active of the habit to create, boolean, default false",
        default=True,
    )
    subparser.add_argument(
        "--start",
        type=str,
        help="The start of the habit to create, iso format, default now",
        default=datetime.now().isoformat(),
    )
    subparser.add_argument(
        "--end",
        type=str,
        help="The end of the habit to create, iso format, default 1 year from now",
        default=(datetime.now() + timedelta(days=365)).isoformat(),
    )
    subparser.set_defaults(func=lambda args: print_tabular(req_habits_create(args)))


def assign_subparser_habits_list():
    """Assign subparser for habits:list."""
    subparser = subparsers.add_parser("habits:list", help="List habits")
    subparser.add_argument("--id", type=int, help="Filter by id")
    subparser.add_argument("--name", type=str, help="Filter by name")
    subparser.add_argument("--description", type=str, help="Filter by description")
    subparser.add_argument("--interval", type=str, help="Filter by interval")
    subparser.add_argument("--lifetime", type=str, help="Filter by lifetime")
    subparser.add_argument("--active", type=bool, help="Filter by active")
    subparser.add_argument(
        "--start",
        type=str,
        help="Filter by start date, can use < or > to filter, e.g. >2021-10-19T13:43:12",
    )
    subparser.add_argument(
        "--end",
        type=str,
        help="Filter by end date, can use < or > to filter, e.g. >2021-10-19T13:43:12",
    )
    subparser.set_defaults(func=lambda args: print_tabular(req_habits_list(args)))


def assign_subparser_tasks_list():
    """Assign subparser for tasks:list."""
    subparser = subparsers.add_parser("tasks:list", help="List tasks")
    subparser.add_argument("--habit_id", type=int, help="Filter by habit id")
    subparser.add_argument("--completed", type=bool, help="Filter by completed")
    subparser.add_argument("--start", type=str, help="Filter by start date")
    subparser.add_argument("--end", type=str, help="Filter by end date")
    subparser.set_defaults(func=lambda args: print_tabular(req_tasks_list(args)))


def assign_subparser_tasks_active():
    """Assign subparser for tasks:active."""
    subparser = subparsers.add_parser(
        "tasks:active", help="List tasks that are active and can be completed"
    )
    subparser.set_defaults(func=lambda args: print_tabular(tasks_active(args)))


def assign_subparser_tasks_complete():
    """Assign subparser for tasks:complete."""
    subparser = subparsers.add_parser("tasks:complete", help="Complete a task")
    subparser.add_argument("--id", type=int, help="The id of the task to complete")
    subparser.set_defaults(func=lambda args: req_tasks_complete(tasks_active(args)))


def assign_subparser_analytics():
    """Assign subparser for analytics."""
    choices = {
        "list_current_habits": "List current (active) habits (can be filtered by interval)",
        "list_longest_streaks": "List longest streaks (can be filtered by habit_id)",
        "get_longest_streak": "Get longest streak (can be filtered by habit_id)",
    }

    subparser = subparsers.add_parser(
        "analytics",
        help="Query analytics. You can already get a lot of information using the list commands, but this is a central analytics helper.",
    )
    help_text = "The type of analytics to query. The following options are possible:"
    for key, value in choices.items():
        help_text += "\n" + key + ": " + value + ";"
    subparser.add_argument(
        "type",
        choices=choices.keys(),
        help=help_text,
    )
    subparser.add_argument(
        "--interval", type=str, help="The interval to filter by, e.g. P1Y"
    )
    subparser.add_argument("--habit_id", type=int, help="The habit id to filter by")
    subparser.set_defaults(func=lambda args: analytics(args))


assign_subparser_habits_create()
assign_subparser_habits_list()
assign_subparser_tasks_list()
assign_subparser_tasks_active()
assign_subparser_tasks_complete()
assign_subparser_analytics()

# Parse arguments and call the function

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)

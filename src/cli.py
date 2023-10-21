import argparse
from datetime import datetime, timedelta
import requests


url_base = "http://127.0.0.1"


def create_url(
    port: int,
    endpoint: str,
    parameters: dict[str, str | int | bool | None] | None = None,
):
    url = url_base + ":" + str(port) + endpoint
    if parameters is not None:
        url += "?"
        for key, value in parameters.items():
            if value is not None:
                url += key + "=" + str(value) + "&"
        url = url[:-1]
    return url


def habit_create(args):
    print(args)
    r = requests.post(
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
    )
    print(r.status_code)
    print(r.text)


def habit_list(args):
    r = requests.get(
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
    )
    print(r.status_code)
    print(r.text)


def task_list(args):
    r = requests.get(
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
    )
    print(r.status_code)
    print(r.text)


def task_complete(args):
    r = requests.patch(
        create_url(args.port, "/tasks"),
        json={
            "id": args.id,
        },
    )
    print(r.status_code)
    print(r.text)


parser = argparse.ArgumentParser(description="Habit Tracker CLI")
parser.add_argument("--port", type=int, help="Port of the server", default=5000)
parser.set_defaults(func=lambda args: parser.print_help())

subparsers = parser.add_subparsers(
    title="subcommands", description="available sub-commands"
)

parser_habit_create = subparsers.add_parser("habit:create", help="Create a new habit")
parser_habit_create.add_argument(
    "--name", type=str, help="The name of the habit to create", required=True
)
parser_habit_create.add_argument(
    "--description",
    type=str,
    help="The description of the habit to create",
    required=True,
)
parser_habit_create.add_argument(
    "--interval",
    type=str,
    help="The interval of the habit to create, must follow ISO8601 duration standard (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. P1Y",
    required=True,
)
parser_habit_create.add_argument(
    "--lifetime",
    type=str,
    help="The lifetime of the habit to create, must follow ISO8601 duration standard (P[n]Y[n]M[n]DT[n]H[n]M[n]S), e.g. PT1H",
    required=True,
)
parser_habit_create.add_argument(
    "--active",
    type=bool,
    help="The active of the habit to create, boolean, default false",
    default=True,
)
parser_habit_create.add_argument(
    "--start",
    type=str,
    help="The start of the habit to create, iso format, default now",
    default=datetime.now().isoformat(),
)
parser_habit_create.add_argument(
    "--end",
    type=str,
    help="The end of the habit to create, iso format, default 1 year from now",
    default=(datetime.now() + timedelta(days=365)).isoformat(),
)
parser_habit_create.set_defaults(func=habit_create)

parser_habit_list = subparsers.add_parser("habit:list", help="List habits")
parser_habit_list.add_argument("--id", type=int, help="Filter by id")
parser_habit_list.add_argument("--name", type=str, help="Filter by name")
parser_habit_list.add_argument("--description", type=str, help="Filter by description")
parser_habit_list.add_argument("--interval", type=str, help="Filter by interval")
parser_habit_list.add_argument("--lifetime", type=str, help="Filter by lifetime")
parser_habit_list.add_argument("--active", type=bool, help="Filter by active")
parser_habit_list.add_argument("--start", type=str, help="Filter by start date")
parser_habit_list.add_argument("--end", type=str, help="Filter by end date")
parser_habit_list.set_defaults(func=habit_list)

parser_habit_list = subparsers.add_parser("task:list", help="List tasks")
parser_habit_list.add_argument("--habit_id", type=int, help="Filter by habit id")
parser_habit_list.add_argument("--completed", type=bool, help="Filter by completed")
parser_habit_list.add_argument("--start", type=str, help="Filter by start date")
parser_habit_list.add_argument("--end", type=str, help="Filter by end date")
parser_habit_list.set_defaults(func=task_list)

parser_habit_list = subparsers.add_parser("task:complete", help="Complete a task")
parser_habit_list.add_argument("--id", type=int, help="The id of the task to complete")
parser_habit_list.set_defaults(func=task_complete)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)

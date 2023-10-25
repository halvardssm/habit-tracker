import sqlite3
from datetime import datetime
from duration import Duration
from habit import Habit
from task import Task


con = sqlite3.connect("database.db", check_same_thread=False)
db = con.cursor()

# Create tables if not exists
db.execute(
    """CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    interval TEXT NOT NULL,
    lifetime TEXT NOT NULL,
    active INTEGER NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL
)"""
)
db.execute(
    """CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    habit_order INTEGER NOT NULL,
    completed INTEGER NOT NULL,
    completed_at TEXT,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
)"""
)


def add_filters_to_query(query: str, filters: dict[str, str]) -> tuple[str, list[str]]:
    """Adds filters to a query"""

    if len(filters) == 0:
        return query

    params = []
    query += " WHERE"
    for key, value in filters.items():
        if value == None:
            continue

        if isinstance(value, str):
            if value.startswith("<"):
                query += f" {key} < ? AND"
                params.append(value[1:])
                continue
            if value.startswith(">"):
                query += f" {key} > ? AND"
                params.append(value[1:])
                continue
            if value.startswith("*in(") and value.endswith(")"):
                query += (
                    f" {key} in ({','.join(['?' for _ in value[4:-1].split(',')])}) AND"
                )
                params.extend(value[4:-1].split(","))
                continue

        query += f" {key} = ? AND"
        params.append(value)

    return query[:-4], params


# Habits


def habit_create(habit: Habit, start_time: datetime | None = None):
    """Creates a habit in the database"""

    db.execute(
        """INSERT INTO habits (
            name, 
            description, 
            interval, 
            lifetime,
            active, 
            start,
            end
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            habit.name,
            habit.description,
            habit.interval.duration_str,
            habit.lifetime.duration_str,
            habit.active,
            habit.start.isoformat(),
            habit.end.isoformat(),
        ),
    )
    con.commit()
    habit.id = db.lastrowid

    create_tasks_for_habit(habit, start_time=start_time)


def habit_update(habit: Habit):
    """Updates a habit in the database"""

    if habit.id is None:
        raise ValueError("Habit id is None")

    db.execute(
        """UPDATE habits SET 
            name = ?,
            description = ?,
            interval = ?,
            lifetime = ?,
            active = ?
        WHERE id = ?""",
        (
            habit.name,
            habit.description,
            habit.interval.duration_str,
            habit.lifetime.duration_str,
            habit.active,
            habit.id,
        ),
    )

    db.execute(
        """DELETE FROM tasks WHERE id IN (SELECT id FROM tasks WHERE habit_id = ? AND start > ?)""",
        (
            habit.id,
            datetime.now().isoformat(),
        ),
    )

    con.commit()

    db.execute("""SELECT habit_order FROM tasks ORDER BY habit_order DESC LIMIT 1""")

    habit_order_no = db.fetchone()[0]

    create_tasks_for_habit(habit, habit_order_no)

    return habit_list(id=habit.id)[0]


def habit_list(
    id: int | None = None,
    name: str | None = None,
    description: str | None = None,
    interval: Duration | None = None,
    lifetime: Duration | None = None,
    active: bool | None = None,
) -> list[Habit]:
    """Lists habits with filtering support"""

    query, params = add_filters_to_query(
        "SELECT * FROM habits",
        {
            "id": id,
            "name": name,
            "description": description,
            "interval": interval.duration_str if interval is not None else None,
            "lifetime": lifetime.duration_str if lifetime is not None else None,
            "active": active,
        },
    )

    db.execute(query, params)

    habits = db.fetchall()

    return [
        Habit(
            id=habit[0],
            name=habit[1],
            description=habit[2],
            interval=habit[3],
            lifetime=habit[4],
            active=bool(habit[5]),
            start=habit[6],
            end=habit[7],
        )
        for habit in habits
    ]


def habit_delete(ids: tuple[int]):
    """Deletes a Habit from the database"""

    query = "DELETE FROM habits WHERE id in (" + ",".join(["?" for _ in ids]) + ")"

    db.execute(
        query,
        ids,
    )
    con.commit()

    task_delete_by_habit(ids)


# Tasks


def task_create(task: Task):
    """Creates a task in the database"""

    db.execute(
        """INSERT INTO tasks (
            habit_id, 
            habit_order,
            completed, 
            start, 
            end
        ) VALUES (?, ?, ?, ?, ?)""",
        (
            task.habit_id,
            task.habit_order,
            task.completed,
            task.start.isoformat(),
            task.end.isoformat(),
        ),
    )
    con.commit()
    task.id = db.lastrowid


def task_complete(task_id: int):
    """Marks a task as completed"""

    db.execute(
        """UPDATE tasks SET completed = 1, completed_at = ? WHERE id = ?""",
        (datetime.now(), task_id),
    )
    con.commit()


def task_list(
    habit_id: int | None = None,
    completed: bool | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[Task]:
    """Lists tasks with filtering support"""

    query, params = add_filters_to_query(
        "SELECT * FROM tasks",
        {"habit_id": habit_id, "completed": completed, "start": start, "end": end},
    )

    db.execute(query, params)

    tasks = db.fetchall()

    return [
        Task(
            id=task[0],
            habit_id=task[1],
            habit_order=task[2],
            completed=bool(task[3]),
            completed_at=task[4],
            start=task[5],
            end=task[6],
        )
        for task in tasks
    ]


def task_delete_by_habit(habit_ids: tuple[int]):
    """Deletes Tasks from the database"""

    query = (
        "DELETE FROM tasks WHERE habit_id in ("
        + ",".join(["?" for _ in habit_ids])
        + ")"
    )

    db.execute(
        query,
        habit_ids,
    )

    con.commit()


def create_tasks_for_habit(
    habit: Habit, habit_order_no: int = 0, start_time: datetime | None = None
):
    """Creates tasks for a habit. If start_time is provided, tasks will be created from that time onwards.
    Otherwise, tasks will be created from the habit's start time onwards.
    If habit_order_no is provided, tasks will be created from that order onwards.
    """
    current = (
        start_time
        if start_time is not None and (start_time >= habit.start)
        else habit.start
    )
    current_order = habit_order_no + 1
    while current < habit.end:
        task_create(
            Task(
                habit_id=habit.id,
                habit_order=current_order,
                completed=False,
                start=current,
                end=current + habit.lifetime.duration,
            )
        )
        current += habit.interval.duration
        current_order += 1

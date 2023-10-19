import sqlite3
from datetime import datetime
from duration import Duration
from habit import Habit
from task import Task


con = sqlite3.connect("database.db")
db = con.cursor()

# Create table if not exists
db.execute(
    """CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    interval TEXT NOT NULL,
    lifetime TEXT NOT NULL,
    active INTEGER NOT NULL,
    created_at TEXT NOT NULL,
)"""
)
db.execute(
    """CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    completed INTEGER NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    FOREIGN KEY(habit_id) REFERENCES habits(id)
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
        query += f" {key} = ? AND"
        params.append(value)

    return query[:-4], params


# Habits


def habit_create(habit: Habit):
    """Creates a habit in the database"""

    created_at = datetime.now()
    db.execute(
        """INSERT INTO habits (
            name, 
            description, 
            interval, 
            lifetime,
            active, 
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?)""",
        (
            habit.name,
            habit.description,
            habit.interval,
            habit.lifetime,
            habit.active,
            created_at.isoformat(),
        ),
    )
    con.commit()
    habit.id = db.lastrowid
    habit.created_at = created_at


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
            habit.interval,
            habit.lifetime,
            habit.active,
            habit.id,
        ),
    )
    con.commit()


def habit_get(habit_id: int) -> Habit:
    db.execute(
        """SELECT * FROM habits WHERE id = ?""",
        (habit_id,),
    )
    habit = db.fetchone()
    if habit is None:
        raise ValueError(f"Habit with id {habit_id} not found")
    return Habit(
        id=habit[0],
        name=habit[1],
        description=habit[2],
        interval=habit[3],
        lifetime=habit[4],
        active=habit[5],
        created_at=datetime.fromisoformat(habit[6]),
    )


def habit_list(
    name: str | None = None,
    description: str | None = None,
    interval: Duration | None = None,
    lifetime: Duration | None = None,
    active: bool | None = None,
) -> list[Habit]:
    query, params = add_filters_to_query(
        "SELECT * FROM habits", {name, description, interval, lifetime, active}
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
            active=habit[5],
            created_at=datetime.fromisoformat(habit[6]),
        )
        for habit in habits
    ]


# Tasks


def task_create(task: Task):
    db.execute(
        """INSERT INTO tasks (
            habit_id, 
            completed, 
            start, 
            end,
        ) VALUES (?, ?, ?, ?)""",
        (
            task.habit_id,
            task.completed,
            task.start,
            task.end,
        ),
    )
    con.commit()
    task.id = db.lastrowid


def task_complete(task_id: int):
    db.execute(
        """UPDATE tasks SET completed = 1 WHERE id = ?""",
        (task_id),
    )
    con.commit()


def task_list(
    habit_id: int | None = None,
    completed: bool | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[Task]:
    query, params = add_filters_to_query(
        "SELECT * FROM tasks", {habit_id, completed, start, end}
    )

    db.execute(query, params)

    tasks = db.fetchall()

    return [
        Task(
            id=task[0],
            habit_id=task[1],
            completed=task[2],
            start=task[3],
            end=task[4],
        )
        for task in tasks
    ]

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
    completed INTEGER NOT NULL,
    start TEXT NOT NULL,
    end TEXT NOT NULL,
    FOREIGN KEY(habit_id) REFERENCES habits(id)
)"""
)

# Habits


def habit_create(habit: Habit):
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

    con.commit()

    return habit_list(id=habit.id)[0]


def habit_list(
    id: int | None = None,
) -> list[Habit]:
    """Lists habits with filtering support"""

    if id is not None:
        query = "SELECT * FROM habits WHERE id = ?"
        params = (id,)
    else:
        query = "SELECT * FROM habits"
        params = None

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


# Tasks


def task_create(task: Task):
    """Creates a task in the database"""

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
            task.start.isoformat(),
            task.end.isoformat(),
        ),
    )
    con.commit()
    task.id = db.lastrowid


def task_complete(task_id: int):
    """Marks a task as completed"""

    db.execute(
        """UPDATE tasks SET completed = 1 WHERE id = ?""",
        (task_id),
    )
    con.commit()


def task_list(
    habit_id: int | None = None,
) -> list[Task]:
    """Lists tasks with filtering support"""

    if habit_id is not None:
        query = "SELECT * FROM tasks WHERE habit_id = ?"
        params = (habit_id,)
    else:
        query = "SELECT * FROM tasks"
        params = None

    db.execute(query, params)

    tasks = db.fetchall()

    return [
        Task(
            id=task[0],
            habit_id=task[1],
            completed=bool(task[2]),
            start=task[3],
            end=task[4],
        )
        for task in tasks
    ]


if len(habit_list()) < 1:
    """Seeds default habits if none exist"""
    
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, 8, 0, 0)
    end = datetime(now.year+1, now.month+2, now.day+3, 22, 0, 0)
    habit_create(
        Habit(
            name="Drink Water",
            description="Drink 1 glass of water",
            interval=Duration("4h"),
            lifetime=Duration("5h"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Exercise",
            description="Exercise for 30 minutes",
            interval=Duration("1d"),
            lifetime=Duration("1d"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Read",
            description="Read for 30 minutes",
            interval=Duration("1d"),
            lifetime=Duration("12h"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Meditate",
            description="Meditate for 10 minutes",
            interval=Duration("5h"),
            lifetime=Duration("5h"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Sleep",
            description="Sleep for 8 hours",
            interval=Duration("1d"),
            lifetime=Duration("1d"),
            active=True,
            start=start,
            end=end,
        )
    )

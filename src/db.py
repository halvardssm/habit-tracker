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

    create_tasks_for_habit(habit)


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

    create_tasks_for_habit(habit)

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
            "interval": interval,
            "lifetime": lifetime,
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


# Tasks


def task_create(task: Task):
    """Creates a task in the database"""

    db.execute(
        """INSERT INTO tasks (
            habit_id, 
            completed, 
            start, 
            end
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
        (task_id,),
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
            completed=bool(task[2]),
            start=task[3],
            end=task[4],
        )
        for task in tasks
    ]


def create_tasks_for_habit(habit: Habit, start_time: datetime = datetime.now()):
    # itterate over the start to end using interval as the accumulator of the habit and create tasks
    # for each interval
    current = (
        start_time
        if start_time is not None and (start_time > habit.start)
        else habit.start
    )
    while current < habit.end:
        task_create(
            Task(
                habit_id=habit.id,
                completed=False,
                start=current,
                end=current + habit.lifetime.duration,
            )
        )
        current += habit.interval.duration


if len(habit_list()) < 1:
    """Seeds default habits if none exist"""

    now = datetime.now()
    start = datetime(now.year, now.month, now.day, 8, 0, 0)
    end = datetime(now.year + 1, now.month + 2, now.day + 3, 22, 0, 0)
    habit_create(
        Habit(
            name="Drink Water",
            description="Drink 1 glass of water",
            interval=Duration("PT4H"),
            lifetime=Duration("PT5H"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Exercise",
            description="Exercise for 30 minutes",
            interval=Duration("P1D"),
            lifetime=Duration("P1D"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Read",
            description="Read for 30 minutes",
            interval=Duration("P1D"),
            lifetime=Duration("PT12H"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Meditate",
            description="Meditate for 10 minutes",
            interval=Duration("PT5H"),
            lifetime=Duration("PT5H"),
            active=True,
            start=start,
            end=end,
        )
    )

    habit_create(
        Habit(
            name="Sleep",
            description="Sleep for 8 hours",
            interval=Duration("P1D"),
            lifetime=Duration("P1D"),
            active=True,
            start=start,
            end=end,
        )
    )

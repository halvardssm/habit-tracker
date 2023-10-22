from datetime import datetime


class Task:
    """A class representing a task"""

    id: int | None
    habit_id: int
    start: datetime
    end: datetime
    completed: bool

    def __init__(
        self,
        habit_id: int,
        start: datetime | str,
        end: datetime | str,
        completed: bool = False,
        id: int | None = None,
    ):
        """Initializes the class with validation"""

        if not isinstance(habit_id, int):
            raise TypeError("name must be a int")
        self.habit_id = habit_id

        if isinstance(start, datetime):
            self.start = start
        elif isinstance(start, str):
            self.start = datetime.fromisoformat(start)
        else:
            raise TypeError("start must be a datetime or string")

        if isinstance(end, datetime):
            self.end = end
        elif isinstance(end, str):
            self.end = datetime.fromisoformat(end)
        else:
            raise TypeError("end must be a datetime or string")

        if completed is not True and completed is not False:
            raise TypeError("completed must be a boolean")
        self.completed = completed

        if isinstance(id, int):
            self.id = id
        elif id is not None:
            raise TypeError("id must be an int or None")
        else:
            self.id = None

    def to_dict(self):
        """Converts the class to a dictionary"""

        return {
            "id": self.id,
            "habit_id": self.habit_id,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "completed": self.completed,
        }

from duration import Duration
from habit import Habit


class Task:
    """A class representing a task"""

    def __init__(
        self,
        habit_id: Habit["id"],
        start: None,
        end: None,
        completed: bool = False,
        id: None = None,
    ):
        self.habit_id = habit_id
        self.start = start
        self.end = end
        self.completed = completed
        self.id = id

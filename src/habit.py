from datetime import datetime
from duration import Duration


class Habit:
    """A class representing a habit"""

    id: int | None
    name: str
    description: str
    interval: Duration
    lifetime: Duration
    active: bool
    start: datetime
    end: datetime

    def __init__(
        self,
        name: str,
        description: str,
        interval: Duration | str,
        lifetime: Duration | str,
        start: datetime | str,
        end: datetime | str,
        active: bool = True,
        id: int | None = None,
    ):
        """Initializes the class with validation"""

        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.name = name

        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self.description = description

        if isinstance(interval, Duration):
            self.interval = interval
        else:
            self.interval = Duration(interval)

        if isinstance(lifetime, Duration):
            self.lifetime = lifetime
        else:
            self.lifetime = Duration(lifetime)

        if active is not True and active is not False:
            raise TypeError("active must be a boolean")
        self.active = active

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
            "name": self.name,
            "description": self.description,
            "interval": self.interval.duration_str,
            "lifetime": self.lifetime.duration_str,
            "active": self.active,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }

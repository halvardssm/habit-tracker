from duration import Duration


class Habit:
    """A class representing a habit"""

    def __init__(
        self,
        name: str,
        description: str,
        interval: Duration,
        lifetime: Duration,
        active: bool = True,
        created_at: None = None,
        id: None = None,
    ):
        self.name = name
        self.description = description
        self.interval = interval
        self.lifetime = lifetime
        self.active = active
        self.created_at = created_at
        self.id = id

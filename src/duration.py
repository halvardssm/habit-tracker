from datetime import datetime
import isodate


class Duration:
    """A class representing a duration"""

    def __init__(self, duration: str, start_time: datetime = datetime.now()):
        self.duration = isodate.parse_duration(duration)
        self.duration_str = duration
        self.start_time = start_time

    def find_next_instance(self, current_time: datetime = datetime.now()) -> datetime:
        """Calculates the next instance"""

        next_instance = self.start_time
        while next_instance <= current_time:
            next_instance += self.duration

        return next_instance

    def __str__(self):
        return str(self.duration_str)

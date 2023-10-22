import unittest
from datetime import datetime, timedelta
from duration import Duration
from habit import Habit


class TestHabit(unittest.TestCase):
    def test_class_habit_simple(self):
        """Test the Habit class with valid parameters"""

        habit1 = Habit(
            name="testName",
            description="testDescription",
            interval="P1D",
            lifetime="P1D",
            start="2023-10-19T13:43:12",
            end="2023-10-20T13:43:12",
            active=False,
            id=1,
        )
        self.assertEqual(
            habit1.to_dict(),
            {
                "id": 1,
                "name": "testName",
                "description": "testDescription",
                "interval": "P1D",
                "lifetime": "P1D",
                "start": "2023-10-19T13:43:12",
                "end": "2023-10-20T13:43:12",
                "active": False,
            },
        )

        habit2 = Habit(
            name="testName",
            description="testDescription",
            interval=Duration("P1D"),
            lifetime=Duration("P1D"),
            start=datetime(2023, 10, 19, 13, 43, 12),
            end=datetime(2023, 10, 20, 13, 43, 12),
        )
        self.assertEqual(
            habit2.to_dict(),
            {
                "id": None,
                "name": "testName",
                "description": "testDescription",
                "interval": "P1D",
                "lifetime": "P1D",
                "start": "2023-10-19T13:43:12",
                "end": "2023-10-20T13:43:12",
                "active": True,
            },
        )


if __name__ == "__main__":
    unittest.main()

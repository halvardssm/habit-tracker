import unittest
from datetime import datetime
from task import Task


class TestTask(unittest.TestCase):
    def test_class_task_simple(self):
        """Test the Task class with valid parameters"""

        task1 = Task(
            habit_id=1,
            start="2023-10-19T13:43:12",
            end="2023-10-20T13:43:12",
            completed=False,
            id=1,
        )
        self.assertEqual(
            task1.to_dict(),
            {
                "id": 1,
                "habit_id": 1,
                "start": "2023-10-19T13:43:12",
                "end": "2023-10-20T13:43:12",
                "completed": False,
            },
        )

        task2 = Task(
            habit_id=1,
            start=datetime(2023, 10, 19, 13, 43, 12),
            end=datetime(2023, 10, 20, 13, 43, 12),
        )
        self.assertEqual(
            task2.to_dict(),
            {
                "id": None,
                "habit_id": 1,
                "start": "2023-10-19T13:43:12",
                "end": "2023-10-20T13:43:12",
                "completed": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
